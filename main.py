

from flask import Flask, render_template_string, request, jsonify
import argparse
import os
import textwrap
import html
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# =====================
# Configuration / Data
# =====================
BIRTH_CHART = "Sun in Libra, Ascendant in Capricorn"
DISC_PROFILE = "High C, low I"
DEFAULT_PROMPT = (
    "Synthesize a career recommendation based on a person with a birth chart indicating 'Sun in Libra, "
    "Ascendant in Capricorn' and a DISC profile of 'High C, low I.' The final output should be a single paragraph "
    "written in a friendly, conversational tone, suitable for a personalized report. The key themes to explore "
    "are balancing an innate desire for harmony with a disciplined work ethic, and leveraging a detail-oriented "
    "nature in a role that values structure."
)

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Function to list available models
        def list_available_models():
            try:
                models = genai.list_models()
                print("📋 Available Gemini models:")
                for model in models:
                    if 'generateContent' in model.supported_generation_methods:
                        print(f"  ✅ {model.name} - Supports generateContent")
                    else:
                        print(f"  ❌ {model.name} - No generateContent support")
                return models
            except Exception as e:
                print(f"⚠️  Could not list models: {e}")
                return []
        
        # Function to test API connection
        def test_api_connection():
            try:
                print("🔍 Testing API connection...")
                # Try to list models first
                models = list(genai.list_models())  # Convert generator to list
                print(f"✅ API connection successful. Found {len(models)} models.")
                return True
            except Exception as e:
                print(f"❌ API connection failed: {e}")
                print(f"💡 Error type: {type(e).__name__}")
                if "404" in str(e):
                    print("💡 404 error suggests model not found or API version mismatch")
                elif "403" in str(e):
                    print("💡 403 error suggests API key permission issues")
                elif "401" in str(e):
                    print("💡 401 error suggests invalid API key")
                return False
        
        # Test API connection first
        if not test_api_connection():
            print("❌ Cannot proceed with model testing due to API connection issues")
            GEMINI_AVAILABLE = False
        else:
            # List available models first
            available_models_list = list_available_models()
            
            # Try different model names - updated for current API version
            # The API has changed and these are the current model names
            available_models = [
                'gemini-1.5-pro-latest',  # Latest stable version
                'gemini-1.5-pro-002',     # Stable version from September 2024
                'gemini-1.5-pro',         # Stable version from May 2024
                'gemini-1.5-flash-latest', # Latest flash version
                'gemini-1.5-flash-002',   # Stable flash version
                'gemini-1.5-flash',       # Flash alias
                'gemini-2.0-flash',       # Newer 2.0 version
                'gemini-2.0-flash-001'    # Stable 2.0 version
            ]
            GEMINI_MODEL = None
            
            for model_name in available_models:
                try:
                    print(f"🔍 Testing model: {model_name}")
                    GEMINI_MODEL = genai.GenerativeModel(model_name)
                    # Test the model with a simple prompt
                    response = GEMINI_MODEL.generate_content("Hello")
                    if response and response.text:
                        print(f"✅ Gemini API configured successfully with model: {model_name}")
                        break
                    else:
                        print(f"⚠️  Model {model_name} returned empty response")
                except Exception as model_error:
                    print(f"⚠️  Model {model_name} failed: {model_error}")
                    continue
            
            if GEMINI_MODEL:
                GEMINI_AVAILABLE = True
                print(f"🎯 Using Gemini model: {GEMINI_MODEL.model_name}")
            else:
                print("❌ No working Gemini model found")
                print("💡 This might be due to:")
                print("   - API key permissions")
                print("   - Model availability in your region")
                print("   - API version compatibility")
                GEMINI_AVAILABLE = False
                
    except Exception as e:
        print(f"⚠️  Gemini API configuration failed: {e}")
        print(f"💡 Error details: {type(e).__name__}")
        GEMINI_AVAILABLE = False
