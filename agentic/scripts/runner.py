"""
Core runner functions for executing Claude on Lean tasks.
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, List, Literal

from .task import TaskMetadata, TaskResult
from .lean_checker import find_lean_files, check_lean_files_parallel
from .mcp_stats import analyze_mcp_log, get_mcp_log_path
from .statement_tracker import StatementTracker, RoundResult
from .failure_memory import (
    extract_experience_triples,
    FailureMemory,
    analyze_round_log,
    generate_directions,
)
from .failure_memory.analyzer import compute_tool_usage_stats

# Enable line buffering for real-time output when redirecting to file
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Match END_REASON:{reason} on a single line
PAT_REASON = re.compile(r"(?m)^\s*END_REASON:(LIMIT|COMPLETE|SELECTED_TARGET_COMPLETE)\s*$", re.I)


def get_line_counts(files: List[Path]) -> dict:
    """Get line counts for files. Returns {filename: line_count}."""
    counts = {}
    for f in files:
        try:
            counts[f.name] = sum(1 for _ in open(f, encoding="utf-8"))
        except Exception:
            counts[f.name] = 0
    return counts


def run_claude_once(
    args: List[str],
    env: Optional[dict] = None,
    cwd: Optional[Path] = None,
) -> tuple[str, Optional[str], int]:
    """
    Execute a single claude command.

    Args:
        args: Claude command arguments list
        env: Environment variables (MCP_LOG_NAME should be set here)
        cwd: Working directory

    Returns:
        (stdout, end_reason, returncode)
        end_reason: "COMPLETE" | "LIMIT" | None
    """
    kwargs = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "universal_newlines": True,
        "bufsize": 1,
    }
    if env:
        kwargs["env"] = env
    if cwd:
        kwargs["cwd"] = str(cwd)

    is_stream_json = "--output-format" in args and "stream-json" in args
    output_chars = []

    try:
        cp = subprocess.Popen(args, **kwargs)
        if cp.stdout is not None:
            while True:
                line = cp.stdout.readline()
                if not line and cp.poll() is not None:
                    break
                if line:
                    output_chars.append(line)
                    if is_stream_json:
                        try:
                            data = json.loads(line)
                            event_type = data.get("type", "")
                            if event_type == "message_chunk" and "text" in data:
                                sys.stdout.write(data["text"])
                                sys.stdout.flush()
                            elif event_type == "tool_call":
                                tool_name = data.get("tool_name", "UNKNOWN_TOOL")
                                sys.stdout.write(f"\n[Tool Use: {tool_name}]\n")
                                sys.stdout.flush()
                            elif event_type == "error":
                                sys.stdout.write(f"\n[Claude Error: {data.get('error', '')}]\n")
                                sys.stdout.flush()
                        except:
                            if not line.strip().startswith("{"):
                                sys.stdout.write(line)
                                sys.stdout.flush()
                    else:
                        sys.stdout.write(line)
                        sys.stdout.flush()
        
        cp.wait()
        out = "".join(output_chars)
        m = PAT_REASON.search(out)
        reason = m.group(1).upper() if m else None
        return out, reason, cp.returncode
    except Exception as e:
        print(f"[error] run_claude_once failed: {e}")
        return "", None, 1


def commit_round(round_num: int, cwd: Optional[Path] = None):
    """Create a git commit after a round."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    msg = f"[{timestamp}]_claude_round_{round_num:02d}"
    kwargs = {"cwd": str(cwd)} if cwd else {}
    try:
        subprocess.run(["git", "add", "-A"], check=True, **kwargs)
        subprocess.run(["git", "commit", "-m", msg], check=True, **kwargs)
        print(f"[info] Committed: {msg}")
    except subprocess.CalledProcessError as e:
        print(f"[warn] Round {round_num}: git commit failed - {e} (possibly no changes to commit)")
    except Exception as e:
        print(f"[error] Round {round_num}: unexpected error during git commit - {e}")


