\begin{theorem}[projective_isProper]
Let $S$ be a scheme, and let $f : X \to S$ be a projective morphism. Then $f$ is proper.
\end{theorem}

\begin{proof}
By definition, a morphism $f : X \to S$ is projective if there exists an integer $n \ge 0$ and a closed immersion
\[
i : X \hookrightarrow \mathbb{P}^n_S
\]
such that $f$ factors as
\[
X \xrightarrow{i} \mathbb{P}^n_S \xrightarrow{\pi} S,
\]
where $\pi$ is the structure morphism.

Thus it suffices to show that:
\begin{enumerate}
\item the morphism $\pi : \mathbb{P}^n_S \to S$ is proper, and
\item proper morphisms are stable under composition and closed immersions.
\end{enumerate}

First, the projection $\pi : \mathbb{P}^n_S \to S$ is proper. Indeed, $\mathbb{P}^n_S$ is covered by finitely many affine opens of the form
\[
D_+(x_i) \cong \operatorname{Spec}(\mathcal{O}_S[x_0/x_i,\dots,x_n/x_i]),
\]
so $\pi$ is of finite type. It is separated because projective space is separated over the base. Finally, $\pi$ is universally closed; this follows from the fact that projective space over a base is universally closed (for instance, by the valuative criterion or by standard results on Proj). Hence $\pi$ is proper.

Second, closed immersions are proper morphisms. Indeed, a closed immersion is finite, hence proper.

Finally, proper morphisms are stable under composition. Therefore, since $f = \pi \circ i$ is a composition of proper morphisms, it follows that $f$ is proper.
\end{proof}
