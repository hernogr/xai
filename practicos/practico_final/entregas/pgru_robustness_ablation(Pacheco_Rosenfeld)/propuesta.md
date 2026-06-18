# PGRU Robustness and Component Ablation via Synthetic Data (Pacheco, Rosenfeld)

**Integrantes:** Paula Pacheco, Hernán Rosenfeld

---

## Objetivos

Este trabajo plantea dos preguntas de investigación complementarias sobre el modelo PGRU (*Physics-Guided Regime Unmixing*, Pacheco et al., 2026):

**Pregunta 1:** ¿Es el modelo PGRU capaz de recuperar con precisión las abundancias de materiales en píxeles con mezclas complejas y niveles variables de ruido?

**Pregunta 2:** ¿Cuánto contribuye cada componente de PGRU —el ensemble de modelos físicos (GBM/PPNM/Hapke), la activación guiada por features físicas ($\xi_i$), y la regularización espacial del mapa de régimen— a la mejora de reconstrucción y a la coherencia física del modelo?

**Hipótesis central:** El modelo PGRU presenta una mayor robustez que los modelos tradicionales para estimar abundancias en escenarios donde la mezcla no es puramente lineal, manteniendo un error bajo incluso ante la presencia de ruido y variabilidad en el grado de interacción entre materiales. A su vez, se hipotetiza que esta robustez se extiende a dinámicas de mezcla no lineales que no están explícitamente incorporadas en el diseño matemático de su ensemble (como MLM). Además, los tres componentes internos del modelo contribuyen de forma independiente y cuantificable: la activación guiada por features físicas ($\xi_i$) es el factor dominante en la coherencia física ($\rho$), mientras que el ensemble de modelos contribuye principalmente a la precisión de reconstrucción (rRMSE).

---

## Propuesta Experimental

### Parte 1 — Generación de datos sintéticos y evaluación de robustez

El núcleo de este experimento consiste en la creación de un entorno controlado con *ground-truth* conocido para auditar el desempeño del modelo.

**Modelos de mezcla para simulación.** Se generarán píxeles ficticios utilizando cuatro arquitecturas matemáticas que representan diferentes interacciones físico-químicas de la luz:
* **LMM** (*Linear Mixing Model*): El estándar donde cada fotón interactúa con un solo material antes de llegar al sensor (Keshava & Mustard, 2002; Bioucas-Dias et al., 2012).
* **GBM** (*Generalized Bilinear Model*): Modela interacciones de segundo orden, como rebotes de luz entre dos materiales distintos (Halimi et al., 2011).
* **PPNM** (*Post-Nonlinear Mixing Model*): Aplica una distorsión polinomial después de la mezcla, simulando efectos de sensores o sombras (Altmann et al., 2012).
* **MLM** (*Multilinear Mixing Model*): Representa interacciones de orden infinito mediante una cadena de Markov, ideal para vegetación densa (Heylen & Scheunders, 2016).

**Evitar la circularidad en la evaluación:** Como PGRU ya usa los modelos GBM y PPNM en su estructura interna, evaluarlo solo con datos generados por esos mismos modelos le daría una ventaja artificial. Para hacer una prueba realmente independiente, usaremos **MLM** como un escenario de validación externa. Dado que MLM es un modelo matemático que PGRU no conoce ni utiliza por dentro, ver cómo rinde frente a estos píxeles sintéticos será la prueba definitiva de su verdadera robustez y de su capacidad para adaptarse a situaciones reales que no fueron contempladas en su diseño.

**Control de variables.** Para estresar el modelo PGRU, se variarán sistemáticamente los siguientes parámetros:
* **Niveles de Ruido:** Se evaluará la relación señal-ruido (**SNR**) en 20, 30 y 40 dB.
* **Grado de No Linealidad:** Se barrerán los parámetros de interacción ($\gamma$ en GBM y $P$ en MLM) en un rango de 0 (lineal puro) a 1 (máxima complejidad).
* **Métricas de Evaluación:** Se utilizará el **RMSE** (Error Cuadrático Medio) para abundancias y la **SAD** (Distancia de Ángulo Espectral) para la reconstrucción.

### Parte 2 — Estudio de ablación de componentes

Este experimento extiende el trabajo presentado en PGRU mediante un estudio de ablación sistemático sobre los tres datasets de referencia ya utilizados (Samson, Jasper Ridge, Urban). Se entrena una variante del modelo por cada componente eliminado o degradado, manteniendo todo lo demás constante.

1. **Sin guía física (ξᵢ = constante):** Se reemplaza el mecanismo de activación basado en features observables por un escalar global, sin señal espacialmente variable. Mide cuánto aporta la localización del régimen.

2. **Modelo único (sin ensemble):** Se reemplaza la combinación GBM/PPNM/Hapke por un solo modelo no lineal, eliminando la atención sobre el ensemble. Mide cuánto aporta la diversidad de mecanismos físicos.

3. **Sin regularización espacial ($\lambda_{sp}$ = 0):** Se entrena el modelo completo sin el término Laplaciano que promueve coherencia del mapa de régimen. Mide el impacto en suavidad del mapa de activación y en coherencia física $\rho$.

