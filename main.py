from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, json, os, sys
import resize
import sticker as stickerModule
import drawText

BASE_FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + "/tmp/{}_{}.jpg"
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Send me a picture in a private message to add it to a sticker pack. Add a caption to draw it on the sticker. Start the caption with hyphen - to insert text to the bottom')



def handlePhoto(bot, update):
    """Handle a photo sent in by user"""
    message = update.message
    user = update.effective_user
    if message.photo and len(message.photo):
        # get full size photo
        photoObj = message.photo[-1]
        chatId = message.chat_id
        messageId = message.message_id
        filePath = BASE_FILE_PATH.format(chatId, messageId)
        file = bot.get_file(photoObj.file_id)
        file.download(filePath)
        imgPath = resize.resize(filePath)
        #add caption
        if message.caption and len(message.caption) < 50:
            imgPath = drawText.draw(imgPath, message.caption.strip())
        sticker = stickerModule.createSticker(bot, user.id, imgPath)
        if sticker:
            update.message.reply_sticker(sticker.file_id)
        else:
            update.message.reply_text('error2')
        #remove tmp files
        os.remove(filePath)
        os.remove(filePath.split('.')[0] + '_r.png')

    else:
        update.message.reply_text('error')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    if 'HEROKU' in os.environ:
        key = os.environ['BOT_KEY']
    else:
        key = json.loads(open("key.json").read())['key']

    updater = Updater(key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("addSticker", addSticker))
    dp.add_handler(MessageHandler(Filters.photo & Filters.private, handlePhoto))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
