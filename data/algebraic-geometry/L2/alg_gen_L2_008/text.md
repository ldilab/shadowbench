\begin{definition}[FiniteType]
A morphism \(f : X \to Y\) is said to be \emph{of finite type} if \(Y\) is the union of a family \((V_\alpha)\) of affine open subsets having the following property:

\medskip

\noindent
(P) The inverse image \(f^{-1}(V_\alpha)\) is a finite union of affine open subsets \(U_{\alpha i}\) such that each of the rings \(\Gamma(U_{\alpha i},\mathcal O_X)\) is a finitely type \(\Gamma(V_\alpha,\mathcal O_Y)\)-algebra.

\medskip

In that case one also says that \(X\) is a scheme of finite type over \(Y\), or a \(Y\)-scheme of finite type.
\end{definition}

\begin{theorem}[hasPropertyP_of_finiteType]
    If \(f:X \to Y \) is a morphism of finite type, then every open affine subset \(W\) of \(Y\) has the property (P).
\end{theorem}
\begin{proof}
Let \(W\subseteq Y\) be an open affine. Then, \(W\) is quasi-compact. Therefore, \(W\) is covered by finitely many distinguished opens \(D(g_i)\subseteq V_{\alpha(i)}\), \( g_i\in \Gamma(V_{\alpha(i)},\mathcal O_Y)\), where each \(V_{\alpha(i)}\) belongs to the covering given by the definition. Fix one such distinguished open \(D(g)\subseteq V_\alpha\). By hypothesis, \(f^{-1}(V_\alpha)=\bigcup_j Z_j\) with \(Z_j\) affine and \(\Gamma(Z_j,\mathcal O_X)\) a finite type \(\Gamma(V_\alpha,\mathcal O_Y)\)-algebra. Let \(\varphi_j:\Gamma(V_\alpha,\mathcal O_Y)\to \Gamma(Z_j,\mathcal O_X)\) be the homomorphism induced by the restriction of \(f\) to \(Z_j\), and put \(g_j=\varphi_j(g)\). Then \(f^{-1}(D(g))\cap Z_j=D(g_j)\), and \(\Gamma(D(g_j),\mathcal O_X) = \Gamma(Z_j,\mathcal O_X)_{g_j} = \Gamma(Z_j,\mathcal O_X)[1/g_j]\). Hence, \(\Gamma(D(g_j),\mathcal O_X)\) is a finite type algebra over \(\Gamma(V_\alpha,\mathcal O_Y)[1/g] = \Gamma(D(g),\mathcal O_Y)\). Thus \(D(g)\) has the property (P). Since the \(D(g_i)\) form a finite affine cover of \(W\), it follows that \(W\) itself has the property \((P)\).
\end{proof}

\begin{theorem}[immersion_is_of_finiteType]
Let \(f : X \to Y\) be an immersion. If the underlying space of \(Y\) (resp. of \(X\)) is locally noetherian (resp. noetherian), then \(f\) is of finite type.
\end{theorem}

\begin{proof}
One may always suppose \(Y\) is affine by the lemma; if the underlying space of \(Y\) is locally noetherian, one may moreover suppose it is noetherian, since the underlying space of \(X\), being a subspace of it, is then noetherian. Otherwise, one may suppose \(Y\) is affine and the underlying space of \(X\) noetherian; then \(X\) admits a finite covering by affine opens \(D(g_i)\subset X\), \(g_i\in \Gamma(Y,\mathcal{O}_Y)\), each \(X\cap D(g_i)\) being closed in \(D(g_i)\) (hence an affine scheme), since \(X\) is locally closed in \(Y\). Therefore, \(\Gamma(X\cap D(g_i),\mathcal{O}_Y)\) is a finite type algebra over \(\Gamma(D(g_i),\mathcal{O}_Y)\), and thus \(X\cap D(g_i)\to D(g_i)\) is of finite type. Finally, \(\Gamma(D(g_i),\mathcal{O}_Y)=\Gamma(Y,\mathcal{O}_Y)_{g_i}=\Gamma(Y,\mathcal{O}_Y)[1/g_i]\), which is of finite type over \(\Gamma(Y,\mathcal{O}_Y)\), and this completes the proof.
\end{proof}
