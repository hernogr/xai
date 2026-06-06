---
title: "\\emoji{wtf} XAI Lecture 20"
subtitle: "Explainability for Fair ML \\& Robust Counterfactuals under the Right to be Forgotten"
bibliography: references.bib

---

# Disclaimer

\input{../disclaimer.tex}

---

# Paper 1

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/paper1.png}
\end{center}


[@begley2020explainability]

---

# Introduction + Motivation

**The core tension in fair ML**

:::: {.columns}
::: {.column width="50%"}

\vspace{1em}

- ML models make high-stakes decisions affecting individuals
- **Detecting unfairness is non-trivial**: many competing definitions exist
- Existing XAI tools **do not reliably indicate** whether a model is fair
- Using explainability to validate fairness can be misleading

:::
::: {.column width="48%"}

\begin{alertblock}{Central Questions}
\begin{enumerate}
\item Can XAI tools detect unfairness?
\item Can we \textbf{attribute} unfairness to individual features?
\item Can we use that attribution to \textbf{intervene} modularly?
\end{enumerate}
\end{alertblock}

:::
::::


---

# Fairness Definitions: Examples

**Demographic parity:** $f(x)$ is unconditionally independent of sensitive attribute $a$

- If 100 female and 100 male students apply to Harvard, parity is achieved if the admission rate is equal for both groups, regardless of average qualification.

**Equalized odds:** $f(x)$ is independent of $a$ given $y$

- Qualified female and male applicants have the same probability of admission; same for unqualified applicants.

:::: {.columns}
::: {.column width="44%"}

\begin{center}
\textbf{Group A (Female)}
\end{center}

\begin{center}
\begin{tabular}{l|cc}
 & \textbf{Qualified} & \textbf{Unqualified} \\
\hline
\textbf{Admitted}  & 45 & 2  \\
\textbf{Rejected}  & 45 & 8  \\
\hline
\textbf{Total}     & 90 & 10 \\
\end{tabular}
\end{center}

:::
::: {.column width="12%"}

\vspace{3em}
\begin{center}
{\color{darkgreen}\Huge $\checkmark$}
\end{center}

:::
::: {.column width="44%"}

\begin{center}
\textbf{Group B (Male)}
\end{center}

\begin{center}
\begin{tabular}{l|cc}
 & \textbf{Qualified} & \textbf{Unqualified} \\
\hline
\textbf{Admitted}  & 5  & 18 \\
\textbf{Rejected}  & 5  & 72 \\
\hline
\textbf{Total}     & 10 & 90 \\
\end{tabular}
\end{center}

:::
::::



---

# The Explanation Attack

:::: {.columns}
::: {.column width="45%"}

\vspace{1em}

Explanation methods can be **manipulated**. 

\vspace{.5em}

An explanation attack can easily mask a model's disciminatory use of a sensitive feature without hurting accuracy [@dimanov2020shouldnt].

\vspace{.5em}

\begin{flushright}
{\small\textit{\textcolor{gray}{Importance ranking histograms for gender as the sensitive feature on the adult test set of original (left) and modified (right) models}}}
\end{flushright}
\par


\vfill

:::
::: {.column width="52%"}

\begin{center}
\includegraphics[width=\linewidth]{imgs/explanation_attack.png}
\end{center}

:::
::::

## Key Gap

If explanations can be manipulated, they cannot serve as evidence of fairness.
Begley et al.'s solution: Fairness Shapley Values **must sum** to the chosen fairness metric --- manipulation is impossible without changing the metric itself.

---

# Background: Shapley Values

**Cooperative game theory $\rightarrow$ feature attribution**

$$\phi_v(i) = \sum_{S \subseteq N \smallsetminus \{i\}} \frac{|S|!\,(n - |S| - 1)!}{n!} \left[ v(S \cup \{i\}) - v(S) \right]$$

:::: {.columns}
::: {.column width="50%"}

\footnotesize

| Symbol | Meaning |
|--------|---------|
| $\phi_v(i)$ | Shapley value of feature $i$ |
| $N$ | Set of all features |
| $S \subseteq N \smallsetminus \{i\}$ | Coalition not containing $i$ |

:::
::: {.column width="50%"}

\footnotesize

| Symbol | Meaning |
|--------|---------|
| $v(S)$ | Value of coalition $S$ |
| $v(S \cup \{i\}) - v(S)$ | Marginal contribution of $i$ to $S$ |
| $\frac{\vert S\vert!(n-\vert S\vert-1)!}{n!}$ | Weighting over all orderings |

