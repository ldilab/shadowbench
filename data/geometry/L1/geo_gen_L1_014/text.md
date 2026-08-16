\begin{theorem}[partial_x_ne_partial_xtilde_at_p]
Let $(x,y)$ denote the standard coordinates on $\mathbb{R}^2$. Verify that $(\tilde{x}, \tilde{y})$ are global smooth coordinates on $\mathbb{R}^2$, where
\[ \tilde{x} = x, \quad \tilde{y} = y + x^3. \]
Let $p$ be the point $(1,0) \in \mathbb{R}^2$ (in standard coordinates), and show that
\[ \frac{\partial}{\partial x}\bigg|_p \neq \frac{\partial}{\partial \tilde{x}}\bigg|_p, \]
even though the coordinate functions $x$ and $\tilde{x}$ are identically equal.
\end{theorem}

\begin{proof}
Consider the map $\Phi:\mathbb{R}^2\to\mathbb{R}^2$ given by $\Phi(x,y)=(\tilde{x},\tilde{y})=(x,y+x^3)$. This map is smooth, and its inverse is $\Phi^{-1}(\tilde{x},\tilde{y})=(\tilde{x},\tilde{y}-\tilde{x}^3)$, which is also smooth. Hence $(\tilde{x},\tilde{y})$ are global smooth coordinates on $\mathbb{R}^2$.

Now let $p=(1,0)$, and let $\hat p=(x(p),y(p))=(1,0)$ denote its standard coordinate representation. By the chain rule,
\begin{align*}
\left.\frac{\partial}{\partial x}\right|_p
&=
\frac{\partial \tilde{x}}{\partial x}(\hat p)
\left.\frac{\partial}{\partial \tilde{x}}\right|_p
+
\frac{\partial \tilde{y}}{\partial x}(\hat p)
\left.\frac{\partial}{\partial \tilde{y}}\right|_p \\
&=
\left.\frac{\partial}{\partial \tilde{x}}\right|_p
+
3\left.\frac{\partial}{\partial \tilde{y}}\right|_p
\neq
\left.\frac{\partial}{\partial \tilde{x}}\right|_p.
\end{align*}
Thus the two tangent vectors are different, even though the coordinate functions $x$ and $\tilde{x}$ are identically equal.
\end{proof}
