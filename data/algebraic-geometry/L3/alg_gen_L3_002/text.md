Theorem (ExcessLociCrossings)

Let $C_1$ and $C_2$ be algebraic curves on a projective plane $\mathbb{P}^2(K)$, each of degree $m$ and $n$. If
$$
|C_1 \cap C_2| > mn,
$$
then there is an algebraic curve $C$ such that
$$
C \subseteq C_1 \cap C_2.
$$

Proof.

Suppose the curves $C_1$ and $C_2$ are defined by homogeneous polynomials $\varphi_1(x, y, z)$ and $\varphi_2(x, y, z)$ each of degree $m$ and $n$. Organizing the polynomials in the descending order of $z$, we have
$$
\begin{align*}
\varphi_1(x, y, z) &= a_0(x,y)z^m + a_1(x,y)z^{m-1} + \cdots + a_m(x, y),\\
\varphi_2(x,y,z) &= b_0(x,y)z^n + b_1(x,y)z^{n-1} + \cdots + b_n(x,y),
\end{align*}
$$
where each of $a_i(x,y)$ and $b_j(x,y)$ is a homogeneous polynomial of degree $i$ and $j$ respectively.

Consider the resultant $R(\varphi_1, \varphi_2)$ of $\varphi_1$ and $\varphi_2$, namely the determinant of the following $(m+n)\times(m+n)$ matrix.
$$
M(\varphi_1, \varphi_2) = \begin{pmatrix}
a_0 & a_1 & \cdots & \cdots & a_m & 0 & 0 & \cdots & 0 \\
0 & a_0 & \cdots & \cdots & a_{m-1} & a_m & 0 & \cdots & 0 \\\
\cdot & \cdot & \cdots & \cdots & \cdots & \cdots &  \cdots & \cdots & \cdot \\
0 & \cdot & \cdots & a_0 & \cdots & \cdots & \cdots & \cdots & a_m \\
b_0 & b_1 & \cdots & \cdots & \cdots & b_n & 0 & \cdots & 0 \\
0 & b_0 & \cdots & \cdots & \cdots & b_{n-1} & b_n & \cdots & 0 \\
\cdot & \cdot & \cdots & \cdots & \cdots & \cdots & \cdots & \cdots &\cdot \\
0 & 0 & \cdots & 0 & b_0 & b_1 & \cdots & \cdots & b_n
\end{pmatrix}
$$
Then this is a homogeneous polynomial of degree $mn$ in $x$ and $y$.

Now, suppose $\{[x_i, y_i, z_i] \mid 0 \le i \le mn \} \subseteq C_1 \cap C_2$. After some appropriate change of variables, we might assume $[x_i, y_i, z_i] \ne [0,0,1]$ for each $0 \le i \le mn$. In the algebraic closure $\overline{K}$ of $K$, for each $0 \le i \le mn$, there are $m$ roots $\lambda_{ij}$(where $1 \le j \le m$) of $\varphi_1(x_i, y_i, z)$ and $n$ roots $\mu_{ik}$(where $1 \le k \le n$) of $\varphi_2(x_i, y_i, z)$. Then we have
$$
R(\varphi_1, \varphi_2)(x_i, y_i) = a_0(x_i, y_i)^n b_0(x_i, y_i)^m \prod_{1 \le j \le m,\ 1 \le k \le n} (\lambda_{ij} - \mu_{ik}),
$$
so that $R(\varphi_1, \varphi_2)(x_i, y_i) = 0$ for each $0 \le i \le mn$, hence $R(\varphi_1, \varphi_2) = 0$.

Suppose arbitrary polynomials
$$
\begin{align*}
a(x,y,z) &= \alpha_0(x,y) + \alpha_1(x,y) z + \cdots + \alpha_{n-1}(x,y)z^{n-1}, \\
b(x,y,z) &= \beta_0(x,y) + \beta_1(x,y) z + \cdots + \beta_{m-1}(x,y)z^{m-1},
\end{align*}
$$
and the linear combination of $\varphi_1$ and $\varphi_2$ by them, namely
$$
\begin{align*}
c(x,y,z) &= a(x,y,z)\varphi_1(x,y,z) + b(x,y,z)\varphi_2(x,y,z) \\
&= \gamma_0(x,y) + \gamma_1(x,y)z + \cdots + \gamma_{m+n-1}(x,y)z^{m+n-1}.
\end{align*}
$$
Then
$$
(\gamma_{m+n-1}, \cdots, \gamma_0) = (\alpha_{n-1}, \cdots, \alpha_0, \beta_{m-1}, \cdots, \beta_0) \cdot M(\varphi_1, \varphi_2),
$$
hence there exists a pair of nonzero polynomials $a(x,y,z)$ and $b(x,y,z)$ which makes $c(x,y,z) = 0$.

Now let
$$
a(x,y,z)\varphi_1(x,y,z) + b(x,y,z)\varphi_2(x,y,z) = 0.
$$
If $\varphi_1$ and $\varphi_2$ don't have a nontrivial common divisor in $K[x,y,z]$(which is a UFD), then every factor of $\varphi_1$ must be that of $b(x,y,z)$. But this is a contradiction, since the total degree of $b(x,y,z)$ is smaller than $\varphi_1$. Thus $\varphi_1$ and $\varphi_2$ attain a nontrivial common divisor, namely $\psi(x,y,z)$. Having $\varphi_1$ and $\varphi_2$ both homogeneous, their common divisor $\psi$ must also be homogeneous. Now the result simply comes as the curve $C$ defined by $\psi$ satisfies $C \subseteq C_1 \cap C_2$.
