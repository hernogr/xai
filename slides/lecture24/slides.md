---
title: "\\emoji{brain} XAI: LMs for Commonsense Reasoning \\& Contrastive Explanations"
bibliography: references.bib

---

# Disclaimer

\input{../disclaimer.tex}

---

\begin{center}
\Large\textbf{Explain Yourself!}\\
\Large\textbf{Leveraging Language Models for Commonsense Reasoning}\\
\vspace{0.5cm}
\normalsize Rajani, McCann, Xiong \& Socher\\
\vspace{0.3cm}
\footnotesize Presenters: Karly Hou, Eshika Saxena, Leonard Tang, Kat Zhang
\end{center}

---

# Introduction

- **Commonsense reasoning**: making human-like presumptions and judgements about ordinary situations
- Modern ML methods struggle with commonsense reasoning
- Explanations help verbalize reasoning that models learn while training
- Common sense Question Answering (CQA) dataset

\begin{exampleblock}{Example}
\textbf{Question:} While eating a \textit{hamburger with friends}, what are people trying to do?\\
\textbf{Choices:} \textbf{have fun}, tasty, or indigestion
\end{exampleblock}

\vspace{0.3cm}
\begin{center}
\textbf{How do these models perform reasoning and to what extent is that reasoning based on world knowledge?}
\end{center}

---

# Key Contributions: CoS-E Dataset

Common Sense Explanations (CoS-E): Collected human explanations (annotations and natural language explanations) to build on top of CQA

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/cos_e_examples_table.png}
\end{center}

---

# Key Contributions

1. Common Sense Explanations (CoS-E)
2. Commonsense Auto-Generated Explanations (CAGE)
3. CAGE outperforms best baseline by 10% and produces explanations to justify its predictions
4. Explanation transfer on two out-of-domain datasets

---

# Related Work: Commonsense Reasoning

- Commonsense reasoning datasets:
  - Story Cloze: predicting story ending from a set of plausible endings
  - Situations with Adversarial Generations (SWAG): predicting next scene based on initial event
- Models achieve human-level performance on some datasets
- Models struggle with understanding how pronouns resolve between sentences and world knowledge

- CQA addresses this by requiring models to infer from the question
- Language models perform poorly compared to human participants on CQA

\begin{center}
\textbf{Unclear: Do models actually do common-sense reasoning?}
\end{center}

---

# Related Work: Natural Language Explanations

- Rationale generation by highlighting complete phrases in input text that are sufficient to predict desired output [@lei2016rationale]
- Human-generated natural language explanations to train a semantic parser to generate noisy labeled data and train a classifier for generating explanations [@hancock2018training]
- Interpretability comes at the cost of loss in performance on Stanford Natural Language Inference dataset [@camburu2018snli]
- Multi-modal: Ensemble explanations and visual explanations improve performance [@rajani2018multimodal]

\begin{center}
\textbf{Do explanations for CQA lead to improved performance?}
\end{center}

---

# Related Work: Knowledge Transfer in NLP

- Reliance on transfer of knowledge through pre-trained word vectors (e.g. Word2vec, GloVe) and contextualized word vectors (more refined with general encoding)
- Language models trained from scratch on large amounts of data and fine-tuned on specific tasks perform well
  - Only a few parameters need to be learned from scratch
  - Perform well on small amounts of supervised data

- \textcolor{red}{Gap: Fine-tuned language models don't perform as well on CQA}

\vspace{0.3cm}
\begin{center}
\textbf{Can we leverage these models to generate explanations and show that these explanations capture common sense?}
\end{center}

---

\begin{center}
\vfill
\Large Common Sense Explanations (CoS-E)
\vfill
\end{center}

---

# Dataset Structure/Creation

- Based on the CQA dataset
- CoS-E provides natural-language explanations for the correct answer choice and highlights important words in the question
- Explanations generated using MTurk
- Goal: To show whether models are performing reasoning correctly

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/dataset_structure.png}
\end{center}

---

# Dataset Considerations

