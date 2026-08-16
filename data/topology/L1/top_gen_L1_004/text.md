Theorem (exists_preirreducible)

Let $X$ be a topological space. Let $S$ be a preirreducible subset of $X$. Then there exists a maximal preirreducible subset $T$ of $X$ containing $S$.

Proof

We use Zorn's Lemma. Consider the set $\mathcal{S} = \{T \subseteq X | T \text{ is preirreducible and } S \subseteq T\}$. It is nonempty since $S \in \mathcal{S}$.
If $\mathcal{C}$ is a chain of $\mathcal{S}$, we claim that $C_0:=\cup_{C \in \mathcal{C}} C$ is the upper bound of the chain $\mathcal{C}$.
It suffices to show that $C_0$ is preirreducible. Suppose $U,V$ are open subsets of $X$ such that $C_0 \cap U \ne \emptyset$, $C_0 \cap V \ne \emptyset$.
Pick $x \in C_0 \cap U$ and $y \in C_0 \cap V$. Then there exist $P,Q \in \mathcal{C}$ such that $x \in P \cap U$ and $y \in Q \cap V$.
Since $\mathcal{C}$ is a chain, we have $P \subseteq Q$ or $Q \subseteq P$.
If $P \subseteq Q$, then $Q \cap U \ne \emptyset$ and $Q \cap V \ne \emptyset$. Since $Q$ is preirreducible, $Q \cap (U \cap V) \ne \emptyset$ and thus $C_0 \cap (U \cap V) \ne \emptyset$.
Conversely, if $ Q \subseteq P$, then $P \cap U \ne \emptyset$ and $Q \cap V \ne \emptyset$. Since $P$ is preirreducible, $P \cap (U \cap V) \ne \emptyset$ and hence $C_0 \cap (U \cap V) \ne \emptyset$.
Therefore, $C_0$ is an upper bound of the chain $\mathcal{C}$. By Zorn's Lemma, $\mathcal{S}$ has the maximal element $T$ which satisfies the desired conditions.
