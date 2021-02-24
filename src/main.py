# encoding: utf-8
import asyncio
import logging, json, os, sys, re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import emoji
import resize
import sticker as stickerModule
import drawText

BASE_FILE_PATH = "../tmp/{}_{}.jpg"
DEFAULT_EMOJI = '😎'
HARCODED_USER_ID_TODO_REPLACE = os.environ['USER_ID']
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    text = """Send me an image to add to a sticker pack. A new pack is created for each user or group if it does not exist. Add a text caption to draw it on the sticker. If the bot is used in a group, the caption should start with "/sticker".

If the first character of image caption is an emoji, it will be used as the chosen emoji for the sticker. Start text portion of caption with a "-" to write on the bottom of image instead of top.

Example of caption:
/sticker 🆘 -BOTTOM TEXT
    """
    update.message.reply_text(text)

# return file path
def getImageFromImageMessage(update, context):
    message = update.message
    photoObj = message.photo[-1]
    filePath = BASE_FILE_PATH.format(message.chat_id, message.message_id)
    file = context.bot.get_file(photoObj.file_id)
    file.download(filePath)
    return filePath


def handlePhoto(update, context, isGroup):
    """Handle a photo sent in by user"""
    message = update.message
    user = update.effective_user
    usableCaption = message.caption or ''
    if len(usableCaption):
        usableCaption = usableCaption.strip()
    if (isGroup):
        if not usableCaption or not len(usableCaption) >= 8 or not usableCaption[:8] == '/sticker':
            return
        usableCaption = message.caption[8:].strip()
        setName = 'set_' + str(update.effective_chat.id).replace('-', 'm')
        setTitle = update.effective_chat.title + ' pack'
        setOwnerId = HARCODED_USER_ID_TODO_REPLACE
        member = context.bot.getChatMember(update.effective_chat.id, setOwnerId)
        if member.status not in ["member", "creator", "administrator"]:
            return
    else:
        setName = 'set_' + str(user.id).replace('-', 'm')
        setTitle = user.first_name + ' pack'
        setOwnerId = user.id

    if len(usableCaption) > 50:
        return update.message.reply_text('caption too long (max 50)')
    if message.photo and len(message.photo):
        # get full size photo
        filePath = getImageFromImageMessage(update, context)
        imgPath = resize.resize(filePath)
        stickerEmoji = DEFAULT_EMOJI
        if usableCaption and emoji.emoji_count(usableCaption[0]) == 1:

            stickerEmoji = usableCaption[0]
            usableCaption = usableCaption[1:].strip()
        #add caption
        if usableCaption:
            drawOnBottom = len(usableCaption) > 1 and usableCaption[0] == '-'
            if (drawOnBottom):
                usableCaption = usableCaption[1:].strip()
            imgPath = drawText.draw(imgPath, usableCaption, drawOnBottom)

        sticker = stickerModule.createSticker(context.bot, setOwnerId, imgPath, setName, setTitle, stickerEmoji)
        if sticker:
            update.message.reply_sticker(sticker.file_id)
        else:
            update.message.reply_text('error creating sticker')
        #remove tmp files
        os.remove(filePath)
        os.remove(filePath.split('.')[0] + '_r.png')

    else:
        update.message.reply_text('error')

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    token = os.environ.get('TOKEN')
    if not token:
        return

    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("addSticker", addSticker))
    dp.add_handler(MessageHandler(Filters.photo & Filters.private, lambda a, b: handlePhoto(a, b, False)))
    dp.add_handler(MessageHandler(Filters.photo & Filters.group, lambda a, b: handlePhoto(a, b, True)))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
