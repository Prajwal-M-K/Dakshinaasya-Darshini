# Dakshinaasya Darshini (Next.js)

A sleek Next.js front-end for the Dakshinaasya Darshini demo with inline mode selector and mic-to-text input.

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

The server reads `../Dakshina_Murthi_Context.txt` at runtime, so keep that file in the repo root.

## Build & deploy

- Production build: `npm run build` then `npm start`.
- Vercel: set `GEMINI_API_KEY` as an env var; the API route works server-side only.

## Notes

- Mic uses the Web Speech API (Chrome recommended). If unavailable, type instead.
- Modes: ⚡ Quick help, 🌿 Balanced, 📿 Deep study map to the same instructions as the Streamlit version.
