# Common Agent Rules

> **Purpose**: Shared rules and conventions for ALL agents in the Lean theorem proving system

---

## 1. No Axioms Policy

**NEVER use `axiom`. ALWAYS use `sorry` instead.**

### Why
- `axiom` creates unfounded assumptions that invalidate proofs
- `sorry` explicitly marks gaps while allowing compilation
- `axiom` hides incompleteness, `sorry` makes it visible

### Rules
1. If you cannot prove something, use `sorry`
2. Leave ONLY the smallest stuck part as `sorry`
3. Everything else must be proven
4. Code MUST compile cleanly (no severity-1 errors)

### Example

❌ **Bad**: Using axiom
```lean
axiom foo : P
```

✅ **Good**: Using sorry for stuck part
```lean
lemma foo : P := by
  have h1 : A := by simp  -- proven
  have h2 : B := sorry    -- only this step stuck
  exact combine h1 h2     -- works given h1, h2
```

---

## 2. Blueprint Synchronization

**BLUEPRINT.md is the SINGLE SOURCE OF TRUTH. Update it immediately after any progress.**

### Rules
```
┌─────────────────────────────────────────────────────────────────┐
│  UPDATE BLUEPRINT.md IMMEDIATELY AFTER ANY PROGRESS.            │
│                                                                 │
│  Do NOT batch updates. Do NOT delay. Do NOT forget.             │
│                                                                 │
│  If out of sync, next session will have WRONG information.      │
└─────────────────────────────────────────────────────────────────┘
```

### When to Update
- After completing/failing a lemma → update NOW
- Lemma status changes (todo → partial → done) → update NOW
- Attempt count increases → update NOW
- Before ending session → VERIFY BLUEPRINT matches reality

---

## 3. Status Comment Format

**Every lemma/theorem must have a status comment.**

### Format
```lean
/- (by claude)
State: done | partial | todo
Priority: 1-5
Attempts: N / M
tmp file: <path_or_empty>
-/
lemma name : statement := by
  ...
```

### Fields
- **State**: Current proof status
  - `✅ done` - completely proven
  - `🔄 partial` - partially proven, has sorries
  - `❌ todo` - not started
- **Priority**: 1 (highest) to 5 (lowest)
- **Attempts**: Current attempts / Max budget (20-50)
- **tmp file**: Path to temporary work file (if applicable)

### Example
```lean
/- (by claude)
State: 🔄 partial
Priority: 1
Attempts: 12 / 20
tmp file: PutnamLean/tmp_base_case.lean
-/
lemma base_case (n : ℕ) : f 0 = 1 := by
  have h : 0! = 1 := Nat.factorial_zero
  sorry  -- stuck on type alignment
```

---

## 4. Temporary File Workflow

**Proof agents work in temporary files to avoid cluttering original code.**

### Protocol
1. **Note tmp file** in original file's status comment
   ```lean
   tmp file: tmp_<lemma_name>.lean
   ```

2. **Create tmp file** in same directory as original
   ```bash
   # If original is PutnamLean/Example.lean
   # Create PutnamLean/tmp_base_case.lean
   ```

3. **Work in tmp file**
   - Import original file
   - Copy lemma statement
   - Attempt proof
   - Iterate until proven or budget exhausted

4. **Copy back when proven**
   - Replace sorry in original with working proof
   - Update status comment (State: ✅ done, remove tmp file note)

5. **Delete tmp file**
   - Clean up after successful proof
   - Or keep if returning for later attempts

### Example Tmp File
```lean
-- File: PutnamLean/tmp_base_case.lean
import PutnamLean.Example

lemma base_case (n : ℕ) : f 0 = 1 := by
  -- Working proof here
  ...
```

---

## 5. Tool Priority Order

**Use tools in this specific order to maximize efficiency.**

### Search Tools (Library Lemmas)

**ALWAYS search in this order:**

```
1. leandex    (semantic search - natural language)
   ↓ (if not found)
2. loogle     (type pattern matching)
   ↓ (if not found)
3. local_search (fast confirmation in current project)
```

### Why This Order
- **leandex**: Understands natural language, finds lemmas by concept
  - Example: "factorial of zero equals one"
- **loogle**: Requires exact type patterns, more precise but harder
  - Example: `?f (?x + ?y) = ?f ?x + ?f ?y`
