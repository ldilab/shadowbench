\begin{theorem}[existsUnique_continuousMap_lifts_of_range_le]
Let \(p : E \to X\) be a covering map, let \(A\) be path connected and locally path connected, and let
\[
f : A \to X
\]
be continuous. Fix points \(a_0 \in A\) and \(e_0 \in E\) such that
\[
p(e_0)=f(a_0).
\]
Assume that
\[
f_*\bigl(\pi_1(A,a_0)\bigr)\subseteq p_*\bigl(\pi_1(E,e_0)\bigr)
\subseteq \pi_1(X,f(a_0)).
\]
Then there exists a unique continuous map
\[
F : A \to E
\]
such that
\[
F(a_0)=e_0
\qquad\text{and}\qquad
p\circ F=f.
\]
\end{theorem}

\begin{proof}
For each \(a \in A\), choose a path
\[
\gamma_a : I \to A
\]
from \(a_0\) to \(a\). Since
\[
(f\circ \gamma_a)(0)=f(a_0)=p(e_0),
\]
the path lifting property for covering maps gives a unique lift
\[
\widetilde{\gamma}_a : I \to E
\]
such that
\[
\widetilde{\gamma}_a(0)=e_0
\qquad\text{and}\qquad
p\circ \widetilde{\gamma}_a=f\circ \gamma_a.
\]
Define
\[
F(a):=\widetilde{\gamma}_a(1).
\]

We first show that \(F(a)\) is independent of the choice of \(\gamma_a\).

Let \(\gamma,\gamma' : I \to A\) be two paths from \(a_0\) to the same point \(a\), and let
\[
\widetilde{\gamma},\widetilde{\gamma}' : I \to E
\]
be the lifts of \(f\circ \gamma\) and \(f\circ \gamma'\) starting at \(e_0\). We must prove that
\[
\widetilde{\gamma}(1)=\widetilde{\gamma}'(1).
\]

Consider the loop at \(a_0\)
\[
\alpha:=\gamma\cdot \overline{\gamma'}.
\]
Then \(f\circ \alpha\) is a loop at \(f(a_0)\). Its homotopy class lies in
\[
f_*\bigl(\pi_1(A,a_0)\bigr),
\]
hence, by hypothesis, also in
\[
p_*\bigl(\pi_1(E,e_0)\bigr).
\]
Therefore there exists a loop
\[
\beta : I \to E
\]
based at \(e_0\) such that
\[
[p\circ \beta]=[f\circ \alpha]
\]
in \(\pi_1(X,f(a_0))\). So there exists a homotopy $h_t$ with $h_0 = f \circ \alpha$ and $h_1 = p \circ \beta$. By the covering homotopy property, we have a lifting $\widetilde{h}_t$ of $h_t$ which is a homotopy relative to endpoints such that $\widetilde{h}_0$ is the lift of $f \circ \alpha$ starting at $e_0$ and $\widetilde{h}_1 = \beta$ since $\beta$ is a lift of $p \circ \beta$ starting at $e_0$. As $\widetilde{h}_1$ is a loop at $e_0$, so is $\widetilde{h}_0$.

Let
\[
\widetilde{\alpha} := \widetilde{h}_0.
\]

By the uniqueness of the lifted paths, the first half of $\alpha$ is $\widetilde{\gamma}$ and the second half of $\alpha$ is $\overline{\widetilde{\gamma}'}$ so that the endpoints of $\widetilde{\gamma}$ and $\widetilde{\gamma}'$ coincide, and thus \(F(a)\) is well defined.

By construction,
\[
F(a_0)=e_0.
\]
Also, for every \(a\in A\),
\[
p(F(a))
=
p\bigl(\widetilde{\gamma}_a(1)\bigr)
=
(f\circ \gamma_a)(1)
=
f(a),
\]
so
\[
p\circ F=f.
\]

To prove that \(F\) is continuous, let \(U \subseteq X\) be an open neighborhood of \(f(a)\) having a lift \(\widetilde{U} \subseteq E\)  containing \(F(a)\) such that \(p : \widetilde{U} \to U\) is a homeomorphism. Choose a path-connected open neighborhood \(V\) of \(a\) with \(f(V) \subseteq U\). For paths from \(a_0\) to points \(a' \in V\) we can take a fixed path \(\gamma\) from \(a_0\) to \(a\) followed by paths \(\eta\) in \(V\) from \(a\) to the points \(a'\). Then the paths \((f \circ \gamma )\cdot (f \circ \eta)\) in \(X\) have lifts \((\widetilde{f \circ \gamma}) \cdot (\widetilde{f \circ \eta}) \) where \(\widetilde{(f \circ \eta)} = p^{-1}(f \circ \eta)\) and \(p^{-1} :U \to \widetilde{U}\) is the inverse of \(p:\widetilde{U} \to U\). Thus \(F(V) \subseteq \widetilde{U}\) and \(F|_V = p^{-1} \circ f\), hence \(F\) is continuous at \(a\).

Finally, \(F\) is unique. Indeed, suppose
\[
F' : A \to E
\]
is another continuous map such that
\[
F'(a_0)=e_0
\qquad\text{and}\qquad
p\circ F'=f.
\]
Let \(a\in A\), and let \(\gamma_a\) be any path from \(a_0\) to \(a\). Then
\[
F'\circ \gamma_a
\]
is a lift of \(f\circ \gamma_a\) starting at \(e_0\). By uniqueness of path lifting,
\[
F'\circ \gamma_a=\widetilde{\gamma}_a.
\]
Evaluating at \(1\), we get
\[
F'(a)=\widetilde{\gamma}_a(1)=F(a).
\]
Thus \(F'=F\).
\end{proof}