:::
::::

## In Plain English

The Shapley value of feature $i$ is its **average marginal contribution** when added to every possible coalition of other features --- a fair division of the outcome among all participants.


---

# Fair Machine Learning - Proposed Solution

- A **unified** approach that works for many **group-fairness** criteria
    - demographic parity, equalised odds, conditional demographic parity
    - for each definition, choose Shapley value functions that attribute overall fairness to individual features.

\vspace{2em}

- **Cannot hide unfairness** by manipulating explanations
    - Fairness Shapley values collectively must sum to the chosen fairness metric

---

# Explaining Model Accuracy

\small
\setlength{\abovedisplayskip}{2pt}
\setlength{\belowdisplayskip}{2pt}
\setlength{\abovedisplayshortskip}{0pt}
\setlength{\belowdisplayshortskip}{0pt}

- Shapley value $\phi_v(i)$ attributes a portion to player $i$:
$$\phi_v(i) = \sum_{S \subseteq N \smallsetminus \{i\}} \frac{|S|!\,(n - |S| - 1)!}{n!} \left[ v(S \cup \{i\}) - v(S) \right] \tag{1}$$

\vspace{.5em}

- Binary classification problem:
$$f_y(x) = (1-y)(1-f(x)) + y\,f(x) \tag{2}$$

\vspace{.5em}

- Value function by marginalising over out-of-coalition features:
$$v_{f_y(x)}(S) = \mathbb{E}_{p(x')}\!\left[f_y(x_S \cup x'_{N \smallsetminus S})\right] \tag{3}$$

\vspace{.5em}

- Global explanation of model performance:
$$\Phi_f(i) = \mathbb{E}_{p(x,y)}\!\left[\phi_{f_y(x)}(i)\right] \tag{4}$$

---

# Explaining Model Accuracy (cont)

- Aggregating global Shapley values:

$$\sum_i \Phi_f(i) = \underbrace{\mathbb{E}_{p(x,y)}\!\left[f_y(x)\right]}_{\substack{\scriptsize\text{Expected accuracy for a} \\ \scriptsize\text{model which samples a} \\ \scriptsize\text{predicted label according} \\ \scriptsize\text{to the predicted probability}}} - \underbrace{\mathbb{E}_{p(x')p(y)}\!\left[f_y(x')\right]}_{\substack{\scriptsize\text{The accuracy that is not} \\ \scriptsize\text{attributable to any of the} \\ \scriptsize\text{features and is related to the} \\ \scriptsize\text{class balance}}} \tag{5}$$

## In Plain English

Total accuracy decomposes as a sum of individual feature contributions, with a baseline term capturing class imbalance.

---

# Explaining Model Fairness

\small
\setlength{\abovedisplayskip}{1pt}
\setlength{\belowdisplayskip}{1pt}
\setlength{\abovedisplayshortskip}{0pt}
\setlength{\belowdisplayshortskip}{0pt}

- To explain fairness, define a new value function that captures this effect :

:::: {.columns}
::: {.column width="40%"}

\vspace{.5em}
\begin{flushright}
{\footnotesize\textit{Demographic parity calls for $f(x)$ to be unconditionally independent of $a$}}
\end{flushright}

:::
::: {.column width="60%"}

$$g_a(x) = f(x) \cdot \frac{(-1)^a}{p(a)}, \qquad a: \text{sensitive attribute} \tag{6}$$

:::
::::

- The value function on coalitions is defined through marginalisation:

:::: {.columns}
::: {.column width="50%"}

$$v_{g_a(x)}(S) = \mathbb{E}_{p(x')}\!\left[g_a(x_S \cup x'_{N \smallsetminus S})\right] \tag{7}$$

:::
::: {.column width="50%"}

$$\Phi_g(i) = \mathbb{E}_{p(x,a)}\!\left[\phi_{g_a(x)}(i)\right] \tag{8}$$

:::
::::

\vspace{.2em}
- Each feature's marginal contribution to the overall demographic disparity:
$$\sum_i \Phi_g(i) = \int dx\, p(x|a=0)\,f(x) - \int dx\, p(x|a=1)\,f(x) \tag{9}$$

## In Plain English

Each feature receives a share of the model's **total demographic disparity**. The sum of all Fairness Shapley Values equals exactly the chosen fairness metric --- it cannot be manipulated without changing the metric.

---

# Learning Corrective Perturbations

