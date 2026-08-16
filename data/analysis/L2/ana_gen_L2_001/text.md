\begin{theorem}[exists_affine_between_of_concaveOn_le_convexOn]
Suppose $f : \mathbb{R}^n \to \mathbb{R}$ is convex, $g : \mathbb{R}^n \to \mathbb{R}$ is concave, $\operatorname{dom} f = \operatorname{dom} g = \mathbb{R}^n$, and for all $x$, $g(x) \le f(x)$. Show that there exists an affine function $h$ such that for all $x$, $g(x) \le h(x) \le f(x)$. In other words, if a concave function $g$ is an underestimator of a convex function $f$, then we can fit an affine function between $f$ and $g$.
\end{theorem}

\begin{proof}
Define
\[
E := \{(x,t)\in \mathbb R^n\times \mathbb R : t>f(x)\},
\qquad
H := \{(x,t)\in \mathbb R^n\times \mathbb R : t<g(x)\}.
\]

Since $f$ is convex, $E$ is convex; since $g$ is concave, $H$ is convex.
Because $f$ and $g$ are finite-valued on all of $\mathbb R^n$, they are continuous, so
both $E$ and $H$ are open.
They are also nonempty: for any $x\in\mathbb R^n$,
\[
(x,f(x)+1)\in E,
\qquad
(x,g(x)-1)\in H.
\]
Finally, $E\cap H=\varnothing$, because if $(x,t)\in E\cap H$, then
\[
t>f(x)\ge g(x)>t,
\]
a contradiction.

Therefore, by the Hahn--Banach separation theorem for two disjoint nonempty open convex
sets in a real topological vector space, there exist a nonzero linear functional
$L:\mathbb R^{n+1}\to\mathbb R$ and a scalar $u\in\mathbb R$ such that
\[
L(z)<u \quad \text{for all } z\in H,
\qquad
u<L(z) \quad \text{for all } z\in E.
\]

Let
\[
A(x):=L(x,0), \qquad c:=L(0,1).
\]
Then
\[
L(x,t)=A(x)+ct
\]
for all $(x,t)\in \mathbb R^n\times\mathbb R$, where $A:\mathbb R^n\to\mathbb R$ is linear. Thus
\[
A(x)+ct<u \quad \text{for all } (x,t)\in H,
\]
\[
u<A(x)+ct \quad \text{for all } (x,t)\in E.
\]

We claim that $c>0$.

Assume for contradiction that $c\le 0$.
Since
\[
(0,g(0)-1)\in H,
\qquad
(0,f(0)+1)\in E,
\]
the separation inequalities give
\[
A(0)+c(g(0)-1)<u,
\qquad
u<A(0)+c(f(0)+1).
\]
Since $A(0)=0$, it follows that
\[
c(g(0)-1)<u<c(f(0)+1),
\]
hence
\[
c(g(0)-1)<c(f(0)+1).
\]
On the other hand, from $g(0)\le f(0)$ we have
\[
g(0)-1\le f(0)+1.
\]
Because $c\le 0$, multiplying this inequality by $c$ reverses the direction:
\[
c(f(0)+1)\le c(g(0)-1).
\]
This contradicts
\[
c(g(0)-1)<c(f(0)+1).
\]
Therefore $c>0$.

Now define
\[
h(x):=\frac{u-A(x)}{c}.
\]
Then $h$ is affine.

Fix $x\in\mathbb R^n$ and let $\varepsilon>0$. Since
\[
(x,g(x)-\varepsilon)\in H,
\qquad
(x,f(x)+\varepsilon)\in E,
\]
the separation inequalities give
\[
A(x)+c(g(x)-\varepsilon)<u,
\qquad
u<A(x)+c(f(x)+\varepsilon).
\]
Since $c>0$, dividing by $c$ yields
\[
g(x)-\varepsilon < h(x),
\qquad
h(x)<f(x)+\varepsilon
\qquad (\forall \varepsilon>0).
\]

Hence $g(x)\le h(x)$ and $h(x)\le f(x)$. Indeed, if $h(x)<g(x)$, then taking
\[
\varepsilon=\frac{g(x)-h(x)}{2}>0
\]
contradicts $g(x)-\varepsilon<h(x)$. Similarly, if $f(x)<h(x)$, then taking
\[
\varepsilon=\frac{h(x)-f(x)}{2}>0
\]
contradicts $h(x)<f(x)+\varepsilon$.

Therefore
\[
g(x)\le h(x)\le f(x)\qquad \forall x\in\mathbb R^n.
\]
Thus there exists an affine function $h$ lying between $g$ and $f$.
\end{proof}