def run_claude_session(
    prompt: str,
    cwd: Optional[Path] = None,
    permission_mode: str = "bypassPermissions",
    output_format: Optional[str] = None,
    max_rounds: int = 20,
    sleep_between_rounds: float = 1.0,
    env: Optional[dict] = None,
    on_complete: Optional[Callable[[], bool]] = None,
    tracker: Optional[StatementTracker] = None,
    on_statement_change: Literal["error", "warn"] = "warn",
    git_commit_dir: Optional[Path] = None,
    result_dir: Optional[Path] = None,
    task_id: Optional[str] = None,
    files_to_track: Optional[List[Path]] = None,
    use_failure_memory: bool = False,
    mcp_config: Optional[Path] = None,
    model: Optional[str] = None,
    effort: Optional[str] = None,
    disallowed_tools: Optional[List[str]] = None,
) -> tuple[str, int, List[RoundResult]]:
    """
    Run a complete Claude session with automatic continue logic.

    Args:
        prompt: Initial prompt (provided by user)
        cwd: Working directory
        permission_mode: Permission mode
        output_format: Output format (json / None)
        max_rounds: Maximum rounds
        sleep_between_rounds: Sleep between rounds
        env: Environment variables (MCP_LOG_NAME should be set here)
        on_complete: Callback when COMPLETE is received, returns False to resend prompt
        tracker: Statement tracker for detecting changes
        on_statement_change: Action on statement change ("error" to stop, "warn" to continue)
        git_commit_dir: Directory to create git commits in (default: None, no commits)
        result_dir: Directory to save round results immediately (default: None, no immediate save)
        task_id: Task ID for organizing result files

    Returns:
        (end_reason, rounds_used, round_results)
    """
    print(f"[info] Using prompt:\n{prompt[:120]}{'...' if len(prompt) > 120 else ''}\n")

    # Build base command
    # NOTE: --mcp-config is variadic (<configs...>), so it must appear before
    # other flags to prevent the prompt text from being consumed as a config path.
    base = ["claude", "-p"]
    if model:
        base += ["--model", model]
    if mcp_config:
        base += ["--strict-mcp-config", "--mcp-config", str(mcp_config)]
        print(f"[info] MCP isolation enabled: only servers from {mcp_config}")
    if output_format:
        base += ["--output-format", output_format]
        if output_format == "stream-json":
            base += ["--verbose"]
    if permission_mode:
        base += ["--permission-mode", permission_mode]
    if effort:
        base += ["--effort", effort]
    if disallowed_tools:
        base += ["--disallowedTools"] + disallowed_tools

    round_results: List[RoundResult] = []
    statement_error = False
    initial_line_counts = get_line_counts(files_to_track) if files_to_track else {}

    def record_round(round_num: int, stdout: str, reason: Optional[str], returncode: int, duration: float) -> RoundResult:
        """Record a round result and check for statement changes."""
        nonlocal statement_error

        changes = tracker.check() if tracker else []
        line_counts = get_line_counts(files_to_track) if files_to_track else {}

        result = RoundResult(
            round_number=round_num,
            stdout=stdout,
            end_reason=reason,
            returncode=returncode,
            statement_changes=changes,
            duration_seconds=duration,
            line_counts=line_counts,
        )
        round_results.append(result)

        # Handle statement changes
        if changes:
            if on_statement_change == "error":
                print(f"\n[error] Statement changed in round {round_num}! Stopping.")
                for c in changes:
                    print(f"  {c}")
                statement_error = True
            else:
                print(f"\n[warn] Statement changed in round {round_num}:")
                for c in changes:
                    print(f"  {c}")

        # Print line count changes
        if line_counts and initial_line_counts:
            # vs initial
            init_changes = []
            for filename, current in line_counts.items():
                if filename in initial_line_counts:
                    diff = current - initial_line_counts[filename]
                    if diff != 0:
                        ratio = diff / initial_line_counts[filename] * 100 if initial_line_counts[filename] > 0 else 0
                        init_changes.append((filename, initial_line_counts[filename], current, diff, ratio))
            # vs previous round
            prev_changes = []
            if round_results:
                prev_counts = round_results[-1].line_counts
                for filename, current in line_counts.items():
                    if filename in prev_counts:
                        diff = current - prev_counts[filename]
                        if diff != 0:
                            ratio = diff / prev_counts[filename] * 100 if prev_counts[filename] > 0 else 0
                            prev_changes.append((filename, prev_counts[filename], current, diff, ratio))

            if init_changes:
                print(f"[info] Line changes (vs initial):")
                for filename, initial, final, diff, ratio in init_changes:
                    sign = "+" if diff > 0 else ""
                    print(f"  {filename}: {initial} -> {final} ({sign}{diff}, {ratio:+.1f}%)")
            if prev_changes:
                print(f"[info] Line changes (vs prev round):")
                for filename, prev, final, diff, ratio in prev_changes:
                    sign = "+" if diff > 0 else ""
                    print(f"  {filename}: {prev} -> {final} ({sign}{diff}, {ratio:+.1f}%)")


        # Save round result immediately if result_dir is specified
        if result_dir and task_id:
            result_path = result_dir / task_id
            result_path.mkdir(parents=True, exist_ok=True)
            round_file = result_path / f"round_{round_num}.json"
            with open(round_file, "w", encoding="utf-8") as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            print(f"[info] Round {round_num} completed in {result.duration_seconds:.1f}s, result saved to {round_file}")

            # Save corresponding raw run log
            if output_format == "stream-json":
                jsonl_file = result_path / f"run{round_num}.log"
                with open(jsonl_file, "w", encoding="utf-8") as f:
                    f.write(stdout)
                print(f"[info] Saved step-by-step JSONL log to {jsonl_file}")

        return result

    # Initialize failure memory
    memory = FailureMemory() if use_failure_memory else None

    # First call: new session
    round_start = time.time()
    stdout, reason, returncode = run_claude_once(base + ["--", prompt], env=env, cwd=cwd)
    round_duration = time.time() - round_start
    record_round(1, stdout, reason, returncode, round_duration)
    if git_commit_dir:
        commit_round(1, git_commit_dir)

    # Update failure memory after first round
    if memory and stdout:
        signals = analyze_round_log(stdout)
        tool_usage = compute_tool_usage_stats(stdout)
        memory.update(1, signals, tool_usage)
        triples = extract_experience_triples(stdout, round_number=1)
        memory.add_experience(1, triples)
        if signals or triples:
            print(f"[failure_memory] Round 1: {len(signals)} signals, {len(triples)} experience triples")

    if statement_error:
        return "STATEMENT_CHANGED", 1, round_results

    rounds = 1
    consecutive_limits = 1 if reason == "LIMIT" else 0  # Track consecutive LIMIT count
    max_consecutive_limits = 2  # Reset session after 2 consecutive LIMITs

    while reason == "LIMIT" or reason is None or reason == "COMPLETE" or reason == "SELECTED_TARGET_COMPLETE":
        print("=" * 60)

        if rounds >= max_rounds:
            print(
                f"\n[warn] Reached maximum round count {max_rounds}, stopping.",
                file=sys.stderr,
            )
            break

        time.sleep(max(0.0, sleep_between_rounds))

        # If COMPLETE, run verification callback
        if reason == "COMPLETE":
            print("\n[info] Received COMPLETE signal.")
            if on_complete:
                if on_complete():
                    # Verification passed
                    break
                else:
                    # Verification failed, resend prompt
                    print("[info] Verification failed, resending prompt...")
                    rounds += 1
                    round_start = time.time()
                    resend_prompt = prompt
                    if memory:
                        directions = generate_directions(memory)
                        if directions:
                            resend_prompt = prompt + "\n\n" + directions
                            print(f"[failure_memory] Injecting directions into verification retry")
                    stdout, reason, returncode = run_claude_once(base + ["--", resend_prompt], env=env, cwd=cwd)
                    round_duration = time.time() - round_start
                    record_round(rounds, stdout, reason, returncode, round_duration)
                    if git_commit_dir:
                        commit_round(rounds, git_commit_dir)
                    if statement_error:
                        return "STATEMENT_CHANGED", rounds, round_results
                    continue
            else:
                # No verification callback, accept COMPLETE
                break

        # If SELECTED_TARGET_COMPLETE, continue to next target
        if reason == "SELECTED_TARGET_COMPLETE":
            print("\n[info] Received SELECTED_TARGET_COMPLETE signal, continuing to next target...")

        rounds += 1

        # Check if we need to reset session due to consecutive LIMITs
        should_reset_session = (reason == "LIMIT" and consecutive_limits >= max_consecutive_limits)

        # Build prompt with failure memory directions if enabled
        augmented_prompt = prompt
        if memory:
            directions = generate_directions(memory)
            if directions:
                augmented_prompt = prompt + "\n\n" + directions
                print(f"[failure_memory] Injecting directions from {memory.total_signals} signals")

        # Continue with prompt again if reason is None or need to reset session
        round_start = time.time()
        if reason is None:
            print("[info] No END_REASON detected, continuing with prompt...")
            stdout, reason, returncode = run_claude_once(base + ["--", augmented_prompt], env=env, cwd=cwd)
        elif should_reset_session:
            print(f"[info] Resetting session after {consecutive_limits} consecutive LIMITs...")
            stdout, reason, returncode = run_claude_once(base + ["--", augmented_prompt], env=env, cwd=cwd)
            consecutive_limits = 0  # Reset counter after starting new session
        else:
            # Continue the same session
            cmd = ["claude", "-c", "-p"]
            if model:
                cmd += ["--model", model]
            if mcp_config:
                cmd += ["--strict-mcp-config", "--mcp-config", str(mcp_config)]
            if output_format:
                cmd += ["--output-format", output_format]
                if output_format == "stream-json":
                    cmd += ["--verbose"]
            if permission_mode:
                cmd += ["--permission-mode", permission_mode]
            if effort:
                cmd += ["--effort", effort]
            continue_msg = "continue"
            if memory:
                directions = generate_directions(memory)
                if directions:
                    continue_msg = "continue\n\n" + directions
            stdout, reason, returncode = run_claude_once(cmd + ["--", continue_msg], env=env, cwd=cwd)
        round_duration = time.time() - round_start

        record_round(rounds, stdout, reason, returncode, round_duration)
        if git_commit_dir:
            commit_round(rounds, git_commit_dir)

        # Update failure memory after each round
        if memory and stdout:
            signals = analyze_round_log(stdout)
            tool_usage = compute_tool_usage_stats(stdout)
            memory.update(rounds, signals, tool_usage)
            triples = extract_experience_triples(stdout, round_number=rounds)
            memory.add_experience(rounds, triples)
            if signals or triples:
                print(f"[failure_memory] Round {rounds}: {len(signals)} signals, {len(triples)} experience triples")
            # Save memory for post-hoc analysis
            if result_dir and task_id:
                mem_path = result_dir / task_id / "failure_memory.json"
                memory.save(mem_path)

        if statement_error:
            return "STATEMENT_CHANGED", rounds, round_results

        # Update consecutive_limits counter
        if reason == "LIMIT":
            consecutive_limits += 1
        else:
            consecutive_limits = 0

    return reason, rounds, round_results


