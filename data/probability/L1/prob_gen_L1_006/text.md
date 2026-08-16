\begin{theorem}[Strengthened Chernoff bound]
Let $X_1,\ldots,X_n$ be indicator random variables. Let $k,t$ be
integers with $0<k<t\leq n$, and let $0<\beta<1$ satisfy $t=\beta n$.
Then
\[
\mathbb{P}\!\left(\sum_{i=1}^{n}X_i\geq t\right)
\leq
\frac{1}{\binom{t}{k}}
\sum_{\substack{S\subseteq\{1,\ldots,n\}\\|S|=k}}
\mathbb{P}\!\left(\bigwedge_{i\in S}(X_i=1)\right).
\]

In particular, let $0<\alpha<\beta$ and suppose
\[
k=\left(\frac{\beta-\alpha}{1-\alpha}\right)n
\]
is an integer. If
\[
\mathbb{P}\!\left(\bigwedge_{i\in S}(X_i=1)\right)\leq\alpha^k
\]
for every $k$-element subset $S\subseteq\{1,\ldots,n\}$, then
\[
\mathbb{P}\!\left(\sum_{i=1}^{n}X_i\geq t\right)
\leq \exp\!\left(-D(\beta\mathbin\|\alpha)n\right),
\]
where the binary relative entropy is
\[
D(\beta\mathbin\|\alpha)
=\beta\log\!\left(\frac{\beta}{\alpha}\right)
+(1-\beta)\log\!\left(\frac{1-\beta}{1-\alpha}\right).
\]
\end{theorem}
