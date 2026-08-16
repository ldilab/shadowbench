\begin{theorem}[existsUnique_continuousMap_lifts]
Let \(p:E\to X\) be a local homeomorphism. Let \(A\) be a path-connected and locally path-connected topological space. Let
\[
f:A\to X
\]
be a continuous map, and fix points \(a_0\in A\) and \(e_0\in E\) such that
\[
p(e_0)=f(a_0).
\]

Assume the following two conditions.

\begin{enumerate}
\item For every path \(\gamma:I\to A\) with \(\gamma(0)=a_0\), there exists a path \(\Gamma:I\to E\) such that
\[
\Gamma(0)=e_0
\qquad\text{and}\qquad
p\circ \Gamma = f\circ \gamma .
\]

\item Whenever \(\gamma,\gamma':I\to A\) are paths with
\[
\gamma(0)=\gamma'(0)=a_0,
\]
and \(\Gamma,\Gamma':I\to E\) are lifts satisfying
\[
\Gamma(0)=\Gamma'(0)=e_0,\qquad
p\circ\Gamma=f\circ\gamma,\qquad
p\circ\Gamma'=f\circ\gamma',
\]
then
\[
\gamma(1)=\gamma'(1)\quad\Longrightarrow\quad \Gamma(1)=\Gamma'(1).
\]
\end{enumerate}

Then there exists a unique continuous map
\[
F:A\to E
\]
such that
\[
F(a_0)=e_0
\qquad\text{and}\qquad
p\circ F=f.
\]
\end{theorem}

\begin{proof}
We first define \(F\) pointwise.

Since \(A\) is path-connected, for every \(a\in A\) there exists a path
\[
\gamma_a:I\to A
\]
from \(a_0\) to \(a\), meaning
\[
\gamma_a(0)=a_0,\qquad \gamma_a(1)=a.
\]
By assumption (1), there exists a lift
\[
\Gamma_a:I\to E
\]
such that
\[
\Gamma_a(0)=e_0,\qquad p\circ \Gamma_a=f\circ \gamma_a.
\]
Define
\[
F(a):=\Gamma_a(1).
\]

We must check that this does not depend on the choice of \(\gamma_a\) or of the lift \(\Gamma_a\). But this is exactly what assumption (2) gives: if \(\gamma_a,\gamma'_a\) are two paths from \(a_0\) to \(a\), and \(\Gamma_a,\Gamma'_a\) are lifts starting at \(e_0\), then since
\[
\gamma_a(1)=a=\gamma'_a(1),
\]
assumption (2) implies
\[
\Gamma_a(1)=\Gamma'_a(1).
\]
So \(F(a)\) is well defined.

Now for each \(a\in A\),
\[
p(F(a))=p(\Gamma_a(1))=f(\gamma_a(1))=f(a).
\]
Hence
\[
p\circ F=f.
\]
Also, taking the constant path at \(a_0\), the lifted path starts at \(e_0\), so
\[
F(a_0)=e_0.
\]

It remains to prove that \(F\) is continuous.

Fix a point \(a\in A\). Since \(p\) is a local homeomorphism, there exists an open neighborhood \(V\subseteq E\) of \(F(a)\) such that \(p|_V:V\to U\) is a homeomorphism onto an open set \(U\subseteq X\) containing
\[
p(F(a))=f(a).
\]

Since \(f\) is continuous, \(f^{-1}(U)\) is an open neighborhood of \(a\). Because \(A\) is locally path-connected, we may choose an open path-connected neighborhood
\[
W\subseteq f^{-1}(U)
\]
of \(a\).

We claim that on \(W\),
\[
F=(p|_V)^{-1}\circ f.
\]
This will prove continuity of \(F\) at \(a\), since the right-hand side is continuous.

Take any \(x\in W\). Because \(W\) is path-connected, choose a path
\[
\delta:I\to W
\]
from \(a\) to \(x\), so
\[
\delta(0)=a,\qquad \delta(1)=x.
\]
Also choose once and for all a path \(\gamma_a\) from \(a_0\) to \(a\), together with a lift \(\Gamma_a\) from \(e_0\) to \(F(a)\).

Now define a path in \(E\) by
\[
\widetilde\delta := (p|_V)^{-1}\circ f\circ \delta.
\]
This is well defined because \(f(\delta(t))\in U\) for all \(t\), since \(\delta(I)\subseteq W\subseteq f^{-1}(U)\). Moreover,
\[
\widetilde\delta(0)=(p|_V)^{-1}(f(a))=(p|_V)^{-1}(p(F(a)))=F(a),
\]
because \(F(a)\in V\).

Now concatenate \(\Gamma_a\) with \(\widetilde\delta\). This gives a path in \(E\) starting at \(e_0\), and its projection under \(p\) is exactly the concatenation of \(\gamma_a\) with \(\delta\), which is a path from \(a_0\) to \(x\).

By construction, the endpoint of this lifted concatenated path is
\[
\widetilde\delta(1)=(p|_V)^{-1}(f(x)).
\]
But by the definition of \(F(x)\) and the uniqueness of lifted endpoints in assumption (2), the endpoint of any lift of a path from \(a_0\) to \(x\) starting at \(e_0\) must be \(F(x)\). Therefore
\[
F(x)=(p|_V)^{-1}(f(x)).
\]
This proves the claim.

So around every point \(a\), the map \(F\) agrees locally with the continuous map \((p|_V)^{-1}\circ f\). Hence \(F\) is continuous on all of \(A\).

Finally, we prove uniqueness. Suppose
\[
F':A\to E
\]
is another continuous map such that
\[
F'(a_0)=e_0,\qquad p\circ F'=f.
\]
Let \(a\in A\), and choose any path \(\gamma:I\to A\) from \(a_0\) to \(a\). Then
\[
F'\circ \gamma:I\to E
\]
is a path satisfying
\[
(F'\circ \gamma)(0)=F'(a_0)=e_0
\]
and
\[
p\circ(F'\circ \gamma)=f\circ\gamma.
\]
Similarly,
\[
F\circ \gamma:I\to E
\]
is also a lift of \(f\circ \gamma\) starting at \(e_0\). Hence, by assumption (2),
\[
F'(a)=(F'\circ\gamma)(1)=(F\circ\gamma)(1)=F(a).
\]
Since this holds for every \(a\in A\), we get
\[
F'=F.
\]

Therefore there exists a unique continuous map \(F:A\to E\) such that
\[
F(a_0)=e_0
\qquad\text{and}\qquad
p\circ F=f.
\]
This completes the proof.
\end{proof}
