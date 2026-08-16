\begin{definition}[normalizedMooreComplex]
Let $C$ be an abelian category. We define the normalized Moore complex to be a functor
\begin{align*}
    N_\bullet: \mathbf{sC} \to \mathbf{Ch}_{\ge 0}(C), \quad X \mapsto N_\bullet(X)
\end{align*}
from the category $\mathbf{sC}$ of simplicial objects of $C$ to the category $\mathbf{Ch}_{\ge 0}(C)$ of chain complexes in $C$ where
\begin{align*}
    N_n(X) = \begin{cases}
        X_0, &\text{for $n=0$}\\
        \bigcap_{i=1}^n \ker (d_i^n:X_n \to X_{n-1}), &\text{for $n > 0$}
    \end{cases}
\end{align*}
where $d_i^n:X_n \to X_{n-1}$ is the $i$-th face map. The differentials are defined to be $d_n := d_0^n|_{N_n(X)}:N_n(X) \to N_{n-1}(X)$ where $d_0^n:X_n \to X_{n-1}$ is the $0$-th face map. For a morphism $f:X \to Y$ in the category $\mathbf{sC}$, we define $N_\bullet(f):N_\bullet(X) \to N_\bullet(Y)$ by $N_n(f):=f_n|_{N_n(X)}:N_n(X) \to N_n(Y)$.
\end{definition}
\begin{theorem}[normalizedMooreComplex_objD]
    $N_\bullet$ is a well-defined functor.
\end{theorem}
\begin{proof}
    We first show that it is well-defined on objects. That is, for each simplicial object $X$ in $C$, the sequence $N_\bullet(X)$ together with $d_\bullet$ is a chain complex. It suffices to prove that for each $n=1,2,\cdots$, $d_n:N_n(X) \to N_{n-1}(X)$ is well-defined and $d_{n-1} \circ d_n$ is the zero map.

    For well-definedness, it suffices to check $d_i^{n-1} \circ d_0^n|_{N_n(X)} : N_n(X) \to X_{n-1} \to X_{n-2}=0$ for all $i=1,2,\cdots,n-1$. Indeed, by simplicial identities, we have
    \begin{align*}
        d_i^{n-1} \circ d_0^n|_{N_n(X)} = d_0^{n-1} \circ d_{i+1}^n|_{N_n(X)} = 0 
    \end{align*}
    by construction of $N_n(X)$. Similarly, we have
    \begin{align*}
        d_{n-1} \circ d_n = d_0^{n-1} \circ d_0^n|_{N_n(X)} = d_0^{n-1} \circ d_1^n|_{N_n(X)} = 0.
    \end{align*}

    Now we prove that $N_\bullet$ is well-defined on morphisms. A morphism $f:X \to Y$ in the category $\mathbf{sC}$ is a collection of morphisms $f_n:X_n \to Y_n$ in the category $C$ compatible with face maps of $X$ and $Y$. That is, we have $f_{n-1} \circ d_i^n = d_i^n \circ f_n$ for all $n \ge 0$. Then, for all $i=1,\cdots,n$,
    \[
    d_i^n \circ N_n(f) = d_i^n \circ f_n|_{N_n(X)} = f_{n-1} \circ d_i^n |_{N_n(X)} = 0
    \]
    so that $f_n|_{N_n(X)}: N_n(X) \to Y_n$ factors through $N_n(Y)$ so that $N_n(f)$ is a well-defined morphism $N_n(X) \to N_n(Y)$.
\end{proof}
