---
title: "\\emoji{wtf} XAI: Lecture 17"
subtitle: "Unified Frameworks for Model Explanation"
bibliography: references.bib
header-includes:
  - \let\makesavenoteenv\relax
---

# Disclaimer

\input{../disclaimer.tex}

---

# Paper 1

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/paper1_title.png}
\end{center}

**Authors:** Ian C. Covert, Scott Lundberg, Su-In Lee

[@covert2021explaining]

---

# Motivation: Ordering the XAI Chaos

\begin{exampleblock}{} \centering There is a need for a unifying framework \end{exampleblock}
\begin{center} \includegraphics[width=0.75\columnwidth]{imgs/motivation_diagram.png} \end{center}
\vspace{0.2cm}
:::: columns 
::: {.column width="48%"} 
\begin{block}{The Problem} 
\small The field is currently a "chaos" of disparate methods (LIME, SHAP, RISE, etc.) with their own math and promises. 
\end{block} 
:::
::: {.column width="48%"} 
\begin{alertblock}{The Strategic Goal} 
\small Instead of treating methods as disjoint islands, can we find a \textbf{single mathematical framework}? 
\end{alertblock} 
::: 
::::

---

# The Feature Removal Principle

\begin{block}{Definition}
\textbf{Removal-based explanations} are model explanations that quantify the impact of removing groups of features from the model to understand their influence.
\end{block}

\vfill

\textbf{The Core Intuition:} 
Explaining is equivalent to asking a \textbf{subtractive counterfactual} question:
\begin{center}
    \textit{"How would the model's behavior change if this specific information were missing?"}
\end{center}


---

# Contributions

1. A unified framework that characterizes **26** existing explanation methods $\rightarrow$ **removal-based explanations**

2. **Mathematical tools** to represent different approaches for **removing features** from ML models

3. Removal-based explanations can be studied through **cooperative game theory** $\rightarrow$ advantages and limitations of **Shapley values** and related allocation strategies

4. Feature removal can be interpreted as **subtractive counterfactual reasoning**

5. The empirical section tests many unexplored combinations of removal, behavior, and summary choices

---


# Mathematical Formulation

\begin{block}{Notation Quick-Ref}
\small
\begin{itemize}
    \item $D = \{1, \dots, d\}$ (Indices) \quad $S \subseteq D$ (Subset)
    \item $x_S$: Observed features \quad $x_{\bar{S}}$: Removed features
\end{itemize}
\end{block}

\vfill

A supervised ML model $f$ is a mapping $f: \mathcal{X} \mapsto \mathcal{Y}$. 
To explain it by removing features, we must formalize how it behaves with incomplete data.

---

# Formalizing Feature Removal

To handle missing data, we transition from the original model $f$ to a new mathematical object.

