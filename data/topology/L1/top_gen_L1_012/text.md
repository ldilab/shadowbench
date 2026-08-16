\begin{definition}[skyscraperPresheaf]
    Let $X$ be a topological space. $p_0 \in X$. Let $\mathcal{C}$ be a category with a terminal object and $A \in \text{Ob}(\mathcal{C})$ be an object of $\mathcal{C}$. A skyscraper sheaf $\mathcal{F}$ with value $A$ is a presheaf on $X$ with values in $\mathcal{C}$ such that
    $\mathcal{F}(U) = A$ if $p_0 \in U$ and $\mathcal{F}(U) = 1_\mathcal{C}$ if $p_0 \notin U$ where $1_\mathcal{C}$ is some terminal object of $\mathcal{C}$.
\end{definition}

\begin{theorem}[skyscraperPresheaf_isSheaf]
    A skyscraper presheaf with value $A$ is a sheaf.
\end{theorem}
\begin{proof}
    Consider the obvious continuous map $f: * \to X$ from the one-point space to $X$ such that $f(*) = p_0$. Let $\mathcal{F}$ be a skyscraper presheaf on $X$ at $p_0$ with value $A$, and $\mathcal{G}$ a skyscraper presheaf on $*$ with value $A$. We claim that
    \begin{align*}
        \mathcal{F} = f_*\mathcal{G}
    \end{align*}
    Indeed, for an open set $U \subseteq X$, we have
    \begin{align*}
        (f_*\mathcal{G})(U) = \mathcal{G}(f^{-1}(U)) = \mathcal{G}(*) = A, \quad p_0 \in U \\
        (f_*\mathcal{G})(U) = \mathcal{G}(f^{-1}(U)) = \mathcal{G}(\emptyset) = 1_\mathcal{C}, \quad p_0 \notin U
    \end{align*}
    so that $\mathcal{F} = f_*\mathcal{G}$.

    Note that on the one-point space, a presheaf is a sheaf if and only if its value at empty set is a terminal object. Hence, a skyscraper presheaf $\mathcal{G}$ is a sheaf on $*$. Meanwhile, since the pushforward of a sheaf is a sheaf, $\mathcal{F} = f_*\mathcal{G}$ is a sheaf on $X$ as well.
\end{proof}
