# Images to extract from Lecture_19_DiffROAR.pdf and Lecture_19_Privacy_Risk.pdf

| Archivo | Slide PDF (página) | Contenido |
|---|---|---|
| diffroar_title.png | DiffROAR p1 | Título del Paper 1: "Do Input Gradients Highlight Discriminative Features?" con autores |
| diffroar_assumption.png | DiffROAR p4 | Diagrama de Assumption (A): mayor magnitud de gradiente → mayor contribución |
| diffroar_framework.png | DiffROAR p9 | Diagrama del pipeline DiffROAR: D → f → attribution A → mask top-k/bot-k → retrain |
| diffroar_unmasking.png | DiffROAR p10 | Tres esquemas de enmascaramiento: random, meaningful, constant |
| diffroar_metric.png | DiffROAR p12 | Fórmula DiffROAR = PredPower(top-k) - PredPower(bot-k) con interpretación visual |
| diffroar_procedure.png | DiffROAR p17 | Procedimiento de 5 pasos para el experimento |
| diffroar_results.png | DiffROAR p18 | Plots de 4 paneles: DiffROAR por método en SVHN/FashionMNIST/CIFAR-10/ImageNet-10 |
| diffroar_blockmnist.png | DiffROAR p20 | Dataset BlockMNIST: dos dígitos lado a lado (relevante y espurio) |
| diffroar_not_always.png | DiffROAR p21 | Resultados "Not always!": DiffROAR positivo en BlockMNIST |
| diffroar_feature_leakage.png | DiffROAR p22 | Hipótesis de Feature Leakage: características relevantes vs espurias separadas |
| diffroar_theorem1.png | DiffROAR p26 | Theorem 1: enunciado formal sobre feature leakage |
| diffroar_empirical.png | DiffROAR p28 | Figure 5: DiffROAR vs grado de feature leakage en BlockMNIST |
| privacy_title.png | Paper p1 | Recorte del inicio del paper: título, autores y comienzo del abstract |
| privacy_motivation.png | Privacy p2 | Tres tipos de explicaciones XAI: LIME, gradient based, counterfactuals |
| privacy_mi_attribution.png | Privacy p7 | Ataques de MI previos vía feature attribution (múltiples queries) |
| privacy_attack_assumptions.png | Paper p3 / Table 1 | Supuestos de ataques MI: Loss, CFD, Loss LRT, CFD LRT |
| privacy_intuition.png | Privacy p23 | Intuición: puntos de entrenamiento más lejos del boundary → CFD mayor |
| privacy_attack1.png | Privacy p24 | Attack 1: umbral sobre CFD — M_Distance(x): MEMBER si c(x,x') ≥ τ_D |
| privacy_cfd_lrt.png | Paper p5 / Algorithm 1 | Algorithm 1: CFD LRT — shadow models, MLE, LRT statistic |
| privacy_dp_theorem.png | Privacy p31 | Theorem 1: BA_A ≤ 1/2 + (1 - e^{-ε})/2 bajo ε-DP |
| privacy_roc.png | Paper p7 / Figure 1 | Curvas ROC: CFD LRT vs CFD Thresholding vs random baseline |
| privacy_roc_scfe.png | Paper p7 / Figure 1(a) | Curvas ROC para SCFE: Adult, HELOC, Diabetes |
| privacy_roc_gs.png | Paper p7 / Figure 1(b) | Curvas ROC para Growing Spheres: Adult, HELOC, Diabetes |
| privacy_roc_cchvae.png | Paper p7 / Figure 1(c) | Curvas ROC para CCHVAE: Adult, HELOC |
| privacy_num_features.png | Paper p9 / Figure 2 | Efectos del número de features: mayor dimensionalidad → mayor éxito del ataque MI |
| privacy_model_arch.png | Paper p9 / Figure 3 | Efectos de la arquitectura del modelo: más compleja → mayor éxito del ataque MI |
