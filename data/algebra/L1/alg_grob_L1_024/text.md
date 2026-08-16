Lemma (mem_monmul_supp_iff)

Let $K[\sigma]$ be a ring of multivariate polynomials, where $\sigma$ is a set of variable symbols, and $K$ is a field. For two exponent tuples $\mu, \nu \in \mathbb{Z}_{\ge 0}^{\oplus \sigma}$, $x^\mu$ divides $x^\nu$ if and only if there exists a polynomial $f \in K[\sigma]$ such that $x^\nu$ is in $x^\mu f$.

Proof)
(==>) It suffices to take $f$ as $x^{\nu - \mu}$.
(<==) Take $f$ satisfying the assumption. Then there exists a monomial $x^\alpha$ in $f$ such that $x^\nu = x^{\alpha + \mu}$, and thus $x^\mu \mid x^{\alpha + \mu} = x^\nu$.
