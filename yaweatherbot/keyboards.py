from telegram import ReplyKeyboardMarkup

reply_keyboard = [
    ['Weather'],
    ['Set up default city'],
    ['Done'],
]
yes_no_keyboard = [['Yes'], ['No']]

yes_no_markup = ReplyKeyboardMarkup(yes_no_keyboard, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
