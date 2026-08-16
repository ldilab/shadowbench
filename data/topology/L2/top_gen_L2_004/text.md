\begin{theorem}[exists_lift_nhds] Let \(p : E \to X\) be a local homeomorphism. Denote the unit interval \([0,1]\) by \(I\). Suppose \(f:I \times A \to X\) is a continuous map and \(g : I \times A \to E\) is a lift of \(f\) continuous on \(\{0\} \times A \cup I \times \{a\}\) for some $a \in A$. Then there exists a neighborhood \(N\) of \(a\) and \(g':I \times A \to E\) continuous on \(I \times N\) that agrees with \(g\) on \(\{0\} \times A \cup I \times \{a\} \).
\end{theorem}
\begin{proof}
For each \(e \in E\), choose a local homeomorphism \(q_e:U_e \to V_e \subseteq X\) from an open neighborhood \(U_e\) of \(e\) such that \(q_e = p|_{U_e}\).

Using the continuity of the map \(t \mapsto g(t,a)\), we cover $I$ by the open sets $g(\cdot,a)^{-1}(U_e)$, and by the compactness of $I$, we may choose a monotone subdivision
\[
0=t_0 \le t_1 \le \cdots \le t_{n_{\max}} = 1
\]
such that for every \(n\), there exists some \(e \in E\) such that
\[
g\bigl([t_n,t_{n+1}] \times \{a\}\bigr) \subseteq U_e.
\]

We claim that for every \(n\), there exist an open set \(N \subseteq A\) with $a \in N$, and a map
\[
g' : I \times A \to E
\]
such that:
\begin{enumerate}
  \item \(g'\) is continuous on \([0,t_n]\times N\);
  \item \(p \circ g' = f\) on all of \(I \times A\);
  \item \(g'(0,a') = g(0,a')\) for all \(a' \in A\);
  \item for every \(t' \le t_n\), one has
  \[
  g'(t',a)=g(t',a).
  \]
\end{enumerate}

Once this is proved, we apply it with \(n=n_{\max}\). Since \(t_{n_{\max}}=1\), the continuity statement becomes continuity on
\[
[0,1]\times N = I\times N,
\]
and the last condition becomes \(g'(t,a)=g(t,a)\) for every \(t\in I\). This gives the theorem.

We now prove the claim by induction on \(n\).

\noindent\textbf{Base case \(n=0\).}
Take
\[
N=A,\qquad g'=g.
\]
Then \(a \in A\), and \(A\) is open in itself. Also \(p\circ g'=f\) by hypothesis, and clearly
\[
g'(0,a')=g(0,a') \quad\text{for all } a',
\]
and
\[
g'(t',a)=g(t',a)
\]
for every \(t'\le t_0\).

It remains to prove continuity of \(g'\) on \([0,t_0]\times A\). Since \(t_0=0\), this set is just \(\{0\}\times A\) and the map \(g'=g\) is continuous on this set by assumption.

\noindent\textbf{Inductive step.}
Assume the statement holds for some \(n\), with corresponding open neighborhood \(N\) of \(a\) and a map \(g':I \times A \to E\).

By construction of the subdivision, choose \(e \in E\) such that
\[
g\bigl([t_n,t_{n+1}] \times \{a\}\bigr) \subseteq U_e.
\]
Since \(p\circ g=f\) and \(q_e=p\) on \(U_e\), it follows that
\[
[t_n,t_{n+1}] \times \{a\} \subseteq f^{-1}(V_e).
\]

Now \(V_e\) is open, and \([t_n,t_{n+1}]\) is compact. By the generalized tube lemma, there exist open sets \(u \subseteq I\) and \(v \subseteq A\) such that
\[
[t_n,t_{n+1}] \subseteq u,\qquad a \in v,
\qquad\text{and}\qquad
u \times v \subseteq f^{-1}(V_e).
\]
In particular,
\[
f\bigl([t_n,t_{n+1}] \times v\bigr) \subseteq V_e.
\]

We now define
\[
N_{n+1}
:=
v \cap N \cap \{\,a' \in A : g'(t_n,a') \in U_e\,\}.
\]
This set is open, since \(v\) and \(N\) are open and \(a' \mapsto g'(t_n,a')\) is continuous on \(N\).
Also \(a \in N_{n+1}\). Indeed, \(a\in v\), \(a\in N\) by the induction hypothesis, and
\[
g'(t_n,a)=g(t_n,a)\in U_e,
\]
because \(g'(t_n,a)=g(t_n,a)\) by the induction hypothesis and
\[
g\bigl([t_n,t_{n+1}] \times \{a\}\bigr)\subseteq U_e.
\]

Define a new map
\[
g_{n+1}' : I \times A \to E
\]
by
\[
g_{n+1}'(t,a')=
\begin{cases}
g'(t,a') & \text{if } t \le t_n,\\
q_e^{-1}(f(t,a')) & \text{if } t>t_n \text{ and } f(t,a') \in V_e,\\
g(t,a') & \text{otherwise.}
\end{cases}
\]

We verify that \(N_{n+1}\) and \(g_{n+1}'\) satisfy the required properties.

\medskip

\noindent\emph{Continuity on \([0,t_{n+1}] \times N_{n+1}\).}
On the closed subset \(\{(t,a'):t \le t_n, a' \in N_{n+1}\}\), the map \(g_{n+1}'\) agrees with \(g'\), hence is continuous there by the induction hypothesis.

On the subset \(\{(t,a'):t>t_n,a' \in N_{n+1}\}\), \(a' \in N_{n+1}\subseteq v\), and \(t \in [0,t_{n+1}]\), we have \(t \in u\) whenever \(t\ge t_n\), hence
\[
f(t,a') \in V_e.
\]
Therefore on this region
\[
g_{n+1}'(t,a') = q_e^{-1}(f(t,a')),
\]
which is continuous.

It remains to check agreement on the frontier \(t=t_n\). Let \((t_n,a') \in [0,t_{n+1}] \times N_{n+1}\). Since \(a' \in N_{n+1}\), we know
\[
g'(t_n,a') \in U_e.
\]
Also \(f(t_n,a') \in V_e\). Now
\[
q_e(g'(t_n,a')) = p(g'(t_n,a')) = f(t_n,a'),
\]
because \(p\circ g'=f\). Hence
\[
g'(t_n,a') = q_e^{-1}(f(t_n,a')),
\]
by injectivity of \(q_e\) on its source. So the two definitions agree on the frontier, and therefore \(g_{n+1}'\) is continuous on \([0,t_{n+1}] \times N_{n+1}\).

\medskip

\noindent\emph{Lift property.}
We show
\[
p \circ g_{n+1}' = f.
\]
If \(t \le t_n\), then \(g_{n+1}'=g'\), so this follows from the induction hypothesis. If \(t>t_n\) and \(f(t,a')\in V_e\), then
\[
g_{n+1}'(t,a') = q_e^{-1}(f(t,a')),
\]
hence
\[
p(g_{n+1}'(t,a')) = q_e(q_e^{-1}(f(t,a'))) = f(t,a').
\]
Otherwise \(g_{n+1}'=g\), and \(p\circ g=f\) by hypothesis.

\medskip

\noindent\emph{Agreement on \(\{0\}\times A\).}
Since \(0 \le t_n\), the first branch applies, so
\[
g_{n+1}'(0,a') = g'(0,a') = g(0,a')
\]
for all \(a' \in A\).

\medskip

\noindent\emph{Agreement on \(I\times\{a\}\) up to \(t_{n+1}\).}
Let \(t' \le t_{n+1}\). We must show
\[
g_{n+1}'(t',a)=g(t',a).
\]
There are three cases.

If \(t' \le t_n\), then
\[
g_{n+1}'(t',a)=g'(t',a)=g(t',a)
\]
by the induction hypothesis.

If \(t'>t_n\) and \(f(t',a)\in V_e\), then
\[
g_{n+1}'(t',a)=q_e^{-1}(f(t',a)).
\]
But also \(g(t',a)\in U_e\), because
\[
g\bigl([t_n,t_{n+1}] \times \{a\}\bigr)\subseteq U_e,
\]
and
\[
q_e(g(t',a)) = p(g(t',a)) = f(t',a).
\]
Hence by injectivity of \(q_e\),
\[
g'_{n+1}(t',a)=q_e^{-1}(f(t',a))=g(t',a).
\]

Finally, if \(t'>t_n\) and \(f(t',a)\notin V_e\), then by definition
\[
g_{n+1}'(t',a)=g(t',a).
\]

Thus all required properties hold for \(n+1\). This completes the induction.

Applying the result to \(n_{\max}\), we obtain an open neighborhood \(N\) of \(a\) and a map
\[
g' : I \times A \to E
\]
such that \(g'\) is continuous on \(I\times N\), satisfies \(p\circ g'=f\), agrees with \(g\) on \(\{0\}\times A \cup I\times\{a\}\). This is exactly the desired conclusion.
\end{proof}
