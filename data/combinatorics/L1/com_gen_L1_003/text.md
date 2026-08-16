\begin{definition}[IsBipartiteWith]
Let \(G\) be a simple graph with vertex set \(V\), and let \(s,t \subseteq V\).
The graph \(G\) is said to be \emph{bipartite with respect to \(s\) and \(t\)} if:
\begin{enumerate}
\item the sets \(s\) and \(t\) are disjoint, and
\item for every edge \(\{v,w\}\) of \(G\), either \(v \in s\) and \(w \in t\),
      or \(v \in t\) and \(w \in s\).
\end{enumerate}
\end{definition}

\begin{theorem}[IsBipartiteWith.symm]
If a simple graph \(G\) is bipartite with respect to sets \(s\) and \(t\),
then it is also bipartite with respect to \(t\) and \(s\).
\end{theorem}

\begin{proof}
Disjointness is symmetric, so \(t\) and \(s\) are disjoint.
Moreover, if an edge connects a vertex in \(s\) to a vertex in \(t\),
then the same edge connects a vertex in \(t\) to a vertex in \(s\) when the roles
of the two sets are swapped.
\end{proof}
