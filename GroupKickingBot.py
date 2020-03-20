#! python3
# coding: latin-1

import telebot
from telebot import types
import collections
import re
import random

bot = telebot.TeleBot("TOKEN")

updates = bot.get_updates()

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start','comandos'])
def handle_start(message):
    bot.reply_to(message, 
    """Oi, meu nome é MicrosUFC_Bot e, como você deve adivinhar, eu sou um bot.
Meus principais comandos são:
    /start ou /comandos - Informações dos comandos disponíveis
    /admin - Informação de admins e membros
    """)
    print(message.chat.username)

      
@bot.message_handler(func=lambda msg: msg.text in ['Good bot', 'good bot', 'Good fucking bot'])
def goodbot(message):
    coracao=u'\u2764'
    bot.reply_to(message, coracao)
    
@bot.message_handler(func=lambda msg: msg.text in ['Bad bot', 'bad bot'])
def badbot(message):
    triste=u'\U0001F614'
    bot.reply_to(message, triste)
    

# Information about admins and members
@bot.message_handler(commands=['admin', 'admins'])
def admins(message):
    lista_admin = []
    numero_membros = bot.get_chat_members_count(message.chat.id)
    admins = bot.get_chat_administrators(message.chat.id)
    bot.send_message(message.chat.id,'O grupo tem ' + str(numero_membros) + ' membros e ' + str(len(admins)) + ' administradores:')
    for admin in admins:
        print(admin.user.username)
        lista_admin.append(admin.user.first_name)
    lista_admin_txt = '\n'.join(lista_admin)
    bot.send_message(message.chat.id, str(lista_admin_txt))

       
# New group member
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def new_member(message):
    bot.reply_to(message, 'Bem vindo, ' + str(message.new_chat_member.first_name))
    bot.kick_chat_member(message.chat.id, message.new_chat_member.id, None)

# Removed group member
@bot.message_handler(func=lambda m: True, content_types=['left_chat_member'])
def remove_member(message):
    bot.reply_to(message, 'Tchau ' + str(message.left_chat_member.first_name))
    
   

bot.polling()
