\begin{theorem}[Generalization of Cantelli's inequality]
Let $X$ be a real-valued random variable with finite variance
$\operatorname{Var}(X)=\sigma^2$ and mean $\mathbb{E}[X]$. Let $n\geq 1$
and suppose
\[
0<\lambda_1<\lambda_2<\cdots<\lambda_n<\infty.
\]
Set $\lambda_0=-\sigma^2/\lambda_1$. Then
\[
\sum_{k=1}^{n}
\frac{(\lambda_1\lambda_k+\sigma^2)^2
      -(\lambda_1\lambda_{k-1}+\sigma^2)^2}
     {(\lambda_1^2+\sigma^2)^2}
\mathbb{P}\!\left(X-\mathbb{E}[X]\geq\lambda_k\right)
\leq \frac{\sigma^2}{\sigma^2+\lambda_1^2}.
\]
\end{theorem}
