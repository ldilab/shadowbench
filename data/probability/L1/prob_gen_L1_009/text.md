\begin{lemma}[Approximate independence under $\varphi$-mixing]
For sub-sigma-algebras $\mathcal{A},\mathcal{B}$ of a probability space,
write
\[
\varphi(\mathcal{A},\mathcal{B})
=\sup\left\{
\left\lvert\frac{\mathbb{P}(E\cap F)}{\mathbb{P}(E)}
-\mathbb{P}(F)\right\rvert:
E\in\mathcal{A},\ F\in\mathcal{B},\ \mathbb{P}(E)>0
\right\}.
\]
Let $M\geq1$ and $\varphi_{\star}\geq0$. Let
$\mathcal{A}_1,\ldots,\mathcal{A}_M$ be sub-sigma-algebras such
that, for $1\leq r\leq M-1$,
\[
\varphi\!\left(
\sigma(\mathcal{A}_1\cup\cdots\cup\mathcal{A}_r),
\mathcal{A}_{r+1}\right)\leq\varphi_{\star}.
\]
Let $C_j\in\mathcal{A}_j$ and set $u_j=\mathbb{P}(C_j)$. Then
\[
\mathbb{P}\!\left(\bigcap_{j=1}^{M}C_j^c\right)
\leq
\prod_{j=1}^{M}\min\!\left(1,1-u_j+\varphi_{\star}\right)
\leq
\exp\!\left(-\sum_{j=1}^{M}(u_j-\varphi_{\star})_+\right),
\]
where $(x)_+=\max(x,0)$.
\end{lemma}
