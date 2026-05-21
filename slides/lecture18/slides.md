---
title: "\\emoji{fire} XAI: Interpreting GAN Latent Spaces"
bibliography: references.bib

---

# Disclaimer

\input{../disclaimer.tex}

---

# Paper 1: GANSpace {.plain}

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/paper1_title.png}
\end{center}

[@harkonen2020ganspace]

---

# GANSpace: Motivation

- GANs are models trained to generate realistic-looking images well—and they do!
- They have not been designed, however, to make the image-generation process
itself interpretable, or to support edits to generated images
- E.g.: This GAN generates faces well and can take in high-level styles or criteria
(gender, age, race), but is not designed to facilitate post-hoc continuous and
meaningful edits, such as head angle, hair length, lighting...

\vspace{1em}
\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/ganspace_motivation.png}
\end{center}



---

# Main Contributions

- Applying a simple technique (**PCA**) in the latent space of GANs gives
semantically significant directions.
- Perturbing inputs in these directions in certain layers of the GANs $\rightarrow$
interpretable edits in properties of generated images.
- Such edits are high-level and nuanced (e.g. object shape to background
landscape)
- A user need only label each “control direction” once to edit the image

## In plain english

In other words, the authors posit that exploring the “EiGANspace” gives us new controls to edit and possibly better understand GANs at low cost

---

# Main contributions example

\vspace{1em}
\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/contributions_example}
\end{center}


---

# Background: Generative Adversarial Networks

> Seminal Paper: *Goodfellow et al. (2014)*

- **Objective:** Generative Image Modeling—create realistic-looking, artificial
images that resemble the training data.
- **GAN** = Generator (G) + Discriminator (D) networks, both CNNs in image
context.
    - **Generator** $G$: maps latent $\mathbf{z}$ to image $G(\mathbf{z})$
    - **Discriminator** $D$: distinguishes real vs. generated images

\vspace{1em}
\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/gan_background.png}
\end{center}


---

# Background: BigGAN

- Class-conditional GAN for high-resolution ImageNet images
- Latent vector $\mathbf{z}$ is passed as **additional input** to all layers (no separate style vector)
- State-of-the-art for diverse, high-quality image generation

\begin{center}
\includegraphics[width=0.55\columnwidth]{imgs/biggan_background.png}
\end{center}

---

# Background: StyleGAN

- Style-based generator: separates high-level attributes from stochastic variation
- Maps $\mathbf{z} \rightarrow \mathbf{w}$ via mapping network; $\mathbf{w}$ controls synthesis via AdaIN
- **$\mathbf{w}$-space** is more disentangled than $\mathbf{z}$-space

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/stylegan_background.png}
\end{center}

---

# Background: PCA

- **Principal Component Analysis**: finds orthogonal axes of maximum variance
- Given data $\mathbf{y}_{1:N}$, PCA yields basis $\mathbf{V}$ and mean $\boldsymbol{\mu}$
- Project data: $\mathbf{x}_{1:N} = \mathbf{V}^T(\mathbf{y}_{1:N} - \boldsymbol{\mu})$
- First PCs capture the most variance; later PCs capture finer details

---

# Related Work

- **Supervised directions**: require attribute labels to train classifiers in latent space
- **GAN analysis**: SeFa, closed-form factorization of generator weights
- GANSpace is **unsupervised** — no attribute annotations needed
- Related applications: camera motion, scene synthesis, image memorability

---

# Methods: StyleGAN Approach

**Idea**: PCA directly on $\mathbf{w}$-space samples

1. Sample $N$ random $\mathbf{z}_{1:N}$, pass through mapping network to get $\mathbf{w}_{1:N}$
2. Apply PCA to $\mathbf{w}_{1:N}$ → basis $\mathbf{V}$, mean $\boldsymbol{\mu}$
3. Represent each $\mathbf{w}$ in new basis: $\mathbf{x} = \mathbf{V}^T(\mathbf{w} - \boldsymbol{\mu})$

\begin{exampleblock}{Editing}
Move in the $k$-th principal direction with magnitude $\alpha$:
$$\mathbf{w}' = \mathbf{w} + \alpha \mathbf{v}_k$$
Apply $\mathbf{w}'$ to some or all synthesis layers for global vs. localized edits.
\end{exampleblock}

---

# Methods: BigGAN Approach

**Issue**: BigGAN has no separate style vector; $\mathbf{z}$ is passed as input at each layer

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/ganspace_pca_biggan.png}
\end{center}

