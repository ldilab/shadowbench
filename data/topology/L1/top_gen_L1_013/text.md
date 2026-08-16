\begin{definition}[IsLocallySurjective]
A map of presheaves \( T : \mathcal{F} \to \mathcal{G} \) is \emph{locally surjective} if for every open set \( U \), every section \( t \in \mathcal{G}(U) \), and every point \( x \in U \), there exists an open set \( V \) such that \( x \in V \subseteq U \) and a section \( s \in \mathcal{F}(V) \) such that \( T(s) = t|_V \).
\end{definition}

\begin{theorem}[locally_surjective_iff_surjective_on_stalks]
A morphism \( T : \mathcal{F} \to \mathcal{G} \) of presheaves is locally surjective if and only if for every point \( x \in X \), the induced map on stalks \( \mathcal{F}_x \to \mathcal{G}_x \) is surjective.
\end{theorem}
\begin{proof}
Suppose \( T \) is locally surjective. Let \( x \in X \) and let \( g \in \mathcal{G}_x \) be a germ. Represent \( g \) as \( \langle t, U \rangle \) for some open set \( U \subseteq X \) containing \( x \) and some section \( t \in \mathcal{G}(U) \). By local surjectivity, there exists an open set \( V \subseteq U \) containing \( x \) and a section \( s \in \mathcal{F}(V) \) such that \( T(s) = t|_V \). The germ of \( s \) at \( x \) maps to \( \langle t|_V ,V \rangle = g \), proving surjectivity on stalks.

Conversely, suppose that for every \( x \in X \), the induced map on stalks is surjective. Let \( U \subseteq X \) be an open set, \( t \in \mathcal{G}(U) \), and \( x \in U \). The germ \( t_x \) of \( t \) at \( x \) is in \( \mathcal{G}_x \), so by surjectivity, there exists a germ \( s_x \in \mathcal{F}_x \) mapping to \( t_x \). Represent \( s_x \) as \( \langle s, V \rangle \) for some open \( V \subseteq X \) containing \( x \) and some \( s \in \mathcal{F}(V) \). There exists an open set \( W \subseteq V \cap U \) containing \( x \) such that \( T(s)|_W = t|_W \). Thus, \( T \) is locally surjective.
\end{proof}
