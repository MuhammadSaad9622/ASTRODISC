# 🚀 Deployment Guide - AstroDISC™ Lite

## 🌟 **Streamlit Cloud (Recommended)**

### **Step 1: Prepare Your Repository**
1. **Ensure your files are in the correct structure**:
   ```
   your-repo/
   ├── streamlit_app.py          # Main application
   ├── requirements_streamlit.txt # Dependencies
   ├── .env                      # Local environment (don't commit this)
   └── README.md                 # Documentation
   ```

2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Streamlit version of AstroDISC Lite"
   git push origin main
   ```

### **Step 2: Deploy to Streamlit Cloud**
1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: Select your GitHub repo
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose a custom subdomain (optional)

### **Step 3: Add Your API Key**
1. **In the Streamlit Cloud dashboard, go to "Settings"**
2. **Click "Secrets"**
3. **Add your Gemini API key**:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
4. **Save and redeploy**

### **Step 4: Access Your App**
- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this URL with others!

## 🐳 **Docker Deployment**

### **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Build and Run**
```bash
# Build the image
docker build -t astrodisc-lite .

# Run the container
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key_here astrodisc-lite
```

## ☁️ **Heroku Deployment**

### **Step 1: Create Heroku App**
```bash
# Install Heroku CLI
heroku create your-astrodisc-app

# Set environment variables
heroku config:set GEMINI_API_KEY=your_api_key_here
```

### **Step 2: Create Procfile**
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### **Step 3: Deploy**
```bash
git push heroku main
```

## 🔧 **Local Development**

### **Install Dependencies**
```bash
pip install -r requirements_streamlit.txt
```

### **Set Environment Variables**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### **Run the App**
```bash
streamlit run streamlit_app.py
```

## 📱 **Environment Variables**

### **Required Variables**
- `GEMINI_API_KEY`: Your Google Gemini API key

### **Optional Variables**
- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

## 🔍 **Troubleshooting**

### **Common Deployment Issues**

1. **"Module not found" errors**:
   - Ensure `requirements_streamlit.txt` includes all dependencies
   - Check that the file path in Streamlit Cloud is correct

2. **API key not working**:
   - Verify the key is set correctly in Streamlit Cloud secrets
   - Check if the key has proper permissions and billing

3. **App not loading**:
   - Check the Streamlit Cloud logs for errors
   - Ensure `streamlit_app.py` is in the root directory

4. **Performance issues**:
   - The app uses caching for API calls
   - Monitor your Gemini API usage to avoid rate limits

### **Performance Optimization**
- **Streamlit caching** is already implemented
- **Model detection** happens once per session
- **API calls** are cached to reduce latency

## 🌐 **Custom Domain (Optional)**

### **Streamlit Cloud**
- Currently doesn't support custom domains
- Use the provided `.streamlit.app` subdomain

### **Heroku**
```bash
heroku domains:add yourdomain.com
# Follow DNS configuration instructions
```

### **Docker/Other**
- Configure your reverse proxy (nginx, etc.)
- Point to the Streamlit port (8501)

## 📊 **Monitoring**

### **Streamlit Cloud**
- Built-in analytics and usage statistics
- Error logs and performance metrics
- Automatic scaling and uptime monitoring

### **Custom Monitoring**
```bash
# Check app health
curl http://your-app-url/_stcore/health

# Monitor logs
heroku logs --tail  # For Heroku
docker logs container_name  # For Docker
```

## 🔒 **Security Considerations**

1. **API Key Protection**:
   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **Input Validation**:
   - The app validates all user inputs
   - No SQL injection or XSS vulnerabilities
   - Rate limiting through Gemini API

3. **Data Privacy**:
   - No user data is stored permanently
   - All processing happens in memory
   - API calls are logged but not stored

---

**Your AstroDISC™ Lite app is now ready for deployment! 🎉**
