install-deps:
	echo TODO

install:
	install -d /opt/tg_sticker_bot/tmp
	install main.py /opt/tg_sticker_bot/main.py
	install resize.py /opt/tg_sticker_bot/resize.py
	install sticker.py /opt/tg_sticker_bot/sticker.py
	install drawText.py /opt/tg_sticker_bot/drawText.py
	install impact.otf /opt/tg_sticker_bot/impact.otf
	install key.json /opt/tg_sticker_bot/key.json
	install start.sh /opt/tg_sticker_bot/start.sh
	cp -r .env /opt/tg_sticker_bot/
	install systemd/tg_sticker_bot.service /etc/systemd/system/tg_sticker_bot.service
