import logging
import EpicCodersContestWatcher
from botTelegramKey import TKN
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# For now, I only want to deal with commands.		#
# I'm not importing this stuff, but I might			#
# need it in the future:							#
# 													#
# from telegram.ext import MessageHandler, Filters  #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

helloPhrase = "Projeto EPIC CODERS (Universidade Federal de Itajubá) - Maratona de Programação\nDigite /comandos para ver a lista de comandos"

helpPhrase = "Comandos disponíveis:\n/contest\n"
groupLink = '<a href="https://codeforces.com/group/OGY9gSUQWd/">Grupo no Codeforces</a>'


def getActiveText():
	
	activeContestList = EpicCodersContestWatcher.activeContests()
	
	if len(activeContestList) == 0:
		return "Não há contests ativos no momento.\n\n"
	
	if activeContestList[0] == "error":
		return activeContestList[1]
	
	answerContent = ""
	
	for contestName in activeContestList:
		answerContent += contestName
		answerContent += "\n"
	
	return answerContent



def getUpcomingText():
	
	upcomingContestList = EpicCodersContestWatcher.upcomingContests()
	
	if len(upcomingContestList) == 0:
		return "Não há contests em breve.\n"
	
	if upcomingContestList[0] == "error":
		return upcomingContestList[1]
	
	answerContent = "Em breve:\n"
	
	for contestName in upcomingContestList:
		answerContent += contestName
		answerContent += "\n"
	
	return answerContent



def startMessage(update, context):
	context.bot.send_message(
		chat_id=update.effective_chat.id, text=helloPhrase)
	return



def contestMessage(update, context):
	context.bot.send_message(
		chat_id=update.effective_chat.id, text=getActiveText() + getUpcomingText())
	return



def commandsMessage(update, context):
	context.bot.send_message(
		chat_id=update.effective_chat.id, text=helpPhrase)
	return



def groupLinkMessage(update, context):
	context.bot.send_message(
		chat_id=update.effective_chat.id, text=groupLink, parse_mode=ParseMode.HTML)
	return



updater = Updater(token=TKN, use_context=True)
dispatcher = updater.dispatcher

# some exceptions are only caught by this
logging.basicConfig(
	format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level = logging.INFO)

startHandler = CommandHandler('start', startMessage)
contestHandler = CommandHandler('contest', contestMessage)
helpHandler = CommandHandler('comandos', commandsMessage)
groupLinkHandler = CommandHandler('grupo', groupLinkMessage)

dispatcher.add_handler(startHandler)
dispatcher.add_handler(contestHandler)
dispatcher.add_handler(helpHandler)
dispatcher.add_handler(groupLinkHandler)

updater.start_polling()

updater.idle()
# properly handles Ctrl + C
