Lemma (lm_add_le_of_both_lm_le_mon)
Upper bound of the leading monomial of addition

Let $f_1, f_2 \in R[\sigma]$ be multivariate polynomials (which might be zero). Here, $\sigma$ is a set of variable symbols over which a monomial order $>$ is fixed, and $R$ is a nontrivial commutative semiring. Given a monomial $x^\delta$ such that $\mathrm{LM}(f_1) \le x^\delta$ and $\mathrm{LM}(f_2) \le x^\delta$, we have $\mathrm{LM}(f_1 + f_2) \le x^\delta$.

Proof)
It suffices to take a polynomial $g \in R[\sigma]$ whose leading monomial is $\delta$. Such polynomial exists from $R \ne \{0\}$; in particular, $g$ can be taken as the monomial $cx^\delta$ for some $c \in R \setminus \{0\}$. Now we obtain the result from the same inequality for $f_1, f_2$ and $g$.
