# Free Deployment Guide for Pharmaceutical Quiz App

## Streamlit Community Cloud (Recommended - 100% Free)

### Prerequisites
- GitHub account (free)
- Public repository

### Steps:
1. **Create GitHub Repository**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name: `pharmaceutical-quiz`
   - Make it **Public** (required for free tier)
   - Initialize with README

2. **Upload Your Files**
   - Click "uploading an existing file"
   - Drag and drop all files from your `pharmaceutical_quiz` folder
   - Commit changes

3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `streamlit_main.py`
   - Click "Deploy!"

4. **Add Environment Variables**
   - In Streamlit Cloud dashboard
   - Go to "Secrets" section
   - Add:
     ```toml
     ANTHROPIC_API_KEY = "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"
     ```

## Alternative: Render.com (Also Free)

### Steps:
1. Go to [render.com](https://render.com)
2. Create account
3. Click "New Web Service"
4. Connect GitHub or upload ZIP
5. Select "Python" environment
6. Build command: `pip install -r requirements.txt`
7. Start command: `streamlit run streamlit_main.py --server.port $PORT`
8. Add environment variable `ANTHROPIC_API_KEY`

## Files Ready for Upload
All necessary files are in your project folder:
- `streamlit_main.py` (main app)
- `requirements.txt` (dependencies)
- `.gitignore` (security)
- All supporting modules

Your app will be accessible at a free URL like:
- Streamlit Cloud: `https://yourapp.streamlit.app`
- Render: `https://yourapp.onrender.com`
