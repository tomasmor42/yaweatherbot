from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler


from config import TOKEN
from consts import CHOOSING, FREE_FORM_TEXT, YES_OR_NO, CHOOSING_CITY
from handlers import start, weather_forecast, enter_city, save_city, default


def conversation():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

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
            CHOOSING_CITY: [
                MessageHandler(~(Filters.command | Filters.regex('^Done$') | Filters.regex('^New city')), save_city)
                , MessageHandler(Filters.regex('^New city'), enter_city)
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
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://ya-weather-bot.herokuapp.com/' + TOKEN)
