---
title: "XAI Lecture 24 --- Explaining LLM Reasoning"
subtitle: "Background, then two papers: \\emph{generate} the reasoning (Rajani 2019) and \\emph{localise} the evidence (Yin \\& Neubig 2022)"
author: "FAMAF - UNC"
date: "First Semester 2026"
bibliography: references.bib
---

# Disclaimer

\input{../disclaimer.tex}

# Background --- the problem before the two papers

Both papers attack the same question --- \textcolor{primarygreen}{\bfseries how do language models (LMs) reason?} --- from opposite ends. Before that, three things must be on the table:

- **What commonsense reasoning is**, and why it is hard for NLU (Natural Language Understanding) systems.
- **ConceptNet** --- the knowledge graph (Speer et al., 2017).
- **CommonsenseQA (CQA)** --- the question-answering (QA) benchmark built *from* ConceptNet (Talmor et al., 2019), used by both papers.

\begin{block}{Why start here}
CQA is not a generic multiple-choice set. \emph{How its questions are manufactured} is exactly what makes them hard --- and it explains a surprising result we will meet in Paper 1.
\end{block}

# Why commonsense is hard for NLU

:::: columns
::: {.column width="56%"}
When people answer, they draw on world knowledge **not present in the text**: space, cause and effect, social conventions.

Example (Talmor et al., 2019):

> *“Where was Simon when he heard the lawn mower?”*

A human silently infers: a lawn mower is **outdoors**, at **street level** $\rightarrow$\ Simon was **outside**.
:::
::: {.column width="42%"}
\begin{block}{The contrast}
Classic QA (e.g.\ SQuAD) hands you a paragraph and asks about \emph{it}. Commonsense QA gives \textbf{no} such paragraph --- the knowledge must already be in the model.
\end{block}

\begin{block}{Remarks}
“Trivial for humans, out of reach for NLU systems” --- the gap this whole lecture circles around.
\end{block}
:::
::::

# ConceptNet: a commonsense knowledge graph (Speer et al., 2017)

:::: columns
::: {.column width="54%"}
ConceptNet stores everyday knowledge as a **graph of triples**:

- nodes are **concepts** (words / phrases);
- edges are **named relations**.

Typical relations: `IsA`, `AtLocation`, `UsedFor`, `CapableOf`, `Causes`, `PartOf`, `HasProperty`.

\begin{block}{Remarks}
Common sense \emph{written down} as a graph: millions of obvious facts, each a typed arrow between two ideas.
\end{block}
:::
::: {.column width="44%"}
\begin{center}
\includegraphics[width=\linewidth]{imgs/d1.pdf}
\end{center}
\footnotesize Other triples: \texttt{knife--UsedFor-->cutting}, \texttt{bird--CapableOf-->fly}.
:::
::::

# From ConceptNet to questions: how CQA is built

:::: columns
::: {.column width="50%"}
\begin{center}
\includegraphics[width=\columnwidth]{imgs/cqa_construction.pdf}
\end{center}
\footnotesize Talmor et al. (2019), Fig.\ 1.
:::
::: {.column width="48%"}
A worker sees a **source concept** (*river*, green) and **three target concepts** (*waterfall, bridge, valley*, blue) sharing one relation (`AtLocation`).

The worker writes **three questions**, one per target as the answer; the other two are distractors.

Then per question: **+1 ConceptNet distractor** (red) and **+1 hand-authored** (purple) $\rightarrow$\ **5 choices** total.
:::
::::

# The generation pipeline (Talmor et al., 2019)

:::: columns
::: {.column width="52%"}
\begin{center}
\includegraphics[width=\columnwidth,height=0.76\textheight,keepaspectratio]{imgs/cqa_pipeline.pdf}
\end{center}
\footnotesize After Talmor et al. (2019).
:::
::: {.column width="46%"}
Six construction stages, top to bottom:

1. **Filter** ConceptNet edges with rules.
2. **Extract** a subgraph (source + 3 targets).
3. Workers **author** one question per target.
4. Workers **add distractors** ($\rightarrow$\ 5 choices).
5. Workers **filter** by a quality score.
6. **Collect web snippets** (for search baselines).
:::
::::

# Why the distractors make it hard

:::: columns
::: {.column width="55%"}
The distractors are **ConceptNet siblings**: same source concept, same relation.

\begin{center}
\includegraphics[width=\linewidth,height=0.46\textheight,keepaspectratio]{imgs/d2.pdf}
\end{center}

So a model **cannot** win by spotting which option “sounds river-ish” --- they all do. It must read the specific situation (*hold a cup upright to catch water*).
:::
::: {.column width="42%"}
\begin{block}{Key insight}
The construction \emph{forces} commonsense: surface word-association is neutralised by design, because every option is equally associated with the source.
\end{block}
:::
::::

