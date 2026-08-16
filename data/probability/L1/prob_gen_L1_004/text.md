\begin{theorem}[Finite-sample $m$-dependence inequality]
Let $m\geq1$ and $N\geq1$ be integers, and let
$(A_k)_{1\leq k\leq N}$ be events on a probability space. Say that this
family is $m$-dependent if, whenever $I,J\subseteq\{1,\ldots,N\}$ and
$|i-j|>m$ for every $i\in I$ and $j\in J$, the sigma-algebras generated
by $(A_i)_{i\in I}$ and $(A_j)_{j\in J}$ are independent. Define
\[
S_N=\sum_{k=1}^{N}\mathbb{P}(A_k).
\]
If $(A_k)_{1\leq k\leq N}$ is $m$-dependent, then
\[
\mathbb{P}\!\left(\bigcup_{k=1}^{N}A_k\right)
\geq 1-\exp\!\left(-\frac{S_N}{m+1}\right).
\]
\end{theorem}
