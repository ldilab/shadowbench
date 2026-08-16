
\begin{theorem}[Strict maximum principle for elliptic operators]
Let $\Omega\subset \mathbb{R}^n$ be connected and open. Let
\[
Lu
=
\sum_{i,j=1}^n a^{ij}(x)u_{ij}
+
\sum_{i=1}^n b^i(x)u_i
+
c(x)u
\]
be uniformly elliptic in $\Omega$, where $a^{ij},b^i,c$ are continuous and
\[
c(x)\le 0 \qquad \text{in } \Omega.
\]
Suppose
\[
u\in C^2(\Omega), \qquad Lu\ge 0 \quad \text{in } \Omega.
\]
If $u$ attains a nonnegative maximum at an interior point $x_0\in \Omega$, i.e.
\[
u(x_0)=\max_{\Omega}u=:M\ge 0,
\]
then
\[
u\equiv M
\qquad \text{in } \Omega.
\]
\end{theorem}
\begin{proof}
Let $M=\max_{\Omega}u$ and set $v:=M-u$. Then $v\ge 0$, $v(x_0)=0$, and $Lv\le 0$.

Let $A:=\{x\in\Omega:\, v(x)=0\}$. Then $A$ is closed and nonempty.

If $z\in A$ is not interior, pick $y\notin A$ and a ball $B_\rho(y)\subset\Omega$ tangent to $A$ at $z_0\in A$; then $v>0$ in $B_\rho(y)$ and $v(z_0)=0$.

By the Hopf lemma, $\partial_\nu v(z_0)<0$, but $z_0$ is an interior minimum of $v$, so $\nabla v(z_0)=0$ — contradiction.

Hence $A$ is open; since $\Omega$ is connected, $A=\Omega$, so $u\equiv M$.
\end{proof}



\begin{lemma}[Hopf lemma]
Let $\Omega\subset \mathbb{R}^n$ be a domain and let $L$ be uniformly elliptic
with continuous coefficients and $c\le 0$.

Suppose
\[
u\in C^2(\Omega)\cap C(\overline{\Omega}),
\qquad
Lu\le 0 \quad \text{in } \Omega.
\]
Let $x_0\in \partial\Omega$ satisfy the interior sphere condition.

If
\[
u(x_0)=\min_{\overline{\Omega}} u,
\qquad
u(x)>u(x_0)\ \text{for all }x\in \Omega,
\]
then
\[
\frac{\partial u}{\partial \nu}(x_0)<0,
\]
where $\nu$ is the outward unit normal at $x_0$.
\end{lemma}

\begin{lemma}[Interior extremum condition]
Let $u\in C^2(\Omega)$ and suppose $x_0\in \Omega$ is a local maximum (or minimum).
Then
\[
\nabla u(x_0)=0,
\qquad
D^2 u(x_0)\le 0 \; (\text{resp. } \ge 0).
\]
\end{lemma}
