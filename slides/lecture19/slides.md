---
title: "\\emoji{magnifying-glass-tilted-left} XAI: Input Gradients \\& Privacy Risks"
bibliography: references.bib

---

# Disclaimer

\input{../disclaimer.tex}

---

# Paper 1: Do Input Gradients Highlight Discriminative Features?

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/Paper-1.png}
\end{center}

[@shah2021gradients]

---

# Do Attribution Methods Work?

\begin{alertblock}{Central Question}
Do input gradient attribution methods actually highlight features that drive model predictions?
\end{alertblock}

- Attribution methods assign **importance scores** to input features
- Common assumption: higher gradient magnitude $\Rightarrow$ higher feature contribution
- But... how do we *rigorously evaluate* this?

\vspace{0.5em}

\begin{block}{Challenge}
Existing evaluations are often qualitative or rely on synthetic benchmarks — lacking a principled framework
\end{block}

---

# Assumption (A)

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/assumption_A.png}
\end{center}

\begin{definition}{}
\textbf{Assumption (A):} For model $f$ and input $x$, feature $i$ is more important than $j$ if $|\nabla_{x_i} f(x)| > |\nabla_{x_j} f(x)|$
\end{definition}

This assumption underlies most gradient-based XAI methods.

---

# Key Contributions

\begin{exampleblock}{DiffROAR: a new evaluation framework}
Systematically evaluate whether attribution methods highlight truly discriminative features via retrain-and-compare
\end{exampleblock}

- **Multiple benchmarks**: SVHN, FashionMNIST, CIFAR-10, ImageNet-10
- **BlockMNIST**: controlled dataset isolating discriminative vs.\ spurious features
- **Feature Leakage Hypothesis**: theoretical explanation for when attribution *appears* to work
- **Theorem**: formal characterization of feature leakage conditions

[@shah2021gradients]

---

# Related Work

\begin{columns}
\begin{column}{0.48\textwidth}
\small
\textbf{Sanity Checks} (Adebayo et al.)

\begin{itemize}
\item Randomize model weights or labels
\item Attribution must change accordingly
\end{itemize}

\vspace{0.4em}

\textbf{Fidelity-based Evaluation}

\begin{itemize}
\item Mask top features, measure accuracy drop
\item Single-pass evaluation can induce distribution shift
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\small
\textbf{Adversarial Robustness}

\begin{itemize}
\item Robust models can have more visually aligned gradients
\item The paper asks whether they also satisfy Assumption (A)
\end{itemize}

\vspace{0.4em}

\begin{alertblock}{Limitation of Prior Work}
Prior tests do not directly compare top-attributed features against bottom-attributed features.
\end{alertblock}
\end{column}
\end{columns}

---

# Why Sanity Checks Are Not Enough

Existing evaluation tools expose different failure modes:

- visual quality can be misleading
- randomization tests check sensitivity to weights/labels
- removal tests can create distribution shift
- ROAR retrains after removing important features

\vspace{0.5em}

\begin{block}{Gap}
ROAR asks whether top-ranked features matter, but Assumption (A) is comparative: top-ranked features should matter \textit{more than bottom-ranked features}.
\end{block}

[@adebayo2018sanity; @hooker2019benchmark]

---

# DiffROAR Framework

---

# Setting

\small

\begin{itemize}
\item Standard classification setting: each independently drawn data point is a pair
$(x^{(i)}, y^{(i)})$ of instance and label.
\item $x^{(i)}_j$ denotes the $j$th coordinate/feature of $x^{(i)}$.
\item \textbf{Feature attribution scheme}
\end{itemize}

\vspace{-0.6em}

\begin{center}
\fbox{\(\displaystyle A:\mathbb{R}^d \to \{\sigma:\sigma \text{ is a permutation of } [d]\}\)}
\end{center}

\vspace{-0.6em}

\begin{itemize}
\item maps a $d$-dimensional instance $x$ to a permutation of its features.
\item e.g., \textbf{input gradient attribution scheme} takes input instance $x$ and predicted label $\hat{y}$, then ranks features in decreasing order of input-gradient magnitude.
\end{itemize}

\vspace{-0.6em}

