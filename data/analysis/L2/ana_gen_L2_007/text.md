\begin{theorem}[diagonal_compact_iff_tendsto_zero]
Suppose $T$ is a bounded operator on a Hilbert space $\mathcal{H}$ which is diagonal with respect to an orthonormal basis $\{\varphi_k\}_{k=1}^{\infty}$, that is,
\[
T\varphi_k = \lambda_k \varphi_k .
\]
Then $T$ is compact if and only if $\lambda_k \to 0$.
\end{theorem}

\begin{proof}
Suppose first that $T$ is compact. Since $\{\varphi_k\}$ is bounded, 
$\{T\varphi_k\}$ has a convergent subsequence. But
\[
T\varphi_k=\lambda_k\varphi_k.
\]
If $\lambda_k\nrightarrow 0$, then for some $\varepsilon>0$ there is a subsequence
$\{\lambda_{k_j}\}$ with $|\lambda_{k_j}|\ge \varepsilon$. Then, for $i\ne j$,
\[
\|T\varphi_{k_i}-T\varphi_{k_j}\|^2
=
|\lambda_{k_i}|^2+|\lambda_{k_j}|^2
\ge 2\varepsilon^2,
\]
so this subsequence has no convergent subsequence, a contradiction. Hence
$\lambda_k\to 0$.

Conversely, assume $\lambda_k\to 0$. Let $P_n$ be the orthogonal projection onto
$\operatorname{span}\{\varphi_1,\dots,\varphi_n\}$. Then $P_nT$ has finite rank, hence is compact. Moreover,
\[
\|P_nT-T\|
=
\sup_{k>n}|\lambda_k|
\to 0.
\]
Thus $T$ is the norm limit of compact operators, and therefore compact.
\end{proof}
