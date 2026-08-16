\begin{theorem}[Generalization of Hoeffding's inequality]
Let $X_1,\ldots,X_N$ be independent random variables such that
$X_i\in[a_i,b_i]$ almost surely for $1\leq i\leq N$, and set
$S_N=\sum_{i=1}^{N}X_i$. Assume
\[
\sum_{i=1}^{N}(b_i-a_i)^2>0
\quad\text{and}\quad
0<\lambda_1<\lambda_2<\cdots<\lambda_n<\infty.
\]
With $\lambda_0=-\infty$, one has
\[
\sum_{k=1}^{n}
\left[
\exp\!\left((\lambda_k-\lambda_1)
  \frac{4\lambda_1}{\sum_{i=1}^{N}(b_i-a_i)^2}\right)
-
\exp\!\left((\lambda_{k-1}-\lambda_1)
  \frac{4\lambda_1}{\sum_{i=1}^{N}(b_i-a_i)^2}\right)
\right]
\mathbb{P}\!\left(S_N-\mathbb{E}[S_N]\geq\lambda_k\right)
\leq
\exp\!\left(-\frac{2\lambda_1^2}
{\sum_{i=1}^{N}(b_i-a_i)^2}\right).
\]
\end{theorem}