\small
\setlength{\abovedisplayskip}{3pt}
\setlength{\belowdisplayskip}{3pt}
\setlength{\abovedisplayshortskip}{0pt}
\setlength{\belowdisplayshortskip}{0pt}

The **linearity axiom** of Shapley values guarantees that fairness Shapley values of a linear ensemble are the corresponding linear combination of the underlying models' values.

This motivates learning an additive perturbation to the original model:
\vspace{-0.8em}

$$f_\theta = f + \delta_\theta$$

\vspace{-0.5em}

$$\delta_\theta(f(x), x, a) = \sigma\!\left(\sigma^{-1}(f(x)) + \tilde{\delta}_\theta(f(x), x, a)\right) - f(x)$$

\vspace{-0.5em}
\footnotesize

| Symbol | Meaning |
|--------|---------|
| $f$ | Original model (black box) |
| $\tilde{\delta}_\theta$ | Any training-time fairness algorithm |
| $f_\theta$ | Corrected model |

\normalsize

\vspace{-0.5em}

## In Plain English

Instead of retraining the full model, a lightweight **patch** is learned to impose fairness. Shapley linearity ensures the corrected model's values remain interpretable in terms of its components.

---

# Experimental Setup

**Datasets:**

| Dataset | Task | Sensitive attribute $a$ |
|---------|------|------------------------|
| Adult (UCI) | Income prediction $>$50K | Sex, Race |
| COMPAS | Recidivism prediction | Race |

**Evaluation:** fairness metric and accuracy, before and after intervention.

---

# Results: Explainability

:::: {.columns}
::: {.column width="25%"}

\small

\vspace{2em}

On the Adult dataset, the features with the highest contribution to unfairness are `marital status`, `sex`, and `relationship` --- even when `sex` does not appear directly in the model.

:::
::: {.column width="75%"}

\begin{center}
\includegraphics[width=\linewidth]{imgs/explainability_results.png}
\end{center}

:::
::::

---

# Results: Robustness of Fairness Explanations

:::: {.columns}
::: {.column width="30%"}

\small

\vspace{3em}

An attack suppressing the importance of `sex` reduces the Demographic Parity Difference from 0.193 to 0.184 --- a minimal reduction.

\vspace{2em}

Fairness Shapley Values **cannot** be manipulated to hide unfairness without changing the global metric.

:::
::: {.column width="70%"}

\begin{center}
\includegraphics[width=.9\linewidth]{imgs/robustness_results.png}
\end{center}

:::
::::

---

# Results: Learned Perturbations (Demographic Parity)

:::: {.columns}
::: {.column width="70%"}

\begin{center}
\includegraphics[width=\linewidth]{imgs/table1_dp.png}
\end{center}

:::
::: {.column width="30%"}

\vspace{3em}
\small

- **No significant accuracy loss** across all thresholds
- Perturbed models track their originals closely
- Achieving near-perfect fairness costs less than **2 percentage** points of accuracy.
:::
::::

---

# Results: Learned Perturbations (Equalized Odds)

:::: {.columns}
::: {.column width="70%"}

\begin{center}
\includegraphics[width=\linewidth]{imgs/table2_eo.png}
\end{center}

:::
::: {.column width="30%"}

\vspace{3em}
\small

- **No significant accuracy loss** under equalized odds
- Results generalize across fairness definitions



:::
::::


---

# Results: Learned Perturbations

\vspace{1em}
\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/perturbation_results.png}
\end{center}

\vspace{-0.5em}

- No significant accuracy reduction under demographic parity or equalized odds
- The perturbative approach has **lower variance** and higher mean accuracy than baselines
- **Model-agnostic**: structure or access requirements apply only to the perturbation, not the original model

---

# Limitations (Paper 1)

- The choice of disparity measure $\delta$ is **normative**, not technical
- Exact Shapley computation is **exponential** in $|F|$; approximations (SHAP) are used in practice
- The framework is **global**; local fairness attributions remain an open problem
- Does not resolve **which** fairness definition is appropriate for a given context

## Notes

Does Shapley attribution *explain* unfairness, or merely *measure* it?

---

# Summary of Contributions (Paper 1)

| Contribution | Key point |
|---|---|
| Fairness Shapley Values | Attributes $\sum_i \Phi_g(i)$ to individual features |
| Linearity property | Unfairness decomposes additively |
| Meta-algorithm | Wraps any training-time fairness intervention |
| Robustness | Explanations cannot be manipulated |

---


# Paper 2

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/paper2.png}
\end{center}

[@krishna2023bridging]

---

# Motivation (Paper 2)

