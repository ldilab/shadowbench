Definition(BuffonMeasure)

Consider the uniform probability space $[0, d] \times [0, \pi]$, where each coordinate means the midpoint position relative to the closest lower line and the angle relative to a fixed direction of the ruling respectively.

Theorem(BuffonNeedle)

Suppose a short needle of length $\ell$ is dropped onto a paper ruled with equally spaced lines of distance $d \ge \ell$. Then the probability that the needle crosses a line on the paper is $\frac{2\ell}{\pi d}$.

Proof.

Under the setting of the probability measure above, the needle crosses a line with angle $\theta$ exactly when its height $y$ of midpoint is lower than $\frac{\ell \sin \theta}{2}$ or higher than $d - \frac{\ell \sin \theta}{2}$. Thus the marginal probability for $\theta$ is $\frac{\ell \sin \theta}{d}$. Now we get the probability as the average of probability over $\theta$, namely
$$
\frac{1}{\pi} \int_0^\pi \frac{\ell \sin \theta}{d} d\theta = \frac{2\ell}{\pi d}.
$$