**(Step 1)** PCA at intermediate layer $i$: sample $\mathbf{z}_{1:N}$, process to $\mathbf{y}_{1:N}$, apply PCA → $\mathbf{V}$, $\boldsymbol{\mu}$, project to $\mathbf{x}_{1:N} = \mathbf{V}^T(\mathbf{y}_{1:N} - \boldsymbol{\mu})$

**(Step 2)** Find latent directions: $\mathbf{U} = \arg\min_{\mathbf{U}} \sum_j \|\mathbf{U}\mathbf{x}_j - \mathbf{z}_j\|^2$

Edit: $\mathbf{z}' = \mathbf{z} + \mathbf{U}\mathbf{x}$

---

# Methods: Granularity of Edits

:::: columns
::: {.column width="50%"}
**Layerwise control**

- **StyleGAN**: pass modified $\mathbf{w}'$ to some layers, original $\mathbf{w}$ to others
- **BigGAN**: pass modified $\mathbf{z}'$ to some layers + keep original $\mathbf{z}$ at start of network
:::
::: {.column width="50%"}
**Composed edits**

- Edits can be *composed* by moving in **several** principal directions simultaneously
- Directions can be **labelled** by users to correspond to semantic concepts
:::
::::

---

# Findings and Results

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/ganspace_cats_grid.png}
\end{center}

\begin{exampleblock}{Key Finding 1}
Changing the \textbf{first 20} PCs in latent space corresponds to changes in image \textbf{layout}, \textbf{configuration}, and \textbf{perspective}; later PCs dictate object appearance, background, and smaller details.
\end{exampleblock}

---

# Findings and Results

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/ganspace_variance_pdf.png}
\end{center}

\begin{exampleblock}{Key Finding 2}
StyleGAN's \textbf{first 100 PCs sufficiently explain overall image} appearance, and are distributed unimodally and almost independently.
\end{exampleblock}

---

# Findings and Results

\begin{center}
\includegraphics[width=0.8\columnwidth]{imgs/ganspace_class_independent.png}
\end{center}

\begin{exampleblock}{Key Finding 3}
BigGAN's PCs seem to be \textbf{class-independent}: PCA gives the same results for different images in different classes.
\end{exampleblock}

---

# Analyzing GANs Through Principal Components

:::: columns
::: {.column width="48%"}
**Limitations** (inherited from dataset)

- StyleGAN faces cannot be translated in the image
- PCs for wrinkles/makeup have no effect on children/men

\begin{center}
\includegraphics[width=\columnwidth]{imgs/ganspace_limitations.png}
\end{center}
:::
::: {.column width="48%"}
**Entanglement/Superposition**

- One PC for StyleGAN cars corresponds to sportiness *and* open-road backgrounds
- Rotating a dog causes its mouth to open

\begin{center}
\includegraphics[width=\columnwidth]{imgs/ganspace_entanglement.png}
\end{center}
:::
::::

---

# Comparison with Related Techniques

:::: columns
::: {.column width="50%"}
**GANSpace (PCA)**

- Gives separated, ordered series of stylistic edit axes
- Random directions produce indiscernible changes

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/ganspace_comparison.png}
\end{center}
:::
::: {.column width="50%"}
**vs. Supervised methods**

- Results similar to supervised approaches, without extra training
- Provides **many more** edit directions
- Some additional entanglement
:::
::::

---

# Strengths / Weaknesses

:::: columns
::: {.column width="50%"}
\textcolor{primarygreen}{\textbf{Strengths}}

- Unsupervised and computationally simpler than supervised methods
- PC directions elucidate interpretable GAN latent representations
- After labelling directions, users can perform numerous edits on various styles
:::
::: {.column width="50%"}
\textcolor{red}{\textbf{Weaknesses}}

- Approach limited to specific GAN architectures
- PCs are not *a priori* linked to semantic meaning
- Choice of which PCs to modify at which layers seems arbitrary
- Entanglement of PC styles hinders practicality
- Does this constitute actual **interpretability** for GANs?
:::
::::

---

# GANSpace: Discussion Questions

- Are these principal components a useful tool for **interpreting** GANs?
- How does their utility compare with other interpretability methods we've studied?
- Most conceptually-aligned PCs for StyleGAN are in $\mathbf{w}$-space; most useful PCs for BigGAN originate in the first linear layer (then projected to $\mathbf{z}$-space)
- Do these findings provide novel insights into the models?
- How could this tool help **identify and reduce biases** in a model?

