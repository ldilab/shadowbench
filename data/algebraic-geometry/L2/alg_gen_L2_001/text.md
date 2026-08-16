\begin{lemma}[smooth_of_grpObj_of_isAlgClosed]
If $G$ is a group scheme over an algebraically closed field $k$ that is reduced and locally of finite type, then $G$ is smooth over $k$.
\end{lemma}

\begin{proof}
Let \(U \subseteq G\) be the smooth locus of \(f\). Since smoothness is an open condition for morphisms locally of finite presentation, \(U\) is an open subset of \(G\). We must show that \(U=G\).

Suppose for contradiction that \(U \neq G\). Then \(G \setminus U\) is a nonempty closed subset of \(G\).

Because \(f\) is locally of finite presentation over the field \(k\), the scheme \(G\) is Jacobson. On the other hand, since \(k\) is algebraically closed, hence perfect, and \(G\) is reduced, the smooth locus \(U\) is dense in \(G\). Therefore both \(G \setminus U\) and \(U\) contain closed points. Choose closed points
\[
x \in G \setminus U
\qquad\text{and}\qquad
y \in U.
\]

Since \(k\) is algebraically closed, every closed point of \(G\) is a \(k\)-rational point. Thus \(x\) and \(y\) arise from morphisms
\[
x,y : \mathrm{Spec} k \to G
\]
over \(\mathrm{Spec} k\).

Now use the group structure on \(G\). For every \(k\)-point \(a : \mathrm{Spec} K \to G\), right translation by \(a'\) defines an automorphism of the group scheme \(G\) over \(\mathrm{Spec} k\). In particular, right translation by \(x\) and by \(y\) are automorphisms of \(G\), so
\[
\alpha := R_{y} \circ R_{x}^{-1}
\]
is an automorphism of \(G\) over \(\mathrm{Spec} k\). By construction, \(\alpha\) sends \(x\) to \(y\); hence, on underlying topological points,
\[
\alpha(x)=y.
\]

Because \(\alpha\) is an isomorphism over \(\mathrm{Spec} k\), it preserves the smooth locus:
\[
\alpha^{-1}(U)=U.
\]
Since \(y\in U\), it follows that \(x \in U\), contradicting the choice of \(x \in G \setminus U\).

This contradiction shows that \(G \setminus U\) is empty. Therefore \(U=G\), so \(f\) is smooth.
\end{proof}
