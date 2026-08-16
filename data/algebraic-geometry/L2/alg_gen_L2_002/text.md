\begin{theorem}[descendsAlong_isOpenImmersion_surjective_inf_flat_inf_quasicompact']
     Being an open immersion satisfies fpqc descent.
\end{theorem}
\begin{proof}
    Let $S' \to S$ be a flat surjective morphism of affine schemes, and let $f:X \to S$ be a morphism. Assume that the base change $f':X' \to S'$ is an open immersion. We claim that $f$ is an open immersion. Then $f'$ is universally open, and universally injective. Hence we conclude that $f$ is universally open, and universally injective. In particular, $f(X) \subset S$ is open. If for every affine open $U \subset f(X)$ we can prove that $f^{-1}(U) \to U$ is an isomorphism, then $f$ is an open immersion and we're done. If $U' \subset S'$ denotes the inverse image of $U$, then $U' \to U$ is a faithfully flat morphism of affines and $(f')^{-1}(U') \to U'$ is an isomorphism (as $f'(X')$ contains $U'$ by our choice of $U$). Thus we reduce to the case discussed in the next paragraph.

    Let $S' \to S$ be a flat surjective morphism of affine schemes, let $f:X \to S$ be a morphism, and assume that the base change $f':X' \to S'$ is an isomorphism. We have to show that $f$ is an isomorphism also. It is clear that $f$ is surjective, universally injective, and universally open. Hence $f$ is bijective, i.e., $f$ is a homeomorphism. Thus, $f$ is affine. Since 
    \[
        \mathcal{O}(S') \to \mathcal{O}(X') = \mathcal{O}(S') \otimes_{\mathcal{O}(S)} \mathcal{O}(X)
    \]
    is an isomorphism and since $\mathcal{O}(S) \to \mathcal{O}(S')$ is faithfully flat, this implies that $\mathcal{O}(S) \to \mathcal{O}(X)$ is an isomorphism. Thus, $f$ is an isomorphism. This finishes the proof of the claim above. 

    Therefore, an open immersion descends along an arbitrary flat surjective morphism.
\end{proof}
