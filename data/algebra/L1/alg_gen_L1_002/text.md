\begin{theorem}[exists_nonzero_remainder_of_lt_span_leadingTerms]
Suppose that $I=\langle f_1,\dots,f_s\rangle$ is an ideal such that $\langle \operatorname{LT}(f_1),\dots,\operatorname{LT}(f_s)\rangle$ is strictly smaller than $\langle \operatorname{LT}(I)\rangle$.
\begin{enumerate}
\item[(a)] Prove that there is some $f\in I$ whose remainder on division by $f_1,\dots,f_s$ is nonzero.
\end{enumerate}
\end{theorem}

\begin{proof}
Since
\[
  \langle \operatorname{LT}(f_1),\ldots,\operatorname{LT}(f_s)\rangle
  \subsetneq
  \langle \operatorname{LT}(I)\rangle,
\]
there exists an element \(f\in I\) such that
\[
  \operatorname{LT}(f)\notin
  \langle \operatorname{LT}(f_1),\ldots,\operatorname{LT}(f_s)\rangle .
\]
Divide \(f\) by \(B=\{f_1,\ldots,f_s\}\). By the division algorithm, we get
\[
  f=\sum_{i=1}^s q_i f_i+r,
\]
where \(r\) is the remainder, and no term of \(r\) is divisible by any
\(\operatorname{LT}(f_i)\).

Suppose, for contradiction, that \(r=0\). Then
\[
  f=\sum_{i=1}^s q_i f_i.
\]
By the division algorithm, every nonzero term \(q_i f_i\) has leading term no larger
than \(\operatorname{LT}(f)\). Hence the leading term of \(f\) must be divisible by
one of the \(\operatorname{LT}(f_i)\). Therefore
\[
  \operatorname{LT}(f)\in
  \langle \operatorname{LT}(f_1),\ldots,\operatorname{LT}(f_s)\rangle,
\]
contradicting the choice of \(f\).

Thus \(r\neq 0\). Hence there exists \(f\in I\) whose remainder on division by
\(B\) is nonzero.
\end{proof}
