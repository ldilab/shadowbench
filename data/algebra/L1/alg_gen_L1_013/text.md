\begin{theorem}[zariskiClosure_is_smallest_algebraic_set]
If $S \subseteq k^n$, the affine algebraic set $\mathbf{V}(\mathbf{I}(S))$ is the \emph{smallest algebraic set that contains} $S$ [in the sense that if $W \subseteq k^n$ is any affine algebraic set containing $S$, then $\mathbf{V}(\mathbf{I}(S)) \subseteq W$].
\end{theorem}

\begin{proof}
If $W \supseteq S$, then $\mathbf{I}(W) \subseteq \mathbf{I}(S)$ because $\mathbf{I}$ is inclusion-reversing. But then $\mathbf{V}(\mathbf{I}(W)) \supseteq \mathbf{V}(\mathbf{I}(S))$ because $\mathbf{V}$ also reverses inclusions. Since $W$ is an affine algebraic set, $\mathbf{V}(\mathbf{I}(W)) = W$ by The Ideal–Variety Correspondence, and the result follows.
\end{proof}