# The numbers, and the gap

:::: columns
::: {.column width="55%"}
- **12,247** questions in total (Talmor et al., 2019).
- Best baseline **BERT-large $\approx 56\%$** vs **human $\approx 89\%$**.
- Even adding **Google-search snippets** does **not** help $\rightarrow$\ the difficulty is reasoning, not missing data.

\begin{block}{Two versions --- remember this!}
\textbf{v1.0}: $\approx$ 9,500 questions, \textbf{3} choices (GPT 54.8\%, human 95.3\%).\quad
\textbf{v1.11}: 12,247 questions, \textbf{5} choices.
\end{block}
:::
::: {.column width="42%"}
\begin{block}{Why it returns}
Paper 1 reports results on \emph{both} versions. The jump from 3 to 5 ConceptNet-sibling choices is exactly where its method will stumble.
\end{block}
:::
::::

# Background $\rightarrow$ the two papers

\begin{block}{The set-up for the lecture}
Given this hard benchmark, two natural questions follow:
\end{block}

- **Paper 1 (Rajani et al., 2019):** can a model that *writes its reasoning* answer better? $\rightarrow$\ *generate* explanations.
- **Paper 2 (Yin \& Neubig, 2022):** can we *point at the exact input word* that drove a prediction? $\rightarrow$\ *localise* evidence.

\begin{center}
\textcolor{primarygreen}{\bfseries verbalise the reasoning} \qquad vs.\qquad \textcolor{primarygreen}{\bfseries localise the evidence}
\end{center}

# The two papers at a glance

\small\textcolor{primarygreen}{\bfseries Unit IV $\cdot$ Week 12.}\ Both methods explain a trained \textbf{language model (LM)} \emph{from the outside} (inputs $\to$ outputs) --- but the LM itself differs per paper.\normalsize

:::: columns
::: {.column width="49%"}
\begin{block}{Paper 1 $\cdot$ Rajani et al. (2019) --- CAGE}
\textcolor{primarygreen}{\bfseries Verbalise the reasoning}\par\smallskip
\footnotesize
\begin{itemize}\setlength{\itemsep}{1pt}
\item \textbf{Explains:} a BERT classifier (few answer options).
\item \textbf{What:} a natural-language narrative.
\item \textbf{Goal:} plausibility $+$ accuracy.
\item \textbf{Family:} generated explanation.
\item \textbf{Nature:} black-box (internals not inspected).
\end{itemize}
\end{block}
:::
::: {.column width="49%"}
\begin{block}{Paper 2 $\cdot$ Yin \& Neubig (2022)}
\textcolor{primarygreen}{\bfseries Localise the evidence}\par\smallskip
\footnotesize
\begin{itemize}\setlength{\itemsep}{1pt}
\item \textbf{Explains:} a generative LM --- GPT-2 / GPT-Neo ($\sim 50{,}000$ tokens).
\item \textbf{What:} attributes the output to input tokens.
\item \textbf{Goal:} faithfulness, fine-grained evidence.
\item \textbf{Family:} contrastive attribution (gradient/erasure).
\item \textbf{Nature:} gradients (white-box) or perturbation.
\end{itemize}
\end{block}
:::
::::

\begin{center}
\includegraphics[width=0.78\linewidth,height=0.18\textheight,keepaspectratio]{imgs/d7.pdf}
\end{center}

# Paper 1

\begin{center}
\includegraphics[width=0.92\columnwidth]{imgs/paper1_title.png}
\end{center}

# Introduction + Motivation

:::: columns
::: {.column width="55%"}
**The problem:** deep models do poorly on tasks needing commonsense reasoning --- knowledge not present in the input.

- An **explanation** verbalises the reasoning a model uses.
- **CommonsenseQA** is the benchmark (Talmor et al., 2019) --- *see Background*.
- Open question: *do* these models reason, and how much rests on world knowledge?
:::
::: {.column width="42%"}
\begin{block}{Core idea}
Train a language model to \textbf{generate explanations}, feed them to a classifier, and \textbf{measure whether they help}.
\end{block}

\begin{block}{Remarks}
Test whether the explanation \emph{helps accuracy} --- not merely whether it sounds nice.
\end{block}
:::
::::

# The pipeline, end to end

:::: columns
::: {.column width="55%"}
1. Take a CQA example: question $q$, choices $c_0,c_1,c_2$, gold answer $a$.
2. A human writes explanation $e_h$ for *why* $a$ is correct (this is **CoS-E** --- Common Sense Explanations).
3. Fine-tune a language model (**GPT** --- generative pre-training, Radford et al., 2018) to generate $e \approx e_h$.
4. Concatenate $q+$choices$+\,e$ and feed to a **BERT** classifier (bidirectional encoder, Devlin et al., 2019).
5. Measure: does $e$ raise accuracy?
:::
::: {.column width="42%"}
\begin{center}
\includegraphics[width=\linewidth]{imgs/d3.pdf}
\end{center}
\begin{block}{Remarks}
\textbf{GPT explains, BERT decides.} The LM is a commentator, not the judge.
\end{block}
:::
::::

