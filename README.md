---
title: AI Data Scientist Agent
emoji: 📊
sdk: streamlit
app_file: app.py
pinned: false
license: mit
sdk_version: 1.49.1
---

# 🤖 AI Data Scientist Agent

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-lg.svg)](https://huggingface.co/spaces/Sanchay3011/ai-ds-agent)

Un **Agente de Ciencia de Datos potenciado por IA** que automatiza todo el flujo de trabajo de análisis de datos:

## ✨ Características Principales

### 📂 **Carga Multi-Formato**
- ✅ Soporte para múltiples archivos simultáneos
- ✅ Formatos: CSV, Excel (.xlsx, .xls), JSON, Parquet
- ✅ Manejo automático de codificación
- ✅ Selector de datasets activos

### 🧹 **Limpieza Avanzada de Datos**
- ✅ Eliminación de duplicados y valores nulos
- ✅ Imputación inteligente (media, mediana, moda, interpolación)
- ✅ Detección automática de outliers (IQR y Z-score)
- ✅ Transformación de tipos de datos
- ✅ Estandarización de nombres de columnas

### 📊 **Visualización Interactiva**
- ✅ Gráficos interactivos con Plotly
- ✅ Histogramas, box plots, violin plots
- ✅ Scatter plots con líneas de tendencia
- ✅ Mapas de calor de correlación
- ✅ Gráficos 3D y coordenadas paralelas
- ✅ Pair plots y sunburst charts

### 🤖 **Modelado ML Avanzado**
- ✅ **Clasificación:** Logistic Regression, Random Forest, SVM, KNN, XGBoost
- ✅ **Regresión:** Linear, Ridge, Lasso, Random Forest, Gradient Boosting
- ✅ Validación cruzada automática
- ✅ Optimización de hiperparámetros (GridSearch)
- ✅ Estandarización de características
- ✅ Métricas completas y comparación de modelos

### 📑 **Reportes Automatizados**
- ✅ Generación de reportes PDF profesionales
- ✅ Estadísticas descriptivas
- ✅ Visualizaciones incluidas
- ✅ Resumen del mejor modelo

### 💬 **Chatbot IA**
- ✅ Consultas en lenguaje natural sobre tus datos
- ✅ Powered by Groq (llama-3.1-8b-instant)
- ✅ Análisis y respuestas contextuales

---

## 🚀 Inicio Rápido

### 1️⃣ Requisitos Previos

**API Key de Groq (GRATIS):**
- Regístrate en [console.groq.com](https://console.groq.com)
- Genera tu API key gratuita
- Tier gratuito: ~14,000 tokens/minuto (más que suficiente)

### 2️⃣ Instalación

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd ai-ds-agent

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Editar .env y agregar tu GROQ_API_KEY
```

### 3️⃣ Ejecutar

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

---

## 📦 Requisitos

- **Python:** 3.8+
- **Groq API:** Cuenta gratuita en [console.groq.com](https://console.groq.com)
- **Hugging Face Spaces:** Hosting gratuito (opcional)

---

## 🛠️ Tecnologías

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

## 📖 Uso

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

### 💬 Chatbot
- Abre el sidebar (>>) en cualquier momento
- Haz preguntas sobre tus datos en lenguaje natural
- Obtén insights y recomendaciones

---

## 🐳 Docker

```bash
docker build -t ai-ds-agent .
docker run -p 8501:8501 ai-ds-agent
```

---

## 🌟 Características Destacadas

### 🆕 Mejoras Implementadas

1. **Multi-Archivo**: Carga y gestiona múltiples datasets simultáneamente
2. **Más Formatos**: Soporte para Excel, JSON y Parquet además de CSV
3. **Limpieza Avanzada**: Detección de outliers, imputación inteligente
4. **Visualizaciones Interactivas**: Plotly para exploración dinámica
5. **Más Algoritmos ML**: 8+ algoritmos con validación cruzada
6. **Optimización**: GridSearch para hiperparámetros
7. **Mejor Chatbot**: Validación de API key y manejo de errores robusto
8. **Documentación Completa**: Instrucciones detalladas y ejemplos

---

## 💰 Costos

- ✅ **Groq API:** GRATUITO (hasta 14K tokens/min)
- ✅ **Hugging Face Spaces:** GRATUITO (CPU hosting)
- ✅ **Código:** Open Source (MIT License)

**Total: $0 USD/mes** 🎉

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

---

## 🙏 Agradecimientos

- [Groq](https://groq.com) por su API ultra-rápida y gratuita
- [Hugging Face](https://huggingface.co) por hosting gratuito
- [Streamlit](https://streamlit.io) por el framework increíble

---

## 📧 Contacto

¿Preguntas o sugerencias? Abre un issue en GitHub.

---

**¡Construido con ❤️ para democratizar la ciencia de datos!**  
