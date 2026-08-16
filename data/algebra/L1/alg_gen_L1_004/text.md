\begin{theorem}[exists_vanishingIdeal_zeroLocus_not_mem_J]
Let $J=\langle x^2+y^2-1,\ y-1\rangle$. Find $f\in \mathbf I(\mathbf V(J))$ such that $f\notin J$.
\end{theorem}

\begin{proof}
Take \(f=x\). If \((a,b)\in \mathbf V(J)\), then \(b-1=0\) and
\(a^2+b^2-1=0\). Hence \(b=1\) and \(a^2=0\), so \(a=0\). Thus
\(\mathbf V(J)=\{(0,1)\}\), and since \(x(0,1)=0\), we have
\(x\in \mathbf I(\mathbf V(J))\).

It remains to show \(x\notin J\). Consider the specialization homomorphism
\(\varphi:\mathbb R[x,y]\to\mathbb R[x]\) given by \(\varphi(g)=g(x,1)\).
Then \(\varphi(y-1)=0\) and \(\varphi(x^2+y^2-1)=x^2\), so
\(\varphi(J)\subseteq \langle x^2\rangle\). If \(x\in J\), then
\(x=\varphi(x)\in\langle x^2\rangle\), impossible. Hence \(x\notin J\).
Therefore \(f=x\) satisfies \(f\in\mathbf I(\mathbf V(J))\) and \(f\notin J\).
\end{proof}
