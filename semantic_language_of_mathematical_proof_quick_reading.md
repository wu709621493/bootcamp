# Semantic Language of Mathematical Proof: Quick Reading

This quick guide helps you read a proof by meaning, not by symbols alone.

## 1) Read a proof as a chain of claims
A proof is usually:
1. **Assumptions** (what is given)
2. **Target** (what must be shown)
3. **Intermediate claims** (lemmas, transformations)
4. **Conclusion** (target reached)

Semantic cue: ask **"Why does this sentence move us closer to the target?"**

## 2) Translate signal words into logical moves
- **"Suppose / Assume"** → temporary world is opened.
- **"Let"** → object is introduced with constraints.
- **"If ... then ..."** → implication goal or tool.
- **"Only if"** → reverse direction.
- **"For all"** → arbitrary element method.
- **"There exists"** → construction or witness needed.
- **"Hence / Therefore"** → derived consequence.
- **"Conversely"** → proving the other direction.
- **"By contradiction"** → assume negation of target.

## 3) Track quantifiers first
Before details, mark:
- Domain of objects
- Universals ($\\forall$)
- Existentials ($\\exists$)
- Order of quantifiers

Example:
- "$\\forall x\\,\\exists y$" means each $x$ may have a different $y$.
- "$\\exists y\\,\\forall x$" means one single $y$ works for all $x$.

This prevents most quick-reading mistakes.

## 4) Recognize common proof skeletons
- **Direct proof**: assume premises, derive result.
- **Contrapositive**: prove $\\neg Q \\Rightarrow \\neg P$ instead of $P \\Rightarrow Q$.
- **Contradiction**: assume statement false, derive impossibility.
- **Induction**: base case + step from $n$ to $n+1$.
- **Case split**: partition domain; prove each case.
- **Construction**: explicitly build required object.

## 5) Build a one-line map while reading
After each paragraph, write:
- **Claim made:**
- **Tool used:** definition / theorem / algebra / inequality
- **Dependency:** which previous line it uses

If you cannot fill one of these, reread that line.

## 6) Minimal symbol-to-semantics dictionary
- "$a \\in A$" → object-membership fact.
- "$A \\subseteq B$" → every element of $A$ is in $B$.
- "$f: A \\to B$" → function with source/target contract.
- "$f$ injective" → distinct inputs keep distinct outputs.
- "$f$ surjective" → every target has a preimage.
- "$\\iff$" → two implications, both directions required.

## 7) Fast check for proof validity
A quick proof passes if:
1. Every introduced object is well-defined.
2. Every logical jump has a cited reason.
3. Quantifiers are respected.
4. No direction in "$\\iff$" is missing.
5. Final line matches exact target statement.

## 8) 30-second reading routine
1. Read theorem statement only.
2. Identify proof type (direct, contradiction, induction, ...).
3. Circle quantifiers and conclusion verb (show/prove/construct).
4. Scan for pivot lines: "thus", "it follows", "contradiction".
5. Verify final sentence equals target, not a nearby variant.

---

Good proof reading is semantic compression: reduce symbol-heavy text into a causal story of valid logical moves.
