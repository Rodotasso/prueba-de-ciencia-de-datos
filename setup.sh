#!/bin/bash

# Quick Deploy Script for AI Data Scientist Agent

echo "🚀 AI Data Scientist Agent - Quick Deploy Setup"
echo "================================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✅ .env created! Please edit it and add your GROQ_API_KEY"
    echo "   Get your free API key at: https://console.groq.com"
    echo ""
else
    echo "✅ .env file found"
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository exists"
fi

# Check Python
echo ""
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✅ $PYTHON_VERSION"
    PYTHON_CMD=python
else
    echo "❌ Python not found! Please install Python 3.8+"
    exit 1
fi

# Check if venv exists
echo ""
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate venv and install requirements
echo ""
echo "📥 Installing dependencies..."
echo "   (This may take a few minutes)"

source venv/bin/activate
pip install -r requirements.txt --quiet

echo "✅ Dependencies installed"

# Summary
echo ""
echo "================================================="
echo "✨ Setup Complete!"
echo "================================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. 🔑 Configure your API key:"
echo "   - Edit .env file"
echo "   - Add: GROQ_API_KEY=your_key_here"
echo "   - Get free key at: https://console.groq.com"
echo ""
echo "2. 🚀 Run locally:"
echo "   source venv/bin/activate  # Activate venv first"
echo "   streamlit run app.py"
echo ""
echo "3. 🌐 Deploy to Hugging Face:"
echo "   - Read: DEPLOY_GUIDE.md"
echo "   - Create Space at: https://huggingface.co/new-space"
echo "   - Use SDK: Streamlit"
echo "   - Add GROQ_API_KEY in Repository secrets"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Overview and features"
echo "   - INSTALLATION.md - Detailed installation guide"
echo "   - DEPLOY_GUIDE.md - Hugging Face deployment"
echo ""
echo "💡 Tip: Test locally first before deploying!"
echo ""
