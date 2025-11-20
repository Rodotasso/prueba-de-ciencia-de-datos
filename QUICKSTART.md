# 🚀 Quick Start - AI Data Scientist Agent

## ⚡ 3 Pasos para Empezar

### 1️⃣ Instalar (2 minutos)

**Windows:**
```powershell
.\setup.ps1
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### 2️⃣ Configurar API Key (1 minuto)

1. Ve a: https://console.groq.com
2. Registrate (gratis)
3. Crea una API key
4. Edita `.env` y pega tu key:
   ```
   GROQ_API_KEY=gsk_tu_key_aqui
   ```

### 3️⃣ Ejecutar (30 segundos)

```bash
streamlit run app.py
```

¡Listo! Tu app abrirá en http://localhost:8501

---

## 🌐 Deploy en Hugging Face (5 minutos)

### Opción A: Con GitHub (Recomendado)

```bash
# 1. Push a GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Crear Space en https://huggingface.co/new-space
# - SDK: Streamlit
# - Conectar con GitHub

# 3. Agregar API key en Settings > Repository secrets
# - Name: GROQ_API_KEY
# - Value: tu_key
```

### Opción B: Sin GitHub

```bash
# 1. Crear Space en https://huggingface.co/new-space
# - SDK: Streamlit

# 2. Clonar y push
git clone https://huggingface.co/spaces/tu-usuario/tu-space
cd tu-space
# Copiar todos tus archivos aquí
git add .
git commit -m "Initial deploy"
git push

# 3. Agregar API key en Settings > Repository secrets
```

---

## 📚 Documentación Completa

- **README.md** - Descripción completa y features
- **INSTALLATION.md** - Guía detallada de instalación
- **DEPLOY_GUIDE.md** - Deploy paso a paso en HF
- **CHECKLIST.md** - Verificación pre-deploy
- **MEJORAS_IMPLEMENTADAS.md** - Resumen de mejoras

---

## 🎯 Características Principales

✅ **Multi-formato:** CSV, Excel, JSON, Parquet  
✅ **Limpieza avanzada:** Outliers, imputación, transformaciones  
✅ **Visualizaciones:** 15+ gráficos interactivos con Plotly  
✅ **15 Algoritmos ML:** XGBoost, Random Forest, SVM, etc.  
✅ **Validación cruzada** y optimización de hiperparámetros  
✅ **Reportes PDF/HTML** profesionales  
✅ **Chatbot IA** con Groq (gratis)  

---

## 💰 Costos

**Total: $0/mes** 🎉

- Groq API: Gratis (14K tokens/min)
- Hugging Face Spaces: Gratis (CPU básico)

---

## 🆘 Ayuda Rápida

**Error: "GROQ_API_KEY not found"**  
→ Edita `.env` y agrega tu API key

**Error al cargar archivos**  
→ Verifica formato (CSV, Excel, JSON, Parquet)

**App lenta**  
→ Normal con archivos grandes, reduce tamaño < 50MB

**Más ayuda:**  
→ Ver INSTALLATION.md para troubleshooting completo

---

## 📞 Soporte

- 📖 Docs completas en archivos .md
- 🐛 Issues: GitHub Issues
- 💬 Community: Hugging Face Discussions

---

**¡Disfruta analizando tus datos con IA!** 🎉📊
