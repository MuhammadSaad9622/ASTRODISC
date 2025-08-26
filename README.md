# 🌟 AstroDISC™ Lite - Beautiful Career Insights

A stunning, responsive, and animated web application that generates personalized career recommendations based on astrological birth charts and DISC personality profiles.

## ✨ Features

- **🎨 Beautiful Modern UI**: Gradient backgrounds, glassmorphism effects, and smooth animations
- **📱 Fully Responsive**: Optimized for all devices from mobile to desktop
- **🎭 Smooth Animations**: Fade-in effects, hover animations, and interactive feedback
- **🔮 AI-Powered Insights**: Generates personalized career recommendations using Google's Gemini API
- **⚡ Smart Fallback**: Automatically uses built-in generator when API is unavailable
- **🎯 Single Paragraph Output**: Concise, actionable career advice as requested
- **🚀 Real-time API Status**: Visual indicator showing whether Gemini API is available

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 🎨 UI Features

### Visual Design
- **Gradient Backgrounds**: Beautiful purple-to-blue gradients
- **Glassmorphism**: Modern glass-like card effects with backdrop blur
- **Icon Integration**: Font Awesome icons for enhanced visual appeal
- **Typography**: Clean Inter font family for optimal readability

### Animations & Interactions
- **Fade-in Effects**: Smooth entrance animations for page elements
- **Hover Effects**: Interactive feedback on buttons and cards
- **Loading States**: Animated loading indicators with progress feedback
- **Success Animations**: Celebratory effects when recommendations are generated
- **Input Focus**: Subtle scaling and highlighting on form inputs

### Responsive Design
- **Mobile-First**: Optimized for small screens
- **Flexible Grids**: Adaptive layouts that work on all devices
- **Touch-Friendly**: Large touch targets for mobile users
- **Breakpoint Optimization**: Smooth transitions between screen sizes

## 🎯 Usage

### Web Interface
1. **Enter your birth chart** (e.g., "Sun in Libra, Ascendant in Capricorn")
2. **Input your DISC profile** (e.g., "High C, low I")
3. **Click "Generate Career Report"** to get your personalized recommendation
4. **View your result** in a beautifully formatted, easy-to-read paragraph

### Command Line Interface
For CLI usage, run:
```bash
python main.py --cli
```

## 🔧 Configuration

### Environment Variables
To enable real AI API integration, create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
```

**Getting a Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key to your `.env` file

**Note:** The Gemini API has evolved over time. The application automatically tries different model names:
- `gemini-1.5-pro` (latest)
- `gemini-1.5-flash` (fastest)
- `gemini-pro` (legacy)

**Example:**
```bash
# Copy the example file
cp env.example .env

# Edit .env and add your actual API key
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
```

### Customization
- Modify `BIRTH_CHART` and `DISC_PROFILE` defaults in `main.py`
- Adjust the `DEFAULT_PROMPT` for different recommendation styles
- Customize colors and animations in the CSS section

## 🏗️ Architecture

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Flask (Python)
- **AI Integration**: Google Gemini API with intelligent fallback
- **Styling**: Tailwind CSS with custom animations
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)

## 🤖 Gemini API Integration

The application intelligently switches between two modes:

### 🚀 **Gemini API Mode** (When API key is available)
- **Real AI Insights**: Uses Google's advanced language model
- **Dynamic Prompts**: Generates unique recommendations for each input
- **Contextual Understanding**: Better synthesis of astrological and DISC data
- **Professional Quality**: More nuanced and personalized career advice

### 📝 **Fallback Generator Mode** (When API is unavailable)
- **Offline Capability**: Works without internet connection
- **Rule-based Logic**: Pre-programmed career insights
- **Consistent Output**: Reliable fallback for assessment requirements
- **No API Dependencies**: Self-contained functionality

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🎨 Customization

### Colors
The application uses a carefully selected color palette:
- **Primary**: Indigo to Purple gradients
- **Secondary**: Blue accents
- **Background**: Purple to Blue gradients
- **Text**: Dark grays for readability

### Animations
- **Duration**: 0.3s for most interactions
- **Easing**: Cubic-bezier curves for natural movement
- **Hover Effects**: Subtle lift and shadow changes
- **Loading**: Smooth progress indicators

## 🔍 Troubleshooting

### Common Issues
1. **Port already in use**: Change the port with `--port 5001`
2. **Dependencies missing**: Ensure you've run `pip install -r requirements.txt`
3. **Font loading issues**: Check internet connection for Google Fonts
4. **Gemini API not working**: Verify your API key in `.env` file and restart the app
5. **API rate limits**: Gemini API has usage limits; check your Google AI Studio dashboard
6. **Model not found errors**: Use the "Check Models" button to see available models
7. **API version issues**: The app automatically tries different model names for compatibility

### Performance
- The application is optimized for fast loading
- Animations use CSS transforms for smooth performance
- Minimal JavaScript for optimal responsiveness

## 📄 License

This project is built for assessment purposes and includes offline fallback functionality.

## 🌟 Future Enhancements

Potential improvements could include:
- Dark mode toggle
- More animation variations
- Additional personality frameworks
- Export functionality for recommendations
- User account system

---

**Built with ❤️ for beautiful, responsive web experiences**