\begin{block}{Definition 2: Subset Function}
A mapping $F: \mathcal{X} \times \mathcal{P}(D) \mapsto \mathcal{Y}$ that is \textbf{invariant} to removed features:
\begin{center}
$F(x, S) = F(x', S)$ if $x_S = x'_S$
\end{center}
\textit{Crucial property:} The output must not depend on the values of features outside of $S$.
\end{block}

\vfill

\begin{block}{Definition 3: Subset Extension}
A subset function $F$ is an extension of $f$ if it agrees with the original model when all features are present:
\begin{center}
$F(x_D) = f(x)$
\end{center}
\end{block}

\vfill
\footnotesize \centering \textit{Removing features is the act of choosing a specific subset extension $F$.}


---

# The Removal-based Explanations Framework

\begin{center}
\includegraphics[width=\textwidth]{imgs/framework_overview.png}
\end{center}

\vspace{-0.2cm}
:::: columns
::: {.column width="33%"}
\centering \textbf{\small 1. Feature removal} \\
\vspace{0.15cm}
\scriptsize $F: \mathcal{X} \times \mathcal{P}(D) \mapsto \mathcal{Y}$
:::
::: {.column width="34%"}
\centering \textbf{\small 2. Model behavior} \\
\vspace{0.15cm}
\scriptsize $u: \mathcal{P}(D) \mapsto \mathbb{R}$
:::
::: {.column width="33%"}
\centering \textbf{\small 3. Summary technique} \\
\vspace{0.15cm}
\scriptsize $E: U \mapsto \mathbb{R}^d$ \textit{or} $\mathcal{P}(D)$
:::
::::


---


# Framework Roadmap: The 3 Crucial Decisions

\begin{block}{Why these three?}
Any removal-based method is a specific combination of these independent dimensions.
\end{block}

\vfill

:::: columns
::: {.column width="33%"}
\centering
\textbf{1. Probe} \\
\textit{How to simulate "missingness"?} \\
\footnotesize $F: \mathcal{X} \times \mathcal{P}(D) \mapsto \mathcal{Y}$
:::

::: {.column width="33%"}
\centering
\textbf{2. Observe} \\
\textit{What behavior to measure?} \\
\footnotesize $u: \mathcal{P}(D) \mapsto \mathbb{R}$
:::

::: {.column width="33%"}
\centering
\textbf{3. Condense} \\
\textit{How to handle $2^d$ subsets?} \\
\footnotesize $E: U \mapsto \mathbb{R}^d / \mathcal{P}(D)$
:::
::::

\vfill

\begin{exampleblock}{Strategic Insight}
Decisions 1 \& 2 define the \textbf{counterfactual question}. Decision 3 makes the answer \textbf{interpretable} for humans.
\end{exampleblock}

---

# Defining Feature Removal

$$F(x) = f(\text{features\_to\_keep},\ \text{features\_to\_remove})$$

- **Zero ablation** $\quad F(x_S) = f(x_S, 0)$
- **Default values** $\quad F(x_S) = f(x_S, r_{\bar{S}})$
- **Generative model** $\quad F(x_S) = f(x_S, \tilde{x}_{\bar{S}})$
- **Train separate models**
  - Train surrogate models
- **"Missingness" during training**

\begin{alertblock}{}
The removal operator defines the counterfactual question. Replacing with zero, a baseline, or a conditional sample are not equivalent.
\end{alertblock}

---

# Defining Feature Removal (cont)

**Marginalization**

- **Marginalize with conditional** $\quad F(x_S) = \mathbb{E}[f(X) \mid X_S = x_S]$
  - Tree distribution
- **Marginalize with marginal** $\quad F(x_S) = \mathbb{E}[f(x_S, X_{\bar{S}})]$
- **Marginalize with product of marginals** $\quad F(x_S) = \mathbb{E}_{\prod_{i \in D} p(X_i)}[f(x_S, X_{\bar{S}})]$
- **Marginalize with uniform** $\quad F(x_S) = \mathbb{E}_{\prod_{i \in D} u_i(X_i)}[f(x_S, X_{\bar{S}})]$
- **Marginalize with replacement distribution** $\quad F(x, S) = \mathbb{E}_{\prod_{i \in D} q_{x_i}(X_i)}[f(x_S, X_{\bar{S}})]$

\vspace{0.3cm}

\begin{block}{Key point}
Conditional removal keeps missing features plausible given the observed features; marginal removal can break feature dependencies.
\end{block}

---


# Explaining Model Behaviors

Given the newly defined model $F(x_S)$, we need a metric to assess how important the $x_S$ features are.

**Options:**

| Behavior | Formula |
|----------|---------|
| Prediction | $F(x_S)$ |
| Prediction loss | $-\ell(F(x_S), y)$ |
| Prediction mean loss | $-\mathbb{E}_{p(Y \mid X=x)}\left[\ell(F(x_S), Y)\right]$ |
| Dataset loss | $-\mathbb{E}_{XY}\left[\ell(F(X_S), Y)\right]$ |
| Prediction loss w.r.t. output | $-\ell(F(x_S), F(x))$ |
| Dataset loss w.r.t. output | $-\mathbb{E}_X\left[\ell(F(X_S), F(X))\right]$ |

\vspace{0.2cm}

\begin{block}{}
"Feature importance" is incomplete until we say: important for prediction, loss, global performance, or fidelity to the full model?
\end{block}

---

# Unified View: Relations Between Behaviors

All behavior functions ($u$) are derived from the basic subset prediction $u_x(S)$.

\begin{block}{The Mathematical Hierarchy}
\begin{itemize}
    \item \textbf{Prediction loss:} $v_{xy}(S) = -\ell(u_x(S), y)$
    \item \textbf{Dataset loss:} $v(S) = \mathbb{E}_{XY} [v_{XY}(S)]$
    \item \textbf{Fidelity (output loss):} $w_x(S) = -\ell(u_x(S), u_x(D))$
\end{itemize}
\end{block}

\vfill
\begin{exampleblock}{Key Insight}
Explanations based on one set function are expectations of another. For instance, \textbf{SAGE} (global) is the expected value of \textbf{LossSHAP} (local).
\end{exampleblock}


---


# Summarizing Feature Influence

Two related approaches:

- **Map feature to real number value (feature attribution)** $\quad E: \mathcal{U} \rightarrow \mathbb{R}^d$
- **Map dataset to a set of important features (feature selection)** $\quad E: \mathcal{U} \rightarrow \mathcal{P}(D)$

Both are related; often the second is just a threshold applied to the first.

\begin{center}
\includegraphics[width=0.5\columnwidth]{imgs/summarizing_influence.png}
\end{center}


---

# Summary Techniques: A Closer Look

\begin{block}{Taxonomy of Summaries}
\small
\begin{itemize}
    \item \textbf{Local Attribution:} Shapley (fairness), LIME (additive), RISE (mean included).
    \item \textbf{Local Selection:} Optimization-based (L2X, INVASE).
    \item \textbf{Global Equivalence:} Selection on dataset loss $\equiv$ Classical Feature Selection.
\end{itemize}
\end{block}


---

# Computational Complexity & Approximations

\vspace{0.5cm}
\begin{block}{The Exponential Wall}
Calculating exact summaries (like Shapley values) requires examining all $2^d$ subsets, making it intractable for $d > 20$.
\end{block}

:::: columns
::: {.column width="55%"}
\textbf{How to bypass this?}
\small
\begin{itemize}
    \item \textbf{Sampling:} Estimate expected values via Monte Carlo (e.g., IME, SAGE).
    \item \textbf{Structural:} Exploit model properties (e.g., DP in \textbf{TreeSHAP}).
    \item \textbf{Optimized Search:} Greedy algorithms (e.g., \textbf{MIR}).
    \item \textbf{Amortized Models:} Second "explainer" model (\textbf{L2X, REAL-X}).
\end{itemize}
:::

::: {.column width="45%"}
\begin{center}
    \includegraphics[width=\textwidth]{imgs/computational_complexity.png}
\end{center}
\centering \scriptsize \textit{KernelSHAP ($2^d$) vs. TreeSHAP (Linear)}
:::
::::

\vfill
\begin{alertblock}{Key Insight}
Approximations change what "missing" means. If the surrogate or generator is wrong, the explanation inherits that error.
\end{alertblock}

---

# Methods Survey: The XAI Landscape

\begin{center}
    % Aumentamos el height al 75% de la slide para que sea bien grande
    \includegraphics[height=0.75\textheight, keepaspectratio]{imgs/methods_survey_table.png}
\end{center}

\centering \footnotesize \textit{Each method is a unique combination of removal, behavior, and summary choices.}


---


# Methods Survey: Key Insights

\vfill

\begin{block}{1. The "Standard" Family}
The most common path is marginalizing removed features using their \textbf{conditional distribution} combined with \textbf{Shapley values}.
\end{block}

\vfill

\begin{block}{2. Unique Approaches}
Methods like \textbf{RISE}, \textbf{LIME (tabular)}, and \textbf{INVASE} are "isolated" in the grid because they make very specific, non-standard choices in how they remove or summarize information.
\end{block}

\vfill

\begin{alertblock}{3. The Opportunity}
The grid reveals many "empty squares": combinations of removal and behavior that \textbf{no one has tested yet}.
\end{alertblock}

\vfill


---


# XAI as a Cooperative Game

To provide a fair summary, we map the machine learning problem into the language of Cooperative Game Theory.

\begin{block}{The Mapping (Definitions)}
\begin{itemize}
    \item \textbf{Players ($i$):} The features of the model ($D = \{1, \dots, d\}$).
    \item \textbf{Coalition ($S$):} Any subset of features ($S \subseteq D$).
    \item \textbf{Value Function ($u(S)$):} The chosen model behavior (Prediction, Loss, etc.).
    \item \textbf{Marginal Contribution:} The change in value when a player joins a coalition: $u(S \cup \{i\}) - u(S)$.
\end{itemize}
\end{block}

\vfill
\begin{exampleblock}{Goal of the Game}
Find an \textbf{allocation} $a \in \mathbb{R}^d$ (attribution scores) that distributes the total value of the "grand coalition" $u(D)$ among the players.
\end{exampleblock}


---


# Shapley Values: Axiomatic Foundations

Shapley values are the \textbf{unique} allocations that satisfy five fundamental axioms of fairness.

\begin{block}{The 5 Pillars of Fair Credit Allocation}
\small
\begin{itemize}
    \item \textbf{Efficiency:} The total value $u(D) - u(\emptyset)$ is fully distributed.
    \item \textbf{Symmetry:} Identical players receive identical allocations.
    \item \textbf{Dummy:} Players with zero marginal contribution receive zero.
    \item \textbf{Additivity:} The summary of a sum of games is the sum of their summaries.
    \item \textbf{Marginalism:} Allocations depend only on marginal contributions.
\end{itemize}
\end{block}

\begin{block}{Mathematical Expression (Eq. 33)}
$$\phi_i(u) = \frac{1}{d} \sum_{S \subseteq D \setminus \{i\}} \binom{d-1}{|S|}^{-1} [u(S \cup \{i\}) - u(S)]$$
\end{block}

\centering \footnotesize \textit{This is the only "fair" way to account for complex interactions.}


---


# Banzhaf Values & Coalitional Excess

While Shapley is the "standard," other game-theoretic concepts explain methods like RISE or L2X.

\begin{block}{Banzhaf Value (Alternative Attribution)}
Instead of permutations, it averages marginal contributions over all \textbf{subsets}:
$$\psi_i(u) = \frac{1}{2^{d-1}} \sum_{S \subseteq D \setminus \{i\}} (u(S \cup \{i\}) - u(S))$$
\textit{Key connection:} The \textbf{RISE} method is a modified version of this value.
\end{block}

\vfill

\begin{block}{Definition 4: Coalitional Excess}
For an allocation $z$ and coalition $S$, the excess measures "unhappiness":
$$e(S, z) = u(S) - \sum_{i \in S} z_i$$
\end{block}

\vfill
\centering \footnotesize \textit{Feature Selection methods (L2X, INVASE) are equivalent to maximizing this excess.}


---

# Game Theory: Modeling via Kernels

Many attribution methods fit an additive model $\sum a_i z_i \approx u(S)$ by solving a \textbf{Weighted Least Squares} game:
$$\min_{a} \sum_{S \subseteq D} \pi(S) (u(S) - (a_0 + \sum_{i \in S} a_i))^2$$

\begin{block}{The Choice of Kernel $\pi(S)$ Determines the Method}
\small
\begin{itemize}
    \item \textbf{Shapley Kernel ($\pi_{Sh}$):} Recovers Shapley values (used by \textbf{KernelSHAP}).
    \item \textbf{Banzhaf Kernel ($\pi = 1$):} Recovers Banzhaf values (unweighted WLS).
    \item \textbf{Exclusion Kernel ($\pi_{Rem}$):} Weight only on $d-1$ subsets $\rightarrow$ \textbf{Occlusion, LOCO}.
    \item \textbf{Inclusion Kernel ($\pi_{Inc}$):} Weight only on size $1$ subsets $\rightarrow$ \textbf{Univariate Predictors}.
\end{itemize}
\end{block}

\centering \footnotesize \textit{LIME is a flexible framework where the kernel choice defines the counterfactual logic.}


---


# Selection: The Concept of Coalitional Excess

For selection methods (L2X, MM), importance is defined by the \textbf{Excess}: the "unhappiness" of a coalition $S$ under allocation $z$:
$$e(S, z) = u(S) - \sum_{i \in S} z_i$$

\begin{block}{Optimization Objectives in the Literature}
\small
\begin{itemize}
    \item \textbf{Minimize Excess (MP):} Finds a low-value coalition $S$ whose complement is most "satisfied" with the allocation.
    \item \textbf{Maximize Excess (L2X, MIR, EP):} Finds the "star team" (coalition of size $k$) with the highest degree of dissatisfaction.
    \item \textbf{Maximize Difference (MM):} Partitions features into a dissatisfied set $S$ and a satisfied complement $\bar{S}$ (Generalizes all other methods).
\end{itemize}
\end{block}

\centering \footnotesize \textit{Feature selection is game theory focused on group power rather than individual credit.}


---


# Information Theory: Consistent Feature Removal

To have a valid information-theoretic interpretation, we must remove features **consistently** with the data distribution $p(x)$.

\begin{block}{The Only Proper Way}
Marginalizing features using their \textbf{conditional distribution} is the \textbf{only} approach consistent with standard probability axioms (Countable Additivity and Bayes' Rule).
\end{block}

\vspace{0.3cm}
**The Result:**
If the model $f$ is optimal, then for any subset of features $S$:
\begin{center}
$F(x_S) = p(Y \mid X_S = x_S)$ (Classification) \\
$F(x_S) = \mathbb{E}[Y \mid X_S = x_S]$ (Regression)
\end{center}

\vfill
\footnotesize \centering \textit{Removing features properly means choosing a subset extension $F$ that behaves like a partial conditional distribution.}


---


# Intuition: Information as Uncertainty Reduction

Under proper removal, explanation methods quantify the **information communicated** by each feature.

:::: columns
::: {.column width="48%"}
\begin{block}{Key Concepts}
\small
\begin{itemize}
    \item \textbf{Entropy $H(Y)$:} Initial uncertainty about the target label.
    \item \textbf{Mutual Info $I(X_S; Y)$:} How much $x_S$ reduces that uncertainty.
\end{itemize}
\end{block}
:::
::: {.column width="48%"}
\begin{exampleblock}{Pointwise Mutual Info}
\small
Quantifies how much \textbf{less surprising} a specific outcome $y$ is given knowledge of $x_S$:
$$v_{xy}(S) = I(y; x_S) + c$$
\end{exampleblock}
:::
::::

\vspace{0.5cm}
\centering \textbf{A feature is "important" if observing it narrows down the possible values of the label.}


---

# Information Theory Quantities

\small
| Model Behavior | Set Function | Methods | Information Quantity |
| :--- | :--- | :--- | :--- |
| Prediction | $u_x$ | SHAP, LIME, etc. | **Cond. Prob / Expectation** |
| Prediction loss | $v_{xy}$ | LossSHAP, CXPlain | **Pointwise Mutual Info** |
| Pred. mean loss | $v_x$ | INVASE | **KL Divergence** (with true $p$) |
| Dataset loss | $v$ | SAGE, Permutation | **Mutual Information** (with label) |
| Pred. loss (output)| $w_x$ | L2X, REAL-X | **KL Divergence** (with full $f$) |
| Dataset loss (out) | $w$ | Shapley Effects | **Mutual Information** (with output) |

\vfill

\begin{alertblock}{Crucial Assumptions} 
These links require: (1) \textbf{Conditional removal} and (2) \textbf{Model optimality} (i.e., $f$ approximates the Bayes classifier).
\end{alertblock}
\vspace{0.4cm}


---


# Warning: Information $\neq$ Mechanism


Information-theoretic importance captures **intrinsic statistical relationships** in the data.

\begin{alertblock}{The "Proxy" Attribute Problem}
A feature can appear important even if the model does not use it \textbf{functionally} (e.g., if it's a proxy for a sensitive attribute like race or gender).
\end{alertblock}

\vfill
:::: columns
::: {.column width="48%"}
\textbf{Statistical Perspective}
- Detects hidden influences (bias).
- "What info does $X_i$ provide?"
:::
::: {.column width="48%"}
\textbf{Mechanistic Perspective}
- How does the model calculate?
- Requires causal interventions.
:::
::::

\vfill
\centering \footnotesize \textit{Conditional removal guarantees that perfectly correlated features receive equal attributions.}


---


# Conditional Distribution Approximations

Since the true conditional distribution $p(x_{\bar{S}} \mid x_S)$ is usually unknown, we must approximate it.

\begin{block}{Group 1: Distribution Assumptions}
\small
\begin{itemize}
    \item \textbf{Feature Independence:} Assumes $p(x_{\bar{S}} \mid x_S) \approx p(x_{\bar{S}})$. Used by \textbf{KernelSHAP} and \textbf{QII}.
    \item \textbf{Model Linearity:} Justifies replacing features with their mean: $F(x_S) \approx f(x_S, \mathbb{E}[x_{\bar{S}}])$. Used by \textbf{LIME} or \textbf{Occlusion}.
    \item \textbf{Parametric Assumptions:} Assumes data follows a specific distribution (e.g., Multivariate Gaussian).
\end{itemize}
\end{block}

\vfill
\centering \footnotesize \textit{Independence is a "rough" approximation; parametric models are better but can still be biased.}


---


# Approximating via Learned Models

More advanced methods learn the distribution or the behavior directly.

:::: columns
::: {.column width="48%"}
\begin{block}{Group 2: Learned Models}
\small
\begin{itemize}
    \item \textbf{Generative Models:} Use a conditional GAN (\textbf{FIDO-CA}) to sample plausible missing values.
    \item \textbf{Surrogate Models:} Train a separate model $F(x_S)$ to match the original $f$ output. (\textbf{L2X}, \textbf{REAL-X}).
\end{itemize}
\end{block}
:::
::: {.column width="48%"}
\begin{exampleblock}{The Gold Standard}
\small
\textbf{Separate Models:} Training a different model for \textit{every} subset $S$. Perfect approximation, but \textbf{computationally impossible} for $d > 20$.
\end{exampleblock}
:::
::::

\vspace{0.4cm}
\begin{alertblock}{Fidelity Risk}
The explanation inherits the error of the approximation. If the surrogate or generator is biased, the attribution will be too.
\end{alertblock}


---


# Cognitive Basis: Subtractive Counterfactuals

Explaining a model is fundamentally a **causality question**: "What makes the model behave this way?".

\begin{block}{The Method of Difference (John Stuart Mill)}
Human induction relies on changing facts of a situation to see if the outcome changes.
\end{block}

\vspace{0.4cm}
**Subtractive Counterfactual Reasoning:**
- In psychology, this is the process of **removing an event** to understand its influence.
- This is precisely what removal-based XAI does: it subtracts the fact that a feature was observed.

\vfill
\centering \textbf{Removal-based explanations are intuitive because they match how humans discuss causes in daily life.}


---


# Norm Theory and the "Downhill Rule"

How do we decide what to use as a "replacement" for a removed feature?

:::: columns
::: {.column width="48%"}
\begin{block}{Norm Theory}
\small
We assess "normality" by averaging outcomes over simulated representations where some features are fixed (\textbf{immutable}) and others vary (\textbf{mutable}).
\end{block}
:::
::: {.column width="48%"}
\begin{exampleblock}{The Downhill Rule}
\small
People assign "blame" to a feature if it has a \textbf{more likely alternative} that would have changed the outcome.
\end{exampleblock}
:::
::::

\vfill
\begin{alertblock}{The Cognitive Link to Math}
These theories justify removing features by \textbf{averaging over their conditional distribution}: we compare the current "surprising" state against a "normal" alternative.
\end{alertblock}


---


# Cognitive Trade-off: Simplicity vs. Completeness

There is a fundamental conflict between the amount of info conveyed and the user's cognitive load.

\begin{center} 
\includegraphics[width=0.85\columnwidth]{imgs/cognition_theory.png} 
\end{center}

\vspace{0.2cm}
**The Complexity Risk:**
- Detailed summaries (like SHAP) provide rich info but can lead to **misunderstanding** or high cognitive load.
- Simpler explanations are more accessible but may fail to convey the model's full nuance.

\vfill
\centering \footnotesize \textit{Users are less likely to draw correct conclusions if an explanation requires too much time or effort.}


---


# Strategic Design: The Explanation Spectrum

The framework provides the flexibility to balance simplicity and completeness according to the user's needs.

\vspace{0.4cm}
\begin{block}{The Spectrum of Choice}
\begin{enumerate}
    \item \textbf{Global Selection:} Simplest, identifying only key features for the whole model.
    \item \textbf{Local Selection:} Moderate, showing features relevant to a specific case.
    \item \textbf{Local Attribution:} Most complete, quantifying every feature's influence (e.g., SHAP).
\end{enumerate}
\end{block}

\vfill
\begin{exampleblock}{Strategic Insight}
XAI designers must tailor explanations. Sometimes, explaining a \textbf{group of features} is better than individual attributions to reduce mental burden.
\end{exampleblock}

---


# Experiments: Methods Survey

\begin{center} \includegraphics[height=0.60\textheight, keepaspectratio]{imgs/methods_survey_table.png} \end{center}
\begin{exampleblock}{The Authors' Insight} 
\footnotesize \textbf{Look at the gaps!} The grid reveals dozens of unexplored combinations. Most existing methods are just a tiny cluster in a much larger space. 
\end{exampleblock}

\vfill
\centering \scriptsize \textit{Colors indicate different model behaviors: \textcolor{blue}{Prediction}, \textcolor{red}{Loss}, \textcolor{green}{Dataset Loss}.}


---


# Experimental Domains & Tasks

The framework was tested across three diverse domains to verify the consistency of the 80 methods.

:::: columns
::: {.column width="32%"}
\begin{center}
\includegraphics[height=2.2cm]{imgs/census_icon.png}
\end{center}
\centering \textbf{Census Income}
\vspace{0.1cm}
\small
\begin{itemize}
    \item 48,842 individuals
    \item 12 socioeconomic features
    \item \textbf{Goal:} $y > \$50k$ income
    \item \textbf{Model:} Light-GBM
\end{itemize}
:::

::: {.column width="32%"}
\begin{center}
\includegraphics[height=2.2cm]{imgs/mnist_icon.png}
\end{center}
\centering \textbf{MNIST Digits}
\vspace{0.1cm}
\small
\begin{itemize}
    \item 70,000 digits
    \item $32 \times 32$ grayscale pixels
    \item \textbf{Goal:} Prediction \textbf{loss}
    \item \textbf{Model:} 14-layer CNN
\end{itemize}
:::

::: {.column width="32%"}
\begin{center}
\includegraphics[height=2.2cm]{imgs/breast_icon.png}
\end{center}
\centering \textbf{Breast Cancer}
\vspace{0.1cm}
\small
\begin{itemize}
    \item 510 patients
    \item 100/17,814 genes
    \item \textbf{Goal:} \textbf{Dataset loss}
    \item \textbf{Model:} Logistic Reg.
\end{itemize}
:::
::::

\vfill
\centering \footnotesize \textit{Dimensionality varies from simple tabular data to high-dimensional image and genomic data.}


---

# Experimental Setup: Mix & Match

 **80 methods** (68 new) implemented by combining choices across the three framework dimensions.

:::: columns
::: {.column width="31%"}
\begin{block}{1. Removal ($F$)}
\small
\begin{itemize}
    \item Default Values
    \item \textbf{Marginalization:}
    \begin{itemize}
        \item Uniform
        \item Product
        \item Joint Marginal
    \end{itemize}
    \item \textbf{Surrogate} (Cond. approx)
\end{itemize}
\end{block}
:::

::: {.column width="31%"}
\begin{block}{2. Behavior ($u$)}
\small
\begin{itemize}
    \item \textbf{Prediction} (Census)
    \item \textbf{Prediction Loss} (MNIST)
    \item \textbf{Dataset Loss} (BRCA)
\end{itemize}
\end{block}
:::

::: {.column width="31%"}
\begin{block}{3. Summary ($E$)}
\small
\begin{itemize}
    \item Remove Individual
    \item Include Individual
    \item Mean when Included
    \item Banzhaf Value
    \item \textbf{Shapley Value}
\end{itemize}
\end{block}
:::
::::

\vfill
\centering \footnotesize \textit{This grid allows us to fill the "empty squares" of the XAI landscape.}


---

# Census Income: Qualitative Analysis

:::: columns
::: {.column width="58%"}
\begin{center}
\includegraphics[width=\textwidth, height=0.80\textheight, keepaspectratio]{imgs/census_income_results_full.png}
\end{center}
:::
::: {.column width="40%"}
\vspace{0.1cm}
\begin{block}{Objective}
\scriptsize Compare 30 explanation methods for a single prediction (Income < 50k).
\end{block}

\begin{block}{1. Removal Impact}
\scriptsize Bottom rows are consistent as they approximate the conditional distribution.
\end{block}

\begin{block}{2. Summary Impact}
\scriptsize Shapley and Banzhaf are similar. \textit{Mean when Included} is the outlier.
\end{block}
:::
::::


---


# Census Income: Similarity Analysis


\small We group methods to observe how removal and summary decisions affect the final explanation.

\begin{center}
\includegraphics[height=0.48\textheight, keepaspectratio]{imgs/census_income_correlation_1.png}
\end{center}

\vspace{-0.2cm}
\begin{block}{Interpreting the Similarity Heatmaps}
\scriptsize
\begin{itemize}
    \item \textbf{Summary (Left):} Shapley and Banzhaf values are very similar (probabilistic values).
    \item \textbf{Removal (Right):} Methods approximating the conditional distribution tend to cluster together.
    \item \textbf{Finding:} The removal strategy can be as influential as the attribution logic.
\end{itemize}
\end{block}

---

# Census Income: Fidelity Boxplots

Quantifying how well each approximation matches the "Ground Truth" (Separate Models).

\begin{center} 
\includegraphics[height=0.55\textheight, keepaspectratio]{imgs/census_income_correlation_2.png} 
\end{center}

\vspace{-0.1cm}
\begin{exampleblock}{Key Finding: Surrogate Performance}
\small
The \textbf{Surrogate Removal} method is the most faithful proxy for the true conditional distribution (highest correlation, lowest MSE), although it is prone to occasional outliers.
\end{exampleblock}


---

# MNIST: Visualizing Prediction Loss

Heatmaps showing which pixels help (red) or hurt (blue) the model's loss.

:::: columns
::: {.column width="53%"}
\begin{center}
\includegraphics[width=\textwidth, height=0.7\textheight, keepaspectratio]{imgs/mnist_qualitative.png}
\end{center}
:::
::: {.column width="45%"}
\vspace{0.4cm}
\begin{block}{Key Observations}
\scriptsize
\begin{itemize}
    \item \textbf{Noise:} Uniform and Product strategies often produce noisy explanations.
    \item \textbf{Blind Spots:} In \textit{Default Values}, zero-valued pixels always receive zero attribution (which is not ideal).
\end{itemize}
\end{block}

\begin{exampleblock}{The Winner: LossSHAP}
\scriptsize \textbf{Surrogate + Shapley} provides the cleanest features and highlights key distinguishing regions (e.g., the top space of the 4).
\end{exampleblock}
:::
::::

---

# MNIST: Insertion & Deletion Metrics

Evaluating explanations by adding/removing features according to their rank.

:::: columns
::: {.column width="55%"}
\begin{center} 
\includegraphics[width=\textwidth]{imgs/mnist_quantitative.png} 
\end{center}
:::
::: {.column width="43%"}
\small
**Insertion (Lower area is better):**
How fast does the model "see" the digit as we add key features?

**Deletion (Higher area is better):**
How fast does the model "blind" if we remove key features?
:::
::::

\vspace{0.2cm}
\begin{alertblock}{The "Evaluation Bias" Warning}
Metrics are not neutral! If a metric uses \textbf{zeros} to remove features, it will favor explanation methods that also use \textbf{zeros}.
\end{alertblock}


---

# Breast Cancer: Global Gene Importance

\small \centering Explaining \textbf{dataset loss} to identify key genes in cancer.

\vspace{0.2cm}
:::: columns
::: {.column width="55%"}  
\begin{center}
\includegraphics[width=\textwidth, height=0.75\textheight, keepaspectratio]{imgs/breast_cancer_qualitative.png}
\end{center}
:::
::: {.column width="43%"} 
\vspace{1.2cm}
\begin{block}{Consensus}
\scriptsize Most methods identify \textbf{ESR1} as the primary influence on cancer molecular subtypes.
\end{block}
:::
::::

---


# BRCA: Quantitative Feature Selection

Evaluating methods by training new models with only the top-ranked $n$ genes (insertion-style metric).

:::: columns
::: {.column width="55%"}
\begin{center} 
\includegraphics[width=\textwidth]{imgs/breast_cancer_quantitative.png} 
\end{center}
:::
::: {.column width="43%"}
\begin{exampleblock}{Key Result: SAGE}
\small
The combination of \textbf{Surrogate + Shapley} (which corresponds to \textbf{SAGE}) performs best, achieving the lowest average cross-entropy loss.
\end{exampleblock}

\vspace{0.2cm}
**Scientific Impact:**
Global explanations like these can generate new hypotheses for laboratory testing by identifying genes with high predictive power.
:::
::::

\vfill
\centering \footnotesize \textit{SAGE authors originally suggested conditional removal, but the surrogate approximation makes it scalable to high-dimensional genomic data.}

---

# Paper 1 Summary: Successes & Open Challenges

The unified framework systematizes the XAI landscape, showing that 26+ methods are just different "recipes" of the same three choices.

:::: columns
::: {.column width="48%"}
\begin{block}{Key Successes}
\small
\begin{itemize}
    \item \textbf{The Winner:} Surrogate + Shapley (\textbf{LossSHAP/SAGE}) provides the most faithful results.
    \item \textbf{Theoretical Foundation:} Explanations are now anchored in \textbf{Game Theory} and \textbf{Info Theory}.
\end{itemize}
\end{block}
:::
::: {.column width="48%"}
\begin{alertblock}{Critical Limitations}
\small
\begin{itemize}
    \item \textbf{Information $\neq$ Mechanism:} Features can appear important just by being \textbf{proxies}.
    \item \textbf{Evaluation Bias:} Metrics favor methods that "remove" features the same way they do.
\end{itemize}
\end{alertblock}
:::
::::

\vfill
\begin{exampleblock}{Final Synthesis}
\centering \small \textit{Removal-based XAI makes modeling decisions visible. There is no "neutral" explanation; every method is a specific counterfactual question.}
\end{exampleblock}

---

# Discussion (Paper 1)

- Are removal-based the right framework to go in XAI?
- How do we reconcile with the fact that removing features may result in out-of-distribution behavior?
- What other unifying frameworks can you think of?
- Do you agree with the assessment that SHAP provides the best explanation?
- What methods do not fall under removal-based methods?

---

# Paper 2

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/paper2_title.png}
\end{center}

**Authors:** Tessa Han, Suraj Srinivas, Himabindu Lakkaraju

[@han2022which]


---

# The Disagreement Problem


\vspace{0.1cm}
\begin{block}{The Practical Challenge}
\small Different methods generate contradictory explanations for the same prediction, undermining trust.
\end{block}

\vspace{0.1cm}
\centering \textbf{8 Popular Methods to Unify:}
\vspace{0.1cm}

:::: columns
::: {.column width="45%"}
\footnotesize \centering
\begin{itemize}
    \item LIME / C-LIME
    \item \textbf{KernelSHAP}
    \item Occlusion
\end{itemize}
:::
::: {.column width="45%"}
\footnotesize \centering
\begin{itemize}
    \item Vanilla Gradients
    \item SmoothGrad / IG
    \item Gradient $\times$ Input
\end{itemize}
:::
::::

\vfill
\begin{exampleblock}{The Function Approximation Perspective}
\small Disagreement stems from using different \textbf{Neighborhoods} and \textbf{Loss Functions} in LFA.
\end{exampleblock}

---

# Summary of Key Contributions.

The LFA framework provides a principled way to understand and select among disparate XAI methods.

\begin{enumerate}
    \item \textbf{Unification:} We show that 8 popular methods (LIME, SHAP, SmoothGrad, etc.) are all instances of \textbf{Local Function Approximation (LFA)}, differing only in neighborhood and loss.
    \item \textbf{No Free Lunch Theorem:} We prove that no single explanation method can perform optimally across all neighborhoods.
    \item \textbf{Guiding Principle (Model Recovery):} We define that an effective method must recover the black-box model when both are in the same model class.
    \item \textbf{Empirical Validation:} We validate these theoretical results across real-world datasets (WHO, HELOC) and diverse model architectures.
\end{enumerate}

\vfill
\centering \footnotesize \textit{This framework transforms XAI selection from personal preference into a mathematical decision.}

---

# LFA: A Unified Recipe for XAI

An explanation $g^*$ is the model that minimizes the difference with $f$ in a specific neighborhood.

\begin{equation}
g^* = \arg \min_{g \in \mathcal{G}} \mathbb{E}_{\xi \sim \mathcal{Z}} \ell(f, g, \mathbf{x}_0, \xi)
\end{equation}

\vspace{0.4cm}
**To design any explanation, you only need 4 choices:**
1. \textbf{Model Class ($\mathcal{G}$):} Usually linear models ($g(x) = w^T x$).
2. \textbf{Neighborhood ($\mathcal{Z}$):} The distribution of perturbations (noise).
3. \textbf{Loss Function ($\ell$):} Measures faithfulness (e.g., Squared Error).
4. \textbf{Operator ($\oplus$):} How noise combines with input (Additive vs. Multiplicative).

\vfill
\begin{block}{The Faithfulness Condition}
\small
A loss $\ell$ is valid only if $\mathbb{E} \ell = 0 \iff f(x_\xi) = g(x_\xi)$. This ensures the explanation is strictly \textbf{faithful} to the model in that neighborhood.
\end{block}

---

# Distinction with LIME

The LFA framework is a formalization of the perspective introduced by LIME, but it differs from the algorithm in three fundamental ways:

\begin{enumerate}
    \item \textbf{Domain Consistency:} LFA requires that $f$ and $g$ share the same input domain $\mathcal{X}$. Using a binary model $g$ to explain a continuous model $f$ (as LIME often does) is not true function approximation.
    \item \textbf{Model Recovery:} LFA imposes conditions on the loss function to ensure that $g^*$ exactly recovers $f$ if the model is simple. LIME does not have this "sanity check" requirement.
    \item \textbf{Generalization:} LFA treats explanation as a learning problem, requiring train/validation/test splits to avoid overfitting to a small number of perturbations.
\end{enumerate}

\vfill
\begin{block}{The Authors' Take}
The paper is not saying LIME is useless; it is making the hidden mathematical assumptions explicit to ensure faithfulness.
\end{block}

---


# The LFA Landscape: Mapping 8 Methods

The LFA framework unifies these methods by varying only the **neighborhood** ($\mathcal{Z}$) and the **loss function** ($\ell$).

\footnotesize
:::: columns
::: {.column width="50%"}
\begin{block}{1. Continuous (Additive)}
\small
\textbf{Neighborhood:} Gaussian noise.
\begin{itemize}
    \item \textbf{C-LIME:} Squared Error.
    \item \textbf{SmoothGrad:} Gradient Matching.
    \item \textbf{Vanilla Grad:} Gradient Matching ($\sigma \rightarrow 0$).
\end{itemize}
\end{block}

\vspace{-0.2cm}

\begin{block}{2. Continuous (Path-based)}
\small
\textbf{Neighborhood:} Multiplicative Uniform. \\
\textbf{Loss:} Gradient Matching.
\begin{itemize}
    \item \textbf{Integrated Gradients}
    \item \textbf{Gradients $\times$ Input}
\end{itemize}
\end{block}
:::

::: {.column width="48%"}
\begin{block}{3. Binary (Perturbation-based)}
\small
\textbf{Neighborhood:} Binary Kernels. \\
\textbf{Loss:} Squared Error.
\begin{itemize}
    \item \textbf{LIME:} Exponential kernel.
    \item \textbf{KernelSHAP:} Shapley kernel.
    \item \textbf{Occlusion:} Random one-hot.
\end{itemize}
\end{block}

\vfill
\begin{exampleblock}{The Unified Insight}
\small
Methods disagree because they use different \textbf{neighborhoods}, not because they have different fundamental goals.
\end{exampleblock}
:::
::::

---

# Theorems 1 & 2: The Mathematical Bridges


The LFA framework uses two primary loss functions to prove that 8 diverse methods are actually solving the same optimization problem.

:::: columns
::: {.column width="48%"}
\begin{block}{1. Gradient Matching (Thm 1)}
\small
Used for \textbf{gradient methods} (SmoothGrad, Integrated Gradients).
$$\ell_{gm} = \|\nabla f - \nabla g\|_2^2$$
\vspace{0.1cm}
By matching the \textbf{slopes} of the functions, LFA becomes equivalent to calculating expectations of gradients.
\end{block}
:::

::: {.column width="48%"}
\begin{block}{2. Squared Error (Thm 2)}
\small
Used for \textbf{perturbation methods} (LIME, KernelSHAP, Occlusion).
\vspace{0.4cm}
Using \textbf{binary noise} and $L_2$ loss, LFA recovers these methods via importance sampling.
\end{block}
:::
::::

\vfill
\begin{exampleblock}{The Unified Reality}
Whether you are matching derivatives (Thm 1) or matching output values (Thm 2), you are performing local function approximation.
\end{exampleblock}

---

# Theorem 3: No Free Lunch for Explanations

**Theorem:** If the model $f$ is more complex than the interpretable class $G$, no single explanation can be optimal across all neighborhoods.

\begin{equation}
\max_{\xi_1} \ell(f, g^*, \mathbf{x}_0, \xi_1) \leq \epsilon \implies \exists \xi_2 : \max_{\xi_2} \ell(f, g^*, \mathbf{x}_0, \xi_2) \geq d(f, \mathcal{G})
\end{equation}

\vspace{0.4cm}
\begin{block}{The Core Intuition}
An explanation is a local approximation. If you try to make it work everywhere, it will necessarily fail somewhere. 
\end{block}

\vfill
\begin{exampleblock}{Strategic Insight}
Seeking the "best" explanation without specifying a neighborhood is \textbf{futile}. The "best" method is simply the one that uses the neighborhood relevant to your task.
\end{exampleblock}


---

# Guiding Principle: Model Recovery

\begin{block}{Definition: Model Recovery}
An explanation method is effective if, when the black-box $f$ and the explainer $g$ are in the same class, the method returns $g^* = f$.
\end{block}

\vspace{0.4cm}
**Why is this our guiding principle?**
- It serves as a **"Sanity Check"** for faithfulness.
- If a method cannot recover a simple linear model using a linear explainer, it is fundamentally unsuited for that domain.
- It allows us to evaluate methods even when we don't know the "ground truth" of a complex neural network.

\vfill
\centering \footnotesize \textit{This principle shifts the choice from "Which method do I like?" to "Which method is mathematically consistent with my data?"}


---

# Selection Guide: Matching Method to Domain

The input domain $\mathcal{X}$ is the primary constraint for achieving **Model Recovery**. You cannot choose a method based on popularity, but on mathematical consistency.

\small Consistency with $\mathcal{X}$ is the primary constraint for \textbf{Model Recovery}.
\vspace{-0.1cm}
\begin{block}{1. Continuous ($\mathbb{R}^d$)} \scriptsize \textbf{Rec:} Additive Continuous Noise (SmoothGrad, C-LIME). \end{block}
\begin{block}{2. Binary ($\{0,1\}^d$)} \scriptsize \textbf{Rec:} Multiplicative Binary Noise (LIME, SHAP). \end{block}
\begin{alertblock}{The Discrete Gap} \scriptsize Current methods are \textbf{not optimal} for discrete data. \end{alertblock}

---

# Summary of Properties of Existing Explanation Methods

\begin{center}
\includegraphics[width=0.95\columnwidth]{imgs/lfa_properties_table.png}
\end{center}

- For **continuous data**: C-LIME, SmoothGrad, Vanilla Gradients perform model recovery
- For **binary data**: LIME, KernelSHAP, Occlusion perform model recovery
- Integrated Gradients and Gradient $\times$ Input: no model recovery in either domain

---

# Experimental Setup: Common Ground

The three experiments use the same datasets and models to validate different parts of the theory.

\begin{block}{1. Datasets (20-24 features)}
\small
\begin{itemize}
    \item \textbf{WHO (World Health Org):} Regression task (Life expectancy).
    \item \textbf{HELOC (FICO):} Classification task (Credit risk).
\end{itemize}
\end{block}

\begin{block}{2. Models (4 per task)}
\small
For each dataset, the following were trained:
\begin{itemize}
    \item \textbf{1 Simple Model:} Linear/Logistic Regression (key for Exp 2 Recovery).
    \item \textbf{3 Neural Networks:} Of increasing complexity (3, 5, and 8 hidden layers).
\end{itemize}
\end{block}

\vfill
\centering \footnotesize \textit{Metrics: L1 Distance and Cosine Distance over 100 random test points.}


---

# Exp 1: Correspondence Validation

:::: columns
::: {.column width="45%"}
\textbf{Goal:} Assess if existing methods are truly LFA instances by comparing original implementations (Captum) vs. LFA re-implementations.

\vspace{0.4cm}
\textbf{Key Findings:}
\small
\begin{itemize}
    \item \textbf{Identity:} Near-zero L1 distance on the diagonal confirms that methods like LIME, SHAP, and SmoothGrad are mathematically equivalent to LFA instances.
    \item \textbf{Clustering:} Methods group naturally by their choice of noise (e.g., SmoothGrad and Vanilla Grad form a distinct family).
\end{itemize}
:::

::: {.column width="53%"}
\begin{center}
    \includegraphics[width=\textwidth, height=0.7\textheight, keepaspectratio]{imgs/eval_exp1_results.png}
\end{center}
\centering \footnotesize \textit{Average L1 distance between pairs of explanations (WHO dataset).}
:::
::::


---

# Exp 2: Model Recovery (Sanity Check)

:::: columns
::: {.column width="45%"}
**Goal:** Empirically assess which methods recover the black-box model $f$ when $f$ is simple (Linear/Logistic).

\vspace{0.4cm}
**The Scale Gap Finding:**
\small
\begin{itemize}
    \item \textbf{Additive Methods:} SmoothGrad and Vanilla Gradients recover the \textbf{true weights} ($w_g = w_f$).
    \item \textbf{Multiplicative Methods:} LIME, SHAP, IG, and Grad$\times$Input recover the \textbf{scaled weights} ($w_g = w_f \odot x$).
\end{itemize}

:::

::: {.column width="53%"}
\begin{center}
    \includegraphics[width=\textwidth, height=0.7\textheight, keepaspectratio]{imgs/eval_exp2_results.png}
\end{center}
\centering \footnotesize \textit{L1 distance to weights (left) and to weights $\times$ input (right).}
:::
::::
\begin{alertblock}{The IG Paradox} \scriptsize Integrated Gradients fails to recover the base linear model in continuous domains. \end{alertblock}

---

# Exp 3: The "No Free Lunch" Reality

:::: columns
::: {.column width="45%"}
**Goal:** Illustrate that no single method performs best across all evaluation neighborhoods.

\vspace{0.4cm}
\begin{block}{Methodology}
\scriptsize $Bottom-k$ perturbations: Replace with zero (Binary) vs. Gaussian noise (Continuous).
\end{block}

\vspace{0.4cm}
\begin{alertblock}{The Evaluation Bias} 
\scriptsize The metric is \textbf{not neutral}; it favors the noise type it uses. 
\end{alertblock}
:::

::: {.column width="53%"}
\begin{center}
    \includegraphics[width=\textwidth, height=0.75\textheight, keepaspectratio]{imgs/eval_exp3_results_bottomk.png}
\end{center}
\centering \footnotesize \textit{Binary perturbations (left) vs. Continuous perturbations (right).}
:::
::::

\vfill
\centering \footnotesize \textit{Results are consistent across Top-K feature evaluation.}


---

# Future Work: Beyond Faithfulness

The LFA framework provides a mathematical foundation for faithfulness, but several open questions remain for the field of XAI.

\begin{itemize}
    \item \textbf{Expanding the Unification:} The current analysis covers 8 methods, but it could be extended to other families (e.g., counterfactual explanations or rule-based surrogates).
    \item \textbf{From Faithfulness to Interpretability:} This work ensures $g$ is a good proxy for $f$, but it doesn't guarantee that $g$ is easy for a human to process.
    \item \textbf{Defining "Interpretable":} The choice of the model class $\mathcal{G}$ (e.g., linear models) is based on the assumption that they are interpretable. Future research should involve \textbf{Human-Computer Interaction (HCI)} and user studies to validate this.
\end{itemize}

\vfill
\begin{exampleblock}{The Research Frontier}
How do we mathematically incorporate human cognitive constraints into the loss function $\ell$ of the LFA framework?
\end{exampleblock}

---

# Discussion Questions (Paper 2)

1. Do you agree that the Local Function Approximation framework is a useful conceptual tool for understanding & comparing explanation methods?

2. If no explainability method can perform optimally across all perturbation distributions, as implied by the No Free Lunch Theorem, does that mean explainability should be defined relative to a perturbation neighborhood?
   - How does that complicate interpretability, especially for practitioners without ML expertise?

3. More broadly, what do you think about papers that attempt to create conceptual coherence & clarity across the field of explainability? Should this be a higher priority area of research?

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References {.allowframebreaks}

\footnotesize
