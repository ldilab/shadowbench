\begin{theorem}[toΓSpec] Let $X$ be a scheme. There is a  canonical morphism $\varphi : X \to \mathrm{Spec}\Gamma(X)$ from $X$ to the spectrum of its global sections  where the underlying continuous map is given by sending a point $x \in X$ to the prime ideal $p$ of global sections that do not map to units in the stalk of the structure sheaf at $x$. 
\end{theorem}
\begin{proof}
  Let $x \in X$ and $U$ be an affine open neighborhood of $x$. Consider the ring homomorphism $\Gamma(X) \to \Gamma(U) \to \mathcal O_{X,x}$ given by restriction and taking germs at $x$.
  Let \[
p
\;=\;
\{\, s \in \Gamma(X) \mid s_x \text{ is not a unit in } \mathcal O_{X,x} \,\}.
\]
 We need to show that the induced map $\varphi^\sharp_x : (\Gamma(X) - p)^{-1} \Gamma(X) \to \mathcal O_{X,x}$ is local. Let $ t \in (\Gamma(X) - p)^{-1} \Gamma(X)$ which can be written as $r/s$ for some $s \not\in p$. We claim that $t \in  (\Gamma(X) - p)^{-1}p$ if and only if its germ $t_x$ is not a unit in $\mathcal O_{X,x}$. If $t \in  (\Gamma(X) - p)^{-1}p$, then $r \in p$ and $r_x$ is not a unit hence $t_x$ is not a unit in $\mathcal O_{X,x}$. Conversely, if $t_x$ is not a unit in $\mathcal O_{X,x}$, then $r_x$ is not a unit in $\mathcal O_{X,x}$ and hence $r \in p$ by definition.


\end{definition}
