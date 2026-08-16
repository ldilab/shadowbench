\begin{definition}[alternatingFaceMapComplex]
    Let $C$ be a preadditive category. We define alternating face map complex to be a functor
    \[
        C_\bullet: \mathbf{sC} \to \mathbf{Ch}_{\ge 0}(C), \quad X \mapsto C_\bullet(X)
    \]
    from the category $\mathbf{sC}$ of simplicial objects of $C$ to the category $\mathbf{Ch}_{\ge 0}(C)$ of chain complexes in $C$ where $C_n(X) = X_n$ for each $n=0,1,\cdots$, and the differentials $d_n:C_n(X) \to C_{n-1}(X)$ are defined by
    \begin{align*}
        d_n = \sum_{i=0}^n (-1)^n d_i^n
    \end{align*}
    where $d_i^n:X_n \to X_{n-1}$ is the $i$-th face map. For a morphism $f:X \to Y$ of simplicial objects, we define $C_\bullet(f):C_\bullet(X) \to C_\bullet(Y)$ by $C_n(f) = f_n$ for all $n$.

Then, $C_\bullet$ is a well-defined functor.
\end{definition}
\begin{proof}
    We first show that it is well-defined on objects. That is, for each simplicial object $X$ of $C$, the sequence $C_\bullet(X)$ together with $d_\bullet$ is a chain complex. It suffices to show that $d_{n-1}\circ d_n = 0$ for all $n=1,2,\cdots$, and we have
    \begin{align*}
        d_{n-1} \circ d_n &= \sum_{i=0}^{n-1} \sum_{j=0}^n (-1)^{i+j} d_i^{n-1} \circ d_j^n \\
        &= \sum_{i < j} (-1)^{i+j} d_i^{n-1} \circ d_j^n + \sum_{i \ge j} (-1)^{i+j} d_i^{n-1} \circ d_j^n \\
        &= \sum_{i < j} (-1)^{i+j} d_{j-1}^{n-1} \circ d_i^n + \sum_{i \ge j} (-1)^{i+j} d_i^{n-1} \circ d_j^n \\
        &= \sum_{i \le j'} (-1)^{i+j'+1} d_{j'}^{n-1} \circ d_i^n + \sum_{i \ge j} (-1)^{i+j} d_i^{n-1} \circ d_j^n \\
        &= 0.
    \end{align*}
    For a morphism $f: X \to Y$, $f_n$'s commute with the face maps of $X$ and $Y$, and hence $f$ is compatible with the differentials of $C_\bullet(X)$ and $C_\bullet(Y)$. That is, $f_{n-1} \circ d_n = d_n \circ f_n$ for each $n$, and thus $C_\bullet(f)$ is a well-defined morphism from $C_\bullet(X)$ to $C_\bullet(Y)$
\end{proof}

\begin{theorem}[inclusionOfMooreComplex]
    Let $C$ be an abelian category. Then there is an inclusion $N_\bullet \hookrightarrow C_\bullet $ from the normalized Moore complex into the alternating face map complex, as a natural transformation of functors.
\end{theorem}
\begin{proof}
    We define the map of functors $i:N_\bullet \to C_\bullet$ as follows. For a simplicial object $X$ in $C$ and for each $n=0,1,2,\cdots$, we have a natural inclusion
    \begin{align*}
        i_n: N_n(X) = \bigcup_{i=0}^n \ker(d_i^n:X_n \to X_{n-1}) \hookrightarrow X_n=C_n(X).
    \end{align*}
    To show that they induce an inclusion of chain complexes, it suffices to show that the inclusions above commute with the differentials. Indeed, denote the differentials of $N_\bullet(X)$, $C_\bullet(X)$ by $d_\bullet^N$, $d_\bullet^C$, respectively. Then, we have
    \begin{align*}
        d_n^C \circ i_n = i_n \circ \sum_{i=0}^n d_i^n|_{N_n(X)} = i_n \circ d_0^n|_{N_n(X)} = i_n \circ d_n^N
    \end{align*}
    since $N_n(X) \subseteq \ker d_i^n$ for all $i=1,2,\cdots,n$. Therefore, we have an inclusion of chain complexes $i_X: N_\bullet(X) \hookrightarrow C_\bullet(X)$ with $(i_X)_n:= i_n:N_n(X) \hookrightarrow C_n(X)$. 

    Moreover, this inclusion defines a natural transformation since for any other simplicial object $Y$ in $C$ and a morphism $f:X \to Y$ of simplicial objects, we have $i_Y \circ N_\bullet(f) = C_\bullet(f) \circ i_X$ by construction.
\end{proof}
