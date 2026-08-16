\begin{theorem}[Decoupling inequality for the second moment]
Let $(\Omega,\mathcal{F},\mathbb{P})$ be a probability space, let
$\mathcal{F}_0\subseteq\cdots\subseteq\mathcal{F}_n\subseteq\mathcal{F}$
be a filtration, and let $d_1,\ldots,d_n$ and $e_1,\ldots,e_n$ be
square-integrable real random variables adapted to this filtration. Let
$\mathcal{G}\subseteq\mathcal{F}$ be a sigma-algebra. Assume that, for
each $1\leq i\leq n$,

1. the conditional laws of $d_i$ and $e_i$ given
   $\mathcal{F}_{i-1}$ are equal;
2. the variables $e_1,\ldots,e_n$ are conditionally independent given
   $\mathcal{G}$;
3. the conditional law of $e_i$ given $\mathcal{F}_{i-1}$ equals its
   conditional law given $\mathcal{G}$; and
4. $d_i$ and $e_i$ have the same distribution.

Then
\[
\mathbb{E}\!\left(\sum_{i=1}^{n}d_i\right)^2
\leq
2\,\mathbb{E}\!\left(\sum_{i=1}^{n}e_i\right)^2.
\]
\end{theorem}
