import os

from padde.bot import Padde

if __name__ == "__main__":
    bot = Padde()
    if os.name != "nt":
        import uvloop

        uvloop.install()

bot.run()