- *CoS-E-selected* refers to the highlighted words, *CoS-E-open-ended* refers to the explanations
- Quality control was performed on the annotations and explanations
- Even explanations that don't discuss the ground truth answer are useful

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/dataset_considerations_chart.png}
\end{center}

---

\begin{center}
\vfill
\Large Commonsense Auto-Generated Explanations (CAGE)
\vfill
\end{center}

---

# CAGE Phase 1

CAGE Phase 1:

- Provide CQA example alongside corresponding CoS-E explanation to a language model
- Train model to generate the CoS-E explanation

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/cage_phase1_diagram.png}
\end{center}

\footnotesize Conditioned on question tokens $\mathcal{Q}$, answer choice tokens $A_1, A_2, A_3$, and previously generated tokens $E_1, \ldots, E_{i-1}$. Trained to generate token $E_i$.

---

# CAGE Phase 2

CAGE Phase 2:

- Use language models to generate explanations for each example in the training and validation sets of CQA
- Provide CAGE explanations to a second model by concatenating it to the original input (question, answer choices, and language model output)

\begin{center}
\includegraphics[width=0.55\columnwidth]{imgs/cage_phase2_diagram.png}
\end{center}

\footnotesize A trained CAGE language model generates explanations for a downstream commonsense reasoning model (CSRM), which predicts one of the answer choices.

---

# CAGE Phase 1: Intuition

\begin{center}
\includegraphics[width=0.72\columnwidth]{imgs/cage_phase1_diagram.png}
\end{center}

\begin{center}
One training step for CAGE
\end{center}

---

# How is CAGE Trained?

- Language Model trained to generate explanations from question-answer choice pairs
- Use pretrained OpenAI GPT
- Fine-tuned on the CQA and CoS-E dataset combination
- Two possible settings:
  - **explain-then-predict (reasoning)**
  - **predict-then-explain (rationalization)**

---

# CAGE Notation

- Question $q$
- Answer choices $c_0, c_1, c_2$
- Correct answer $a \in \{c_0, c_1, c_2\}$
- CoS-E explanation $e_h$
- CAGE predicted explanation $e$

---

# Reasoning {.fragile}

- Model is fine-tuned on the question, answer choices, and explanation tokens, but **not** the actual label.

$$C_{RE} = \text{``}q,\ c_0,\ c_1,\ \text{or}\ c_2\text{?\ commonsense\ says\ ''}$$

- Objective Function (canonical conditional language modeling objective):

$$\sum_i \log P(e_i \mid e_{i-k}, \ldots, e_{i-1}, C_{RE};\ \Theta)$$

---

# Rationalization {.fragile}

- Model is now also given the ground truth label $a$:

$$C_{RA} = \text{``}q,\ c_0,\ c_1,\ \text{or}\ c_2\text{?\ } a\ \text{because ''}$$

- Objective Function is the same as before but also conditioned on the *label* $a$
- Thus, the explanations create rationalization that makes the model more interpretable

---

# Training Parameters

- Generate sequences of maximum length 20
- Batch Size: 36, Epochs: 10
- Selected the best model using BLEU and perplexity scores

---

\begin{center}
\vfill
\Large Commonsense Predictions with Explanations
\vfill
\end{center}

---

# CAGE Phase 2: Intuition

\begin{center}
\includegraphics[width=0.68\columnwidth]{imgs/cage_phase2_diagram.png}
\end{center}

---

# CAGE Inference

- Given human explanation from CoS-E or LM reasoning, can then perform predictions on CQA
- Simply concatenate Question, [Sep], Explanation, [Sep], Answer Choice as input to downstream CSRM (classifier)
- Use binary classification head on top of BERT backbone
  - 3 answer choices $\rightarrow$ 3 input sequences
  - Take sequence yielding highest confidence as output

---

# CSRM (BERT) Training Hyperparameters

- Train batch size: 24
- Test batch size: 12
- 10 training epochs
- Max sequence length of 50 for labels-only; 175 including explanations

---

\begin{center}
\vfill
\Large Experimental Results
\vfill
\end{center}

---

# Experimental Results: CQA with CoS-E

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/experimental_results_table2.png}
\end{center}

