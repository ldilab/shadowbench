\begin{definition}[singularChainComplexFunctor]
    Given a preadditive category $C$ with coproducts and homology, the singular chain complex functor is the functor
    \begin{align*}
        C_\bullet(-;-): C \to \text{Fun}(\textbf{Top}, \textbf{Ch}_{\ge 0}(C)),\quad R \mapsto (X \to C_\bullet(X;R))
    \end{align*}
    from $C$ to the category of functors from the category $\textbf{Top}$ of topological spaces and the category $\textbf{Ch}_{\ge 0}(C)$ of chain complexes in $C$ defined as follows. Given a topological space $X$, we have an associated simplicial set $\text{Sing}(X) = \{\text{Sing}(X)_n\}$ where $\text{Sing}(X)_n$ is the set of singular $n$-simplices, that is, continuous maps from the standard $n$-simplex $\Delta_n$ to $X$. For each $n =0,1,2,\cdots$, the $i$-th face map $d_i^n:X_n \to X_{n-1}$ maps the singular $n$-simplex $\sigma$ to its restriction to the $i$-th face of $\Delta_n$ which is the set of points of $\Delta_n$ whose $i$-th coordinate is $0$. Then $C_\bullet(X;R)$ is the chain complex with
    \begin{align*}
        C_n(X;R) = \coprod_{X_n} R, \quad d_n:C_n(X;R) \to C_{n-1}(X;R),\,\, d_n = \sum_{i=0}^n (-1)^i d_i^n
    \end{align*}
\end{definition}

\begin{definition}[singularHomologyFunctor]
    Let $C$ be a preadditive category wth coproducts and homology. Then the singular homology functor is the functor
    \begin{align*}
        H_\bullet(-;-):C \to \text{Fun}(\textbf{Top},\textbf{Ch}_{\ge 0}(C)), R \mapsto (X \mapsto H_\bullet(X;R))
    \end{align*}
    where $H_n(X;R)$ is the $n$-th homology of the chain complex $C_\bullet(X;R)$.
\end{definition}

\begin{theorem}[isZero_singularHomologyFunctor_of_totallyDisconnectedSpace]
    Let $X$ be a totally disconnected topological space, $C$ a preadditive category with coproducts and homology, and $R$ an object of $C$. Then, we have
    \begin{align*}
        H_n(X;R) = 0 
    \end{align*}
for all $n > 0$.
\end{theorem}
\begin{proof}
    Since $X$ is totally disconnected, any singleton of $X$ is open. So any continuous map from a connected space is constant. Hence, any singular $n$-simplex of $X$ is a constant map, and we have identification $\text{Sing}(X)_n \simeq X$, $\sigma \mapsto \text{Im}(\sigma)$. Moreover, face maps $d_i^n$ are just restrictions of singular simplices, so they are all the identity map $X \to X$ under the identifications $\text{Sing}(X)_n \simeq X \simeq \text{Sing}(X)_{n-1}$. Thus, we have
    \begin{align*}
        d_n = \sum_{i=0}^n (-1)^nd_i^n = \begin{cases}
            0, &\text{if } n= \text{ even} \\
            \text{id}, &\text{if } n= \text{ odd}
        \end{cases}
    \end{align*}
    and the singular chain complex $C_\bullet(X;R)$ is of the form
    \begin{align*}
        \coprod_{x \in X} R \xleftarrow{0} \coprod_{x \in X} R \xleftarrow{\text{id}} \coprod_{x \in X} R \xleftarrow{0} \cdots
    \end{align*}
    Therefore, we have
    \begin{align*}
        H_n(X;R) = 0
    \end{align*}
for all $n > 0$.
\end{proof}

\begin{theorem}[singularHomologyFunctorZeroOfTotallyDisconnectedSpace]
    Let $X$ be a totally disconnected topological space, $C$ a preadditive category with coproducts and homology, and $R$ an object of $C$. Then, we have
    \begin{align*}
        H_0(X;R) =  \coprod_{x \in X} R
    \end{align*}
\end{theorem}
\begin{proof}
    Since $X$ is totally disconnected, any singleton of $X$ is open. So any continuous map from a connected space is constant. Hence, any singular $n$-simplex of $X$ is a constant map, and we have identification $\text{Sing}(X)_n \simeq X$, $\sigma \mapsto \text{Im}(\sigma)$. Moreover, face maps $d_i^n$ are just restrictions of singular simplices, so they are all the identity map $X \to X$ under the identifications $\text{Sing}(X)_n \simeq X \simeq \text{Sing}(X)_{n-1}$. Thus, we have
    \begin{align*}
        d_n = \sum_{i=0}^n (-1)^nd_i^n = \begin{cases}
            0, &\text{if } n= \text{ even} \\
            \text{id}, &\text{if } n= \text{ odd}
        \end{cases}
    \end{align*}
    and the singular chain complex $C_\bullet(X;R)$ is of the form
    \begin{align*}
        \coprod_{x \in X} R \xleftarrow{0} \coprod_{x \in X} R \xleftarrow{\text{id}} \coprod_{x \in X} R \xleftarrow{0} \cdots
    \end{align*}
    Therefore, we have
    \begin{align*}
        H_0(X;R) = \coprod_{x \in X} R.
    \end{align*}
\end{proof}
