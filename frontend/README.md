# Dakshinaasya Darshini

## About

Dakshinaasya Darshini is an AI-powered spiritual guide grounded in the teachings of the Dakshinamurthy Ashtakam, as conveyed through the upanyasas (discourses) of His Holiness Sri Shankara Bharati Mahaswaminaha. The application serves as a conversational companion that helps users navigate real-life challenges through the lens of Advaita Vedanta philosophy.

The name "Dakshinaasya Darshini" translates to "one who reveals the south-facing one" — a reference to Lord Dakshinamurthy, the aspect of Shiva as the supreme teacher who imparts wisdom through silence. This application embodies that spirit by offering thoughtful, practical guidance rooted in ancient wisdom but delivered in accessible, modern language.

Key capabilities include:

- Three response modes: Quickfire (concise answers), Default (balanced guidance), and Deep Dive (comprehensive philosophical exploration)
- Bilingual support for English and Kannada
- Voice input via Web Speech API for hands-free interaction
- Text-to-speech for listening to responses
- Conversation export for personal reference

The frontend is built with Next.js and communicates with the Gemini API to generate contextually aware responses based on the teachings provided in the knowledge base.

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
- Modes: Quickfire, Default, and Deep Dive provide progressively detailed responses based on user needs.
