\begin{theorem}[saddle_sections_hasFDerivAt_eq_zero]
Suppose $f : \mathbb{R}^n \times \mathbb{R}^m \to \mathbb{R}$ satisfies the \textit{saddle-point property} at $(\tilde{x}, \tilde{z})$: for all $x \in \mathbb{R}^n$ and $z \in \mathbb{R}^m$, 
\[
f(\tilde{x}, z) \le f(\tilde{x}, \tilde{z}) \le f(x, \tilde{z}).
\]
If the $x$-section $x \mapsto f(x, \tilde{z})$ is differentiable at $\tilde{x}$, and the $z$-section $z \mapsto f(\tilde{x}, z)$ is differentiable at $\tilde{z}$, then $\nabla f(\tilde{x}, \tilde{z}) = 0$.
\end{theorem}

\begin{proof}
First, consider the function of $x$ defined by $g(x) = f(x, \tilde{z})$, where $\tilde{z}$ is fixed. From the second inequality of the saddle-point property, we have:
\[
g(\tilde{x}) = f(\tilde{x}, \tilde{z}) \le f(x, \tilde{z}) = g(x) \quad \text{for all } x \in \mathbb{R}^n.
\]
This implies that $\tilde{x}$ is a global minimizer of $g(x)$. **Since $g$ is differentiable at $\tilde{x}$**, a necessary condition for a minimizer is that its gradient must vanish. Therefore:
\[
\nabla_x f(\tilde{x}, \tilde{z}) = \nabla g(\tilde{x}) = 0.
\]

Next, consider the function of $z$ defined by $h(z) = f(\tilde{x}, z)$, where $\tilde{x}$ is fixed. From the first inequality of the saddle-point property, we have:
\[
h(z) = f(\tilde{x}, z) \le f(\tilde{x}, \tilde{z}) = h(\tilde{z}) \quad \text{for all } z \in \mathbb{R}^m.
\]
This implies that $\tilde{z}$ is a global maximizer of $h(z)$. **Since $h$ is differentiable at $\tilde{z}$**, its gradient at the maximizer must be zero:
\[
\nabla_z f(\tilde{x}, \tilde{z}) = \nabla h(\tilde{z}) = 0.
\]
\end{proof}
