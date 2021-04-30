from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext

from consts import CHOOSING, FREE_FORM_TEXT, CONFIRM, YES_OR_NO, CHOOSING_CITY
from keyboards import markup, yes_no_markup
from find_cities import check_closest_city
from weather import get_weather_forecast


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
    closest_cities = check_closest_city(city)
    if city.lower() not in closest_cities:
        closest_cities = set(closest_cities)
        closest_city_keyboard = [[close_city] for close_city in closest_cities]
        closest_city_keyboard.append(['New city'])
        update.message.reply_text(
            f"We can't show the weather in {city}. Is it a typo? Choose one of the we suggested or type it from scratch",
            reply_markup=ReplyKeyboardMarkup(closest_city_keyboard),
        )
        return CHOOSING_CITY

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
            "Set up a default city first by clicking on the Setup default city button",
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
        "Thanks you for using the bot! Please choose a city to get a weather for.",
        reply_markup=markup,
    )
    return CHOOSING
