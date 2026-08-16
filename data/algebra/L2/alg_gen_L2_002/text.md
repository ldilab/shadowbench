\begin{theorem}[ideal_xsq_add_one_radical_and_zeroLocus_empty]
Show that $\langle x^2 + 1\rangle \subseteq \mathbb{R}[x]$ is a radical ideal, but that $V(x^2 + 1)$ is the empty set.
\end{theorem}

\begin{proof}
Let $f(x)=x^2+1\in\mathbb{R}[x]$ and $I=\langle f\rangle$.

\medskip
\noindent\textbf{(Radicality.)}
First, $f$ has no real root: for every $r\in\mathbb{R}$ we have
\[
f(r)=r^2+1>0,
\]
so $f(r)\neq 0$. Hence $f$ is irreducible in $\mathbb{R}[x]$.
Since $\mathbb{R}[x]$ is a UFD, an irreducible element is prime; therefore $f$ is prime, hence radical as an element.
Using the equivalence that $f$ is radical if and only if the principal ideal $\langle f\rangle$ is radical,
we conclude that $I$ is a radical ideal.

\medskip
\noindent\textbf{(Zero locus is empty.)}
By definition,
\[
\mathbf{V}(I)=\{\, r\in\mathbb{R}\mid \forall g\in I,\ g(r)=0 \,\}.
\]
If $r\in\mathbf{V}(I)$, then since $f\in I$ we must have $f(r)=0$.
But $f(r)=r^2+1\neq 0$ for all $r\in\mathbb{R}$, a contradiction.
Thus $\mathbf{V}(x^2+1)=\varnothing$.
\end{proof}
