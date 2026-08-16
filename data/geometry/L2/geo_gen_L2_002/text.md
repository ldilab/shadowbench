\begin{theorem}[ballRnDiffeomorph]
\begin{enumerate}
    \item[(a)] Consider the maps $F: \mathbb{B}^n \to \mathbb{R}^n$ and $G: \mathbb{R}^n \to \mathbb{B}^n$ given by
    \[
    F(x) = \frac{x}{\sqrt{1 - |x|^2}}, \qquad G(y) = \frac{y}{\sqrt{1 + |y|^2}}.
    \]

    These maps are smooth, and it is straightforward to compute that they are inverses of each other. Thus they are both diffeomorphisms, and therefore $\mathbb{B}^n$ is diffeomorphic to $\mathbb{R}^n$.
\end{enumerate}
\end{theorem}

\begin{proof}
To show that $F$ and $G$ are inverses, we first compute $|F(x)|^2$ for $x \in \mathbb{B}^n$:
\[
|F(x)|^2 = \frac{|x|^2}{1 - |x|^2}.
\]
Then, substituting $F(x)$ into $G$, we have:
\[
G(F(x)) = \frac{F(x)}{\sqrt{1 + |F(x)|^2}} = \frac{\frac{x}{\sqrt{1 - |x|^2}}}{\sqrt{1 + \frac{|x|^2}{1 - |x|^2}}} = \frac{\frac{x}{\sqrt{1 - |x|^2}}}{\sqrt{\frac{1 - |x|^2 + |x|^2}{1 - |x|^2}}} = \frac{\frac{x}{\sqrt{1 - |x|^2}}}{\frac{1}{\sqrt{1 - |x|^2}}} = x.
\]

Similarly, for $y \in \mathbb{R}^n$, we compute $|G(y)|^2$:
\[
|G(y)|^2 = \frac{|y|^2}{1 + |y|^2}.
\]
Substituting $G(y)$ into $F$, we have:
\[
F(G(y)) = \frac{G(y)}{\sqrt{1 - |G(y)|^2}} = \frac{\frac{y}{\sqrt{1 + |y|^2}}}{\sqrt{1 - \frac{|y|^2}{1 + |y|^2}}} = \frac{\frac{y}{\sqrt{1 + |y|^2}}}{\sqrt{\frac{1 + |y|^2 - |y|^2}{1 + |y|^2}}} = \frac{\frac{y}{\sqrt{1 + |y|^2}}}{\frac{1}{\sqrt{1 + |y|^2}}} = y.
\]

Next, we address smoothness:
\begin{itemize}
    \item $F$ is smooth on $\mathbb{B}^n$ because the function $|x|^2 = \sum (x^i)^2$ is smooth, and the denominator $\sqrt{1 - |x|^2}$ is smooth and strictly positive for all $|x| < 1$.
    \item $G$ is smooth on $\mathbb{R}^n$ because the denominator $\sqrt{1 + |y|^2}$ is smooth and satisfies $\sqrt{1 + |y|^2} \ge 1$ for all $y \in \mathbb{R}^n$, so it never vanishes.
\end{itemize}
Since $F$ and $G$ are smooth maps and $G = F^{-1}$, both are diffeomorphisms.
\end{proof}
