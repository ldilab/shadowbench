\begin{definition}[Trivialization.pullback_linear]
Let $E$ be a vector bundle over a base space $B$ with fiber $F$, where $F$ is a normed space over a normed field $k$. Given a continuous map $f: B' \to B$, the pullback bundle $f^*E$ is defined to be a vector bundle over $B'$ whose fiber $(f^*E)_x$ is defined as $E_{f(x)}$ for each $x \in B'$. It is a disjoint union $\bigsqcup_{x \in B'} (f^*E)_x$ of all these fibers equipped with the coarsest topology for which both the projections $\pi'$ to the base $B'$ and $f'$ to the original bundle $E$
\begin{align*}
    \pi': f^*E \to B', \quad (x,v) \mapsto x, \quad f':f^*E \to E, \quad (x,v) \mapsto v, \quad x \in B',\, v \in (f^*E)_x
\end{align*}
are continuous.
\end{definition}

\begin{theorem}[VectorBundle.pullback]
Given a vector bundle $E$ over a base space $B$ with fiber $F$ and a continuous map $f:B' \to B$, the pullback bundle $f^*E$ over $B'$ inherits the structure of a vector bundle.
\end{theorem}
\begin{proof}
Let $\pi:E \to B$ be a vector bundle with fiber $F$, a normed space over a normed field $k$, and let $f: B' \to B$ be a continuous map. We aim to show that the pullback bundle $ \pi':f^*E \to B'$ is naturally a vector bundle.

For each $x \in B'$, the fiber $(f^*E)_x$ is defined as $E_{f(x)}$. Since $E_{f(x)}$ is a vector space over $k$, the fiber $(f^*E)_x$ inherits the same vector space structure.

Let $e$ be a local trivialization of $E$ over an open set $U \subseteq B$. That is, $e: E|_U \xrightarrow{\simeq} U \times F$ is a homeomorphism such that $\pi = p \circ e$ where $p: U \times F \to U$ is the projection, and $e|_{E_x}: E_x \xrightarrow{\simeq} F$ is a linear isomorphism. The pullback of $ e $ along $ f $ gives a local trivialization 
\begin{align*}
	f^*e:= (f^*E)|_{f^{-1}(U)} \xrightarrow{\simeq} f^{-1}(U) \times F, \quad (x,v) \mapsto (x,e|_{E_{f(x)}}(v)), \quad x \in f^{-1}(U), \, v \in E_{f(x)}
\end{align*}
Then, each $(f^*e)|_{E_x} = e|_{E_{f(x)}}$ is a linear isomorphism as desired.

The transition maps for $f^*E$ are obtained by pulling back the transition maps of $ E $ along $ f $. Explicitly, given two trivializations $e_U:E|_U \xrightarrow{\simeq} U \times F$, $e_V:E|_V \xrightarrow{\simeq} V \times F$ for open subsets $U,V \subseteq B$, we have 
\begin{align*}
	(U \cap V) \times F \xrightarrow[e_U^{-1}]{\simeq} E|_{U \cap V} \xrightarrow[e_V]{\simeq} (U \cap V) \times F, \quad (x,a) \mapsto (e_U|_{E_x})^{-1}(a) \mapsto (x,(e_V|_{E_x} \circ (e_U|_{E_x})^{-1})(a))
\end{align*}
and transition map $g_{UV}: U \cap V \to \text{GL}(F)$ is defined to be
\begin{align*}
	g_{UV}(x) = e_V|_{E_x} \circ (e_U|_{E_x})^{-1}, \quad x \in U \cap V.
\end{align*}
Then, the transition maps of the pullback bundle $f^*E$ are of the form
\begin{align*}
	(f^*g)_{f^{-1}(U) f^{-}(V)}(x) &= (f^*e)_{f^{-1}(V)}|_{(f^*E)_x} \circ ((f^*e)_{f^{-1}(U)}|_{(f^*E)_x})^{-1}, \quad x \in f^{-1}(U) \cap f^{-1}(V) \\
    &= e_V|_{E_{f(x)}} \circ (e_U|_{E_{f(x)}})^{-1} \\
    &= g_{UV}(f(x))
\end{align*}
That is, we have
\begin{align*}
    (f^*g)_{f^{-1}(U) f^{-}(V)} = g_{UV} \circ f.
\end{align*}
Since $f$ is continuous, transition maps of $f^*E$ are continuous and define a linear automorphism of $F$ for each $x \in B'$. Therefore, $f^*E$ inherits the natural structure of a vector bundle.
\end{proof}
