\begin{lemma}[Fourier_transform_integrable]
Let $V$ be a finite-dimensional real inner product space, equipped with its Borel $\sigma$-algebra and a measure $dv$.

Let $E$ be a complex normed vector space (assumed complete when needed), and let $f : V \to E$.

We write the Fourier transform and inverse Fourier transform as follows:
\[
(\mathcal{F}f)(w) \;=\; \int_V e^{-2\pi i \langle w,x\rangle}\, f(x)\,dx,
\qquad
(\mathcal{F}^{-}g)(v) \;=\; \int_V e^{2\pi i \langle w,v\rangle}\, g(w)\,dw.
\]
\end{lemma}


\begin{lemma}[tendsto_integral_cexp_sq_smul] If $f$ is integrable, then as $c$ tends to infinity,
\[
\int_V e^{-c^{-1}\|v\|^2}\, f(v)\,dv
\;\xrightarrow{}\;
\int_V f(v)\,dv .
\]
\end{lemma}
\begin{proof}
We shall apply the dominated convergence theorem. 

(i) \, For each fixed $v \in V$, we have
\[e^{-c^{-1}\|v\|^2}\, f(v)
\;\longrightarrow\;
f(v)\]
as $c \to +\infty$. Moreover, for all sufficiently large $c$,
\[
\|e^{-c^{-1}\|v\|^2}\, f(v)\| \le \|f(v)\|
\]

(ii) \, For each $c \in \mathbb{R}$, the function
\[
v \longmapsto e^{-\frac{1}{c}\,\|v\|^2}
\]
is continuous, hence measurable. Since $f$ is integrable, it is
almost everywhere strongly measurable. Therefore the product
\[
v \longmapsto e^{-\frac{1}{c}\,\|v\|^2}\, f(v)
\]
is almost everywhere strongly measurable for each $c$.

(iii) \, Restrict to $c \ge 0$. Then for all $v \in V$,
\[
\bigl\| e^{-\frac{1}{c}\,\|v\|^2}\, f(v) \bigr\|
=
\bigl| e^{-\frac{1}{c}\,\|v\|^2} \bigr|\, \|f(v)\|
=
e^{-\frac{1}{c}\,\|v\|^2}\, \|f(v)\|
\;\le\;
\|f(v)\|.
\]
The function $v \mapsto \|f(v)\|$ is integrable by assumption, so it
dominates the integrand for all sufficiently large $c$.

Now, we may apply the dominated convergence theorem and conclude that
\[
\lim_{c \to +\infty}
\int_V e^{-\frac{1}{c}\,\|v\|^2}\, f(v)\, d\mu(v)
=
\int_V f(v)\, d\mu(v),
\]
as claimed.
\end{proof}
