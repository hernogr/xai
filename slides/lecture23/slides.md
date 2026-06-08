---
title: "Chain-of-Thought Prompting: Eliciting Reasoning in LLMs"
bibliography: references.bib

---

# Disclaimer

\input{../disclaimer.tex}

---

# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

\vfill


[@wei2022chain]



---

# Introduction & Related Work

---

# Challenges in LLMs

- Scaling up model size alone has not proved sufficient for achieving high performance on challenging tasks such as arithmetic, commonsense, and symbolic reasoning.
- Large language models still have limitations in their ability to reason and understand the context of a situation.

---

# Previous Work

- Models can generate intermediate natural language steps by training from scratch [@ling2017program] or finetuning a pretrained model [@cobbe2021training].
    - Costly to create large sets of high-quality rationales.
- Large language models offer the prospect of in-context few-shot learning via prompting [@brown2020language].
    - Works poorly on tasks that require reasoning abilities.
    - Often does not improve substantially with increasing model scale.

---

# Contribution

- Explores few-shot prompting for reasoning tasks using prompts structured as triples: $\langle \text{input},\ \textit{chain of thought},\ \text{output} \rangle$.
    - **Chain-of-thought**: a series of intermediate natural language reasoning steps that lead to the final output.
- Presents empirical evaluations on arithmetic, commonsense, and symbolic reasoning benchmarks, showing that chain-of-thought prompting outperforms standard prompting.

[@wei2022chain]

---

# Methodology

---

# How Do We Solve Complicated Problems?

Decompose the problem into intermediate steps and solve each before giving the final answer.

\begin{exampleblock}{Example}
\textit{"After Jane gives 2 flowers to her mom she has 10 \ldots\ then after she gives 3 to her dad she will have 7 \ldots\ so the answer is 7."}
\end{exampleblock}

\vspace{0.5em}
The paper shows sufficiently large LMs can generate chains of thought if demonstrations of chain-of-thought reasoning are provided as few-shot prompting.

---

# Standard vs Chain-of-Thought Prompting

\begin{center}
\includegraphics[width=0.92\columnwidth]{imgs/cot_vs_standard.png}
\end{center}

---

# Benefits of Chain-of-Thought

1. Allows models to decompose multi-step problems into intermediate steps, allocating more computation where needed.
2. Provides an interpretable window into the model's reasoning process.
3. Potentially applicable to any task requiring a multi-step approach.
4. Can be induced simply by including chain-of-thought examples in the prompt.

[@wei2022chain]

---

# Sensitivity to Prompt Engineering

Chain-of-thought is robust to:

1. Different annotators writing prompts.
2. Annotators without machine learning background.
3. Different types, ordering, and number of prompt examples.
4. Different language models (LaMDA, GPT-3, PaLM).

\vspace{0.5em}
However, prompt engineering still improved performance significantly in many cases.

---

# Robustness: Number of Exemplars

\begin{center}
\includegraphics[width=0.88\columnwidth]{imgs/robustness_exemplars.png}
\end{center}

\footnotesize Figure: CoT improvement over standard prompting is robust to varying the number of few-shot exemplars.

---

# Experiments & Results

---

# Experimental Setup — Benchmarks

**Benchmarks** (five math word problem datasets):

- GSM8K [@cobbe2021training]
- SVAMP [@patel2021nlp]
- ASDiv [@miao2020diverse]
- AQuA
- MAWPS [@koncel2016mawps]

\begin{center}
\includegraphics[width=0.75\columnwidth]{imgs/prompt_example.png}
\end{center}

---

# Experimental Setup — Models

**Baseline**: standard few-shot prompting [@brown2020language].

**Chain-of-thought** prompting tested on five LLMs:

- GPT-3 [@brown2020language]
- LaMDA [@thoppilan2022lamda]
- PaLM
- UL2 20B [@tay2022ul2]
- Codex [@chen2021evaluating]

---

# Results — Arithmetic Reasoning

Three key takeaways:

- Chain-of-thought prompting is an **emergent ability of model scale**.
- Larger performance gains for **more-complicated problems**.
- GPT-3 175B and PaLM 540B **compare favorably** to prior state of the art.

\begin{center}
\includegraphics[width=0.72\columnwidth]{imgs/results_arithmetic.png}
\end{center}

---

# Ablation Study

**Three variations compared against full chain-of-thought:**

- Equation only
- Variable compute only
- Chain-of-thought after the answer

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/ablation.png}
\end{center}

---

# Robustness of Chain-of-Thought

**Findings:** chain-of-thought prompting for arithmetic reasoning is robust to:

- Annotators
- Independently-written chains of thought
- Different exemplars and exemplar orders
- Various language models
- Varying numbers of exemplars

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/robustness_annotators.png}
\end{center}

---

# Commonsense Reasoning

---

# Commonsense & Symbolic: Example Prompts

\begin{center}
\includegraphics[width=0.92\columnwidth]{imgs/commonsense_examples.png}
\end{center}

---

# Results — Commonsense Reasoning

- Chain-of-thought prompting works better when the model is **sufficiently large**.

\begin{center}
\includegraphics[width=0.92\columnwidth]{imgs/results_commonsense.png}
\end{center}

---

# Symbolic Reasoning

---

# Results — Symbolic Reasoning (OOD)

- **In-domain and out-of-domain** evaluations show CoT enables length generalization.

\begin{center}
\includegraphics[width=0.88\columnwidth]{imgs/results_symbolic.png}
\end{center}

---

# Limitations & Discussion

\begin{alertblock}{Limitations}
\begin{itemize}
  \item CoT emulates human reasoning but does not prove the network actually "reasons."
  \item Emergence only at large model scales makes deployment costly.
\end{itemize}
\end{alertblock}