def run_task(task: TaskMetadata) -> TaskResult:
    """
    Execute a single task.

    Args:
        task: Task metadata

    Returns:
        Task result
    """
    start_time = datetime.now()
    error_message = None
    mcp_stats = None
    round_results: List[RoundResult] = []
    statement_changed = False

    try:
        # Get prompt
        prompt = task.get_prompt()

        # Build environment with MCP_LOG_NAME
        env = task.build_env()

        # Get MCP log path for later analysis
        mcp_log_path = get_mcp_log_path(task.mcp_log_name, task.mcp_log_dir)

        # Get files to track
        if task.task_type == "file":
            files_to_track = [task.target_path]
        else:
            files_to_track = find_lean_files(task.target_path)

        # Initialize statement tracker if enabled
        tracker = None
        if task.track_statements and files_to_track:
            tracker = StatementTracker(files_to_track)
            print(f"[info] Tracking statements in {len(files_to_track)} file(s)")

        # Build verification callback
        def on_complete_callback() -> bool:
            if not task.check_after_complete:
                return True

            check_path = task.get_check_path()

            # Determine files to check based on task_type
            if task.task_type == "file":
                lean_files = [check_path] if check_path.suffix == ".lean" else []
            else:
                lean_files = find_lean_files(check_path)

            if not lean_files:
                return True

            print(f"[info] Verifying {len(lean_files)} .lean files...")
            results = check_lean_files_parallel(lean_files)

            # Filter errors based on allow_sorry setting
            if task.allow_sorry:
                errors = [f for f, e, _, _, _ in results if e]
                print(f"[info] allow_sorry=True, ignoring sorry warnings")
            else:
                errors = [f for f, e, s, _, _ in results if e or s]

            if errors:
                print(f"\n[error] {len(errors)} files have errors{'' if task.allow_sorry else '/sorry'}:")
                for f in errors:
                    print(f"  - {f}")
                return False

            print(f"[info] All {len(lean_files)} files verified successfully!")
            return True

        # Run Claude session
        git_commit_dir = None
        if task.git_commit:
            git_commit_dir = task.target_path if task.task_type == "folder" else task.target_path.parent

        # Prepare result_dir for immediate round saving
        result_dir_path = Path(task.result_dir) if task.result_dir else None

        end_reason, rounds_used, round_results = run_claude_session(
            prompt=prompt,
            cwd=task.cwd,
            permission_mode=task.permission_mode,
            output_format=task.output_format,
            max_rounds=task.max_rounds,
            sleep_between_rounds=task.sleep_between_rounds,
            env=env,
            on_complete=on_complete_callback if task.check_after_complete else None,
            tracker=tracker,
            on_statement_change=task.on_statement_change,
            git_commit_dir=git_commit_dir,
            result_dir=result_dir_path,
            task_id=task.task_id,
            files_to_track=files_to_track,
            use_failure_memory=task.use_failure_memory,
            mcp_config=task.mcp_config,
            model=task.model,
            effort=task.effort,
            disallowed_tools=task.disallowed_tools,
        )

        # Check if any statement was changed
        statement_changed = any(rr.has_statement_changes() for rr in round_results)

        # Final check if reached limit (not COMPLETE)
        if task.check_after_complete and end_reason != "COMPLETE":
            check_path = task.get_check_path()

            # Determine files to check based on task_type
            if task.task_type == "file":
                lean_files = [check_path] if check_path.suffix == ".lean" else []
            else:
                lean_files = find_lean_files(check_path)

            if lean_files:
                print(f"\n[info] Reached limit, performing final verification on {len(lean_files)} .lean files...")
                results = check_lean_files_parallel(lean_files)

                # Filter errors based on allow_sorry setting
                if task.allow_sorry:
                    errors = [f for f, e, _, _, _ in results if e]
                    print(f"[info] allow_sorry=True, ignoring sorry warnings")
                else:
                    errors = [f for f, e, s, _, _ in results if e or s]

                if errors:
                    print(f"[error] {len(errors)} files have errors{'' if task.allow_sorry else '/sorry'}:")
                    for f in errors:
                        print(f"  - {f}")
                else:
                    print(f"[info] All {len(lean_files)} files verified successfully!")
                    # Update end_reason to COMPLETE if verification passed
                    if not task.allow_sorry: # Only set to COMPLETE if allow_sorry is False (which means the file is indeed done)
                        end_reason = "COMPLETE"

        # Analyze MCP stats if result_dir is specified
        if task.result_dir and mcp_log_path and mcp_log_path.exists():
            stats_dir = Path(task.result_dir) / task.task_id
            stats_dir.mkdir(parents=True, exist_ok=True)
            print(f"[info] Generating MCP stats to {stats_dir}")
            mcp_stats = analyze_mcp_log(str(mcp_log_path), str(stats_dir))

        success = end_reason == "COMPLETE"

    except Exception as e:
        end_reason = "ERROR"
        rounds_used = 0
        success = False
        error_message = str(e)
        print(f"[error] Task failed: {e}", file=sys.stderr)

    end_time = datetime.now()

    result = TaskResult(
        task_id=task.task_id,
        success=success,
        end_reason=end_reason,
        rounds_used=rounds_used,
        start_time=start_time,
        end_time=end_time,
        error_message=error_message,
        mcp_stats=mcp_stats,
        round_results=round_results,
        statement_changed=statement_changed,
    )

    print(f"\n[info] Task {task.task_id} completed:")
    print(f"  Success: {result.success}")
    print(f"  End reason: {result.end_reason}")
    print(f"  Rounds used: {result.rounds_used}")
    print(f"  Duration: {result.duration_seconds:.1f}s")
    if statement_changed:
        print(f"  Statement changed: Yes")

    # Save final result to JSON if result_dir is specified
    # (Individual round results are already saved immediately during execution)
    if task.result_dir:
        result_path = Path(task.result_dir) / task.task_id
        result_path.mkdir(parents=True, exist_ok=True)

        # Save final result summary
        result_file = result_path / "result.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        print(f"[info] Final result saved to {result_file}")

    return result


def run_tasks(
    tasks: List[TaskMetadata],
    parallel: bool = False,
    max_workers: int = 1,
) -> List[TaskResult]:
    """
    Execute multiple tasks.

    Args:
        tasks: List of task metadata
        parallel: Whether to run in parallel
        max_workers: Maximum parallel workers

    Returns:
        List of results (in same order as tasks)
    """
    if not tasks:
        return []

    if not parallel or max_workers <= 1:
        # Sequential execution
        results = []
        for i, task in enumerate(tasks, 1):
            print(f"\n{'=' * 60}")
            print(f"[{i}/{len(tasks)}] Running task: {task.task_id}")
            print("=" * 60)
            result = run_task(task)
            results.append(result)
        return results

    # Parallel execution
    from concurrent.futures import ThreadPoolExecutor, as_completed

    results = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(run_task, task): idx for idx, task in enumerate(tasks)
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                # Create error result
                task = tasks[idx]
                results[idx] = TaskResult(
                    task_id=task.task_id,
                    success=False,
                    end_reason="ERROR",
                    rounds_used=0,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message=str(e),
                )

    return results
