---
title: "XAI Lecture 23"
subtitle: "Understanding and Reasoning in Large Language Models"
bibliography: references.bib
suppress-bibliography: true
---

# Disclaimer

\input{../disclaimer.tex}

---

# Paper 1

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/paper1_title.png}
\end{center}

[@wei2022chain]

---

# Introduction 

**Challenges in Large language models (LLMs)**

- LLMs have limitations in their ability to reason and understand the context of a situation.
- Scaling up model size alone has not proved sufficient for achieving high performance on challenging tasks, such as *arithmetic, commonsense, and symbolic reasoning*.

**Previous work**

- LLMs have the ability to generate natural language intermediate steps by training from scratch [@ling2017program] or finetuning a pretrained model [@cobbe2021training].
  - It is costly to create a large set of high quality rationales.
- LLMs offer the exciting prospect of in-context few-shot learning via *prompting* [@brown2020language].
  - Works poorly on tasks that require reasoning abilities.
  - Often does not improve substantially with increasing model scale.

---

# Contribution

- Combining few-shot prompting with explicit intermediate reasoning steps, avoiding the limitations of both prior approaches.
  - Prompts consist of triples $\langle\text{input},\ \textit{\text{chain of thought}}, \ \text{output}\rangle$
  - Chain of thought (CoT): series of intermediate natural language reasoning steps leading to the final answer.
  - No large training dataset required --- a single model checkpoint can perform many tasks without loss of generality.
- Showing sufficiently large LMs can generate CoT if demonstrations are provided as few-shot prompting.
- Empirical evaluations on **arithmetic, commonsense, and symbolic reasoning** benchmarks, showing that CoT prompting outperforms standard prompting.

---

# CoT Prompting

When solving a complex reasoning task, we naturally tend to decompose it into intermediate steps and solve each one before giving the final answer.

\begin{exampleblock}{Example}
\textit{"After Jane gives 2 flowers to her mom she has 10 \ldots\ then after she gives 3 to her dad she will have 7 \ldots\ so the answer is 7."}
\end{exampleblock}

**Goal of the paper:** to endow LLMs with the ability to generate a similar CoT—a coherent series of intermediate reasoning steps that lead to the final answer for a problem.

---

# Standard Prompting vs. CoT Prompting 

\begin{center}
\includegraphics[width=0.95\columnwidth]{imgs/standard_vs_cot.png}
\end{center}

---

# More examples of CoT Prompting

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/cot_examples.png}
\end{center}

---

# Benefits of Chain-of-Thought

1. Allows models to decompose multi-step problems into intermediate steps so additional computation can be allocated to problems that require more reasoning steps.

2. Provides an interpretable window into the behavior of the model, suggesting how it might have arrived at a particular answer and providing opportunities to debug where the reasoning path went wrong (although fully characterizing a model’s computations that support an answer remains an open question).

3. Potentially applicable to any task that requires a multi-step approach.

4. Can be readily elicited in sufficiently large off-the-shelf LLMs simply by including examples of CoT sequences while prompting.

---

# General Experimental Setup

**Objective**: to observe the utility of CoT prompting for *arithmetic reasoning*, *commonsense reasoning*, and *symbolic reasoning*.

**Prompts**:

- Baseline: standard few-shot prompting [@brown2020language], where exemplars are formatted as questions and answers.
- Chain-of-thought: augment each exemplar in few-shot prompting with a CoT for an associated answer.

**Models**:

- GPT-3   [@brown2020language].
- LaMDA   [@thoppilan2022lamda].
- PaLM    [@chowdhery2022palm].
- UL2 20B [@tay2022ul2].
- Codex   [@chen2021evaluating].

---

# Arithmetic Reasoning: Experimental Setup

:::: columns
::: {.column width="48%"}

\vspace{1em}

**Benchmarks:**

- **GSM8K** [@cobbe2021training]
- **SVAMP** [@patel2021nlp]
- **ASDiv** [@miao2020diverse]
- **AQuA**  [@ling2017program]
- **MAWPS** [@koncel2016mawps]

