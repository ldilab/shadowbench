Theorem (EulerQuadrilateralThm)

Let $A$, $B$, $C$, $D$ be points in $\mathbb{R}^n$, $M$ the midpoint of $A$ and $C$, and $N$ the midpoint of $B$ and $D$. Then,
$$
\overline{AB}^2 + \overline{BC}^2 + \overline{CD}^2 + \overline{DA}^2 = \overline{AC}^2 + \overline{BD}^2 + 4 \overline{MN}^2.
$$

Proof.

Simply let the coordinates of points as $A = (a_1, \cdots, a_n)$, $B = (b_1, \cdots, b_n)$, $C = (c_1, \cdots, c_n)$, and $D = (d_1, \cdots, d_n)$ for each $a_i, b_i, c_i, d_i \in \mathbb{R}$; then we have $M = \left(\frac{a_1 + c_1}{2}, \cdots, \frac{a_n + c_n}{2}\right)$ and $N = \left(\frac{b_1 + d_1}{2}, \cdots, \frac{b_n + d_n}{2}\right)$. Using these coordinates, the above equality can be expressed as follows:
$$
\begin{align}
&\sum_{i=1}^n (a_i - b_i)^2 + \sum_{i=1}^n (b_i - c_i)^2 + \sum_{i=1}^n (c_i - d_i)^2 + \sum_{i=1}^n (d_i - a_i)^2 \\
& = \sum_{i=1}^n (a_i - c_i)^2 + \sum_{i=1}^n (b_i - d_i)^2 + \sum_{i=1}^n (a_i - b_i + c_i - d_i)^2.
\end{align}
$$
For each index $1 \le i \le n$, the direct expansion shows the equality by $i$'th summands, namely
$$
(a_i - b_i)^2 + (b_i - c_i)^2 + (c_i - d_i)^2 + (d_i - a_i)^2 = (a_i - c_i)^2 + (b_i - d_i)^2 + (a_i - b_i + c_i - d_i)^2.
$$
Hence the original equality on the sums holds, and the theorem is shown.