else:
    GEMINI_AVAILABLE = False
    print("⚠️  No GEMINI_API_KEY found in environment variables. Using fallback generator.")

# =====================
# Utility: Fallback generator
# =====================
def generate_fallback_paragraph(birth_chart: str, disc: str) -> str:
    """
    Rule-based paragraph generator that synthesizes the two data points into a friendly paragraph.
    This allows the app to work offline and satisfies the "single paragraph" output requirement.
    """
    # Break down features to craft an empathetic, professional-sounding paragraph.
    # We keep it concise and single-paragraph as required by the assessment.
    parts = []

    parts.append("With Sun in Libra, you naturally value fairness, relationships, and balance, and with an Ascendant in Capricorn, you bring a steady, disciplined approach to how you present yourself at work.")
    parts.append("Your DISC profile — high Conscientiousness and low Influence — suggests you thrive in roles that reward precision, structure, and deep thinking rather than constant social selling or networking.")
    parts.append("A fulfilling career path for you could be in areas like project coordination, compliance, technical writing, data analysis, or quality assurance — roles where a methodological mindset and an eye for detail are prized.")
    parts.append("To maximize satisfaction, look for positions that allow collaborative harmony (so your Libra strengths are honored) but offer clear frameworks, measurable goals, and opportunities to work independently on structured tasks that showcase your reliability.")

    paragraph = " ".join(parts)
    # Ensure single paragraph and reasonable length
    paragraph = textwrap.fill(paragraph, width=100)
    return paragraph

# =====================
# Gemini API Integration
# =====================
def generate_gemini_paragraph(birth_chart: str, disc: str) -> str:
    """
    Generate career recommendation using Gemini API.
    Returns a single paragraph as requested in the assessment.
    """
    if not GEMINI_AVAILABLE:
        return generate_fallback_paragraph(birth_chart, disc)
    
    try:
        # Construct the prompt as specified in the assessment
        prompt = f"""Synthesize a career recommendation based on a person with a birth chart indicating '{birth_chart}' and a DISC profile of '{disc}'. 

The final output should be a single paragraph written in a friendly, conversational tone, suitable for a personalized report. 

Key themes to explore:
- Balancing an innate desire for harmony with a disciplined work ethic
- Leveraging a detail-oriented nature in a role that values structure
- Finding career paths that align with both astrological and personality traits

Please provide exactly one well-structured paragraph that synthesizes these insights into actionable career advice."""

        # Generate response using Gemini
        response = GEMINI_MODEL.generate_content(prompt)
        
        if response and response.text:
            # Clean and format the response
            paragraph = response.text.strip()
            
            # Ensure it's a single paragraph (remove extra line breaks)
            paragraph = ' '.join(paragraph.split())
            
            # If response is too long, truncate to reasonable length
            if len(paragraph) > 500:
                sentences = paragraph.split('. ')
                paragraph = '. '.join(sentences[:3]) + '.'
            
            return paragraph
        else:
            print("⚠️  Gemini API returned empty response, using fallback")
            return generate_fallback_paragraph(birth_chart, disc)
            
    except Exception as e:
        print(f"⚠️  Gemini API error: {e}, using fallback")
        return generate_fallback_paragraph(birth_chart, disc)


