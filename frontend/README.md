# Dakshinaasya Darshini (Next.js)

A sleek Next.js front-end for the Dakshinaasya Darshini demo with inline mode selector and voice-to-text input.

## Quick start

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000.

## Environment

Create `.env.local` in `frontend/`:

```
GEMINI_API_KEY=your_key_here
```

The server reads `Dakshina_Murthi_Context.txt` from the frontend directory at runtime.

## Build & deploy

### Local production build
```bash
npm run build
npm start
```

### Vercel deployment
1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Import the project in Vercel
3. Set the root directory to `frontend`
4. Add the environment variable `GEMINI_API_KEY` in Vercel project settings
5. Deploy

The API route works server-side only, so the API key is secure.

## Notes

- Voice input uses the Web Speech API (Chrome recommended). If unavailable, use text input instead.
- Modes: Quick help, Balanced, Deep study map to the same instructions as the Streamlit version.
