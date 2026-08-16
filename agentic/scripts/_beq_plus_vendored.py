"""Vendored BEq / BEq+ metric functions from a third-party Lean-interact library
(MIT-licensed). Author/citation details withheld for double-blind review; the
camera-ready version will restore the upstream attribution and reference to the
EMNLP 2025 paper that introduced the metric.

Only the core metric functions are kept; the upstream's dataset-evaluation code
has been removed.
"""

import json

from rich.console import Console

from lean_interact import AutoLeanServer, Command
from lean_interact.interface import (
    CommandResponse,
    LeanError,
    Pos,
    message_intersects_code,
)
from lean_interact.utils import (
    clean_last_theorem_string,
    indent_code,
    split_conclusion,
)

console = Console()
DEFAULT_TIMEOUT = 60


def extract_exact_proof(lean_output: CommandResponse, proof_start_line: int | None = None) -> str | None:
    start = Pos(line=proof_start_line, column=0) if proof_start_line else None
    for message in lean_output.messages:
        if message_intersects_code(message, start, None):
            if message.severity == "error":
                return None
            if message.severity == "info" and message.data.startswith("Try this:"):
                return message.data.split("Try this:")[1].strip()
    return None


def check_proof_sub(
    server: AutoLeanServer,
    formal_code: str,
    formal_2_start_line: int,
    proof: str,
    timeout: int,
    indent_level: int = 2,
    mathlib_env: int | None = None,
) -> str | None:
    prepended = "\nintros\nsymm_saturate\n"
    try:
        lean_output = server.run(
            Command(cmd=formal_code + indent_code(prepended + proof, indent_level), env=mathlib_env),
            timeout=timeout,
        )
        if isinstance(lean_output, LeanError):
            return None
        if proof == "sorry":
            if lean_output.lean_code_is_valid(start_pos=Pos(line=formal_2_start_line, column=0)):
                return proof
            return None
        if lean_output.lean_code_is_valid(start_pos=Pos(line=formal_2_start_line, column=0), allow_sorry=False):
            if proof == "exact?":
                return extract_exact_proof(lean_output, proof_start_line=formal_2_start_line)
            return proof
    except TimeoutError:
        pass
    except (ConnectionAbortedError, json.JSONDecodeError) as e:
        console.log(f"Error during proof checking: {e}")
    return None


def beql(
    formalization_1: str,
    formalization_2: str,
    src_header: str,
    server: AutoLeanServer,
    timeout_per_proof: int,
    verbose: bool = False,
    mathlib_env: int | None = None,
) -> bool:
    base_thm_name = "base_theorem"
    reformulated_thm_name = "reformulated_theorem"

    res = [False, False]
    for i, (base_thm, reform_thm) in enumerate(
        [(formalization_1, formalization_2), (formalization_2, formalization_1)]
    ):
        if verbose:
            console.print(f"=====\nChecking {'1 -> 2' if i == 0 else '2 -> 1'}")
        try:
            formal_1_code = (
                src_header + "\n\n" + clean_last_theorem_string(base_thm, base_thm_name, add_sorry=True) + "\n\n"
            )
            formal_2_start_line = formal_1_code.count("\n") + 1
            formal_2_code = f"{clean_last_theorem_string(reform_thm, reformulated_thm_name, add_sorry=False)} := by"
        except ValueError:
            if verbose:
                console.print("Invalid theorems encountered, skipping this pair.")
            break

        formal_code = formal_1_code + formal_2_code
        if check_proof_sub(server, formal_code, formal_2_start_line, "sorry", timeout_per_proof, mathlib_env=mathlib_env) is None:
            if verbose:
                console.print("Ill-typed formalization encountered, skipping this pair.")
            break

        proof_exact = check_proof_sub(server, formal_code, formal_2_start_line, "exact?", timeout_per_proof, mathlib_env=mathlib_env)
        if proof_exact and base_thm_name in proof_exact:
            res[i] = True
            if verbose:
                console.print("Proof exact")
        else:
            break

    return res[0] and res[1]


