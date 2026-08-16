\begin{theorem}[main_theorem]
If $g(x)[e^{2y} - e^{-2y}]$ is harmonic, $g(0) = 0, g'(0) = 1$, then $g(x)=\frac{1}{2}\sin(2x).$
\end{theorem}

\begin{proof}
Let $f(x,y) = g(x)[e^{2y} - e^{-2y}]$. Then
\[
\frac{\partial^2 f}{\partial x^2} = g''(x)[e^{2y} - e^{-2y}], \qquad \frac{\partial^2 f}{\partial y^2} = 4g(x)[e^{2y} - e^{-2y}].
\]
Since $f$ is harmonic, $\Delta f = 0$ implies $g''(x) + 4g(x) = 0$, which has the general solution $g(x) = A\sin(2x) + B\cos(2x)$. 
Applying the initial conditions, $g(0) = B = 0$ and $g'(0) = 2A\cos(0) = 1$, which gives $A = 1/2$. Therefore,
\[
g(x) = \frac{1}{2}\sin(2x).
\]
\end{proof}
