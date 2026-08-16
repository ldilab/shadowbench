\begin{definition}[sheafify]
	Let $X$ be a topological space and $\mathcal{F}$ a presheaf of sets on $X$. Let $\widetilde{\mathcal{F}}$ be the presheaf 
\begin{align*}
U \mapsto \{(s_x)_{x \in U} \in \prod_{x \in U} \mathcal{F}_x  \text{ such that $(*)$.}\}
\end{align*}
where $(*)$ is the property that for any $x \in U$, there exists an open neighborhood $V \subseteq U$ of $x$, and a section $s \in \mathcal{F}(V)$ such that $s_y = (V,s) \in \mathcal{F}_y$ for all $y \in V$. Then $\widetilde{\mathcal{F}}$ is a sheaf and is called the sheafification of the presheaf $\mathcal{F}$.
\end{definition}

\begin{theorem}[sheafifyStalkIso]
	Let $X$ be a topological space and $\mathcal{F}$ a presheaf of sets on $X$. Let $\widetilde{\mathcal{F}}$ be the sheafification of $\mathcal{F}$. For $x \in X$, an obvious map
\begin{align*}
	\phi_x: \widetilde{\mathcal{F}}_x \to \mathcal{F}_x, \quad (U,s) \mapsto s(x)
\end{align*}
is an isomorphism of stalks $\widetilde{\mathcal{F}}_x$ and $\mathcal{F}_x$.
\end{theorem}

\begin{proof}
We prove the surjectivity first. Let $(U,s) \in \mathcal{F}_x$ be given where $U$ is an open neighborhood of $x$ and $s \in \mathcal{F}(U)$. Then, $t:=(s_y)_{y \in U} \in \widetilde{F}(U)$ and we have $(U,t) \in \widetilde{F}_x$ which is mapped to $(U,s)$ under $\phi_x$ since $t(x) = s_x = (U,s)$.

For injectivity, suppose we have $(U,s), (V,t) \in \widetilde{\mathcal{F}}_x$ such that $s(x) = t(x)$. By definition of the sheafification, there exist open neighborhoods $U’\subseteq U$,$V’\subseteq V$ of $x$ and sections $s’ \in \mathcal{F}(U’)$, $t’ \in \mathcal{F}(V’)$ such that $s’_y = s(y)$ for all $y \in U’$ and $t’_z = t(z)$ for all $z \in V’$. Thus, we have
\begin{align*}
(U’,s’) = s’_x = s(x) = t(x) = t’_x = (V’,t’)
\end{align*}
and it follows that there exists an open neighborhood $W \subseteq U’ \cap V’$ of $x$ such that $s’|_W = t’|_W$. Then, for any $y \in W$, we have
\begin{align*}
	s(y) = s’_y = (W,s’) = (W,t’) = t’_y = t(y)
\end{align*}
that is, two sections $s,t$ of $\widetilde{\mathcal{F}}$ agree on $W$. Therefore, we have
\begin{align*}
	(U,s) = (W,s|_W) = (W,t|_W) = (V,s)
\end{align*}
and the map $\phi_x$ is injective.
\end{proof}
