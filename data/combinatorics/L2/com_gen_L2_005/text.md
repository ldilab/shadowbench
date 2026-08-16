\begin{definition}[IsBipartiteWith]
Let \(G\) be a simple graph on a vertex set \(V\), and let \(s,t \subseteq V\).
We say that \(G\) is \emph{bipartite with respect to \(s\) and \(t\)} if:
\begin{enumerate}
\item \(s\) and \(t\) are disjoint, and
\item every edge of \(G\) connects a vertex in \(s\) to a vertex in \(t\)
      (in one direction or the other).
\end{enumerate}
\end{definition}

\begin{theorem}[isBipartiteWith_sum_degrees_eq_card_edges]
Let \(G\) be a finite simple graph, and let \(s,t \subseteq V\) be a bipartition of \(G\)
in the above sense. Then
\[
\sum_{v \in s} \deg_G(v) \;=\; |E(G)|.
\]
\end{theorem}

\begin{proof}
Each edge of a bipartite graph has exactly one endpoint in \(s\) and the other endpoint in \(t\).
When summing degrees over \(s\), every edge is counted exactly once (via its unique endpoint in \(s\)).
Therefore the sum of degrees over \(s\) equals the total number of edges.
\end{proof}
