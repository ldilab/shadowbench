\begin{theorem}[T_spectrum]
Consider the \textit{Volterra integral operator} $T : L^2([0, 1]) \to L^2([0, 1])$ defined by:
\begin{equation*}
    (Tf)(x) = \int_0^x f(y) \, dy, \quad x \in [0, 1]
\end{equation*}

\begin{enumerate}
    \item Prove that $T$ is a \textbf{compact operator}.
    \item Prove that the \textbf{spectrum} of $T$ consists of only the origin, i.e., $\sigma(T) = \{0\}$.
\end{enumerate}
\end{theorem}

\begin{proof}
\begin{enumerate}
\item \textbf{$T$ is compact.}

First, $T$ is bounded since
\[
\|Tf\|_{L^2}^2
=
\int_0^1 \left|\int_0^x f(y)\,dy\right|^2 dx
\le
\int_0^1 \|f\|_{L^1}^2\,dx
\le
\|f\|_{L^2}^2.
\]
Also, we may rewrite $T$ as
\[
(Tf)(x)=\int_0^1 k(x,y)f(y)\,dy,
\]
where
\[
k(x,y)=
\begin{cases}
1,& y\le x,\\
0,& y>x.
\end{cases}
\]
Since $k\in L^2([0,1]^2)$, $T$ is Hilbert--Schmidt, hence compact.

\item \textbf{$\sigma(T)=\{0\}$.}

Since $T$ is compact on the infinite-dimensional space $L^2([0,1])$, we know that
$0\in \sigma(T)$, and every nonzero spectral value is an eigenvalue.

Suppose $\lambda\ne 0$ and $\lambda\in \sigma(T)$. Then there exists $f\ne 0$ such that
\[
Tf=\lambda f,
\qquad\text{i.e.}\qquad
\int_0^x f(y)\,dy=\lambda f(x).
\]
Since $f\in L^1([0,1])$, by the fundamental theorem of calculus we may differentiate to obtain
\[
f(x)=\lambda f'(x),
\]
so
\[
f(x)=ce^{x/\lambda}.
\]
Putting $x=0$ into the integral equation gives
\[
0=\lambda f(0),
\]
hence $f(0)=0$, so $c=0$. This contradicts $f\ne 0$.

Therefore no $\lambda\ne 0$ belongs to $\sigma(T)$, and thus
\[
\sigma(T)=\{0\}.
\]
\end{enumerate}
\end{proof}
