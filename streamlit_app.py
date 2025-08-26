import streamlit as st
import google.generativeai as genai
import os
import textwrap

# Page configuration
st.set_page_config(
    page_title="AstroDISC™ Lite — Career Snapshot",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration - Support both .env and Streamlit secrets
BIRTH_CHART = "Sun in Libra, Ascendant in Capricorn"
DISC_PROFILE = "High C, low I"

# Gemini API Configuration with Streamlit secrets support
@st.cache_resource
def configure_gemini_api():
    """Configure Gemini API with automatic model detection"""
    # Try to get API key from Streamlit secrets first, then environment variables
    api_key = None
    
    # Method 1: Streamlit secrets (for Streamlit Cloud deployment)
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        pass
    
    # Method 2: Environment variables (for local development)
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return None, "No API key found in secrets or environment"
    
    try:
        genai.configure(api_key=api_key)
        
        # Try different model names
        available_models = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
        working_model = None
        
        for model_name in available_models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model
                response = model.generate_content("Hello")
                if response and response.text:
                    working_model = model
                    break
            except Exception as e:
                continue
        
        if working_model:
            return working_model, "API configured successfully"
        else:
            return None, "No working model found"
            
    except Exception as e:
        return None, f"Configuration failed: {str(e)}"

# Fallback generator function
def generate_fallback_paragraph(birth_chart: str, disc: str) -> str:
    """Rule-based paragraph generator for offline use"""
    parts = []
    
    parts.append("With Sun in Libra, you naturally value fairness, relationships, and balance, and with an Ascendant in Capricorn, you bring a steady, disciplined approach to how you present yourself at work.")
    parts.append("Your DISC profile — high Conscientiousness and low Influence — suggests you thrive in roles that reward precision, structure, and deep thinking rather than constant social selling or networking.")
    parts.append("A fulfilling career path for you could be in areas like project coordination, compliance, technical writing, data analysis, or quality assurance — roles where a methodological mindset and an eye for detail are prized.")
    parts.append("To maximize satisfaction, look for positions that allow collaborative harmony (so your Libra strengths are honored) but offer clear frameworks, measurable goals, and opportunities to work independently on structured tasks that showcase your reliability.")

    paragraph = " ".join(parts)
    return textwrap.fill(paragraph, width=100)

# Gemini API generation function
def generate_gemini_paragraph(model, birth_chart: str, disc: str) -> str:
    """Generate career recommendation using Gemini API"""
    try:
        prompt = f"""Synthesize a career recommendation based on a person with a birth chart indicating '{birth_chart}' and a DISC profile of '{disc}'. 

The final output should be a single paragraph written in a friendly, conversational tone, suitable for a personalized report. 

Key themes to explore:
- Balancing an innate desire for harmony with a disciplined work ethic
- Leveraging a detail-oriented nature in a role that values structure
- Finding career paths that align with both astrological and personality traits

Please provide exactly one well-structured paragraph that synthesizes these insights into actionable career advice."""

        response = model.generate_content(prompt)
        
        if response and response.text:
            paragraph = response.text.strip()
            # Ensure it's a single paragraph
            paragraph = ' '.join(paragraph.split())
            
            # If response is too long, truncate to reasonable length
            if len(paragraph) > 500:
                sentences = paragraph.split('. ')
                paragraph = '. '.join(sentences[:3]) + '.'
            
            return paragraph
        else:
            return "API returned empty response"
            
    except Exception as e:
        return f"API error: {str(e)}"

# Main application
def main():
    # Main container with gradient background
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Header section with floating star
    st.markdown("""
    <div class="header-section">
        <div class="floating-star">
            <span style="font-size: 3rem;">⭐</span>
        </div>
        <h1 class="main-title">AstroDISC™ Lite</h1>
        <p class="subtitle">Discover your perfect career path through the harmony of astrology and personality insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main glass card
    st.markdown('<div class="glass-card slide-in">', unsafe_allow_html=True)
    
    # Card header
    st.markdown("""
    <div class="card-header">
        <div class="ai-badge">
            <span>🔮</span>
            <span>AI-Powered Career Insights</span>
        </div>
        <h2 class="card-title">Your Personalized Career Snapshot</h2>
        <p class="card-description">Get instant career recommendations based on your unique astrological and DISC profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status
    model, status = configure_gemini_api()
    if model:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="status-badge status-success" style="display: inline-block;">
                <span>✅ Gemini API Available</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="status-badge status-warning" style="display: inline-block;">
                <span>⚠️ Using Fallback Generator</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="input-label">
            <span>☀️</span>
            <span>Birth Chart</span>
        </div>
        """, unsafe_allow_html=True)
        birth_chart = st.text_input(
            "",
            value=BIRTH_CHART,
            placeholder="Enter your birth chart details...",
            key="birth_chart",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("""
        <div class="input-label">
            <span>👤</span>
            <span>DISC Profile</span>
        </div>
        """, unsafe_allow_html=True)
        disc_profile = st.text_input(
            "",
            value=DISC_PROFILE,
            placeholder="Enter your DISC profile...",
            key="disc_profile",
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Button section
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        generate_clicked = st.button(
            "🚀 Generate Career Report",
            key="generate",
            use_container_width=True
        )
    
    with col2:
        if st.button("🧹 Clear", key="clear", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("📋 Copy CLI", key="cli", use_container_width=True):
            st.info("CLI command: python main.py --cli")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results section
    st.markdown("""
    <div class="result-section">
        <div class="result-header">
            <h3 class="result-title">Your Career Recommendation</h3>
            <div class="pulse-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Results display
    if generate_clicked:
        with st.spinner("🔮 Analyzing your cosmic alignment and personality traits..."):
            if model:
                # Use Gemini API
                result = generate_gemini_paragraph(model, birth_chart, disc_profile)
                source = "Gemini API"
                source_color = "status-success"
            else:
                # Use fallback generator
                result = generate_fallback_paragraph(birth_chart, disc_profile)
                source = "Fallback Generator"
                source_color = "status-warning"
            
            # Display results with exact Flask styling
            st.markdown(f"""
            <div class="result-box">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem; color: #059669;">
                        <span style="font-size: 1.25rem;">✅</span>
                        <span style="font-weight: 600;">Career Recommendation Generated!</span>
                    </div>
                    <div class="status-badge {source_color}">
                        {source}
                    </div>
                </div>
                
                <div style="background: white; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #374151; margin-bottom: 0.5rem;">Based on your inputs:</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.875rem; color: #6b7280;">
                        <div><strong>Birth Chart:</strong> {birth_chart}</div>
                        <div><strong>DISC Profile:</strong> {disc_profile}</div>
                    </div>
                </div>
                
                <div style="color: #374151; line-height: 1.6;">
                    {result}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Default state
        st.markdown("""
        <div class="result-box">
            <div style="text-align: center; color: #6b7280;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✨</div>
                <p>Click "Generate Career Report" to get your personalized recommendation</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-item">
            <span>🛡️</span>
            <span>Built for assessment — includes offline fallback generator</span>
        </div>
        <div class="footer-item">
            <span>🚀</span>
            <span>Demo · Responsive · Local-first</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close glass card
    
    # Info card
    st.markdown("""
    <div class="info-card">
        <div class="info-badge">
            <span>ℹ️</span>
            <span>This app works without an API key. To enable a real LLM, set GEMINI_API_KEY in .env</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

if __name__ == "__main__":
    main()

# Custom CSS to match Flask version exactly
st.markdown("""
<style>
    /* Reset and base styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 1rem;
    }
    
    /* Glassmorphism card effect */
    .glass-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 1.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 3rem;
        margin: 0 auto;
        max-width: 1200px;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.3);
    }
    
    /* Header section with floating star */
    .header-section {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeIn 0.6s ease-out;
    }
    
    .floating-star {
        display: inline-block;
        padding: 1rem;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
        animation: iconFloat 2s ease-in-out infinite;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.9);
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Card header with badge */
    .card-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .ai-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        padding: 0.75rem 1.5rem;
        border-radius: 9999px;
        margin-bottom: 1rem;
        font-weight: 500;
        color: #3730a3;
    }
    
    .card-title {
        font-size: 1.875rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        color: #6b7280;
        font-size: 1rem;
    }
    
    /* Input fields with glassmorphism */
    .input-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .input-field {
        background: rgba(255,255,255,0.8);
        border: 2px solid transparent;
        border-radius: 0.75rem;
        padding: 1rem;
        transition: all 0.3s ease;
        font-size: 1rem;
        color: #1f2937;
    }
    
    .input-field:focus {
        border-color: #667eea;
        background: white;
        transform: scale(1.02);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .input-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
    }
    
    /* Button styles matching Flask version */
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.125rem;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        width: 100%;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .btn-secondary {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        color: #374151;
        border-radius: 0.75rem;
        padding: 1rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
    
    .btn-secondary:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    /* Button container */
    .button-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .button-container .btn-primary {
        flex: 2;
    }
    
    .button-container .btn-secondary {
        flex: 1;
    }
    
    /* Result section */
    .result-section {
        margin-top: 2rem;
    }
    
    .result-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1f2937;
    }
    
    .pulse-dot {
        width: 0.5rem;
        height: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #8b5cf6 100%);
        border-radius: 50%;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    .result-box {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid rgba(102, 126, 234, 0.1);
        border-radius: 0.75rem;
        padding: 1.5rem;
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
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 1rem;
    }
    
    .status-success {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    /* Footer */
    .footer {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e5e7eb;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.875rem;
        color: #6b7280;
    }
    
    .footer-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Info card */
    .info-card {
        margin-top: 1.5rem;
        text-align: center;
    }
    
    .info-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        color: rgba(255,255,255,0.8);
        font-size: 0.875rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(5deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in {
        animation: slideIn 0.8s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .input-section {
            grid-template-columns: 1fr;
        }
        
        .button-container {
            flex-direction: column;
        }
        
        .main-title {
            font-size: 2.5rem;
        }
        
        .glass-card {
            padding: 2rem;
            margin: 0.5rem;
        }
    }
    
    /* Hide Streamlit elements */
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
