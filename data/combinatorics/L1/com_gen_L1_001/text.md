\begin{definition}[sigma]
Let \(\iota\) be an index set, let \(\alpha_i\) be a type for each \(i \in \iota\), and let
\(M_i\) be a matroid on \(\alpha_i\).
The \emph{sum} of the family \((M_i)_{i \in \iota}\) is the matroid on the sigma-type
\(\Sigma_{i \in \iota} \alpha_i\) defined as follows:
\begin{itemize}
\item its ground set is
\[
E = \bigcup_{i \in \iota} \{i\} \times E(M_i),
\]
\item a set \(I \subseteq \Sigma_{i \in \iota} \alpha_i\) is independent if and only if
for every \(i \in \iota\), the fiber
\[
\{x \in \alpha_i \mid (i,x) \in I\}
\]
is independent in \(M_i\),
\item a set \(B \subseteq \Sigma_{i \in \iota} \alpha_i\) is a basis if and only if
for every \(i \in \iota\), the corresponding fiber is a basis of \(M_i\).
\end{itemize}
\end{definition}

\begin{lemma}[abm_combinatorics_l2_com_gen_l2_001_item_2]
A set \(I \subseteq \Sigma_{i \in \iota} \alpha_i\) is independent if and only if
there exists a basis \(B\) such that \(I \subseteq B\).
\end{lemma}

\begin{proof}
For each \(i\), the fiber of \(I\) over \(i\) is independent in \(M_i\), and hence can be
extended to a basis of \(M_i\).
The union of these bases is a basis of the sum containing \(I\).
Conversely, any subset of a basis is independent.
\end{proof}

\begin{lemma}[abm_combinatorics_l2_com_gen_l2_001_item_3]
The sum matroid admits a basis.
Moreover, if \(B_i\) is a basis of \(M_i\) for each \(i \in \iota\), then
\[
\bigcup_{i \in \iota} \{i\} \times B_i
\]
is a basis.
\end{lemma}

\begin{proof}
Choose a basis \(B_i\) of \(M_i\) for each index \(i\).
By definition, the disjoint union of these bases is a basis of the sum matroid.
\end{proof}

\begin{theorem}[abm_combinatorics_l2_com_gen_l2_001_item_4]
Let \(B_1\) and \(B_2\) be bases of the sum matroid.
For any element \(e \in B_1 \setminus B_2\), there exists an element
\(f \in B_2 \setminus B_1\) such that
\[
(B_1 \setminus \{e\}) \cup \{f\}
\]
is again a basis.
\end{theorem}

\begin{proof}
The element \(e\) belongs to a unique component indexed by some \(i\).
Applying the basis exchange property in the matroid \(M_i\) yields an element \(f\) in the
corresponding fiber of \(B_2\) that restores a basis in that component.
All other components remain unchanged, so the resulting set is a basis of the sum.
\end{proof}

\begin{theorem}[abm_combinatorics_l2_com_gen_l2_001_item_5]
Let \(I \subseteq X\) be subsets of the ground set.
If \(I\) is independent and maximal among independent subsets of \(X\), then \(I\) is a basis of \(X\).
\end{theorem}

\begin{proof}
For each index \(i\), the fiber of \(I\) is a maximal independent subset of the fiber of \(X\),
and hence a basis there.
By the definition of bases in the sum matroid, \(I\) is a basis of \(X\).
\end{proof}

\begin{definition}[abm_combinatorics_l2_com_gen_l2_001_item_6]
Every independent set and every basis is contained in the ground set.
\end{definition}

\begin{proof}
Each fiberwise independent set or basis lies in the ground set of the corresponding matroid,
so their union lies in the ground set of the sum matroid.
\end{proof}
