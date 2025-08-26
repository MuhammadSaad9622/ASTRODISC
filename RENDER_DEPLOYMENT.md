# 🚀 Render Deployment Guide - AstroDISC™ Lite

## 🌟 **Quick Deploy to Render**

### **Option 1: One-Click Deploy (Recommended)**
1. **Click this button**: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
2. **Connect your GitHub repository**
3. **Set environment variables** (see below)
4. **Deploy!**

### **Option 2: Manual Deployment**
1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure as shown below

## ⚙️ **Configuration Settings**

### **Basic Settings**
- **Name**: `astrodisc-lite` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (root of repo)

### **Build & Deploy**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py --host 0.0.0.0 --port $PORT`

### **Environment Variables**
Add these in the Render dashboard:

| Key | Value | Description |
|-----|-------|-------------|
| `GEMINI_API_KEY` | `your_api_key_here` | Your Google Gemini API key |
| `HOST` | `0.0.0.0` | Bind to all interfaces (required for Render) |
| `PORT` | `$PORT` | Use Render's assigned port |

## 🔧 **What I Fixed for Render:**

### **1. Host Binding Issue**
- **❌ Before**: `127.0.0.1` (localhost only)
- **✅ After**: `0.0.0.0` (all interfaces)

### **2. Port Configuration**
- **❌ Before**: Fixed port 5000
- **✅ After**: Uses `$PORT` environment variable

### **3. Dependencies**
- **✅ Added**: `gunicorn` for production WSGI server
- **✅ Updated**: All required packages

## 📁 **Required Files**

Your repository must include:
```
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── render.yaml         # Render configuration (optional)
└── .env                # Local development (don't commit)
```

## 🚀 **Deployment Steps**

### **Step 1: Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### **Step 2: Deploy on Render**
1. **Create Web Service**
2. **Connect Repository**
3. **Set Environment Variables**
4. **Deploy**

### **Step 3: Configure Environment**
In Render dashboard, add:
```
GEMINI_API_KEY = AIzaSyCUqOEyJ4mVyhQ0CvH1_aaBL7p4wQLFpLo
HOST = 0.0.0.0
```

## 🔍 **Troubleshooting**

### **"No open ports detected" Error**
- ✅ **Fixed**: App now binds to `0.0.0.0`
- ✅ **Fixed**: Uses `$PORT` environment variable
- ✅ **Fixed**: Proper start command

### **Common Issues**
1. **Port Binding**: Ensure `--host 0.0.0.0` is used
2. **Environment Variables**: Set `GEMINI_API_KEY` in Render dashboard
3. **Dependencies**: All packages in `requirements.txt`

### **Health Check**
- **Path**: `/` (root endpoint)
- **Expected**: 200 OK response
- **Timeout**: 30 seconds (default)

## 📊 **Performance & Scaling**

### **Free Tier**
- **Build Time**: 10 minutes max
- **Sleep After**: 15 minutes of inactivity
- **Bandwidth**: 750 GB/month

### **Upgrade Options**
- **Starter**: $7/month (always on)
- **Standard**: $25/month (auto-scaling)

## 🔒 **Security**

### **Environment Variables**
- **Never commit** API keys to Git
- **Use Render dashboard** for secrets
- **Local development** uses `.env` file

### **API Key Management**
1. **Get key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Set in Render** dashboard
3. **Restart service** after changes

## ✅ **Verification**

After deployment:
1. **Check logs** for successful startup
2. **Test health check** at your app URL
3. **Verify API status** shows "✅ Gemini API Available"
4. **Test generation** with sample inputs

## 🌐 **Your App URL**

Once deployed, your app will be available at:
```
https://astrodisc-lite.onrender.com
```

## 🎯 **Next Steps**

1. **Deploy to Render** using the guide above
2. **Test the application** with your API key
3. **Share the URL** with others
4. **Monitor usage** in Render dashboard

---

**Your AstroDISC™ Lite app is now ready for Render deployment! 🎉**
