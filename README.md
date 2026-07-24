# AI-Chatbot
AI Chatbot developed using FastAPI, Streamlit, Gemini API, SQLite, and PDF Question Answering.

## Netlify Deployment
This repository is configured for Netlify deployment using the `landing` frontend app.

- Build command: `npm install && npm run build`
- Publish directory: `landing/dist`
- Base directory: `landing`

### Deploy steps
1. Create a new Netlify site.
2. Connect the repository.
3. Use the default `main` branch.
4. Set the build command to `npm install && npm run build`.
5. Set the publish directory to `landing/dist`.
6. Optionally define environment variables in Netlify if you need to override `VITE_APP_URL` or `VITE_API_URL`.

### Local build
```bash
cd landing
npm install
npm run build
```
