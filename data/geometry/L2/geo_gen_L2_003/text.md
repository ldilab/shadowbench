\begin{theorem}[dual_cone_matrix_image_nonneg]
Let $A \in \mathbb{R}^{m \times n}$ and consider the cone $K = \{Ax \mid x \succeq 0\}$. Then the dual cone of $K$ is given by
\[
K^* = \{y \in \mathbb{R}^m \mid A^T y \succeq 0\}.
\]
\end{theorem}

\begin{proof}
By definition, the dual cone $K^*$ consists of all vectors $y \in \mathbb{R}^m$ such that $\langle z, y \rangle \ge 0$ for all $z \in K$. 

First, let $y \in K^*$. Then for any $x \in \mathbb{R}^n$ with $x \succeq 0$, we have $Ax \in K$, which implies
\[
\langle Ax, y \rangle = y^T Ax = (A^T y)^T x = \langle x, A^T y \rangle \ge 0.
\]
To show that $A^T y \succeq 0$, we test this condition with the standard basis vectors $e_i \in \mathbb{R}^n$ for each $i = 1, \dots, n$. Since $e_i \succeq 0$, we must have
\[
\langle e_i, A^T y \rangle = (A^T y)_i \ge 0.
\]
Since this holds for every $i$, it follows that $A^T y \succeq 0$. This proves that $K^* \subseteq \{y \mid A^T y \succeq 0\}$.

Conversely, suppose $y \in \mathbb{R}^m$ satisfies $A^T y \succeq 0$. For any $z \in K$, there exists an $x \in \mathbb{R}^n$ such that $x \succeq 0$ and $z = Ax$. We then compute:
\begin{align*}
\langle z, y \rangle &= \langle Ax, y \rangle \\
&= \langle x, A^T y \rangle \\
&= \sum_{i=1}^n x_i (A^T y)_i.
\end{align*}
Since $x_i \ge 0$ and $(A^T y)_i \ge 0$ for all $i$, each term in the sum is non-negative, hence $\langle z, y \rangle \ge 0$. This shows that $y \in K^*$, which proves the reverse inclusion $\{y \mid A^T y \succeq 0\} \subseteq K^*$.

Therefore, we conclude that $K^* = \{y \in \mathbb{R}^m \mid A^T y \succeq 0\}$.
\end{proof}
