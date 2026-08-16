\begin{theorem}[isClique_iff]
Let \(G\) be a simple graph on a vertex set \(V\).
A subset \(S \subseteq V\) is a \emph{clique} if it is pairwise adjacent, i.e.
for all distinct \(v,w \in S\), the vertices \(v\) and \(w\) are adjacent in \(G\).
\end{theorem}

\begin{lemma}[not_isClique_iff]
Let \(S \subseteq V\). Then \(S\) is not a clique if and only if there exist distinct vertices
\(v,w \in S\) such that \(v\) is not adjacent to \(w\) in \(G\).
\end{lemma}

\begin{proof}
If \(S\) is not pairwise adjacent, then by negating the defining condition there exist
\(v,w \in S\) with \(v \ne w\) and \(\neg\,\mathrm{Adj}_G(v,w)\).
Conversely, the existence of such a pair directly contradicts pairwise adjacency.
\end{proof}

\begin{theorem}[isClique_iff_induce_eq]
Let \(S \subseteq V\). Then \(S\) is a clique in \(G\) if and only if the induced subgraph \(G[S]\)
is the complete graph on the vertex set \(S\).
\end{theorem}

\begin{proof}
Assume \(S\) is a clique. Then any two distinct vertices \(v,w \in S\) are adjacent in \(G\),
hence adjacent in the induced subgraph \(G[S]\). Therefore \(G[S]\) has exactly the edges of the
complete graph on \(S\).

Conversely, if \(G[S]\) is complete, then any two distinct vertices \(v,w \in S\) are adjacent in
\(G[S]\), hence adjacent in \(G\). Thus \(S\) is pairwise adjacent, i.e. a clique.
\end{proof}
