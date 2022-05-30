"""System module."""
from lib.bot import Bot

bot = Bot()
try:
    bot.run()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        bot.leave()
        sys.exit(0)
    except SystemExit:
        os._exit(0)
