\begin{theorem}[compactOpen_strictly_weaker_than_supNorm]
    Show that the compact open topology is strictly weaker than the sup-norm topology on $C_b ([0, \infty) \to \mathbb{C})$, the set of continuous bounded maps.
\end{theorem}

\begin{proof}
If $\|f_n-f\|_\infty\to 0$, then for every compact set $K\subset [0,\infty)$,
\[
\sup_{x\in K}|f_n(x)-f(x)|\le \|f_n-f\|_\infty \to 0.
\]
Thus convergence in the sup-norm topology implies convergence in the compact-open
topology, i.e. the compact-open topology is weaker than the sup-norm topology.

To show that it is strictly weaker, consider a continuous function $f$ supported
on $[0,1]$ with $\|f\|_\infty=1$, and define
\[
f_n(x)=f(x-n).
\]
For any compact set $K\subset [0,\infty)$, $K$ is bounded, so for all sufficiently
large $n$ the support of $f_n$ is disjoint from $K$. Hence $f_n\to 0$ uniformly on
every compact subset of $[0,\infty)$, so $f_n\to 0$ in the compact-open topology.

However,
\[
\|f_n\|_\infty=\|f\|_\infty=1
\]
for every $n$, so $f_n$ does not converge to $0$ in the sup-norm topology. Therefore
the compact-open topology on $C_b([0,\infty),\mathbb C)$ is strictly weaker than
the sup-norm topology.
\end{proof}
