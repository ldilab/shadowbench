\begin{theorem}[isGCD_iff_span_least_principal]
Given polynomials $f,g,h$ in $k[x_1,\dots,x_n]$, where
$h=\gcd(f,g)$ means that $h$ divides both $f$ and $g$ and is divisible by every common divisor of
$f$ and $g$, prove that $h=\gcd(f,g)$ if and only if $\langle h\rangle$ is the smallest
principal ideal containing $\langle f,g\rangle$.
\end{theorem}

\begin{proof}
Suppose \(h=\gcd(f,g)\). Then \(\langle f,g\rangle\subseteq \langle h\rangle\).
If \(J=\langle q\rangle\) is a principal ideal containing \(\langle f,g\rangle\), then
\(q\mid f\) and \(q\mid g\). Hence \(q\mid h\), and therefore
\(\langle h\rangle\subseteq \langle q\rangle=J\). Thus \(\langle h\rangle\) is the
smallest principal ideal containing \(\langle f,g\rangle\).

Conversely, suppose that \(\langle h\rangle\) is the smallest principal ideal
containing \(\langle f,g\rangle\). Then \(h\mid f\) and \(h\mid g\). If \(q\) is
any common divisor of \(f\) and \(g\), then
\(\langle f,g\rangle\subseteq \langle q\rangle\). By minimality,
\(\langle h\rangle\subseteq \langle q\rangle\), so \(q\mid h\). Therefore
\(h=\gcd(f,g)\), up to multiplication by a unit.
\end{proof}
