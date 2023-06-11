from aiogram import Bot, Dispatcher, executor, types
import openai
from test import detect_language

API_TOKEN = 'TELEGRAM_BOT_TOKEN'
OPENAI_API_KEY = "OPENAI_API_KEY"

MODEL = "gpt-3.5-turbo"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

user_messages = {}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_messages[user_id] = [{"role": "system",
                               "content": "Kino bo'yicha maslahat, Nima Kinolar yoqishi, Kino haiqda ma'lumot, Советы по фильмам, какие фильмы нравятся, информация о фильмах"}]

    await message.reply("Assalom alaykum men sizga filmlar tavsiya qilaman. Qanday Kinolarni yoqtirasiz?")


@dp.message_handler()
async def process_message(message: types.Message):
    user_id = message.from_user.id
    messages = user_messages.get(user_id, [])

    if detect_language(message.text.lower()) == 'ru':
        messages.append({"role": "user", "content": "~~Russian"})
        loading_message = await message.answer('Biroz kuting...')
        await bot.send_chat_action(message.chat.id, 'typing')

        response = await generate_response(messages)

        messages.append({"role": "assistant", "content": response})
        user_messages[user_id] = messages

        await bot.delete_message(loading_message.chat.id, loading_message.message_id)
        await message.answer(response)

    elif detect_language(message.text.lower()) == 'uz':
        messages.append({"role": "user", "content": f'{message.text},Kino, Kino haqida'})
        loading_message = await message.answer('Biroz kuting...')
        await bot.send_chat_action(message.chat.id, 'typing')

        response = await generate_response(messages)

        messages.append({"role": "assistant", "content": response})
        user_messages[user_id] = messages

        await bot.delete_message(loading_message.chat.id, loading_message.message_id)
        await message.answer(response)

    else:
        await message.answer("Men Uzbek va Rus tilida sizni tushina olaman!")


async def generate_response(messages):
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        max_tokens=200
    )
    response = completion.choices[0].message.content
    return response


executor.start_polling(dp, skip_updates=True)
