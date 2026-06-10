# Images to Replace — Lecture 25

## Paper 1: Acquisition of Chess Knowledge in AlphaZero

| Archivo | Slide PDF (página) | Contenido |
|---|---|---|
| `alphazero_network.png` | 4 | AlphaZero network diagram: input z⁰ → 20 ResNet blocks (3x3 conv; 256 channels) → policy head p + value head v; with residual connection formulas on the right |
| `human_concepts_evolution.png` | 8 | 6 3D surface plots (Block × Training steps × Test accuracy) for: total_t_ph, has_contested_open_file, in_check, threats_t_ph, can_capture_queen_opponent, has_mate_threat |
| `progression_human_history.png` | 13 | Stacked area chart of opening moves (d4, e4, Nf3, c4, …) by year from [1400,1800] to [2010,2020] |
| `progression_alphazero_history.png` | 14 | Three stacked area charts of AlphaZero opening move priors (same color coding) vs. training steps 0 to 1,000,000 |
| `opening_theory_plots.png` | 16 | 3 scatter plots: (1) AZ prior at starting position: 1.d4 vs 1.e4 over 0–100k steps; (2) After 1.e4 e5: 2.Nf3 vs 2.d4; (3) After 1.e4: 1…c5,c6,e5,e6 vs all other 16 moves |
| `material_positional_plots.png` | 17 | Left: piece value line plots (Queen, Rook, Bishop, Knight) in pawns over 10³–10⁶ training steps. Right: concept weight line plots (Imbalance, King Safety, Material, Mobility, Space, Threats) over training steps |
| `kramnik_photo.png` | 18 | Photo of GM Vladimir Kramnik (man in suit, thinking pose, chess pieces visible) |
| `nmf_results.png` | 23 | 3×2 grid of chess board visualizations: left column = Diagonal Moves (1st Layer), middle = Diagonal Moves (2nd Layer), right = # of Pieces that could move to each square. Green/tan highlighted squares. |
| `covariance_results.png` | 25 | Row of 5 chess boards showing 5 covariances with different channels for square (5,4): 1-2 diagonal-attacking, 3-4 horizontal-attacking, 5 both |

## Paper 2: What the DAAM