# Didactic aside: what does “fine-tune GPT to generate $e$” mean?

:::: columns
::: {.column width="55%"}
- A language model already knows how to **continue text** (next-word prediction).
- **Fine-tuning** = keep training it, but now on `(question + choices) --> explanation` pairs from CoS-E.
- After fine-tuning, given a *new* question it can **write its own explanation**, imitating the human ones.
:::
::: {.column width="42%"}
\begin{block}{Mental model}
We are not teaching new facts; we are teaching a \emph{format}: “given a question, produce the kind of one-sentence justification a person would write.”
\end{block}
:::
::::

# CoS-E: Common Sense Explanations

:::: columns
::: {.column width="55%"}
A new dataset **on top of CQA**, collected via Amazon Mechanical Turk.

- **CoS-E-selected:** highlighted words in the question.
- **CoS-E-open-ended:** a free-form explanation sentence.
- Sizes (train / dev): v1.0 $=$ 7,610 / 950; v1.11 $=$ 9,741 / 1,221.
- Quality control: $\geq 1$ highlighted word, explanation $\geq 4$ words, not a substring, templates filtered.
:::
::: {.column width="42%"}
\begin{block}{Remarks}
Before GPT can \emph{write} explanations, it needs \emph{examples} of explanations. CoS-E is that supervision.
\end{block}
:::
::::

# CoS-E: three concrete examples (Table 1)

\footnotesize
\begin{block}{From the paper}
\textbf{Q:} “While eating a hamburger with friends, what are people trying to do?” \quad Choices: \textbf{have fun}, tasty, indigestion.\\
\textbf{CoS-E:} “Usually a hamburger with friends indicates a good time.”
\end{block}
\begin{block}{}
\textbf{Q:} “After getting drunk people couldn't understand him, it was because of his what?” \quad Choices: lower standards, \textbf{slurred speech}, falling down.\\
\textbf{CoS-E:} “People who are drunk have difficulty speaking.”
\end{block}
\begin{block}{}
\textbf{Q:} “People do what during their time off from work?” \quad Choices: \textbf{take trips}, brow shorter, become hysterical.\\
\textbf{CoS-E:} “People usually do something relaxing, such as taking trips, when they don't need to work.”
\end{block}

# CoS-E: a worked example, link by link

:::: columns
::: {.column width="55%"}
\begin{block}{Question}
While eating a hamburger with friends, what are people trying to do? --- \textbf{have fun} / tasty / indigestion.
\end{block}

The bare question never says friends are enjoyable. The explanation supplies the missing world-knowledge link:

\begin{center}
hamburger $+$ friends $\rightarrow$\ social $\rightarrow$\ enjoyable $\rightarrow$\ \textcolor{primarygreen}{\bfseries have fun}
\end{center}
:::
::: {.column width="42%"}
\begin{block}{Remarks}
That chain --- “hamburger with friends $=$ a good time” --- is commonsense made \emph{explicit in words}. That is what CoS-E records.
\end{block}
:::
::::

# CoS-E: what it actually contains

:::: columns
::: {.column width="52%"}
\begin{center}
\includegraphics[width=\linewidth]{imgs/d5.pdf}
\end{center}
:::
::: {.column width="46%"}
- **58\%** of explanations contain the ground-truth answer.
- Even explanations with **no** word overlap with any choice still beat the no-explanation baseline.

\begin{block}{Takeaway}
The explanation adds \emph{real signal}, not mere repetition of the answer.
\end{block}
:::
::::

# CAGE: Commonsense Auto-Generated Explanations

:::: columns
::: {.column width="55%"}
\begin{center}
\includegraphics[width=\linewidth]{imgs/d4.pdf}
\end{center}
:::
::: {.column width="42%"}
- **Phase 1 --- generate:** fine-tune GPT on CQA $+$ CoS-E to produce $e$.
- **Phase 2 --- classify:** BERT predicts the answer using $q+$choices$+\,e$.

\begin{block}{Recall}
First \emph{manufacture} the “why”; then \emph{decide} with its help.
\end{block}
:::
::::

# CAGE-reasoning (explain-then-predict)

:::: columns
::: {.column width="55%"}
**Main approach.** LM conditioned on question $+$ choices $+$ human explanation, **not** the gold label.

Input context (the prompt $C_{RE}$):

\footnotesize
“$q$, $c_0$, $c_1$, or $c_2$? commonsense says \_\_\_”
\normalsize

