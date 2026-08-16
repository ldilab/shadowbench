\begin{theorem}[IsQuasiSeparated.image_of_isEmbedding]
Let $S \subseteq X$ be a quasiseparated set and $h:X \to Y$ is a topological embedding. Then, $f(S)$ is quasiseparated.
\end{theorem}

\begin{proof}
Let $U,V$ be compact open subsets of $f(S)$. Since $f$ is an embedding, $f^{-1}(U), f^{-1}(V)$ are compact open subsets of $S$. Then $f^{-1}(U) \cap f^{-1}(V)$ is compact since $S$ is quasiseparated. Hence, $U \cap V = f(f^{-1}(U) \cap f^{-1}(V))$ is compact and thus $f(S)$ is quasiseparated.
