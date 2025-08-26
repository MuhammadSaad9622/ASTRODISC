# Gemini API Troubleshooting Guide

## Error: "404 models/gemini-pro is not found for API version v1beta"

This error occurs when there's a mismatch between your Google Generative AI library version and the current Gemini API.

## Quick Fix

1. **Update your dependencies:**
   ```bash
   pip install --upgrade google-generativeai python-dotenv
   ```

2. **Test your API connection:**
   ```bash
   python test_gemini.py
   ```

## Detailed Steps

### 1. Check Your Current Setup
```bash
pip show google-generativeai
```

**Expected:** Version 0.8.0 or higher
**If lower:** Update using the command above

### 2. Verify Your API Key
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key if needed
- Copy it to your `.env` file:
  ```
  GEMINI_API_KEY=your_actual_api_key_here
  ```

### 3. Test API Connection
Run the test script to diagnose issues:
```bash
python test_gemini.py
```

This will:
- Test your API key
- List available models
- Test model generation
- Provide specific error guidance

### 4. Common Issues & Solutions

#### Issue: "404 models/gemini-pro not found"
**Cause:** Using an outdated library version
**Solution:** Update to google-generativeai >= 0.8.0

#### Issue: "403 Forbidden"
**Cause:** API key permissions or quota issues
**Solution:** Check API key permissions and usage limits

#### Issue: "401 Unauthorized"
**Cause:** Invalid or expired API key
**Solution:** Generate a new API key

#### Issue: "Quota exceeded"
**Cause:** API usage limits reached
**Solution:** Check your Google Cloud billing and quotas

### 5. Model Names
The current API supports these models:
- `gemini-1.5-pro` (recommended)
- `gemini-1.5-flash`
- `gemini-1.0-pro`
- `gemini-pro`

### 6. Fallback Mode
If the Gemini API fails, your app will automatically use the built-in fallback generator, so it will still work offline.

## Still Having Issues?

1. **Check the test script output** for specific error messages
2. **Verify your API key** is correct and active
3. **Check your Google Cloud project** has Gemini API enabled
4. **Ensure you're not behind a restrictive firewall** or proxy

## Support
- [Google AI Studio Documentation](https://ai.google.dev/docs)
- [Google Generative AI Python Library](https://github.com/google/generative-ai-python)
- [API Status Page](https://status.ai.google.dev/)