\begin{center}
\small Table 2: Results on CQA dev-random-split with CoS-E used during training.
\end{center}

---

# Experimental Results: Comparison with SOTA

\begin{columns}
\begin{column}{0.48\textwidth}
\begin{itemize}
\item Google search ``question + answer choice'' collected 100 top snippets per answer as context for \textbf{Reading Comprehension model}
\item Extra data did not improve accuracy
\item CAGE-reasoning resulted in \textbf{10\% accuracy gain} over previous SOTA
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\includegraphics[width=\columnwidth]{imgs/experimental_results_sota.png}
\end{column}
\end{columns}

---

# Experimental Results: Oracle Upper-Bound

\begin{columns}
\begin{column}{0.46\textwidth}
\includegraphics[width=\columnwidth]{imgs/experimental_results_oracle.png}

\small Table 4: Oracle results on CQA dev-random-split.
\end{column}
\begin{column}{0.50\textwidth}
\begin{itemize}
\item Oracle upper-bound: \textbf{human-generated explanations} from CoS-E provided during training and validation
\item Unfair setting because human had ground truth answer
\item ``CoS-E selected'': explanation consists of words humans selected as justification for model
\end{itemize}
\end{column}
\end{columns}

---

# Transferring Explanations Across Domains

- How well do natural language explanations transfer from CQA to SWAG and Story Cloze Test?
- Use GPT CAGE model fine-tuned on CQA train/dev to generate explanations on SWAG and Story Cloze Spring 2016 train/val
- Rinse and repeat using BERT with classifier head

---

# Experimental Results: Domain Transfer

\begin{columns}
\begin{column}{0.44\textwidth}
\includegraphics[width=\columnwidth]{imgs/transfer_results.png}
\end{column}
\begin{column}{0.52\textwidth}
\begin{itemize}
\item Camburu et al (2018): transferring explanations from SNLI to MultiNLI performs very poorly
\item Transfer of explanations on commonsense reasoning tasks
\item NLI has small fixed set of pre-defined labels unlike commonsense reasoning tasks (CQA, SWAG, Story Cloze)
\item \textbf{Adding explanations led to very small decrease in performance}
\end{itemize}
\end{column}
\end{columns}

---

\begin{center}
\vfill
\Large Qualitative Analysis
\vfill
\end{center}

---

# Analysis of CAGE

- CAGE-reasoning at train + validation $\rightarrow$ 72\% accuracy
- CoS-E-open-ended performance at 90\%---why the gap?
- Measure quality of CAGE:
  - Human evaluation (42\% CAGE vs 52\% CoS-E-open-ended)
  - BLEU score measures syntactical precision by n-gram overlap
  - Perplexity: token-level measure of how well language models predict next word
- Result: beneficial to fine-tune the LM, but humans and LMs have widely varying ways of providing useful explanations

---

# Analysis of Baseline BERT Model

- Error analysis on baseline BERT w/o explanations: performs poorly on longer/more compositional questions $\rightarrow$ explanations help
- CAGE reasoning typically simpler construction than CoS-E-open-ended, but adds meaningful context
- However, CAGE still provides ``incorrect'' answers often

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/baseline_bert_examples.png}
\end{center}

---

# Domain Transfer: SWAG + Story Cloze

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/domain_transfer_examples.png}
\end{center}

---

\begin{center}
\vfill
\Large Conclusion \& Group Discussion
\vfill
\end{center}

---

# Conclusion

- CoS-E on top of CommonsenseQA
- CAGE framework $\rightarrow$ LM leverages explanations
- Classifier on top of explanations
- SOTA performance on a difficult commonsense reasoning task
- Opens further avenues for studying explanation as it relates to interpretable commonsense reasoning

---

# Discussion Questions

- BLEU and perplexity as measures of goodness?
  - Has been shown multiple times to correlate poorly with human judgement
