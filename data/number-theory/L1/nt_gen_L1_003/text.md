\begin{theorem}
Let $n>q>0$ be integers, and let $p$ be a prime satisfying $p\equiv 1\pmod q$. Define
\[
G_{n,q}=\gcd\left\{\binom{n}{qk}: k\in\mathbb{Z},\ 0<qk<n\right\}.
\]
For a positive integer $M$, let $v_p(M)$ denote the largest nonnegative integer $e$ such that $p^e$ divides $M$. Also let $\alpha_p(n)$ be the sum of the digits in the base-$p$ expansion of $n$. Then
\[
v_p(G_{n,q})=
\begin{cases}
1,&\text{if }\alpha_p(n)\le q,\\
0,&\text{otherwise.}
\end{cases}
\]
Equivalently, $\alpha_p(n)$ is the smallest integer $r$ for which
\[
n=p^{i_1}+\cdots+p^{i_r}
\]
with integers $0\le i_1\le\cdots\le i_r$.
\end{theorem}
