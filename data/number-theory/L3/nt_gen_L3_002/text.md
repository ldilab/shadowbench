\begin{definition}[LCM]
Define \(\text{LCM}(m)\) as the least common multiple of all positive integers up to a given natural number \( m \).
\end{definition}

\begin{lemma}[LCM_gt_0]
For any natural number \( m \), the least common multiple \( \text{LCM}(m) \) is greater than zero.
\end{lemma}
\begin{proof}
We unfold the definition of \( \text{LCM} \) and use logical simplifications to reduce the statement to basic properties of natural numbers. The key steps involve showing that the least common multiple cannot be zero, as it is defined over positive integers and their multiples. The simplification tactic resolves the inequality \( \text{LCM}(m) > 0 \) by verifying that zero cannot be the least common multiple of any natural number \( m \).
\end{proof}

\begin{lemma}[LCM_monotone]
For all natural numbers \( m \le n \), \( \mathrm{LCM}(m) \le \mathrm{LCM}(n) \).
\end{lemma}
\begin{proof}
We verify monotonicity by showing \( \mathrm{LCM}(n) \mid \mathrm{LCM}(n+1) \). For \( n > 0 \), the interval \( [1, n] \) is contained in \( [1, n+1] \), so the least common multiple over the larger set is divisible by the smaller one. For \( n = 0 \), we directly confirm \( \mathrm{LCM}(0) = 1 \le \mathrm{LCM}(1) = 1 \).
\end{proof}

\begin{lemma}[LCM_dvd_by]
For natural numbers \( m \) and \( n \) with \( 1 \leq m \leq n \), the product \( m \cdot \binom{n}{m} \) divides the least common multiple \( \mathrm{LCM}(1, 2, \dots, n) \). That is, \( m \cdot \binom{n}{m} \mid \mathrm{LCM}(n) \).
\end{lemma}
\begin{proof}
We begin by defining a function \( \beta'(m, n) \) as the integral \( \int_0^1 x^{m-1}(1-x)^{n-m} \, dx \), which is known to equal \( \frac{1}{m \cdot \binom{n}{m}} \). This is established using properties of the Gamma function and factorial identities.

Next, we expand \( \beta'(m, n) \) into a sum involving rational coefficients divided by integers from 1 to \( n \). This expansion is achieved by expressing the integrand as a polynomial, applying the binomial theorem, and integrating term-by-term. The result is a sum of the form \( \sum_{i=1}^n \frac{a_i}{i} \), where \( a_i \) are integers derived from binomial coefficients and powers of \( -1 \).

By equating the two expressions for \( \beta'(m, n) \), we find that \( \frac{1}{m \cdot \binom{n}{m}} = \sum_{i=1}^n \frac{a_i}{i} \). Multiplying both sides by \( m \cdot \binom{n}{m} \cdot \mathrm{LCM}(n) \), we obtain an integer linear combination of terms \( \mathrm{LCM}(n) \cdot \frac{a_i}{i} \), which are integers due to the divisibility of \( \mathrm{LCM}(n) \) by all \( i \in \{1, \dots, n\} \).

This implies that \( m \cdot \binom{n}{m} \) divides \( \mathrm{LCM}(n) \), completing the proof.
\end{proof}

\begin{lemma}[LCM_range_lower_bdd]
For all natural numbers \( m \geq 7 \), the least common multiple of the numbers from \( 1 \) to \( m \) satisfies \( \mathrm{LCM}(m) \geq 2^m \).
\end{lemma}
\begin{proof}
We proceed by case analysis on \( m \). For \( m < 9 \), we directly verify the inequality for \( m = 7 \) and \( m = 8 \) using computational checks. For \( m \geq 9 \), we consider two subcases based on the parity of \( m \).

For the odd case \( m = 2k + 1 \), we establish the inequality \( 2^{2k+2} \leq \mathrm{LCM}(2k+1) \) using properties of binomial coefficients and the fact that certain products divide \( \mathrm{LCM}(2k+1) \). Specifically, we show that \( k \cdot (k+1) \cdot \binom{2k+1}{k} \) divides \( \mathrm{LCM}(2k+1) \), and use this to derive the required bound.

For the even case \( m = 2k \), we reduce it to the odd case by showing that \( \mathrm{LCM}(2k) \geq \mathrm{LCM}(2l+1) \) for an appropriate \( l \), and then apply the previously established bound for the odd case.

The key steps involve bounding the sum of binomial coefficients, using monotonicity of the LCM function, and applying properties of divisibility and coprimality to combine bounds from multiple divisors.
\end{proof}
