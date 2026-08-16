\begin{definition}[homotopyTo]
Let $X$ be a topological space, let $x \in X$, and let $N$ be a finite index set.
Fix an index $i \in N$, and write $N \setminus i := N \setminus \{i\}$.
Let
\[
\Psi_i : I \times I^{N\setminus i} \xrightarrow{\cong} I^N
\]
denote the canonical homeomorphism that inserts the coordinate $t \in I$ in the $i$-th position.

For a generalized $N$-loop
\[
p \in \Omega^{N}(X,x),
\qquad
p : I^N \to X,
\]
define a path
\[
\mathrm{toLoop}_i(p) : I \longrightarrow \Omega^{N\setminus i}(X,x)
\]
by
\[
\bigl(\mathrm{toLoop}_i(p)\bigr)(t)(y) := p\bigl(\Psi_i(t,y)\bigr),
\qquad
t \in I,\ y \in I^{N\setminus i}.
\]
\end{definition}

\begin{theorem}[homotopyTo_apply]
We have a well-defined map
\[
\mathrm{toLoop}_i :
\Omega^{N}(X,x)
\longrightarrow
\Omega\bigl(\Omega^{N\setminus i}(X,x),\,\mathrm{const}\bigr),
\]
sending an $N$-dimensional generalized loop to a loop of generalized
$(N\setminus i)$-loops based at the constant loop.
\end{theorem}
\begin{proof}
For each fixed $t \in I$, the map $y \mapsto p(\Psi_i(t,y))$ is a generalized
$(N\setminus i)$-loop based at $x$, since if $y \in \partial I^{N\setminus i}$ then
$\Psi_i(t,y) \in \partial I^N$ and hence $p(\Psi_i(t,y)) = x$.

Moreover, $\mathrm{toLoop}_i(p)$ is a based loop in the loop space
$\Omega^{N\setminus i}(X,x)$: for all $y \in I^{N\setminus i}$,
\[
\bigl(\mathrm{toLoop}_i(p)\bigr)(0)(y) = x,
\qquad
\bigl(\mathrm{toLoop}_i(p)\bigr)(1)(y) = x,
\]
since $\Psi_i(0,y)$ and $\Psi_i(1,y)$ lie in $\partial I^N$.
\end{proof}




\begin{theorem}[homotopicTo] Let $X$ be a topological space, $x\in X$, and $N$ an index set.
Fix $i\in N$.
Let
\[
p,q \in \Omega^{N}(X,x).
\]
Assume that the associated paths
\[
\mathrm{toLoop}_i(p),\ \mathrm{toLoop}_i(q) : I \longrightarrow \Omega^{N\setminus\{i\}}(X,x)
\]
are homotopic relative to endpoints.
Then $p$ and $q$ are homotopic relative to the boundary $\partial I^{N}$.
\end{theorem}

\begin{proof}
We identify the cube with a product via the homeomorphism
\[
\Phi_i : I^{N} \xrightarrow{\ \cong\ } I \times I^{N\setminus\{i\}},
\qquad
\Phi_i(y) = (y(i),\, y|_{N\setminus\{i\}}),
\]
with inverse $\Psi_i : I\times I^{N\setminus\{i\}}\to I^{N}$.

Assume we are given a homotopy
\[
H : I\times I \longrightarrow \Omega^{N\setminus\{i\}}(X,x)
\]
from $\mathrm{toLoop}_i(p)$ to $\mathrm{toLoop}_i(q)$.
Thus for each $(t,s)\in I^2$, the value $H(t,s)$ is a continuous map
$I^{N\setminus\{i\}}\to X$ sending $\partial I^{N\setminus\{i\}}$ to $x$, and
\[
H(t,0)=\mathrm{toLoop}_i(p)(t),
\qquad
H(t,1)=\mathrm{toLoop}_i(q)(t).
\]

Define a map
\[
\widetilde H : I\times I^{N} \longrightarrow X
\]
by
\[
\widetilde H(s,y)
\;:=\;
H\bigl(t_0,s\bigr)(y'),
\quad (t_0,y')=\Phi_i(y).
\]
By continuity of $H$ and of $\Phi_i$, the map $\widetilde H$ is continuous.

We first verify that $\widetilde H$ fixes the boundary $\partial I^{N}$.
Let $y\in\partial I^{N}$.
Then there exists $j\in N$ such that $y(j)\in\{0,1\}$.
Write $(t_0,y')=\Phi_i(y)$.
Suppose  $j=i$. Then $t_0\in\{0,1\}$. Since $H$ is a homotopy between based loops, for such $t_0$ the generalized loop
$H(t_0,s)$ is the constant loop at $x$ for all $s$.
Hence
\[
\widetilde H(s,y)=x.
\]
Suppose now that $j\neq i$. Then $y'\in\partial I^{N\setminus\{i\}}$.
By definition of $\Omega^{N\setminus\{i\}}(X,x)$, every loop
$H(t_0,s)$ sends $\partial I^{N\setminus\{i\}}$ to $x$.
Therefore again
\[
\widetilde H(s,y)=x.
\]
Thus $\widetilde H$ is constant equal to $x$ on $\partial I^{N}\times I$.

Finally, we check the endpoints.
For any $y\in I^{N}$, writing $(t_0,y')=\Phi_i(y)$, we have
\[
\widetilde H(0,y)
=
H(t_0,0)(y')
=
\mathrm{toLoop}_i(p)(t_0)(y')
=
p\bigl(\Psi_i(t_0,y')\bigr)
=
p(y),
\]
and similarly,
\[
\widetilde H(1,y)=q(y).
\]
Therefore $\widetilde H$ is a homotopy from $p$ to $q$ relative to $\partial I^{N}$.

Hence $p$ and $q$ are homotopic relative to the boundary, as claimed.
\end{proof}
