import telebot
from telebot import types

bot = telebot.TeleBot("ТВОЙ_ТОКЕН")  # <-- сюда вставь свой токен

questions = [
    {
        "question": "🌀 Как выглядит мир внутри тебя?",
        "images": ["1A.jpg", "1B.jpg", "1C.jpg"],
        "options": ["1A", "1B", "1C"]
    },
    {
        "question": "🌍 Как выглядит мир вокруг тебя?",
        "images": ["2A.jpg", "2B.jpg", "2C.jpg"],
        "options": ["2A", "2B", "2C"]
    }
]

descriptions = {
    "1A": "Ты спокойна и ценишь гармонию.",
    "1B": "Ты динамична, любишь перемены.",
    "1C": "Ты загадочна и любишь уединение.",
    "2A": "Мир для тебя — это порядок и структура.",
    "2B": "Ты воспринимаешь мир через чувства и интуицию.",
    "2C": "Ты замечаешь тонкости и любишь детали."
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = []
    bot.send_message(message.chat.id, "👋 Привет! Сейчас мы проведём диагностику.")
    send_question(message.chat.id, 0)

def send_question(chat_id, q_index):
    if q_index >= len(questions):
        show_result(chat_id)
        return

    question = questions[q_index]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i, option in enumerate(question["options"]):
        markup.add(str(i + 1))

    bot.send_message(chat_id, question["question"])

    for i, image in enumerate(question["images"]):
        with open(image, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=f"{i+1}")

    bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: handle_answer(msg, q_index))

def handle_answer(message, q_index):
    try:
        index = int(message.text) - 1
        selected_option = questions[q_index]["options"][index]
        user_data[message.chat.id].append(selected_option)
        send_question(message.chat.id, q_index + 1)
    except:
        bot.send_message(message.chat.id, "Пожалуйста, выбери цифру 1, 2 или 3.")
        send_question(message.chat.id, q_index)

def show_result(chat_id):
    result = "🔮 Вот твоя диагностика:\n\n"
    for code in user_data[chat_id]:
        result += f"🖼 {descriptions[code]}\n"
    bot.send_message(chat_id, result)

bot.polling()
