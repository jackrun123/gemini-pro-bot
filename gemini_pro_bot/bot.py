import logging
import os
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Application,
)
from gemini_pro_bot.filters import AuthFilter, MessageFilter, PhotoFilter
from dotenv import load_dotenv
from gemini_pro_bot.handlers import (
    post_init,
    start,
    help_command,
    newchat_command,
    handle_message,
    handle_image,
)

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.WARN)


def start_bot() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("BOT_TOKEN"))\
        .post_init(post_init)\
        .build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start, filters=AuthFilter))
    application.add_handler(CommandHandler("help", help_command, filters=AuthFilter))
    application.add_handler(CommandHandler("new", newchat_command, filters=AuthFilter))

    # Any text message is sent to LLM to generate a response
    application.add_handler(MessageHandler(MessageFilter, handle_message))

    # Any image is sent to LLM to generate a response
    application.add_handler(MessageHandler(PhotoFilter, handle_image))

    logger.warn("started")
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

