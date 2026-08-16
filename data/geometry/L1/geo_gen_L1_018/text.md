\begin{theorem}[affineSubspace_image_of_linear_constraints]
\textbf{Affine set.} Show that the set $\{Ax + b \mid Fx = g\}$ is affine. Here $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$, $F \in \mathbb{R}^{p \times n}$, and $g \in \mathbb{R}^p$.
\end{theorem}

\begin{proof}
A set $S$ is affine if for every $z_1, z_2 \in S$ and $\theta \in \mathbb{R}$, the point $\theta z_1 + (1 - \theta)z_2$ is also in $S$.

Let $S = \{Ax + b \mid Fx = g\}$. Suppose $z_1, z_2 \in S$. Then there exist $x_1, x_2 \in \mathbb{R}^n$ such that:
\begin{align*}
z_1 &= Ax_1 + b, \quad Fx_1 = g \\
z_2 &= Ax_2 + b, \quad Fx_2 = g
\end{align*}
Now, for any $\theta \in \mathbb{R}$, consider the affine combination:
\begin{align*}
\theta z_1 + (1 - \theta)z_2 &= \theta(Ax_1 + b) + (1 - \theta)(Ax_2 + b) \\
&= A(\theta x_1 + (1 - \theta)x_2) + (\theta + (1 - \theta))b \\
&= A(\theta x_1 + (1 - \theta)x_2) + b.
\end{align*}
Let $\bar{x} = \theta x_1 + (1 - \theta)x_2$. We then check the condition $F\bar{x} = g$:
\[
F\bar{x} = F(\theta x_1 + (1 - \theta)x_2) = \theta Fx_1 + (1 - \theta)Fx_2 = \theta g + (1 - \theta)g = g.
\]
Since $\theta z_1 + (1 - \theta)z_2 = A\bar{x} + b$ with $F\bar{x} = g$, it follows that $\theta z_1 + (1 - \theta)z_2 \in S$. Therefore, $S$ is affine.
\end{proof}
