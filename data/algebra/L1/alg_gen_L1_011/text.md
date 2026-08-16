\begin{theorem}[zeroLocus_mul]
If $I$ and $J$ are ideals in $k[x_1, \dots, x_n]$, then $\mathbf{V}(I \cdot J) = \mathbf{V}(I) \cup \mathbf{V}(J)$.
\end{theorem}

\begin{proof}
Let $a \in \mathbf{V}(I \cdot J)$. Then $g(a)h(a) = 0$ for all $g \in I$ and all $h \in J$. If $g(a) = 0$ for all $g \in I$, then $a \in \mathbf{V}(I)$. If $g(a) \neq 0$ for some $g \in I$, then we must have $h(a) = 0$ for all $h \in J$. In either event, $a \in \mathbf{V}(I) \cup \mathbf{V}(J)$.

Conversely, suppose $a \in \mathbf{V}(I) \cup \mathbf{V}(J)$. Either $g(a) = 0$ for all $g \in I$ or $h(a) = 0$ for all $h \in J$. Thus, $g(a)h(a) = 0$ for all $g \in I$ and $h \in J$. Thus, $f(a) = 0$ for all $f \in I \cdot J$ and, hence, $a \in \mathbf{V}(I \cdot J)$.
\end{proof}
