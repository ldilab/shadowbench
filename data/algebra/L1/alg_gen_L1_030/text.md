\begin{theorem}[isCoprime_iff_zeroLocus_inter_eq_empty]
Two ideals $I$ and $J$ of $k[x_1,\ldots,x_n]$ are said to be \emph{coprime} if and only if
$I+J = k[x_1,\ldots,x_n]$. Show the following:
\begin{enumerate}
  \item If $k=\mathbb C$, then $I$ and $J$ are coprime if and only if
  $\mathbf V(I)\cap \mathbf V(J)=\varnothing$.
  \item If $I$ and $J$ are coprime, then $IJ = I \cap J$.
\end{enumerate}
\end{theorem}

\begin{proof}
\begin{enumerate}
  \item First note that
  \[
    \mathbf V(I)\cap \mathbf V(J)=\mathbf V(I+J).
  \]
  Indeed, a point lies in $\mathbf V(I)\cap \mathbf V(J)$ iff it vanishes on every polynomial in $I$
  and in $J$, equivalently on every polynomial in the sum $I+J$.

  If $I$ and $J$ are coprime, then $I+J=k[x_1,\ldots,x_n]$, hence $\mathbf V(I+J)=\varnothing$ and
  therefore $\mathbf V(I)\cap \mathbf V(J)=\varnothing$.

  Conversely, assume $\mathbf V(I)\cap \mathbf V(J)=\varnothing$. Then $\mathbf V(I+J)=\varnothing$.
  Over $k=\mathbb C$, Hilbert's Nullstellensatz implies that $\mathbf V(K)=\varnothing$ if and only if
  $\sqrt{K}=k[x_1,\ldots,x_n]$. Applying this to $K=I+J$ gives $\sqrt{I+J}=k[x_1,\ldots,x_n]$, hence
  $I+J=k[x_1,\ldots,x_n]$ and $I,J$ are coprime.

  \item We always have $IJ\subseteq I\cap J$.

  For the reverse inclusion, let $f\in I\cap J$. Since $I$ and $J$ are coprime, we can write
  $1=a+b$ with $a\in I$ and $b\in J$. Then
  \[
    f=f\cdot 1=f(a+b)=fa+fb.
  \]
  Here $fa\in JI=IJ$ because $f\in J$ and $a\in I$, and similarly $fb\in IJ$ because $f\in I$ and
  $b\in J$. Hence $f\in IJ$, so $I\cap J\subseteq IJ$.
\end{enumerate}
\end{proof}
