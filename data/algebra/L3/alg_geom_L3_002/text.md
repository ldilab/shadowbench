Theorem (cannot_double_cube)

$\sqrt[3]{2}$ is not constructible.

Proof.

This comes directly from $[\mathbb{Q}(\sqrt[3]{2}) : \mathbb{Q}] = 3$, which is because the polynomial $x^3 - 2$ is the minimal polynomial of $\sqrt[3]{2}$ over $\mathbb{Q}$.

Theorem (cannot_square_circle)

$\sqrt{\pi}$ is not constructible.

Proof.

If $\sqrt{\pi}$ were constructible, then so were $\pi$ which is known to be transcendental. Since any constructible number is algebraic over $\mathbb{Q}$, we have the result.

Theorem (cannot_trisect_60deg)

The angle $20^\circ$ is not constructible.

Proof.

We use the fact that $\cos 3\theta = 4 \cos^3 \theta - 3 \cos \theta$. Replacing $\theta$ with $20^\circ$, we have for $\alpha = \cos 20^\circ$ that
$$
\frac{1}{2} = 4\alpha^3 - 3\alpha, \quad \textrm{hence} \quad 8\alpha^3 - 6\alpha - 1 = 0.
$$
The latter equation can be rewritten into $(2\alpha)^3 - 3(2\alpha) - 1 = 0$. Applying the prime-3 Eisenstein criterion gives that the polynomial $X^3 - 3X - 1$ is irreducible over $\mathbb{Q}$. Hence the polynomial is minimal, so that $[\mathbb{Q}(\alpha) : \mathbb{Q}] = 3 \ne 2^m$ for some $m \in \mathbb{N}$. The conclusion follows.
