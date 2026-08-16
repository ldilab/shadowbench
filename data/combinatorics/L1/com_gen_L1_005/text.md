\begin{theorem}[IsClique.of_subsingleton]
Let \(G\) be a simple graph on a vertex set \(V\).
A subset \(S \subseteq V\) is a \emph{clique} if every two distinct vertices in \(S\) are adjacent in \(G\).
Equivalently, \(S\) is a clique if adjacency holds pairwise on \(S\).
\end{theorem}

\begin{lemma}[isClique_iff_isChain_adj]
A subset \(S \subseteq V\) is a clique if and only if it is a chain for the adjacency relation,
i.e. any two distinct elements of \(S\) are related by adjacency.
\end{lemma}

\begin{proof}
Unfold the definitions: being a clique is exactly the pairwise adjacency condition, which is
the same as being a chain for a symmetric relation.
\end{proof}

\begin{lemma}[isClique_empty]
The empty set is a clique. Every singleton set \(\{a\}\) is a clique.
\end{lemma}

\begin{proof}
Both statements hold because there are no pairs of distinct vertices to check.
\end{proof}

\begin{lemma}[IsClique.of_subsingleton]
If \(S \subseteq V\) has at most one element, then \(S\) is a clique.
\end{lemma}

\begin{proof}
If \(S\) has at most one element, there are no distinct \(v,w \in S\), so the pairwise condition holds vacuously.
\end{proof}

\begin{lemma}[isClique_pair]
For vertices \(a,b \in V\), the set \(\{a,b\}\) is a clique if and only if
\(a \neq b\) implies that \(a\) is adjacent to \(b\).
\end{lemma}

\begin{proof}
The only potentially nontrivial adjacency condition in \(\{a,b\}\) is between \(a\) and \(b\),
and it matters only when \(a \neq b\).
\end{proof}

\begin{theorem}[isClique_insert]
Let \(S \subseteq V\) and \(a \in V\). Then \(S \cup \{a\}\) is a clique if and only if:
(i) \(S\) is a clique, and
(ii) \(a\) is adjacent to every \(b \in S\) with \(b \neq a\).
If moreover \(a \notin S\), then condition (ii) reduces to: \(a\) is adjacent to every \(b \in S\).
\end{theorem}

\begin{proof}
Unfold the pairwise condition on \(S \cup \{a\}\).
Pairs entirely inside \(S\) give (i). Pairs involving \(a\) give (ii). If \(a \notin S\), then \(b \neq a\) holds automatically for \(b \in S\).
\end{proof}

\begin{theorem}[IsClique.mono]
If \(G\) is a subgraph of \(H\), then every clique in \(G\) is a clique in \(H\).
If \(T \subseteq S\) and \(S\) is a clique in \(G\), then \(T\) is also a clique in \(G\).
\end{theorem}

\begin{proof}
Subgraph inclusion preserves adjacency, so the pairwise adjacency condition is preserved.
Similarly, restricting from \(S\) to a subset \(T\) preserves pairwise adjacency.
\end{proof}

\begin{theorem}[isClique_bot_iff]
In the graph with no edges, a subset \(S\) is a clique if and only if \(S\) has at most one element.
\end{theorem}

\begin{proof}
If there are no edges, the only way for all distinct pairs in \(S\) to be adjacent is for there to be no distinct pairs, i.e. \(S\) has at most one element.
\end{proof}

\begin{theorem}[IsClique.map]
Let \(f : V \hookrightarrow W\) be an injective map and let \(G\) be a graph on \(V\).
If \(S \subseteq V\) is a clique in \(G\), then \(f(S) \subseteq W\) is a clique in the image graph \(f_\ast(G)\).
\end{theorem}

\begin{proof}
Distinct vertices in \(f(S)\) come from distinct vertices in \(S\) by injectivity.
Adjacency in the image graph is defined by adjacency of preimages, so pairwise adjacency is preserved.
\end{proof}

\begin{theorem}[isClique_map_iff_of_nontrivial]
Let \(f : V \hookrightarrow W\) be injective and let \(T \subseteq W\) be a nontrivial set (containing at least two distinct elements).
Then \(T\) is a clique in the image graph \(f_\ast(G)\) if and only if there exists a set \(S \subseteq V\)
such that \(S\) is a clique in \(G\) and \(f(S)=T\).
\end{theorem}

\begin{proof}
(\(\Rightarrow\)) Take \(S = f^{-1}(T)\). Using injectivity, adjacency of two elements of \(S\) follows from adjacency of their images in \(T\), so \(S\) is a clique, and \(f(S)=T\) holds under the nontriviality assumption.

(\(\Leftarrow\)) If \(T=f(S)\) for a clique \(S\), then the previous lemma shows \(T\) is a clique in the image graph.
\end{proof}
