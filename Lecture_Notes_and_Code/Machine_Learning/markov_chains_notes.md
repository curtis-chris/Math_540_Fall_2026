# Markov Chains as a Template Problem for Stochastic Sequential Data 

**Data:** $\{Y_t\}_{t=1}^{T}$ with $Y_t \in \{1, \ldots, K\}$, where $K \in \mathbb{N}$ is the "vocabulary" size and each $Y_t$ takes on the value of a particular "word".  Again, this is downstream of some tokenization process.

**Goal.** We want to sdescribe $\mathbb{P}(Y_{t}=j)$ at *time* $t$ evolves.  If we look at even one time step, we see that 

$$
\mathbb{P}(Y_{2}=j) = \sum_{l=1}^{K}\mathbb{P}(Y_{2}=j|Y_{1}=l)\mathbb{P}(Y_{1}=l). 
$$
where we have used 
$$
\mathbb{P}(X, Y) =
\begin{cases}
\mathbb{P}(X \mid Y)\, \mathbb{P}(Y) \\
\mathbb{P}(Y \mid X)\, \mathbb{P}(X),
\end{cases}
$$
to introduce the conditioning of the state $Y_{2}=j$ on the prior state at $Y_{1}$.  To go further, we need to make use of the: 

### Chain rule

Treating $(X, Y)$ given $Z$ as a whole distribution in its own right,

$$
\mathbb{P}(x, y, z) = \mathbb{P}(x, y \mid z)\, \mathbb{P}(z) = \mathbb{P}(x \mid y, z)\, \mathbb{P}(y \mid z)\, \mathbb{P}(z).
$$

**Show:**

$$
\mathbb{P}(x, y, z) = \mathbb{P}(z \mid x, y)\, \mathbb{P}(x \mid y)\, p(y).
$$

So, now if we want to describe $\mathbb{P}(Y_{3}=j)$, then we can write 

\begin{align*}
\mathbb{P}(Y_{3}=j) = & \sum_{l_{1}=1}^{K}\sum_{l_{2}=1}^{K}\mathbb{P}\left(Y_{3}|Y_{1}=l_{1},Y_{2}=l_{2}\right)\mathbb{P}\left(Y_{1}=l_{1},Y_{2}=l_{2}\right)\\
= & \sum_{l_{1}=1}^{K}\sum_{l_{2}=1}^{K}\mathbb{P}\left(Y_{3}|Y_{1}=l_{1},Y_{2}=l_{2}\right)\mathbb{P}\left(Y_{2}=l_{2}|Y_{1}=l_{1}\right)\mathbb{P}\left(Y_{1}=l_{1}\right).
\end{align*}

Following our nose, we then see for general time $t>1$, 

$$
\mathbb{P}\left(Y_{t}=j\right) = \sum_{l_{1}\cdots l_{t-1}}\mathbb{P}(Y_{t}=j| Y_{1:t-1})\mathbb{P}(Y_{t-1}|Y_{1:t-2})\cdots \mathbb{P}(Y_{2}=l_{2}|Y_{1}=l_{1})\mathbb{P}(Y_{1}=l_{1}),
$$

where $Y_{1:t} = (Y_{1},\cdots, Y_{t})$.  

---

## The Markov Assumption

Thus if we try to keep the full history of our data, then as we move forward in time, that demands using ever more complicated probability distributions conditioned on ever longer pasts.  A natural simplification then is to limit the amount of history that we track.  The most straightforward simplification that still preserves some history is:  

**Markov assumption / approximation:**

$$
\mathbb{P}(Y_t \mid Y_{1:t-1}) = \mathbb{P}(Y_t \mid Y_{t-1}).
$$

- History is encoded up to the prior step.
- Therefore,

$$
\mathbb{P}(Y_{t}=j) = \sum_{l=1}^{K}\mathbb{P}(Y_{t}=j|Y_{t-1}=l)\mathbb{P}(Y_{t-1}=l).
$$

**Stationarity:** we are talking about

$$
\mathbb{P}(Y_t = j \mid Y_{t-1} = \ell), \qquad j, \ell \in \{1, \ldots, K\}.
$$

If $Y_{1:T}$ is "stationary", then

$$
\mathbb{P}(Y_t = j \mid Y_{t-1} = \ell) = P_{j\ell},
$$

i.e. it does not depend on "time" or position in the sequence.

This reduces the problem to the Markov matrix $\mathbf{P}$ with entries $P_{j\ell}$ satisfying

$$
0 \le P_{j\ell} \le 1, \qquad \sum_{j=1}^{K} P_{j\ell} = 1,
$$

or equivalently,

$$
\sum_{j=1}^{K} \mathbb{P}(Y_t = j \mid Y_{t-1} = \ell) = 1.
$$

**Vocabulary $\to$ graph:**

:::{figure} figures/markov_graph.svg
:name: fig-markov-graph
:align: center
:width: 60%

