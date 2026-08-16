\begin{lemma}[contract_closure_eq_contract_delete]
For any \(C\subseteq E(M)\),
\[
M/\mathrm{cl}_M(C)= (M/C)\setminus\bigl(\mathrm{cl}_M(C)\setminus C\bigr).
\]
\end{lemma}
\begin{proof}
Reduce to the case \(C\subseteq E(M)\). Choose a basis \(I\) of \(C\).
Then \(\mathrm{cl}_M(C)=\mathrm{cl}_M(I)\), and contracting \(\mathrm{cl}_M(I)\) can be expressed as
contracting \(I\) and deleting the remaining elements \(\mathrm{cl}_M(I)\setminus I\).
Rearranging with associativity/commutativity of contraction/deletion gives the displayed equality.
\end{proof}

\begin{lemma}[contract_closure_eq]
For any sets \(C,X\),
\[
\mathrm{cl}_{M/C}(X)=\mathrm{cl}_M(X\cup C)\setminus C.
\]
\end{lemma}
\begin{proof}
Using the loop description \(\mathrm{loops}(M/C)=\mathrm{cl}_M(C)\setminus C\) and the fact that
closure can be characterized via loops after contracting, one shows both inclusions:
elements in \(\mathrm{cl}_{M/C}(X)\) correspond exactly to elements in \(\mathrm{cl}_M(X\cup C)\)
that are not in \(C\). A straightforward manipulation of closure axioms completes the proof.
\end{proof}

\begin{lemma}[contract_spanning_iff]
Assume \(C\subseteq E(M)\). Then
\[
X \text{ is spanning in } M/C
\;\Longleftrightarrow\;
\bigl(X\cup C \text{ is spanning in } M\bigr)\ \wedge\ \mathrm{Disjoint}(X,C).
\]
\end{lemma}
\begin{proof}
By definition, \(X\) is spanning in \(N\) iff \(\mathrm{cl}_N(X)=E(N)\).
Apply the closure formula \(\mathrm{cl}_{M/C}(X)=\mathrm{cl}_M(X\cup C)\setminus C\) and the ground-set
formula \(E(M/C)=E(M)\setminus C\), and rewrite equality of set-differences as spanning of \(X\cup C\)
together with \(X\cap C=\varnothing\).
\end{proof}