- **local_search**: Fast but limited to current project

### CRITICAL: Don't Give Up If Mathlib Doesn't Have It

```
┌─────────────────────────────────────────────────────────────────┐
│  "Mathlib doesn't have this lemma" is NOT an excuse to give up!  │
│                                                                 │
│  If you searched and didn't find it:                            │
│  1. Build it yourself, step by step                             │
│  2. Break down into smaller intermediate lemmas                 │
│  3. Use have/suffices to construct the proof gradually          │
│  4. Create helper lemmas if needed                              │
│                                                                 │
│  Mathlib is a SHORTCUT, not a REQUIREMENT.                      │
│  You are capable of proving things from first principles.       │
└─────────────────────────────────────────────────────────────────┘
```

**When mathlib search fails**:
- ❌ DON'T: "I couldn't find a lemma, so this is impossible"
- ✅ DO: "No existing lemma found. Let me construct the proof step by step."

### Automation Tools (Tactics)

**First response to ANY goal or error:**

```
1. hint      (shows 🎉 for successful tactics)
   ↓ (if hint doesn't help)
2. grind     (general automation for complex goals)
   ↓ (if automation fails)
3. Manual    (analyze and choose tactic manually)
```

### Why hint/grind First
- **hint**: Tries multiple tactics, shows which ones work
- **grind**: Combines multiple automation strategies
- **Manual**: Time-consuming, save for when automation fails

### Standard Tactic Toolkit

| Tactic | Purpose | When to Use |
|--------|---------|-------------|
| `hint` | Discovery | Don't know what works |
| `grind` | General automation | Complex goals |
| `omega` | Linear arithmetic | ℕ/ℤ inequalities |
| `aesop` | Goal search | Structural proofs |
| `simp` | Simplification | Reduce complexity |
| `rfl` | Definitional equality | By definition |
| `ring` | Ring identities | Algebraic equality |

---

## 6. Error Response Protocol

**When compilation errors occur, follow this protocol:**

### Step 1: Try Automation FIRST
```lean
-- Error occurs
theorem foo : P := by
  hint   -- try hint first
  sorry  -- temporarily replace with sorry
```

If `hint` shows 🎉, use suggested tactic.

### Step 2: Try grind
```lean
theorem foo : P := by
  grind  -- general automation
```

### Step 3: Manual Analysis
Only if both hint and grind fail:
1. Read error message carefully
2. Check goal state
3. Search for lemmas (leandex → loogle)
4. Choose appropriate tactic manually

### Example Flow
```lean
-- Original (has error)
lemma foo : n + 0 = n := by
  exact add_zero  -- error: type mismatch

-- Step 1: Try hint
lemma foo : n + 0 = n := by
  hint  -- 🎉 suggests: simp

-- Step 2: Use hint suggestion
lemma foo : n + 0 = n := by
  simp  -- SUCCESS
```

---

## 7. Agent Log Recording

**Every agent execution MUST create a log in `docs/agent_logs/raw/`.**

### Log Naming
```
<agent_type>_<YYYYMMDD>_<HHMMSS>.md
```

Examples:
- `proof_agent_20260113_143052.md`
- `sketch_agent_20260113_150231.md`
- `blueprint_agent_20260114_092145.md`

### Required Log Sections
1. **Meta Information**: Agent type, session ID, timestamps, goal, target
2. **TODO List**: Task tracking table (updated in place)
3. **Chronological Log**: Timestamped actions (append-only)
4. **Summary**: Result, attempts, key approach, key lemmas
5. **Learnings**: Extracted insights (numbered list)

### Log Format
```markdown
# Agent Execution Log: <agent_type>

## Meta Information
- **Agent Type**: proof_agent
- **Session ID**: 20260113_143052
- **Start Time**: 2026-01-13 14:30:52
- **End Time**: 2026-01-13 15:42:18
- **Overall Goal**: Prove lemma [lem:base_case]
- **Target**: `PutnamLean/Example.lean:67`

## TODO List

| Task | Status | Notes |
|------|--------|-------|
| Read current proof state | ✅ Done | Attempt: 12/20 |
| Try library search (leandex) | ✅ Done | Found lemma |
| Apply found lemma | ✅ Done | SUCCESS |
| Update blueprint | ✅ Done | - |

## Chronological Log

### [14:30:52] Session Start
Starting proof for [lem:base_case], status: 🔄 partial (12/20)

### [14:31:15] Library Search
leandex query: "factorial of zero equals one"
Found: Nat.factorial_zero ✓

### [14:35:28] Attempt 14: SUCCESS
```lean
lemma base_case : f 0 = 1 := by
  have h : f 0 = 0! := by unfold f; rfl
  rw [h]; exact Nat.factorial_zero
