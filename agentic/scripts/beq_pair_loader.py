"""Load (reference, candidate) pairs for BEq evaluation.

Extracts .extracted.lean files from a run's tar.gz and matches them
against ground truth in leanproblems/shadowbench_lift_textcode/.

Usage (as library):
    from scripts.beq_pair_loader import load_pairs_for_run
    pairs = load_pairs_for_run(run_id, tar_gz_path)
    # pairs: list of dicts with keys: task_id, area, level, ref_path, ref_content, cand_content

Filename convention in tar.gz:
    {area}_{level}_{problem_basename}.extracted.lean
    e.g.: algebra_L1_alg_gen_L1_001.extracted.lean

Ground truth path:
    leanproblems/shadowbench_lift_textcode/{level}/{gt_dir}/{problem_basename}.lean
"""

import re
import tarfile
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GROUND_TRUTH_BASE = REPO_ROOT / "leanproblems" / "shadowbench_lift_textcode"

# Map from tar-file category prefix → ground truth subdirectory name
CATEGORY_DIR_MAP: dict[str, str] = {
    "algebra": "algebra",
    "analysis": "analysis",
    "college-math-competition": "competition",
    "geometry": "geometry",
    "topology": "topology",
    # "number-theory" intentionally absent: no ground truth in shadowbench_lift_textcode
}

TASK_FILENAME_RE = re.compile(
    r"^(?P<area>[^_]+(?:-[^_]+)*)_(?P<level>L[123])_(?P<basename>.+)\.extracted\.lean$"
)


def _parse_task_filename(filename: str) -> tuple[str, str, str] | None:
    """Return (area, level, problem_basename) or None if unrecognised."""
    m = TASK_FILENAME_RE.match(filename)
    if not m:
        return None
    return m.group("area"), m.group("level"), m.group("basename")


def find_ground_truth(area: str, level: str, basename: str) -> Path | None:
    """Look up the ground truth .lean file for a task."""
    gt_dir_name = CATEGORY_DIR_MAP.get(area)
    if gt_dir_name is None:
        return None  # no ground truth for this category
    candidate = GROUND_TRUTH_BASE / level / gt_dir_name / f"{basename}.lean"
    if candidate.exists():
        return candidate
    return None


def _build_pairs_from_extracted_files(extracted_files: dict[str, str]) -> list[dict]:
    """Build pair list from {filename: content} mapping."""
    pairs = []
    for filename in sorted(extracted_files):
        cand_content = extracted_files[filename]
        parsed = _parse_task_filename(filename)
        if parsed is None:
            pairs.append({
                "task_id": filename,
                "area": None,
                "level": None,
                "problem_name": None,
                "ref_path": None,
                "ref_content": None,
                "cand_content": None,
                "skip_reason": f"unrecognised filename: {filename}",
            })
            continue

        area, level, basename = parsed
        task_id = f"{area}_{level}_{basename}"

        ref_path = find_ground_truth(area, level, basename)
        if ref_path is None:
            pairs.append({
                "task_id": task_id,
                "area": area,
                "level": level,
                "problem_name": basename,
                "ref_path": None,
                "ref_content": None,
                "cand_content": cand_content,
                "skip_reason": f"no ground truth for area '{area}'",
            })
            continue

        ref_content = ref_path.read_text(encoding="utf-8")
        pairs.append({
            "task_id": task_id,
            "area": area,
            "level": level,
            "problem_name": basename,
            "ref_path": ref_path,
            "ref_content": ref_content,
            "cand_content": cand_content,
            "skip_reason": None,
        })
    return pairs


def load_pairs_from_tar(tar_gz_path: str | Path) -> list[dict]:
    """Load pairs from a tar.gz archive."""
    tar_gz_path = Path(tar_gz_path)
    extracted_files = {}
    with tarfile.open(tar_gz_path, "r:gz") as tf:
        members = {Path(m.name).name: m for m in tf.getmembers() if m.isfile()}
        for name, m in members.items():
            if name.endswith(".extracted.lean"):
                fobj = tf.extractfile(m)
                extracted_files[name] = fobj.read().decode("utf-8") if fobj else ""
    return _build_pairs_from_extracted_files(extracted_files)


def load_pairs_from_dir(run_dir: str | Path) -> list[dict]:
    """Load pairs from a directory containing .extracted.lean files (no tar.gz)."""
    run_dir = Path(run_dir)
    # Support two layouts: files directly in run_dir, or in a single subdirectory
    extracted = list(run_dir.glob("*.extracted.lean"))
    if not extracted:
        sub_dirs = [d for d in run_dir.iterdir() if d.is_dir()]
        if sub_dirs:
            extracted = list(sub_dirs[0].glob("*.extracted.lean"))
    extracted_files = {}
    for p in extracted:
        extracted_files[p.name] = p.read_text(encoding="utf-8")
    return _build_pairs_from_extracted_files(extracted_files)


def load_pairs_for_run(run_id: str, tar_gz_path: str | Path | None = None) -> list[dict]:
    """
    Load (reference, candidate) pairs for a run.

    Tries tar.gz first; falls back to reading .extracted.lean files from the run directory.

    Returns a list of dicts:
        task_id        str  — e.g. "algebra_L1_alg_gen_L1_001"
        area           str  — category
        level          str  — L1 / L2 / L3
        problem_name   str  — basename, e.g. "alg_gen_L1_001"
        ref_path       Path — path to ground truth .lean
        ref_content    str  — full ground truth file content
        cand_content   str  — full extracted.lean content
        skip_reason    str | None — set if this pair should be skipped
    """
    naive_dir = REPO_ROOT / "results" / "naive_prompting"
    run_dir = naive_dir / run_id

    # Try tar.gz first
    if tar_gz_path is not None and Path(tar_gz_path).exists():
        return load_pairs_from_tar(tar_gz_path)

    # Default tar.gz location
    default_tar = run_dir / f"{run_id}.tar.gz"
    if default_tar.exists():
        return load_pairs_from_tar(default_tar)

    # Fall back to directory
    if run_dir.exists():
        return load_pairs_from_dir(run_dir)

    raise FileNotFoundError(f"No tar.gz or directory found for run {run_id}")


if __name__ == "__main__":
    import sys
    import json as _json

    run_id = sys.argv[1] if len(sys.argv) > 1 else "claude-sonnet-4-6-4096-6edc4b"
    tar_gz = (
        REPO_ROOT / "results" / "naive_prompting" / run_id / f"{run_id}.tar.gz"
    )
    pairs = load_pairs_for_run(run_id, tar_gz)
    total = len(pairs)
    skipped = sum(1 for p in pairs if p["skip_reason"])
    print(f"Loaded {total} tasks, {skipped} skipped, {total - skipped} matchable.")
    for p in pairs[:5]:
        print(f"  {p['task_id']:50} skip={p['skip_reason']}")
