\begin{theorem}[convex_partialSum]
Show that if $S_1$ and $S_2$ are convex sets in $\mathbb{R}^{m+n}$, then so is their partial sum
\[
S = \{(x, y_1 + y_2) \mid x \in \mathbb{R}^m, y_1, y_2 \in \mathbb{R}^n, (x, y_1) \in S_1, (x, y_2) \in S_2\}.
\]
\end{theorem}

\begin{proof}
To show that $S$ is convex, let $z, z' \in S$ and let $\theta \in [0, 1]$. We need to show that $\theta z + (1 - \theta)z' \in S$.

By the definition of $S$, we can write:
\begin{itemize}
    \item $z = (x, y_1 + y_2)$ where $(x, y_1) \in S_1$ and $(x, y_2) \in S_2$.
    \item $z' = (x', y'_1 + y'_2)$ where $(x', y'_1) \in S_1$ and $(x', y'_2) \in S_2$.
\end{itemize}

Now, consider the convex combination:
\begin{align*}
\theta z + (1 - \theta)z' &= \theta(x, y_1 + y_2) + (1 - \theta)(x', y'_1 + y'_2) \\
&= (\theta x + (1 - \theta)x', \theta(y_1 + y_2) + (1 - \theta)(y'_1 + y'_2)) \\
&= (\theta x + (1 - \theta)x', (\theta y_1 + (1 - \theta)y'_1) + (\theta y_2 + (1 - \theta)y'_2)).
\end{align*}

Let $\bar{x} = \theta x + (1 - \theta)x'$, $\bar{y}_1 = \theta y_1 + (1 - \theta)y'_1$, and $\bar{y}_2 = \theta y_2 + (1 - \theta)y'_2$. 
Then we have $\theta z + (1 - \theta)z' = (\bar{x}, \bar{y}_1 + \bar{y}_2)$.

To verify that this point is in $S$, we check the conditions on $(\bar{x}, \bar{y}_1)$ and $(\bar{x}, \bar{y}_2)$:
\begin{enumerate}
    \item Since $S_1$ is convex and $(x, y_1), (x', y'_1) \in S_1$, it follows that:
    \[
    \theta(x, y_1) + (1 - \theta)(x', y'_1) = (\theta x + (1 - \theta)x', \theta y_1 + (1 - \theta)y'_1) = (\bar{x}, \bar{y}_1) \in S_1.
    \]
    \item Since $S_2$ is convex and $(x, y_2), (x', y'_2) \in S_2$, it follows that:
    \[
    \theta(x, y_2) + (1 - \theta)(x', y'_2) = (\theta x + (1 - \theta)x', \theta y_2 + (1 - \theta)y'_2) = (\bar{x}, \bar{y}_2) \in S_2.
    \]
\end{enumerate}

Since $(\bar{x}, \bar{y}_1) \in S_1$ and $(\bar{x}, \bar{y}_2) \in S_2$, the vector $(\bar{x}, \bar{y}_1 + \bar{y}_2)$ satisfies the definition of $S$. Thus, $\theta z + (1 - \theta)z' \in S$, which proves that $S$ is a convex set.
\end{proof}
