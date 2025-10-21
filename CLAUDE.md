# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Web-based Terminal Application** - a Flask web application that provides a browser-accessible shell interface. Users can execute shell commands through a web UI and view real-time streaming output. The application is designed for deployment on Hugging Face Spaces.

## Technology Stack

- **Backend**: Flask 3.0.3 (Python 3.10)
- **Frontend**: Single HTML page with vanilla JavaScript + Tailwind CSS (CDN)
- **Communication**: Server-Sent Events (SSE) for real-time command output streaming
- **Deployment**: Docker containers on Hugging Face Spaces
- **CI/CD**: GitHub Actions auto-deploys to Hugging Face on pushes to main

## Development Commands

### Running the Application

**Local development (direct):**
```bash
python src/app.py
```
The app runs on `http://localhost:7860` (Hugging Face default port).

**Docker development:**
```bash
docker build -t terminal-web .
docker run -p 7860:7860 terminal-web
```

### Testing

Manual testing script available:
```bash
python testing.py
```
This sends a test command to the `/exec` endpoint and streams the response.

No formal test suite exists currently.

## Architecture

### Application Structure

```
src/app.py              # Main Flask application (86 lines)
src/templates/terminal.html  # Single-page UI with embedded JavaScript
Dockerfile              # Container definition with system packages
requirements.txt        # Python dependencies
packages.txt           # System packages (ffmpeg, handbrake-cli, etc.)
.github/workflows/main.yml  # Auto-deploy to Hugging Face Spaces
```

### Key Components

**Backend (src/app.py):**
- `execute_command(command, pwd)` - Executes shell commands via subprocess and yields streaming output
- Route `/` - Renders terminal UI with initial `uname -a` output
- Route `/exec` - Command execution endpoint returning SSE stream
- Route `/ping` - Health check endpoint (204 response)

**Frontend (src/templates/terminal.html):**
- Terminal UI with command input and history display
- JavaScript EventSource client consuming SSE stream
- Working directory state management (pwd tracked client-side)
- ANSI color code stripping for clean display

### Architecture Patterns

1. **Server-Sent Events for Streaming**: Uses EventSource (SSE) instead of WebSockets for unidirectional server-to-client streaming. Output is buffered for 0.3 seconds before sending to reduce message overhead.

2. **Stateful Session Management**: Current working directory (pwd) is tracked client-side and sent with each command to maintain session context across requests.

3. **Special Command Handling**: The `cd` command is detected and handled specially - it executes `cd && pwd` to capture the new directory and update client state.

4. **Security Model**: All commands execute server-side with full shell access. The Dockerfile sets permissive permissions (`chmod 777`) on directories.

## System Dependencies

The application includes media processing tools installed via `packages.txt`:
- ffmpeg, handbrake-cli, mencoder - Video/audio processing
- mkvtoolnix - Matroska video tools
- libsm6, libxext6 - X11 libraries
- net-tools - Network utilities
- unrar-free - Archive extraction

## Deployment

**Automatic Deployment:**
- Pushes to `main` branch trigger GitHub Actions workflow
- Code syncs to Hugging Face Space: `dakunesu/terminal`
- Uses `nateraw/huggingface-sync-action` to sync `hugging/` subdirectory
- Requires `HF_TOKEN` secret configured in GitHub repository

**Docker Container:**
- Base image: Python 3.10
- Working directory: `/app`
- Startup command: `python src/app.py`
- Initial working directory for terminal: `/root`
- README.txt copied to `/root` for display on first run

## Important Implementation Details

1. **Output Buffering**: Command output accumulates for 0.3 seconds before streaming to reduce overhead (see src/app.py:38-41)

2. **Directory Change Detection**: Commands starting with `cd` (without `&&`) trigger special handling to capture and return the new pwd (see src/app.py:26-31)

3. **Completion Signal**: Streaming ends with `[DONE]` marker in the output (see src/app.py:49)

4. **Error Handling**: Subprocess errors are captured and streamed as regular output via `stderr=subprocess.STDOUT`

5. **Initial State**: The terminal loads with `uname -a` pre-executed to show system information (see src/app.py:57-60)

## Git Commit Convention

Always use scoped commits following the format:
```
scope(component): description
```

Examples:
- `feat(api): add command timeout support`
- `fix(ui): resolve terminal scroll behavior`
- `docs(readme): update deployment instructions`