- Joint training of explanation and label? Not one prior to the other
- Can commonsense reasoning help general reasoning (e.g. mathematics, Fermi, counterfactual) in other domains?
- How to align human/machine explanations?
- Recent work (RLPrompt, AutoPrompt) has shown that optimal prompts for LMs are often gibberish
  - What does this say about the validity of using SOTA LMs for explanations?
  - Can we regularize LM training to better align with human reasoning?

---

\begin{center}
\Large\textbf{Interpreting Language Models}\\
\Large\textbf{with Contrastive Explanations}\\
\vspace{0.5cm}
\normalsize Kayo Yin \& Graham Neubig\\
\vspace{0.3cm}
\footnotesize Presented by Charumathi Badrinath, Eric Shen, Leonard Tang, and Skyler Wu
\end{center}

---

# Motivation + Example

- We've seen many interpretability and explanation strategies being applied to LMs, including transformer-based autoregressive LMs...
  - **Gradient-based/erasure-based feature attribution** methods provide a straightforward way to do this
  - Interpret each token of the input text as a feature
  - At each step, use gradients to calculate a **saliency score** to quantify the importance of each previous token to the model output (i.e. logit prediction for the next token)
- E.g. gradient $\times$ input

---

# Motivation + Example: How It Works

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/motivation_gradient_input.png}
\end{center}

---

# Motivation + Example: The Problem

- **Problem:** For many LMs, using typical gradient- or erasure-based methods doesn't provide informative explanations
- Most of the time, the token with the highest saliency is the token immediately before the prediction
- How can we create more meaningful attributions? By ***contrasting*** them with other token predictions.

\begin{center}
\includegraphics[width=0.55\columnwidth]{imgs/motivation_problem.png}
\end{center}

\begin{center}
\small\textit{Knowing the previous word is certainly very important for figuring out the next word, but that's not very helpful!}
\end{center}

---

# Main Contributions and Key Ideas

1. **Contrastive explanations:** why did the model predict one token *instead* of another? Extended previous methods.
2. **Grammatical consistency:** contrastive $>$ non-contrastive explanations w.r.t. verifying linguistic/grammatical phenomena.
3. **Human simulatability:** contrastive explanations help users better predict LLM behavior, also found to be more useful by humans.

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/contrastive_key_ideas.png}
\end{center}

\footnotesize \textcolor{red}{Red} = raises probability of ``barking,'' \textcolor{blue}{Blue} = decreases probability of ``barking,'' White = little influence.

---

# Background: GPT-2

- Authors focus on GPT-2 (1.5B) and GPT-Neo (2.7B) $\rightarrow$ very similar to each other
- **Training:** WebText dataset of 8 million web-pages
  - No task-specific supervised training = ``Multi-task training''
- **Objective:** predict the next word, given all previous words in input
- **Behavior:** ``chameleon-like,'' adapts to style + content of the input text
- **Architecture:** Transformer-based
  - ``Autoregressive'': outputs tokens one at a time, *but* each token generated is appended to the input sequence $\rightarrow$ fed back to model for next step

---

# Background: Gradient Norm Saliency Scores {.fragile}

- **Originally for image classification:** compute gradient of class score w.r.t. input image, take the norm.
  - Big gradient = big influence.
- **For LLMs:** compute gradient of next token logit w.r.t. current input.

$$g(x_i) = \nabla_{x_i} q(y_t \mid \mathbf{x})$$

$$S_{GN}(x_i) = \|g(x_i)\|_{L_1}$$

[@simonyan2013saliency]

---

# Background: Gradient $\times$ Input Saliency Scores {.fragile}

- **Method:** Similar gradient computation as Gradient Norm, simply replacing $L_1$ norm with dot product with input itself.

$$g(x_i) = \nabla_{x_i} q(y_t \mid \mathbf{x})$$

$$S_{GI}(x_i) = g(x_i) \cdot x_i$$

[@shrikumar2016gradientinput]

---

# Background: Input Erasure Saliency Scores {.fragile}

- **Intuition:** how does erasing different parts of the input affect the output?
- **Procedure:** compute difference in model outputs using full input vs. input with a specific token zeroed out. NOT gradient-based!