:::
::: {.column width="52%"}

\begin{center}
\includegraphics[height=0.55\textheight]{imgs/arithmetic_reasoning.png}
\end{center}

:::
::::

---

# Arithmetic Reasoning: Results

:::: columns
::: {.column width="35%"}

\vspace{1em}

**Three key takeaways:**

- CoT prompting is an emergent ability of **model scale**.
- Larger performance gains for **more-complicated problems**.
- GPT-3 175B and PaLM 540B **compare favorably to prior state of the art**.

:::
::: {.column width="65%"}

\begin{center}
\includegraphics[height=0.78\textheight]{imgs/results_arithmetic.png}
\end{center}

:::
::::

---

# Ablation Study

:::: columns
::: {.column width="52%"}

\vspace{1em}

A study with three variations:

- **Equation only:** only the math equation, no natural language.
  - Still fails on hard problems --- semantics matter.
- **Variable compute only:** dots (`...`) matching CoT length (same tokens, no reasoning).
  - No improvement --- extra compute alone is not enough.
- **Chain of thought after answer:** reasoning appears *after* the answer.
  - Also fails --- sequential reasoning *before* the answer is essential.

:::
::: {.column width="48%"}

\begin{center}
\includegraphics[height=0.7\textheight]{imgs/ablation.png}
\end{center}

:::
::::

---

# Robustness of Chain of Thought

:::: columns
::: {.column width="52%"}

\vspace{1em}

Chain of thought is robust to:

1. Independently-written chains of thought:
   1. Different annotators.
   2. Annotators without ML background.
2. Different types, ordering, and number of exemplars.
3. Different language models (LaMDA, GPT-3, PaLM).

However, prompt engineering improved performance significantly in many cases.

:::
::: {.column width="48%"}

\begin{center}
  \includegraphics[width=\columnwidth,height=0.75\textheight,keepaspectratio]{imgs/robustness_cot.png}
  \smallskip \\
  \footnotesize{Figure shows results for LaMDA 137B.}
\end{center}

:::
::::

---

\begin{center}
  \includegraphics[width=\columnwidth,height=0.75\textheight,keepaspectratio]{imgs/number_examples_few-shot.png}
  \smallskip \\
  \footnotesize{Figure shows results for LaMDA 137B.}
\end{center}

---

# Commonsense Reasoning: Experimental Setup

:::: columns
::: {.column width="48%"}

\vspace{1em}

**Benchmarks:**

- **CSQA** [@talmor2019commonsenseqa].
- **StrategyQA** [@geva2021strategyqa].
- **Date Understanding** (set from the BIG-bench [@srivastava2022bigbench]).
- **Sports Understanding** (set from the BIG-bench [@srivastava2022bigbench]).
- **SayCan** [@ahn2022saycan].

:::
::: {.column width="52%"}

\begin{center}
\includegraphics[height=0.55\textheight]{imgs/commonsense_example.png}
\end{center}

:::
::::

---

# Commonsense Reasoning: Results

- CoT gains scale with model size: PaLM 540B achieves best results across all benchmarks.
- New SOTA on StrategyQA: 75.6% vs. prior best 69.4%.
- Surpasses human baseline on Sports Understanding: 95.4% vs. 84%.
- Minimal gains on CSQA: CoT benefits complex multi-step reasoning more than factual recall.

---

# Commonsense Reasoning: Results

\begin{center}

\includegraphics[height=0.42\textheight]{imgs/commonsense_reasoning2.png}

\vspace{0.4cm}

\includegraphics[height=0.24\textheight]{imgs/commonsense_reasoning1.png}

\vspace{0.15cm}

{\footnotesize Figure above shows results for PaLM.}

\end{center}

---

# Symbolic Reasoning: Experimental Setup

**Tasks:**

- **Last Letter Concatenation:** concatenate the last letters of words in a name (e.g., "Lady Gaga" → "ya").
- **Coin Flip:** track whether a coin is heads or tails after a series of flips.

**Evaluation:**

- **In-domain (ID):** test examples of the same length as the few-shot demonstrations.
- **Out-of-domain (OOD):** test examples with more steps than shown in the prompt --- evaluates length generalization.

