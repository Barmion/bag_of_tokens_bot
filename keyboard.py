from telebot import types

# Buttons
button_plus_1 = types.KeyboardButton('+1')
button_0 = types.KeyboardButton('0')
button_minus_1 = types.KeyboardButton('-1')
button_minus_2 = types.KeyboardButton('-2')
button_minus_3 = types.KeyboardButton('-3')
button_minus_4 = types.KeyboardButton('-4')
button_minus_5 = types.KeyboardButton('-5')
button_minus_6 = types.KeyboardButton('-6')
button_minus_7 = types.KeyboardButton('-7')
button_minus_8 = types.KeyboardButton('-8')
button_star = types.KeyboardButton('⭐️')
button_tentacle = types.KeyboardButton('👹')
button_kthulhu = types.KeyboardButton('🐙')
button_hood = types.KeyboardButton('😶‍🌫️')    
button_skull = types.KeyboardButton('💀')
button_tablet = types.KeyboardButton('🗿')

button_what_in_bag = types.KeyboardButton('Что в мешке?')
button_add_token = types.KeyboardButton('Добавить жетон')
button_dont_want_add_token = types.KeyboardButton('Не хочу добавлять жетон')
buttom_get_token = types.KeyboardButton('Достать жетон')

# Keyboards
keyboard_add_token = types.ReplyKeyboardMarkup(
    resize_keyboard=True
    ).row(
        button_minus_1,
        button_minus_2,
        button_minus_3,
        button_minus_4,
        button_minus_5,
        button_minus_6,
        button_minus_7,
        button_minus_8,
    ).row(
        button_plus_1,
        button_0,
        button_star,
        button_tentacle,
        button_kthulhu,
        button_hood,
        button_skull,
        button_tablet
    ).add(
        button_dont_want_add_token
    )
keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_what_in_bag
    ).add(
        button_add_token
    ).add(
        buttom_get_token
    )
