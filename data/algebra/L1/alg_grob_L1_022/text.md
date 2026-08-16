Lemma (monomial_set_union_distrib)
Commutativity of union and monomial set

Let $F, G \subseteq R[\sigma]$ be some finite subsets of multivariate polynomials, where $\sigma$ is a set of variable symbols over which a monomial order $>$ is fixed, and $R$ is a commutative semiring. Let $\mathrm{Mon}(F)$ be the entire set of monomials in some $f \in F$. Then $\mathrm{Mon}(F) \cup \mathrm{Mon}(G) = \mathrm{Mon}(F \cup G)$.

Proof)
Denote by $\mathrm{Mon}(f)$ for $f \in R[\sigma]$ the set of monomials in $f$. Then $\mathrm{Mon}(F) = \bigcup_{f \in F} \mathrm{Mon}(f)$. Using this, we obtain
$$
\begin{aligned}
\mathrm{Mon}(F \cup G)
&= \bigcup_{f \in F \cup G} \mathrm{Mon}(f) \\
&= \bigcup_{f \in F}  \mathrm{Mon}(f) \cup \bigcup_{f \in G} \mathrm{Mon}(f) \\
&= \mathrm{Mon}(F) \cup \mathrm{Mon}(G).
\end{aligned}
$$
