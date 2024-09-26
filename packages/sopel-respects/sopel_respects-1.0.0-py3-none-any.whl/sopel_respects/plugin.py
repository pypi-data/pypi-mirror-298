"""Press F to pay respects.

Originally released under The Unlicense by xnaas at
https://git.actionsack.com/xnaas/sopel-respects
"""
from sopel import plugin

@plugin.rule(r"^[F𝔽]$")
def pay_respects(bot, trigger):
	bot.action("pays respects")