**Two pillars of algorithmic accountability under GDPR**

:::: {.columns}
::: {.column width="50%"}

\vspace{1em}

- **Art. 22 (Right to Explanation):** individuals subject to automated decisions must receive a meaningful explanation
- **Art. 17 (Right to be Forgotten):** individuals may request deletion of their personal data from models and databases
- Both rights are **legally enforceable simultaneously**

:::
::: {.column width="48%"}

\begin{alertblock}{The Problem}
\begin{enumerate}
\item Both rights are legally binding
\item Enforcing one may \textbf{automatically violate} the other
\item No existing framework addresses their \textbf{joint satisfaction}
\end{enumerate}
\end{alertblock}

:::
::::
---

# The Conflict: A Concrete Example

\vspace{1em}
\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/conflict_diagram.png}
\end{center}

- A bank trains $f_{\theta_1}$ on $D$; denies a loan to $x_0$; provides counterfactual explanation $x^*$ under $f_{\theta_1}$
- Another user invokes Art. 17; their data is deleted; model updates to $f_{\theta_w}$
- Explanation $x^*$ is no longer valid under $f_{\theta_w}$ --- **Art. 22 is violated**


---

# Contributions (Paper 2)

- First algorithmic framework (**ROCERF**) to address the tradeoff between the right to explanation and the right to be forgotten
- ROCERF not only bridges the gap but also **outperforms** existing counterfactual explanation methods

---

# ROCERF Framework

**RObust Counterfactual Explanations under the Right to be Forgotten**

The framework proceeds in four steps:

- CFE as a standard optimization problem
- CFE as an optimization problem under data removal
- Efficient approximation (naive solution is intractable)
- Theoretical bounds on cost and validity

---


# Notation: ROCERF

**Data and classifier:**

$$D = \{(x_i, y_i)\}_{i=1}^n, \quad x_i \in \mathcal{X},\; y_i \in \{-1, +1\}$$

$$f_{\theta_1} = \operatorname{arg\,min}_{\theta} \frac{1}{n}\sum_{i=1}^n l_i(\theta), \qquad f_{\theta_w} = \operatorname{arg\,min}_{\theta} \frac{1}{\|w\|_1}\sum_{i=1}^n w_i\, l_i(\theta)$$

**Data weight vector** $w \in \{0,1\}^n$:

$$w_i = \begin{cases} 1 & \text{data point } i \text{ in training set} \\ 0 & \text{data point } i \text{ deleted} \end{cases}$$

$w = \mathbf{1}$ means no data point has been removed.

---

# Counterfactual Explanation (CFE)


- The Counterfactual Explanation is:
    - Optimisation problem - find valid counterfactual with minimum cost
    - the closest point to $x_0$ that flips the prediction:

$$\min_{x \in \mathcal{X}} \;\; \|x - x_0\|_2 \qquad \text{s.t.} \quad f_{\hat\theta_1}(x) \geq 0$$

## In Plain English

"What is the minimum change to your profile so the model approves your loan?"
This counterfactual is valid for the current model --- but may become invalid if the model changes.

---

# k-Removal Robust CFE

**Definition:** a k-RR CFE is a counterfactual that remains valid upon removal of *any* $k$ data points.

$$\mathcal{W}^{(k)} = \{w \in \{0,1\}^n : \|w\|_1 = n - k\}$$

$$\min_{x \in \mathcal{X}} \;\; \|x - x_0\|_2 \qquad \text{s.t.} \quad f_{\hat\theta_w}(x) \geq 0,\; \forall w \in \mathcal{W}^{(k)}$$

Naive solution: train $\binom{n}{k}$ classifiers and optimise with $\binom{n}{k}$ constraints.

## Key Gap

Computationally intractable. An efficient approximation is needed.

---

# Efficient Approximation: First-Order Taylor

For fixed $x$, approximate $f_{\hat\theta_w}(x)$ via Taylor expansion w.r.t. $w$ (Giordano et al., 2019):

$$\tilde f_{\hat\theta_w}(x) = f_{\hat\theta_1}(x) + \frac{1}{n} \sum_{i:\, w_i = 0} \beta(x)^T H^{-1} g_i(\hat\theta_1)$$

where:

$$\beta(x) := \left(\left.\frac{\partial f_\theta(x)}{\partial \theta}\right|_{\theta = \hat\theta_1}\right)^T, \quad H := \frac{1}{n}\sum_{i=1}^n h_i(\hat\theta_1), \quad g_i(\theta) := \frac{\partial l_i(\theta)}{\partial \theta}$$

