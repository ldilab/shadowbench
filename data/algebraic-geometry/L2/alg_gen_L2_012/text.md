\begin{definition}[IsLimitPreservingOver]
     Let $S$ be a scheme. We say that a functor $F:(\mathrm{Sch}/S)^{\mathrm{opp}} \to \mathrm{Sets}$ is limit preserving if for every directed inverse system ${T_i}_{i \in I}$ of affine schemes with limit $T$ we have $F(T)=\mathrm{colim}_i F(T_i)$.
\end{definition}
\begin{theorem}[locallyOfFinitePresentation_iff_functorOfPoints_limitPreserving]
    Let $f:X \to S$ be a morphism of schemes. Then $f$ is locally of finite presentation if and only if the functor of points $h_X$ of $X$ is limit preserving.
\end{theorem}
\begin{proof}
    First, assume that $h_X$ is limit preserving. Choose any affine opens $U \subset X$ and $V\subset S $ such that $f(U) \subset V$. We have to show that $\mathcal{O}_S(V) \to \mathcal{O}_X(U)$ is of finite presentation. Let $(A_i, \varphi_{ii'})$ be a directed system of $\mathcal{O}_S(V)$-algebras. Set $A=\mathrm{colim}_i A_i$. We have to show that
    \[
        \mathrm{Hom}_{\mathcal{O}_S(V)} (\mathcal{O}_X(U),A) = \mathrm{colim}_i\mathrm{Hom}_{\mathcal{O}_S(V)}(\mathcal{O}_X(U),A_i)
    \]
    Consider the schemes $T_i=\mathrm{Spec}(A_i)$. They form an inverse system of $V$-schemes over $I$ with transition morphisms $f_{ii'}:T_i \to T_{i'}$ induced by the $\mathcal{O}_S(V)$-algebra maps $\varphi_{i'i}$. Set $T:=\mathrm{Spec}(A)=\mathrm{lim}_i T_i$. The formula above becomes in terms of morphism sets of schemes
    \[
        \mathrm{Mor}_V(\mathrm{lim}_i T_i,U) = \mathrm{colim}_i \mathrm{Mor}_V (T_i,U).
    \]
    We first observe that $\mathrm{Mor}_V(T_i,U)=\mathrm{Mor}_S(T_i,U)$ and $\mathrm{Mor}_V(T,U)=\mathrm{Mor}_S(T,U)$. Hence we have to show that
    \[
        \mathrm{Mor}_S(\mathrm{lim}_i T_i,U) = \mathrm{colim}_i \mathrm{Mor}_S(T_i,U)
    \]
    and we are given that
    \[
        \mathrm{Mor}_S(\mathrm{lim}_i T_i,X) = \mathrm{colim}_i \mathrm{Mor}_S(T_i,X).
    \]
    Hence it suffices to prove that given a morphism $g_i:T_i \to X$ over $S$ such that the composition $T \to T_i \to X$ ends up in $U$ there exists some $i' \ge i$ such that the composition $g_{i'}:T_{i'} \to T_i \to X$ ends up in $U$. Denote $Z_{i'}= g_{i'}^{-1}(X \setminus U)$. Assume each $Z_{i'}$ is nonempty to get a contradiction. Note that there exists a point $t$ of $T$ which is mapped into $Z_{i'}$ for all $i' \ge i$. Such a point is not mapped into $U$. A contradiction.

    Now assume that $f$ is locally of finite presentation. Let an inverse directed system $(T_i,f_{ii'})$ of $S$-schemes with each $T_i$ affine be given. Since each $T_i$ is affine, the morphisms $f_{ii'}$ are affine and each $T_i$ is quasi-compact and quasi-separated as a scheme. Let $T=\mathrm{lim}_i T_i$. Denote $f_i:T \to T_i$ the projection morphisms. We have to show:
    \begin{enumerate}[label=(\alph*)]
        \item Given morphisms $g_i,g_i':T_i \to X$ over $S$ such that $g_i \circ f_i=g_i' \circ f_i$, then there exists an $i' \ge i$ such that $g_i\circ f_{i'i}=g_i' \circ f_{i'i}$.
        \item Given any morphism $g:T \to X$ over $S$ there exists an $i \in I$ and a morphism $g_i:T_i \to X$ such that $g=f_i \circ g_i$.
    \end{enumerate}

    First let us prove the uniqueness part (a). Let $g_i,g_i':T_i \to X$ be morphisms such that $g_i \circ f_i=g_i' \circ f_i$. For any $i' \ge i$ we set $g_i' = g_i \circ f_{i' i}$ and $g_{i'}'=g_i' \circ f_{i'i}$. We also set $g=g_i \circ f_i=g_i' \circ f_i$. Consider the morphism $(g_i,g_i'):T_i \to X \times_S X$. Set
    \[
        W = \bigcup \nolimits _{U \subset X \text{ affine open}, V \subset S \text{ affine open}, f(U) \subset V} U \times_V U.
    \]
    This is an open in $X \times_S X$, with the property that the morphism $\Delta_{X/S}$ factors through a closed immersion into $W$. Note that the composition $(g_i,g_i') \circ f_i:T \to X \times_S X$ is a morphism into $W$ because it factors through the diagonal by assumption. Set $Z_{i'}=(g_{i'},g_{i'}')^{-1}(X \times_S X \setminus W)$. If each $Z_{i'}$ is nonempty, then there exists a point $t \in T$ which maps to $Z_{i'}$ for all $i' \ge i$. This is a contradiction with the fact that $T$ maps into $W$. Hence we may increase $i$ and assume that $(g_i,g_i'):T_i \to X \times_S X$ is a morphism into $W$. By construction of $W$, and since $T_i$ is quasi-compact we can find a finite affine open covering $T_i=T_{1,i} \cup \dots \cup T_{n,i}$ such that $(g_i,g_i')|_{T_{j,i}}$ is a morphism into $U \times_V U$ for some pair $(U,V)$ as in the definition of $W$ above. Since it suffices to prove that $g_{i'}$ and $g_{i'}'$ agree on each of the $f_{i'i}^{-1}(T_{j,i})$ this reduces us to the affine case. The affine case follows from the fact that the ring map $\mathcal{O}_S(V) \to \mathcal{O}_X(U)$ is of finite presentation.

    Finally, we prove the existence part (b). Let $g:T \to X$ be a morphism of schemes over $S$. We can find a finite affine open covering $T=W_1 \cup \dots \cup W_n$ such that for each $j \in \{1,\dots,n\}$ there exist affine opens $U_j \subset X$ and $V_j \subset S$ with $f(U_j) \subset V_j$ and $g(W_j) \subset U_j$. After possibly shrinking $I$, we may assume that there exist affine open coverings $T_i=W_{1,i} \cup \dots \cup W_{n,i}$ compatible with transition maps such that $W_j=\mathrm{lim}_i W_{j,i}$. Since $\mathcal{O}_S(V_j) \to \mathcal{O}_X(U_j)$ is of finite presentation, we can find for each $j$ an index $i_j \in I$ and a morphism $g_{j,i_j}:W_{j,i_j} \to X$ such that $g_{j,i_j}\circ f_i|_{W_j}:W_j \to W_{j,i} \to X$ equals $g|_{W_j}$. By part (a) proved above, using the quasi-compactness of $W_{j_1,i} \cap W_{j_2,i}$ which follows as $T_i$ is quasi-separated, we can find an index $i' \in I$ larger than all $i_j$ such that
    \[
        g_{j_1,i_{j_1}} \circ f_{i' i_{j_1}} |_{W_{j_1,i'} \cap W_{j_2,i'}} = g_{j_2,i_{j_2}} \circ f_{i' i_{j_2}} |_{W_{j_1,i'} \cap W_{j_2,i'}}
    \]
    for all $j_1,j_2 \in \{1,\dots,n\}$. Hence the morphisms $g_{j,i_j} \circ f_{i' i_j}|_{W_{j,i'}}$ glue to give the desired morphism $T_{i'} \to X$.
\end{proof}
