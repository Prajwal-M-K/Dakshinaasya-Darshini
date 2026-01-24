# Dakshinaasya Darshini - Deployment Guide

## Project Overview

This repository contains two versions of the Dakshinaasya Darshini application:
1. **Streamlit app** (app.py) - Python-based version
2. **Next.js app** (frontend/) - Modern web application

For Vercel deployment, use the **Next.js version** in the `frontend/` directory.

## Vercel Deployment Instructions

### Prerequisites
- A Vercel account (free tier works fine)
- A Google Gemini API key
- Your code in a Git repository (GitHub, GitLab, or Bitbucket)

### Step-by-Step Deployment

1. **Push your code to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com
   - Click "Add New" → "Project"
   - Import your Git repository
   - Select the repository

3. **Configure the project**
   - **Root Directory**: Set to `frontend`
   - **Framework Preset**: Next.js (should auto-detect)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

4. **Set Environment Variables**
   - Click "Environment Variables"
   - Add variable:
     - Name: `GEMINI_API_KEY`
     - Value: Your Google Gemini API key
   - Apply to all environments (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (usually 2-3 minutes)
   - Your app will be live at `https://your-project-name.vercel.app`

### Post-Deployment

- **Custom Domain**: You can add a custom domain in Vercel project settings
- **Automatic Deployments**: Every push to your main branch will trigger a new deployment
- **Preview Deployments**: Pull requests automatically get preview deployments

### Important Files

- `frontend/Dakshina_Murthi_Context.txt` - Required context file for the AI
- `frontend/.env.local` - Local environment variables (not committed to Git)
- `frontend/vercel.json` - Vercel configuration
- `frontend/.gitignore` - Ensures sensitive files aren't committed

### Troubleshooting

**Build fails:**
- Check that all dependencies are in package.json
- Verify Node.js version compatibility
- Check build logs in Vercel dashboard

**API errors:**
- Verify `GEMINI_API_KEY` is set in Vercel environment variables
- Check API key has necessary permissions
- Review function logs in Vercel dashboard

**Context file not found:**
- Ensure `Dakshina_Murthi_Context.txt` is in the `frontend/` directory
- Verify file is committed to Git

### Local Development

```bash
cd frontend
npm install
# Create .env.local with GEMINI_API_KEY=your_key_here
npm run dev
```

Visit http://localhost:3000

## Features

- **Three Response Modes:**
  - Quick help: Concise, actionable advice (2-3 sentences)
  - Balanced: Practical guidance with spiritual context (4-6 sentences)
  - Deep study: Philosophical depth with sloka citations

- **Voice Input:** Uses Web Speech API (Chrome recommended)
- **Real-time Streaming:** Responses appear as they're generated
- **Mobile Responsive:** Works on all device sizes

## Tech Stack

- **Frontend:** Next.js 15, React 18, TypeScript
- **Styling:** Custom CSS with spiritual design theme
- **AI:** Google Gemini 2.5 Flash
- **Deployment:** Vercel (serverless)

## Security Notes

- API key is stored as environment variable (never in code)
- API route runs server-side only (key never exposed to browser)
- Context file is read server-side
- .env files are gitignored

---

For questions or issues, refer to the frontend/README.md or check the Vercel documentation.
