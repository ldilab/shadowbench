\begin{definition}[isUnital_auxGroup]
   Let $X$ be a topological space and $N$ be a finite index set.  
   Let $\pi_N(X,x)\ :=\ \Omega^{N}(X,x)\big/\simeq_{\partial I^N}$ be the set of homotopy classes relative to the boundary. Fix $i\in N$. There is an induced identification of $N$-loops as ``loops of $(N\setminus\{i\})$-loops'',
\[
\mathrm{toLoop}_i : \Omega^{N}(X,x)\ \longrightarrow\ \Omega\!\bigl(\Omega^{N\setminus\{i\}}(X,x),\,\mathrm{const}\bigr),
\]
and hence an induced binary operation $\ast_i$  on $\pi_N(X,x)$ obtained by transporting the usual loop
concatenation in the $i$-direction. We define $\mathrm{auxGroup}(i)$ be the group whose underlying set and binary operation are $\pi_N(X,x)$ and $\ast_i$, respectively.
\end{definition}


\begin{theorem}[auxGroup_indep]
Let $i,j\in N$. Then the groups $\mathrm{auxGroup}(i)$ and $\mathrm{auxGroup}(j)$ are isomorphic.
\end{theorem}

\begin{proof}
If $i=j$ there is nothing to prove, so assume $i\neq j$.
Consider the two unital multiplications $\ast_i$ and $\ast_j$ on the same set $\pi_N(X,x)$, both
having the same unit $[c]$ by the previous theorem.

The Eckmann--Hilton argument applies in the following form: if two unital binary operations
$\star$ and $\diamond$ on a set have the same unit and satisfy the \emph{interchange law}
\[
(a\star b)\diamond(c\star d) \;=\; (a\diamond c)\star(b\diamond d)
\qquad \forall a,b,c,d,
\]
then $\star=\diamond$ (and in fact the common operation is commutative).

Thus it suffices to verify the interchange law for $\ast_i$ and $\ast_j$ on $\pi_N(X,x)$.
Let $[a],[b],[c],[d]\in \pi_N(X,x)$ be represented by generalized loops $a,b,c,d\in\Omega^{N}(X,x)$.
Form the two composites
\[
([a]\ast_i [b])\ast_j([c]\ast_i [d])
\qquad\text{and}\qquad
([a]\ast_j [c])\ast_i([b]\ast_j [d]).
\]
By construction of $\ast_i$ and $\ast_j$, each side is represented by a generalized $N$-loop obtained
by concatenating maps $I^{N}\to X$ in the $i$-direction and $j$-direction respectively.
When $i\neq j$, these two iterated concatenations correspond to the two ways of composing a map
defined on the square $I\times I$ (in the $(i,j)$-coordinates) by first concatenating horizontally
and then vertically, or vice versa. These two constructions are homotopic relative to the boundary
of the square (and hence relative to $\partial I^{N}$) by the standard ``grid homotopy'' that
reparameterizes the $(i,j)$-coordinates.

Therefore the two composites represent the same element of $\pi_N(X,x)$, i.e.\ the interchange law
holds:
\[
([a]\ast_i [b])\ast_j([c]\ast_i [d])
\;=\;
([a]\ast_j [c])\ast_i([b]\ast_j [d]).
\]
By Eckmann--Hilton it follows that $\ast_i=\ast_j$, hence the group structures
$\mathrm{auxGroup}(i)$ and $\mathrm{auxGroup}(j)$ coincide.
\end{proof}
