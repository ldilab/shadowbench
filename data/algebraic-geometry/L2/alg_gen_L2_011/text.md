\begin{theorem}[isAffineHom_of_isAffineHom_struct_of_isAffineHom_diagonal] Let $g:X \to Y$ be a morphism of schemes over $S$. If $X$ is affine over $S$ and the diagonal map $\Delta:Y \to Y \times_S Y$ is affine, then $g$ is affine.
\end{theorem}
\begin{proof}
    The base change \(X\times_S Y \to Y\) of \(X \to S\) by \(Y \to S\) is affine since the affine morphisms are stable under base change. The morphism \((1,g):X \to X \times_S Y\) is the base change of \(\Delta:Y \to Y\times_S Y\) by the morphism \(X \times_S Y \to Y\times_SY\). Hence, it is affine. Now the result follows since the composition of affine morphisms is affine.
\end{proof}
