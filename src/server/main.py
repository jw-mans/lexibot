import threading
import uvicorn
from .connections import app, launch_gradio, run_telegram_polling
from ..logger import logger

def start_background_services():
    logger.info("Starting background services...")

    tg_thread = threading.Thread(
        target=lambda: run_telegram_polling(),
        daemon=True,
        name="TelegramPollingThread"
    )
    tg_thread.start()
    logger.info("Telegram polling thread started.")

    gradio_thread = threading.Thread(
        target=lambda: launch_gradio(share=False),
        daemon=True,
        name="GradioThread"
    )
    gradio_thread.start()
    logger.info("Gradio thread started.")

def main():
    logger.info("Starting server main()...")

    start_background_services()

    logger.info("Launching FastAPI (uvicorn) on 0.0.0.0:8000")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    main()
