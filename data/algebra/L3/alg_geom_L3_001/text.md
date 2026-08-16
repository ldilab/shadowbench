Definition (IsConstructiblePoint)

A point in $\mathbb{R}^2$ is \textbf{constructible} if a point is $(0, 0)$, or $(1, 0)$, or an intersection of two lines, a line and a circle, or two circles defined by constructible points.

Definition (IsConstructibleNumber)

We say $\alpha \in \mathbb{R}$ \textbf{constructible} if $\alpha = |P|$ for a constructible point $P$.

Definition (IsConstructibleAngle)

An angle $\theta \in \mathbb{R}$ is \textbf{constructible} if $\cos \theta$ is constructible.

Definition (ConstructibleNumbers)

The set $C$ of entire constructible numbers is a subfield of $\mathbb{R}$ including $\mathbb{Q}$. We call this set **the field of constructible numbers**.

Proof of well-definedness.

Since $O(0, 0)$ and $U(1, 0)$ are constructible, we have $0, 1 \in C$. Also, suppose $\alpha$ and $\beta$ are both constructible. Then simply drawing two circles each of radius $\alpha$ and $\beta$ and center on $(0, 0)$ and $(\alpha, 0)$ gives $(\alpha\pm\beta, 0)$ crossing with the line through $(0, 0)$ and $(1, 0)$. Thus, $C$ is closed under addition and subtraction.

To see that it is closed under multiplication and division, we again suppose $\alpha, \beta > 0$ both constructible. Now construct $V(0, 1)$, $A(\alpha, 0)$ and $B(0, \beta)$. Note that we can construct the line passing through a given point and parallel to another given line. Thus, we can also construct the points $X(\alpha\beta, 0)$ and $Y(\alpha/\beta,0)$, for $XB$ is parallel to $AU$ and $YU$ is parallel to $AB$.

Summing up the above arguments, $C$ holds $0$ and $1$, and is closed under the field operations, hence $C$ is a field.

Theorem (sqrt_constructible)

If $\alpha \ge 0$ is constructible, then so is $\sqrt{\alpha}$. (Therefore, the field of constructible numbers is quadratically closed.)

Proof.

Clearly the three points $(0, 0)$, $(-1, 0)$ and $(\alpha, 0)$ can be constructed. Now, construct the circle with $(-1, 0)$ and $(\alpha, 0)$ as the endpoints of a diameter, and then the line going through $(0, 0)$ perpendicular to the diameter line. Then the crossing points of the circle and the line have coordinate $(0, \pm \sqrt{a})$, hence comes the result.

Theorem (constructible_degree_power_2)

If $\alpha$ is a constructible number, then the extension degree $[\mathbb{Q}(\alpha) : \mathbb{Q}]$ is a power of $2$.

Proof.

Since a constructible point is a solution of system of two lines, a line and a circle, or two circles, we have that a constructible number is a root of an at most quadratic equation whose coefficients are also constructible. This is equivalent to some rational operation done to $\sqrt{d_n}$ for some $n$ where $0 < d_i \in \mathbb{Q}(\sqrt{d_1}, \cdots, \sqrt{d_{i - 1}})$ for each $i$.

From this we can take some sequence of $d_i$'s such that $\alpha \in \mathbb{Q}(\sqrt{d_1}, \cdots, \sqrt{d_r})$, where $0 < d_i \in \mathbb{R}$ is in $\mathbb{Q}(\sqrt{d_1}, \cdots, \sqrt{d_{i - 1}})$. Considering the tower
$$
\mathbb{Q} \le \mathbb{Q}(\sqrt{d_1}) \le \cdots \le \mathbb{Q} (\sqrt{d_1}, \cdots, \sqrt{d_r}),
$$
the extension degree $[\mathbb{Q}(\sqrt{d_1}, \cdots, \sqrt{d_r}) : \mathbb{Q}]$ must be a power of $2$. Since $\mathbb{Q}(\alpha)$ is an intermediate field of $\mathbb{Q}(\sqrt{d_1}, \cdots, \sqrt{d_r}) / \mathbb{Q}$, the degree $[\mathbb{Q}(\alpha) : \mathbb{Q}]$ must also be a power of $2$.

Theorem (half_angle_constructible)

For a constructible angle $\theta \in \mathbb{R}$, its half-angle $\theta/2$ is also constructible.

Proof.

Note that $\cos^2 (\theta/2) = (1 + \cos \theta) / 2$, hence $\cos(\theta/2) = \pm \sqrt{(1+\cos\theta)/2}$. Since the constructible number field is quadratically closed, we have $\sqrt{(1+\cos\theta)/2}$ constructible, hence so is the half-angle $\theta/2$.

Theorem (algebraic_of_constructible)

A constructible number $\alpha \in \mathbb{R}$ is algebraic over $\mathbb{Q}$.

Proof.

This directly comes from `constructible_degree_power_2`; since the degree of simple extension is finite, the adjoined element is algebraic.