---

# GANSpace: Summary

Experiment targets: **StyleGAN**, **BigGAN** (methods differed for the models)

1. Changing the **first 20** PCs corresponds to changes in image **layout**, **configuration**, and **perspective**; later PCs dictate appearance and details
2. StyleGAN's **first 100 PCs** sufficiently explain overall image appearance, distributed unimodally and almost independently
3. BigGAN's PCs seem to be **class-independent**

[@harkonen2020ganspace]

---

# Paper 2: InterFaceGAN {.plain}

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/paper2_title.png}
\end{center}

[@shen2020interfacegan]

---

# InterFaceGAN: Roadmap

- Introduction
- Method
- Experiments

---

# Background: What are GANs?

- **GAN**: generative models that generate realistic synthetic data mimicking training data
  - **Generator**: generates samples similar to training data
  - **Discriminator**: distinguishes generated (fake) from real samples
- **Latent representation**: a low-dimensional representation of an image
- **Latent space**: the set of all possible latent representations
  - Through adversarial training, the generator learns a mapping from latent space to real images

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/gan_diagram.png}
\end{center}

---

# Background: GANs for Image Editing

- **Latent code**: the version of an image in the latent space
  - **GAN inversion**: identifying the latent code for a given image such that the generator could reconstruct it
- **Semantic editing**: editing the latent code to manipulate some features of the resulting image, such that only the desired features are changed

\begin{center}
\includegraphics[width=0.6\columnwidth]{imgs/latent_code_editing.png}
\end{center}

---

# Related Work

- **Exploring latent spaces in GANs**
  - Laine et al.: smoothly varying outputs across latent space
  - Radford et al. observe the *vector arithmetic property*:
    `vector("King") - vector("Man") + vector("Woman") = vector("Queen")`
  - Applications in camera motion, scene synthesis, memorability

- **Semantic face editing with GANs**
  - Previous methods required carefully designed loss functions or specialized architectures
  - No existing method to perform controlled facial editing by varying latent codes

---

# Research Questions

- **How do semantics in the latent space originate, and how are they organized?**
  - Does there exist structure in the latent space relating to disentangled semantic representations?
- **What does a GAN actually learn with respect to the latent space?**
  - How does the GAN connect the latent space and the image semantic space?
- **How can the latent code be used for image editing?**
  - How are various semantic attributes of an individual's face (gender, age) determined and entangled?

---

# Contributions and Main Findings

- Proposed **InterFaceGAN**, a framework to identify semantics encoded in the latent space of face synthesis models
  - GANs learn **latent subspaces** corresponding to specific attributes
- InterFaceGAN enables **semantic face editing with any pre-trained GAN**
  - Found theoretical and experimental results verifying that linear subspaces align with emerging semantics
- Applied InterFaceGAN to **real image editing**
  - Successfully edited attributes of real faces by varying the latent code

---

# Method: Semantic Subspace

For any binary attribute, define the signed distance from hyperplane $\mathbf{n}$:

$$d(\mathbf{n}, \mathbf{z}) = \mathbf{n}^T \mathbf{z}$$

\begin{alertblock}{Key Hypothesis}
The generator $g$ satisfies:
$$f(g(\mathbf{z})) = \lambda \, d(\mathbf{n}, \mathbf{z})$$
where $f$ scores the semantic attribute. The hyperplane $\mathbf{n}^T\mathbf{z} = 0$ separates the latent space into two semantic regions.
\end{alertblock}

In practice, find $\mathbf{n}$ by training a **linear SVM** on labeled latent codes.

---

# Method: Conditional Manipulation

To edit attribute $A_1$ while **preserving** attribute $A_2$, project out the component of $\mathbf{n}_1$ along $\mathbf{n}_2$:

$$\mathbf{n}_1^* = \mathbf{n}_1 - (\mathbf{n}_1^T \mathbf{n}_2)\mathbf{n}_2$$

\begin{center}
\includegraphics[width=0.5\columnwidth]{imgs/interfacegan_subspace_projection.png}
\end{center}

Move along $\mathbf{n}_1^*$ to change $A_1$ while remaining on the hyperplane of $A_2$.

---

# Experiment 1: Latent Space Separation

**Model**: PGGAN (Progressive Growing GAN) — trained on CelebA-HQ (30K images, 40 attributes)

\begin{center}
\includegraphics[width=0.8\columnwidth]{imgs/pggan_architecture.png}
\end{center}

