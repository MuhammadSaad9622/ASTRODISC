# 🔧 Streamlit Configuration Guide

## 🌟 **Streamlit Cloud Deployment**

### **Step 1: Add Secrets in Streamlit Cloud**
1. Go to your app dashboard in [share.streamlit.io](https://share.streamlit.io)
2. Click **"Settings"** → **"Secrets"**
3. Add your Gemini API key in this format:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

### **Step 2: Deploy**
- The app will automatically use the secrets from Streamlit Cloud
- No additional configuration needed

## 🏠 **Local Development**

### **Option 1: Using .streamlit/secrets.toml (Recommended)**

1. **Create the secrets directory**:
   ```bash
   mkdir .streamlit
   ```

2. **Create secrets.toml file**:
   ```bash
   cp .streamlit/secrets.toml .streamlit/secrets.toml
   ```

3. **Edit the file** with your actual API key:
   ```toml
   GEMINI_API_KEY = "AIzaSyC...your_actual_key_here"
   ```

4. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

### **Option 2: Using Environment Variables**

1. **Set environment variable**:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

2. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 📁 **File Structure**

```
your-project/
├── streamlit_app.py              # Main application
├── requirements_streamlit.txt     # Dependencies
├── .streamlit/
│   └── secrets.toml             # Local secrets (don't commit)
├── .gitignore                   # Should include .streamlit/
└── README.md
```

## 🔒 **Security Best Practices**

### **Never Commit Secrets**
```bash
# Add to .gitignore
echo ".streamlit/" >> .gitignore
echo "secrets.toml" >> .gitignore
```

### **Use Different Keys**
- **Development**: Use a test API key
- **Production**: Use your main API key in Streamlit Cloud

## 🚀 **Quick Start Commands**

### **First Time Setup**
```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Create secrets directory
mkdir -p .streamlit

# Copy secrets template
cp .streamlit/secrets.toml .streamlit/secrets.toml

# Edit with your API key
nano .streamlit/secrets.toml
```

### **Run Locally**
```bash
streamlit run streamlit_app.py
```

### **Deploy to Streamlit Cloud**
1. Push to GitHub
2. Connect in Streamlit Cloud
3. Add secrets in dashboard
4. Deploy!

## 🔍 **Troubleshooting**

### **"No API key found" Error**
- Check if `secrets.toml` exists in `.streamlit/` folder
- Verify the key format: `GEMINI_API_KEY = "key_here"`
- Ensure no spaces around the `=` sign

### **Local vs Cloud Differences**
- **Local**: Uses `.streamlit/secrets.toml`
- **Cloud**: Uses dashboard secrets
- **Environment**: Falls back to `os.getenv()`

### **File Permissions**
```bash
# Ensure proper permissions
chmod 600 .streamlit/secrets.toml
```

## 📝 **Example secrets.toml**

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz"

# Optional customizations
# BIRTH_CHART = "Sun in Aries, Ascendant in Leo"
# DISC_PROFILE = "High D, low S"
```

## 🌐 **Environment Variables (Alternative)**

If you prefer environment variables:

```bash
# macOS/Linux
export GEMINI_API_KEY="your_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_key_here
```

## ✅ **Verification**

To verify your configuration is working:

1. **Check API Status**: The app shows "✅ Gemini API Available"
2. **Test Generation**: Try generating a career recommendation
3. **Check Console**: Look for any error messages

---

**Your Streamlit app is now properly configured! 🎉**
