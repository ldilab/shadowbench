# Guideline: Extracting Target Code from Gold Lean Code
*(for autoformalization / proof-completion benchmarks)*

This document describes a **safe, reproducible workflow** for extracting a Lean
*target file* (with `sorry`s) from a *gold Lean development* (fully proved),
while avoiding conflicts with mathlib and preventing trivial solutions via imports.

---

## 0. Decide What the Benchmark Is Testing

Before extraction, fix the benchmark intent:

- **Definition completion**: solver must write definitions.
- **Proof completion**: definitions are given; solver fills proofs.
- **Mixed**: some definitions + some proofs.

**Rule of thumb**  
If a concept is explicitly defined in the NL text, **copy the definition verbatim**
into the target code. Do **not** replace it with `:= sorry` unless definition synthesis
is the point of the benchmark.

---

## 1. Lock Imports (Minimal, Non-Trivializing)

A valid benchmark target must:

> Parse and elaborate *up to `sorry`* with **no missing identifiers**.

### Import-minimization procedure
1. Start from the gold file’s imports.
2. Remove imports one by one until the file no longer elaborates.
3. Add back the **minimal imports** required for:
   - core structures (`Matroid`, `Set`, etc.)
   - operations explicitly mentioned in the NL text
   - algebraic lemmas the solver is expected to use
4. **Do not import** any file that already proves the target theorem.

Example (good for matroid minors):
```lean
import Mathlib.Combinatorics.Matroid.Minor.Contract
```

This exposes contraction/deletion algebra but not the finished minor order.

---

## 2. Use a Dedicated Namespace

Always isolate benchmark code from mathlib.

```lean
namespace BenchmarkMatroid
-- benchmark content
end BenchmarkMatroid
```

### Why this matters
- Prevents name clashes (`IsMinor`, `IsStrictMinor`, etc.)
- Prevents accidental reuse of mathlib constants with the same names
- Makes evaluation deterministic

---

## 3. Use `scoped` Notations (Not Global)

Mathlib may already define the same notation (`≤m`, `<m`).

### Preferred pattern
```lean
def IsMinor (N M : Matroid α) : Prop := ...
scoped infixl:50 " ≤m " => BenchmarkMatroid.IsMinor

def IsStrictMinor (N M : Matroid α) : Prop := ...
scoped infixl:50 " <m " => BenchmarkMatroid.IsStrictMinor
```

Enable locally:
```lean
open scoped BenchmarkMatroid
```

This prevents global notation conflicts.

---

## 4. Copy Definitions Verbatim from Gold Code

If the NL text defines something, **the Lean target should define it exactly**.

Example:
```lean
def IsMinor (N M : Matroid α) : Prop :=
  ∃ C D, N = M ／ C ＼ D
```

Avoid:
```lean
def IsMinor (N M : Matroid α) : Prop := sorry
```

unless definition synthesis is explicitly intended.

---

## 5. Be Careful with Typeclass Instances

### Important fact
Typeclass instances are resolved by **type**, not by name.

So defining:
```lean
instance : PartialOrder (Matroid α)
```
may conflict with mathlib, even if it’s inside a namespace.

### Recommended strategies

#### Strategy A (safest)
Do **not** define global instances at all.  
Prove the component lemmas (`refl`, `trans`, `antisymm`) only.

#### Strategy B (good for benchmarks)
Use a **local instance**:
```lean
section
local instance : PartialOrder (Matroid α) := ...
end
```

This prevents pollution of the global instance search.

#### Strategy C (max isolation)
Wrap the type:
```lean
structure BM (α) := (M : Matroid α)
```
and define instances on `BM α`.

---

## 6. Replace Proofs Cleanly with `sorry`

When extracting from gold code:

- Keep the **lemma statement identical**
- Replace the entire proof with `sorry`

Valid forms:
```lean
lemma foo : P := sorry
```
or
```lean
lemma foo : P := by sorry
```

Do **not** leave partial proofs or tactic fragments.

---

## 7. Ensure Each Goal Is Solvable from Allowed Imports

A common failure mode is asking the solver to prove something that requires
lemmas not available from the allowed imports.

### Checklist
- Inspect which lemmas the gold proof uses.
- Verify those lemmas are available from the allowed imports.
- If not:
  - add a minimal import that does **not** trivialize the benchmark, or
  - downgrade the goal, or
  - explicitly include a helper lemma in the benchmark (and NL text).

---

## 8. Prevent “Cheating by Import” in Evaluation

Even if you say “no extra imports”, solvers will try.

### Robust evaluation setup
- Provide a **fixed header** (imports + namespace + variables).
- Allow the solver to submit **only the hole-filling code**.
- Concatenate header + submission before compilation.
- Reject submissions containing:
  - `import`
  - `open scoped` for forbidden scopes
  - `attribute` hacks (optional)

Compile with `--no-sorries` to ensure all holes are filled.

---

## 9. Canonical Extraction Template

```lean
import Mathlib.Combinatorics.Matroid.Minor.Contract

namespace BenchmarkMatroid

open Set
open scoped BenchmarkMatroid

section Minor
variable {α : Type*} {M N M₁ M₂ M₃ : Matroid α} {C D : Set α}

def IsMinor (N M : Matroid α) : Prop := ∃ C D, N = M ／ C ＼ D
scoped infixl:50 " ≤m " => BenchmarkMatroid.IsMinor

def IsStrictMinor (N M : Matroid α) : Prop := N ≤m M ∧ ¬ M ≤m N
scoped infixl:50 " <m " => BenchmarkMatroid.IsStrictMinor

lemma IsMinor.refl {M : Matroid α} : M ≤m M := by
  sorry

lemma IsMinor.trans (h : M₁ ≤m M₂) (h' : M₂ ≤m M₃) : M₁ ≤m M₃ := by
  sorry

lemma IsMinor.antisymm (h : N ≤m M) (h' : M ≤m N) : N = M := by
  sorry

-- optional, local only
section
local instance : PartialOrder (Matroid α) where
  le N M := N ≤m M
  lt N M := N <m M
  le_refl _ := IsMinor.refl
  le_trans _ _ _ := IsMinor.trans
  lt_iff_le_not_ge _ _ := Iff.rfl
  le_antisymm _ _ := IsMinor.antisymm
end

end Minor
end BenchmarkMatroid
```

---

## 10. Final “Ship / No-Ship” Checklist

Before publishing a benchmark:

- [ ] Target file elaborates with only `sorry` warnings
- [ ] No forbidden imports available
- [ ] Dedicated namespace used
- [ ] Notations are scoped
- [ ] No global instance conflicts
- [ ] Every Lean goal corresponds to NL text
- [ ] Goals are solvable from allowed imports
- [ ] Evaluation harness forbids extra imports and remaining `sorry`s

---

*This guideline is designed to produce benchmarks that are fair, non-trivial,
and robust against library shortcuts, while staying closely aligned with the
natural-language mathematics.*