\begin{block}{Assumption}
For any binary attribute, there exists a hyperplane in latent space such that all samples from the same side share the same attribute.
\end{block}

---

# Experiment 1: Hyperplane Assumption

\begin{center}
\includegraphics[width=0.55\columnwidth]{imgs/separation_hyperplane.png}
\end{center}

Train 5 independent linear SVMs on pose, smile, age, gender, eyeglasses. Evaluate on validation set (6K samples) and full set (480K samples).

---

# Experiment 1: Classification Accuracy

\begin{center}
\includegraphics[width=0.75\columnwidth]{imgs/interfacegan_separation_table.png}
\end{center}

High accuracy on validation set (95.6–100%) confirms that **linear hyperplanes successfully separate semantic attributes** in latent space.

---

# Experiment 1: Latent Space Visualization

Choose $\mathbf{z}$ far away from and on the decision boundary, then generate from it.

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/interfacegan_separation_viz.png}
\end{center}

---

# Experiment 2: Single Attribute Manipulation

Verify whether the semantics found by InterFaceGAN are manipulable.

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/interfacegan_single_attr.png}
\end{center}

Generate central image, then move away from boundary in positive/negative directions. Works for pose, smile, age, gender, eyeglasses.

---

# Experiment 2: Distance Effect

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/interfacegan_distance_effect.png}
\end{center}

Samples suffer severe appearance changes when moved **too far** from the boundary — extreme samples are unlikely to be drawn from a standard normal distribution.

---

# Experiment 2: Artifacts Correction

\begin{center}
\includegraphics[width=0.7\columnwidth]{imgs/interfacegan_artifacts.png}
\end{center}

Manually labelled 4K bad syntheses (with artifacts), trained a linear SVM to find the separation hyperplane, then moved along the "quality" direction to fix them.

---

# Experiment 3: Conditional Manipulation

Study the disentanglement between different attributes.

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/interfacegan_correlation_tables.png}
\end{center}

Attribute correlations (age$\leftrightarrow$gender, age$\leftrightarrow$eyeglasses) reflect those in the training dataset — male older people are more likely to wear eyeglasses.

---

# Experiment 3: Conditional Manipulation Results

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/interfacegan_conditional_results.png}
\end{center}

Conditional manipulation preserves the untargeted attribute while editing the targeted one.

---

# Experiment 4: Results on StyleGAN

**StyleGAN** extends PGGAN with:

| Component | Description |
|---|---|
| **Mapping Network** | Casts $\mathbf{z}$ as $\mathbf{w}$ ("style vector") |
| **Synthesis Network** | Uses style vector + noise via AdaIN |
| **Bilinear Sampling** | Replaces nearest-neighbor upsampling |
| **Mixing Regularization** | Uses 2 latent codes to generate |

\begin{center}
\includegraphics[width=0.65\columnwidth]{imgs/stylegan_architecture.png}
\end{center}

---

# Experiment 4: W-Space vs Z-Space

\begin{center}
\includegraphics[width=0.85\columnwidth]{imgs/interfacegan_stylegan_results.png}
\end{center}

- **W-space** learns a more disentangled representation
- **W-space** performs better in long-distance manipulation
- **W-space** better captures attribute correlations

---

# Experiment 5: Real Image Manipulation

Take a real face image → invert to latent code → use InterFaceGAN to edit.

:::: columns
::: {.column width="50%"}
**Latent Code Optimization**

Optimize latent code with fixed generator to minimize pixel-wise reconstruction error.

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/interfacegan_real_image.png}
\end{center}
:::
::: {.column width="50%"}
**Encoder-Based**

Extra encoder learns inverse mapping from image to latent code by training with generator and discriminator.

\begin{center}
\includegraphics[width=0.9\columnwidth]{imgs/interfacegan_encoder.png}
\end{center}
:::
::::

---

# InterFaceGAN: Discussion Questions

1. Do you believe the use of GANs for generating photo-realistic images should be **regulated**? (Potential misuse)
2. Why do we think there are such simple linear boundaries separating binary semantics in the latent space (is it only for face GANs)?
3. How can analyzing semantic representations be used to **detect biases** in the training data?
4. Have you ever used GANs for photo generation, if so how realistic did you find them?
5. How relevant is this paper given that **GANs are progressively going out of style** (diffusion taking over)?

---

\begin{center}
\Huge Thank You!
\end{center}

---

# References {.allowframebreaks}

\footnotesize
