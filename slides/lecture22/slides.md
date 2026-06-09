---
title: "\\emoji{wtf} XAI Lecture 22"
subtitle: "Compiled Transformers as a Laboratory for Interpretability"
bibliography: references.bib
suppress-bibliography: true
nocite: |
  @lindner2023tracr, @weiss2021thinking, @cammarata2020circuits, @cammarata2021curve, @elhage2022superposition, @olah2017feature

---

# Disclaimer

\input{../disclaimer.tex}

---

# \large Compiled Transformers as a Laboratory for Interpretability

\begin{center}
\includegraphics[width=0.90\columnwidth,height=0.70\textheight,keepaspectratio]{imgs/paper.png}
\end{center}

[@lindner2023tracr]

---

# Motivations — Tracr

- **Controlled experiments:** Creates simple, controlled Transformer models from RASP programs.

- **Ground truth availability:** Provides known internal mechanisms to evaluate interpretability methods.

- **Bridge algorithms $\leftrightarrow$ Transformers:** Shows how algorithms can be implemented inside attention-based models.

- **Reduction of confounding factors:** Avoids training noise and unclear learned objectives.

- **Educational and research utility:** Works as a laboratory for mechanistic interpretability.

---

# The Core Problem: No Ground Truth

\begin{center}
\includegraphics[width=0.84\columnwidth,height=0.52\textheight,keepaspectratio]{imgs/no_ground_truth.png}
\end{center}

\begin{alertblock}{Interpretability bottleneck}
For a trained neural network, there is usually no independent ground-truth mechanism telling us whether an explanation is correct.
\end{alertblock}

---

# What If We Had Ground Truth?

\begin{center}
\includegraphics[width=0.86\columnwidth,height=0.56\textheight,keepaspectratio]{imgs/ground_truth_loop.png}
\end{center}

If the network is compiled from a **known mechanism**, then an explanation can be checked against the program that generated the weights.

---

# Introducing Tracr

\vspace{2em}
\begin{center}
\includegraphics[width=0.58\columnwidth,height=0.38\textheight,keepaspectratio]{imgs/tracr_intro.png}
\end{center}

\begin{center}
\Large Known Mechanism {\Huge$\longrightarrow$} Neural Network
\end{center}

\vspace{1.6em}

\begin{center}
\begin{tabular}{l}
\large Tracr is a compiler from \textbf{RASP programs} into \textbf{decoder-only transformer}\\
\large \textbf{weights}.\\[0.25em]
\small (Lindner et al. 2023)
\end{tabular}
\end{center}

---

# Plan for Today

\begin{center}
\vspace{0.6em}
\setlength{\fboxsep}{0.8em}
\setlength{\fboxrule}{1.2pt}

\fcolorbox{darkgreen}{white}{%
\begin{minipage}[c][0.20\textheight][c]{0.84\textwidth}
\begin{minipage}[c]{0.56\linewidth}
\Large 1. Building a \textbf{compiler} for\\ transformer models
\end{minipage}
\hfill
\begin{minipage}[c]{0.36\linewidth}
\centering
\includegraphics[width=\linewidth,height=0.15\textheight,keepaspectratio]{imgs/build_compiler.png}
\end{minipage}
\end{minipage}
}

\vspace{0.9em}

\fcolorbox{darkgreen}{white}{%
\begin{minipage}[c][0.20\textheight][c]{0.84\textwidth}
\begin{minipage}[c]{0.60\linewidth}
\Large 2. Studying \textbf{superposition} in\\ compiled models
\end{minipage}
\hfill
\begin{minipage}[c]{0.28\linewidth}
\centering
\includegraphics[width=\linewidth,height=0.15\textheight,keepaspectratio]{imgs/plan_superposition.png}
\end{minipage}
\end{minipage}
}
\end{center}

---

# Why Not Hand-Code Weights?

