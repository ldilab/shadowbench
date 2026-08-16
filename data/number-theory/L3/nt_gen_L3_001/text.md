Theorem (MertensTheorem0)

$$
\sum_{m = 1}^n \frac{\Lambda(n)}{n} - \log n = O(1).
$$
Here, $\Lambda(n)$ is the von Mangoldt function, namely
$$
\Lambda(n) = \sum_{p^k \le n,\ p\ \textrm{prime}} \log p.
$$

Proof.

First note that
$$
\begin{align*}
\log n! &= \sum_{p^k \le n,\ p\ \textrm{prime}} \left\lfloor \frac{n}{p^k} \right\rfloor \log p \\
&= \sum_{p^k \le n,\ p\ \textrm{prime}} \left( \frac{n}{p^k} + O(1) \right) \log p \\
&= n \sum_{p^k \le n,\ p\ \textrm{prime}} \frac{\log p}{p^k} + O(n).
\end{align*}
$$
Here, $\sum_{p^k \le n,\ p\ \textrm{prime}} \log p = O(n)$ is used to obtain the last equality. To see why this holds, observe that
$$
\sum_{n < p \le 2n,\ p\ \textrm{prime}} \log p \le \log \binom{2n}{n} = O(n),
$$
since $\binom{2n}{n}$ has all the primes $n < p \le 2n$ as factors. Telescoping the left side downward then gives
$$
\sum_{\textrm{prime}\ p \le n} \log p = O(n).
$$
The sum for $p^k \le n$ is merely the left-hand side summed up for $n, n^{1/2}, n^{1/3}, \cdots$ for an appropriate $O(\log n)$ times, hence
$$
\sum_{p^k \le n,\ p\ \textrm{prime}} \log p = \sum_{\textrm{prime}\ p \le n} \log p  + O(\sqrt{n} \log n) = O(n).
$$
Returning to the theorem, we have $\log n! = n \log n + O(n)$, thanks to Sterling's approximation. Comparing the two approximation on $\log n!$ thus results in
$$
\sum_{p^k \le n,\ p\ \textrm{prime}} \frac{\log p}{p^k} = \log n + O(1),
$$
and its left-hand side is exactly equal to $\sum_{m = 1}^n \frac{\Lambda(n)}{n}$.

Theorem (MertensTheorem1)

$$
\sum_{\textrm{prime}\ p \le n} \frac{\log p}{p} - \log n = O(1).
$$

Proof.

This is the result of the above theorem, in that the sum of $\frac{\log p}{p^k}$ over prime powers with $k \ge 2$ converges.

Theorem (MertensTheorem2)

For some real constant $M$,
$$
\sum_{\textrm{prime}\ p \le n} \frac{1}{p} - \log \log n = M + O\left(\frac{1}{\log n}\right).
$$

Proof.

Denoting
$$
R(x) = \sum_{\textrm{prime}\ p \le x} \frac{\log p}{p} - \log x
$$
for general real $x \ge 2$, we have from the above theorem that $R(x) = O(1)$. Now, use the method of partial summation to obtain

$$
\begin{align*}
\sum_{\textrm{prime}\ p \le n} \frac{1}{p}
&= \sum_{\textrm{prime}\ p \le n} \frac{\log p}{p} \cdot \frac{1}{\log p} \\
&= \sum_{\textrm{prime}\ p \le n} \frac{\log p}{p} \left( \frac{1}{\log n} - \left(\frac{1}{\log n} - \frac{1}{\log p}\right) \right) \\
&= \frac{1}{\log n} \sum_{\textrm{prime}\ p \le n} \frac{\log p}{p} + \sum_{\textrm{prime}\ p \le n} \frac{\log p}{p} \int_p^n \frac{dt}{t \log^2 t} \\
&= \frac{1}{\log n} \sum_{\textrm{prime}\ p \le n} \frac{\log p}{p} + \int_2^n \sum_{2 \le p \le t,\ p\ \textrm{prime}} \frac{\log p}{p} \frac{dt}{t \log^2 t} \\
&= 1 + \frac{R(n)}{\log n} + \int_2^n \frac{\log t + R(t)}{t \log^2 t} \ dt \\
&= 1 + \frac{R(n)}{\log n} + \log \log n - \log \log 2 + \int_2^\infty \frac{R(t)}{t \log^2 t} \ dt - \int_n^\infty \frac{R(t)}{t \log^2 t} \ dt \\
&= \log \log n + \left(1 - \log \log 2 + \int_2^\infty \frac{R(t)}{t \log^2 t} \ dt\right) + O\left(\frac{1}{\log n}\right).
\end{align*}
$$
The final integrals converge; letting $M = 1 - \log \log 2 + \int_2^\infty \frac{R(t)}{t \log^2 t} \ dt$, we have the desired fact.

Definition (MeisselMertensConstant)

The Meissel-Mertens constant is the unique constant $M$ to which the left-hand side in the last theorem above converges.
