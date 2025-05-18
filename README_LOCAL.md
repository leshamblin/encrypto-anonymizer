# 🔐 Encrypto-Anonymizer (Local Version)

A secure, locally-running tool to anonymize and encrypt CSV data, perfect for handling sensitive student data.

## 🔒 Security Features

- **100% Local Processing**: All data stays on your machine
- **No Cloud Dependencies**: No data is uploaded anywhere
- **Secure Encryption**: Uses industry-standard Fernet encryption
- **Flexible Anonymization**: Supports both individual and composite key anonymization

## 🚀 Quick Start with UV

### 1. Install UV (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Setup the project
```bash
./setup.sh
```

### 3. Run JupyterLab
```bash
uv run jupyter lab encrypto_anonymizer_local.ipynb
```

## 📋 Features

### Anonymization Modes

1. **Composite Key Mode** (default): Creates a single anonymous ID for all selected columns in each row
   - Perfect for keeping related data (Name, Email, ID) linked
   - Maintains relationships between fields

2. **Individual Mode**: Creates separate anonymous IDs for each value
   - Traditional anonymization approach
   - Each value gets its own unique identifier

### Smart Mapping

- Automatically detects if a value has already been anonymized
- Reuses existing mappings to avoid duplicates
- Maintains reverse mapping for efficiency

## 🔧 Manual Setup (without UV)

If you prefer not to use UV:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pandas cryptography jupyterlab ipykernel

# Install Jupyter kernel
python -m ipykernel install --user --name=encrypto-anonymizer

# Run JupyterLab
jupyter lab encrypto_anonymizer_local.ipynb
```

## 📁 File Structure

After anonymization, you'll have:
- `anonymized.csv`: Your anonymized data
- `mapping.json`: Encrypted mapping of anonymous IDs to original values
- `key.key`: Encryption key (keep this secure!)

## ⚠️ Important Security Notes

1. **Keep the key.key file secure** - Without it, you cannot decrypt your data
2. **Store mapping.json safely** - It contains the encrypted original values
3. **Never share these files publicly** - They can be used to de-anonymize your data
4. **Make backups** - Especially of the key and mapping files

## 🔄 Workflow

1. Load your CSV file
2. Select columns to anonymize
3. Choose anonymization mode (composite or individual)
4. Save anonymized data and secure files
5. Later: Load all three files to restore original data

## 🛡️ Best Practices

- Always test on sample data first
- Keep original data in a secure location
- Store key and mapping files separately from anonymized data
- Consider using different storage locations for added security
- Document which files belong together

## 📝 License

Same as the original Encrypto-Anonymizer project.