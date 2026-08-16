\begin{theorem}[integral_cos_sq_tendsto_half_measure]
If $f$ is integrable on $[0, 2\pi]$, then $\int_0^{2\pi} f(x) e^{-inx} dx \to 0$ as $|n| \to \infty$. Show as a consequence that if $E$ is a measurable subset of $[0, 2\pi]$, then
\[ \int_E \cos^2(nx + u_n) dx \to \frac{m(E)}{2}, \quad \text{as } n \to \infty \]
for any sequence $\{u_n\}$.
\end{theorem}

\begin{proof}
First, note that $\int_0^{2\pi} f(x) \cos(nx) dx \to 0$ and $\int_0^{2\pi} f(x) \sin(nx) \to 0$ since these are the real and imaginary parts of $\int_0^{2\pi} f(x) e^{-inx} dx$. In particular, if we let $f(x) = \chi_E(x)$ for some measurable $E \subset [0, 2\pi]$, then for any $\epsilon > 0$, $\exists N$ such that $\left| \int_0^{2\pi} \chi_E(x) \sin(nx) dx \right|$ and $\left| \int_0^{2\pi} \chi_E(x) \cos(nx) dx \right|$ are both less than $\frac{\epsilon}{2}$ provided $|n| > N$. Then for any sequence $u_n$,
\begin{align*}
\left| \int_E \cos(2nx + 2u_n) dx \right| &= \left| \int_E \cos(2nx) \cos(2u_n) - \sin(2nx) \sin(2u_n) dx \right| \\
&= \left| \cos(2u_n) \int_0^{2\pi} \chi_E(x) \cos(2nx) dx - \sin(2u_n) \int_0^{2\pi} \chi_E(x) \sin(2nx) dx \right| \\
&\le |\cos(2u_n)| \left| \int_0^{2\pi} \chi_E(x) \cos(2nx) dx \right| + |\sin(2u_n)| \left| \int_0^{2\pi} \chi_E(x) \sin(2nx) dx \right| \\
&\le 1 \cdot \frac{\epsilon}{2} + 1 \cdot \frac{\epsilon}{2} = \epsilon
\end{align*}
for $|n| > N$. Hence $\int_E \cos(2nx + 2u_n) dx \to 0$ as $|n| \to \infty$. Now
\begin{align*}
\int_E \cos^2(nx + u_n) dx &= \int_E \frac{1}{2} (1 + \cos(2(nx + u_n))) dx \\
&= \frac{m(E)}{2} + \frac{1}{2} \int_0^{2\pi} \chi_E(x) \cos(2nx + 2u_n) dx
\end{align*}
and we have shown that the second term tends to $0$ as $|n| \to \infty$. \qed
\end{proof}