| Archivo | Slide PDF (página) | Contenido |
|---|---|---|
| `daam_intro.png` | 31 | Right side of outline slide: top = "monkey with hat walking" prompt + generated image; bottom = DAAM heatmaps for "monkey", "hat", "walking" (red-green-blue overlay) |
| `generative_models_comparison.png` | 35 | Final animation state: GAN/VAE/Flow rows faded, Diffusion row highlighted. Shows x₀→x₁→x₂→…→z forward and reverse arrows. Source: lilianweng blog. Labels "Multi-step time-series" visible. |
| `image_generation_unet.png` | 36 | Conditioning "7" → embed → UNet (blue box "predicts") → noisy image = noise + clean "7" image. Source: Deep Learning Foundations to Stable Diffusion 2022. |
| `unet_architecture.png` | 37 | Classic U-Net encoder-decoder with skip connections (blue channels). Reference: [1505.04597]. |
| `forward_reverse_process.png` | 39 | Two rows of truck images: top row = forward process (clean→noisy, →, white arrow), bottom row = reverse process (←, denoising model ε_θ(image, timestep)). Source: Diffusion models from scratch in PyTorch. |
| `ldm_with_latent.png` | 44 | Diagram with two dogs: Input dog → Encoder → noisy latent (Add noise in latent space) → UNet → Denoised image in latent space → Decoder → Output dog. Label "Easier to estimate noise in latent space!" |
| `sd_architecture.png` | 48 | Full LDM architecture diagram: pixel space (pink) with x,E,D; latent space (green) with diffusion process and denoising U-Net with Q/K/V cross-attention blocks; conditioning (black box) with Text/BERT tokenizer/τ_θ transformer. Cross-attention highlighted in red box. |
| `daam_heatmaps_method.png` | 50 | Diagram: "monkey with hat walking" → τ_θ → token "hat" → LDM architecture with red arrows from Q/K/V blocks → "Sum of cross-attention maps for 30 timesteps wrt 'hat' token" → overlay heatmap on monkey+hat image |
| `daam_formula.png` | 51 | Formula diagram: F_t^(i)↓ ∈ ℝ^[w/cⁱ]×[h/cⁱ]×l_H×l_W with annotations (Width/height of downsampled UNet block, Number of words, Number of attention heads). D_k^ℝ[x,y] := Σ F̃^(i)↓_{tj,k,ℓ}[x,y] + F̃^(i)↑_{tj,k,ℓ}[x,y] with subscript annotations. Right side shows bicubic interpolation → summed map diagram. |
| `object_attribution.png` | 53 | Three side-by-side heatmap images of monkey: labeled "monkey" (face highlighted red), "hat" (hat area highlighted red), "walking" (lower body highlighted red) |
| `segmentation_table.png` | 54 | Table with # Method / COCO-Gen (mIoU⁸⁰, mIoU∞) / Unreal-Gen columns. Supervised: Mask R-CNN, QueryInst, Mask2Former, CLIPSeg. Unsupervised: Whole image, PiCIE+H, STEGO, Our DAAM-0.3/0.4/0.5 (DAAM-0.4 in bold). Right: IoU = Area of Overlap / Area of Union Venn diagram. |
| `generalized_attribution.png` | 55 | 2×3 grid: NUM (three giraffes), ADV (running person, "quickly" highlighted), ADJ (blue teapot), VERB (running man, "running"), PROPN (Eiffel tower), NOUN (plate of oranges). Each shows original + heatmap. |
| `user_study_results.png` | 56 | Left: "Human Rater Opinion by Part of Speech" horizontal bar chart (NUM, ADV, ADJ, VERB, PROPN, NOUN vs Poor/Fair/Good/Excellent). Below: "Proportion of Fair-Excellent Scores by POS" bar chart. Right: stacked bar chart "Response Statistics by Part of Speech" (Error/Poor image/Too abstract/No error). |
| `visuosyntactic_head_dependent.png` | 59 | Three sentence boxes: "The [cat] sat on the [mat]" (Head=cat, Dependent=mat), "The [red] [car]" (Dependent=red, Head=car), "She [ate] the [pizza]" (Head=ate, Dependent=pizza). Blue/pink boxes with Head/Dependent annotations. |
| `measures_of_overlap.png` | 60 | 2×2 grid of Venn diagrams: mIoD (small blue circle inside red), mIoH (small red inside blue), mIoD>mIoH (red larger), mIoD<mIoH (blue larger). Labels on right: mIoU, mIoD, mIoH definitions. |
| `visuosyntactic_table.png` | 63 | Table: # Relation / mIoD / mIoH / Δ / mIoU for: Unrelated pairs (65.1/66.1), All head-dep pairs (62.3/62.0), compound (71.3/71.5), punct, nconj:and, det, case, acl, nsubj, amod, nmod:of, obj, Coreferent word pairs (84.8/77.4). |
| `visuosyntactic_examples.png` | 64 | 4×3 grid of paired image examples showing relations: unrelated (smiles/tv), compound (ice/cream), punct (baseball/<comma>), nconj:and (cat/dog), det (the/donut), case (on/tv), amod (wooden/bench), nsubj (bird/stands), acl (people/performing), obj (wearing/shirt), nmod:of (pile/oranges), coreference (man/his). |
| `cohyponym_results.png` | 76 | Two sections: Top (Cohyponym "a giraffe and a zebra"): 4 generated images + 4 heatmaps labeled giraffe/zebra alternating, in blue box. Bottom (Non-cohyponym): same images faded. Takeaway boxes: "SD image generation worsens", "Generates one…not both", "Attribution maps overlap → Feature Entanglement" |
| `adjectival_results.png` | 80 | 2×4 grid: top row = heatmaps (rusty/rusty/metallic/wooden shovels), bottom row = heatmaps (bumpy/bumpy/smooth/spiky balls). Attribution maps shown as colored overlays. Takeaway: "Attribution maps for adjectives attend too broadly across images beyond nouns they modify → Feature Entanglement" |
