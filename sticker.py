from telegram import TelegramError

def upload(bot, userId, filePath):
    """Upload file and return it"""
    try:
        f = open(filePath, 'rb')
    except IOError as e:
        print(e)
        return None
    return bot.uploadStickerFile(userId, f)


def createSticker(bot, userId, filePath, setName='tt_bot_test'):
    """Create a sticker, return file or None"""
    file = upload(bot, userId, filePath)
    if not file:
        return None
    name = setName + '_by_' + bot.username
    try:
        bot.getStickerSet(name)
        if bot.addStickerToSet(userId, name, file.file_id, '😎'):
            return bot.getStickerSet(name).stickers[-1]
        else:
            return None
    except TelegramError:
        createSet(bot, userId, filePath, setName)



def createSet(bot, userId, filePath, setName='tt_bot_test'):
    """Create a sticker set"""
    file = upload(bot, userId, filePath)
    title = 'TT_Test_Set'
    if not file:
        return None
    name = setName + '_by_' + bot.username
    if bot.createNewStickerSet(userId, name, title, file.file_id, '😎'):
        return bot.getStickerSet(name).stickers[-1]
    else:
        return None
