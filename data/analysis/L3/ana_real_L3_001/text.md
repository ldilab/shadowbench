\begin{theorem}[hilbertT_bounded_norm_one]
Prove that the operator
\[
Tf(x)=\frac{1}{\pi}\int_0^\infty \frac{f(y)}{x+y}\,dy
\]
is bounded on $L^2(0,\infty)$ with norm $\|T\|=1$.
\end{theorem}

\begin{proof}
We first prove the upper bound. Since \(C_c(0,\infty)\) is dense in
\(L^2(0,\infty)\), it suffices to prove the estimate first for
\(f,g\in C_c(0,\infty)\). 
\[
\begin{aligned}
\left|\int_0^\infty Tf(x)\overline{g(x)}\,dx\right|
&=
\left|
\frac1\pi\int_0^\infty\int_0^\infty
\frac{f(xt)\overline{g(x)}}{1+t}\,dx\,dt
\right|  \\
&\le
\frac1\pi\int_0^\infty
\frac{1}{1+t}
\left|
\int_0^\infty f(xt)\overline{g(x)}\,dx
\right|dt  \\
&\le
\frac1\pi\int_0^\infty
\|f\|_2\|g\|_2\frac{t^{-1/2}}{1+t}\,dt  \\
&=
\|f\|_2\|g\|_2 .
\end{aligned}
\]
Thus $\|Tf\|_2\le \|f\|_2$, and hence $\|T\|\le 1$.

For the lower bound, let $\lambda>1$ and define
\[
f_\lambda(y)=
\begin{cases}
y^{-1/2}, & 1\le y\le \lambda,\\
0, & \text{otherwise}.
\end{cases}
\]
Then
\[
\|f_\lambda\|_2=\sqrt{\log \lambda}.
\]
Moreover,
\[
\begin{aligned}
Tf_\lambda(x)
&=
\frac1\pi\int_1^\lambda \frac{y^{-1/2}}{x+y}\,dy  \\
&=
\frac{1}{\pi\sqrt{x}}
\int_{1/x}^{\lambda/x}\frac{t^{-1/2}}{1+t}\,dt  \\
&=
\frac{2}{\pi\sqrt{x}}
\int_{\sqrt{1/x}}^{\sqrt{\lambda/x}}
\frac{1}{1+u^2}\,du  \\
&=
\frac{2}{\pi\sqrt{x}}
\left(
\tan^{-1}\sqrt{\frac{\lambda}{x}}
-
\tan^{-1}\sqrt{\frac1x}
\right) \\
&=
\frac{2}{\pi\sqrt{x}}
\tan^{-1}
\left(
\frac{(1-\lambda^{-1/2})\sqrt{x}}{1+x/\sqrt{\lambda}}
\right).
\end{aligned}
\]
Hence, for any $0 < \alpha < 1/2$,
\[
\begin{aligned}
\frac{\|Tf_\lambda\|_2^2}{\|f_\lambda\|_2^2}
&=
\frac1{\log\lambda}
\int_0^\infty |Tf_\lambda(x)|^2\,dx  \\
&\ge
\frac{4}{\pi^2\log\lambda}
\int_{\lambda^\alpha}^{\lambda^{1-\alpha}}
\frac1x
\left[
\tan^{-1}
\left(
\frac{1-\lambda^{-1/2}}{2}\lambda^{\alpha/2}
\right)
\right]^2
dx  \\
&=
(1-2\alpha)\frac{4}{\pi^2}
\left[
\tan^{-1}
\left(
\frac{1-\lambda^{-1/2}}{2}\lambda^{\alpha/2}
\right)
\right]^2 .
\end{aligned}
\]
Letting $\lambda\to\infty$, we obtain
\[
\liminf_{\lambda\to\infty}
\frac{\|Tf_\lambda\|_2^2}{\|f_\lambda\|_2^2}
\ge
1-2\alpha .
\]
Since $0 < \alpha < 1/2$ is arbitrary, $\|T\|\ge 1$.  Together with
$\|T\|\le 1$, this gives
\[
\|T\|=1.
\]
\end{proof}
