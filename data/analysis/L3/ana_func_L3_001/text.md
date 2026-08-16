\begin{theorem}[exists_projection_near_of_approx_selfadj_idempotent]
Let $\mathcal A$ be a $C^*$-algebra. Show that for any $\varepsilon > 0$ there exists a
$\delta_\varepsilon > 0$ such that if $a \in \mathcal A$ obeys
\[
    \max\left\{\|a-a^*\|,\ \|a^2-a\|\right\}\le \delta_\varepsilon,
\]
then there exists a self-adjoint projection $p\in \mathcal A$ with
\[
    \|a-p\|\le \varepsilon.
\]
\end{theorem}

\begin{proof}
Fix $\varepsilon>0$. Choose $\delta>0$ sufficiently small, to be specified later, and suppose
$a\in\mathcal A$ satisfies
\[
    \max\{\|a-a^*\|,\|a^2-a\|\}\le \delta .
\]
Put
\[
    b=\frac{a+a^*}{2}.
\]
Then $b=b^*$ and
\[
    \|a-b\|=\frac12\|a-a^*\|\le \frac{\delta}{2}.
\]
Moreover,
\[
    b^2-b
    =
    \frac12\bigl((a^2-a)+(a^2-a)^*\bigr)
    -\frac14(a-a^*)^2,
\]
so
\[
    \|b^2-b\|
    \le
    \|a^2-a\|+\frac14\|a-a^*\|^2
    \le
    \delta+\frac{\delta^2}{4}.
\]
Set
\[
    \eta:=\delta+\frac{\delta^2}{4}.
\]

Since $b$ is self-adjoint, $\sigma(b)\subset\mathbb R$. By the spectral mapping theorem, for every
$\lambda\in\sigma(b)$,
\[
    |\lambda(\lambda-1)|
    =
    |\lambda^2-\lambda|
    \le
    \|b^2-b\|
    \le \eta .
\]
Assume $\delta$ is chosen so that $\eta<1/4$. Then $1/2\notin\sigma(b)$.

Define
\[
    f:\sigma(b)\to\mathbb C,\qquad
    f(\lambda)=
    \begin{cases}
    0, & \lambda<1/2,\\
    1, & \lambda>1/2.
    \end{cases}
\]
This is continuous on $\sigma(b)$. Let
\[
    p=f(b)
\]
via the continuous functional calculus. Since $f$ is real-valued and $f^2=f$, we have
\[
    p^*=p,\qquad p^2=p.
\]
Thus $p$ is a self-adjoint projection.

It remains to estimate the distance. If $\lambda\in\sigma(b)$ and $\lambda<1/2$, then
$|1-\lambda|\ge 1/2$, hence
\[
    |\lambda|\le 2|\lambda(1-\lambda)|\le 2\eta.
\]
If $\lambda>1/2$, then $|\lambda|\ge 1/2$, hence
\[
    |\lambda-1|\le 2|\lambda(\lambda-1)|\le 2\eta.
\]
Thus
\[
    |\lambda-f(\lambda)|\le 2\eta
    \qquad(\lambda\in\sigma(b)).
\]
By the isometric property of the continuous functional calculus,
\[
    \|b-p\|
    =
    \|b-f(b)\|
    \le 2\eta.
\]
Therefore
\[
    \|a-p\|
    \le
    \|a-b\|+\|b-p\|
    \le
    \frac{\delta}{2}
    +2\left(\delta+\frac{\delta^2}{4}\right).
\]

Finally choose
\[
    0<\delta_\varepsilon\le
    \min\left\{\frac15,\frac{\varepsilon}{3}\right\}.
\]
Then $\eta<1/4$ and
\[
    \frac{\delta_\varepsilon}{2}
    +2\left(\delta_\varepsilon+\frac{\delta_\varepsilon^2}{4}\right)
    \le \varepsilon.
\]
Hence $\|a-p\|\le\varepsilon$, as required.
\end{proof}
