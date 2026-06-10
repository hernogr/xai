# Images to Replace — Lecture 24

| Archivo | Slide PDF (página) | Contenido |
|---|---|---|
| `cos_e_examples_table.png` | 3 | Table 1: CoS-E dataset examples (Question, Choices, CoS-E explanation for 3 samples) |
| `dataset_structure.png` | 9 | Diagram showing CQA (red box) + CoS-E (blue box) structure with hamburger example |
| `dataset_considerations_chart.png` | 10 | Horizontal bar chart: % of examples containing Answer / Distractor / Answer or Distractor / Question Bigram / Question Trigram |
| `cage_phase1_diagram.png` | 14 | CAGE Phase 1 intuition: sequence [Q, A0, A1, A3, E0, ..., E_{i-1}] → LM → E_i. "One training step for CAGE" |
| `cage_phase2_diagram.png` | 21 | CAGE Phase 2 intuition: [Q, A0, A1, A3] → LM → [E0...En] + direct path → CSRM → A1 |
| `experimental_results_table2.png` | 25 | Table 2: BERT baseline 63.8%, CoS-E-open-ended 65.5%, CAGE-reasoning 72.6% |
| `experimental_results_sota.png` | 26 | Table (right column): RC 47.7%, GPT 54.8%, CoS-E-open-ended 60.2%, CAGE-reasoning 64.7% |
| `experimental_results_oracle.png` | 27 | Table 4: Oracle results — CoS-E-selected w/o ques 53.0%, ..., CoS-E-open-ended* 89.8% |
| `transfer_results.png` | 29 | Transfer table: Method vs SWAG vs Story Cloze — BERT 84.2/89.8, BERT+expl transfer 83.6/89.5 |
| `baseline_bert_examples.png` | 32 | Two side-by-side example tables showing CAGE Reason vs CoS-E explanations for CQA questions |
| `domain_transfer_examples.png` | 33 | Large table with SWAG and Story Cloze (ROCStories) examples with Question, Choices, Explanation columns |
| `motivation_gradient_input.png` | 39 | Diagram showing forward pass → logits → sample token → back-propagate gradient → Gradient×Input feature importance (Jay Alammar style) |
| `motivation_problem.png` | 40 | Box: Input "Can you stop the dog from" / Output "barking" / Why did model predict "barking"? → highlight on "from" |
| `contrastive_key_ideas.png` | 41 | Side-by-side: non-contrastive (highlight "from") vs. contrastive explanations Q1 "barking" vs "crying", Q2 "barking" vs "walking" with red/blue highlights |
| `method_contrastive.png` | 48 | Two green boxes: "why did model predict y?" → "why predict y_t instead of foil y_f?"; Two dark boxes: "gradients of logit of y" → "gradients of difference in logits y_t and y_f" |
| `method_formulas_table.png` | 49 | Table with 3 rows (Gradient Norm, Gradient×Input, Input Erasure) × 2 cols (Non-Contrastive, Contrastive) showing all saliency score formulas |
| `method_lm_diagram.png` | 50 | Same as motivation_gradient_input.png but with yellow highlight on step 3 "we calculate and back-propagate a different quantity" |
| `blimp_table.png` | 52 | BLiMP paradigms table: Phenomenon, UID, Acceptable Example, Unacceptable Example for Anaphor Agreement, Argument Structure, Det-Noun Agreement, NPI Licensing, Subject-Verb Agreement |
| `linguistic_agreement_bars.png` | 54 | Figure 1: 3 subplots (Dot Product, Probes Needed, MRR) × 2 models (GPT-2, GPT-Neo), orange bars = non-contrastive, hatched blue = contrastive |
| `linguistic_agreement_scatter.png` | 55 | Figure 2: Scatter plot distance vs. difference in MRR for GPT-2 and GPT-Neo with Pearson r values |
| `user_study.png` | 56 | Figure 3: Example user study prompt — colored token saliency bar + "Which token did model predict?" + "Was explanation useful?" question |
| `user_alignment_table.png` | 57 | Table 3: Simulation accuracy (%) for None/S_GI/S*_GI/S_E/S*_E — Acc, Acc Correct, Acc Incorrect, Acc Useful, Acc Not Useful columns |
| `context_decisions_table.png` | 59 | Table: Phenomenon/POS, Target, Foil Cluster, Embd Nearest Neighbors, Example — for Anaphor Agreement, Animate Subject, Determiner-Noun Agreement |
