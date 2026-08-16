\begin{theorem}[zeroLocus_subset_of_ideal_le]
If $I_1 \subseteq I_2$ are ideals, then $\mathbf V(I_1) \supseteq \mathbf V(I_2)$.
\end{theorem}

\begin{proof}
First, let $I_1 \subseteq I_2$ be ideals. If $a \in \mathbf V(I_2)$, then $f(a)=0$ for every $f \in I_2$.
Since $I_1 \subseteq I_2$, we also have $f(a)=0$ for every $f \in I_1$, hence $a \in \mathbf V(I_1)$.
Therefore $\mathbf V(I_2) \subseteq \mathbf V(I_1)$, i.e., $\mathbf V(I_1) \supseteq \mathbf V(I_2)$.
\end{proof}

\begin{theorem}[vanishingIdeal_le_of_subset]
If $V_1 \subseteq V_2$ are affine algebraic sets, then $\mathbf I(V_1) \supseteq \mathbf I(V_2)$.
\end{theorem}

\begin{proof}
Similarly, if $V_1 \subseteq V_2$ and $f \in \mathbf I(V_2)$, then $f(a)=0$ for every $a \in V_2$.
In particular, $f(a)=0$ for every $a \in V_1$, so $f \in \mathbf I(V_1)$.
Thus $\mathbf I(V_2) \subseteq \mathbf I(V_1)$, i.e., $\mathbf I(V_1) \supseteq \mathbf I(V_2)$.
\end{proof}

\begin{theorem}[zeroLocus_radical_eq_zeroLocus]
For any ideal $I$, $\mathbf V(\sqrt{I})=\mathbf V(I)$.
\end{theorem}

\begin{proof}
Finally, we prove $\mathbf V(\sqrt{I})=\mathbf V(I)$.
Since $I \subseteq \sqrt{I}$, the inclusion-reversing property implies $\mathbf V(\sqrt{I}) \subseteq \mathbf V(I)$.
Conversely, let $a \in \mathbf V(I)$ and let $f \in \sqrt{I}$. Then $f^m \in I$ for some $m \ge 1$,
so $(f(a))^m = (f^m)(a) = 0$. Since we are over a field, this implies $f(a)=0$, hence $a \in \mathbf V(\sqrt{I})$.
Therefore $\mathbf V(I) \subseteq \mathbf V(\sqrt{I})$, and the equality follows.
\end{proof}
