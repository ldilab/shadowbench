\begin{definition}[contract]
Let \( M \) be a matroid on a ground set \( E \), and let \( C \subseteq E \).
The \emph{contraction} of \( C \) from \( M \), denoted \( M / C \), is defined by
\[
M / C := (M^\ast \setminus C)^\ast .
\]
\end{definition}

\begin{lemma}[contract_ground]
For any matroid \( M \) and set \( C \subseteq E \),
\[
E(M / C) = E(M) \setminus C .
\]
\end{lemma}

\begin{proof}
By definition \( M / C = (M^\ast \setminus C)^\ast \).
Taking ground sets and using the corresponding facts for deletion and duality yields
\( E(M / C) = E(M) \setminus C \).
\end{proof}

\begin{lemma}[dual_delete_dual]
For any matroid \( M \) and set \( X \subseteq E \),
\[
(M / X)^\ast = M^\ast \setminus X,
\qquad
(M \setminus X)^\ast = M^\ast / X .
\]
\end{lemma}

\begin{proof}
Both identities follow directly from the definition of contraction
\( M / X := (M^\ast \setminus X)^\ast \) and the involutivity of matroid duality.
\end{proof}

\begin{lemma}[contract_contract]
For any matroid \( M \) and sets \( C_1, C_2 \subseteq E \),
\[
M / C_1 / C_2 = M / (C_1 \cup C_2).
\]
In particular,
\[
M / C_1 / C_2 = M / C_2 / C_1 .
\]
\end{lemma}

\begin{proof}
Using the definition of contraction via duality, iterated contraction corresponds to
iterated deletion in the dual matroid.
Since deletion distributes over unions, the result follows.
Commutativity is immediate from the commutativity of union.
\end{proof}

\begin{lemma}[contract_empty]
For any matroid \( M \),
\[
M / \varnothing = M .
\]
\end{lemma}

\begin{proof}
This follows from the definition of contraction and the fact that deleting the empty set
has no effect on a matroid.
\end{proof}

\begin{lemma}[contract_eq_contract_iff]
For any matroid \( M \) and sets \( C_1, C_2 \subseteq E \),
\[
M / C_1 = M / C_2
\;\Longleftrightarrow\;
C_1 \cap E(M) = C_2 \cap E(M).
\]
\end{lemma}

\begin{proof}
Using the dual characterization of contraction, the statement reduces to the corresponding
criterion for equality of deletions in the dual matroid.
\end{proof}

\begin{lemma}[coindep_contract_iff]
Let \( M \) be a matroid, \( C \subseteq E(M) \), and \( X \subseteq E(M) \).
Then
\[
X \text{ is coindependent in } M / C
\;\Longleftrightarrow\;
X \text{ is coindependent in } M \text{ and } X \cap C = \varnothing .
\]
\end{lemma}

\begin{proof}
This follows by rewriting coindependence in terms of independence in the dual matroid
and applying the characterization of deletion.
\end{proof}

\begin{lemma}[contract_isCocircuit_iff]
Let \( M \) be a matroid and \( C \subseteq E(M) \).
A set \( K \) is a cocircuit of \( M / C \) if and only if
\( K \) is a cocircuit of \( M \) and \( K \cap C = \varnothing \).
\end{lemma}

\begin{proof}
This is an immediate consequence of the previous lemma together with the definition
of cocircuits in terms of coindependence.
\end{proof}

\begin{lemma}[Indep.contract_isBase_iff]
Let \( M \) be a matroid and let \( I \subseteq E(M) \) be independent.
A set \( B \) is a basis of \( M / I \) if and only if
\[
B \cup I \text{ is a basis of } M
\quad\text{and}\quad
B \cap I = \varnothing .
\]
\end{lemma}

\begin{proof}
Using duality, the statement reduces to the corresponding characterization of bases
under deletion.
Translating back yields the claim.
\end{proof}

\begin{lemma}[Indep.contract_indep_iff]
Let \( M \) be a matroid and let \( I \subseteq E(M) \) be independent.
For any set \( J \subseteq E(M) \),
\[
J \text{ is independent in } M / I
\;\Longleftrightarrow\;
J \cap I = \varnothing
\;\text{ and }\;
J \cup I \text{ is independent in } M .
\]
\end{lemma}

\begin{proof}
A set is independent if and only if it is contained in a basis.
Applying the previous lemma on bases yields the equivalence.
\end{proof}

\begin{lemma}[IsNonloop.contractElem_indep_iff]
Let \( M \) be a matroid and let \( e \) be a non-loop element of \( M \).
For any set \( I \),
\[
I \text{ is independent in } M / \{e\}
\;\Longleftrightarrow\;
e \notin I
\;\text{ and }\;
I \cup \{e\} \text{ is independent in } M .
\]
\end{lemma}

\begin{proof}
This is the specialization of the previous lemma to the case \( I = \{e\} \),
using that \( e \) is independent.
\end{proof}

\begin{lemma}[IsBasis.contract_eq_contract_delete]
Let \( M \) be a matroid, \( X \subseteq E(M) \), and let \( I \) be a basis of \( X \).
Then
\[
M / X = M / I \setminus (X \setminus I).
\]
\end{lemma}

\begin{proof}
Decompose \( X \) as the disjoint union of the basis \( I \) and the remaining elements
\( X \setminus I \).
Contracting \( X \) is equivalent to contracting \( I \) and deleting the remaining elements,
which gives the stated equality.
\end{proof}