The vocabulary as a directed graph. An edge from node $\ell$ to node $j$ carries the transition probability $P_{j\ell}$.
:::

---

## Evolving the Distribution

So now we have

$$
\begin{aligned}
\mathbb{P}(Y_2 = j, Y_1 = \ell) &= \mathbb{P}(Y_2 = j \mid Y_1 = \ell)\, \mathbb{P}(Y_1 = \ell) \\
&= P_{j\ell}\, \mathbb{P}(Y_1 = \ell),
\end{aligned}
$$

and so

$$
\mathbb{P}(Y_2 = j) = \sum_{\ell=1}^{K} P_{j\ell}\, \mathbb{P}(Y_1 = \ell).
$$

Denote

$$
\vec{\pi}_1 = \{\mathbb{P}(Y_1 = \ell)\}_{\ell=1}^{K}, \qquad
\vec{\pi}_2 = \{\mathbb{P}(Y_2 = j)\}_{j=1}^{K}.
$$

Then

$$
\vec{\pi}_2 = \mathbf{P}\, \vec{\pi}_1.
$$

**Show:**

$$
\vec{\pi}_{t+1} = \mathbf{P}^{t}\, \vec{\pi}_1, \qquad t \ge 0.
$$

---

## Equilibrium Distributions

So if $\exists\, \vec{\pi}_e$ such that

$$
\mathbf{P}\, \vec{\pi}_e = \vec{\pi}_e,
$$

then $\mathbf{P}^{t} \vec{\pi}_e = \vec{\pi}_e$, and $\vec{\pi}_e$ is called an **"equilibrium" distribution**.

- $\mathbf{P}$ has eigenvalue $1$ with eigenvector $\vec{\pi}_e$.
- Does it exist? Is it unique?

:::{prf:proof} Existence of the eigenvalue 1
For $\vec{b} = (1, 1, \ldots, 1)^{\top}$ we have $\vec{b}^{\top} \mathbf{P} = \vec{b}^{\top}$, since the columns of $\mathbf{P}$ sum to one. Hence $\lambda = 1$ is always an eigenvalue of $\mathbf{P}$.
:::

:::{prf:proof} All eigenvalues have modulus at most one
Suppose $\mathbf{P}\vec{\pi} = \lambda \vec{\pi}$. We claim $|\lambda| \le 1$. Componentwise,

$$
\lambda \pi_j = \sum_{\ell} P_{j\ell}\, \pi_\ell
\quad \Longrightarrow \quad
|\lambda|\, |\pi_j| \le \sum_{\ell} P_{j\ell}\, |\pi_\ell|.
$$

Summing over $j$,

$$
|\lambda| \sum_{j} |\pi_j|
\le \sum_{j} \sum_{\ell} P_{j\ell}\, |\pi_\ell|
= \sum_{\ell} |\pi_\ell| \underbrace{\sum_{j} P_{j\ell}}_{=\,1}.
$$

That is, $|\lambda|\, \|\vec{\pi}\|_1 \le \|\vec{\pi}\|_1$, and therefore $|\lambda| \le 1$.
:::

### Spectrum of $\mathbf{P}$

So, for $\mathbf{P} = V \Lambda V^{-1}$ (over $\mathbb{C}$):

:::{figure} figures/unit_circle_spectrum.svg
:name: fig-unit-circle-spectrum
:align: center
:width: 70%

Eigenvalues of $\mathbf{P}$ lie in the closed unit disk. The eigenvalue $\lambda = 1$ corresponds to an equilibrium distribution.
:::

- $|\lambda| < 1$: these modes decay as $\mathbf{P}^t$ iterates.
- $|\lambda| = 1$: these modes oscillate... what?
- Equilibrium distribution: one or more?

Though, let $\mathbf{P}\vec{\pi} = \lambda \vec{\pi}$ with $\lambda \ne 1$. Then

$$
\lambda \pi_j = \sum_{\ell} P_{j\ell}\, \pi_\ell
\;\Longrightarrow\;
\lambda \sum_{j} \pi_j = \sum_{j} \sum_{\ell} P_{j\ell}\, \pi_\ell
= \sum_{\ell} \pi_\ell
\;\Longrightarrow\;
\sum_{\ell} \pi_\ell = 0.
$$

---

## Detailed Balance

For a probability distribution $\{\pi_k\}_{k=1}^{K}$, **detailed balance** is the condition

$$
P_{ij}\, \pi_j = P_{ji}\, \pi_i.
$$

- The flow $j \to i$ "=" the flow $i \to j$. $\Rightarrow$ So much of chemistry.

:::{prf:proof} Detailed balance implies equilibrium
$$
\sum_{j} P_{ij}\, \pi_j = \sum_{j} P_{ji}\, \pi_i = \pi_i
\quad \Longrightarrow \quad
\mathbf{P}\,\vec{\pi} = \vec{\pi}.
$$
:::
