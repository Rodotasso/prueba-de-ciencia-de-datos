# 🚀 Deploy en Hugging Face Spaces

Esta guía te ayudará a deployar tu aplicación en Hugging Face Spaces en minutos.

## ✅ Pre-requisitos

1. Cuenta en [Hugging Face](https://huggingface.co) (gratis)
2. Cuenta en [Groq](https://console.groq.com) con API key (gratis)
3. (Opcional) Cuenta en GitHub para sincronización automática

---

## 📝 Método 1: Sincronización con GitHub (Recomendado)

### Paso 1: Subir a GitHub

```bash
# Inicializar repositorio (si no lo has hecho)
git init

# Agregar archivos
git add .
git commit -m "Initial commit - AI Data Scientist Agent"

# Crear repositorio en github.com y luego:
git remote add origin https://github.com/tu-usuario/ai-ds-agent.git
git branch -M main
git push -u origin main
```

### Paso 2: Crear Space en Hugging Face

1. Ve a https://huggingface.co/new-space
2. Configura:
   - **Owner:** Tu usuario
   - **Space name:** `ai-ds-agent` (o el que prefieras)
   - **License:** MIT
   - **Select the Space SDK:** Streamlit ⭐
   - **Space hardware:** CPU basic - Free! ✅
   - **Repo type:** Public (o Private si prefieres)

3. Click **"Create Space"**

### Paso 3: Conectar GitHub con Hugging Face

1. En tu Space, ve a **Settings**
2. Busca **"GitHub"** section
3. Click **"Link to GitHub"**
4. Autoriza Hugging Face
5. Selecciona tu repositorio `ai-ds-agent`
6. ✅ Listo! Ahora cada push a GitHub actualizará tu Space automáticamente

### Paso 4: Configurar API Key (IMPORTANTE)

**⚠️ NUNCA subas tu API key al código público**

1. En tu Space, ve a **Settings**
2. Scroll hasta **"Repository secrets"**
3. Click **"New secret"**
4. Agrega:
   - **Name:** `GROQ_API_KEY`
   - **Value:** Tu API key de Groq (empieza con `gsk_...`)
5. Click **"Add"**

### Paso 5: Esperar el Build

- Hugging Face detectará automáticamente `requirements.txt`
- Instalará todas las dependencias
- Proceso tarda 3-5 minutos
- Verás logs en tiempo real

### Paso 6: ¡Listo!

Tu app estará disponible en:
```
https://huggingface.co/spaces/tu-usuario/ai-ds-agent
```

---

## 📝 Método 2: Subida Directa (Sin GitHub)

### Paso 1: Crear Space

Igual que el método 1, crea el Space en Hugging Face.

### Paso 2: Clonar el Space localmente

```bash
# Instalar git-lfs si no lo tienes
git lfs install

# Clonar tu Space
git clone https://huggingface.co/spaces/tu-usuario/ai-ds-agent
cd ai-ds-agent

# Copiar tus archivos aquí
# (copia todo excepto .git, .env, venv)

# Commit y push
git add .
git commit -m "Initial deployment"
git push
```

### Paso 3: Configurar API Key

Igual que el método 1, agrega `GROQ_API_KEY` en Repository secrets.

---

## 🔧 Verificación Pre-Deploy

Antes de hacer deploy, verifica que tu repositorio tenga:

### ✅ Archivos Requeridos:
- [x] `app.py` - Archivo principal
- [x] `requirements.txt` - Dependencias
- [x] `README.md` - Con metadata correcto
- [x] `chatbot.py` - Módulo del chatbot
- [x] `pages/` - Carpeta con todas las páginas
- [x] `.gitignore` - Para no subir archivos innecesarios
- [x] `.env.example` - Plantilla (NO subir .env real)

### ✅ Metadata en README.md:
El README.md debe tener este header (ya lo tienes):
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

### ✅ requirements.txt actualizado:
Verifica que incluya todas las dependencias (ya está completo).

---

## 🚨 Problemas Comunes y Soluciones

### Error: "Application error"
**Causa:** Falta GROQ_API_KEY
**Solución:** Agregar en Repository secrets

### Error: "Module not found"
**Causa:** Falta dependencia en requirements.txt
**Solución:** Verificar y actualizar requirements.txt

### App muy lenta
**Causa:** CPU básico es limitado
**Solución:** 
- Usa tier gratis (suficiente)
- O upgrade a CPU upgrade ($9/mes) si necesitas más velocidad

### Error al cargar archivos grandes
**Causa:** Límite de memoria en CPU básico
**Solución:** 
- Archivos < 100MB funcionan bien
- Para archivos más grandes, usa local o upgrade hardware

---

## 🔄 Actualización Continua

### Con GitHub conectado:
```bash
# Haces cambios locales
git add .
git commit -m "Nueva característica"
git push

# Automáticamente se actualiza en Hugging Face! 🎉
```

### Sin GitHub:
```bash
# Haces cambios locales en el directorio del Space clonado
git add .
git commit -m "Nueva característica"
git push
```

---

## 🌐 Compartir tu App

Una vez deployada, comparte:
```
https://huggingface.co/spaces/tu-usuario/ai-ds-agent
```

### Opciones:
- **Public:** Cualquiera puede acceder
- **Private:** Solo tú y colaboradores invitados
- **Embed:** Puedes embeber en tu sitio web

---

## 📊 Monitoreo

En tu Space dashboard puedes ver:
- ✅ Usuarios activos
- ✅ Logs en tiempo real
- ✅ Uso de recursos
- ✅ Historial de builds

---

## 💡 Tips

1. **Desarrollo local primero:** Prueba todo localmente antes de deployar
2. **Commits descriptivos:** Facilita debug si algo falla
3. **Secrets seguros:** Nunca pongas API keys en el código
4. **README atractivo:** Agrega screenshots y ejemplos
5. **Tags:** Usa tags en Hugging Face para que te encuentren

---

## 🎯 Checklist Final

Antes de deployar, verifica:

- [ ] App funciona correctamente local
- [ ] requirements.txt completo
- [ ] README.md con metadata correcto
- [ ] .gitignore configurado (no subir .env)
- [ ] API key de Groq lista
- [ ] Space creado en Hugging Face
- [ ] Repository secrets configurado
- [ ] Primera versión pusheada

---

## 🆘 Ayuda

Si tienes problemas:

1. **Logs de build:** Revisa en tu Space > Logs
2. **Hugging Face Docs:** https://huggingface.co/docs/hub/spaces
3. **Streamlit Docs:** https://docs.streamlit.io/
4. **Community:** https://discuss.huggingface.co/

---

## ✨ Próximos Pasos

Después del primer deploy:

1. Agrega screenshots al README
2. Crea un demo video
3. Comparte en redes sociales
4. Pide feedback a usuarios
5. Itera y mejora

---

¡Buena suerte con tu deploy! 🚀

**Recuerda:** Todo es GRATIS (Groq API + Hugging Face Spaces CPU básico) 💰✅
