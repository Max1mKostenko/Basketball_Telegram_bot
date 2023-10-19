import urllib.request
from random import randrange
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler
from database.database import Session
from models.model import User

from utils.get_nba_api import show_team_info
from utils.save_logs import log_decorator
from utils.get_nba_news import get_nba_news

# states for conversation handler (see below)
NAME, SURNAME, TEAM = range(3)


@log_decorator
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi, {update.effective_user.first_name}.\n"
                                  f"This is your news nba bot.\n"
                                  f"I'll notify you about the hottest news from nba!\n"
                                  f"Press /help for more info.")
    sticker = open('static/' + 'sticker.webp', 'rb')
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)
    return ConversationHandler.END


@log_decorator
def help_(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="\n📝 Things you can manage 📝\n"
                                  "- /add_or_update_info: to add/update personal info to the database.\n\n"
                                  "- /show_info: to show info about yourself.\n\n"
                                  "- /del_info: to delete info about yourself.\n\n"
                                  "- /show_team_info: to show info about your favourite team.\n\n"
                                  "- /video_of_team: to show video of favourite team.\n\n"
                                  "- /news_of_team: to show news about your favourite team.")

    return ConversationHandler.END


@log_decorator
def show_info(update: Update, context: CallbackContext):
    # get user's telegram id
    user = update.message.from_user.id

    # opening db session
    session = Session()

    # looking for user in db by id
    database_user = session.query(User).filter(User.telegram_id == user).first()

    if database_user:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"📄 Your info. 📄\n"
                                      f"✔ Name: {database_user.username}.\n"
                                      f"✔ Surname: {database_user.surname}.\n"
                                      f"✔ Favourite Team: {database_user.team}.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="✖ You don't exist in the database.")
    # closing dp session
    session.close()


@log_decorator
def del_info(update: Update, context: CallbackContext):
    # get user's telegram id
    user = update.message.from_user.id

    # opening db session
    session = Session()

    # looking for user in db by id
    database_user = session.query(User).filter(User.telegram_id == user).first()

    if database_user:
        session.query(User).filter(User.telegram_id == user).delete()
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='✔All your info successfully deleted!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="✖ You don't exist in the database")
    # closing dp session
    session.close()


@log_decorator
def show_favourite_team_info(update: Update, context: CallbackContext):
    user = update.message.from_user.id

    session = Session()

    database_user = session.query(User).filter(User.telegram_id == user).first()

    if database_user:
        fav_team = database_user.team
        data_of_team = show_team_info(fav_team)
        if data_of_team:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"📄 Info about your favourite team. 📄\n"
                                          f"✔ Abbreviation: {data_of_team['abbreviation']}.\n"
                                          f"✔ City: {data_of_team['city']}.\n"
                                          f"✔ Conference: {data_of_team['conference']}.\n"
                                          f"✔ Division: {data_of_team['division']}.\n"
                                          f"✔ Full Name: {data_of_team['full_name']}.\n"
                                          f"✔ Name: {data_of_team['name']}.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="✖ The API service doesn't work.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="✖ User doesn't exist in database")


@log_decorator
def video_of_team(update: Update, context: CallbackContext):
    random_search = randrange(0, 50)

    user = update.message.from_user.id

    session = Session()

    database_user = session.query(User).filter(User.telegram_id == user).first()

    if database_user:
        searching_sport = database_user.team.replace(' ', '+')
        #  opening html page with fav sport
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={searching_sport}")
        #  generating video id url
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"https://www.youtube.com/watch?v={video_ids[random_search]}")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n✖No user's info provided.\n")

    session.close()


@log_decorator
def news_of_team(update: Update, context: CallbackContext):
    # getting user's id from chat
    user = update.message.from_user.id

    # opening dp
    session = Session()

    # searching user in database by telegram id
    database_user = session.query(User).filter(User.telegram_id == user).first()

    # checking if user exist (checking by id)
    if database_user:
        fav_team = database_user.team

        # getting info from api
        data_of_team = show_team_info(fav_team)

        # checking if we get data from API
        if data_of_team:
            team = data_of_team["name"].lower()

            # getting info from parsing the website
            news = get_nba_news(team)

            if news:
                random_search = randrange(0, len(news))

                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Your latest news: {news[random_search ]}")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="\n✖ Something went wrong with parsing.\n")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="\n✖ No user's info provided.\n")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n✖ No user's info provided.\n")

    # closing db
    session.close()


# Commands
# entry point for starting the conversation for personal info
@log_decorator
def add_info(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='1️⃣ Enter your name, please (ex. Maxim):')
    return NAME