## In Plain English

Instead of retraining for each possible deletion, the Hessian of the original model estimates how the prediction would change --- in a single pass.

---

# Eff. Approx: Reducing $\binom{n}{k}$ Constraints to One

The term $\beta(x)^T H^{-1} g_i(\hat\theta_1)$ is **independent of** $w$. Only the tightest constraint needs to be retained:

$$\mathcal{A}(x) := \{\beta(x)^T H^{-1} g_i(\hat\theta_1)\}_{i=1}^n$$

$$\fcolorbox{darkgreen}{white}{$\displaystyle f^{(k)}_{\mathcal{A}}(x):= f_{\hat\theta_1}(x) + \frac{1}{n} \min_{\mathcal{B} \subseteq \mathcal{A}(x),\, |\mathcal{B}|=k} \sum_{b \in \mathcal{B}} b$}$$

$$\min_{x \in \mathcal{X}} \|x - x_0\|_2 \qquad \text{s.t.} \quad f^{(k)}_{\mathcal{A}}(x) \geq \delta$$

## In Plain English

The worst case is deleting the $k$ points that most damage the prediction — pick the $k$ smallest values of $\mathcal{A}(x)$.

---

# Eff. Approx.: Final Optimisation Problem

- Solving the constrained optimization problem.
- Penalty method:

$$\phi(z) := \max(z, 0)^2$$

$$\min_{x \in \mathcal{X}} J_t(x) = \lambda_t\, \phi\!\left(\delta - f^{(k)}_{\mathcal{A}}(x)\right) + \|x - x_0\|_2$$


## In Plain English

The constraint becomes a penalty term that grows until the solution satisfies $f^{(k)}_{\mathcal{A}}(x) \geq \delta$ — standard unconstrained optimisation.

---

# Theoretical Guarantees: Linear Models

For regularised logistic regression with $l_i(\theta) = \log(1 + \exp(-y_i \theta^T x_i)) + \gamma\|\theta\|_2^2$:

$$\|\tilde{x}_0^{(k)} - x_0\|_2 \leq \|\tilde{x}_0 - x_0\|_2 + \frac{kC}{n\|\hat\theta_1\|_2}$$

The additional cost of robustness has an upper bound of $\mathcal{O}(k/n)$, with theoretical guarantees on validity.

## In Plain English

Larger $k$ (more deletions to tolerate) or smaller $n$ (less data) increases the cost of the robust counterfactual --- but the growth is controlled and bounded.

---

# Theoretical Guarantees: Nonlinear Models

Under regularity assumptions (Lipschitz, convexity), for nonlinear models:

$$\|\tilde{x}_0^{(k)} - x_0\|_2 \leq \|\tilde{x}_0 - x_0\|_2 + \frac{2kC}{n}$$

If the function is $\mu$-strongly convex, the bound improves further.

The linear approximation may not capture deep neural network behaviour --- authors report cases where validity **improves** as more data is deleted, which is counterintuitive.

---

# Experimental Setup

**Datasets:** three real-world binary classification datasets from high-stakes decision-making scenarios:

- **German Credit** (Dua & Graff, 2017): 1,000 individuals, 60 features (demographic, personal, financial). Target: credit risk — "good" or "bad".
- **Adult** (Yeh & Lien, 2009): 48,842 individuals, features include demographics, education, employment, and financial data. Target: income — above or below \$50 k/year.
- **COMPAS** (Jordan & Freiburger, 2015): 18,876 defendants, criminal records and demographic features. Target: bail decision — "bail" or "no bail".

**Models:**

- **Logistic Regression (LR):** regularised logistic regression (scikit-learn default). Accuracy: German Credit 72.2%, COMPAS 85.8%, Adult 84.0%.
- **Neural Network (NN):** 3-layer fully-connected feedforward network, hidden size $= 2 \times$ input dim, centered-softplus activation, trained with SGD (lr $= 0.01$). Accuracy: German Credit 73.9%, COMPAS 85.1%, Adult 84.7%.

---

# Experimental Setup cont.

**Baselines:**

- **SCFE** (Wachter et al., 2017): gradient-based optimization to find the CFE closest to the input — solves the standard problem (1) without any robustness consideration.
- **C-CHVAE** (Pawelczyk et al., 2020): manifold-based method that searches for CFEs in a latent space, encouraging realistic counterfactuals on the data manifold.
- **ROAR** (Upadhyay et al., 2021): generates CFEs robust to small Gaussian perturbations of model parameters — the strongest baseline, as it addresses model changes but without guarantees under data deletion.

