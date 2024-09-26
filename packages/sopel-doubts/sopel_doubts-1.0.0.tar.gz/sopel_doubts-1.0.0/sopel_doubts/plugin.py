"""Press X to doubt.

Originally released under The Unlicense by xnaas at
https://git.actionsack.com/xnaas/sopel-doubts
"""
from sopel import plugin

@plugin.rule(r"^[XⓍ𝕏]$")
def x_to_doubt(bot, trigger):
	bot.action("doubts")