@log_decorator
def name_handler(update: Update, context: CallbackContext):
    # receiving the name from user from the last input
    username = update.effective_message.text
    # validating username
    if not username.isalpha():
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='⚠ Please enter correct username (ex. Maxim):')
        return NAME

    if len(username) > 15:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='⚠ Your name is too long. Please enter correct username (ex. Maxim):')
        return NAME

    # temporary saving of data in telegram session
    context.user_data['username'] = username.capitalize()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='✔ Info accepted.',
                             reply_markup=button_back_menu())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='2️⃣ Please, enter your surname (ex. Kostenko):')
    return SURNAME


@log_decorator
def surname_handler(update: Update, context: CallbackContext):
    # receiving the surname from user from the last input
    surname = update.effective_message.text
    # validating surname
    if not surname.isalpha():
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="⚠ Please enter correct surname (ex. Kostenko):")
        return SURNAME

    if len(surname) > 15:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='⚠ Your surname is too long. Please enter correct surname (ex. Maxim):')
        return SURNAME

    # temporary saving of data in telegram session
    context.user_data["surname"] = surname.capitalize()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="✔ Info accepted.",
                             reply_markup=button_back_menu())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="3️⃣ Please enter your favourite nba team (ex. Miami Heat):")

    return TEAM


@log_decorator
# final handler for saving/updating data to db
def finish_handler(update: Update, context: CallbackContext):

    # saving team from last user's input
    team = update.effective_message.text

    # validating
    list_of_teams = ['atlanta hawks', 'boston celtics', 'brooklyn nets', 'charlotte hornets', 'chicago bulls',
                     'cleveland cavaliers', 'dallas mavericks', 'denver nuggets', 'detroit pistons', 'la clippers',
                     'golden state warriors', 'houston rockets', 'indiana pacers', 'los angeles lakers', 'miami heat',
                     'memphis grizzlies', 'milwaukee bucks', 'orlando magic', 'new orleans pelicans', 'new york knicks',
                     'oklahoma city thunder', 'minnesota timberwolves', 'philadelphia 76ers', 'washington wizards',
                     'portland trail blazers', 'sacramento kings', 'utah jazz', 'san antonio spurs', 'toronto raptors',
                     'phoenix suns']

    if team.lower() not in list_of_teams:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='⚠ Please enter an existing and correct basketball team(ex. Boston Celtics):')
        return TEAM

    elif team[0] == "/":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="⚠ You can't use '/' during adding info! Please enter an existing and correct "
                                      "basketball team:")
        return TEAM

    # temporary saving the team into telegram session
    if team.title() == "Philadelphia 76Ers":
        context.user_data['team'] = "Philadelphia 76ers"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='✔ Info accepted.')
    else:
        context.user_data['team'] = team.title()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='✔ Info accepted.')
    # sticker = open('static/' + 'sticker_2.webp', 'rb')
    # context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)

    # saving unique user from telegram context
    user = update.message.from_user.id

    # temporary saving data into telegram session
    context.user_data['telegram_user_id'] = user

    # starting database session
    session = Session()

    # checking if user exist in database
    database_user = session.query(User).filter(User.telegram_id == user).first()
    # send sticker
    sticker = open('static/' + 'sticker_2.webp', 'rb')

    if not database_user:
        # if user doesn't exist - add him
        database_user = User(telegram_id=user,
                             username=context.user_data['username'],
                             surname=context.user_data['surname'],
                             team=context.user_data['team'])
        # adding user into session
        session.add(database_user)
        # saving user in db
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='✔ Collecting the info has been completed.\n'
                                      '✔ You can return to /help info.')
        context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)

    else:
        # if exist - updating info
        database_user.username = context.user_data['username']
        database_user.surname = context.user_data['surname']
        database_user.team = context.user_data['team']
        session.add(database_user)
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='✔ Updating the info has been completed.\n'
                                      '✔ You can return to /help info.')
        context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)

    # closing db session
    session.close()
    return ConversationHandler.END


@log_decorator
def manage_text(update: Update, context: CallbackContext):
    msg = update.message.text.lower()

    if msg in ('hi', 'hey', 'hello', 'hi bot', 'olla', 'holla'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Hi, {update.effective_user.first_name}.\n"
                                      f"This is your news nba bot.\n"
                                      f"I'll notify you about the hottest news from nba!\n"
                                      f"Press /help for more info.")
        sticker = open('static/' + 'sticker.webp', 'rb')
        context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I can't understand you.\n"
                                      "Press /help for more info.")
        sticker = open('static/' + 'sticker_5.webp', 'rb')
        context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)


@log_decorator
def button_back_menu():
    button = [[InlineKeyboardButton('Break conversation.', callback_data='cancel')]]
    return InlineKeyboardMarkup(button)


@log_decorator
def cancel_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='⚠ Adding/updating info has been cancelled.\n'
                                  'To return to the main menu press /help.')
    return ConversationHandler.END