**Protocol:** randomly remove a fraction $\alpha \in [0.5\%, 5\%]$ of training data, repeated $M = 100$ times. Hyperparameters: $k = 0.5\%$ of training set size, $\delta = 0$.

---

# Experimental Results: Logistic Regression

* The x-axis corresponds to the fraction of data removal $\alpha$ and the y-axis corresponds to the average validity. 
* The error bars indicate the standard errors across $M = 100$ trials with each trial having an $\alpha$ fraction of training data points randomly removed. 

\vspace{0.1em}
\begin{center}
\includegraphics[width=0.8\columnwidth]{imgs/experiment_results_log_p2.png}
\end{center}

* ROCERF maintains validity $\approx 1.0$ while all baselines degrade significantly.

---

# Experimental Results: Neural Networks Logistic Regression

\vspace{0.1em}
\begin{center}
\includegraphics[width=0.8\columnwidth]{imgs/experiment_results_NN_p2.png}
\end{center}

* More dataset-dependent behaviour. 
    - German Credit shows counterintuitive improvement 
    - Small dataset size causes dramatic boundary shifts after deletion.



---

# Experimental Results: Average Cost

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/experiment_results_table1_p2.png}
\end{center}

- **SCFE** has the lowest cost but significantly worse validity — cheap recourse that breaks under any deletion.
- **C-CHVAE** pays very high cost across all datasets — manifold constraint makes CFEs expensive.
- **ROAR** is close to **ROCERF** but **ROCERF** consistently achieves lower or equal cost with better validity.

---

# Experimental Results: Average Cost Neural Networks

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/experiment_results_table2_p2.png}
\end{center}

- **C-CHVAE** cost explodes on Adult ($8.83$) — manifold search fails badly in complex model settings.
- **ROAR** and **ROCERF** track closely on COMPAS and Adult — consistent with the validity results.
- **ROCERF** achieves the best cost/validity tradeoff overall: robustness does not require paying a large extra cost.

---

# Sensitivity Analysis — Hyperparameter $k$

\begin{center}
\includegraphics[width=0.90\columnwidth]{imgs/rocerf_sensitivity_k_p2.png}
\end{center}

- **COMPAS and Adult:** all variants of $k$ achieve 100% validity across all $\alpha$ values.
- **German Credit:** lowest $k$ shows a slight drop for high $\alpha$ — fixed by increasing $k$.
- Key guarantee: $k = 0.01n$ achieves 100% validity for any $\alpha \leq 1\%$; $k = 0.02n$ for any $\alpha \leq 2\%$.

---


# The Validity-Cost Trade-off

:::: {.columns}
::: {.column width="55%"}

\vspace{2em}

Forcing an explanation to remain valid under **more possible deletions** necessarily moves the counterfactual further from the original point.

This is not a bug --- it is the **correct price** for regulatory compliance.

The cost grows as $k$ increases.

:::
::: {.column width="43%"}

\begin{alertblock}{For Regulators}
How much additional cost is
acceptable in exchange for
deletion-robust explanations?
This is a \textbf{policy decision},
not a technical one.
\end{alertblock}

:::
::::

---

# Limitations (Paper 2)

:::: {.columns}
::: {.column width="55%"}

- Taylor approximation is exact only for convex losses; nonlinear models exhibit counterintuitive behaviour
- Inverting $H$ is $\mathcal{O}(p^3)$ --- impractical for large neural networks
- $k$ must be specified in advance; no principled selection method is provided
- ROAR (with the same hyperparameters) tracks ROCERF closely --- is ROCERF really necessary?

:::
::: {.column width="43%"}

\begin{alertblock}{Philosophical Note}
An explanation that changes when
training data changes was never
really about the \textit{individual} ---
it was about the \textit{model state
at a given moment}.
\end{alertblock}

:::
::::

---

# Summary of Contributions (Paper 2)

| Contribution | Key point |
|---|---|
| ROCERF framework | First algorithm bridging the Art. 22 / Art. 17 conflict |
| k-RR CFE | Counterfactual valid under any deletion of $k$ data points |
| $\mathcal{O}(n)$ approximation | Taylor + infinitesimal jackknife reduces $\binom{n}{k}$ constraints to one |
| Theoretical guarantees | Additional cost bounded by $\mathcal{O}(k/n)$ for linear models |

---

# Thank You!

\begin{center}
\Huge Thank You!
\end{center}

---

# References {.allowframebreaks}

\footnotesize
