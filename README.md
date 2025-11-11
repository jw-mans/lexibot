# LexiBot — Document Question Answering Telegram Bot

**LexiBot** is a Telegram bot that helps you interact with your documents using **YandexGPT**.  
You can upload a document (PDF, DOCX, RTF, MD, or TXT), ask questions about its content, and the bot will answer intelligently — keeping conversation context between your questions.

## Features

-  Uses **YandexGPT** for natural language understanding and answering questions
-  Supports multiple document formats:
    - PDF (.pdf)
    - Word (.doc, .docx)
    - Rich Text (.rtf)
    - Markdown / Text (.md, .txt)
-  Remembers chat history per user for contextual conversation
-  Fully containerized via Docker / Docker Compose
-  Built with **Aiogram** (async Telegram bot framework)

## How It Works
1) **User sends a document** to the bot.  
    The file is downloaded, parsed, and its text content is stored.

2) **User asks a question** about the document.  
The bot combines:
    - the extracted text,
    - previous conversation history,
    - and the new question,
    and sends it to **YandexGPT** via its API.

3) **Bot replies** with a generated answer and remembers the conversation for context.

## Installation and Setup
### 1) Clone the repository
```bash
git clone https://github.com/yourusername/lexibot.git
cd lexibot
```
### 2) Create a `.env` file
Inside `src/config/.env`, add your API keys and bot token:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
YANDEX_API_KEY=your_yandex_api_key
YANDEX_API_KEY_ID=your_yandex_key_id
YANDEX_API_MODEL_URI=your_yandex_model_uri
YANDEX_API_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
YANDEX_CLOUD_CATALOG_ID=your_yandex_cloud_catalog_id
```

### 3) *Option A*: Run locally
Install dependencies and run the bot:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.bot.route
```
### 4) *Option B*: Run with Docker
Build and start using Docker Compose:
```bash
docker compose up --build -d
```

This will: 
- Build the bot image from `Dockerfile`

- Mount `./storage` to persist user uploads
- Start the bot container

## Usage

Once the bot is running:

1) Open your bot on Telegram (using the bot username linked to your token).

2) Send `/start`.

3) Upload a file (PDF, DOCX, RTF, MD, or TXT).

4) Ask questions like:

    - “What is this document about?”
    - “Summarize the second section.”
    - “Who is mentioned as the main author?”

The bot will answer using the uploaded document’s content and remember the chat history for follow-up questions.

## Core Components
### Document Loader

Located in `src/core/loader/`, it automatically detects file type and extracts text:

- PDFReader — reads PDFs with PyPDF

- DocReader — parses Word (.docx) files

- RTFReader — converts RTF to plain text

- MDReader — decodes Markdown and text files

### YandexGPT Integration

Implemented in `src/core/llm/`:

- `client.py` — HTTP client for YandexGPT API

- `pipeline.py` — constructs messages and sends queries with document context and conversation history

### User and History Stores

`UserStore` — keeps uploaded document contents per user

`HistoryStore` — saves the chat message history for multi-turn dialogue

## Dependencies

**Main libraries:**
- `aiogram`
 — Telegram bot framework
- `httpx`
 — async HTTP client
- `pypdf`
 — PDF reader
- `python-docx`
 — DOCX parser
- `striprtf`
 — RTF to text
- `markdown`
 — Markdown parser
- `chardet`
 — encoding detection
- `pydantic-settings`
 — environment-based configuration

## Roadmap

Planned improvements and future development goals:

- Implement document **chunking and embedding** for handling large files efficiently  
- Redesign document structure and **improve internal markup parsing**  
- Develop **new storage mechanisms** for user documents  
- Build a robust **user session management system**  
- Enable **multi-file document handling** and cross-file queries  
- Add **LaTeX parsing support** for scientific and mathematical documents  
- Integrate **additional language models** (beyond YandexGPT)  
- Create a **generation pipeline via LangChain** for modular, extensible response generation


 ## Author

**LexiBot** was developed to make document understanding conversational.
Built by **[jw-mans (Daniel Jermakiw)](https://github.com/jw-mans/)**  using Python, Aiogram, and YandexGPT.