\begin{center}
\fbox{\(\displaystyle A(x):[d]\to[d]\)}
\end{center}

---

# Unmasking Schemes

\begin{columns}
\begin{column}{0.45\textwidth}
\small

\begin{itemize}
\item \textbf{Unmasked instance} $x^S$ zeroes out all coordinates not in subset $S$.
\item \textbf{Unmasking scheme} maps instance $x$ to a subset $A(x)$ of coordinates.
\end{itemize}

\vspace{-0.3em}

\begin{center}
\fbox{\(\displaystyle A:\mathbb{R}^d \to \{S:S\subseteq[d]\}\)}
\end{center}

\vspace{-0.4em}

\begin{itemize}
\item \textbf{Top-$k$}: preserve the $k$ coordinates with largest attribution scores.
\item \textbf{Bottom-$k$}: preserve the $k$ coordinates with smallest attribution scores.
\item All other coordinates are set to zero.
\end{itemize}

\vspace{-0.2em}

\begin{alertblock}{DiffROAR intuition}
If the attribution is faithful, top-$k$ should be more predictive than bottom-$k$.
\end{alertblock}

\end{column}
\begin{column}{0.53\textwidth}
\begin{center}
\includegraphics[width=\columnwidth]{imgs/unmasking_schemes.png}
\end{center}
\end{column}
\end{columns}

---

# Predictive Power

For an unmasking scheme $A$, predictive power is

$$
\mathrm{PredPower}_M(A)=
\sup_{f\in M}
\mathbb{E}_{(x,y)\sim D}
\left[\mathbf{1}\{f(x^{A(x)})=y\}\right].
$$

## In plain English

How well can a model of architecture $M$ classify examples if it only sees the features selected by $A$?

- The model is retrained on the masked training set.
- Retraining reduces artifacts from showing an old model unusual masked inputs.
- The output is a test accuracy.

--

# DiffROAR Metric

\footnotesize

\begin{center}
\fbox{
\begin{minipage}{0.92\textwidth}
\[
\mathrm{DiffROAR}_M(A,k)
=
\mathrm{PredPower}_M(A^{\mathrm{top}}_k)
-
\mathrm{PredPower}_M(A^{\mathrm{bot}}_k)
\]
\end{minipage}
}
\end{center}

\vspace{0.7em}

\textbf{Interpretation of the metric:}

\begin{itemize}
\item \textbf{Sign} indicates whether Assumption (A) is satisfied ($>0$) or violated ($<0$).
\item \textbf{Magnitude} quantifies how strongly the attribution separates most and least discriminative coordinates.
\item Random attribution should have expected DiffROAR near $0$.
\end{itemize}

---

# Experiment 1: Image Classification

The first experiment tests Assumption (A) on standard visual datasets.

- **SVHN:** real-world house-number digits.
- **FashionMNIST:** clothing images.
- **CIFAR-10:** small natural images from 10 classes.
- **ImageNet-10:** reduced ImageNet with 10 super-classes.

---

# Experimental Setup

- \textbf{Datasets}: SVHN, FashionMNIST, CIFAR-10, and ImageNet-10.
- \textbf{Models}: standard and adversarially trained two-hidden-layer MLPs and ResNets.
- \textbf{Adversarial training}: $\ell_2$ and $\ell_\infty$ $\epsilon$-robust models trained with PGD.
- \textbf{Metric}: DiffROAR across different unmasking fractions $k$.

---

# Results: Benchmark Datasets

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/benchmark_results_experiment_1.png}
\end{center}

\begin{alertblock}{Surprising Finding}
Most attribution methods yield DiffROAR $\approx 0$ on standard benchmarks — they perform no better than a \textbf{random feature selector}
\end{alertblock}

---

# Results: Benchmark Datasets

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/benchmark_results_experiment_1.png}
\end{center}

---

# Experiment 2: BlockMNIST

\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/block_MNSIT.png}
\end{center}

---

# BlockMNIST Dataset

\begin{center}
\includegraphics[width=0.4\columnwidth]{imgs/block_MNSIT.png}
\end{center}

