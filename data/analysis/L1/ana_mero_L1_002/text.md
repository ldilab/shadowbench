\begin{theorem}[min_divisor_le_divisor_add]
Let $f_1,f_2 : \mathbb K \to E$ be meromorphic on a set $U \subseteq \mathbb K$, and let $z \in U$. Assume that the order of $f_1+f_2$ at $z$ is finite.  Then
\[
\min\bigl(\operatorname{div}_U(f_1)(z),\operatorname{div}_U(f_2)(z)\bigr)
\;\le\;
\operatorname{div}_U(f_1+f_2)(z).
\]
\end{theorem}

\begin{proof}
We distinguish cases.

\medskip
\noindent\textbf{Case 1: $z \notin U$.}
By definition of the divisor, all divisor values at $z$ vanish:
\[
\operatorname{div}_U(f_1)(z)
=
\operatorname{div}_U(f_2)(z)
=
\operatorname{div}_U(f_1+f_2)(z)
=
0.
\]
Hence
\[
\min(0,0) \le 0,
\]
and the inequality holds.

\medskip
\noindent\textbf{Case 2: $z \in U$.}
Since $f_1$, $f_2$, and $f_1+f_2$ are meromorphic on $U$, their divisors at $z$ are given by their orders, with the convention that infinite order contributes zero:
\[
\operatorname{div}_U(f_i)(z)
=
\begin{cases}
\operatorname{ord}_z(f_i), & \text{if } \operatorname{ord}_z(f_i) \text{ is finite},\\
0, & \text{if } \operatorname{ord}_z(f_i)=\infty,
\end{cases}
\qquad (i=1,2),
\]
and similarly for $f_1+f_2$.

\medskip
\noindent\textbf{Case 2a: $\operatorname{ord}_z(f_1)=\infty$.}
Then $\operatorname{div}_U(f_1)(z)=0$, so
\[
\min\bigl(\operatorname{div}_U(f_1)(z),\operatorname{div}_U(f_2)(z)\bigr)=0
\le
\operatorname{div}_U(f_1+f_2)(z),
\]
and the claim follows.

\medskip
\noindent\textbf{Case 2b: $\operatorname{ord}_z(f_2)=\infty$.}
This is symmetric to the previous case and yields the same conclusion.

\medskip
\noindent\textbf{Case 2c: $\operatorname{ord}_z(f_1)$ and $\operatorname{ord}_z(f_2)$ are both finite.}
In this case, the divisor values coincide with the actual orders, and
\[
\min\bigl(\operatorname{div}_U(f_1)(z),\operatorname{div}_U(f_2)(z)\bigr)
=
\min\bigl(\operatorname{ord}_z(f_1),\operatorname{ord}_z(f_2)\bigr).
\]

Since $f_1$ and $f_2$ are meromorphic at $z$, the standard inequality for orders of sums gives
\[
\min\bigl(\operatorname{ord}_z(f_1),\operatorname{ord}_z(f_2)\bigr)
\;\le\;
\operatorname{ord}_z(f_1+f_2).
\]
By the assumption that $\operatorname{ord}_z(f_1+f_2)$ is finite, we have
\[
\operatorname{ord}_z(f_1+f_2)
=
\operatorname{div}_U(f_1+f_2)(z),
\]
and combining the inequalities yields the desired result.
\end{proof}
