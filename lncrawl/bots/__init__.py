supported_bots = [
    "console",
    "telegram",
    "discord",
    "lookup",
    "web_server",
]


def run_bot(bot):
    if bot not in supported_bots:
        bot = "console"

    if bot == "console":
        from ..bots.console import ConsoleBot

        ConsoleBot().start()
    elif bot == "telegram":
        from ..bots.telegram import TelegramBot

        TelegramBot().start()
    elif bot == "discord":
        from ..bots.discord import DiscordBot

        DiscordBot().start_bot()
    elif bot == "lookup":
        from ..bots.lookup import LookupBot

        LookupBot().start()
    elif bot == "web_server":
        from ..bots.web_server import run_server

        run_server()
    else:
        print("Unknown bot: %s" % bot)