- Two MNIST digits placed **side by side**
- **Relevant digit**: correlated with class label
- **Spurious digit**: uncorrelated with label
- A good attribution method should highlight the **relevant** digit

---

# Do Gradients Highlight the Signal Block?

---

# Do Gradients Highlight the Signal Block?. Not Always!

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/not_always_model_gradient_comparisions.png}
\end{center}

---

# Feature Leakage Hypothesis

\begin{definition}{}
\textbf{Feature leakage}: for a given instance, input gradients highlight not only the instance-specific signal, but also locations where signal appears in other instances.
\end{definition}

\vspace{0.5em}

\begin{itemize}
\item In BlockMNIST, the signal block can appear at the \textbf{top} or the \textbf{bottom}.
\item For the current image, only one block contains the digit that determines the label.
\item Standard gradients may still highlight both locations, because both locations are discriminative somewhere in the dataset.
\end{itemize}

\begin{center}
\includegraphics[width=05\columnwidth]{imgs/not_always_model_gradient_comparisions.png}
\end{center}

---

# Testing Feature Leakage: BlockMNIST-Top

\begin{columns}
\begin{column}{0.43\textwidth}
\small

\begin{itemize}
\item Fix the signal block at the \textbf{top} for every instance.
\item Keep the null block at the \textbf{bottom}.
\item If leakage comes from variable signal location, standard gradients should improve.
\end{itemize}

\begin{exampleblock}{Result}
Standard ResNet18 and MLP now highlight the signal block and suppress the null block.
\end{exampleblock}

\end{column}
\begin{column}{0.55\textwidth}
\begin{center}
\includegraphics[width=\columnwidth]{imgs/feature_leakage_hypothesis.png}
\end{center}
\end{column}
\end{columns}

---

# Simplified BlockMNIST: Theory Setup

\begin{columns}[T]
\begin{column}{0.56\textwidth}
\small

To analyze feature leakage formally, the paper replaces images with a block-structured simplified dataset.

\begin{itemize}
\item Each input $x$ is a concatenation of $d$ blocks.
\item The first $d/2$ blocks are \textbf{task-relevant}: the signal may appear in any one of them.
\item For each instance, only one block $j^*(x)$ contains the actual signal for that example.
\item The remaining $d/2$ blocks are \textbf{noise}: they never contain label information.
\end{itemize}

\begin{alertblock}{What a faithful gradient should do}
Highlight the unique signal block $j^*(x)$, not all possible signal locations.
\end{alertblock}

\end{column}
\begin{column}{0.40\textwidth}
\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/simplified_blockmnist_dataset.png}
\end{center}
\end{column}
\end{columns}

---

# Theorem 1: Feature Leakage

\begin{center}
\includegraphics[width=0.98\columnwidth]{imgs/theorem_1_statement.png}
\end{center}

\footnotesize

\begin{itemize}
\item There exists a max-margin classifier whose input-gradient magnitude is nonzero on all task-relevant blocks.
\item But it is \textbf{constant across those blocks}: it does not isolate the unique signal block for the current instance.
\item On noise blocks, the gradient is zero.
\end{itemize}

\begin{alertblock}{Meaning}
This formalizes feature leakage: gradients highlight task-relevant locations that are not specific to the given instance.
\end{alertblock}

---

# Empirical Results: What to Look For

\begin{columns}[T]
\begin{column}{0.72\textwidth}
\begin{center}
\includegraphics[width=\columnwidth]{imgs/figure5_empirical_results.png}
\end{center}
\end{column}
\begin{column}{0.26\textwidth}
\scriptsize

\begin{itemize}
\item All models get \textbf{100\% test accuracy} on this simplified dataset.
\item Linear model: marks all task-relevant coordinates.
\item Standard MLP: still marks all possible signal locations.
\item Robust MLP: marks the instance-specific signal coordinate.
\end{itemize}

\vspace{1.4em}

\begin{exampleblock}{Key point}
Prediction can be perfect while the explanation is not instance-specific.
\end{exampleblock}

\end{column}
\end{columns}

---

# Conclusions: DiffROAR

