\begin{definition}[IsLocallyNoetherian]
A scheme $X$ is locally Noetherian if $\mathcal{O}_X(U)$ is Noetherian for every affine open $U$.
\end{definition}

\begin{theorem}[isLocallyNoetherian_of_affine_cover] 
If a scheme $X$ has an affine open covering $X = \cup_{i \in I} U_i$ such that each $\Gamma(X,U_i)$ is Noetherian, then $X$ is locally Noetherian.
\end{theorem}

\begin{proof}
By the Affine communication lemma, it suffices to prove the following:
(1) If $U$ is an affine open such that $\Gamma(X,U)$ is Noetherian, then $\Gamma(X,U_f)$ is Noetherian for every $f \in \Gamma(X,U)$.
(2) If there exist a finite cover $U = \cup_{i \in S} U_{f_i}$ by basic opens with $f_i \in \Gamma(X,U)$ and each $\Gamma(X,U_{f_i})$ Noetherian, $\Gamma(X,U)$ is Noetherian.

Since $\Gamma(X,U_f) = \Gamma(X,U)_f$ and the localization of a Noetherian ring is Noetherian, we have (1).
For (2), since $f_i$'s generate the unit ideal in $\Gamma(X,U)$ from the given condition, it suffices to prove the following:
\begin{claim} 
Let $R$ be a commutative ring. If $f_1,\cdots,f_r \in R$ generate the unit ideal and each $R_{f_i}$ is Noetherian, then $R$ is Noetherian.
\end{claim}

\begin{proof}
Let $\varphi_i:R \to R_{f_i}$ be the localization map, $i=1,\cdots,r$. For any ideal $\mathfrak{a} \subseteq R$, we have
\[
\mathfrak{a} = \bigcap_{i=1}^r \varphi_i^{-1} (\varphi_i(\mathfrak{a}) \cdot R_{f_i}).
\]
Indeed, the inclusion $\subseteq$ is obvious. Conversely, suppose $b \in \cap_i \varphi_i^{-1} (\varphi_i(\mathfrak{a}) \cdot R_{f_i})$. Then $\varphi_i(b) = a_i/f_i^{n_i}$ in $A_{f_i}$ for each $i$, where $a_i \in \mathfrak{a}$ and $n_i >0$. Increasing $n_i$'s if necessary, we may choose all $n_i$'s equal to a fixed $n>0$. Then,
\[
f_i^{m_i}(f_i^n b - a_i) = 0
\]
in $R$ for some $m_i >0$. As before, we may take all $m_i$'s equal to a fixed $m>0$. Take $N=m+n$. Then $f_1^N,\cdots,f_r^n$ generate the unit ideal in $R$ and hence we have
\[ \sum_{i=1}^r c_i f_i^N = 1
\]
in $R$ for some $c_i $'s. So we have
\[
b = \sum_{i=1}^r c_i f_i^N b =  \sum_{i=1}^r c_i f_i^m a_i \in \mathfrak{a}.
\]

Now consider an ascending chain of ideals
\[
I_1 \subseteq I_2 \subseteq \cdots
\]
in $R$. For each $i$, we have
\[
\varphi_i^{-1} (\varphi_i(I_1) \cdot R_{f_i}) \subseteq \varphi_i^{-1} (\varphi_i(I_2) \cdot R_{f_i}) \subseteq \cdots
\]
which stabilizes since $R_{f_i}$ is Noetherian. Since there are finitely many $f_i$'s, the original chain also stabilizes from the equality we have proved.
\end{proof}
\end{proof}
