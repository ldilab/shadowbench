\begin{definition}[IsMinor]
A matroid $N$ is a \emph{minor} of a matroid $M$ if there exist subsets
$C,D\subseteq \alpha$ such that
\[
N = M / C \setminus D.
\]
We write $N \le_m M$ to denote that $N$ is a minor of $M$.
\end{definition}

\begin{definition}[IsStrictMinor]
A matroid $N$ is a \emph{strict minor} of $M$ if $N$ is a minor of $M$ but $M$
is not a minor of $N$.
We write $N <_m M$.
\end{definition}

\begin{lemma}[IsMinor.exists_eq_contract_delete_disjoint]\label{lem:disjoint-contract-delete}
If $N \le_m M$, then there exist subsets $C,D\subseteq E(M)$ such that
\[
C\cap D=\varnothing
\qquad\text{and}\qquad
N = M / C \setminus D.
\]
\end{lemma}

\begin{proof}
Assume $N \le_m M$. By definition, there exist $C_0,D_0\subseteq \alpha$ with
\[
N = M/C_0 \setminus D_0.
\]
Since deletion and contraction only affect elements of the ground set, we may replace
$C_0$ and $D_0$ by $C_0\cap E(M)$ and $D_0\cap E(M)$ and hence assume
$C_0,D_0\subseteq E(M)$.

Now set
\[
C := C_0,
\qquad
D := D_0\setminus C_0.
\]
Then $C,D\subseteq E(M)$ and $C\cap D=\varnothing$.

It remains to show that deleting $D_0$ after contracting $C_0$ is the same as deleting
$D_0\setminus C_0$ after contracting $C_0$.
After contracting $C_0$, the ground set becomes $E(M)\setminus C_0$, so elements of
$D_0\cap C_0$ are not present in $M/C_0$ and deleting them has no effect. Hence
\[
(M/C_0)\setminus D_0 \;=\; (M/C_0)\setminus (D_0\setminus C_0).
\]
Therefore
\[
N \;=\; M/C \setminus D,
\]
with $C,D\subseteq E(M)$ disjoint, as required.
\end{proof}

\begin{lemma}[IsMinor_antisymm]\label{thm:minor-order}
The minor relation $\le_m$ defines a partial order on the class of matroids on $\alpha$.
Explicitly:
\begin{itemize}
  \item $N \le_m N$ for all $N$ (reflexivity),
  \item if $N \le_m M$ and $M \le_m P$, then $N \le_m P$ (transitivity),
  \item if $N \le_m M$ and $M \le_m N$, then $N = M$ (antisymmetry).
\end{itemize}
\end{lemma}

\begin{proof}
\textbf{Reflexivity.}
For any matroid $N$, taking $C=D=\varnothing$ gives
\[
N = N/\varnothing \setminus \varnothing,
\]
so $N \le_m N$.

\medskip
\textbf{Transitivity.}
Assume $N \le_m M$ and $M \le_m P$.
By Lemma~\ref{lem:disjoint-contract-delete}, choose disjoint $C_1,D_1\subseteq E(M)$ and
disjoint $C_2,D_2\subseteq E(P)$ such that
\[
N = M/C_1 \setminus D_1,
\qquad
M = P/C_2 \setminus D_2.
\]
Since $M = P/C_2 \setminus D_2$ with $C_2\cap D_2=\varnothing$, we have
\[
E(M)=E(P)\setminus(C_2\cup D_2),
\]
so $C_1\cup D_1\subseteq E(M)$ implies $C_1\cap(C_2\cup D_2)=\varnothing$ and
$D_1\cap(C_2\cup D_2)=\varnothing$. In particular, all of $C_1,D_1,C_2,D_2$ are pairwise
disjoint as needed below.

Substituting $M = P/C_2\setminus D_2$ into the expression for $N$ gives
\[
N \;=\; \Bigl( (P/C_2\setminus D_2)/C_1 \Bigr)\setminus D_1.
\]
Using the standard identities for disjoint deletions and contractions
\[
(M\setminus T_1)\setminus T_2 = M\setminus (T_1\cup T_2),\qquad
(M/T_1)/T_2 = M/(T_1\cup T_2),\qquad
(M/T_1)\setminus T_2 = (M\setminus T_2)/T_1,
\]
we may commute and combine these operations (since all the relevant sets are disjoint) to obtain
\[
N \;=\; P/(C_2\cup C_1)\setminus (D_2\cup D_1).
\]
Hence $N \le_m P$.

\medskip
\textbf{Antisymmetry.}
Assume $N \le_m M$ and $M \le_m N$.
By Lemma~\ref{lem:disjoint-contract-delete}, write
\[
N = M/C \setminus D
\quad\text{with}\quad
C,D\subseteq E(M),\ \ C\cap D=\varnothing.
\]
Then the ground set is
\[
E(N)=E(M)\setminus(C\cup D).
\]
In particular $E(N)\subseteq E(M)$. Symmetrically, $E(M)\subseteq E(N)$, hence
$E(M)=E(N)$. Therefore
\[
E(M)=E(M)\setminus(C\cup D),
\]
which forces $C\cup D=\varnothing$, so $C=D=\varnothing$. Thus
\[
N = M/\varnothing\setminus\varnothing = M,
\]
proving antisymmetry.

Since $\le_m$ is reflexive, transitive, and antisymmetric, it is a partial order.
\end{proof}
