\begin{definition}[IsQuasiFiniteModule] Given a local ring $A$ with the maximal ideal \(\mathfrak{m}\), we say that an \(A\)-module \(M\) is quasi-finite over \(A\) if \(M/\mathfrak{m} M \) has finite rank over the residue field \(k = A/\mathfrak{m}\).
\end{definition}
\begin{theorem}[isolated_in_fiber_iff_stalk_quasiFinite]
Let \(f:X\to Y\) be a morphism locally of finite type, and let \(x\) be a point of \(X\). The following conditions are equivalent:
\begin{enumerate}[label=(\alph*)]
    \item The point \(x\) is isolated in its fiber \(f^{-1}(f(x))\).
    \item The ring \(\mathcal O_x\) is a quasi-finite \(\mathcal O_{f(x)}\)-module \((0,7.4.1)\).
\end{enumerate}
\end{theorem}

\begin{proof}
The question being evidently local on \(X\) and on \(Y\), one may suppose \(X=\mathrm{Spec}(A)\) and \(Y=\mathrm{Spec}(B)\) affine, \(A\) being a \(B\)-algebra of finite type. Moreover, one may replace \(X\) by \(X\times_Y\mathrm{Spec}(\mathcal O_{f(x)})\) without changing the fiber \(f^{-1}(f(x))\) nor the local ring \(\mathcal O_x\); thus one may suppose that \(B\) is a local ring, equal to \(\mathcal O_{f(x)}\).

If \(\mathfrak n\) is the maximal ideal of \(B\), then \(f^{-1}(f(x))\) is an affine scheme with ring \(A/\mathfrak n A\), of finite type over \(k(f(x))=B/\mathfrak n\). This being so, if \((a)\) holds, one may moreover suppose that \(f^{-1}(f(x))\) is reduced to the point \(x\); hence \(A/\mathfrak n A\) is of finite rank over \(B/\mathfrak n\), in other words \(A\) is a quasi-finite \(B\)-module.

Conversely, if (b) holds, \(f^{-1}(f(x))\) is an affine Artinian scheme, hence discrete; consequently \(x\) is isolated in its fiber \(f^{-1}(f(x))\).
\end{proof}
