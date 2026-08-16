\begin{definition}[divisor] Let $\mathbb K$ be a nontrivially normed field and let $E$ be a normed vector space over $\mathbb K$.
Let $U \subseteq \mathbb K$ be a set and let $f : \mathbb K \to E$ be a function. The \emph{divisor} of $f$ on $U$ is the function
\[
\operatorname{div}_U(f) : \mathbb K \longrightarrow \mathbb{Z}
\]
defined by
\[
\operatorname{div}_U(f)(z)
=
\begin{cases}
\operatorname{ord}_z(f), & \text{if $f$ is meromorphic on $U$ and $z \in U$},\\[6pt]
0, & \text{otherwise}.
\end{cases}
\]
\end{definition}


\begin{definition}[divisor_support]
The \emph{support} of the divisor is
\[
\operatorname{supp}(\operatorname{div}_U(f))
=
\{ z \in U \mid \operatorname{div}_U(f)(z) \neq 0 \}.
\]

Equivalently,
\[
\operatorname{supp}(\operatorname{div}_U(f))
=
\{ z \in U \mid \operatorname{ord}_z(f) \neq 0 \text{ and } \operatorname{ord}_z(f) \neq \infty \}.
\]
\end{definition}


\begin{theorem}[divisor_support_locally_finite]
If $f$ is meromorphic on $U$, then the support of $\operatorname{div}_U(f)$ is locally finite in $U$.
\end{theorem}
\begin{proof}
Assume that $f$ is meromorphic on $U$.

Let $z_0 \in \mathbb K$. By the definition of meromorphicity, there exists a neighborhood $V$ of $z_0$ such that either:
\begin{itemize}
  \item $f$ has no zeros or poles in $V$, or
  \item $z_0$ is an isolated zero or pole of $f$.
\end{itemize}

Indeed, near any point $z_0 \in U$, there exists an integer $n$ and an analytic function $g$ with $g(z_0) \neq 0$ such that
\[
f(z) = (z - z_0)^n g(z)
\quad \text{for all } z \text{ in a punctured neighborhood of } z_0.
\]

Since zeros of analytic functions are isolated unless the function vanishes identically, it follows that:
\begin{itemize}
  \item the set of zeros of $f$ in $V$ is finite, and
  \item the set of poles of $f$ in $V$ is finite.
\end{itemize}

Therefore,
\[
V \cap \operatorname{supp}(\operatorname{div}_U(f))
\]
is finite.

Since $z_0$ was arbitrary, the support of $\operatorname{div}_U(f)$ is locally finite in $U$.
\end{proof}
