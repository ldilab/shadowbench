\begin{theorem}[weyl_von_neumann]
Let \(H\) be a separable Hilbert space and let \(A=A^*\in\mathcal B(H)\).
Then for every \(\varepsilon>0\), there exist a diagonal self-adjoint operator
\(D\) and a compact self-adjoint operator \(K\) such that
\[
A=D+K,
\qquad
\|K\|<\varepsilon.
\]
\end{theorem}
\begin{proof}
In this proof, we use three lemmas: approximate Spectral localization, compact-tail criterion, and diagonalization lemma. We present the three lemmas, and begin the proof. 



\begin{lemma}[ABM_analysis_L3_ana_gen_L2_006_item_2]
Let \(A=A^*\in\mathcal B(H)\), and let \(E\) be its spectral measure.
If \(I\subset\mathbb R\) is an interval and \(x\in E(I)H\), then for every
\(\lambda_I\in I\),
\[
\|(A-\lambda_I I_H)x\|
\le |I|\,\|x\|.
\]
\end{lemma}



\begin{lemma}[ABM_analysis_L3_ana_gen_L2_006_item_3]
Let \((e_n)_{n=1}^\infty\) be an orthonormal basis of \(H\). Suppose
\(K\in\mathcal B(H)\) satisfies
\[
\|K e_n\|\to 0.
\]
Then \(K\) is compact.
\end{lemma}



\begin{lemma}[weyl_von_neumann_lemma]
Let \(A=A^*\in\mathcal B(H)\), where \(H\) is separable. Then for every
\(\varepsilon>0\), there exist an orthonormal basis \((e_n)\) of \(H\) and
scalars \(\lambda_n\in\mathbb R\) such that
\[
\|(A-\lambda_n I_H)e_n\|<\varepsilon
\quad\text{for all }n,
\]
and
\[
\|(A-\lambda_n I_H)e_n\|\to 0.
\]
\end{lemma}

Now, we begin the proof. 

By the approximate diagonalization lemma, there exist an orthonormal basis
\((e_n)\) of \(H\) and scalars \(\lambda_n\in\mathbb R\) such that
\[
\|(A-\lambda_n I_H)e_n\|<\varepsilon
\]
for every \(n\), and
\[
\|(A-\lambda_n I_H)e_n\|\to 0.
\]

Define \(D\) by
\[
De_n=\lambda_n e_n.
\]
Then \(D\) is diagonal and self-adjoint. Set
\[
K:=A-D.
\]
Then
\[
Ke_n=Ae_n-\lambda_n e_n,
\]
so
\[
\|Ke_n\|<\varepsilon
\quad\text{for all }n,
\qquad
\|Ke_n\|\to 0.
\]

Hence
\[
\|K\|\le \varepsilon,
\]
and by the compact-tail criterion, \(K\) is compact. Replacing \(\varepsilon\)
by \(\varepsilon/2\) gives \(\|K\|<\varepsilon\).

Therefore
\[
A=D+K,
\]
where \(D\) is diagonal self-adjoint and \(K\) is compact self-adjoint.
\end{proof}
