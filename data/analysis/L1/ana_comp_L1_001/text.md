\begin{theorem}[integral_boundary_rect_of_hasFDerivAt_real_off_countable] Let $f : \mathbb{C} \to E$ be a function with values in a real normed vector space $E$.
Let $z^{\ast}, w^{\ast} \in \mathbb{C}$.
Assume the following:

\begin{enumerate}
  \item The function $f$ is continuous on the closed rectangle
  \[
  R := [\Re(z^{\ast}),\, \Re(w^{\ast})] \times [\Im(z^{\ast}),\, \Im(w^{\ast})] \subset \mathbb{C}.
  \]
  \item There exists a countable set $S \subset \mathbb{C}$ such that for every point $z \in \operatorname{int}(R) \setminus S$, the function $f$ is
  real differentiable at $z$, with partial derivatives
  \[
  \frac{\partial f}{\partial x}(z), \qquad \frac{\partial f}{\partial y}(z).
  \]
  \item The function
  \[
  z \longmapsto
  i\,\frac{\partial f}{\partial x}(z)
  \;-\;
  \frac{\partial f}{\partial y}(z)
  \]
  is integrable on $R$.
\end{enumerate}

Then the following identity holds:
\[
\int_{\Re(z^{\ast})}^{\Re(w^{\ast})}
f\bigl(x + i\,\Im(z^{\ast})\bigr)\,dx
\;-\;
\int_{\Re(z^{\ast})}^{\Re(w^{\ast})}
f\bigl(x + i\,\Im(w^{\ast})\bigr)\,dx
\]
\[
\quad
+\;
i \int_{\Im(z^{\ast})}^{\Im(w^{\ast})}
f\bigl(\Re(w^{\ast}) + i\,y\bigr)\,dy
\;-\;
i \int_{\Im(z^{\ast})}^{\Im(w^{\ast})}
f\bigl(\Re(z^{\ast}) + i\,y\bigr)\,dy
\]
\[
=\;
\int_{\Re(z^{\ast})}^{\Re(w^{\ast})}
\int_{\Im(z^{\ast})}^{\Im(w^{\ast})}
\left(
i\,\frac{\partial f}{\partial x}(x+iy)
-
\frac{\partial f}{\partial y}(x+iy)
\right)
\,dy\,dx.
\]
\end{theorem}

\begin{proof}
We identify $\mathbb{C}$ with $\mathbb{R}^2$ via the linear isomorphism
\[
(x,y) \longmapsto x + i y.
\]
Define $F : \mathbb{R}^2 \to E$ by $F(x,y) := f(x+iy)$.

By continuity of $f$ on $R$, the function $F$ is continuous on
$[\Re(z^{\ast}),\Re(w^{\ast})] \times [\Im(z^{\ast}),\Im(w^{\ast})]$.
The exceptional set $S$ pulls back to a countable subset of $\mathbb{R}^2$.

For every $(x,y)$ in the interior of the rectangle outside this exceptional set,
the chain rule shows that $F$ is differentiable with
\[
\frac{\partial F}{\partial x}(x,y)
=
\frac{\partial f}{\partial x}(x+iy),
\qquad
\frac{\partial F}{\partial y}(x,y)
=
\frac{\partial f}{\partial y}(x+iy).
\]

A direct computation shows that the Green-type expression becomes
\[
-\,i\,\frac{\partial F}{\partial x}(x,y)
+
\frac{\partial F}{\partial y}(x,y)
=
-\left(
i\,\frac{\partial f}{\partial x}(x+iy)
-
\frac{\partial f}{\partial y}(x+iy)
\right).
\]

Applying Green's theorem on rectangles (valid for functions differentiable
outside a countable set) yields the stated identity.
\end{proof}
