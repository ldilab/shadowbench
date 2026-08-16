\begin{definition}[fintypeSubtypeWalkLength]
Let \(G\) be a locally finite simple graph with vertex set \(V\).
For \(n \in \mathbb{N}\) and vertices \(u,v \in V\), define a finite set
\[
\mathcal{W}_n(u,v)
\]
of walks of length \(n\) from \(u\) to \(v\) recursively by:
\begin{itemize}
\item If \(n=0\), then \(\mathcal{W}_0(u,v)\) consists of the trivial walk if \(u=v\), and is empty otherwise.
\item If \(n+1\), then \(\mathcal{W}_{n+1}(u,v)\) consists of all walks obtained by choosing a neighbor
\(w\) of \(u\) and prepending the edge \(u\sim w\) to a walk in \(\mathcal{W}_n(w,v)\).
\end{itemize}
\end{definition}

\begin{theorem}[set_walk_length_toFinset_eq]
For all \(n \in \mathbb{N}\) and vertices \(u,v \in V\),
\[
\mathcal{W}_n(u,v)
=
\{\, p \mid p \text{ is a walk from } u \text{ to } v \text{ of length } n \,\}.
\]
\end{theorem}

\begin{proof}
By induction on \(n\).
For \(n=0\), the only walk of length zero is the trivial walk at a vertex.
For \(n+1\), every walk of length \(n+1\) is uniquely determined by its first edge and a walk
of length \(n\) from the adjacent vertex to \(v\).
\end{proof}

\begin{theorem}[card_set_walk_length_eq]
For all \(n \in \mathbb{N}\) and vertices \(u,v \in V\),
\[
\bigl|\{\, p \mid p \text{ is a walk from } u \text{ to } v \text{ of length } n \,\}\bigr|
=
|\mathcal{W}_n(u,v)|.
\]
\end{theorem}

\begin{proof}
By the previous theorem, \(\mathcal{W}_n(u,v)\) contains exactly all walks of length \(n\)
from \(u\) to \(v\).
Since \(G\) is locally finite, this set is finite, so the cardinalities coincide.
\end{proof}
