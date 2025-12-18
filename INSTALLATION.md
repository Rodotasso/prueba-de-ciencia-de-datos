# Guía de Instalación y Uso - AI Data Scientist Agent

## Requisitos Previos

### 1. Software Necesario
- **Python 3.8 o superior** - [Descargar aquí](https://www.python.org/downloads/)
- **Git** (opcional) - Para clonar el repositorio

### 2. API Key de Groq (GRATIS)
El chatbot de IA requiere una API key de Groq. Es **completamente gratuita** con límites generosos.

**Cómo obtener tu API key:**
1. Visita [console.groq.com](https://console.groq.com)
2. Crea una cuenta gratuita
3. Ve a "API Keys" en el menú
4. Click en "Create API Key"
5. Copia tu key (empieza con `gsk_...`)

**Plan Gratuito incluye:**
- ~14,000 tokens por minuto
- Acceso al modelo llama-3.1-8b-instant
- Respuestas ultra-rápidas (milisegundos)
- Sin límite de tiempo
- Sin tarjeta de crédito requerida

---

## Instalación

### Opción 1: Instalación Local

#### Paso 1: Descargar el proyecto
```bash
# Con Git
git clone <url-del-repositorio>
cd ai-ds-agent

# O descarga el ZIP desde GitHub y descomprime
```

#### Paso 2: Crear entorno virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar API Key
```bash
# Copiar archivo de ejemplo
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Editar .env con tu editor favorito y agregar tu API key
# GROQ_API_KEY=tu_api_key_aquí
```

#### Paso 5: Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

### Opción 2: Docker

#### Paso 1: Construir la imagen
```bash
docker build -t ai-ds-agent .
```

#### Paso 2: Ejecutar el contenedor
```bash
docker run -p 8501:8501 -e GROQ_API_KEY=tu_api_key_aquí ai-ds-agent
```

Accede a `http://localhost:8501`

---

## Cómo Usar la Aplicación

### Flujo Completo de Trabajo

#### 1. Cargar Datos
- Click en la pestaña "Upload & Schema"
- Arrastra o selecciona tus archivos
- Formatos soportados: CSV, Excel, JSON, Parquet
- Puedes cargar múltiples archivos a la vez

**Tip:** Si tienes varios datasets, selecciona cuál será el activo para análisis.

#### 2. Limpiar Datos
- Navega a "Clean Data"
- Opciones disponibles:
  - **Remove Data:** Eliminar duplicados, filas vacías, columnas
  - **Handle Missing:** Imputar valores con media, mediana, moda, interpolación
  - **Outliers:** Detectar y manejar valores atípicos (IQR o Z-score)
  - **Transform:** Cambiar tipos de datos, estandarizar nombres

**Importante:** Click en "Save Cleaned Dataset" para aplicar cambios.

#### 3. Visualizar
- Ir a "Data Visualization"
- 5 categorías de visualizaciones:
  - **Distribution:** Histogramas, box plots, violin plots
  - **Relationships:** Scatter plots, líneas de tendencia, correlaciones
  - **Comparisons:** Gráficos de barras, box plots por categoría
  - **Heatmaps:** Matrices de correlación
  - **Advanced:** Pair plots, gráficos 3D, coordenadas paralelas

**Tip:** Todos los gráficos son interactivos - haz zoom, pan, exporta imágenes.

#### 4. Entrenar Modelos
- Accede a "Modeling and Evaluation"
- Configuración:
  1. Selecciona la columna objetivo (target)
  2. Elige las características (features)
  3. Ajusta el tamaño del test set (20% por defecto)
  4. Selecciona algoritmos a entrenar

**Algoritmos disponibles:**
- **Clasificación:** Logistic Regression, Random Forest, SVM, KNN, XGBoost, Decision Tree, Gradient Boosting
- **Regresión:** Linear, Ridge, Lasso, Random Forest, SVM, KNN, XGBoost, Gradient Boosting

**Opciones avanzadas:**
- Estandarización de características
- Validación cruzada (3-10 folds)
- Optimización de hiperparámetros (GridSearch)

**Resultados mostrados:**
- Tabla comparativa de métricas
- Mejor modelo automático
- Matriz de confusión (clasificación)
- Gráfico actual vs predicho (regresión)
- Comparación visual entre modelos

#### 5. Generar Reportes
- Ve a "Report"
- Configura:
  - Título del reporte
  - Nombre del autor
  - Secciones a incluir
- Genera:
  - **PDF:** Reporte profesional para imprimir/presentar
  - **HTML:** Reporte interactivo para navegador

**Incluye:**
- Overview del dataset
- Estadísticas descriptivas
- Análisis de correlación
- Visualizaciones clave
- Resultados de modelos

#### 6. Usar el Chatbot
- Abre el sidebar (>> arriba a la izquierda)
- Haz preguntas sobre tus datos en lenguaje natural
- Ejemplos:
  - "¿Cuál es la correlación más fuerte?"
  - "¿Qué columna tiene más valores nulos?"
  - "Dame un resumen de las variables numéricas"
  - "¿Cómo puedo mejorar mi modelo?"

---

## Ejemplos de Uso

### Ejemplo 1: Análisis de Ventas
1. Cargar `sales_data.csv`
2. Limpiar: Eliminar duplicados, imputar fechas faltantes
3. Visualizar: Gráfico de ventas por mes, correlación precio-cantidad
4. Modelar: Predecir ventas futuras (regresión)
5. Reporte: PDF con insights para presentación

### Ejemplo 2: Clasificación de Clientes
1. Cargar `customer_data.xlsx`
2. Limpiar: Detectar outliers en edad, estandarizar nombres
3. Visualizar: Distribución por categoría, pair plot
4. Modelar: Clasificar tipo de cliente (Random Forest)
5. Chatbot: "¿Qué características son más importantes?"

### Ejemplo 3: Múltiples Datasets
1. Cargar `train.csv` y `test.csv`
2. Limpiar ambos con mismas operaciones
3. Entrenar con train, evaluar con test
4. Comparar distribuciones entre datasets

---

## Solución de Problemas

### Error: "GROQ_API_KEY not found"
- **Solución:** Verifica que el archivo `.env` existe y contiene tu API key
- Formato correcto: `GROQ_API_KEY=gsk_tu_key_aquí`
- Sin espacios ni comillas

### Error al cargar archivo
- **CSV:** Prueba diferentes encodings (UTF-8, Latin-1)
- **Excel:** Verifica que no esté corrupto
- **JSON:** Debe ser lista de objetos o diccionario válido

### Modelo no entrena
- Verifica que hay datos suficientes (mínimo 50 filas)
- Asegúrate que la columna objetivo no tiene valores nulos
- Revisa que hay características numéricas o categóricas válidas

### App lenta
- Reduce el número de filas/columnas para pruebas
- Desactiva validación cruzada
- No uses optimización de hiperparámetros en datasets grandes

### Error de memoria
- Reduce el tamaño del dataset
- Selecciona menos características
- Limita el número de modelos a entrenar simultáneamente

---

## Límites y Consideraciones

### Tamaño de Datos
- **Recomendado:** < 100MB por archivo
- **Máximo práctico:** ~200MB
- Para datos más grandes, considera filtrar o muestrear

### Performance
- **Carga:** Instantánea para archivos < 10MB
- **Limpieza:** < 1 minuto para 100K filas
- **Visualización:** Interactiva para < 50K puntos
- **Modelado:** 2-5 minutos para 100K filas con CV

### Chatbot
- **Rate limit:** ~14,000 tokens/minuto (plan gratis)
- Si alcanzas el límite, espera 1 minuto
- Respuestas típicas: < 2 segundos

---

## Seguridad

### Datos
- Todo se procesa localmente
- Nada se guarda en servidores
- Session state de Streamlit (temporal)
- No se suben datos a la nube

### API Key
- Nunca compartas tu GROQ_API_KEY
- No la subas a GitHub
- Usa `.env` (está en .gitignore)
- Regenera si se compromete

---

## Soporte

### Recursos
- **Documentación:** Este README
- **Bugs:** Abre un issue en GitHub
- **Sugerencias:** Pull requests bienvenidos
- **Preguntas:** Usa el chatbot o issues

### Comunidad
- Dale star al repo si te gusta
- Fork para tus propios proyectos
- Comparte tus casos de uso

---

## Próximos Pasos

Una vez familiarizado con la app:
1. **Experimenta** con diferentes datasets
2. **Compara** algoritmos en tus datos
3. **Personaliza** umbrales y parámetros
4. **Automatiza** tu pipeline de análisis
5. **Comparte** reportes con tu equipo

---

¡Disfruta explorando tus datos con IA!
