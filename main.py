import requests
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, Filters, MessageHandler
from Levenshtein import distance


api_url = 'http://api.openweathermap.org/data/2.5/weather?'
four_days_api_url = 'http://api.openweathermap.org/data/2.5/hourly?'

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

WEATHER, CHOOSING, FREE_FORM_TEXT, CONFIRM, YES_OR_NO = range(5)
CITIES_FILE = ''
reply_keyboard = [
    ['Weather'],
    ['Set up default city'],
    ['Done'],
]
yes_no_keyboard = [['Yes'], ['No']]
yes_no_markup = ReplyKeyboardMarkup(yes_no_keyboard, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

template = "The weather today is from {} to {} which feels like {}. There will be precipitation {}"


def get_weather_forecast(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    resp = requests.get(api_url, params=params)
    if not resp.ok:
        raise ValueError("Something went wrong, try another time")
    forecast = resp.json()['main']
    temp_max = forecast['temp_max']
    temp_min = forecast['temp_min']
    feels_like = forecast['feels_like']
    precipitation = resp.json()['weather'][0]['main'] + ":" + (resp.json()['weather'][0].get('description') or "")
    return template.format(temp_min, temp_max, feels_like, precipitation)

BIG_INT = 1000

def check_closest_city(city):
    min_distance = BIG_INT
    closet_cities = []
    city = city.lower()
    with open('city.txt') as cities:
        for line in cities:
            line = line.strip('\n').lower()
            dist = distance(line, city)
            if dist < min_distance:
                min_distance = dist
                closet_cities = [line]
            elif dist == min_distance:
                closet_cities.append(line)
    return closet_cities





def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("I'm a weather bot. What do you want to do?", reply_markup=markup)
    return CHOOSING


def get_city_name(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data

    update.message.reply_text(
        f"You set your default city to a {user_data['city']}. Is it city you want to check?",
        reply_markup=markup,
    )

    return CONFIRM


def enter_city(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        f"Enter city name",
        reply_markup=markup,
    )
    context.user_data['city'] = ''
    return FREE_FORM_TEXT




def save_city(update: Update, context: CallbackContext) -> int:
    city = update.message.text
    closest_city = check_closest_city(city)
    print(closest_city)

    context.user_data['city'] = update.message.text

    update.message.reply_text(
        f"You set your default city to a {city}. Is it city you want to check?",
        reply_markup=yes_no_markup,
    )
    return YES_OR_NO


def weather_forecast(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if ('city' not in user_data.keys()) or (not user_data['city']):
        update.message.reply_text(
            "Set up a default city first",
            reply_markup=markup,
        )
    else:
        update.message.reply_text(
            "Getting a weather forecast"
        )
        forecast = get_weather_forecast(user_data['city'])
        update.message.reply_text(forecast, reply_markup=markup)
    return CHOOSING


def default(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Getting a weather forecast",
        reply_markup=markup,
    )
    return CHOOSING


if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^Weather$'), weather_forecast
                ),
                MessageHandler(Filters.regex('^Set up default city$'), enter_city),
            ],
            YES_OR_NO: [
                MessageHandler(Filters.regex('^Yes$'), weather_forecast),
                MessageHandler(Filters.regex('^No'), enter_city)

            ],

            FREE_FORM_TEXT: [
                MessageHandler(
                    ~(Filters.command | Filters.regex('^Done$')), save_city
                )
            ],


        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), default)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    #updater.idle()