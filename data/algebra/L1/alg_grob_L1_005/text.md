Lemma (coeff_zero_of_lt_lm)

Let $f, g\in R[\sigma]$ be multivariate polynomials, where $\sigma$ is a set of variable symbols over which a monomial order $>$ is fixed, and $R$ is a commutative semiring. Assume $g \ne 0$ so that it attains a leading monomial. Given $\mathrm{LM}(g) > \mathrm{LM}(f)$, the coefficient of $\mathrm{LM}(g)$ in $f$ is zero.
(Technical detail: for $f = 0$, we assume $\mathrm{LM}(f)$ as `⊥ : WithBot (σ →₀ ℕ)`.)

Proof)
Since any coefficient of $f$ given $f = 0$ is zero, we might suppose $f \ne 0$, so that $f$ also attains a leading monomial. Thanks to the assumption $\mathrm{LM}(g) > \mathrm{LM}(f)$, any monomial $x^\alpha$ with nonzero coefficient in $f$ satisfies $\mathrm{LM}(g) > \mathrm{LM}(f) \ge x^\alpha$. Therefore, none of such $x^\alpha$'s equals $\mathrm{LM}(g)$, meaning that the coefficient of $\mathrm{LM}(g)$ in $f$ must be zero.
