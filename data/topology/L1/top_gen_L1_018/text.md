\begin{definition}[IsFlasque]Let \(X\) be a topological space. A presheaf \(F\) on \(X\) is called \emph{flasque} if for every inclusion of open sets
\[
V \subseteq U,
\]
the restriction map
\[
F(U)\to F(V)
\]
is an epimorphism. A sheaf is called \emph{flasque} if its underlying presheaf is flasque.
\end{definition}


\begin{theorem}[epi_of_shortExact]
Suppose
\[
0 \to \mathcal F \to \mathcal G \to \mathcal H \to 0
\]
is a short exact sequence of sheaves of abelian groups on \(X\).
If \(\mathcal F\) is flasque, then for any open set $U \subseteq X$, the map $\mathcal{G}(U) \to \mathcal{H}(U)$ is surjective.
\end{theorem}
\begin{proof}
Fix an open set \(U \subseteq X\) and a section \(s \in \mathcal H(U)\). Consider the set
\[
\mathcal S = \{(V,t) | V \subseteq U \text{ is an open subset and } t \in \mathcal{F}(V) \text{ such that } g(t) = s|_V\}.
\]
partially ordered as follows: an element \((V',t') \) is said to dominate \((V,\) if \(V \subseteq V'\) and \(t'|_V = t\). We call an element of \(\mathcal S\) a partial lift of $s$. Then every chain of \(\mathcal S\) has an upper bound. Indeed, let
\[
\{(V_\alpha,t_\alpha)\}
\]
be a chain of partial lifts of \(s\).
Because the open sets \(V_\alpha\) are linearly ordered by inclusion, the sections \(t_\alpha\) agree on overlaps.
Hence, by the sheaf gluing axiom, they glue to a section
\[
t \in \mathcal{F}\Bigl(\bigcup_\alpha V_\alpha\Bigr).
\]
This glued section still maps to \(s\) restricted to \(\bigcup_\alpha V_\alpha\), so it defines a partial lift over \(\bigcup_\alpha V_\alpha\).
By construction, this partial lift dominates every member of the chain.

Since \((U,s) \in \mathcal{S}\), by Zorn's lemma, there exists a maximal partial lift
\[
t \in \mathcal G(V),
\qquad
V \subseteq U,
\]
such that
\[
g(t) = s|_V.
\]

We claim that \(V=U\).
Let \(x \in U\).
Since \(g : \mathcal G \to \mathcal H\) is an epimorphism of sheaves, it is locally surjective, so there exists an open neighborhood \(W \ni x\) and a section
\[
t_1 \in \mathcal G(W)
\]
such that
\[
g(t_1)=s|_W.
\]

On the overlap \(V \cap W\), both \(t|_{V\cap W}\) and \(t_1|_{V\cap W}\) map to the same section of \(\mathcal H(V\cap W)\).
Hence their difference
\[
t_2 := t|_{V\cap W} - t_1|_{V\cap W}
\]
lies in the kernel of
\[
g(V\cap W) : \mathcal G(V\cap W)\to \mathcal H(V\cap W).
\]
By exactness, there exists
\[
t_3 \in \mathcal F(V\cap W)
\]
such that
\[
f(t_3)=t_2.
\]

Since \(\mathcal F\) is flasque, the section \(t_3\) extends to a section
\[
t_4 \in \mathcal F(W).
\]
Define
\[
t_1' := t_1 + f(t_4) \in \mathcal G(W).
\]
Then on \(V\cap W\) we have
\[
t_1'|_{V\cap W}
=
t_1|_{V\cap W} + f(t_4)|_{V\cap W}
=
t_1|_{V\cap W} + f(t_3)
=
t_1|_{V\cap W} + t_2
=
t|_{V\cap W}.
\]
Thus \(t\) on \(V\) and \(t_1'\) on \(W\) glue to a section
\[
t_5 \in \mathcal G(V \cup W)
\]
such that
\[
g(t_5)=s|_{V\cup W}.
\]
So \((V \cup W, t_5)\) is a partial lift of \(s\) dominating \((V,t)\).

By maximality of \((V,t)\), this is only possible if
\[
W \subseteq V.
\]
Since \(x \in W\), we conclude that \(x \in V\).
As \(x\) was arbitrary, \(U \subseteq V\).
But already \(V \subseteq U\), so \(V=U\).

Therefore \(s\) lifts to a section of \(\mathcal G(U)\), proving that
\[
g(U) : \mathcal G(U)\to \mathcal H(U)
\]
is surjective.
\end{proof}

\begin{theorem}[of_shortExact_of_isFlasque]
Suppose
\[
0 \to \mathcal F \to \mathcal G \to \mathcal H \to 0
\]
is a short exact sequence of sheaves of abelian groups on \(X\).
If \(\mathcal F\) and \(\mathcal G\) are flasque, then \(\mathcal H\) is flasque.
\end{theorem}

\begin{proof}
Let \(V \subseteq U\) be an inclusion of open sets. We must prove that the restriction map
\[
\mathcal H(U)\to \mathcal H(V)
\]
is surjective.

By naturality, we have a commutative diagram
\[
\begin{array}{ccc}
    \mathcal G(U) & \xrightarrow{g(U)} &\mathcal H(U) \\
    \downarrow & & \downarrow\\
      \mathcal G(V) & \xrightarrow{g(V)}& \mathcal H(V)
\end{array}
\]
Now since \(\mathcal G\) is flasque, the restriction map \(\mathcal G(U)\to \mathcal G(V)\)
is surjective. Also, by the theorem above, since \(\mathcal F\) is flasque, the map \(g(V):\mathcal G(V)\to \mathcal H(V)\) is surjective. Hence, the composition \(
\mathcal G(U)\to \mathcal G(V)\xrightarrow{g(V)} \mathcal H(V)
\) is surjective. Therefore the map
\[
\mathcal H(U)\to \mathcal H(V)
\]
must also be surjective. Thus \(\mathcal H\) is flasque.
\end{proof}
