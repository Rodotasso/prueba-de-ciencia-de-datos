---
title: AI Epidemiology & Public Health Agent
emoji: 🏥
sdk: streamlit
app_file: app.py
pinned: false
license: mit
sdk_version: 1.49.1
tags:
- epidemiology
- public-health
- biostatistics
- survival-analysis
- data-science
---

# AI Epidemiology & Public Health Agent

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-lg.svg)](https://huggingface.co/spaces/Tassdreams/Data_Science_)

Un **Agente de Análisis Epidemiológico y Salud Pública potenciado por IA** especializado en investigación de nivel doctoral. Automatiza análisis bioestadísticos avanzados, modelos epidemiológicos y visualizaciones de salud pública.

## Características Especializadas en Epidemiología

### Modelos Epidemiológicos Avanzados
- **Análisis de Supervivencia**: Kaplan-Meier, curvas de supervivencia estratificadas, log-rank test
- **Cox Proportional Hazards**: Hazard ratios (HR) con IC 95%, forest plots, índice de concordancia
- **Regresión de Poisson**: Modelado de tasas de incidencia, Incidence Rate Ratios (IRR)
- **Odds Ratios**: Regresión logística para estudios caso-control, IC 95%
- **Risk Ratios (RR)**: Riesgo relativo, riesgo atribuible, PAR (Population Attributable Risk)
- **Standardized Mortality Ratio (SMR)**: Análisis de mortalidad estandarizada por estratos
- **Curvas Epidémicas**: Análisis de brotes, identificación de patrones de transmisión

### Visualizaciones Epidemiológicas
- **Pirámides Poblacionales**: Distribución por edad y sexo
- **Forest Plots**: Hazard ratios y odds ratios con intervalos de confianza
- **Curvas de Kaplan-Meier**: Análisis visual de supervivencia con censura
- **Epi Curves**: Visualización temporal de casos con medias móviles
- **Mapas de Calor Geográficos**: Incidencia y prevalencia por región
- **Tablas 2x2**: Análisis de asociación exposición-resultado
- **Tasas Ajustadas por Edad**: Estandarización demográfica

### Métricas de Salud Pública
- **Medidas de Frecuencia**: Incidencia, prevalencia, tasas de mortalidad
- **Medidas de Asociación**: OR, RR, HR, IRR con intervalos de confianza
- **Medidas de Impacto**: Riesgo atribuible, PAR%, fracción prevenible
- **Pruebas de Hipótesis**: Chi-cuadrado, log-rank, pruebas de proporcionalidad
- **Modelado GLM**: Familia Poisson y Binomial para datos de conteo

### Gestión de Datos Epidemiológicos
- Soporte para múltiples archivos simultáneos
- Formatos: CSV, Excel (.xlsx, .xls), JSON, Parquet
- Manejo de datos censurados y tiempo-hasta-evento
- Identificación automática de covariables y estratos

### Limpieza de Datos Biomédicos
- Imputación inteligente para datos clínicos
- Detección de outliers biológicamente implausibles (IQR, Z-score)
- Transformación de variables epidemiológicas
- Codificación de variables categóricas diagnósticas

### ML para Epidemiología
- **Clasificación**: Predicción de riesgo, diagnóstico, outcomes binarios
- **Regresión**: Modelado de variables continuas de salud
- **Algoritmos**: Logistic, Random Forest, SVM, XGBoost
- Validación cruzada y métricas clínicas (sensibilidad, especificidad, AUC)

### Reportes Epidemiológicos
- Reportes PDF con estadísticas de salud pública
- Tablas de resultados con medidas de asociación
- Visualizaciones epidemiológicas integradas
- Interpretación clínica y significancia estadística

### Chatbot Epidemiológico IA
- Consultas especializadas en análisis epidemiológico
- Interpretación de resultados bioestadísticos
- Recomendaciones de métodos según diseño de estudio
- Powered by Groq (llama-3.1-8b-instant) con prompts PhD-level

---

## Inicio Rápido

### 1. Requisitos Previos

**API Key de Groq (GRATIS):**
- Regístrate en [console.groq.com](https://console.groq.com)
- Genera tu API key gratuita
- Tier gratuito: ~14,000 tokens/minuto (más que suficiente)

### 2. Instalación Local

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd ai-ds-agent

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key (opción 1: .env)
cp .env.example .env
# Editar .env y agregar tu GROQ_API_KEY

# O configurar API key (opción 2: Streamlit secrets)
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Editar secrets.toml y agregar tu GROQ_API_KEY
```

### 3. Ejecutar Localmente

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### 4. Desplegar en Hugging Face Spaces

1. **Fork o crea un nuevo Space** en [huggingface.co/spaces](https://huggingface.co/spaces)
2. **Configura el secret de la API:**
   - Ve a Settings ⚙️ de tu Space
   - Scroll a "Repository secrets"
   - Click "New secret"
   - Name: `GROQ_API_KEY`
   - Value: Tu API key de Groq
   - Click "Add secret"
3. **Push tu código** al Space
4. **Espera 2-3 minutos** para que se construya

> **Guía detallada**: Ver [HF_SECRETS_SETUP.md](./HF_SECRETS_SETUP.md) para troubleshooting

---

## Requisitos

- **Python:** 3.8+
- **Groq API:** Cuenta gratuita en [console.groq.com](https://console.groq.com)
- **Hugging Face Spaces:** Hosting gratuito (opcional)

---

## Tecnologías

### Core
- **Streamlit** - Framework de aplicaciones
- **Pandas & NumPy** - Manipulación de datos
- **Scikit-learn** - Machine Learning
- **XGBoost** - Gradient Boosting avanzado

### Visualización
- **Plotly** - Gráficos interactivos
- **Matplotlib & Seaborn** - Visualizaciones estáticas
- **ReportLab** - Generación de PDFs

### IA
- **LangChain** - Framework de IA
- **Groq** - LLM ultra-rápido (llama-3.1-8b-instant)

---

## Uso

### Paso 1: Cargar Datos
- Sube uno o múltiples archivos (CSV, Excel, JSON, Parquet)
- Revisa el esquema y estadísticas
- Selecciona el dataset activo

### Paso 2: Limpiar Datos
- Elimina duplicados y valores nulos
- Imputa valores faltantes (media, mediana, moda)
- Detecta y maneja outliers
- Transforma tipos de datos

### Paso 3: Visualizar
- Explora distribuciones de variables
- Analiza correlaciones
- Crea visualizaciones interactivas
- Genera gráficos 3D y avanzados

### Paso 4: Modelar
- Selecciona la variable objetivo
- Elige características y algoritmos
- Entrena múltiples modelos automáticamente
- Compara métricas y visualiza resultados

### Paso 5: Generar Reporte
- Descarga reporte PDF con todos los análisis
- Incluye estadísticas, visualizaciones y modelos

### Chatbot
- Abre el sidebar (>>) en cualquier momento
- Haz preguntas sobre tus datos en lenguaje natural
- Obtén insights y recomendaciones

---

## Docker

```bash
docker build -t ai-ds-agent .
docker run -p 8501:8501 ai-ds-agent
```

---

## Características Destacadas

### Mejoras Implementadas

1. **Multi-Archivo**: Carga y gestiona múltiples datasets simultáneamente
2. **Más Formatos**: Soporte para Excel, JSON y Parquet además de CSV
3. **Limpieza Avanzada**: Detección de outliers, imputación inteligente
4. **Visualizaciones Interactivas**: Plotly para exploración dinámica
5. **Más Algoritmos ML**: 8+ algoritmos con validación cruzada
6. **Optimización**: GridSearch para hiperparámetros
7. **Mejor Chatbot**: Validación de API key y manejo de errores robusto
8. **Documentación Completa**: Instrucciones detalladas y ejemplos

---

## Costos

- **Groq API:** GRATUITO (hasta 14K tokens/min)
- **Hugging Face Spaces:** GRATUITO (CPU hosting)
- **Código:** Open Source (MIT License)

**Total: $0 USD/mes**

---

## Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

MIT License - ver archivo [LICENSE](LICENSE)

---

## Agradecimientos

- [Groq](https://groq.com) por su API ultra-rápida y gratuita
- [Hugging Face](https://huggingface.co) por hosting gratuito
- [Streamlit](https://streamlit.io) por el framework increíble

---

## Contacto

¿Preguntas o sugerencias? Abre un issue en GitHub.

---

**¡Construido para democratizar la ciencia de datos!**  
