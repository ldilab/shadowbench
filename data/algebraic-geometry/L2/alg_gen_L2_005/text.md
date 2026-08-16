\begin{definition}[IsProjective]
Let $f : X \to S$ be a morphism of schemes. We say that $f$ is \emph{projective} (in the Hartshorne, or $H$-projective, sense) if there exists an integer $n \ge 0$ and a closed immersion
\[
i : X \hookrightarrow \mathbf{P}^n_S
\]
over $S$ such that
\[
f = \pi \circ i,
\]
where $\pi : \mathbf{P}^n_S \to S$ is the structure morphism.
\end{definition}

\begin{theorem}[is_projective_proper]
Let $S$ be a scheme and $n \ge 0$. The structure morphism
\[
\pi : \mathbf{P}^n_S \to S
\]
is proper.
\end{theorem}

\begin{proof}
The morphism $\pi : \mathbf{P}^n_S \to S$ is of finite type, separated, and universally closed.

It is of finite type because $\mathbf{P}^n_S$ is obtained by gluing finitely many affine schemes of finite type over $S$.

It is separated because projective space is separated over the base.

To prove universal closedness, we use the valuative criterion. Let $R$ be a valuation ring with fraction field $K$. Given a morphism $\operatorname{Spec} K \to \mathbf{P}^n_S$ compatible with a morphism $\operatorname{Spec} R \to S$, it corresponds to a point $[x_0 : \cdots : x_n]$ with $x_i \in K$ not all zero. After scaling, we may assume $x_i \in R$ and at least one $x_i$ is a unit. This determines a morphism $\operatorname{Spec} R \to \mathbf{P}^n_S$ extending the given one. Uniqueness follows from separatedness.

Thus $\pi$ satisfies the valuative criterion for properness and is proper.
\end{proof}

\begin{theorem}[projective_isProper]
Every projective morphism is proper.
\end{theorem}

\begin{proof}
Let $f : X \to S$ be projective. Then there exists a factorization
\[
X \xrightarrow{i} \mathbf{P}^n_S \xrightarrow{\pi} S
\]
where $i$ is a closed immersion.

Closed immersions are proper, hence $i$ is proper. The morphism $\pi$ is proper by the previous theorem. Since proper morphisms are stable under composition, it follows that $f = \pi \circ i$ is proper.
\end{proof}
