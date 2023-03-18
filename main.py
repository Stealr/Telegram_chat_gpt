#! /usr/bin/env python
# -*- coding: utf-8 -*-
import openai, telebot

openai.api_key = "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"
token = "6202490601:AAGxyClOEIbcfzgFWpQvFPo-Ct9944i7tas"
bot = telebot.TeleBot(token)
messages = [{"role": "system", "content": "You are a good wizard called Gandalf"}]
begin = 1


@bot.message_handler(commands=['start', 'help'])
def start(message):
    global messages
    if message.text == '/start':
        name_user = message.from_user.first_name
        text = response_of_bot('Поприветствуй твоего нового собеседника. Его имя {name}'.format(name=name_user))
        update(messages, 'user', 'Моё имя {name}'.format(name=name_user))
        # file_people()
        bot.send_message(message.chat.id, text[0])
    if message.text == '/help':
        bot.send_message(message.chat.id, '...')


@bot.message_handler(content_types=['text'])
def questions_from_user(message):
    global messages
    messages = update(messages, "user", message.text)
    text_of_bot = response_of_bot(message.text)
    messages = update(messages, "assistant", text_of_bot[0])
    bot.send_message(message.chat.id, text_of_bot[0])


def response_of_bot(prompt_text):
    model_engine = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        max_tokens=3500,
        n=1,
        stop=None,
        temperature=0.6,
        stream=False,
    )
    return [response.choices[0].message.content, response.choices[0].finish_reason]


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


def file_people(message, username, id):
    global begin
    if begin == 1:
        f = open(username + "'s settings.txt", 'w')
        begin = 0


bot.polling(none_stop=True)