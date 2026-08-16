Theorem (constructible_iff)

Let $\alpha \in \mathbb{R}$ and $K$ the normal closure of $\mathbb{Q}(\alpha)/\mathbb{Q}$(in $\mathbb{C}$). The number $\alpha$ is constructible if and only if $[K:\mathbb{Q}]$ is a power of 2.

Proof.

Suppose $[K:\mathbb{Q}] = 2^a$ for some $a \in \mathbb{N}$. We can then consider a composition series of $G = \mathrm{Gal}(K/\mathbb{Q})$; since its order is $2^a$, there is a sequence of subgroups $H_i$ of order $2^i$ such that
$$
\{\mathrm{id}\} = H_0 \triangleleft H_1 \triangleleft \cdots \triangleleft H_{a-1} \triangleleft H_a = G.
$$
According to Galois theory, this series corresponds to the tower of fixed fields
$$
\mathbb{Q} = K^{H_a} < K^{H_{a-1}} < \cdots < K^{H_1} < K^{H_0} = K,
$$
where $[K^{H_{i-1}}:K^{H_i}] = 2$. Since $\alpha$ is reached through finite consecutive step of quadratic extensions, we have that $\alpha$ is constructible.

Conversely, suppose $\alpha$ is constructible, so that it can be reached in a finite step of quadratic extensions. The normal closure $K$ of $\mathbb{Q}(\alpha)$ is $\mathbb{Q}(\alpha_1 = \alpha, \alpha_2, \cdots, \alpha_b)$ where $\alpha_i$ are the conjugates of $\alpha$. Then each $\alpha_i$ also lies in a finite quadratic extension of $\mathbb{Q}$. Gathering the extension element towards $\alpha_i$'s and then adjoining them in order would still give stepwise (at most) quadratic extension $K/\mathbb{Q}$, ending in $[K:\mathbb{Q}] = 2^a$ for some $a \in \mathbb{N}$.

Theorem (cyclotomic_angle_constructible_iff)

An angle $2\pi/n$ is constructible if and only if $n$ is a product of a power of $2$ and some distinct Fermat primes. Here, the Fermat prime is a prime number which is of the form $2^{2^a}+1$ for some nonnegative integer $a$. (This is equivalent to constructiblity of regular $n$-gon.)

Proof.

We clearly have $n = 1$ and $n = 2$ cases, so assume $n \ge 3$. Let $\zeta_n = \exp(2\pi i/n) = \cos (2\pi/n) + i \sin (2\pi/n)$ which is a primitive $n$-th root of unity; then we have that $\cos(2\pi/n) = (\zeta_n + \zeta_n^{-1})/2$. Note that $[\mathbb{Q}(\zeta_n):\mathbb{Q}] = \phi(n)$ where $\phi$ is Euler's totient function. Furthermore, $[\mathbb{Q}(\zeta_n):\mathbb{Q}(\zeta_n + \zeta_n^{-1})] = 2$ for $n \ge 3$; the extension degree doesn't exceed 2 as $\zeta_n^2 - (\zeta_n + \zeta_n^{-1})\zeta_n + 1 = 0$, where the extension is proper since $\mathbb{Q}(\zeta_n + \zeta_n^{-1})$ is totally real but $\mathbb{Q}(\zeta_n)$ isn't. This leads to $[\mathbb{Q}(\zeta_n + \zeta_n^{-1}) : \mathbb{Q}] = \phi(n)/2$, where the desired $\cos(2\pi/n)$ resides in the left extension field.

If $\cos(2\pi/n)$ is constructible, then the extension over $\mathbb{Q}$ by $\cos(2\pi/n)$ must be a power of 2. This along with the above observation forces $\phi(n)$ to be a power of 2, which is true exactly when $n = 2^c p_1 \cdots p_l$ where $p_i$ are distinct Fermat primes.

Conversely, suppose $n = 2^c p_1 \cdots p_l$ for some distinct Fermat primes $p_i$, so that $\phi(n)$ is a power of 2. Note that a cyclotomic extension over $\mathbb{Q}$ is Galois, and $\mathrm{Gal}(\mathbb{Q}(\zeta_n) / \mathbb{Q})$ holds the complex conjugate action $\tau$(namely $\zeta_n \mapsto \zeta_n^{-1}$) as an element. Then we have $\mathbb{Q}(\zeta_n)^{\{\mathrm{id}, \tau\}} = \mathbb{Q}(\zeta_n + \zeta_n^{-1})$ which is therefore also Galois. As a result of the previous theorem basing on the Galois theory, $\zeta_n + \zeta_n^{-1}$ is constructible if its extension degree $\phi(n)/2$ is a power of 2. Since we assumed it, we have the conclusion.
