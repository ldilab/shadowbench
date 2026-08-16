\begin{theorem}[smooth_function_separating_closed_sets]
Suppose $A$ and $B$ are disjoint closed subsets of a smooth manifold $M$. Show that there exists $f \in C^\infty(M)$ such that $0 \le f(x) \le 1$ for all $x \in M$, $f^{-1}(0) = A$, and $f^{-1}(1) = B$.
\end{theorem}

\begin{proof}
To construct such a function, we rely on the property that for any closed subset $K \subseteq M$, there exists a smooth nonnegative function $g: M \to \mathbb{R}$ such that $g^{-1}(0) = K$ (this is a known result from the theory of smooth partitions of unity, often labeled as Theorem 2.29 in this text).

Let $A$ and $B$ be disjoint closed subsets of $M$.
\begin{enumerate}
    \item By the aforementioned result, there exists a smooth function $g_A \in C^\infty(M)$ such that $g_A(x) \ge 0$ for all $x \in M$ and $g_A^{-1}(0) = A$.
    \item Similarly, there exists a smooth function $g_B \in C^\infty(M)$ such that $g_B(x) \ge 0$ for all $x \in M$ and $g_B^{-1}(0) = B$.
\end{enumerate}

Now, consider the function $f: M \to \mathbb{R}$ defined by:
\[
f(x) = \frac{g_A(x)}{g_A(x) + g_B(x)}.
\]

First, we check that the denominator $g_A(x) + g_B(x)$ is never zero. Since $A \cap B = \emptyset$, for any $x \in M$, $x$ cannot be in both $A$ and $B$. 
\begin{itemize}
    \item If $x \notin A$, then $g_A(x) > 0$.
    \item If $x \in A$, then $x \notin B$, so $g_B(x) > 0$.
\end{itemize}
In either case, $g_A(x) + g_B(x) > 0$ for all $x \in M$. Thus, $f$ is well-defined. Since $g_A$ and $g_B$ are smooth and their sum is non-zero, $f$ is a smooth function, i.e., $f \in C^\infty(M)$.

Next, we verify the required properties:
\begin{itemize}
    \item \textbf{Range:} Since $g_A(x) \ge 0$ and $g_B(x) \ge 0$, it follows that $0 \le \frac{g_A(x)}{g_A(x) + g_B(x)} \le 1$.
    \item \textbf{Preimage of 0:} $f(x) = 0$ if and only if $g_A(x) = 0$. By construction, $g_A(x) = 0 \iff x \in A$. Thus, $f^{-1}(0) = A$.
    \item \textbf{Preimage of 1:} $f(x) = 1$ if and only if $g_A(x) = g_A(x) + g_B(x)$, which implies $g_B(x) = 0$. By construction, $g_B(x) = 0 \iff x \in B$. Thus, $f^{-1}(1) = B$.
\end{itemize}
Therefore, $f$ is the desired smooth function.
\end{proof}
