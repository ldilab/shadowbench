\begin{theorem}[ContinuousOn.absolutelyContinuousOnInterval_and_sub_eq_integral_deriv]
Suppose that $F$ is continuous on $[a,b]$, $F'(x)$ exists for every $x \in (a,b)$, and $F'(x)$ is integrable. Then $F$ is absolutely continuous and
\[
F(b) - F(a) = \int_a^b F'(x)\,dx.
\]
\end{theorem}

\begin{proof}
Let
\[
  G(x) := F(a) + \int_a^x F'(t)\,dt .
\]
Then $F$ agrees with $G$ on $[a,b]$.  
Since $F'$ is integrable on $[a,b]$, the function
\[
  x\mapsto \int_a^x F'(t)\,dt
\]
is absolutely continuous on $[a,b]$. The constant function
$x\mapsto F(a)$ is also absolutely continuous on $[a,b]$. Hence their sum
$G$ is absolutely continuous on $[a,b]$.
Because $F=G$ on $[a,b]$, it follows that $F$ itself is absolutely
continuous on $[a,b]$.

Finally, applying the fundamental theorem of calculus on the whole interval
$[a,b]$, using the continuity of $F$ on $[a,b]$, differentiability on
$(a,b)$, and integrability of $F'$, we obtain
\[
  \int_a^b F'(t)\,dt = F(b)-F(a).
\]
Equivalently,
\[
  F(b)-F(a)=\int_a^b F'(t)\,dt .
\]
Thus
\[
  F \text{ is absolutely continuous on } [a,b]
  \quad\text{and}\quad
  F(b)-F(a)=\int_a^b F'(t)\,dt .
\]
\end{proof}
