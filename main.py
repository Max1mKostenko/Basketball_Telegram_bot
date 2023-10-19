from telegram.ext import MessageHandler, ConversationHandler, CommandHandler, Updater, Filters
from telegram.ext import CallbackQueryHandler

from database.database import engine
from models.model import Base
from view.view import (start, help_, add_info, name_handler, surname_handler, finish_handler,manage_text, cancel_handler,
                  show_info, del_info, show_favourite_team_info, video_of_team, NAME, SURNAME, TEAM)

BOT_TOKEN = "6315814690:AAHxZe71KXEbRfFjYJAW2r0UCGjrKNb9kuM"

if __name__ == '__main__':
    # Create the Updater
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # creating db
    Base.metadata.create_all(engine)

    # act on different commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_))

    # handling the conversation btw user and bot
    personal_data_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_or_update_info', add_info)],
        states={
            NAME: [MessageHandler(Filters.text & (~Filters.command), name_handler, pass_user_data=True)],
            SURNAME: [MessageHandler(Filters.text & (~Filters.command), surname_handler, pass_user_data=True)],
            TEAM: [MessageHandler(Filters.text & (~Filters.command), finish_handler, pass_user_data=True)],
        },
        fallbacks=[MessageHandler(Filters.command, cancel_handler), CommandHandler('cancel', cancel_handler),
                   CallbackQueryHandler(cancel_handler, pattern='cancel'),
                   CommandHandler('start', start)],
    )

    # SQL database
    # handlers which are working with db
    dp.add_handler(personal_data_conv_handler)
    dp.add_handler(CommandHandler('add_info', add_info))
    dp.add_handler(CommandHandler('show_info', show_info))
    dp.add_handler(CommandHandler('del_info', del_info))
    dp.add_handler(CommandHandler('show_team_info', show_favourite_team_info))
    dp.add_handler(CommandHandler('video_of_team', video_of_team))
    # message to an unknown command
    dp.add_handler(MessageHandler(Filters.text, manage_text))

    # Start the Bot
    updater.start_polling()
