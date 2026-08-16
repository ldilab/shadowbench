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

\begin{theorem}[Skew Bollobás Inequality]
If \(\mathcal P=\{(A_i,B_i)\mid i\in[m]\}\) is a skew Bollobás system with
\(A_i,B_i\subseteq[n]\), then
\[
\sum_{i=1}^m
\frac{1}{(1+|A_i|+|B_i|)\binom{|A_i|+|B_i|}{|A_i|}}
\le 1.
\]
\end{theorem}