\begin{columns}
\begin{column}{0.48\textwidth}
\begin{alertblock}{Negative Result}
Input gradient methods do \textbf{not} reliably highlight discriminative features on standard image benchmarks
\end{alertblock}

DiffROAR $\approx 0$ for most methods on SVHN, FashionMNIST, CIFAR-10, ImageNet-10
\end{column}
\begin{column}{0.48\textwidth}
\begin{exampleblock}{Key Nuance}
Feature leakage explains apparent successes:
\begin{itemize}
\item BlockMNIST works due to spatial separation
\item Not evidence of general semantic understanding
\end{itemize}
\end{exampleblock}
\end{column}
\end{columns}

---

# Discussion Questions: DiffROAR

1. DiffROAR requires **retraining** — is this a realistic evaluation paradigm in practice?
2. Does the feature leakage hypothesis generalize beyond synthetic datasets?
3. Can attribution methods be designed to be provably robust to feature leakage?
4. If attribution methods don't highlight discriminative features, what are they actually highlighting?

---

# Paper 2: On the Privacy Risks of Algorithmic Recourse

\begin{center}
\includegraphics[width=0.92\columnwidth]{imgs/privacy_title.png}
\end{center}

---

# Privacy Risks in XAI

\small

\begin{alertblock}{Central Question}
Can XAI mechanisms — specifically \textbf{algorithmic recourse} — leak private information about training data?
\end{alertblock}

\begin{center}
\includegraphics[width=0.62\columnwidth]{imgs/privacy_motivation.png}
\end{center}

\vspace{-0.6em}

\footnotesize
\begin{itemize}
\item XAI outputs are information channels: they can reveal more than the intended explanation.
\item This paper focuses on whether recourse can leak \textbf{training-set membership}.
\end{itemize}

---

# Algorithmic Recourse

**Context:** a rejected loan applicant receives actionable steps to get approved