:::: columns
::: {.column width="42%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.56\textheight,trim=0 120 0 0,clip,keepaspectratio]{imgs/hand_coding.png}

\footnotesize (Cammarata et al. 2021)
\end{center}

:::
::: {.column width="54%"}

Hand-coding weights is a strong form of understanding:
\vspace{0.8em}
\begin{itemize}\setlength\itemsep{0.55em}
\item We specify the circuit directly
\item We know what each component should do
\item We can compare learned behavior against the construction
\end{itemize}

\vspace{1.2em}
\begin{alertblock}{Problem}
\resizebox{\linewidth}{!}{This does not scale. It is like programming a model in bytecode.}
\end{alertblock}

:::
::::

---

# Part 1: Building the Compiler

\begin{center}
\includegraphics[width=\columnwidth,height=0.66\textheight,keepaspectratio]{imgs/tracr_compile.png}
\end{center}

\vspace{0.25em}

\begin{center}
\large Tracr works analogously to how we would translate a programming language into executable code.
\end{center}

---

# Three-Step Translation

\begin{center}
\includegraphics[width=0.90\columnwidth,height=0.56\textheight,keepaspectratio]{imgs/three_steps.png}
\end{center}

\begin{block}{Design principle}
Keep the high-level algorithm explicit as long as possible, then lower it into a standard transformer implementation.
\end{block}

---

# RASP: A Language for Transformer Computations

:::: columns
::: {.column width="53%"}

\vspace{-1em}

\begin{block}{Definition}
\resizebox{\linewidth}{!}{\textbf{RASP} = "Restricted Access Sequence Processing Language"}
\end{block}

\vspace{1.3em}

\begin{itemize}\setlength\itemsep{0.30em}
\item Two variable types: \textbf{sequence operations} and \textbf{selectors}
\item Two instruction types: \textbf{elementwise} and \textbf{select-aggregate}
\item S-ops roughly correspond to transformer \textbf{residual stream state}
\end{itemize}

:::
::: {.column width="42%"}

\vspace{0.8em}

\begin{center}
\includegraphics[width=1.08\columnwidth,height=0.48\textheight,keepaspectratio]{imgs/rasp_language.png}
\end{center}

\vspace{0.45em}

\begin{center}
\begin{minipage}{0.76\columnwidth}
\begin{exampleblock}{Example sequence}
\centering
{\footnotesize\ttfamily bos\quad x\quad a\quad c\quad x}
\end{exampleblock}
\end{minipage}
\end{center}

\vspace{0.7em}

\hspace{-0.6em}\begin{minipage}{0.98\columnwidth}
\begin{exampleblock}{Primitive s-ops}
\footnotesize
{\ttfamily \textcolor{darkgreen}{tokens}\textcolor{black}{("hello")}} $= [h,e,l,l,o]$\\
{\ttfamily \textcolor{darkgreen}{indices}\textcolor{black}{("hello")}} $= [0,1,2,3,4]$
\end{exampleblock}
\end{minipage}

:::
::::

---

# RASP Instructions Map to Transformer Blocks

:::: columns
::: {.column width="48%"}

\begin{block}{Elementwise operations}
\begin{itemize}\setlength\itemsep{0.6em}
\item Apply a function independently at each sequence position
\item Example: {\ttfamily\textcolor{black}{(3 * }\textcolor{darkgreen}{indices}\textcolor{black}{)(}\textcolor{darkgreen}{"hello"}\textcolor{black}{)}} $\textcolor{black}{=}\ \textcolor{darkgreen}{[0, 3, 6, 9, 12]}$
\item Roughly correspond to transformer \textbf{MLP layers}
\end{itemize}
\end{block}

:::
::: {.column width="48%"}

\begin{block}{Select-aggregate operations}
\begin{itemize}\setlength\itemsep{0.6em}
\item Move information between token positions
\item A selector evaluates to an $N \times N$ binary matrix
\item \texttt{select} builds the selector; \texttt{aggregate} reads selected values
\item Roughly correspond to transformer \textbf{attention}
\end{itemize}
\end{block}

:::
::::

\begin{block}{Compiler intuition}
RASP keeps the algorithm readable, while Tracr lowers these operations into transformer components.
\end{block}

---

# RASP Example: Count Previous `x` Tokens

:::: columns
::: {.column width="49%"}

\vspace{2em}
\begin{block}{RASP code}
\small
{\ttfamily\textcolor{black}{is\_x = (tokens == }\textcolor{darkgreen}{"x"}\textcolor{black}{)}}\\
{\ttfamily\textcolor{black}{prevs = }\textcolor{darkgreen}{select}\textcolor{black}{(indices, indices, <=)}}\\
{\ttfamily\textcolor{black}{frac\_prev = }\textcolor{darkgreen}{aggregate}\textcolor{black}{(prevs, is\_x)}}
\end{block}

:::
::: {.column width="47%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.55\textheight,keepaspectratio]{imgs/rasp_example.png}
\end{center}

:::
::::

\begin{block}{In plain English}
For each position, ask: \textit{among all previous positions including this one, what fraction contained the token x?}
\end{block}

---

# From RASP to transformer weights

:::: columns
::: {.column width="50%"}

\begin{block}{Compilation process (6 steps)}
\scriptsize
\begin{enumerate}\setlength\itemsep{0.15em}
\item Construct computational graph.
\item Infer s-op input/output values.
\item Translate s-ops into model blocks.
\item Assign components to layers.
\item Assemble the craft transformer.
\item Generate weight matrices.
\end{enumerate}
\end{block}

\vspace{2em}
\begin{center}
\includegraphics[width=1.06\columnwidth,height=0.39\textheight,keepaspectratio]{imgs/rasp_to_craft_architecture.png}
\end{center}

:::
::: {.column width="47%"}

\vspace{1.0em}

\begin{block}{RASP code}
\scriptsize
{\ttfamily\textcolor{black}{is\_x = (tokens == }\textcolor{darkgreen}{"x"}\textcolor{black}{)}}\\
{\ttfamily\textcolor{black}{prevs = }\textcolor{darkgreen}{select}\textcolor{black}{(indices, indices, <=)}}\\
{\ttfamily\textcolor{black}{frac\_prev = }\textcolor{darkgreen}{aggregate}\textcolor{black}{(prevs, is\_x)}}
\end{block}

\begin{center}
\includegraphics[width=1.06\columnwidth,height=0.55\textheight,keepaspectratio]{imgs/rasp_to_craft_graph.png}
\end{center}

:::
::::

---

# Implementing MLP Layers

\begin{center}
\includegraphics[width=0.82\columnwidth,height=0.40\textheight,keepaspectratio]{imgs/mlp_implementation.png}
\end{center}

:::: columns
::: {.column width="48%"}

\begin{block}{Categorical variables}
An MLP can implement a lookup table over finitely many categories.
\end{block}

:::
::: {.column width="48%"}

\begin{block}{Numerical variables}
A ReLU network can approximate the desired function exactly on the discrete input set used by the program.
\end{block}

:::
::::

---

# Implementing Attention Heads

:::: columns
::: {.column width="50%"}

\vspace{0.12\textheight}

\begin{center}
\textcolor{black}{\textbf{Operation mapping}}

\vspace{0.3em}

\scriptsize
\renewcommand{\arraystretch}{1.45}
\begin{tabular}{@{}l@{\hspace{1.5em}}l@{}}
\hline
\mbox{\textcolor{black}{\textbf{RASP operation}}} & \mbox{\textcolor{black}{\textbf{Transformer component}}} \\
\hline
{\ttfamily\mbox{\textcolor{black}{select(indices, indices, <=)}}} & \mbox{\textcolor{black}{query key scores $W_Q^T W_K$}} \\
{\ttfamily\mbox{\textcolor{black}{aggregate(prevs, is\_x)}}} & \mbox{\textcolor{black}{value output map $W_O^T W_V$}} \\
\hline
\end{tabular}
\renewcommand{\arraystretch}{1.0}
\end{center}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.56\textheight,keepaspectratio]{imgs/attention_implementation.png}
\end{center}

:::
::::

\begin{block}{In plain English}
Attention is used as programmable routing: decide \textit{which positions to read from}, then aggregate their values.
\end{block}

---

# craft Models Map to Standard Transformers

\begin{center}
\includegraphics[width=0.90\columnwidth,height=0.58\textheight,keepaspectratio]{imgs/craft_to_transformer.png}
\end{center}

\begin{block}{Key idea}
\texttt{craft} separates the abstract vector-space computation from implementation details, then maps it into a GPT-like transformer architecture.
\end{block}

---

# What Can Tracr Compile?

:::: columns
::: {.column width="48%"}

\begin{exampleblock}{Examples}
\begin{itemize}
\item Count tokens and build histograms
\item Detect all occurrences of a pattern
\item Sort a sequence
\item Check balanced parentheses
\item ...
\end{itemize}
\end{exampleblock}

:::
::: {.column width="48%"}

\begin{alertblock}{Limitations}
\begin{itemize}
\item Binary attention patterns
\item Algorithmic, not probabilistic, tasks
\item Programs close to transformer structure
\item Large and inefficient compiled models
\end{itemize}
\end{alertblock}

:::
::::

---

# A Compiled Residual Stream

:::: columns
::: {.column width="46%"}

\begin{block}{RASP program}
\footnotesize
{\ttfamily\textcolor{black}{is\_x = (tokens == }\textcolor{darkgreen}{"x"}\textcolor{black}{)}}\\[0.25em]
{\ttfamily\textcolor{black}{prevs = }\textcolor{darkgreen}{select}\textcolor{black}{(indices, indices, <=)}}\\[0.25em]
{\ttfamily\textcolor{black}{frac\_prev = }\textcolor{darkgreen}{aggregate}\textcolor{black}{(prevs, is\_x)}}
\end{block}

:::
::: {.column width="51%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.64\textheight,keepaspectratio]{imgs/compiled_residual_stream.png}
\end{center}

:::
::::

\begin{block}{Key idea}
\footnotesize The residual stream exposes the compiled variables: first the MLP computes \texttt{is\_x}, then attention computes the fraction over previous positions.
\end{block}

---

# What Does Ground Truth Buy Us?

:::: columns
::: {.column width="53%"}

With a compiled model, we know:

\vspace{0.5em}

\begin{itemize}\setlength\itemsep{0.45em}
\item Which variables should exist
\item Which layer computes each variable
\item Which attention head implements each selector
\item Which features are necessary for the final output
\end{itemize}

:::
::: {.column width="44%"}

\begin{block}{Evaluation idea}
Run an interpretability method and ask whether it recovers the same components the compiler inserted.
\end{block}

\begin{alertblock}{Caveat}
This only tests interpretability on synthetic algorithmic models, not arbitrary trained LLMs.
\end{alertblock}

:::
::::

---

# Part 2: Studying Superposition

\begin{center}
\vspace{1.2em}
\setlength{\fboxsep}{0.9em}
\setlength{\fboxrule}{1.3pt}

\fcolorbox{darkgreen}{white}{%
\begin{minipage}[c][0.28\textheight][c]{0.86\textwidth}
\begin{minipage}[c]{0.66\linewidth}
\Large 2. Studying \textbf{superposition} in\\ compiled models
\end{minipage}
\hfill
\begin{minipage}[c]{0.26\linewidth}
\centering
\includegraphics[width=\linewidth,height=0.22\textheight,keepaspectratio]{imgs/plan_superposition.png}
\end{minipage}
\end{minipage}
}
\end{center}

---

# The Superposition Hypothesis

:::: columns
::: {.column width="54%"}

\begin{block}{Observation 1}
Some neurons correspond to clean, interpretable features.
\end{block}

\vspace{0.75em}

\begin{block}{Observation 2}
Other neurons appear to represent multiple features.
\end{block}

\vspace{0.75em}

\begin{block}{Observation 3}
A linear representation can store more features than dimensions when features are sparse.
\end{block}

:::
::: {.column width="43%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.68\textheight,keepaspectratio]{imgs/superposition_hypothesis.png}
\end{center}

:::
::::

---

# Toy Models Show When Superposition Appears

:::: columns
::: {.column width="52%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.51\textheight,keepaspectratio]{imgs/toy_superposition_model.png}
\end{center}

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=1.04\columnwidth,height=0.60\textheight,keepaspectratio]{imgs/toy_superposition_extra_feature.png}
\end{center}

:::
::::

\vspace{-1.8em}

\noindent\hspace{0.05\textwidth}\begin{minipage}{0.43\textwidth}
\[
\begin{aligned}
h &= Wx\\
x' &= \operatorname{ReLU}(W^T h + b)\\
x' &= \operatorname{ReLU}(W^T W x + b)
\end{aligned}
\]
\end{minipage}
\hspace{0.2em}
\begin{minipage}{0.34\textwidth}
\[
L = \sum_x \sum_i I_i(x_i - x'_i)^2
\]
\end{minipage}

\vspace{0.1em}

\scriptsize (Elhage et al., "Toy Models of Superposition", Transformer Circuits Thread, 2022.)

---

# Why Compress Tracr Models?

\vspace{1.0em}

\begin{center}
\setlength{\tabcolsep}{0.7em}
\renewcommand{\arraystretch}{1.45}
\begin{tabular}{@{}p{0.41\textwidth}c p{0.41\textwidth}@{}}
\large \textcolor{darkgreen}{In toy models we see superposition if} & & \large \textcolor{darkgreen}{In Tracr models}\\[0.5em]
1. Features are \textbf{sparse} & \Large $\Longrightarrow$ & 1. Features are \textbf{sparse}\\
2. Some features are more \textbf{important} than others & \Large $\Longrightarrow$ & 2. Some features are more \textbf{important} for the computation\\
3. The model has to use \textbf{fewer dimensions than features} & \Large \textcolor{lightgreen}{$\Longrightarrow$} & 3. Can we \textbf{compress} the model to use \textbf{fewer dimensions}?\\
\end{tabular}
\renewcommand{\arraystretch}{1.0}
\end{center}

\vspace{0.8em}

\begin{block}{}
\footnotesize Tracr models already have sparse, meaningful variables. If we force their residual stream to use fewer dimensions, we can study superposition with a known feature basis.
\end{block}

---

# Linear Compression Objective

\vspace{0.8em}

\begin{center}
\includegraphics[width=0.78\columnwidth,height=0.34\textheight,keepaspectratio]{imgs/linear_compression.png}
\end{center}

\vspace{-0.2em}

\begin{center}
\scriptsize We train $W \in \mathbb{R}^{D \times d}$ to minimize:

\vspace{0.2em}

{\scriptsize
$\displaystyle \mathcal{L}_{\mathrm{total}}(W) =
\mathbb{E}_{x}\!\left[
\mathcal{L}_{\mathrm{out}}(W, x) + \mathcal{L}_{\mathrm{layer}}(W, x)
\right]$
}

\vspace{0.4em}

\begin{minipage}{0.42\textwidth}
\centering
{\scriptsize $\displaystyle \mathcal{L}_{\mathrm{out}}(W, x) =
\mathrm{loss}\!\left(f(x), \hat{f}_{W}(x)\right)$}\\[0.25em]
\textcolor{darkgreen}{\footnotesize \textbf{minimize output loss}}
\end{minipage}
\hspace{1.5em}
\begin{minipage}{0.45\textwidth}
\centering
{\scriptsize $\displaystyle \mathcal{L}_{\mathrm{layer}}(W, x) =
\sum_{\mathrm{layer}\ i}\left(h_i(x)-\hat{h}_{W,i}(x)\right)^2$}\\[0.25em]
\textcolor{darkgreen}{\footnotesize \textbf{implement the same computation}}
\end{minipage}
\end{center}

\vspace{-0.2em}

\begin{block}{In plain English}
\scriptsize Train only a compression map $W$: the compressed model should preserve the final output and keep each intermediate layer close to the original compiled computation.
\end{block}

---

# What Changes After Compression?

\begin{center}
\includegraphics[width=0.82\columnwidth,height=0.52\textheight,keepaspectratio]{imgs/embeddings_superposition.png}
\end{center}

The learned $W^T W$ structure is qualitatively different from PCA: less important and more independent features are packed into shared directions.

---

# Which Features Enter Superposition?

:::: columns
::: {.column width="43%"}

\vspace{2.0em}

The lecture highlights three drivers:

\vspace{0.6em}

\begin{itemize}\setlength\itemsep{0.75em}
\item \textbf{Importance:} how much the computation needs the feature
\item \textbf{Density:} how often the feature is active
\item \textbf{Linear independence:} how easily it can share directions with others
\end{itemize}

:::
::: {.column width="54%"}

\begin{center}
\includegraphics[width=\columnwidth,height=0.66\textheight,keepaspectratio]{imgs/which_features_superposition.png}
\end{center}

:::
::::

---

# Discussion Questions

\begin{itemize}\setlength\itemsep{1.0em}
\item \textbf{Can Tracr create evaluation benchmarks} for interpretability tools?
\item \textbf{Can we reverse superposition} in Tracr models?\\
\textit{Sparse coding, dictionary learning}
\item \textbf{Can we manually replace model components} we think we understand?
\end{itemize}

---

# Summary

:::: columns
::: {.column width="56%"}

\begin{itemize}\setlength\itemsep{0.75em}
\item Tracr compiles RASP programs into transformer weights
\item The compiled model has a known mechanism
\item This gives interpretability methods an answer key
\item Compression induces superposition in a controlled feature basis
\item The main value is experimental control, not realism
\end{itemize}

:::
::: {.column width="40%"}

\begin{exampleblock}{Resources}
\url{https://github.com/google-deepmind/tracr}

\vspace{0.5em}

\url{https://arxiv.org/abs/2301.05062}
\end{exampleblock}

:::
::::

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References

\scriptsize
\begin{list}{}{
\setlength{\leftmargin}{1.4em}
\setlength{\itemindent}{-1.4em}
\setlength{\labelwidth}{0pt}
\setlength{\labelsep}{0pt}
\setlength{\itemsep}{0.55em}
\setlength{\parsep}{0pt}
\setlength{\topsep}{0pt}
}
\item Lindner, David, János Kramár, Sebastian Farquhar, Matthew Rahtz, Thomas McGrath, and Vladimir Mikulik. 2023. "Tracr: Compiled Transformers as a Laboratory for Interpretability." arXiv:2301.05062.
\item Weiss, Gail, Yoav Goldberg, and Eran Yahav. 2021. "Thinking Like Transformers." International Conference on Machine Learning.
\item Cammarata, Nick, Shan Carter, Gabriel Goh, Chris Olah, Michael Petrov, Ludwig Schubert, Chelsea Voss, Ben Egan, and Swee Kiat Lim. 2020. "Thread: Circuits." Distill.
\item Cammarata, Nick, Shan Carter, Gabriel Goh, Chris Olah, Michael Petrov, Ludwig Schubert, and Chelsea Voss. 2021. "Curve Circuits." Distill.
\item Olah, Chris, Alexander Mordvintsev, and Ludwig Schubert. 2017. "Feature Visualization." Distill.
\item Elhage, Nelson, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, and others. 2022. "Toy Models of Superposition." Transformer Circuits Thread.
\end{list}
