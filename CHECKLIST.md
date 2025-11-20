# 🎯 Checklist Pre-Deploy - Hugging Face Spaces

Use esta checklist antes de hacer deploy para asegurar que todo funcione correctamente.

## ✅ Archivos Esenciales

- [x] `app.py` - Archivo principal de entrada
- [x] `requirements.txt` - Todas las dependencias listadas
- [x] `README.md` - Con metadata en el header
- [x] `chatbot.py` - Módulo del chatbot
- [x] `pages/` - Carpeta con todas las páginas (5 archivos .py)
- [x] `.gitignore` - Configurado para no subir .env
- [x] `.env.example` - Plantilla sin la API key real
- [x] `LICENSE` - Archivo de licencia MIT
- [x] `.streamlit/config.toml` - Configuración de Streamlit

## ✅ Metadata en README.md

Verifica que el README.md tenga este header al inicio:

```yaml
---
title: AI Data Scientist Agent
emoji: 📊
sdk: streamlit
app_file: app.py
pinned: false
license: mit
sdk_version: 1.49.1
---
```

## ✅ Configuración de Seguridad

- [ ] Archivo `.env` **NO** está en el repositorio (debe estar en .gitignore)
- [ ] API key de Groq obtenida de https://console.groq.com
- [ ] `.env.example` tiene el formato correcto pero sin la key real
- [ ] No hay API keys hardcodeadas en ningún archivo .py

## ✅ Dependencias

Verifica que `requirements.txt` incluya:

- [x] streamlit
- [x] pandas
- [x] numpy
- [x] scipy
- [x] plotly
- [x] matplotlib
- [x] seaborn
- [x] scikit-learn
- [x] xgboost
- [x] langchain
- [x] langchain-groq
- [x] python-dotenv
- [x] reportlab
- [x] openpyxl
- [x] pyarrow

## ✅ Estructura de Páginas

Verifica que `pages/` contenga:

- [x] `01_📂_Upload_and_Schema.py`
- [x] `02_🧹_Clean_Data.py`
- [x] `03_📊_Data_Visualization.py`
- [x] `04_🤖_Modeling_and_Evaluation.py`
- [x] `05_📑_Report.py`

## ✅ Pruebas Locales

Antes de deployar, verifica localmente:

- [ ] `streamlit run app.py` funciona sin errores
- [ ] Puedes cargar archivos CSV y Excel
- [ ] La limpieza de datos funciona
- [ ] Las visualizaciones se renderizan correctamente
- [ ] El modelado entrena sin errores
- [ ] Los reportes se generan (PDF y HTML)
- [ ] El chatbot responde (con API key configurada)

## ✅ Hugging Face Space

Configuración en Hugging Face:

- [ ] Space creado con SDK: Streamlit
- [ ] Hardware: CPU basic (gratis) seleccionado
- [ ] Repository secret `GROQ_API_KEY` agregado
- [ ] Código pusheado al Space (vía GitHub o directo)

## ✅ Comandos Git

Si usas GitHub para sincronización:

```bash
# Verificar estado
git status

# Agregar cambios
git add .

# Commit
git commit -m "Ready for Hugging Face deployment"

# Push a GitHub
git push origin main

# (Opcional) Push directo a HF Space
git push space main
```

## ✅ Post-Deploy

Después del primer deploy:

- [ ] Build completado sin errores en Hugging Face
- [ ] App carga correctamente en la URL del Space
- [ ] Puedes subir un archivo de prueba
- [ ] El chatbot funciona con la API key
- [ ] No hay errores en los logs

## 🚨 Problemas Comunes

### Build falla con "Application error"
✅ **Solución:** Verifica que GROQ_API_KEY esté en Repository secrets

### "Module not found" error
✅ **Solución:** Agrega la dependencia faltante a requirements.txt

### Chatbot no responde
✅ **Solución:** Verifica que GROQ_API_KEY esté correctamente configurado

### App muy lenta
✅ **Solución:** Normal en CPU básico, considera archivos < 50MB para mejor performance

## 📊 Métricas de Éxito

Tu deploy es exitoso cuando:

- ✅ Build time: < 5 minutos
- ✅ App carga: < 3 segundos
- ✅ Upload archivos: < 5 segundos para 10MB
- ✅ Chatbot responde: < 2 segundos
- ✅ Zero errores en logs

## 🎯 URLs Importantes

- **Hugging Face Spaces:** https://huggingface.co/spaces
- **Tu Space:** https://huggingface.co/spaces/[usuario]/[space-name]
- **Groq Console:** https://console.groq.com
- **Documentación HF:** https://huggingface.co/docs/hub/spaces

---

## ✨ Ready to Deploy!

Una vez completada esta checklist, tu aplicación está lista para:

1. 🚀 Deploy en Hugging Face Spaces
2. 🌐 Compartir con URL pública
3. 👥 Recibir usuarios y feedback
4. 🔄 Actualizar continuamente vía GitHub

**¡Buena suerte con tu deploy!** 🎉
