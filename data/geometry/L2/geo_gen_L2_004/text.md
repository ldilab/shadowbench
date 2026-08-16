\begin{theorem}[smoothVectorField_infinite_dimensional]
Let $M$ be a nonempty positive-dimensional smooth manifold with or without boundary. Then $\mathfrak{X}(M)$, the space of smooth vector fields on $M$, is infinite-dimensional.
\end{theorem}

\begin{proof}
Suppose $\mathfrak{X}(M)$ is finite-dimensional with dimension $k$. 
Since $\dim M \ge 1$, we can choose $k+1$ distinct points $x_1, \dots, x_{k+1}$ in a coordinate chart $U \subseteq M$. 
Because $M$ is Hausdorff, there exist pairwise disjoint open neighborhoods $U_1, \dots, U_{k+1} \subseteq U$ for these points.

For each $i$, let $f_i \in C^\infty(M)$ be a smooth bump function supported on $U_i$ such that $f_i(x_i) = 1$. 
Let $V = \frac{\partial}{\partial x^1}$ be a local coordinate vector field on $U$, and define global vector fields $X_i = f_i V$ (extended by $0$ outside $U$). 
Since the $X_i$ have disjoint supports, they are linearly independent: $\sum c_i X_i = 0$ implies $c_j X_j(x_j) = c_j V|_{x_j} = 0$, so each $c_j = 0$.

This contradicts the assumption $\dim \mathfrak{X}(M) = k$. Therefore, $\mathfrak{X}(M)$ is infinite-dimensional.
\end{proof}