\begin{block}{Discussion Questions}
\begin{itemize}
  \item What reasoning tasks may not be well-suited to chain-of-thought?
  \item What other prompting methods might expand LM capabilities?
  \item Does chain-of-thought truly improve interpretability?
\end{itemize}
\end{block}

---

# Can Language Models Learn from Explanations in Context?

\vfill

[@lampinen2022language]



---

# Introduction

- Language models can perform new tasks by adapting to a few in-context examples (**few-shot learning**) [@brown2020language].
- **Key question:** Could including few-shot *explanations* of the answers in these examples improve LM performance?

---

# Setup: Training vs Evaluation

\begin{center}
\includegraphics[width=0.88\columnwidth]{imgs/setup_explanation.png}
\end{center}

\footnotesize The model sees task instruction + few-shot examples with post-answer explanations, then is evaluated on a new target question.

---

# Related Work

- **In-context learning**: Min et al. (2022) show ground truth labels matter less than label space/distribution; Webson & Pavlick (2021) question whether models truly understand prompts.
- **Explicit instructions**: Liu et al. (2021) show task descriptions help; Wei et al. (2022) show step-by-step reasoning improves few-shot performance.
- **This paper** focuses specifically on the effect of **post-answer** explanations — distinct from chain-of-thought which places reasoning *before* the answer.

[@lampinen2022language]

---

# Research Questions

- Can language models benefit from explanations when learning from examples in-context?
- Do few-shot explanations help the model "understand" the task better?
- What kind of in-context learning abilities do LMs exhibit more generally?

---

# Contributions & Main Findings

- Annotated **40 challenging tasks** from BIG-Bench with human-written explanations.
- Evaluated the effect of **post-answer explanations** (contrast to Wei et al.'s pre-answer chains).

\begin{exampleblock}{Key findings}
\begin{itemize}
  \item Explanations improve LLM performance compared to matched control conditions.
  \item Explanations tuned on a small validation set yield even larger gains.
\end{itemize}
\end{exampleblock}

[@lampinen2022language]

---

# Methods: Data & Model

**Data:** 40 challenging tasks from BIG-Bench, including:

- Inferring goals from actions
- Reasoning about mathematical induction
- Reasoning about causality
- Inferring assumptions behind statements

**Model:** Decoder-only Transformer LMs (Gopher family: 1B, 7B, 280B parameters), evaluated with the same context window and training data.

---

# Methods: Explanation Annotation

- One author annotated **15 examples per task** with human explanations (restricted to multiple-choice tasks).
- Three **control conditions** to isolate the causal effect of explanations:
    - *True non-explanations*: relevant but non-explanatory text.
    - *Other item explanations*: explanations drawn from a different task example.
    - *Scrambled explanations*: words of the explanation randomly reordered.
- **Explanation fine-tuning**: greedily select best 5-shot prompt on a 10-example validation set; also hand-tune explanation wording.

---

# Methods: Evaluation

- Results modeled with **hierarchical logistic regression** to account for:
    - Task difficulty
    - Shared content between prompts
- Each effect estimated at the appropriate level of the hierarchy, quantifying the **unique added contribution** of each prompt component.

---

# How Much Do Explanations Help?

\begin{center}
\includegraphics[width=0.90\columnwidth]{imgs/control_conditions.png}
\end{center}

\footnotesize Three controls test whether it is the explanation *itself* (vs. relevant words, syntactic structure) that drives improvement.

---

# Effect Size (Gopher 280B)

\begin{center}
\includegraphics[width=0.88\columnwidth]{imgs/effect_size.png}
\end{center}

\footnotesize Untuned explanations add $\sim\!\frac{1}{3}$ the effect of few-shot examples. Hand-tuned and selected explanations reach effect sizes comparable to examples alone.

---

# Selection vs Untuned Explanations

\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/selection_vs_untuned.png}
\end{center}

- Untuned explanations are **slightly beneficial on average** but can hurt in many instances.
- **Selection** (greedy 5-shot prompt chosen on validation set) shows a clearer, more consistent benefit.

---

# When Do Explanations Help?

\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/when_help.png}
\end{center}

- Explanations help most when the model is **uncertain** (low baseline score).
- When the model is already correct, explanations can slightly hurt — suggesting a *zone of proximal effect*.

---

# Is Scale Necessary?

\begin{center}
\includegraphics[width=0.78\columnwidth]{imgs/scale.png}
\end{center}

- No benefit at **1B or 7B** parameters.
- Untuned explanations help modestly only at **280B**; selection emerges clearly at that scale.
- Consistent with prior scaling work [@brown2020language; @wei2022emergent].

---

# Not All Tasks Are Created Equal

\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/task_categories.png}
\end{center}

- Explanations help most for **Logic, Mathematics, and Negation** tasks at large scale.
- Causal and linguistic tasks show weaker or inconsistent gains.

---

# Discussion

\begin{block}{Open questions}
\begin{itemize}
  \item Can explanations improve few-shot learning? \textbf{Yes, with sufficient scale and quality.}
  \item Why are post-answer explanations interesting? They decouple reasoning from generation and have no test-time cost.
  \item What do results imply about in-context learning? LMs can extract semantic content from explanations, not just surface structure.
  \item How do explanations relate to instructions? They appear complementary.
  \item How does this relate to human language processing? LMs differ — they lack broader world context.
\end{itemize}
\end{block}

---

# Class Discussion

- Is the dataset large (~600 samples) / diverse (40 tasks) enough to support the conclusions?
- Is the degree of improvement offered by explanations practically significant?
- How does this compare to other in-context learning methods?
    - Chain-of-thought [@wei2022chain]
    - Soft prompts / prompt tuning
    - Finetuning + distillation (Alpaca)
- How could explanations benefit smaller models?

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References {.allowframebreaks}

\footnotesize
