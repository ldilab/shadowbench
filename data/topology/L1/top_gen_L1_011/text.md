\begin{definition}[continuousLinearMap]
    Let $E_1$, $E_2$ be vector bundles over a base space $B$ with fibers $F_1$, $F_2$, respectively, where $F_i$ is a normed space over a normed field $k_i$, for $i=1,2$. Let $\sigma: k_1 \to k_2$ be an isometric ring homomorphism. The Hom-bundle $\text{Hom}_\sigma (E_1,E_2)$ is defined to be a vector bundle over $B$ whose fiber $\text{Hom}_\sigma (E_1,E_2)_x$ is defined as the space of $\sigma$-semilinear maps between $(E_1)_x$ and $(E_2)_x$.
\end{definition}

\begin{theorem}[Bundle.ContinuousLinearMap.vectorBundle]
     Let $E_1$, $E_2$ be vector bundles over a base space $B$ with fibers $F_1$, $F_2$, respectively, where $F_i$ is a normed space over a normed field $k_i$, for $i=1,2$. Let $\sigma: k_1 \to k_2$ be an isometric ring homomorphism. The Hom-bundle $\text{Hom}_\sigma (E_1,E_2)$ inherits the natural structure of a vector bundle.
\end{theorem}
\begin{proof}
    For each $x \in B$, the fiber $\text{Hom}_\sigma(E_1,E_2)_x$ is the space of $\sigma$-semilinear maps between $(E_1)_x$ and $(E_2)_x$. There exist an operator norm of semilinear maps and a scalar multiplication
    \begin{align*}
        (a \cdot f)(m) = a \cdot f(m), \quad a \in k_2,\, f \in \text{Hom}_\sigma(E_1,E_2)_x, \,m \in (E_1)_x
    \end{align*}
    so that $\text{Hom}_\sigma(E_1,E_2)_x$ has the natural structure of a normed space over $k_2$.

    Now we define local trivializations. Let 
    \begin{align*}
        e_1:E_1|_{U_1} \xrightarrow{\simeq} U_1 \times F_1, \quad e_2: E_2|_{U_2} \xrightarrow{\simeq} U_2 \times F_2
    \end{align*}
    be local trivializations of $E_1,E_2$, respectively, for open subsets $U_1,U_2 \subseteq B$. Then we define a local trivialization of the Hom-bundle over $U:= U_1 \cap U_2$ by
    \begin{align*}
        e: \text{Hom}_\sigma(E_1,E_2)|_U \xrightarrow{\simeq} U \times \text{Hom}_\sigma(F_1,F_2), \quad (x,T) \mapsto (x,(e_2)_x \circ T \circ (e_1)_x^{-1})
    \end{align*}
    for $x \in B$, $T \in \text{Hom}_\sigma(E_1,E_2)_x$, where $(e_i)_x=e_i|_{(E_i)_x}: (E_i)_x \xrightarrow{\simeq} F_i$, $i=1,2$ are linear isomorphisms. 

    For transition maps, let $e,e'$ be local trivializations of the Hom-bundle over $U,U'$, respectively, which are induced by the pairs of local trivializations $(e_1,e_2),(e_1',e_2')$. For each $i=1,2$, we have transition maps
    \begin{align*}
        g_i: U_i \cap U_i' \to \text{GL}(F_i)
    \end{align*} 
    where $g_i$ is induced from the composition
    \begin{align*}
        (U_i \cap U_i') \times F_i \xrightarrow[e_i^{-1}]{\simeq} E_i|_{U_i \cap U_i'} \xrightarrow[e_i]{\simeq} (U_i \cap U_i') \times F_i
    \end{align*}
    of the bundle $E_i$. Now for the Hom-bundle, define the transition map as
    \begin{align*}
        g: U \cap U' \to \text{GL}(\text{Hom}_\sigma(F_1,F_2)), \quad x \mapsto (S \mapsto g_2(x) \circ S \circ g_1(x)^{-1})
    \end{align*}
    By construction, local trivializations and transition maps of the Hom-bundle above are continuous and define the natural vector bundle structure on the Hom-bundle.
\end{proof}