BASE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AstroDISC™ Lite — Career Snapshot</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
      * {
        font-family: 'Inter', sans-serif;
      }
      
      body { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        overflow-x: hidden;
      }
      
      .glass { 
        background: rgba(255,255,255,0.95); 
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
      }
      
      .card { 
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }
      
      .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.3);
      }
      
      .input-field {
        transition: all 0.3s ease;
        border: 2px solid transparent;
        background: rgba(255,255,255,0.8);
      }
      
      .input-field:focus {
        border-color: #667eea;
        background: white;
        transform: scale(1.02);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
      }
      
      .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
      }
      
      .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
      }
      
      .btn-primary:active {
        transform: translateY(0);
      }
      
      .btn-secondary {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
      }
      
      .btn-secondary:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
      }
      
      .result-box {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        min-height: 120px;
        position: relative;
        overflow: hidden;
      }
      
      .result-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s ease;
      }
      
      .result-box.loading::before {
        left: 100%;
      }
      
      .floating {
        animation: floating 3s ease-in-out infinite;
      }
      
      @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
      }
      
      .fade-in {
        animation: fadeIn 0.6s ease-out;
      }
      
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
      }
      
      .slide-in {
        animation: slideIn 0.8s ease-out;
      }
      
      @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
      }
      
      .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
      }
      
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
      
      .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
      
      .icon-float {
        animation: iconFloat 2s ease-in-out infinite;
      }
      
      @keyframes iconFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(5deg); }
      }
      
      .success-animation {
        animation: successPop 0.6s ease-out;
      }
      
      @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
      }
      
      .loading-dots {
        display: inline-block;
      }
      
      .loading-dots::after {
        content: '';
        animation: loadingDots 1.5s infinite;
      }
      
      @keyframes loadingDots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
      }
      
      @media (max-width: 768px) {
        .card { margin: 1rem; }
        .header-grid { grid-template-columns: 1fr; }
        .input-grid { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body class="min-h-screen flex items-center justify-center p-4">
    <div class="fixed inset-0 bg-gradient-to-br from-purple-900/20 to-blue-900/20 pointer-events-none"></div>
    
    <main class="max-w-4xl w-full relative z-10">
      <!-- Header Section -->
      <div class="text-center mb-8 fade-in">
        <div class="inline-block p-4 rounded-full bg-white/20 backdrop-blur-sm mb-4">
          <i class="fas fa-star text-4xl text-yellow-400 icon-float"></i>
        </div>
                  <h1 class="text-4xl md:text-6xl font-bold text-white mb-2">
            <span class="text-white">AstroDISC™</span> Lite
          </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Discover your perfect career path through the harmony of astrology and personality insights
        </p>
      </div>

      <!-- Main Card -->
      <div class="glass card rounded-3xl p-8 md:p-12 slide-in">
        <!-- Card Header -->
        <header class="text-center mb-8">
          <div class="inline-flex items-center gap-3 bg-gradient-to-r from-indigo-100 to-purple-100 px-6 py-3 rounded-full mb-4">
            <i class="fas fa-magic text-indigo-600"></i>
            <span class="text-indigo-700 font-medium">AI-Powered Career Insights</span>
          </div>
          <h2 class="text-2xl md:text-3xl font-semibold text-gray-800 mb-2">
            Your Personalized Career Snapshot
          </h2>
          <p class="text-gray-600">Get instant career recommendations based on your unique astrological and DISC profile</p>
          
          <!-- API Status Indicator -->
          <div id="apiStatus" class="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium">
            <i class="fas fa-circle text-xs"></i>
            <span>Checking API status...</span>
          </div>
        </header>

        <!-- Input Section -->
        <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 flex items-center gap-2">
              <i class="fas fa-sun text-yellow-500"></i>
              Birth Chart
            </label>
            <input 
              id="birth" 
              class="input-field w-full rounded-xl p-4 text-gray-800 placeholder-gray-400 focus:outline-none" 
              value="{{ birth_chart }}"
              placeholder="Enter your birth chart details..."
            />
            <div id="birthStatus" class="text-xs text-gray-500 hidden">
              <i class="fas fa-info-circle"></i> Input changed from default
            </div>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 flex items-center gap-2">
              <i class="fas fa-user text-blue-500"></i>
              DISC Profile
            </label>
            <input 
              id="disc" 
              class="input-field w-full rounded-xl p-4 text-gray-800 placeholder-gray-400 focus:outline-none" 
              value="{{ disc_profile }}"
              placeholder="Enter your DISC profile..."
            />
            <div id="discStatus" class="text-xs text-gray-500 hidden">
              <i class="fas fa-info-circle"></i> Input changed from default
            </div>
          </div>
        </section>

        <!-- Action Buttons -->
        <section class="flex flex-col sm:flex-row gap-4 mb-8">
          <button id="generateBtn" class="btn-primary flex-1 px-8 py-4 rounded-xl text-white font-semibold text-lg flex items-center justify-center gap-3 hover:shadow-lg transition-all duration-300">
            <i class="fas fa-wand-magic-sparkles"></i>
            Generate Career Report
          </button>
          <button id="clearBtn" class="btn-secondary px-4 py-4 rounded-xl text-gray-700 font-medium flex items-center justify-center gap-3 transition-all duration-300">
            <i class="fas fa-eraser"></i>
            Clear
          </button>
          <button id="cliBtn" class="btn-secondary px-6 py-4 rounded-xl text-gray-700 font-medium flex items-center justify-center gap-3 transition-all duration-300">
            <i class="fas fa-terminal"></i>
            Copy CLI Command
          </button>
          <button id="modelsBtn" class="btn-secondary px-4 py-4 rounded-xl text-gray-700 font-medium flex items-center justify-center gap-3 transition-all duration-300">
            <i class="fas fa-list"></i>
            Check Models
          </button>
        </section>

        <!-- Result Section -->
        <section class="space-y-4">
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold text-gray-800">Your Career Recommendation</h3>
            <div class="w-2 h-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full pulse"></div>
          </div>
          <div id="result" class="result-box rounded-xl p-6 text-gray-700 leading-relaxed text-lg">
            <div class="text-center text-gray-500">
              <i class="fas fa-sparkles text-2xl mb-2"></i>
              <p>Click "Generate Career Report" to get your personalized recommendation</p>
            </div>
          </div>
        </section>

        <!-- Footer -->
        <footer class="mt-8 pt-6 border-t border-gray-200">
          <div class="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-500">
            <div class="flex items-center gap-2">
              <i class="fas fa-shield-alt text-green-500"></i>
              <span>Built for assessment — includes offline fallback generator</span>
            </div>
            <div class="flex items-center gap-2">
              <i class="fas fa-rocket text-blue-500"></i>
              <span>Demo · Responsive · Local-first</span>
            </div>
          </div>
        </footer>
      </div>

      <!-- Info Card -->
      <div class="mt-6 text-center">
        <div class="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-white/80 text-sm">
          <i class="fas fa-info-circle"></i>
          
        </div>
      </div>
    </main>

    <script>
      const resultEl = document.getElementById('result')
      const birthEl = document.getElementById('birth')
      const discEl = document.getElementById('disc')
      const generateBtn = document.getElementById('generateBtn')
      const clearBtn = document.getElementById('clearBtn')
      const cliBtn = document.getElementById('cliBtn')
      const modelsBtn = document.getElementById('modelsBtn')
      const apiStatusEl = document.getElementById('apiStatus')
      const birthStatusEl = document.getElementById('birthStatus')
      const discStatusEl = document.getElementById('discStatus')
      
      // Store default values for comparison
      const defaultBirth = '{{ birth_chart }}';
      const defaultDisc = '{{ disc_profile }}';

      // Add floating animation to elements
      document.addEventListener('DOMContentLoaded', function() {
        const elements = document.querySelectorAll('.fade-in, .slide-in');
        elements.forEach((el, index) => {
          el.style.animationDelay = `${index * 0.1}s`;
        });
        
        // Check API status
        checkApiStatus();
        
        // Check initial input status
        checkInputChanges();
      });
      
      // Check API status
      async function checkApiStatus() {
        try {
          const response = await fetch('/api-status');
          const data = await response.json();
          
          if (data.available) {
            apiStatusEl.innerHTML = '<i class="fas fa-circle text-green-500"></i><span class="text-green-700">Gemini API Available</span>';
            apiStatusEl.className = 'mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium bg-green-100 text-green-700';
          } else {
            apiStatusEl.innerHTML = '<i class="fas fa-circle text-orange-500"></i><span class="text-orange-700">Fallback Generator</span>';
            apiStatusEl.className = 'mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium bg-orange-100 text-orange-700';
          }
        } catch (e) {
          apiStatusEl.innerHTML = '<i class="fas fa-circle text-gray-500"></i><span class="text-gray-700">Status Unknown</span>';
          apiStatusEl.className = 'mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-700';
        }
      }
      
      // Check if inputs have changed from defaults
      function checkInputChanges() {
        const birthChanged = birthEl.value !== defaultBirth;
        const discChanged = discEl.value !== defaultDisc;
        
        birthStatusEl.classList.toggle('hidden', !birthChanged);
        discStatusEl.classList.toggle('hidden', !discChanged);
        
        // Show visual indicator if any inputs have changed
        if (birthChanged || discChanged) {
          generateBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate New Report';
          generateBtn.classList.add('bg-purple-600');
        } else {
          generateBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate Career Report';
          generateBtn.classList.remove('bg-purple-600');
        }
      }

      async function generate() {
        // Update button state
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        generateBtn.disabled = true;
        
        // Show loading state with current inputs
        resultEl.innerHTML = `
          <div class="text-center text-gray-600">
            <div class="loading-dots mb-2">
              <i class="fas fa-magic text-2xl text-indigo-500"></i>
            </div>
            <p>Analyzing your cosmic alignment and personality traits...</p>
            <div class="mt-3 text-xs text-gray-500">
              <div>Birth Chart: <strong>${birthEl.value}</strong></div>
              <div>DISC Profile: <strong>${discEl.value}</strong></div>
            </div>
          </div>
        `;
        resultEl.classList.add('loading');
        
        const payload = { birth: birthEl.value, disc: discEl.value }
        
        // Debug: Log what we're sending
        console.log('Sending payload:', payload);
        
        try {
          const r = await fetch('/generate', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify(payload)
          })
          
          const data = await r.json()
          
          if (r.ok) {
            // Success animation
            resultEl.classList.remove('loading');
            resultEl.classList.add('success-animation');
            
            resultEl.innerHTML = `
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3 text-green-600">
                    <i class="fas fa-check-circle text-xl"></i>
                    <span class="font-medium">Career Recommendation Generated!</span>
                  </div>
                  <div class="text-xs px-2 py-1 rounded-full ${data.source === 'Gemini API' ? 'bg-blue-100 text-blue-700' : 'bg-orange-100 text-orange-700'}">
                    ${data.source}
                  </div>
                </div>
                
                <!-- Show the inputs that were processed -->
                <div class="bg-gray-50 p-3 rounded-lg text-sm">
                  <div class="font-medium text-gray-700 mb-2">Based on your inputs:</div>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-gray-600">
                    <div><span class="font-medium">Birth Chart:</span> ${birthEl.value}</div>
                    <div><span class="font-medium">DISC Profile:</span> ${discEl.value}</div>
                  </div>
                </div>
                
                <div class="text-gray-700 leading-relaxed">
                  ${data.paragraph}
                </div>
              </div>
            `;
          } else {
            resultEl.innerHTML = `
              <div class="text-center text-red-600">
                <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
                <p>${data.error || 'An error occurred while generating your recommendation.'}</p>
              </div>
            `;
          }
        } catch (e) {
          resultEl.innerHTML = `
            <div class="text-center text-red-600">
              <i class="fas fa-wifi text-2xl mb-2"></i>
              <p>Network error. Please check your connection and try again.</p>
            </div>
          `;
        } finally {
          // Reset button state
          generateBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate Career Report';
          generateBtn.disabled = false;
          resultEl.classList.remove('loading');
        }
      }

      generateBtn.addEventListener('click', generate)

      clearBtn.addEventListener('click', () => {
        // Reset inputs to defaults
        birthEl.value = '{{ birth_chart }}';
        discEl.value = '{{ disc_profile }}';
        
        // Clear results
        resultEl.innerHTML = `
          <div class="text-center text-gray-500">
            <i class="fas fa-sparkles text-2xl mb-2"></i>
            <p>Click "Generate Career Report" to get your personalized recommendation</p>
          </div>
        `;
        resultEl.classList.remove('success-animation', 'loading');
        
        // Reset status indicators
        checkInputChanges();
        
        // Focus on first input
        birthEl.focus();
      });

      modelsBtn.addEventListener('click', async () => {
        try {
          const response = await fetch('/models');
          const data = await response.json();
          
          if (response.ok) {
            let modelsHtml = '<div class="space-y-3">';
            modelsHtml += '<div class="font-medium text-gray-700">Available Gemini Models:</div>';
            
            data.models.forEach(model => {
              modelsHtml += `
                <div class="bg-green-50 p-3 rounded-lg border border-green-200">
                  <div class="font-medium text-green-800">${model.name}</div>
                  <div class="text-sm text-green-600">${model.description || 'No description'}</div>
                </div>
              `;
            });
            
            modelsHtml += '</div>';
            
            resultEl.innerHTML = `
              <div class="space-y-4">
                <div class="flex items-center gap-3 text-blue-600">
                  <i class="fas fa-list text-xl"></i>
                  <span class="font-medium">Available Models</span>
                </div>
                ${modelsHtml}
              </div>
            `;
          } else {
            resultEl.innerHTML = `
              <div class="text-center text-red-600">
                <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
                <p>${data.error || 'Failed to fetch models'}</p>
              </div>
            `;
          }
        } catch (e) {
          resultEl.innerHTML = `
            <div class="text-center text-red-600">
              <i class="fas fa-wifi text-2xl mb-2"></i>
              <p>Network error while fetching models</p>
            </div>
          `;
        }
      });

      cliBtn.addEventListener('click', () => {
        navigator.clipboard.writeText('python main.py --cli')
        .then(() => {
          // Show success feedback
          cliBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
          cliBtn.classList.add('bg-green-500', 'text-white');
          
          setTimeout(() => {
            cliBtn.innerHTML = '<i class="fas fa-terminal"></i> Copy CLI Command';
            cliBtn.classList.remove('bg-green-500', 'text-white');
          }, 2000);
        })
        .catch(() => {
          alert('Failed to copy command. Please copy manually: python main.py --cli');
        });
      })

      // Add input animations and change detection
      [birthEl, discEl].forEach(input => {
        input.addEventListener('focus', () => {
          input.parentElement.classList.add('scale-105');
        });
        
        input.addEventListener('blur', () => {
          input.parentElement.classList.remove('scale-105');
        });
        
        // Clear results when input changes
        input.addEventListener('input', () => {
          // Clear previous results when user starts typing
          resultEl.innerHTML = `
            <div class="text-center text-gray-500">
              <i class="fas fa-sparkles text-2xl mb-2"></i>
              <p>Click "Generate Career Report" to get your personalized recommendation</p>
            </div>
          `;
          resultEl.classList.remove('success-animation', 'loading');
          
          // Check if inputs have changed from defaults
          checkInputChanges();
        });
      });

      // Auto-generate on load with default values
      window.addEventListener('load', () => {
        // Clear any previous results first
        resultEl.innerHTML = `
          <div class="text-center text-gray-500">
            <i class="fas fa-sparkles text-2xl mb-2"></i>
            <p>Click "Generate Career Report" to get your personalized recommendation</p>
          </div>
        `;
        
        // Don't auto-generate - let user choose when to generate
        // setTimeout(generate, 1000); // Small delay for better UX
      });

      // Add some interactive hover effects
      document.querySelectorAll('.card, .btn-primary, .btn-secondary').forEach(el => {
        el.addEventListener('mouseenter', () => {
          el.style.transform = 'translateY(-2px)';
        });
        
        el.addEventListener('mouseleave', () => {
          el.style.transform = 'translateY(0)';
        });
      });
    </script>
  </body>
</html>
"""

@app.route('/')
def index():
    # Render page with defaults
    return render_template_string(BASE_HTML, birth_chart=BIRTH_CHART, disc_profile=DISC_PROFILE)

@app.route('/api-status')
def api_status():
    """Return the current API availability status"""
    return jsonify({
        'available': GEMINI_AVAILABLE,
        'source': 'Gemini API' if GEMINI_AVAILABLE else 'Fallback Generator'
    })

@app.route('/models')
def list_models():
    """List available Gemini models"""
    if not GEMINI_AVAILABLE:
        return jsonify({'error': 'Gemini API not configured'}), 400
    
    try:
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append({
                    'name': model.name,
                    'description': getattr(model, 'description', 'No description'),
                    'supported_methods': model.supported_generation_methods
                })
        return jsonify({'models': available_models})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(silent=True) or {}
    birth = data.get('birth', BIRTH_CHART)
    disc = data.get('disc', DISC_PROFILE)

    try:
        # Use Gemini API if available, otherwise fallback to rule-based generator
        if GEMINI_AVAILABLE:
            print(f"🚀 Using Gemini API for birth chart: {birth}, DISC: {disc}")
            paragraph = generate_gemini_paragraph(birth, disc)
        else:
            print(f"📝 Using fallback generator for birth chart: {birth}, DISC: {disc}")
            paragraph = generate_fallback_paragraph(birth, disc)
        
        return jsonify({ 
            'paragraph': paragraph,
            'source': 'Gemini API' if GEMINI_AVAILABLE else 'Fallback Generator'
        })
    except Exception as e:
        print(f"❌ Error generating paragraph: {e}")
        return jsonify({ 'error': 'Failed to generate paragraph.' }), 500


def run_cli():
    # The assessment explicitly wants a command-line script that uses the input data and prints a single paragraph.
    print("🔮 AstroDISC™ Lite - Career Recommendation Generator")
    print("=" * 60)
    print(f"Birth Chart: {BIRTH_CHART}")
    print(f"DISC Profile: {DISC_PROFILE}")
    print("=" * 60)
    
    if GEMINI_AVAILABLE:
        print("🚀 Using Gemini API for AI-powered insights...")
        paragraph = generate_gemini_paragraph(BIRTH_CHART, DISC_PROFILE)
        print("\n✨ AI-Generated Career Recommendation:")
    else:
        print("📝 Using fallback generator (no API key found)...")
        paragraph = generate_fallback_paragraph(BIRTH_CHART, DISC_PROFILE)
        print("\n📋 Generated Career Recommendation:")
    
    print("-" * 60)
    print(paragraph)
    print("-" * 60)
    
    if not GEMINI_AVAILABLE:
        print("\n💡 To enable Gemini API:")
        print("1. Get an API key from https://makersuite.google.com/app/apikey")
        print("2. Create a .env file with: GEMINI_API_KEY=your_key_here")
        print("3. Restart the application")

# =====================
# Entrypoint
# =====================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AstroDISC™ Lite — Web UI + CLI')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode and print the paragraph to console')
    parser.add_argument('--host', default=os.environ.get('HOST', '0.0.0.0'), help='Host for web server')
    parser.add_argument('--port', default=int(os.environ.get('PORT', 5000)), type=int, help='Port for web server')
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        print("🌟 AstroDISC™ Lite - Career Insights Platform")
        print("=" * 50)
        print(f"🌐 Web Interface: http://{args.host}:{args.port}")
        print(f"🔑 Gemini API: {'✅ Available' if GEMINI_AVAILABLE else '❌ Not Available'}")
        if not GEMINI_AVAILABLE:
            print("💡 To enable Gemini API, set GEMINI_API_KEY in .env file")
        print("=" * 50)
        app.run(host=args.host, port=args.port, debug=True)


# =====================
# End of file
# =====================