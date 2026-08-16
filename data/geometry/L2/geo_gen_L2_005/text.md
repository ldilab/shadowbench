\begin{theorem}[proj_homotopyEquiv]
Let $E$ be a real vector bundle over a topological space $M$. 
Show that the projection map $\pi : E \to M$ is a homotopy equivalence.
\end{theorem}

\begin{proof}
Let $\sigma \colon M \to E$ be the zero section, defined by
\[
\sigma(p)=0_p \in E_p .
\]
Then $\pi \circ \sigma = \operatorname{id}_M$, because the zero vector $0_p$ lies in the fiber $E_p$.

It remains to show that $\sigma \circ \pi$ is homotopic to $\operatorname{id}_E$.
Define
\[
H \colon E \times [0,1] \to E
\]
by
\[
H(v,t)=t\,v ,
\]
where $v \in E_p$ for some $p \in M$, and $t\,v$ denotes scalar multiplication in the fiber $E_p$.
Moreover, $H$ is continuous since scalar multiplication is continuous in each local trivialization of the vector bundle.

Now evaluate $H$ at the endpoints:
\[
H(v,1)=1\cdot v=v,
\]
so $H_1=\operatorname{id}_E$, and
\[
H(v,0)=0\cdot v=0_p=\sigma(\pi(v)),
\]
so $H_0=\sigma\circ\pi$.

Thus $H$ is a homotopy from $\sigma\circ\pi$ to $\operatorname{id}_E$.
Therefore $\pi$ has a homotopy inverse $\sigma$, and hence $\pi \colon E \to M$ is a homotopy equivalence.
\end{proof}
