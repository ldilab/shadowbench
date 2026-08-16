\begin{lemma}[Laplace bound for a positive Gaussian quadratic form]
Let $x\sim N(0,I_n)$ and let
\[
Q=
\begin{pmatrix}
q_{11} & q_{12}^{\mathsf T}\\
q_{12} & Q_{22}
\end{pmatrix}
\in\mathbb{S}^{n+1}_{\geq0}
\]
be positive semidefinite. Then, for every $\lambda>0$,
\[
\mathbb{E}\!\left[
\exp\!\left(
-\lambda
\begin{pmatrix}1\\x\end{pmatrix}^{\mathsf T}
Q
\begin{pmatrix}1\\x\end{pmatrix}
\right)
\right]
\leq
\det(I_n+2\lambda Q_{22})^{-1/2}.
\]
\end{lemma}
