\begin{theorem}[isProperMap_proj_iff_compactSpace]
Suppose $\pi : E \to M$ is a fiber bundle with fiber $F$.
Then $\pi$ is a proper map if and only if $F$ is compact.
\end{theorem}

\begin{proof}
Because $\pi : E \to M$ is a fiber bundle projection, it is continuous, and for every $p \in M$ there exists an open neighborhood $U$ of $p$ and a homeomorphism
\[
\Phi:\pi^{-1}(U)\to U\times F
\]
such that
\[
\pi|_{\pi^{-1}(U)}=\operatorname{pr}_1\circ \Phi,
\]
where $\operatorname{pr}_1:U\times F\to U$ is projection onto the first factor.

\medskip
\noindent $(\Rightarrow)$ Suppose $\pi$ is proper. For any $p\in M$, the singleton $\{p\}$ is compact. Hence
\[
\pi^{-1}(\{p\})=\pi^{-1}(p)
\]
is compact. But each fiber $\pi^{-1}(p)$ is homeomorphic to $F$, so $F$ is compact.

\medskip
\noindent $(\Leftarrow)$ Suppose $F$ is compact. We will show that $\pi$ is proper by proving that $\pi$ is a continuous closed map with compact fibers (Proposition A.53(b)).

First, for each $p\in M$, the fiber $\pi^{-1}(p)$ is homeomorphic to $F$, hence compact.

Now let $C\subseteq E$ be closed. We show that $\pi(C)$ is closed in $M$. Let $p\in M\setminus \pi(C)$. Choose a trivializing neighborhood $U$ of $p$ and a trivialization
\[
\Phi:\pi^{-1}(U)\to U\times F.
\]
Then $C\cap \pi^{-1}(U)$ is closed in $\pi^{-1}(U)$, so $\Phi(C\cap \pi^{-1}(U))$ is closed in $U\times F$. Since $F$ is compact, the projection
\[
\operatorname{pr}_1:U\times F\to U
\]
is a closed map. Therefore
\[
\pi(C)\cap U
=
\pi(C\cap \pi^{-1}(U))
=
\operatorname{pr}_1\bigl(\Phi(C\cap \pi^{-1}(U))\bigr)
\]
is closed in $U$.

Because $p\notin \pi(C)$, we have
\[
p\in U\setminus (\pi(C)\cap U),
\]
and this is an open neighborhood of $p$ in $M$ disjoint from $\pi(C)$. Hence every point of $M\setminus \pi(C)$ has an open neighborhood contained in $M\setminus \pi(C)$, so $M\setminus \pi(C)$ is open. Thus $\pi(C)$ is closed, and $\pi$ is a closed map.

Therefore $\pi$ is a continuous closed map with compact fibers. By Proposition A.53(b), $\pi$ is proper.

Hence $\pi$ is proper if and only if $F$ is compact.
\end{proof}
