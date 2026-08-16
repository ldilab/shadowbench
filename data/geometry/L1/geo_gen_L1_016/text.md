\begin{theorem}[hyperbolic_set_convex]
Show that the hyperbolic set $S = \{x \in \mathbb{R}_+^n \mid \prod_{i=1}^n x_i \ge 1\}$ is convex. 
\textit{Hint:} If $a, b \ge 0$ and $0 \le \theta \le 1$, then $a^\theta b^{1-\theta} \le \theta a + (1-\theta)b$.
\end{theorem}

\begin{proof}
Let $x, y \in S$ and let $\theta \in [0, 1]$. We need to show that $z = \theta x + (1-\theta)y \in S$.
Since $x_i \ge 0$ and $y_i \ge 0$ for all $i$, it is clear that $z_i = \theta x_i + (1-\theta)y_i \ge 0$.

Now we evaluate the product condition. According to the weighted AM-GM inequality (the hint provided):
\[ x_i^\theta y_i^{1-\theta} \le \theta x_i + (1-\theta)y_i, \quad \forall i = 1, \dots, n. \]
Taking the product over all $i$:
\[ \prod_{i=1}^n (\theta x_i + (1-\theta)y_i) \ge \prod_{i=1}^n \left( x_i^\theta y_i^{1-\theta} \right) = \left( \prod_{i=1}^n x_i \right)^\theta \left( \prod_{i=1}^n y_i \right)^{1-\theta}. \]
Since $x, y \in S$, we have $\prod x_i \ge 1$ and $\prod y_i \ge 1$. Substituting these into the inequality:
\[ \prod_{i=1}^n z_i \ge (1)^\theta (1)^{1-\theta} = 1. \]
Thus $z \in S$, which proves that the set $S$ is convex.
\end{proof}
