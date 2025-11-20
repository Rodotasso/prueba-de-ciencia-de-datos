# Quick Deploy Script for AI Data Scientist Agent

Write-Host "🚀 AI Data Scientist Agent - Quick Deploy Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "📝 Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env created! Please edit it and add your GROQ_API_KEY" -ForegroundColor Green
    Write-Host "   Get your free API key at: https://console.groq.com" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "✅ .env file found" -ForegroundColor Green
}

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository exists" -ForegroundColor Green
}

# Check Python
Write-Host ""
Write-Host "🐍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if venv exists
Write-Host ""
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
}

# Activate venv and install requirements
Write-Host ""
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
Write-Host "   (This may take a few minutes)" -ForegroundColor Cyan

.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --quiet

Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 🔑 Configure your API key:" -ForegroundColor White
Write-Host "   - Edit .env file" -ForegroundColor Gray
Write-Host "   - Add: GROQ_API_KEY=your_key_here" -ForegroundColor Gray
Write-Host "   - Get free key at: https://console.groq.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 🚀 Run locally:" -ForegroundColor White
Write-Host "   streamlit run app.py" -ForegroundColor Green
Write-Host ""
Write-Host "3. 🌐 Deploy to Hugging Face:" -ForegroundColor White
Write-Host "   - Read: DEPLOY_GUIDE.md" -ForegroundColor Gray
Write-Host "   - Create Space at: https://huggingface.co/new-space" -ForegroundColor Cyan
Write-Host "   - Use SDK: Streamlit" -ForegroundColor Gray
Write-Host "   - Add GROQ_API_KEY in Repository secrets" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - README.md - Overview and features" -ForegroundColor Gray
Write-Host "   - INSTALLATION.md - Detailed installation guide" -ForegroundColor Gray
Write-Host "   - DEPLOY_GUIDE.md - Hugging Face deployment" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tip: Test locally first before deploying!" -ForegroundColor Cyan
Write-Host ""
