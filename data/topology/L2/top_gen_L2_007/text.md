\begin{lemma}[liftPath_zero]
Let
\[
p:E\to X
\]
be a covering map. Let
\[
\gamma:I\to X
\]
be a path, and let \(e\in E\) be such that
\[
\gamma(0)=p(e).
\]
Then there exists a path
\[
\Gamma:I\to E
\]
such that
\[
p\circ \Gamma=\gamma
\qquad\text{and}\qquad
\Gamma(0)=e.
\]
\end{lemma}

\begin{proof}
Since \(p\) is a covering map, every point \(x\in X\) has an evenly covered open neighborhood \(U_x\). The image \(\gamma(I)\) is compact, so finitely many such neighborhoods cover it. By subdividing the interval \(I=[0,1]\), we may choose numbers
\[
0=t_0\le t_1\le \cdots \le t_n=1
\]
such that for each \(i\), the image of \(\gamma\) on \([t_i,t_{i+1}]\) is contained in some evenly covered open set \(U_i\).

We construct the lift \(\Gamma\) inductively. At \(t=0\), we require
\[
\Gamma(0)=e.
\]
Since \(p(e)=\gamma(0)\in U_0\), there is a unique sheet of \(p^{-1}(U_0)\) containing \(e\), and the restriction of \(p\) to that sheet is a homeomorphism onto \(U_0\). Hence \(\gamma|_{[t_0,t_1]}\) has a unique lift on \([t_0,t_1]\) starting at \(e\).

Now suppose \(\Gamma\) has been defined continuously on \([0,t_i]\). Then the point \(\Gamma(t_i)\) lies above \(\gamma(t_i)\). Since \(\gamma([t_i,t_{i+1}])\subseteq U_i\), there is again a unique sheet over \(U_i\) containing \(\Gamma(t_i)\), and by inverting the homeomorphism on that sheet we obtain a unique continuation of \(\Gamma\) over \([t_i,t_{i+1}]\).

Proceeding inductively over all subintervals, we obtain a continuous path
\[
\Gamma:I\to E
\]
such that
\[
p\circ \Gamma=\gamma
\qquad\text{and}\qquad
\Gamma(0)=e.
\]
\end{proof}


\begin{lemma}[eq_liftPath_iff]
Let
\[
f:E\to X
\]
be a covering map, and let \(A\) be a preconnected topological space. Suppose
\[
g_1,g_2:A\to E
\]
are continuous maps such that
\[
f\circ g_1=f\circ g_2.
\]
If there exists a point \(a\in A\) such that
\[
g_1(a)=g_2(a),
\]
then
\[
g_1=g_2.
\]
\end{lemma}

\begin{proof}
Let
\[
S=\{x\in A \mid g_1(x)=g_2(x)\}.
\]
We will show that \(S\) is both open and closed in \(A\). Since \(a\in S\), the set \(S\) is nonempty. Because \(A\) is preconnected, it will follow that \(S=A\), hence \(g_1=g_2\).

First we show that \(S\) is open. Let \(x\in S\). Set
\[
e:=g_1(x)=g_2(x).
\]
Since \(f\) is a covering map, there exists an evenly covered open neighborhood \(U\subseteq X\) of \(f(e)\). Let \(V\) be the sheet of \(f^{-1}(U)\) containing \(e\). Then
\[
f|_V:V\to U
\]
is a homeomorphism.

Since \(g_1\) and \(g_2\) are continuous and \(g_1(x),g_2(x)\in V\), after shrinking to an open neighborhood \(W\) of \(x\) in \(A\), we may assume that
\[
g_1(W)\subseteq V
\qquad\text{and}\qquad
g_2(W)\subseteq V.
\]
For every \(y\in W\), we have
\[
f(g_1(y))=f(g_2(y)).
\]
Since \(f|_V\) is injective, it follows that
\[
g_1(y)=g_2(y).
\]
Thus \(W\subseteq S\), so \(S\) is open.

Next we show that \(S\) is closed. Let \(x\in \overline{S}\). We again choose an evenly covered neighborhood \(U\subseteq X\) of \(f(g_1(x))=f(g_2(x))\), and let \(V_1,V_2\) be the sheets containing \(g_1(x)\) and \(g_2(x)\), respectively. By continuity, after shrinking to some open neighborhood \(W\) of \(x\), we may assume that
\[
g_1(W)\subseteq V_1
\qquad\text{and}\qquad
g_2(W)\subseteq V_2.
\]
Since \(x\in \overline{S}\), the set \(W\cap S\) is nonempty. Choose \(y\in W\cap S\). Then
\[
g_1(y)=g_2(y).
\]
But \(g_1(y)\in V_1\) and \(g_2(y)\in V_2\), and distinct sheets over \(U\) are disjoint. Therefore
\[
V_1=V_2.
\]
Hence both \(g_1\) and \(g_2\) map \(W\) into the same sheet \(V_1\), and since
\[
f\circ g_1=f\circ g_2
\]
and \(f|_{V_1}\) is injective, we get
\[
g_1|_W=g_2|_W.
\]
In particular, \(g_1(x)=g_2(x)\), so \(x\in S\). Therefore \(S\) is closed.

We have shown that \(S\) is a nonempty clopen subset of the preconnected space \(A\). Hence \(S=A\), and therefore \(g_1=g_2\).
\end{proof}

\begin{lemma}[eq_liftPath_iff']
Let
\[
p:E\to X
\]
be a covering map, let
\[
\gamma:I\to X
\]
be a path, and let \(e\in E\) satisfy
\[
\gamma(0)=p(e).
\]
Let
\[
\widetilde{\gamma}:I\to E
\]
be the chosen lift of \(\gamma\) starting at \(e\), so that
\[
p\circ \widetilde{\gamma}=\gamma
\qquad\text{and}\qquad
\widetilde{\gamma}(0)=e.
\]

Then for any map \(\Gamma:I\to E\),
\[
\Gamma=\widetilde{\gamma}
\]
if and only if
\[
\Gamma \text{ is continuous},\qquad p\circ \Gamma=\gamma,\qquad \Gamma(0)=e.
\]
\end{lemma}

\begin{proof}
If \(\Gamma=\widetilde{\gamma}\), then \(\Gamma\) is continuous, since \(\widetilde{\gamma}\) is a path, and it satisfies
\[
p\circ \Gamma = p\circ \widetilde{\gamma}=\gamma
\]
and
\[
\Gamma(0)=\widetilde{\gamma}(0)=e.
\]

Conversely, suppose \(\Gamma:I\to E\) is continuous and satisfies
\[
p\circ \Gamma=\gamma
\qquad\text{and}\qquad
\Gamma(0)=e.
\]
Then both \(\Gamma\) and \(\widetilde{\gamma}\) are lifts of the same path \(\gamma\), and they agree at the point \(0\in I\). Since \(p\) is a covering map and \(I\) is connected, the uniqueness of lifts (the Lemma above) implies that
\[
\Gamma=\widetilde{\gamma}.
\]
\end{proof}