$$S_E(x_i) = q(y_t \mid \mathbf{x}) - q(y_t \mid \mathbf{x}_{\neg i})$$

[@li2016erasure]

---

# Background: Related Work + Limitations (Pt. 1)

- Non-contrastive saliency score methods:
  - Simonyan et al. 2013, Shrikumar et al. 2016, Li et al. 2016 --- not NLP specific!
  - Not very developed in NLP use cases.
  - When applied to NLP (Wallace et al. 2019), methods often \underline{\textbf{return last token before output as most influential.}}
- Adversarial Methods on NLP:
  - Wallace et al. 2019: HotFlip on NLPs, replace words to change model's prediction. AllenNLP suite.

---

# Background: Related Work + Limitations (Pt. 2)

- Counterfactual explanations in *text classification*:
  - Jacovi et al. 2021: erase features, project into ``contrastive space'' $\rightarrow$ measure importance by comparing class probabilities before/after erasure.
  - Unsure how to extend into *language modeling* space with much bigger input + output spaces.
- Contrastive methods are not new, just not used for NLP very much (Stepin et al. 2021, survey).

---

# Method: Contrastive Setup

- Simple modification to formulation of existing gradient-based explanations.
- **Contrastive** setup:

\begin{center}
\includegraphics[width=0.82\columnwidth]{imgs/method_contrastive.png}
\end{center}

---

# Method: Contrastive Saliency Formulas

Let $q(y_t|\mathbf{x})$ be the model output for token $y_t$, $S(x_i)$ the saliency score for token $x_i$ in input $\mathbf{x}$, and $\mathbf{x}_{\neg i}$ the input $\mathbf{x}$ where $x_i$ is zeroed out.

\begin{center}
\includegraphics[width=0.95\columnwidth]{imgs/method_formulas_table.png}
\end{center}

---

# Method: Back-Propagation in Contrastive Setting

\begin{center}
\includegraphics[width=0.88\columnwidth]{imgs/method_lm_diagram.png}
\end{center}

\begin{center}
\small Step 3 is changed: we calculate and back-propagate the \textbf{difference in logits} between $y_t$ and $y_f$.
\end{center}

---

# Evaluation: Grammatical Consistency

\textbf{Q:} Are contrastive explanations $\gg$ non-contrastive in identifying words that we think should influence the output token?

\begin{block}{Experimental Setup}
\begin{itemize}
\item \textbf{BLiMP dataset:} pairs of minimally different English sentences that contrast in grammatical acceptability under some linguistic paradigm
\item 5 linguistic phenomena with 12 paradigms
\item Used spaCy NLP library to extract grammatically relevant parts of each sentence
\end{itemize}
\end{block}

---

# Evaluation: BLiMP Linguistic Paradigms

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/blimp_table.png}
\end{center}

---

# Evaluation: Linguistic Consistency Metrics {.fragile}

- $S$ = explanation vector; $S_i$ = saliency of $x_i$
- $E$ = known evidence; $E_i = \mathbf{1}(x_i\ \text{grammatically influences output token})$
- $S \cdot E$ $\rightarrow$ sum of saliency scores of all input tokens that are part of evidence
- **Probes needed** $\rightarrow$ ranking of first token $x_i$ where $E_i = 1$ when sorted by decreasing saliency
- **MRR (mean reciprocal rank)** $\rightarrow$ average (over all sentences) of inverse rank of first $x_i$ where $E_i = 1$ sorted by descending saliency

---

# Findings: Linguistic Agreement

\begin{columns}
\begin{column}{0.50\textwidth}
\begin{itemize}
\item Contrastive explanations are more aligned with linguistic paradigms
\item Contrastive explanations have a better alignment with BLiMP than random vectors baseline
\item Non-contrastive explanations do \textbf{not} outperform random baseline
\end{itemize}
\end{column}
\begin{column}{0.47\textwidth}
\includegraphics[width=\columnwidth]{imgs/linguistic_agreement_bars.png}
\end{column}
\end{columns}

---

# Findings: Linguistic Agreement (Distance Effect)

