\begin{theorem}
Let $I = \langle x^2, xy, y^2 \rangle \subseteq k[x, y]$.
\begin{enumerate}
    \item[I_isPrimary] $I$ is primary.
    \item[I_not_infIrred] $I = \langle x^2, y \rangle \cap \langle x, y^2 \rangle$ and conclude that $I$ is not irreducible.
\end{enumerate}
\end{theorem}

\begin{proof}
Let $\mathfrak m:=\langle x,y\rangle$. Then
\[
  I=\langle x^2,xy,y^2\rangle=\mathfrak m^2,
  \qquad
  \sqrt I=\sqrt{\mathfrak m^2}=\mathfrak m.
\]
Since $k[x,y]/\mathfrak m\simeq k$, $\mathfrak m$ is maximal. Thus $\sqrt I$ is maximal, and hence $I$ is primary.

Now put $J:=\langle x^2,y\rangle$ and $K:=\langle x,y^2\rangle$. We show that $I=J\cap K$. Clearly $I\subseteq J\cap K$. Conversely, for a monomial $x^ay^b$,
\[
  x^ay^b\in J\cap K
  \iff
  (a\ge2 \text{ or } b\ge1)
  \text{ and }
  (a\ge1 \text{ or } b\ge2).
\]
This implies $a\ge2$, or $a,b\ge1$, or $b\ge2$, so $x^ay^b$ is divisible by $x^2$, $xy$, or $y^2$. Hence $x^ay^b\in I$. Since these are monomial ideals, $J\cap K\subseteq I$, and therefore $I=J\cap K$.

Finally, $I\subsetneq J$ because $y\in J\setminus I$, and $I\subsetneq K$ because $x\in K\setminus I$. Thus $I=J\cap K$ is a nontrivial intersection, so $I$ is not irreducible.
\end{proof}
