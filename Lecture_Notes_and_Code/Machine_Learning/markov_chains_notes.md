# Markov Chains as a Template Problem for Stochastic Sequential Data 

## Setup: Tokens and Sequences

Assuming prior tokenization, i.e.

$$
\{\vec{x}_t\} \longrightarrow \{\vec{x}'_t\}
$$

where $\{\vec{x}_t\}$ is the **data** and $\{\vec{x}'_t\}$ are the **"tokens"**, with $\vec{x}'_t \in \mathbb{R}^D$ (who knows what $D$ is?).

**Variable length:** the data are $\{\vec{x}_t\}_{t=0}^{T}$, where $T$ can be arbitrary.

**Output:** the output can depend on the task:

- **Vec-2-Seq:** $\vec{x}' \longrightarrow \{\vec{y}_t\}_{t=1}^{T}$ (generation)
- **Seq-2-Vec:** $\{\vec{x}_t\}_{t=1}^{T} \longrightarrow \vec{y}'$ (classification)
- **Seq-2-Seq:** $\{\vec{x}_t\}_{t=1}^{T} \longrightarrow \{\vec{y}_t\}_{t=1}^{T'}$, where $T = T'$ is *aligned* and $T \neq T'$ is *unaligned*.

---

## The Template Problem

**Data:** $\{Y_t\}_{t=1}^{T}$ with $Y_t \in \{1, \ldots, K\}$, where $K \in \mathbb{N}$ is the "vocabulary" size and each $Y_t$ is a "word".

Again, this is downstream of some tokenization process.

**Goal.** We want

$$
p(Y_1, \ldots, Y_T) \equiv p(Y_{1:T}) \qquad \text{(discrete probability)}.
$$

In general,

$$
p(X, Y) =
\begin{cases}
p(X \mid Y)\, p(Y) \\
p(Y \mid X)\, p(X).
\end{cases}
$$

### Chain rule

Treating $(X, Y)$ given $Z$ as a whole distribution in its own right,

$$
p(x, y, z) = p(x, y \mid z)\, p(z) = p(x \mid y, z)\, p(y \mid z)\, p(z).
$$

**Show:**

$$
p(x, y, z) = p(z \mid x, y)\, p(x \mid y)\, p(y).
$$

So,

$$
\begin{aligned}
p(Y_{1:T}) &= p(Y_1, Y_{2:T}) \\
&= p(Y_1)\, p(Y_{2:T} \mid Y_1) \\
&= p(Y_1)\, p(Y_2 \mid Y_1)\, p(Y_{3:T} \mid Y_1, Y_2) \\
&\;\;\vdots \\
&= \left( \prod_{t=2}^{T} p(Y_t \mid Y_{1:t-1}) \right) p(Y_1).
\end{aligned}
$$

---

## The Markov Assumption

But that's really hard, so we simplify:

**Markov assumption / approximation:**

$$
p(Y_t \mid Y_{1:t-1}) = p(Y_t \mid Y_{t-1}).
$$

- History is encoded up to the prior step.
- Therefore,

$$
p(Y_{1:T}) = p(Y_1) \prod_{t=2}^{T} p(Y_t \mid Y_{t-1}).
$$

**Stationarity:** we are talking about

$$
p(Y_t = j \mid Y_{t-1} = \ell), \qquad j, \ell \in \{1, \ldots, K\}.
$$

If $Y_{1:T}$ is "stationary", then

$$
p(Y_t = j \mid Y_{t-1} = \ell) = P_{j\ell},
$$

i.e. it does not depend on "time" or position in the sequence.

This reduces the problem to the Markov matrix $\mathbf{P}$ with entries $P_{j\ell}$ satisfying

$$
0 \le P_{j\ell} \le 1, \qquad \sum_{j=1}^{K} P_{j\ell} = 1,
$$

or equivalently,

$$
\sum_{j=1}^{K} p(Y_t = j \mid Y_{t-1} = \ell) = 1.
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
p(Y_2 = j, Y_1 = \ell) &= p(Y_2 = j \mid Y_1 = \ell)\, p(Y_1 = \ell) \\
&= P_{j\ell}\, p(Y_1 = \ell),
\end{aligned}
$$

and so

$$
p(Y_2 = j) = \sum_{\ell=1}^{K} P_{j\ell}\, p(Y_1 = \ell).
$$

Denote

$$
\vec{\pi}_1 = \{p(Y_1 = \ell)\}_{\ell=1}^{K}, \qquad
\vec{\pi}_2 = \{p(Y_2 = j)\}_{j=1}^{K}.
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

:::{prf:proof} All eigenvalues satisfy $|\lambda| \le 1$
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

:::{prf:proof} Detailed balance implies $\vec{\pi}$ is an equilibrium distribution
$$
\sum_{j} P_{ij}\, \pi_j = \sum_{j} P_{ji}\, \pi_i = \pi_i
\quad \Longrightarrow \quad
\mathbf{P}\,\vec{\pi} = \vec{\pi}.
$$
:::
