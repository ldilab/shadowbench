For a nonnegative integer \(q\), write \([q]=\{1,\ldots,q\}\), with \([0]=\varnothing\).
A family of ordered pairs
\[
\mathcal P=\{(A_i,B_i)\mid i\in[m]\},\qquad A_i,B_i\subseteq[n],
\]
is a \emph{skew Bollobás system} if
\[
A_i\cap B_i=\varnothing\quad\text{for every }i\in[m],
\]
and
\[
A_i\cap B_j\ne\varnothing\quad\text{whenever }i<j.
\]

\begin{theorem}[Partitioned Skew Bollobás Inequality]
Let \(r\ge 1\), and suppose that \(X=[n]\) is the disjoint union of
\(X_1,\ldots,X_r\), where \(|X_k|=n_k\). If
\(\mathcal P=\{(A_i,B_i)\mid i\in[m]\}\) is a skew Bollobás system with
\(A_i,B_i\subseteq X\), then
\[
\sum_{i=1}^m
\left(
\prod_{k=1}^r
\binom{|A_i\cap X_k|+|B_i\cap X_k|}{|A_i\cap X_k|}
\right)^{-1}
\le
\prod_{k=1}^r(1+n_k)
\le
\left(1+\frac nr\right)^r.
\]
\end{theorem}
