\begin{theorem}[flat_is_open]
Let $f : X \to Y$ be a flat morphism of finite type of Noetherian schemes. Then $f$ is an open morphism.
\end{theorem}

\begin{proof}
Since openness of a morphism is local on the source and target, we may work locally on $X$ and $Y$. Thus we may assume
\[
X = \operatorname{Spec}(B), \qquad Y = \operatorname{Spec}(A),
\]
where $A$ is a Noetherian ring, $B$ is a finitely generated $A$-algebra, and $B$ is flat as an $A$-module.

We must show that the map
\[
f^\# : \operatorname{Spec}(B) \to \operatorname{Spec}(A)
\]
is open. Since principal open sets form a basis for the topology on $\operatorname{Spec}(B)$, it is enough to show that for every $g \in B$, the image of the open set
\[
D(g) \subset \operatorname{Spec}(B)
\]
is open in $\operatorname{Spec}(A)$.

Now the restriction of $f$ to $D(g)$ is again flat and of finite type. Indeed,
\[
D(g)=\operatorname{Spec}(B_g),
\]
and $B_g$ is a finitely generated flat $A$-algebra. Thus it suffices to show that the image of $\operatorname{Spec}(B)$ in $\operatorname{Spec}(A)$ is open.

Let
\[
Z = f(X) \subset \operatorname{Spec}(A).
\]
Since $f$ is of finite type, Chevalley's theorem implies that $Z$ is constructible. We will show that $Z$ is stable under generalization. Because $A$ is Noetherian, every constructible subset stable under generalization is open. Hence $Z$ will be open, as desired.

So let $\mathfrak p \subset \mathfrak q$ be prime ideals of $A$, and assume that $\mathfrak q \in Z$. We must show that $\mathfrak p \in Z$. Since $\mathfrak q \in Z$, there exists a prime ideal $\mathfrak Q \subset B$ such that
\[
\mathfrak Q \cap A = \mathfrak q.
\]

Consider the localized ring map
\[
A_{\mathfrak q} \to B_{\mathfrak q}.
\]
Because localization preserves flatness and finite type, this is again a flat ring map of finite type, with $A_{\mathfrak q}$ Noetherian. The prime $\mathfrak Q$ determines a prime of $B_{\mathfrak q}$ lying over the maximal ideal $\mathfrak q A_{\mathfrak q}$.

Now flat finite type morphisms satisfy the going-down theorem. Hence, since
\[
\mathfrak p A_{\mathfrak q} \subset \mathfrak q A_{\mathfrak q},
\]
there exists a prime ideal $\mathfrak P \subset B_{\mathfrak q}$ lying under the chosen prime over $\mathfrak q A_{\mathfrak q}$ such that
\[
\mathfrak P \cap A_{\mathfrak q} = \mathfrak p A_{\mathfrak q}.
\]
Contracting $\mathfrak P$ back to $B$, we obtain a prime ideal of $B$ lying over $\mathfrak p$. Therefore $\mathfrak p \in Z$.

Thus $Z$ is stable under generalization. Since $Z$ is constructible and $A$ is Noetherian, it follows that $Z$ is open in $\operatorname{Spec}(A)$. As noted above, the same argument applies to the image of every principal open subset $D(g)$ of $\operatorname{Spec}(B)$, and therefore $f$ is an open morphism.

This proves the theorem.
\end{proof}



\begin{corollary}[flat_open_image]
Let \(f \colon X \to Y\) be a flat morphism of finite type of Noetherian schemes. Let \(U \subset X\) be open. Then $f(U)$ is open in $Y$.
\end{corollary}

\begin{proof}
By the theorem, $f$ is open and the statement follows from the definition of open map. 
\end{proof}

\begin{theorem}[flat_morphism_complement_of_image_is_closed]
Let \(f \colon X \to Y\) be a flat morphism of schemes. Let \(U \subset X\) be open, and let
\(V = \operatorname{Spec} B \subset Y\) be an affine open subset. Then there exists an ideal
\(I \subset B\) such that
\[
V \setminus \bigl(f(U) \cap V\bigr) = V(I).
\]
\end{theorem}

\begin{proof}
By the theorem, $f(U) \cap V$ is open in $V$, and the statement follows. 
\end{proof}