---

# Symbolic Reasoning: Results

- CoT enables **length generalization**: solves longer sequences than those shown in few-shot examples.
- Standard prompting fails completely on OOD symbolic tasks --- CoT succeeds.
- PaLM 540B achieves near-perfect accuracy on ID tasks.
- Again, emergent ability: benefits only appear at models with 100B+ parameters.

---

# Symbolic Reasoning: Results

:::: columns
::: {.column width="45%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.75\textheight,keepaspectratio]{imgs/symbolic_reasoning1.png}
\smallskip \\
{\footnotesize Figure above shows results for PaLM.}
\end{center}

:::
::: {.column width="55%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.75\textheight,keepaspectratio]{imgs/symbolic_reasoning2.png}
\end{center}

:::
::::

---

# Conclusion

Through experiments on arithmetic, symbolic, and commonsense reasoning, we find that chain-of-thought reasoning is an emergent property of model scale that allows sufficiently large language models to perform reasoning tasks that otherwise have flat scaling curves.

---

# Limitations \& Discussion

\begin{alertblock}{Limitations}
\begin{itemize}
  \item CoT emulates human reasoning but does not prove the network actually "reasons".
  \item Emergence only at large model scales makes deployment costly.
  \item Generated chains of thought can be incorrect even when the final answer is right.
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

# Paper 2

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/paper2_title.png}
\end{center}

[@lampinen2022explanations]

---

# Introduction

- Language models (LMs) have been found to be able to perform new tasks by adapting to a few in-context examples [@brown2020language].
  - In-context example: an example (question + right answer) for a specific task prompt.
  - Few-shot: a few examples are given to guide the model.
- **Key question:** Could including few-shot *explanations* of the answers in these examples
  improve LM performance?

---

# Few-shot + Explanation

\begin{center}
\includegraphics[height=0.82\textheight, keepaspectratio]{imgs/few-shot_explanation.png}
\end{center}

---

# Related Work

**In-context and prompt-based learning:**

- Min et al., 2022: Find that ground truth labels don’t have a large effect on model performance, and identify other aspects (label space / distribution) that drive performance.
- Webson and Pavlick, 2021: Find limitation in models’ ability to truly understand the meaning of their prompts.

**Prompting with explicit instructions:**

- Liu et al., 2021: Prompting with explicit instructions or task descriptions helps LMs adapt to a task.
- Wei et al, 2022: Breaking down the steps of a reasoning process for LMs improve few-shot performance.

**This paper** focuses specifically on the effect of **post-answer** explanations --- distinct from chain-of-thought which places reasoning *before* the answer.

---

# Research Questions

- Can language models benefit from explanations when learning from examples in-context?
- Do few-shot explanations help the model "understand" the task better?
- What kind of in-context learning abilities do LMs exhibit more generally?

---

# Contributions

- Annotated **40 challenging tasks** from BIG-Bench with human-written explanations.
- Evaluated the effect of **post-answer explanations** (contrast to Wei et al.'s pre-answer chains).

\begin{block}{Key findings}
\begin{itemize}
  \item Explanations improve LLM performance compared to matched control conditions.
  \item Explanations tuned on a small validation set yield even larger gains.
\end{itemize}
\end{block}

---

# Methods: Data \& Model

**Data:** 40 tasks from BIG-Bench, including:

- Inferring goals from actions.
- Reasoning about mathematical induction.
- Reasoning about causality.
- Inferring assumptions behind statements.

**Model:** Decoder-only Transformer LMs (Gopher family: 1B, 7B, 280B parameters), evaluated
with the same context window and training data.

---

# Methods: Explanation Annotation

- One author annotated **15 examples per task** with human explanations (restricted to
  multiple-choice tasks).
- Three **control conditions** to isolate the causal effect of explanations:
  - *True non-explanations*: relevant but non-explanatory text.
  - *Other item explanations*: explanations drawn from a different task example.
  - *Scrambled explanations*: words of the explanation randomly reordered.
- **Explanation tuning**: greedily select best 5-shot prompt; also hand-tune explanation wording.

---

# Methods: Evaluation

- Results modeled with **hierarchical logistic regression** to account for:
  - Task difficulty.
  - Shared content between prompts.
- Each effect estimated at the appropriate level of the hierarchy, quantifying the **unique
  added contribution** of each prompt component.

---

# Effect Size (Gopher 280B)

\begin{center}
\includegraphics[width=0.75\columnwidth]{imgs/benefits_components.png}
\end{center}

---

# Selection vs. Untuned Explanations

\begin{center}
\includegraphics[width=0.75\columnwidth]{imgs/adding_explanations.png}
\end{center}

---

# When Do Explanations Help?

\begin{center}
\includegraphics[width=0.75\columnwidth]{imgs/when_explanations_help.png}
\end{center}

---

# Is Scale Necessary?

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/scale.png}
\end{center}

---

# Not All Tasks Are Created Equal

\begin{center}
\includegraphics[width=0.75\columnwidth]{imgs/tasks_clusters.png}
\end{center}

---

# Discussion

\begin{block}{Open questions}
\begin{itemize}
  \item Can explanations improve few-shot learning? Yes, with sufficient scale and quality.
  \item Why are post-answer explanations interesting? They decouple reasoning from generation
    and have no test-time cost.
  \item What do results imply about in-context learning? LMs can extract semantic content from
    explanations, not just surface structure.
  \item How do explanations relate to instructions? They appear complementary.
  \item How does this relate to human language processing? LMs differ --- they lack broader world
    context.
\end{itemize}
\end{block}

---

# Conclusion

- Including explanations with examples in a few-shot prompt can improve in-context task inference for language models. 
- Explanations that are tuned using a validation set are especially effective, but even untuned explanations have modest positive effects and outperform carefully matched control conditions. 
- However, in our experiments this capability only emerges in the largest models (although it is possible smaller models might benefit from more explanations, or on simpler tasks).

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References (1/2)

\scriptsize

\begin{list}{}{%
\setlength{\leftmargin}{1.2em}
\setlength{\itemindent}{-1.2em}
\setlength{\itemsep}{0.25em}
}

\item Ahn et al. (2022). \textit{Do As I Can, Not As I Say: Grounding Language in Robotic Affordances}.

\item Brown et al. (2020). \textit{Language Models Are Few-Shot Learners}.

\item Chen et al. (2021). \textit{Evaluating Large Language Models Trained on Code}.

\item Chowdhery et al. (2022). \textit{PaLM: Scaling Language Modeling with Pathways}.

\item Cobbe et al. (2021). \textit{Training Verifiers to Solve Math Word Problems}.

\item Geva et al. (2021). \textit{Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies}.

\item Koncel-Kedziorski et al. (2016). \textit{MAWPS: A Math Word Problem Repository}.

\item Lampinen et al. (2022). \textit{Can Language Models Learn from Explanations in Context?}.

\item Ling et al. (2017). \textit{Program Induction by Rationale Generation}.

\end{list}

---

# References (2/2)

\scriptsize

\begin{list}{}{%
\setlength{\leftmargin}{1.2em}
\setlength{\itemindent}{-1.2em}
\setlength{\itemsep}{0.25em}
}

\item Miao et al. (2020). \textit{A Diverse Corpus for Evaluating and Developing English Math Word Problem Solvers}.

\item Patel et al. (2021). \textit{Are NLP Models Really Able to Solve Simple Math Word Problems?}.

\item Rae et al. (2021). \textit{Scaling Language Models: Methods, Analysis and Insights from Training Gopher}.

\item Srivastava et al. (2022). \textit{Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models}.

\item Talmor et al. (2019). \textit{CommonsenseQA}.

\item Tay et al. (2022). \textit{UL2: Unifying Language Learning Paradigms}.

\item Thoppilan et al. (2022). \textit{LaMDA: Language Models for Dialog Applications}.

\item Wei et al. (2022). \textit{Chain-of-Thought Prompting Elicits Reasoning in Large Language Models}.

\end{list}