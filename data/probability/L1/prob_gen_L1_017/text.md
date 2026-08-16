\begin{lemma}[Small-ball bound for a Gaussian quadratic form]
Let $x\sim N(0,I_n)$ and let
\[
Q=
\begin{pmatrix}
q_{11} & q_{12}^{\mathsf T}\\
q_{12} & Q_{22}
\end{pmatrix}
\in\mathbb{S}^{n+1}_{\geq0}
\]
be positive semidefinite. Then, for every $\varepsilon>0$,
\[
\mathbb{P}\!\left(
\begin{pmatrix}1\\x\end{pmatrix}^{\mathsf T}
Q
\begin{pmatrix}1\\x\end{pmatrix}
\leq\varepsilon\operatorname{Tr}(Q_{22})
\right)
\leq(e\varepsilon)^{1/2}.
\]
\end{lemma}
