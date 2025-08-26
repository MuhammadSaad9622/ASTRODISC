# 🌟 AstroDISC™ Lite - Streamlit Version

A beautiful, responsive Streamlit application that generates personalized career recommendations based on astrological birth charts and DISC personality profiles.

## 🚀 **Why Streamlit?**

- **✅ Cloud-Ready**: Built for deployment on Streamlit Cloud, Heroku, and other platforms
- **✅ No Server Issues**: No Flask signal handler conflicts
- **✅ Interactive**: Real-time updates and beautiful UI components
- **✅ Responsive**: Automatically adapts to different screen sizes
- **✅ Easy Deployment**: One-click deployment to Streamlit Cloud

## 🎯 **Features**

- **🔮 AI-Powered Insights**: Uses Google's Gemini API for personalized recommendations
- **⚡ Smart Fallback**: Automatically switches to built-in generator when API is unavailable
- **🎨 Beautiful UI**: Modern design with gradients, cards, and smooth animations
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **🔧 Easy Configuration**: Simple API key setup in the sidebar
- **📊 Real-time Status**: Live API status and model detection

## 🚀 **Quick Start**

### **Local Development**
1. **Install dependencies**:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Set up environment**:
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

### **Streamlit Cloud Deployment**
1. **Push to GitHub** (if not already done)
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set the path to `streamlit_app.py`
   - Add your `GEMINI_API_KEY` as a secret

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in your project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### **Getting a Gemini API Key**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key to your `.env` file

## 🎨 **UI Features**

### **Main Interface**
- **Gradient Header**: Beautiful purple-to-blue gradient with app title
- **Sidebar Configuration**: API status, key input, and information
- **Form Inputs**: Clean, labeled input fields for birth chart and DISC profile
- **Results Display**: Professional card-based results with source indicators

### **Responsive Design**
- **Two-Column Layout**: Main content and quick actions
- **Mobile Optimized**: Automatically adjusts for small screens
- **Touch-Friendly**: Large buttons and input fields

### **Interactive Elements**
- **Real-time Status**: Live API availability indicators
- **Form Validation**: Input validation and helpful placeholders
- **Loading States**: Spinner animations during API calls
- **Error Handling**: Graceful fallbacks and user-friendly messages

## 🔮 **How It Works**

### **1. Input Processing**
- Users enter their birth chart details (e.g., "Sun in Libra, Ascendant in Capricorn")
- Users input their DISC profile (e.g., "High C, low I")

### **2. AI Generation**
- **Gemini API Mode**: Uses Google's AI to generate unique recommendations
- **Fallback Mode**: Uses built-in logic when API is unavailable

### **3. Output Delivery**
- **Single Paragraph**: Concise, actionable career advice
- **Source Indication**: Clear labeling of whether AI or fallback was used
- **Input Confirmation**: Shows exactly what inputs were processed

## 📱 **Deployment Options**

### **Streamlit Cloud (Recommended)**
- **Free hosting** for public repositories
- **Automatic updates** when you push to GitHub
- **Easy secret management** for API keys
- **Global CDN** for fast loading worldwide

### **Heroku**
- **Custom domain** support
- **Environment variables** for configuration
- **Scalable** infrastructure

### **Local Development**
- **Fast iteration** during development
- **Full control** over environment
- **Debug capabilities**

## 🔍 **Troubleshooting**

### **Common Issues**
1. **API Key Not Working**:
   - Verify the key is correct
   - Check if billing is enabled
   - Ensure the key has proper permissions

2. **Model Not Found**:
   - The app automatically tries different models
   - Check your API quota and rate limits
   - Try restarting the application

3. **Deployment Issues**:
   - Ensure `streamlit_app.py` is in the root directory
   - Check that all dependencies are in `requirements_streamlit.txt`
   - Verify environment variables are set correctly

### **Performance Tips**
- **Use Streamlit caching** for API calls (already implemented)
- **Optimize model selection** (automatic in this app)
- **Monitor API usage** to avoid rate limits

## 🏗️ **Architecture**

### **Frontend**
- **Streamlit**: Modern web framework for data apps
- **Custom CSS**: Beautiful styling with gradients and animations
- **Responsive Layout**: Adaptive design for all devices

### **Backend**
- **Python**: Core logic and API integration
- **Google Generative AI**: Advanced language model integration
- **Environment Management**: Secure configuration handling

### **AI Integration**
- **Automatic Model Detection**: Tries multiple Gemini models
- **Intelligent Fallback**: Seamless offline capability
- **Error Handling**: Graceful degradation on API issues

## 📊 **Example Usage**

### **Input Examples**
```
Birth Chart: Sun in Aries, Ascendant in Leo
DISC Profile: High D, High I, Low C, Low S
```

### **Expected Output**
A personalized, single-paragraph career recommendation that synthesizes the astrological and DISC insights into actionable advice.

## 🌟 **Future Enhancements**

- **Dark Mode Toggle**: User preference for light/dark themes
- **Export Functionality**: Save recommendations as PDF or text
- **History Tracking**: Remember previous recommendations
- **Advanced Analytics**: Insights into career pattern trends
- **Multi-language Support**: Internationalization for global users

---

**Built with ❤️ for beautiful, responsive web experiences using Streamlit**
