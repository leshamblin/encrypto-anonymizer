#!/bin/bash

# Setup script for encrypto-anonymizer with UV

echo "🔐 Setting up Encrypto-Anonymizer..."

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Create virtual environment and install dependencies
echo "Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate
uv pip install -e .

# Install Jupyter kernel
echo "Installing Jupyter kernel..."
python -m ipykernel install --user --name=encrypto-anonymizer

echo "✅ Setup complete!"
echo ""
echo "To start JupyterLab, run:"
echo "  source .venv/bin/activate"
echo "  jupyter lab encrypto_anonymizer_local.ipynb"
echo ""
echo "Or use UV to run directly:"
echo "  uv run jupyter lab encrypto_anonymizer_local.ipynb"