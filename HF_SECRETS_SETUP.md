# Configuración de API Key en Hugging Face Spaces

## Problema Actual
La API key de Groq no se reconoce en HF Spaces porque el archivo `.env` no se lee automáticamente.

## Solución: Usar Repository Secrets de Hugging Face

### Pasos para configurar:

1. **Ve a tu Space en Hugging Face**
   - URL: https://huggingface.co/spaces/Tassdreams/Data_Science_

2. **Accede a Settings**
   - Click en la pestaña "Settings"

3. **Agrega Repository Secrets**
   - Scroll down hasta la sección **"Repository secrets"**
   - Click en **"New secret"**
   
4. **Configura el secret:**
   ```
   Name: GROQ_API_KEY
   Value: [tu_api_key_de_groq_aquí]
   ```
   
5. **Guarda y espera**
   - Click "Add secret"
   - El Space se reconstruirá automáticamente (2-3 minutos)

## Obtener API Key de Groq

Si no tienes una API key:
1. Ve a: https://console.groq.com/keys
2. Crea una cuenta gratuita
3. Genera una nueva API key
4. Copia la key (empieza con `gsk_...`)

## Verificar que funciona

Después de agregar el secret:
1. Espera a que el Space termine de reconstruirse
2. Abre el chatbot en la barra lateral
3. Si la API key está correctamente configurada, NO verás el mensaje de error "⚠️ GROQ_API_KEY not found!"

## Troubleshooting

### El error persiste después de agregar el secret:
- Verifica que el nombre sea exactamente `GROQ_API_KEY` (mayúsculas)
- Asegúrate de que la API key sea válida
- Revisa los logs del Space en la pestaña "Logs"
- Fuerza un rebuild: Settings > Factory reboot

### Para desarrollo local:
Crea un archivo `.streamlit/secrets.toml` con:
```toml
GROQ_API_KEY = "tu_api_key_aquí"
```

## 📚 Más información
- [Hugging Face Spaces Secrets](https://huggingface.co/docs/hub/spaces-overview#managing-secrets)
- [Groq API Documentation](https://console.groq.com/docs)
