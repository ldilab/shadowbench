\begin{theorem}[exists_unitary_near_of_approx_unitary]
Let $\mathcal A$ be a unital $C^*$-algebra. Show that for any $\varepsilon > 0$ there exists a
$\delta_\varepsilon > 0$ such that if $a \in \mathcal A$ obeys
\[
    \max\left\{ \|a^*a-\mathbf 1\|,\ \|aa^*-\mathbf 1\| \right\} \le \delta_\varepsilon,
\]
then there exists a unitary $u \in \mathcal A$ with
\[
    \|a-u\| \le \varepsilon.
\]
\end{theorem}

\begin{proof}
Fix $\varepsilon>0$ and put
\[
    \delta_\varepsilon:=\min\left\{\frac12,\varepsilon\right\}.
\]
Suppose that
\[
    \max\{\|a^*a-\mathbf 1\|,\|aa^*-\mathbf 1\|\}\le \delta_\varepsilon.
\]
Set
\[
    b:=a^*a.
\]
Then $b$ is positive, hence $b=b^*$ and $\sigma(b)\subset[0,\infty)$. Moreover,
\[
    \|b-\mathbf 1\|\le\delta_\varepsilon<1,
\]
so $b$ is invertible. Also, since $b=b^*$, for every $\lambda\in\sigma(b)$ we have
\[
    |\lambda-1|\le \|b-\mathbf 1\|\le \delta_\varepsilon.
\]
Thus
\[
    \sigma(b)\subset[1-\delta_\varepsilon,1+\delta_\varepsilon].
\]

By the square root lemma, let
\[
    h:=\sqrt b.
\]
Then
\[
    h=h^*,\qquad \sigma(h)\subset[0,\infty),\qquad h^2=b.
\]
Since $b$ is invertible, $h$ is invertible. Define
\[
    u:=ah^{-1}.
\]
Then
\[
    u^*u
    =
    h^{-1}a^*ah^{-1}
    =
    h^{-1}bh^{-1}
    =
    \mathbf 1.
\]

Also, since $\|aa^*-\mathbf 1\|<1$, the element $aa^*$ is invertible. Thus $a$ has a left inverse
\[
    (a^*a)^{-1}a^*
\]
and a right inverse
\[
    a^*(aa^*)^{-1}.
\]
Hence $a$ is invertible, and so $u=ah^{-1}$ is invertible. Since $u^*u=\mathbf 1$, we get
\[
    u^{-1}=u^*.
\]
Therefore
\[
    uu^*=\mathbf 1.
\]
Thus $u$ is unitary.

Finally, since $a=uh$,
\[
    a-u=u(h-\mathbf 1).
\]
As multiplication by a unitary preserves the norm,
\[
    \|a-u\|=\|h-\mathbf 1\|.
\]
By spectral mapping,
\[
    \sigma(h)
    \subset
    \left[
        \sqrt{1-\delta_\varepsilon},
        \sqrt{1+\delta_\varepsilon}
    \right].
\]
Since $h=h^*$,
\[
    \|h-\mathbf 1\|
    =
    \sup_{\lambda\in\sigma(h)}|\lambda-1|
    \le
    \max\left\{
        1-\sqrt{1-\delta_\varepsilon},
        \sqrt{1+\delta_\varepsilon}-1
    \right\}.
\]
For $0<\delta_\varepsilon\le 1$,
\[
    1-\sqrt{1-\delta_\varepsilon}\le\delta_\varepsilon,
    \qquad
    \sqrt{1+\delta_\varepsilon}-1\le\delta_\varepsilon.
\]
Therefore
\[
    \|a-u\|
    =
    \|h-\mathbf 1\|
    \le
    \delta_\varepsilon
    \le
    \varepsilon.
\]
This proves the claim.
\end{proof}
