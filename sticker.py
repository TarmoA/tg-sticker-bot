# encoding: utf-8
from telegram import TelegramError

def upload(bot, userId, filePath):
    """Upload file and return it"""
    try:
        f = open(filePath, 'rb')
    except IOError as e:
        print(e)
        return None
    return bot.uploadStickerFile(userId, f)


def createSticker(bot, userId, filePath, setName='tt_bot_test', setTitle='TT_Test_Set', emoji='😎'):
    """Create a sticker, return file or None
        Will use sticker set given with setName, or create one if it does not exist
        Note sticker sets are bound to a specific user
        Adds the suffix _by_botname to the sticker set name
        This is required by the Telegram api
    """
    file = upload(bot, userId, filePath)
    if not file:
        return None
    name = setName + '_by_' + bot.username
    try:
        bot.getStickerSet(name)
        if bot.addStickerToSet(userId, name, file.file_id, emoji):
            return bot.getStickerSet(name).stickers[-1]
        else:
            return None
    except TelegramError:
        return createSet(bot, userId, filePath, setName, setTitle, emoji)


def createSet(bot, userId, filePath, setName, setTitle, emoji='😎'):
    """Create a sticker set"""
    file = upload(bot, userId, filePath)
    if not file:
        return None
    name = setName + '_by_' + bot.username
    print name
    try:
        if bot.createNewStickerSet(userId, name, setTitle, file.file_id, emoji):
            return bot.getStickerSet(name).stickers[-1]
        else:
            return None
    except TelegramError as e:
        print e
        return None