def beq_plus(
    formalization_1: str,
    formalization_2: str,
    src_header: str,
    server: AutoLeanServer,
    timeout_per_proof: int,
    verbose: bool = False,
    mathlib_env: int | None = None,
) -> bool:
    base_thm_name = "base_theorem"
    reformulated_thm_name = "reformulated_theorem"

    def prove_all(tactics: list[str]) -> str:
        prove_independent = " ; ".join([f"(all_goals try {t})" for t in tactics])
        prove_combined = "all_goals (" + " ; ".join([f"(try {t})" for t in tactics]) + ")"
        return "all_goals intros\nfirst | (" + prove_independent + ") | (" + prove_combined + ")"

    solver_tactics_apply = ["tauto", "simp_all_arith!", "noncomm_ring", "exact?"]
    solver_tactics_have = ["tauto", "simp_all_arith!", "exact? using this"]
    proof_all_apply = prove_all(solver_tactics_apply)
    proof_all_have = prove_all(solver_tactics_have)

    res = [False, False]
    for i, (base_thm, reform_thm) in enumerate(
        [(formalization_1, formalization_2), (formalization_2, formalization_1)]
    ):
        if verbose:
            console.print(f"=====\nChecking {'1 -> 2' if i == 0 else '2 -> 1'}")
        try:
            formal_1_code = (
                src_header + "\n\n" + clean_last_theorem_string(base_thm, base_thm_name, add_sorry=True) + "\n\n"
            )
            formal_2_start_line = formal_1_code.count("\n") + 1
            formal_2_code = f"{clean_last_theorem_string(reform_thm, reformulated_thm_name, add_sorry=False)} := by"
        except ValueError:
            if verbose:
                console.print("Invalid theorem encountered, skipping this pair.")
            break

        formal_code = formal_1_code + formal_2_code
        if check_proof_sub(server, formal_code, formal_2_start_line, "sorry", timeout_per_proof, mathlib_env=mathlib_env) is None:
            if verbose:
                console.print("Ill-typed formalization encountered, skipping this pair.")
            break

        # 1. BEqL
        proof_exact = check_proof_sub(server, formal_code, formal_2_start_line, "exact?", timeout_per_proof, mathlib_env=mathlib_env)
        if proof_exact and base_thm_name in proof_exact:
            res[i] = True
            if verbose:
                console.print("Proof exact")
            continue

        # Skip if trivially provable by assumption
        if check_proof_sub(server, formal_code, formal_2_start_line, "assumption", timeout_per_proof, mathlib_env=mathlib_env):
            if verbose:
                console.print("Skipping as provable by assumption")
            continue

        # 2. Apply base theorem directly
        proof_apply = check_proof_sub(
            server, formal_code, formal_2_start_line,
            f"apply {base_thm_name}\n" + proof_all_apply, timeout_per_proof, mathlib_env=mathlib_env,
        )
        if proof_apply:
            res[i] = True
            if verbose:
                console.print("Proof apply")
            continue

        # 3. Have strategy (introduce conclusion of base theorem as hypothesis)
        provable_without_have = False
        try:
            res_without_have = server.run(Command(cmd=formal_2_code + proof_all_have, env=mathlib_env), timeout=timeout_per_proof)
            if isinstance(res_without_have, CommandResponse):
                provable_without_have = res_without_have.lean_code_is_valid(allow_sorry=False)
        except TimeoutError:
            pass
        except (ConnectionAbortedError, json.JSONDecodeError) as e:
            console.log(f"Error during proof checking: {e}")

        if not provable_without_have:
            idx_conclusion = split_conclusion(formal_1_code)
            if idx_conclusion:
                idx_end_conclusion = formal_1_code.rfind(":=")
                conclusion = formal_1_code[idx_conclusion:idx_end_conclusion].strip()
                have_stmt_proof = (
                    f"have {conclusion} := by\n"
                    + indent_code(f"apply_rules [{base_thm_name}]\n" + proof_all_apply, 2)
                    + "\n"
                )
                proof_have = check_proof_sub(
                    server, formal_code, formal_2_start_line,
                    have_stmt_proof + proof_all_have, timeout_per_proof, mathlib_env=mathlib_env,
                )
                if proof_have:
                    res[i] = True
                    if verbose:
                        console.print("Proof have")
                    continue

        # 4. Convert strategy (tolerance 0–4)
        for max_step in range(0, 5):
            proof_convert = check_proof_sub(
                server, formal_code, formal_2_start_line,
                f"convert (config := .unfoldSameFun) {base_thm_name} using {max_step}\n" + proof_all_apply,
                timeout_per_proof, mathlib_env=mathlib_env,
            )
            if proof_convert:
                res[i] = True
                if verbose:
                    console.print(f"Proof convert (using {max_step})")
                break

        if not res[i]:
            break

    return res[0] and res[1]