```

**Learning**: Intermediate `have` needed to bridge type difference.

### [14:37:12] Update Blueprint
Updated [lem:base_case] status: ✅ done, attempts: 14/20

### [14:37:45] Session End
Proven in 14 attempts.

## Summary
**Result**: SUCCESS
**Total Attempts**: 14/20
**Key Approach**: Library search (leandex) + intermediate `have`
**Key Lemmas**: Nat.factorial_zero

## Learnings
1. leandex highly effective for standard library lemmas
2. Type mismatches often need intermediate `have` to align types
3. Unfolding definitions helps expose definitional equality
```

---

## 8. Compact Context Handling

**Use temporary files and isolated subagents to prevent context explosion.**

### Principles
- **Work in tmp files**: Keeps iteration context separate from main code
- **Use subagents**: Each subagent has isolated context
- **Return essentials**: Only return summary, not full attempt history
- **Log details**: Full details go in agent logs, not returned to coordinator

### Context Budget
- **Coordinator**: Maintains high-level view (blueprint, file structure)
- **Subagents**: Deep dive on specific lemmas (tmp files, many attempts)
- **Logs**: Permanent record (everything captured here)

---

## 9. Keep Comments Minimal

**NO verbose inline comments in proof code.**

### Rules
- Max 1-2 comment lines per logical block
- No long runs of consecutive comment-only lines
- Compress verbose explanations to one line
- Detailed notes → BLUEPRINT or agent logs

### Example

❌ **Bad**: Too many comments
```lean
lemma foo : P := by
  -- Alternative approach (Attempt 12): Use alternating sequence
  -- This reduces to showing alternating is better
  unfold isAlternating at hna
  push_neg at hna
  -- hna now says: NOT (all s i = (-1)^(i+1))
  -- So we can use either alternating type as witness
  use fun i => (-1 : ℤˣ) ^ (i.val + 1)
  -- Need: f n s < f n (fun i => (-1)^(i+1))
  -- This is the CORE result
  sorry
```

✅ **Good**: Compressed
```lean
lemma foo : P := by
  unfold isAlternating at hna
  push_neg at hna
  use fun i => (-1 : ℤˣ) ^ (i.val + 1)
  -- Core: non-alternating has fewer valid perms
  sorry
```

---

## NOT TO DO | WHY | HOW (Instead)

| NOT TO DO | WHY | HOW (Instead) |
|-----------|-----|---------------|
| Use `axiom` | Invalidates proofs | Use `sorry` |
| Work in original file | Clutters code, context explosion | Use tmp files |
| Skip leandex | Miss obvious lemmas | Always leandex first |
| Manual tactics first | Waste time | `hint` → `grind` → manual |
| Forget blueprint | State goes stale | Update immediately |
| Skip agent log | Lose learnings | Log every execution |
| Batch blueprint updates | Sync issues | Update after each change |
| Verbose comments | Code bloat | One-line comments, details in logs |
| Ignore hint/grind | Miss easy wins | Try automation first |
| loogle before leandex | Harder syntax | leandex (natural) → loogle (pattern) |

---

## Summary

All agents must follow these rules:
1. ✅ Use `sorry`, never `axiom`
2. ✅ Update BLUEPRINT immediately after progress
3. ✅ Add status comments to all lemmas
4. ✅ Work in tmp files for proof attempts
5. ✅ Search: leandex → loogle → local_search
6. ✅ Tactics: hint → grind → manual
7. ✅ Try automation before manual analysis
8. ✅ Create agent log for every execution
9. ✅ Keep context compact (tmp files, subagents)
10. ✅ Keep comments minimal (one-liners only)

These rules ensure consistency, prevent context explosion, and capture learnings across all agents.
