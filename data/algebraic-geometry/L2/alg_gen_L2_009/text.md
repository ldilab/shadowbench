\begin{definition}[FiniteType]
A morphism \(f : X \to Y\) is said to be \emph{of finite type} if \(Y\) is the union of a family \((V_\alpha)\) of affine open subsets having the following property:

\medskip

\noindent
(P) The inverse image \(f^{-1}(V_\alpha)\) is a finite union of affine open subsets \(U_{\alpha i}\) such that each of the rings \(\Gamma(U_{\alpha i},\mathcal O_X)\) is a finitely type \(\Gamma(V_\alpha,\mathcal O_Y)\)-algebra.

\medskip

In that case one also says that \(X\) is a scheme of finite type over \(Y\), or a \(Y\)-scheme of finite type.
\end{definition}

\begin{theorem}[surjective_iff_surjective_on_algClosed_points_of_finiteType]
Let \(f:X\to Y\) be a morphism of finite type. In order that \(f\) be surjective, it is necessary and sufficient that, for every algebraically closed field \(\Omega\), the map \(
X(\Omega)\to Y(\Omega)\) corresponding to \(f\) be surjective.
\end{theorem}
\begin{proof}
The condition is sufficient, as one sees by considering, for every \(y\in Y\), an algebraically closed extension \(\Omega\) of \(k(y)\), and the commutative diagram
\[
\begin{array}{ccc}
& \mathrm{Spec}(\Omega) & \\
& \swarrow \quad \searrow & \\
X & \xrightarrow{\ f\ } & Y .
\end{array}
\]

Conversely, suppose \(f\) is surjective, and let \(g:\{\xi\}=\mathrm{Spec}(\Omega)\to Y\) be a morphism, where \(\Omega\) is an algebraically closed field. Consider the Cartesian diagram
\[
\begin{array}{ccc}
X_\Omega & \longrightarrow & X \\
f_\Omega \downarrow  & & \downarrow f \\
\mathrm{Spec}(\Omega) & \xrightarrow{\ g\ } & Y .
\end{array}
\]
It is therefore enough to show that there exists in \(X_\Omega\) a point rational over \(\Omega\). Since \(f\) is surjective, \(X_\Omega\) is not empty, and since \(f\) is of finite type, the same is true of \(f_\Omega\). Hence \(X_\Omega\) contains a nonempty affine open subset \(Z\) such that \(\Gamma(Z,\mathcal O_{X_\Omega})\) is a nonzero algebra of finite type over \(\Omega\). By Hilbert's Nullstellensatz, there exists an \(\Omega\)-homomorphism \(
\Gamma(Z,\mathcal O_{X_\Omega})\to \Omega\), hence a section of \(X_\Omega\) over \(\mathrm{Spec}(\Omega)\). 
\end{proof}
