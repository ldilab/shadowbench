
\begin{theorem}[monodromy_theorem]
Let $\gamma_0,\gamma_1:I\to X$ be paths and let $\gamma:I\times I\to X$ be a homotopy rel.\ endpoints
between them. Let $\Gamma:I\to C(I,E)$ be a family of continuous paths in $E$ such that
\[
p(\Gamma(t)(s))=\gamma(t,s)\quad \forall t,s\in I,
\qquad
\Gamma(t)(0)=\Gamma(0)(0)\quad \forall t\in I.
\]
Then $\Gamma(t)(1)=\Gamma(0)(1)$ for all $t\in I$.
\end{theorem}

\begin{proof}
Define $G:I\times I\to E$ by $G(s,t)=\Gamma(t)(s)$. Then for each fixed $t$, the map $s\mapsto G(s,t)$
is continuous, and by hypothesis the map $t\mapsto G(0,t)$ is constant, hence continuous. Moreover
\[
p(G(s,t))=p(\Gamma(t)(s))=\gamma(t,s)= (\gamma\circ\mathrm{swap})(s,t).
\]
By Theorem B, $G$ is continuous.
Now consider the path $t\mapsto G(1,t)$ in $E$. Its projection is
$t\mapsto p(G(1,t))=\gamma(t,1)$, which is constant in $t$ because $\gamma$ is a homotopy rel.\ endpoints.
Since $p$ is separated and $G(0,t)$ is constant, uniqueness of lifts forces $G(1,t)$ to be constant.
Thus $G(1,t)=G(1,0)$ for all $t$, i.e.\ $\Gamma(t)(1)=\Gamma(0)(1)$.
\end{proof}
