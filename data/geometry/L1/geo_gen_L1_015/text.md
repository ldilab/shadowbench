\begin{theorem}[separatingHyperplanes_is_pointed]
Suppose that $C$ and $D$ are disjoint subsets of $\mathbb{R}^n$. Consider the set of $(a, b) \in \mathbb{R}^{n+1}$ for which $a^T x \le b$ for all $x \in C$, and $a^T x \ge b$ for all $x \in D$. Show that this set is a convex cone containing the origin. (which is the singleton $\{0\}$ if there is no hyperplane that separates $C$ and $D$).
\end{theorem}

\begin{proof}
Let $S = \{ (a, b) \in \mathbb{R}^n \times \mathbb{R} \mid \forall x \in C, a^T x \le b \text{ and } \forall x \in D, a^T x \ge b \}$.

\textbf{1. Cone property:} 
Let $(a, b) \in S$ and $\lambda > 0$. Multiplying the given inequalities by $\lambda$:
\[ \lambda (a^T x) \le \lambda b \implies (\lambda a)^T x \le \lambda b, \quad \forall x \in C \]
\[ \lambda (a^T x) \ge \lambda b \implies (\lambda a)^T x \ge \lambda b, \quad \forall x \in D \]
Thus, $\lambda(a, b) \in S$. The case for $\lambda=0$ is trivial as $(0,0) \in S$ since $0 \le 0$ and $0 \ge 0$.

\textbf{2. Convexity (Addition):} 
Let $(a_1, b_1), (a_2, b_2) \in S$. Adding the respective inequalities:
\[ a_1^T x + a_2^T x \le b_1 + b_2 \implies (a_1 + a_2)^T x \le b_1 + b_2, \quad \forall x \in C \]
\[ a_1^T x + a_2^T x \ge b_1 + b_2 \implies (a_1 + a_2)^T x \ge b_1 + b_2, \quad \forall x \in D \]
Thus, the sum $(a_1 + a_2, b_1 + b_2)$ belongs to $S$. 

Since $S$ is a cone and is closed under addition, it is a pointed convex cone.
\end{proof}
