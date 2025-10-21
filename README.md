# Terminal Web

A web-based terminal application that provides a browser-accessible shell interface.

## Features

- Execute shell commands through a web interface
- Real-time streaming output
- Working directory state management
- Pre-installed media processing tools

## Technology Stack

- Backend: Flask 3.0.3 (Python 3.10)
- Frontend: HTML + JavaScript + Tailwind CSS
- Communication: Server-Sent Events (SSE)
- Deployment: Docker on Hugging Face Spaces

## Running Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

The application runs on `http://localhost:7860`

## Docker

```bash
docker build -t terminal-web .
docker run -p 7860:7860 terminal-web
```

## Deployment

Automatic deployment to Hugging Face Spaces via GitHub Actions on push to main branch.

Required GitHub Actions secrets:
- `HF_TOKEN` - Hugging Face access token
- `HF_SPACE` - Hugging Face Space name (format: `username/space-name`)

## License

MIT
