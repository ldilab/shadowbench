\begin{theorem}[brahmagupta_formula]\label{thm:brahmagupta_formula}
In Euclidean geometry, Brahmagupta's formula gives the area $K$ of a convex cyclic quadrilateral (a quadrilateral inscribed in a circle) given the lengths of its sides. 
Formally, let $A, B, C, D$ be the vertices of a convex cyclic quadrilateral in order. Let $a = |AB|, b = |BC|, c = |CD|$, and $d = |DA|$ be the lengths of the sides, and let $s$ be the semiperimeter, defined as:
\[
s = \frac{a + b + c + d}{2}
\]
Then the area $K$ of the quadrilateral is given by:
\[
K = \sqrt{(s - a)(s - b)(s - c)(s - d)}
\]
\end{theorem}

\begin{proof}
Let $\alpha=\angle DAB$ and $\gamma=\angle BCD$. Since the quadrilateral is cyclic, the opposite angles are supplementary, so $\alpha+\gamma=\pi$. Hence $\sin\gamma=\sin\alpha$ and $\cos\gamma=-\cos\alpha$.

The area $K$ of the quadrilateral is the sum of the areas of $\triangle DAB$ and $\triangle BCD$. Therefore
\[
K=\frac12 ad\sin\alpha+\frac12 bc\sin\gamma
=\frac12(ad+bc)\sin\alpha.
\]
Thus
\begin{align*}
4K^2
&=(ad+bc)^2\sin^2\alpha \\
&=(ad+bc)^2(1-\cos^2\alpha) \\
&=(ad+bc)^2-\bigl((ad+bc)\cos\alpha\bigr)^2.
\end{align*}

Now solve for the common diagonal $DB$. By the law of cosines in $\triangle DAB$ and $\triangle BCD$,
\[
a^2+d^2-2ad\cos\alpha=b^2+c^2-2bc\cos\gamma.
\]
Since $\cos\gamma=-\cos\alpha$, this becomes
\[
a^2+d^2-2ad\cos\alpha=b^2+c^2+2bc\cos\alpha.
\]
Rearranging, we get
\[
(ad+bc)\cos\alpha=\frac12(a^2+d^2-b^2-c^2).
\]
Substituting this into the equation for the area gives
\begin{align*}
4K^2
&=(ad+bc)^2-\frac14(a^2+d^2-b^2-c^2)^2,\\
16K^2
&=4(ad+bc)^2-(a^2+d^2-b^2-c^2)^2.
\end{align*}
The right-hand side is a difference of squares, so
\begin{align*}
16K^2
&=\bigl(2(ad+bc)-a^2-d^2+b^2+c^2\bigr)
  \bigl(2(ad+bc)+a^2+d^2-b^2-c^2\bigr) \\
&=\bigl((b+c)^2-(a-d)^2\bigr)
  \bigl((a+d)^2-(b-c)^2\bigr) \\
&=(-a+b+c+d)(a+b+c-d)(a-b+c+d)(a+b-c+d).
\end{align*}
Since $s=\frac{a+b+c+d}{2}$, this becomes
\[
16K^2=16(s-a)(s-b)(s-c)(s-d).
\]
Therefore
\[
K^2=(s-a)(s-b)(s-c)(s-d).
\]
Taking the positive square root, since $K$ is the area of the quadrilateral, we obtain
\[
K=\sqrt{(s-a)(s-b)(s-c)(s-d)}.
\]
\end{proof}
