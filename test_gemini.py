#!/usr/bin/env python3
"""
Simple test script to diagnose Gemini API issues
Run this to test your API key and see what models are available
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_api():
    """Test Gemini API connection and list available models"""
    print("🔍 Testing Gemini API Connection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No GEMINI_API_KEY found in environment variables")
        print("💡 Create a .env file with: GEMINI_API_KEY=your_key_here")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        print("✅ API configuration successful")
        
        # Test API connection by listing models
        print("\n📋 Testing API connection...")
        models = list(genai.list_models())  # Convert generator to list
        print(f"✅ API connection successful! Found {len(models)} models")
        
        # List available models
        print("\n📋 Available Models:")
        print("-" * 50)
        
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model)
                print(f"✅ {model.name}")
                if hasattr(model, 'description') and model.description:
                    print(f"   Description: {model.description}")
                print(f"   Methods: {', '.join(model.supported_generation_methods)}")
            else:
                print(f"❌ {model.name} (no generateContent support)")
            print()
        
        if not available_models:
            print("❌ No models found that support generateContent")
            return False
        
        # Test a specific model
        print("🧪 Testing model generation...")
        test_models = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro']
        
        working_model = None
        for model_name in test_models:
            try:
                print(f"🔍 Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, this is a test.")
                
                if response and response.text:
                    print(f"✅ {model_name} working! Response: {response.text[:50]}...")
                    working_model = model_name
                    break
                else:
                    print(f"⚠️  {model_name} returned empty response")
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
                continue
        
        if working_model:
            print(f"\n🎯 Success! {working_model} is working correctly")
            return True
        else:
            print("\n❌ No working models found")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print(f"💡 Error type: {type(e).__name__}")
        
        # Provide specific error guidance
        if "404" in str(e):
            print("💡 404 error suggests model not found or API version mismatch")
        elif "403" in str(e):
            print("💡 403 error suggests API key permission issues")
        elif "401" in str(e):
            print("💡 401 error suggests invalid API key")
        elif "quota" in str(e).lower():
            print("💡 Quota exceeded - check your API usage limits")
        
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Gemini API is working correctly!")
        print("💡 You can now run your main application")
    else:
        print("❌ Gemini API test failed")
        print("💡 Check your API key and try again")
        print("💡 Make sure you have the latest google-generativeai library")
