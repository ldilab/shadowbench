\begin{definition}[MeromorphicAt] Let $\mathbb{K}$ be a nontrivially normed field and let $E$ be a normed vector space over $\mathbb{K}$. Let $f : \mathbb{K} \to E$ be an $E$-valued function on $\mathbb K$ and let $x \in \mathbb{K}$. We say that $f$ is \emph{meromorphic at $x$} if there exists $n \in \mathbb{N}$ such that the function
\[
z \longmapsto (z - x)^n f(z)
\]
is analytic at $x$.
\end{definition}

\begin{lemma}[AnalyticAt.meromorphicAt] 
Let $f : \mathbb K \to E$ and let $x \in \mathbb K$. If $f$ is analytic at $x$, then $f$ is meromorphic at $x$.
\end{lemma}


\begin{proof}
Assume that $f$ is analytic at $x$. Choose $n = 0$. Then
\[
(z - x)^0 f(z) = f(z),
\]
which is analytic at $x$ by assumption. Hence $f$ is meromorphic at $x$ by definition.
\end{proof}
