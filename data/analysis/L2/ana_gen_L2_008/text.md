\begin{theorem}[intervalIntegrable_g_and_integral_g_eq_integral]
Suppose $f$ is integrable on $[0, b]$, and
\[
g(x) = \int_x^b \frac{f(t)}{t} dt \quad \text{for } 0 < x \le b.
\]
Prove that $g$ is integrable on $[0, b]$ and
\[
\int_0^b g(x) dx = \int_0^b f(t) dt.
\]
\end{theorem}

\begin{proof}
We first assume that \(f(x) \geq 0\). Then \(g(x) \geq 0\) as well.
This is enough, since in general we can write
\[
f=f^{+}-f^{-},
\]
and use the linearity of the Lebesgue integral.

For \(f \geq 0\), Tonelli's theorem allows us to interchange the order of
integration. Thus
\[
\begin{aligned}
\int_{0}^{b} g(x)\,dx
&= \int_{0}^{b} \int_{x}^{b} \frac{f(t)}{t}\,dt\,dx \\
&= \int_{0}^{b} \int_{0}^{b}
\frac{f(t)}{t}\chi_{\{t\geq x\}}(t)\,dx\,dt \\
&= \int_{0}^{b} \frac{f(t)}{t}
\int_{0}^{b}\chi_{\{x\leq t\}}(x)\,dx\,dt \\
&= \int_{0}^{b} \frac{f(t)}{t}
\int_{0}^{t} dx\,dt \\
&= \int_{0}^{b} \frac{f(t)}{t}t\,dt \\
&= \int_{0}^{b} f(t)\,dt.
\end{aligned}
\]
Since \(f\) is integrable on \([0,b]\), the last integral is finite. Hence
\(g\) is integrable on \([0,b]\).

Finally, applying the same argument to \(f^{+}\) and \(f^{-}\), and using
linearity, we obtain
\[
\int_{0}^{b} g(x)\,dx=\int_{0}^{b} f(t)\,dt.
\]
\end{proof}
