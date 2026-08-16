\begin{theorem}[exists_seq_finite_rank_strongly_convergent_to]
Consider a separable Hilbert space $\mathcal{H}$.
Show that for any bounded operator $T$ there is a sequence $\{T_n\}$ of bounded operators of finite rank so that $T_n \to T$ strongly as $n \to \infty$.
\end{theorem}

\begin{proof}
Let $(g_k)_{k=1}^{\infty}$ be a orthonormal basis of $\mathcal{H}$. Let $T_n g_k = T g_k$ for $k \le n$ and $T_n g_k = 0$ for $k > n$. Then each $T_n$ has finite rank (i.e. dimension of range is finite) and $\|T_n g_k - T g_k\| = 0$ for $n$ sufficiently large. For an arbitrary vector $g$, applying the triangle inequality gives $\|T_n g - T g\| = 0$ for $n$ sufficiently large.
\end{proof}
