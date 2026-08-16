Theorem (CayleyTreeCount)

There are $n^{n-2}$ distinct vertex-labeled trees with $n$ vertices.

Proof.

Consider the vertex label $\{1, 2, \cdots, n\}$, and denote by $T_{n, k}$ the number of vertex-labeled forests with the $n$ vertices consisting of $k$ trees, where a fixed set $\{1, 2, \cdots, k\}$ of $k$ vertices belong to different trees.
Suppose the vertex $1$ has $i$ neighboring vertices. Then removing the vertex $1$ from the forest yields $i-1$ more trees, and thus the resulting forest consists of $k-1+i$ trees. Now any forest of $n$ vertices and $k$ trees can be restored by fixing some $0 \le i \le n - k$, choosing $i$ neighbors of $1$ out of $(n-1)-(k-1) = n-k$ vertices in $\binom{n-k}{i}$ possible ways, and then connecting the rest part of the trees in $T_{n-1, k-1+i}$ possible ways. Summing up the cases yields
$$
T_{n, k} = \sum_{i=0}^{n-k} \binom{n-k}{i} T_{n-1, k-1+i}.
$$
We claim for each $n \ge 1$ and $0 \le k \le n$ that
$$
T_{n,k} = kn^{n-k-1},
$$
and in particular, denoting by $T_n$ the number of vertex-labeled trees,
$$
T_n = T_{n, 1} = n^{n-2}.
$$
For the base case $n = 1$, it is simply checked that $T_{1,0} = 0$ and $T_{1,1} = 1$, both fitting into the claim. Applying induction on $n$, we have
$$
\begin{align}
T_{n,k}
&= \sum_{i=0}^{n-k} \binom{n-k}{i} (k-1+i) (n-1)^{n-1-k-i} & (i \to n - k - i)\\
&= \sum_{i=0}^{n-k} \binom{n-k}{i} (n-1+i) (n-1)^{i-1}  \\
&= \sum_{i=0}^{n-k} \binom{n-k}{i} (n-1)^i - \sum_{i=1}^{n-k} \binom{n-k}{i} i(n-1)^{i-1}\\
&= n^{n-k} - (n-k) \sum_{i=1}^{n-k} \binom{n-1-k}{i-1} (n-1)^{i-1} \\
&= n^{n-k} - (n-k) \sum_{i=0}^{n-1-k} \binom{n-1-k}{i} (n-1)^i \\
&= n^{n-k} - (n-k) n^{n-1-k} \\
&= k n^{n-1-k}.
\end{align}
$$
Here in the fourth equality, binomial theorem is applied in the form $((n-1)+1)^{n-k}$. The desired fact is now shown.