$$x' = \arg\min_{x' \in \mathcal{A}^p} \ell(f_\theta(x'), 1) + \lambda \cdot c(x, x')$$

- $x'$: counterfactual (the recourse)
- $c(x, x')$: cost/distance from $x$ to $x'$
- $\mathcal{A}^p$: set of actionable features

\begin{definition}{}
\textbf{CFD (Counterfactual Distance):} $c(x, x')$ — distance from input $x$ to its recourse $x'$
\end{definition}

\begin{block}{Why CFD matters}
The recourse algorithm outputs not only a counterfactual $x'$, but also a distance $c(x,x')$ that can be used as a statistic.
\end{block}

---

# Previous Works

\begin{center}
\includegraphics[width=0.68\columnwidth]{imgs/privacy_mi_attribution.png}
\end{center}

\small

\begin{columns}[T]
\begin{column}{0.48\textwidth}
\textbf{MI via Feature Attribution}
\begin{itemize}
\item Shokri et al.: attribute $\to$ infer membership
\item Requires \textbf{multiple queries}
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\textbf{Model Extraction via Counterfactuals}
\begin{itemize}
\item Repeated counterfactual queries
\item Also requires \textbf{many queries}
\end{itemize}

\begin{alertblock}{Limitation}
Prior attacks assume multiple queries — impractical for real recourse systems
\end{alertblock}
\end{column}
\end{columns}

---

# Contributions

\begin{exampleblock}{Novel Contribution}
First \textbf{single-query} membership inference (MI) attack using counterfactual distances
\end{exampleblock}

1. **CFD Thresholding Attack**: simple threshold on counterfactual distance
2. **CFD LRT Attack**: likelihood ratio test using shadow models (more powerful)
3. **Theoretical bounds**: DP-based upper bounds on adversary success
4. **Empirical evaluation**: diverse datasets (Adult, HELOC, Diabetes) and recourse methods (SCFE, GS, CCHVAE)

[@pawelczyk2022privacy]

---

# MI Attacks: Background

\begin{block}{Attack objective}
Given a target instance, decide whether it belonged to the model owner's training set.
\end{block}

\begin{columns}[T]
\begin{column}{0.48\textwidth}
\textbf{Loss Thresholding}

\begin{itemize}
\item Training samples often have lower loss than test samples
\item $M_\text{Loss}$ predicts MEMBER when $\ell(f(x),y)$ is below a threshold
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\textbf{Loss LRT}

\begin{itemize}
\item Uses shadow models to estimate loss/confidence distributions
\item Predicts membership by comparing likelihoods
\item More powerful than simple thresholding
\end{itemize}
\end{column}
\end{columns}

---

# Attack Assumptions

\begin{center}
\includegraphics[width=0.78\columnwidth]{imgs/privacy_attack_assumptions.png}
\end{center}

\begin{exampleblock}{Important Distinction}
Recourse-based attacks do not require true labels, the model loss, or direct query access to the predictive model.
\end{exampleblock}

- CFD attacks need access to the recourse system $\mathcal{R}$
- CFD LRT additionally assumes sample access to the data distribution $\mathcal{D}^N$

---

# Recourse-based MI Game

**Owner $O$** (model provider):

1. Trains $f_\theta$ on training set $S$
2. Provides recourse $\mathcal{R}(x) \to x'$ when queried

**Adversary $\mathcal{A}$** (attacker):

1. Queries $\mathcal{R}(x)$ for target sample $x$
2. Receives CFD $= c(x, x')$
3. Predicts: is $x \in S$?

\begin{alertblock}{Single-Query Constraint}
The adversary can only query the recourse system \textbf{once} per sample — making this a realistic threat model
\end{alertblock}

---

# Intuition: Why CFD Works

\footnotesize

\begin{center}
\includegraphics[width=0.54\columnwidth]{imgs/privacy_intuition.png}
\end{center}

\vspace{-0.5em}

\begin{block}{Intuition}
Training samples tend to be \textbf{further from the decision boundary} (the model fits them well). Their counterfactuals require a larger shift $\Rightarrow$ larger CFD.
\end{block}

\vspace{-0.4em}

\begin{center}
\begin{tabular}{@{}p{0.45\textwidth}p{0.45\textwidth}@{}}
MEMBER $\to$ large CFD (far from boundary)
&
NON-MEMBER $\to$ small CFD (closer to boundary)
\end{tabular}
\end{center}

---

# Attack 1: CFD Thresholding

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/privacy_attack1.png}
\end{center}

$$M_\text{Distance}(x) = \begin{cases} \text{MEMBER} & \text{if } c(x, x') \geq \tau_D \\ \text{NON-MEMBER} & \text{otherwise} \end{cases}$$

- Simple and practical: only requires the recourse output $c(x, x')$
- $\tau_D$ chosen to maximize balanced accuracy at a given FPR

---

# Attack 2: CFD LRT Intuition

\begin{block}{LRT idea}
Use counterfactual distance as the statistic, then ask whether the observed CFD looks likely under member vs.\ non-member behavior.
\end{block}

\begin{columns}[T]
\begin{column}{0.48\textwidth}
\textbf{Full likelihood ratio}

$$
\Lambda =
\frac{\Pr[c(x,x') \mid x \in D_t]}
{\Pr[c(x,x') \mid x \notin D_t]}
$$

\begin{itemize}
\item Inspired by loss-based LRT attacks
\item Uses recourse distance instead of model loss
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\textbf{Practical one-sided version}

\begin{itemize}
\item Exact member likelihood is computationally expensive
\item Estimate the non-member CFD distribution using shadow models
\item Test the observed CFD against a threshold for target FPR $\alpha$
\end{itemize}
\end{column}
\end{columns}

---

# Attack 2: CFD LRT Algorithm

\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/privacy_cfd_lrt.png}
\end{center}

\begin{exampleblock}{Advantage}
Leverages distributional information from shadow models — more powerful than simple thresholding in higher-dimensional settings
\end{exampleblock}

---

# Privacy Bounds via Differential Privacy

\vspace{0.8em}

\begin{block}{Theorem 1}
If the model training mechanism is $\varepsilon$-DP, then for any MI adversary $\mathcal{A}$:
$$\text{BA}_{\mathcal{A}} \leq \frac{1}{2} + \frac{1 - e^{-\varepsilon}}{2}$$
\end{block}

\begin{alertblock}{DP is Not a Silver Bullet}
Small $\varepsilon$ bounds adversary success — but significantly degrades recourse quality (utility-privacy tradeoff)
\end{alertblock}

---

# Experimental Setup

\small

\begin{columns}[T]
\begin{column}{0.48\textwidth}
\textbf{Datasets:}

\begin{itemize}
\item Adult (income prediction)
\item HELOC (credit risk)
\item Diabetes
\item Synthetic (controlled)
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\textbf{Recourse Methods:}

\begin{itemize}
\item SCFE
\item GS (Growing Spheres)
\item CCHVAE
\end{itemize}

\textbf{Baselines:} $M_\text{Loss}$ threshold, Loss LRT
\end{column}
\end{columns}

---

# Attack Efficiency: ROC Curves (SCFE)

\begin{center}
\includegraphics[width=0.96\columnwidth]{imgs/privacy_roc_scfe.png}
\end{center}

\begin{block}{How to read}
Curves above the random diagonal indicate membership signal at that false-positive rate.
\end{block}

---

# Attack Efficiency: ROC Curves (GS)

\begin{center}
\includegraphics[width=0.96\columnwidth]{imgs/privacy_roc_gs.png}
\end{center}

\begin{block}{How to read}
The low-FPR region is especially important: even a small high-confidence leakage can be privacy-relevant.
\end{block}

---

# Attack Efficiency: ROC Curves (CCHVAE)

\begin{center}
\includegraphics[width=0.78\columnwidth]{imgs/privacy_roc_cchvae.png}
\end{center}

\begin{exampleblock}{Key Takeaway}
CFD LRT is often above the random baseline, especially on HELOC — counterfactual distances can carry membership signal.
\end{exampleblock}

---

# Effect of Feature Dimensionality

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/privacy_num_features.png}
\end{center}

\begin{alertblock}{Finding}
Higher-dimensional feature spaces $\Rightarrow$ greater MI attack success
\end{alertblock}

More features $\to$ richer counterfactual signal $\to$ more distinguishable CFD distributions

---

# Effect of Model Architecture

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/privacy_model_arch.png}
\end{center}

\begin{alertblock}{Finding}
More complex model architectures $\Rightarrow$ greater MI attack success
\end{alertblock}

Complex models memorize training data more strongly $\to$ larger margin for training samples $\to$ larger CFD gap

---

# Conclusion: Privacy Risks

\begin{columns}[T]
\begin{column}{0.48\textwidth}
\textbf{Novel Attacks}

\begin{itemize}
\item Leverage recourses to infer training data membership
\item MI attacks using counterfactual distances (\textbf{CFD})
\item \textbf{Single-query} — practical threat model
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\textbf{Evidence of Privacy Leakage}

\begin{itemize}
\item Recourse algorithms carry membership signal
\item \textbf{Explainability-privacy tradeoff} is real
\item Attacks effective across diverse domains (lending, healthcare, law)
\end{itemize}
\end{column}
\end{columns}

---

# Limitations

- CFD is only a **heuristic** — an approximation of distance to the decision boundary
- Single-query assumption (adversary can only query once per sample)
- Must assume adversary knows the optimal threshold maximizing TPR at fixed FPR
- Paper highlights the **problem**, not yet a **solution**
- Evaluated on binary classification tasks only

---

# Future Work

- **Generalization**: can recourse lead to reconstruction attacks or attacks on training data statistics?
- **Other XAI mechanisms**: which other explanation methods involve privacy violations?
- **Solutions to protect privacy**: train models that provide recourse while mitigating privacy risks
  - How to construct faithful explanations that don't leak training data?
  - What is the privacy-utility trade-off?

[@pawelczyk2022privacy]

---

# Discussion Questions: Privacy Risks

1. Given the explainability-privacy tradeoff, what is the role of **ML practitioners** vs.\ **end users** in setting explainability and privacy benchmarks?
2. Both privacy and explainability cultivate user *trust* in ML models. In what situations would you prioritize one pillar over the other?
3. Besides recourse, what other XAI mechanisms might lead to privacy violations?
4. Is it even possible to have **private explanations**? Is this worth pursuing?

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References {.allowframebreaks}

\footnotesize
