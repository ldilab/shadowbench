\begin{definition}[fourierIntegral] Let $K$ be a commutative ring and let $V, W$ be modules over $K$. 

Let $E$ be a complete normed  $\mathbb{C}$-vector space, $\mu$ be a measure on $V$, $L : V \times W \to K$ a bilinear form, and let $e : K \to \mathbb{S}$ be an additive character.  
For a function $f : V \to E$, its Fourier transform is defined:
\[
\widehat{f}_{e,\mu,L}(w)
\;:=\;
\int_V e\!\bigl(-L(v,w)\bigr)\, f(v)\, d\mu(v),
\qquad w \in W.
\]
We define $\mathcal F_{e,\mu,L}(f) = \widehat{f}_{e,\mu,L}$.
\end{definition}


\begin{theorem}[fourierIntegral_const_smul]
Let $r \in \mathbb{C}$. Then $
\mathcal F_{e,\mu,L}(r \cdot f)
\;=\;
r \cdot \widehat{f}_{e,\mu,L}. $
\end{theorem}
\begin{proof}
    We show that the two functions are equal at any $w \in W$.
\[
\begin{aligned}
\hat{rf}_{e,\mu,L}(w)
&=
\int_V e\!\bigl(-L(v,w)\bigr)\, (r \cdot f(v))\, d\mu(v) \\
&=
r \int_V e\!\bigl(-L(v,w)\bigr)\, f(v)\, d\mu(v)
\qquad\text{(linearity of the integral)} \\
&=
r \cdot \widehat{f}_{e,\mu,L}(w).
\end{aligned}
\]
\end{proof}
