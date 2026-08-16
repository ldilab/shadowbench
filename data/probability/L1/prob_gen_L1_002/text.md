\begin{theorem}[Quantitative second Borel--Cantelli lemma]
Let $(A_i)_{i=1}^{\infty}$ be mutually independent events. Suppose that
$\omega:\mathbb{N}_{>0}\to\mathbb{N}_{>0}$ is a rate of divergence for
their cumulative probabilities, meaning that
\[
\sum_{i=1}^{\omega(N)}\mathbb{P}(A_i)\geq N
\qquad\text{for every }N\geq 1.
\]
Then, for all $n,N\geq 1$,
\[
\mathbb{P}\!\left(\bigcup_{i=n}^{\omega(n+N-1)}A_i\right)
\geq 1-e^{-N}.
\]
\end{theorem}
