\begin{theorem}[convexOn_sq_div]
Suppose that $f : \mathbb{R}^n \to \mathbb{R}$ is nonnegative and convex, and $g : \mathbb{R}^n \to \mathbb{R}$ is positive and concave. Show that the function $f^2/g$, with domain $\mathbf{dom} f \cap \mathbf{dom} g$, is convex.
\end{theorem}

\begin{proof}
Consider the function $h : \mathbb{R} \times \mathbb{R}_{++} \to \mathbb{R}$ defined by $h(x, y) = x^2 / y$. 
It is easy to show that the quadratic-over-linear function $h$ is convex.

Furthermore, we observe the monotonicity properties of $h(x, y)$ on the restricted domain where $x \ge 0$ and $y > 0$:
\begin{itemize}
    \item $h$ is non-decreasing in $x$, because $\frac{\partial h}{\partial x} = \frac{2x}{y} \ge 0$.
    \item $h$ is non-increasing in $y$, because $\frac{\partial h}{\partial y} = -\frac{x^2}{y^2} \le 0$.
\end{itemize}

Now, consider the composition $h(f(z), g(z)) = f(z)^2 / g(z)$. 
By the assumptions, $f(z) \ge 0$ and $g(z) > 0$ for all $z \in \mathbf{dom} f \cap \mathbf{dom} g$, meaning the outputs of $f$ and $g$ always fall into the region where the above monotonicity properties hold.

We can apply the composition rule: since $f$ is convex, $g$ is concave, and the outer function $h$ is convex, non-decreasing in its first argument, and non-increasing in its second argument (on the range of the inner functions), the composition $h(f(z), g(z))$ is convex.

Therefore, $f^2/g$ is convex.
\end{proof}
