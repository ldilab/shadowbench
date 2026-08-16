\begin{lemma}[IsExtremal]
Let \(V\) be a finite vertex set, and let \(p\) be a property of simple graphs on \(V\).
A simple graph \(G\) on \(V\) is called \emph{extremal with respect to \(p\)} if
\[
p(G)
\quad\text{and}\quad
\text{for every simple graph } G' \text{ on } V \text{ with } p(G'),
\; |E(G')| \le |E(G)|.
\]
\end{lemma}

\begin{theorem}[exists_isExtremal_iff_exists]
Let \(V\) be a finite vertex set, and let \(p\) be a property of simple graphs on \(V\).
Then the following are equivalent:
\[
\exists\, G \text{ on } V \text{ such that } p(G)
\quad\Longleftrightarrow\quad
\exists\, G \text{ on } V \text{ that is extremal with respect to } p.
\]
\end{theorem}

\begin{proof}
The forward implication is immediate, since any extremal graph satisfies \(p\) by definition.

For the reverse implication, assume there exists at least one simple graph on \(V\) satisfying \(p\).
Because the set of simple graphs on a fixed finite vertex set is finite, the number of edges
attained among graphs satisfying \(p\) has a maximum.
Choose a graph \(G\) satisfying \(p\) with the maximum possible number of edges.
Then \(G\) satisfies \(p\), and for any other graph \(G'\) on \(V\) with \(p(G')\),
we have \(|E(G')| \le |E(G)|\).
Thus \(G\) is extremal with respect to \(p\).
\end{proof}
