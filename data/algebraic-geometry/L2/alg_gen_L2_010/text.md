\begin{theorem}[isAffineOpen_inf_preimage]
Let \(Y\) be a separated scheme, and let \(f:X\to Y\) be a morphism. For every affine open subset \(U\) of \(X\) and every affine open subset \(V\) of \(Y\), \(U\cap f^{-1}(V)\) is affine.
\end{theorem}

\begin{proof}
Let \(p_1,p_2\) be the projections of \(X\times_{\mathbb Z}Y\). The subspace \(U\cap f^{-1}(V)\) is the image under \(p_1\) of \(\Gamma_f(X)\cap p_1^{-1}(U)\cap p_2^{-1}(V)\). Now \(p_1^{-1}(U)\cap p_2^{-1}(V)\) is identified with the underlying space of the scheme \(U\times_{\mathbb Z}V\), and is therefore an affine scheme. Since \(\Gamma_f\) is closed in
\(X\times_{\mathbb Z}Y\), the intersection \(\Gamma_f(X)\cap p_1^{-1}(U)\cap p_2^{-1}(V)
\) is closed in \(U\times_{\mathbb Z}V\). Consequently, the scheme induced by the subscheme of \(X\times_{\mathbb Z}Y\) associated with \(\Gamma_f\), on the open subset \(\Gamma_f(X)\cap p_1^{-1}(U)\cap p_2^{-1}(V)\) of its underlying space, is a closed subscheme of an affine scheme, hence is affine. The theorem then follows from the fact that \(\Gamma_f\) is an immersion.
\end{proof}