\begin{columns}
\begin{column}{0.48\textwidth}
\begin{itemize}
\item Further apart \textit{known evidence} token is from \textit{target token} $\rightarrow$ larger increase in MRR alignment of contrastive cf. non-contrastive
\item Contrastive explanations can particularly capture model decisions requiring \textit{longer-range context}
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\includegraphics[width=\columnwidth]{imgs/linguistic_agreement_scatter.png}
\end{column}
\end{columns}

---

# Evaluation: Human Simulatability

\textbf{Q:} Do contrastive explanations increase users' ability to predict a model's output token (i.e. ``simulate'' model behavior)?

\begin{block}{Experimental Setup}
\begin{itemize}
\item Model = GPT-2; explanation = \{no explanation, $S_{GI}$, $S^*_{GI}$, $S_E$, $S^*_E$\}
\item 10 word pairs from BLiMP, 10 word pairs selected to maximize confusion score on WikiText-103 test split
\end{itemize}
\end{block}

\begin{center}
\includegraphics[width=0.60\columnwidth]{imgs/user_study.png}
\end{center}

---

# Findings: User Alignment

\begin{columns}
\begin{column}{0.52\textwidth}
\begin{itemize}
\item All four types of explanations help users simulate model behavior
\item \textit{Contrastive explanations} lead to \textit{more accurate simulations}
\item \textit{Contrastive explanations} are considered \textit{more useful}
\item Takeaway: contrastive explanations help human observers accurately simulate model predictions the most
\end{itemize}
\end{column}
\begin{column}{0.44\textwidth}
\includegraphics[width=\columnwidth]{imgs/user_alignment_table.png}
\end{column}
\end{columns}

---

# Evaluation: What Context Do Models Use?

\textbf{Q:} How do language models achieve various linguistic distinctions? Is similar evidence necessary to disambiguate foils that are similar linguistically?

\begin{block}{Experimental Setup}
\begin{itemize}
\item Targets = 10 most frequent words per major POS; Foils = 10000 most frequent vocab items
\item For each target $y_t$ select 500 sentences from WikiText-103
\item For each foil $y_f$ generate contrastive explanation $e(x_i, y_t, y_f)$ and concatenate
\item Apply k-means on explanation vectors $e(x_i, y_t, \text{all foils})$
\end{itemize}
\end{block}

\begin{alertblock}{Idea}
Explanation vectors represent \textit{type of context} needed to disambiguate foil from target
\end{alertblock}

---

# Findings: What Context Do Models Use?

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/context_decisions_table.png}
\end{center}

- (Paradigmatically) linguistically similar foils cluster together
- Examining cluster explanations yields insights into GPT-2 (``BERTology'')
  - Pronoun Ex: GPT-2 influenced by unrelated pronouns $\rightarrow$ produces incorrect gender

---

# Strengths / Weaknesses

\begin{columns}
\begin{column}{0.48\textwidth}
\textcolor{primarygreen}{\textbf{Strengths}}
\begin{itemize}
\item Simple yet effective modification applicable to a variety of feature attribution methods
\item Easy to compute, extensible to general LMs (including NMT)
\item Evaluated with interesting foil clustering analysis
\item Empirically shown to help with human observers (good for interpretability)
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\textcolor{red}{\textbf{Weaknesses}}
\begin{itemize}
\item Only applied to three feature attribution methods in the paper
\item Only GPT-2 and GPT-Neo used as LM examples
\item Human study very limited in scope
\item Does not attempt to look at model internals; saliency scores are arguably a crude approximation of interpretation
\end{itemize}
\end{column}
\end{columns}

---

# Questions for the Audience

- Given that LLMs often exhibit ``phase shifts'' at different sizes, to what extent do you expect the results to generalize to cutting-edge models like GPT-4?
- In practice, how would one create foils for free-response questions and/or general conversational use? How generalizable are these contrastive tools?
- How effective do you think saliency scores (through gradient/erasure-based methods) are for achieving interpretability?
- How much do we trust the GPT-2 embeddings (primary workhorse for most methods) and the generalizability of the authors' results?

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References {.allowframebreaks}

\footnotesize
