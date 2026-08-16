Definition (topologicalKrullDim)

Let $T$ be a topological space. 
A chain of irreducible closed subsets of $T$ is a sequence $Z_0 \subset Z_1 \subset \cdots Z_n \subset T$ with $Z_i$ closed irreducible and $Z_i \ne Z_{i+1}$ for $i=0,\cdots,n-1$. 
The length of a chain $Z_0 \subset Z_1 \subset \cdots Z_n \subset T$ of irreducible closed subsets is the integer $n$.
The Krull dimension $\text{dim}(T)$ of T is the supremum of lengths of chains of irreducible closed subsets.


Let $X$, $Y$ be topological spaces.

Theorem (IsInducing.topologicalKrullDim_le)

If $f: Y \to X$ is inducing, then $\text{dim}(Y) \le \text{dim}(X)$.

proof

If $Z_0 \subset Z_1 \subset \cdots Z_n \subset X$ is a chain of irreducible closed subsets of $X$, then $f^{-1}(Z_0) \subset f^{-1}(Z_1) \subset \cdots f^{-1}(Z_n) \subset Y$ is a chain of irreducible closed subsets of $Y$.


Theorem (IsHomeomorph.topologicalKrullDim_eq)

The topological Krull dimension is invariant under homeomorphisms.

Proof

Let $f:X \to Y$ be a homeomorphism with its inverse $f^{-1}:Y \to X$. Then both $f$ and $f^{-1}$ are inducing, so we have $\text{dim}(X) \le \text{dim}(Y)$ and $\text{dim}(Y) \le \text{dim}(X)$. It follows that $\text{dim}(X) = \text{dim}(Y)$.


Theorem (topologicalKrullDim_subspace_le)

For any subspace $Y \subseteq X$, we have $\text{dim}(Y) \le \text{dim}(X)$.

Proof

Since any embedding $Y \to X$ is inducing, we have $\text{dim}(Y) \le \text{dim}(X)$.
