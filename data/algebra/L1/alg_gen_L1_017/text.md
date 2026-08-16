\begin{lemma}[mem_monomialIdeal_iff_divisible]\label{lem:mem_monomialIdeal_iff_divisible} % [Cox] 70p Lemma 2
    Let $I = \langle x^\alpha \mid \alpha \in A \rangle$ be a monomial ideal.
    Then a monomial $x^\beta$ lies in $I$ if and only if $x^\beta$ is divisible by $x^\alpha$ for some $\alpha \in A$.
\end{lemma}
\begin{proof}
  If $x^\beta$ is a multiple of $x^\alpha$ for some $\alpha \in A$, then $x^\beta \in I$ by the definition of ideal. 
  Conversely, if $x^\beta \in I$, then $x^\beta = \sum_{i=1}^s h_i x^{\alpha(i)}$, where $h_i \in k[x_1, \dots, x_n]$ and $\alpha(i) \in A$. 
  If we expand each $h_i$ as a sum of terms, we obtain
  \[
  x^\beta = \sum_{i=1}^s h_i x^{\alpha(i)} = \sum_{i=1}^s \left(\sum_j c_{i,j} x^{\beta(i,j)}\right) x^{\alpha(i)} = \sum_{i,j} c_{i,j} x^{\beta(i,j)} x^{\alpha(i)}.
  \]
\end{proof}