4. **Sin decaimiento progresivo de $\lambda_{feat}$:** Se elimina la reducción gradual del término de guía física durante el entrenamiento. Mide si el esquema de entrenamiento es en sí mismo un componente relevante.

Para cada variante y para el modelo completo se reportan SAD, RMSE, rRMSE y coherencia física $\rho$ = corr($\xi$, \Delta_{res}). El análisis identifica qué componente es más crítico por dataset y si el ranking de importancia de features es consistente entre escenas.

---

## Plan de Actividades

| Semana | Tarea | Descripción Detallada |
| ------ | ------ | ------ |
| **Semana 1** | **Implementación del Generador** | Programación en Python (NumPy/PyTorch) de los modelos LMM, GBM, PPNM y MLM utilizando materiales puros (*endmembers*) de referencia. |
|  | **Preparación del estudio de Ablación** | Adaptación del código base de PGRU para soportar las cuatro variantes, con control de semilla y reproducibilidad. |
| **Semana 2** | **Simulación y Procesamiento** | Generación de datasets sintéticos bajo condiciones controladas de ruido y no linealidad. Ejecución del modelo PGRU sobre estos datos. |
|  | **Entrenamiento de Variantes** | Entrenamiento de las cuatro variantes abladas sobre los datasets Samson, Jasper Ridge y Urban. Verificación de reproducibilidad. |
| **Semana 3** | **Análisis de Robustez** | Cálculo de métricas (RMSE, SAD). Creación de curvas de degradación (Error vs. SNR) para identificar escenarios críticos de falla. **Análisis comparativo desagregado entre modelos conocidos por el ensemble (GBM/PPNM) y el modelo ciego (MLM) para discutir explícitamente el alcance y las limitaciones de la validación sintética.** |
|  | **Análisis de Ablación** | Cálculo de SAD, RMSE, rRMSE y coherencia física $\rho$ por variante y dataset. Generación de mapas de régimen comparativos y análisis estadístico de contribución relativa de cada componente. |
| **Semana 4** | **Redacción y Reporte** | Escritura del paper final, documentando el diseño experimental y las justificaciones físicas, integración de ambas secciones y revisión conjunta. |

---

## Relación con los Temas del Curso

- **Análisis mecanístico:** el proyecto se centra en entender los procesos físicos internos que llevan al modelo a elegir un régimen de mezcla específico, respondiendo a la pregunta de por qué un píxel es clasificado como no lineal.
- **Evaluación de robustez:** siguiendo los criterios de evaluación de explicaciones, se utilizan datos sintéticos y variabilidad de ruido (SNR) para auditar si el modelo mantiene coherencia y precisión en escenarios críticos.
- **Atribución de características (Feature Attribution):** los pesos $w$ del módulo de guía física son atribuciones interpretables sobre la decisión de activar régimen no lineal, vinculándose con los métodos de atribución vistos en clase.
- **Pitfalls y evaluación de explicaciones:** el ablation study valida que el mapa de régimen $\xi$ es efectivamente resultado de los componentes declarados y no de artefactos del entrenamiento.
- **Teoría de explicabilidad:** la coherencia física ρ actúa como métrica de faithfulness del mapa de régimen respecto al comportamiento real del modelo.

---

## Referencias

- Altmann, Y., Halimi, A., Dobigeon, N. and Tourneret, J-Y. (2012). Supervised nonlinear spectral unmixing using a postnonlinear mixing model for hyperspectral imagery. *IEEE Transactions on Image Processing*, 21(6):3017–3025.
- Bioucas-Dias, J. M., Plaza, A., Dobigeon, N., Parente, M., Du, Q., Gader, P. and Chanussot, J. (2012). Hyperspectral Unmixing Overview: Geometrical, Statistical, and Sparse Regression-Based Approaches. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*, 5.
- Covert, I., Lundberg, S. and Lee, S. (2021). Explaining by Removing: A Unified Framework for Model Explanation. *JMLR*, 22(209):1–90.
- Halimi, A., Altmann, Y., Dobigeon, N. and Tourneret, J-Y. (2011). Nonlinear unmixing of hyperspectral images using a generalized bilinear model. *IEEE Transactions on Geoscience and Remote Sensing*, 49(11):4153–4162.
- Hapke, B. (1981). Bidirectional reflectance spectroscopy: 1. Theory. *Journal of Geophysical Research: Solid Earth*, 86(B4):3039–3054.
- Heylen, R. and Scheunders, P. (2016). Multilinear Mixing Model for Hyperspectral Unmixing. *IEEE Transactions on Geoscience and Remote Sensing*, 54:1–12.
- Keshava, N. and Mustard, J. F. (2002). Spectral unmixing. *IEEE Signal Processing Magazine*, 19(1):44–57.
- Pacheco, P., Granitto, P. and Cabral, J.B. (2026). Physics-Guided Regime Unmixing. arXiv:2605.04247.
- Zhu, F. (2017). Hyperspectral unmixing: ground truth labeling, datasets, benchmark performances and survey. arXiv:1708.05125.