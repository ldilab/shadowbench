\begin{theorem}[erdos_mordell_inequality]\label{thm:erdos_mordell}
In Euclidean geometry, the Erdős–Mordell inequality states that for any triangle $ABC$ and point $P$ inside $ABC$, the sum of the distances from $P$ to the sides is less than or equal to half of the sum of the distances from $P$ to the vertices.
Let $PL, PM, PN$ be the perpendiculars from $P$ to the sides $BC, CA, AB$ respectively. Then:
\[
PA + PB + PC \ge 2(PL + PM + PN)
\]
\end{theorem}

\begin{proof}
Let the sides of $ABC$ be $a$ opposite $A$, $b$ opposite $B$, and $c$ opposite $C$; also let $PA=p$, $PB=q$, $PC=r$, $\operatorname{dist}(P,BC)=x$, $\operatorname{dist}(P,CA)=y$, and $\operatorname{dist}(P,AB)=z$.

First, we prove that $cr \ge ax+by$. This is equivalent to
\[
\frac{c(r+z)}{2} \ge \frac{ax+by+cz}{2}.
\]
The right side is the area of triangle $ABC$, but on the left side, $r+z$ is at least the height of the triangle; consequently, the left side cannot be smaller than the right side.

Now reflect $P$ in the angle bisector at $C$. We find that $cr \ge ay+bx$ for $P$'s reflection. Similarly, $bq \ge az+cx$ and $ap \ge bz+cy$. We solve these inequalities for $r$, $q$, and $p$:
\begin{align*}
r &\ge \frac{a}{c}y+\frac{b}{c}x,\\
q &\ge \frac{a}{b}z+\frac{c}{b}x,\\
p &\ge \frac{b}{a}z+\frac{c}{a}y.
\end{align*}
Adding the three up, we get
\begin{align*}
p+q+r
&\ge
\left(\frac{b}{c}+\frac{c}{b}\right)x
+
\left(\frac{a}{c}+\frac{c}{a}\right)y
+
\left(\frac{a}{b}+\frac{b}{a}\right)z.
\end{align*}
Since the sum of a positive number and its reciprocal is at least $2$ by AM--GM inequality, we are finished:
\[
p+q+r \ge 2x+2y+2z.
\]
Therefore,
\[
PA+PB+PC \ge 2(PL+PM+PN).
\]
Equality holds only for the equilateral triangle, where $P$ is its centroid.
\end{proof}