Objective:

\resizebox{\linewidth}{!}{$\displaystyle \max_{\Theta}\ \sum_i \log P(e_i \mid e_{i-k},\dots,e_{i-1},\,C_{RE};\,\Theta)$}
:::
::: {.column width="42%"}
\begin{block}{Memory hook}
The prompt ends in \texttt{commonsense says \_\_\_}: \textbf{no answer inside}. So the explanation is produced \emph{before} the answer is known.
\end{block}
:::
::::

# Deep dive: the training objective, term by term

:::: columns
::: {.column width="55%"}
Decompose $\displaystyle \max_{\Theta}\sum_i \log P(e_i \mid e_{<i},C_{RE};\Theta)$.

- $e_i$ --- the $i$-th token of the explanation to produce.
- $e_{<i}$ --- tokens already written (read to continue).
- $C_{RE}$ --- prompt: question $+$ choices $+$ “commonsense says”.
- $\Theta$ --- the LM parameters being fine-tuned.
- $\sum_i \log P$ --- next-token likelihood over explanation tokens.
:::
::: {.column width="42%"}
\begin{block}{Remarks}
Ordinary next-word training, but the “text to predict” is the \emph{explanation}, and the prompt \emph{excludes the label} --- so nothing leaks the answer.
\end{block}
:::
::::

# Didactic aside: “label in the prompt” --- the same example, both ways

