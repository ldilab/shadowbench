\begin{lemma}[tendsto_integral_gaussian_smul] Suppose that  $f\in L^{1}(V;E)$ and $f$  is continuous at $v\in V$. Then we have:
    \[
\lim_{c\to\infty}
\int_{w\in V}
\Bigl((\pi c)^{\frac{\dim_{\mathbb R}V}{2}}\;
e^{-\pi^{2}c\,\|v-w\|^{2}}\Bigr)\, f(w)\,d\mu(w)
= f(v),
\]
under the hypotheses that $f$ is integrable and continuous at $v$.
\end{lemma}

\begin{proof}
Define the fixed Gaussian
\[
\varphi(w) := \pi^{\frac n2} e^{-\pi^2 \|w\|^2},
\qquad w \in V.
\]
Consider the family of kernels
\[
K_c(w) := c^n\, \varphi(c w), \qquad c > 0.
\]
Then
\[
\int_V K_c(w)\, d\mu(w)
=
\int_V c^n \varphi(c w)\, d\mu(w)
= 1,
\]
by the standard Gaussian integral formula. Moreover, $K_c \ge 0$ and the family $\{K_c\}_{c>0}$ concentrates at the origin:
for any $\varepsilon>0$,
\[
\int_{\|w\|>\varepsilon} K_c(w)\, d\mu(w) \longrightarrow 0
\qquad (c\to\infty),
\]
since $\varphi$ has exponential decay and $t^{\alpha} e^{-t} \to 0$ as $t \to \infty$ for any $\alpha>0$.

By the standard approximate identity theorem, using the integrability of $f$ and continuity of $f$ at $v$, we obtain
\[
\lim_{c \to \infty}
\int_V c^n \varphi\bigl(c(v-w)\bigr)\, f(w)\, d\mu(w)
= f(v).
\]
Replacing $c$ by $c^{1/2}$ yields
\begin{equation} \tag{$\dagger$}
\lim_{c \to \infty}
\int_V (c^{1/2})^n \varphi\bigl((c^{1/2})(v-w)\bigr)\, f(w)\, d\mu(w)
= f(v),
\end{equation}
For $c>0$ and all $w\in V$, we compute
\[
(c^{1/2})^n \varphi\bigl((c^{1/2})(v-w)\bigr)
=
\pi^{\frac n2} c^{\frac n2}
\exp\!\bigl(-\pi^2 \|(c^{1/2})(v-w)\|^2\bigr).
\]
Since $\|(c^{1/2})(v-w)\|^2 = c\,\|v-w\|^2$, this simplifies to
\[
(\pi c)^{\frac n2} e^{-\pi^2 c \|v-w\|^2}.
\]


Therefore, for all sufficiently large $c$, the integrand in ($\dagger$) coincides with the integrand in the statement. Hence,
\[
\lim_{c \to \infty}
\int_V
(\pi c)^{\frac n2} e^{-\pi^2 c \|v-w\|^2}\, f(w)\, d\mu(w)
= f(v),
\]
as claimed.
\end{proof}