\footnotesize
\begin{block}{Reasoning ($C_{RE}$) --- answer absent}
“While eating a hamburger with friends, what are people trying to do? \textbf{have fun}, tasty, or indigestion? \emph{commonsense says} \underline{\hspace{2cm}}”
\end{block}
\begin{block}{Rationalisation ($C_{RA}$) --- answer present}
“While eating a hamburger with friends \ldots? have fun, tasty, or indigestion? \textbf{have fun} \emph{because} \underline{\hspace{2cm}}”
\end{block}
\normalsize
\begin{center}
\textcolor{primarygreen}{\bfseries Only one word's worth of difference --- but in one case the model already knows the answer.}
\end{center}

# CAGE-rationalization (predict-then-explain)

:::: columns
::: {.column width="55%"}
**The reverse.** LM conditions on the **predicted label**; produces a post-hoc justification.

\footnotesize
$C_{RA} =$ “$q$, $c_0$, $c_1$, or $c_2$? $a$ because \_\_\_”
\normalsize

\footnotesize Hyper-parameters: max length 20, batch 36, $\leq 10$ epochs, lr 1e-6, warmup 0.002, weight decay 0.01.
:::
::: {.column width="42%"}
\begin{block}{Remarks}
The explanation comes \emph{after} the answer $\rightarrow$\ a \textbf{rationalisation}, not reasoning. More interpretable, but it cannot be the \emph{cause} of the prediction.
\end{block}
:::
::::

# Deep dive: reasoning vs.\ rationalisation

:::: columns
::: {.column width="55%"}
**One word changes everything: where the label sits.**

- **Reasoning** ($C_{RE}$): no label $\rightarrow$\ $e$ made at inference, used as genuine new context.
- **Rationalisation** ($C_{RA}$): label in prompt $\rightarrow$\ $e$ conditioned on the answer.
- Accuracy: reasoning **$+10\%$** over the previous state of the art (SOTA); rationalisation **$+6\%$**.
- Only reasoning can be called “commonsense reasoning”.
:::
::: {.column width="42%"}
\begin{block}{Key insight (the heart of the lecture)}
Faithfulness is decided by \textbf{information flow}, not output quality. A \emph{fluent} rationalisation can still be \emph{unfaithful}.
\end{block}
:::
::::

# Results: CommonsenseQA v1.0 (3 choices)

:::: columns
::: {.column width="48%"}
**Dev (random split)**

\begin{tabular}{lr}\hline
Method & Acc.\ (\%)\\ \hline
BERT baseline & 63.8\\
CoS-E-open-ended & 65.5\\
CAGE-reasoning & \textbf{72.6}\\ \hline
\end{tabular}
:::
::: {.column width="48%"}
**Test split (v1.0)**

\begin{tabular}{lr}\hline
Method & Acc.\ (\%)\\ \hline
RC (Talmor) & 47.7\\
GPT (Talmor) & 54.8\\
CoS-E-open-ended & 60.2\\
CAGE-reasoning & \textbf{64.7}\\
Human & 95.3\\ \hline
\end{tabular}
:::
::::

\footnotesize RC $=$ reading-comprehension baseline (Talmor et al., 2019).\normalsize

\vspace{4pt}
\begin{block}{Headline}
$\approx 10\%$ absolute over previous SOTA on test --- yet still far below the human 95.3\%.
\end{block}

# Results: CQA v1.11 (5 choices) --- the uncomfortable result

:::: columns
::: {.column width="48%"}
\begin{tabular}{lr}\hline
Method & Acc.\ (\%)\\ \hline
CAGE-reasoning & 55.7\\
BERT baseline & 56.7\\
\textbf{CoS-E-open-ended} & \textbf{58.2}\\ \hline
\end{tabular}
:::
::: {.column width="48%"}
\begin{block}{Remarks}
On the harder 5-choice version \textbf{CAGE loses to the plain baseline}. The explanation often \emph{contains} the right answer, but the classifier cannot exploit it.
\end{block}
:::
::::

\begin{block}{Connect to Background}
Recall: v1.11 has \textbf{five ConceptNet siblings}. With options that semantically close, simply \emph{concatenating} the explanation is not enough. The authors report this honestly.
\end{block}

# Results: out-of-domain transfer

:::: columns
::: {.column width="50%"}
\begin{tabular}{lrr}\hline
Method & SWAG & Story Cloze\\ \hline
BERT & 84.2 & 89.8\\
$+$ explanation transfer & 83.6 & 89.5\\ \hline
\end{tabular}
:::
::: {.column width="46%"}
\begin{block}{Remarks}
Transfer with no retraining costs only a \textbf{tiny drop} ($<0.6\%$). Fluent, relevant explanations --- but no downstream gain. An \emph{honest negative result}.
\end{block}
:::
::::

# Qualitative analysis

:::: columns
::: {.column width="55%"}
- CAGE explanations use **simpler constructions** than humans, yet can be *more* informative.
- Contain an answer choice **43\%** of the time; the *predicted* choice only **21\%**.
- **BLEU** (n-gram overlap with references) vs human explanations peaks at **4.1** (vs 0.8 untuned); perplexity 32.
:::
::: {.column width="42%"}
\begin{block}{Foreshadowing}
Low BLEU but real usefulness $\rightarrow$\ something can be \emph{useful without resembling human wording}. This previews Paper 2's \textbf{faithfulness vs.\ plausibility} tension.
\end{block}
:::
::::

# Limitations + critical reading of Rajani et al.

- **Human simulatability is low:** from the explanation alone, Turkers recover the model's answer **42\%** (CAGE) vs **52\%** (human) $\rightarrow$\ the explanation does not transparently reveal the model.
- **Adversarial explanations are catastrophic:** misleading explanations drop accuracy **60\% $\to$ 30\%** --- below the 50\% baseline.
- **Bias propagation:** CQA gender disparity flows into CoS-E and the trained models.

# Bridge to Paper 2

:::: columns
::: {.column width="55%"}
\begin{block}{What Rajani et al.\ leave open}
They \emph{generate} explanations, but never ask: \textbf{which input tokens caused this prediction}, and \textbf{why this token instead of another?}
\end{block}

- Generated explanations are **plausible** but not necessarily **faithful**.
- Language generation has an enormous output space $\rightarrow$\ we need a **token-level** lens.
:::
::: {.column width="42%"}
\begin{block}{Next}
\textbf{Yin \& Neubig (2022):} contrastive input-saliency --- look \emph{inside} the model.
\end{block}
:::
::::

# Paper 2

\begin{center}
\includegraphics[width=0.92\columnwidth]{imgs/paper2_title.png}
\end{center}

# Introduction + Motivation: the output-space problem

:::: columns
::: {.column width="55%"}
- Classification: **small** output space (few labels).
- Language modelling: **tens of thousands** of tokens per step.
- A single prediction conflates **many** decisions: part of speech, number, tense, semantics.
:::
::: {.column width="42%"}
\begin{block}{Symptom}
Non-contrastive saliency just highlights the token \textbf{right before} the prediction --- uninformative about subtle choices.
\end{block}
:::
::::

# Didactic aside: “output space”, concretely

:::: columns
::: {.column width="55%"}
- A spam classifier picks among $\{\text{spam}, \text{ham}\}$ --- 2 options. “Why?” is easy.
- A language model picks the next token among **$\sim 50{,}000$** options.

\begin{center}
“Can you stop the dog \underline{\hspace{1.6cm}}” $\rightarrow$\ \{barking, crying, walking, running, \dots\}
\end{center}
:::
::: {.column width="42%"}
\begin{block}{Why this matters}
With 50,000 outputs, “what mattered for the prediction?” blurs together grammar, number, tense and meaning into one uninformative answer.
\end{block}
:::
::::

# The contrastive lens

:::: columns
::: {.column width="55%"}
Why did the model predict **“barking”** given *“Can you stop the dog from \_\_\_”*?

- Non-contrastive: highlights “from” (obvious preceding token).
- “barking” **instead of** “crying”? $\rightarrow$\ **“dog”** matters.
- “barking” **instead of** “walking”? $\rightarrow$\ **“stop”** matters.
:::
::: {.column width="42%"}
\begin{block}{Key insight}
Contrastive explanation (Lipton, 1990) asks why target $y_t$ \emph{rather than} foil $y_f$. The \textbf{foil} picks \emph{which} conflated decision we explain.
\end{block}
:::
::::

# Didactic aside: what is a “foil”?

:::: columns
::: {.column width="55%"}
- $y_t$ = the **target** = what the model actually said (*barking*).
- $y_f$ = the **foil** = a chosen rival you compare against (*crying*, *walking*, \dots).

\begin{center}
barking vs crying $\rightarrow$\ \textcolor{primarygreen}{\bfseries dog}\qquad barking vs walking $\rightarrow$\ \textcolor{primarygreen}{\bfseries stop}
\end{center}
:::
::: {.column width="42%"}
\begin{block}{The trick}
Change the foil, change the \emph{question}. The foil is how you \emph{aim} the explanation at one specific decision.
\end{block}
:::
::::

# Formal definition: contrastive saliency

:::: columns
::: {.column width="55%"}
Non-contrastive gradient:
$$ g(x_i) = \nabla_{x_i}\, q(y_t \mid x) $$
Contrastive gradient:
$$ g^{*}(x_i) = \nabla_{x_i}\big( q(y_t \mid x) - q(y_f \mid x) \big) $$
:::
::: {.column width="42%"}
\begin{block}{Remarks}
$\nabla$ just means “how much it influences”. Not “what raised $y_t$?” but “what raised $y_t$ \emph{while lowering} $y_f$?” --- the subtraction cancels shared evidence.
\end{block}
:::
::::

# Deep dive: why the subtraction works

:::: columns
::: {.column width="55%"}
Walk $g^{*}(x_i) = \nabla_{x_i}(q(y_t\mid x) - q(y_f\mid x))$:

1. $\nabla_{x_i}q(y_t\mid x)$ --- how $x_i$ pushes the **target** up.
2. $\nabla_{x_i}q(y_f\mid x)$ --- how the **same** token pushes the **foil** up.
3. Subtract: evidence raising *both* (“predict some verb-ing”) cancels.
4. What survives separates $y_t$ from $y_f$ specifically.
5. Norm $\Rightarrow$ magnitude; gradient $\times$ input $\Rightarrow$ signed direction.
:::
::: {.column width="42%"}
\begin{block}{Remarks}
Generic syntactic pressure is shared, so it disappears. The leftover is the \textbf{semantic / long-range} cue we wanted.
\end{block}
:::
::::

# Method 1: Contrastive Gradient Norm

:::: columns
::: {.column width="55%"}
$$ S^{*}_{GN}(x_i) = \lVert g^{*}(x_i) \rVert_{L_1} $$

- White-box, cheap (one backward pass).
- **Magnitude** only, no direction.
:::
::: {.column width="42%"}
\begin{block}{Use it for}
“Does this token matter at all?” --- it tells you \emph{how strongly} $x_i$ tips the decision, not \emph{which way}.
\end{block}
:::
::::

# Method 2: Contrastive Gradient $\times$ Input

:::: columns
::: {.column width="55%"}
$$ S_{GI}(x_i) = g(x_i)\cdot x_i,\quad S^{*}_{GI}(x_i) = g^{*}(x_i)\cdot x_i $$

- White-box, cheap, and **signed**.
- Multiplying by the embedding weights influence by how present the token is.
:::
::: {.column width="42%"}
\begin{block}{Use it for}
“\emph{Towards} $y_t$ (positive) or \emph{towards} the foil (negative)?” --- more information than Method 1.
\end{block}
:::
::::

# Method 3: Contrastive Input Erasure

:::: columns
::: {.column width="58%"}
\resizebox{\linewidth}{!}{$\displaystyle S^{*}_{E}(x_i) = \big(q(y_t\mid x) - q(y_t\mid x_{\neg i})\big) - \big(q(y_f\mid x) - q(y_f\mid x_{\neg i})\big)$}

- **Black-box:** remove $x_i$ and measure the change.
- **Expensive:** one forward pass per token.
:::
::: {.column width="40%"}
\begin{block}{Remarks}
$x_{\neg i}$ is the sentence \emph{without} that word. Delete it: if $y_t$ drops and the foil $y_f$ rises, the word mattered.
\end{block}
:::
::::

# Deep dive: the three methods on one axis

:::: columns
::: {.column width="55%"}
**Same question, three trade-offs.**

- $S^{*}_{GN}$ (norm): cheap, white-box, *magnitude* --- “relevant?”
- $S^{*}_{GI}$ (grad $\times$ input): cheap, white-box, *signed* --- “towards target or foil?”
- $S^{*}_{E}$ (erasure): expensive, black-box, *direct* --- “measured, not approximated”.
:::
::: {.column width="42%"}
\begin{block}{Key insight}
Gradients \textbf{approximate} a perturbation; erasure \textbf{performs} it. Erasure is the ground truth you cannot afford at scale.
\end{block}
:::
::::

# Evaluation setup: BLiMP minimal pairs

:::: columns
::: {.column width="55%"}
- **BLiMP** --- the Benchmark of Linguistic Minimal Pairs (Warstadt et al., 2020): 67 paradigms of minimal sentence pairs.
- They use **5 phenomena / 12 paradigms** (anaphor, argument structure, determiner-noun, NPI [negative-polarity items], subject-verb).
- Models: **GPT-2** (1.5B), **GPT-Neo** (2.7B).
- Each paradigm has a **rule** marking the token that enforces grammaticality.
:::
::: {.column width="42%"}
\begin{block}{Why BLiMP}
They need an exam where the \emph{correct} causal token is known \emph{in advance} --- so a method can be graded objectively.
\end{block}
:::
::::

# Didactic aside: what is a “minimal pair”?

:::: columns
::: {.column width="55%"}
Two sentences that differ in **one** spot, one grammatical and one not:

\begin{center}
“The \textbf{author laughs}.” \quad(\textbf{ok})\\
“The \textbf{author laugh}.” \quad(*)
\end{center}

The single contrast isolates exactly one grammatical decision (subject--verb agreement).
:::
::: {.column width="42%"}
\begin{block}{Why it is perfect here}
A minimal pair \emph{is} a target/foil pair: \emph{laughs} vs \emph{laugh}. We already know the cause (the subject) --- so we can check whether the method points there.
\end{block}
:::
::::

# Deep dive: the alignment metrics

:::: columns
::: {.column width="55%"}
$E$ = binary vector of “correct” evidence tokens; $S$ = saliency scores.

- **Dot product** $S\cdot E$ --- saliency on true evidence (higher $=$ better).
- **Probes needed** --- rank of the first true-evidence token (lower $=$ better).
- **MRR** --- mean reciprocal rank of that token (higher $=$ better).
:::
::: {.column width="42%"}
\begin{block}{Remarks}
All three ask: \textbf{does the method put the correct token near the top?} Probes-needed and MRR are two views of the same ranking.
\end{block}
:::
::::

# BLiMP: which input token is the cause?

:::: columns
::: {.column width="55%"}
\begin{block}{Anaphor number agreement}
Acceptable: “Many \underline{teenagers} were helping \textbf{themselves}.”\\
Unacceptable: “Many teenagers were helping \textbf{herself}.”
\end{block}

- The rule marks the antecedent **“teenagers”** as the evidence.
- A good explanation of *themselves* vs *herself* ranks **teenagers** high.
:::
::: {.column width="42%"}
\begin{block}{The test}
Explaining \emph{themselves} vs \emph{herself}: if the method points at \textcolor{primarygreen}{\bfseries teenagers} it is good; if it points elsewhere, it is poor.
\end{block}
:::
::::

# Quantitative results: alignment on BLiMP

:::: columns
::: {.column width="55%"}
\begin{center}
\includegraphics[width=\linewidth]{imgs/d6.pdf}
\end{center}
:::
::: {.column width="42%"}
- Contrastive variants ($S^{*}$, green) align **better** with known evidence.
- The gain **grows with distance**: further evidence $\Rightarrow$ bigger contrastive advantage.
:::
::::

# Human study: contrastive simulatability

:::: columns
::: {.column width="42%"}
\begin{tabular}{lr}\hline
Method & Acc.\ (\%)\\ \hline
None & 61.38\\
$S_{GI}$ & 64.00\\
$S^{*}_{GI}$ & \textbf{65.62}\\
$S_{E}$ & 63.12\\
$S^{*}_{E}$ & \textbf{64.62}\\ \hline
\end{tabular}
:::
::: {.column width="55%"}
10 ML grad students predict GPT-2's output from input $+$ explanation (4,000 judgments; model correct 50\%).

\begin{block}{Remarks}
Contrastive explanations make the model more \textbf{predictable} to a human --- that property is \emph{simulatability}.
\end{block}
:::
::::

# Use case: clustering decisions by their causes

:::: columns
::: {.column width="55%"}
- Represent each foil by its contrastive-saliency vector, then **k-means cluster**.
- Clusters recover grammatical categories **without supervision**:
  - target male pronoun $\rightarrow$\ cluster of **female** pronouns;
  - animate noun $\rightarrow$\ cluster of **inanimate** nouns;
  - singular noun $\rightarrow$\ cluster of **plural** foils.
:::
::: {.column width="42%"}
\begin{block}{Key insight}
These clusters differ from word-embedding neighbours --- they reflect what the \textbf{model uses to decide}, not lexical similarity.
\end{block}
:::
::::

# Limitations of Yin \& Neubig

- **Foil selection is hard and consequential:** open-ended generation has no rule for which foil to contrast against --- and changing the foil changes the result.
- **Faithfulness vs.\ plausibility:** matching human intuition does not *prove* the saliency captures the true computation.
- **Cost:** erasure is the most direct but scales poorly with length and foil-space size.

# Concluding thoughts: connecting the two papers

:::: columns
::: {.column width="48%"}
**Rajani et al. (2019)**

- *Generated* natural-language explanations.
- Optimised for **plausibility** $+$ accuracy.
- Cannot guarantee the explanation *caused* the prediction.
:::
::: {.column width="48%"}
**Yin \& Neubig (2022)**

- *Token-level, contrastive* saliency.
- Targets **faithful**, fine-grained evidence.
- Needs a foil; faithfulness still not proven.
:::
::::

\begin{block}{The shared thread}
Both attack \emph{how do LMs reason} from opposite ends: \textbf{verbalise} the reasoning vs.\ \textbf{localise} the evidence.
\end{block}

# Recap --- the two papers at a glance

\small\textcolor{primarygreen}{\bfseries Recap.}\ Both methods explain a trained \textbf{language model (LM)} \emph{from the outside} (inputs $\to$ outputs) --- but the LM itself differs per paper.\normalsize

:::: columns
::: {.column width="49%"}
\begin{block}{Paper 1 $\cdot$ Rajani et al. (2019) --- CAGE}
\textcolor{primarygreen}{\bfseries Verbalise the reasoning}\par\smallskip
\footnotesize
\begin{itemize}\setlength{\itemsep}{1pt}
\item \textbf{Explains:} a BERT classifier (few answer options).
\item \textbf{What:} a natural-language narrative.
\item \textbf{Goal:} plausibility $+$ accuracy.
\item \textbf{Family:} generated explanation.
\item \textbf{Nature:} black-box (internals not inspected).
\end{itemize}
\end{block}
:::
::: {.column width="49%"}
\begin{block}{Paper 2 $\cdot$ Yin \& Neubig (2022)}
\textcolor{primarygreen}{\bfseries Localise the evidence}\par\smallskip
\footnotesize
\begin{itemize}\setlength{\itemsep}{1pt}
\item \textbf{Explains:} a generative LM --- GPT-2 / GPT-Neo ($\sim 50{,}000$ tokens).
\item \textbf{What:} attributes the output to input tokens.
\item \textbf{Goal:} faithfulness, fine-grained evidence.
\item \textbf{Family:} contrastive attribution (gradient/erasure).
\item \textbf{Nature:} gradients (white-box) or perturbation.
\end{itemize}
\end{block}
:::
::::

\begin{center}
\includegraphics[width=0.78\linewidth,height=0.18\textheight,keepaspectratio]{imgs/d7.pdf}
\end{center}

# Open questions

- Can generated explanations (Paper 1) be **constrained to be faithful** via contrastive saliency (Paper 2)?
- What is the right way to **choose foils** for open-ended generation?
- For regulated settings (EU AI Act, Art.\ 13), is a **plausible** explanation enough, or is **faithfulness** legally required?

\begin{center}
\vspace{0.6em}
\Large\textbf{Discussion?}
\end{center}

# Thank you

\begin{center}
\vspace{1.2em}
{\Huge \textcolor{primarygreen}{\bfseries Thank You!}}
\end{center}

# References {.allowframebreaks}

\footnotesize

- Devlin, J., Chang, M.-W., Lee, K., Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL-HLT.
- Lipton, P. (1990). *Contrastive Explanation.* Royal Institute of Philosophy Supplement 27: 247--266.
- Radford, A., Narasimhan, K., Salimans, T., Sutskever, I. (2018). *Improving Language Understanding by Generative Pre-Training.* OpenAI tech report.
- Rajani, N. F., McCann, B., Xiong, C., Socher, R. (2019). *Explain Yourself! Leveraging Language Models for Commonsense Reasoning.* ACL, 4932--4942.
- Speer, R., Chin, J., Havasi, C. (2017). *ConceptNet 5.5: An Open Multilingual Graph of General Knowledge.* AAAI.
- Talmor, A., Herzig, J., Lourie, N., Berant, J. (2019). *CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge.* NAACL-HLT, 4149--4158.
- Warstadt, A., Parrish, A., Liu, H., et al. (2020). *BLiMP: The Benchmark of Linguistic Minimal Pairs for English.* TACL 8: 377--392.
- Yin, K., Neubig, G. (2022). *Interpreting Language Models with Contrastive Explanations.* EMNLP, 184--198.
