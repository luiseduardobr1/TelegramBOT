#! python3
# coding: latin-1

import telebot
from telebot import types
import collections
import re

bot = telebot.TeleBot("TOKEN")

updates = bot.get_updates()

user_dic={}

# Site with updates: https://api.telegram.org/botTOKEN/getUpdates

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "This is a start")
    print(message.chat.username)
    bot.send_message(message.chat.id, 'text')
    # Local de casa
    bot.send_location(message.chat.id, -3.7413135, -38.5031922)
    
# Remove political post's
@bot.message_handler(regexp="\w*bolsonaro\w*|\w*Bolsonaro\w*|\w*Lula\w*|\w*lula\w*")
def political_posts_remove(message):
    #bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Por favor, sem discussões políticas no grupo!')
    
# Remove political post's
@bot.message_handler(regexp="contar \w*")
def contadora(message):
    try:
        frase = message.text
        palavra = re.findall('contar (\w*)', frase)[0]
        print(list(palavra))
        bot.reply_to(message, "Número de letras: " + str(len(list(palavra))))
    except:
        pass

# ----- GET USER ANSWERS ------
@bot.message_handler(commands=['help'])
def handle_help(message):    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('a')
    itembtn2 = types.KeyboardButton('v')
    itembtn3 = types.KeyboardButton('d')
    itembtn4 = types.KeyboardButton('x')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_sex_step)

# Receive letter choice from HELP command
def process_sex_step(message):
    user_dic['sexo'] = message.text
    teste1 = bot.reply_to(message, "Qual seu nome: ")
    bot.register_next_step_handler(teste1, process_sex_step2)

def process_sex_step2(message):
    user_dic['nome'] = message.text
    bot.reply_to(message, user_dic['sexo']+user_dic['nome'])

#---------------------------------

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

# Get member who writes a message in a specific group
@bot.message_handler(func=lambda m: m.chat.id==-1001256130386)
def memberid(message):
    
    #Member Name and ID
    if str(message.from_user.first_name)!='None':
        primeiro_nome=str(message.from_user.first_name)
    else:
        primeiro_nome=' '
    if str(message.from_user.last_name)!='None':
        ultimo_nome=str(message.from_user.last_name)
    else:
        ultimo_nome=' '
    if str(message.from_user.username)!='None':
        username=str(message.from_user.username)
    else:
        username=''
    print(primeiro_nome+' '+ultimo_nome+' - '+str(message.from_user.id) + ' (@' + username+')')
    open('Usuarios.txt', 'a').write(primeiro_nome+' '+ultimo_nome+' - '+str(message.from_user.id) + ' (@' + username+')'+'\n')
    
    # Get number of occurrence by user
    lista_usuarios = open("Usuarios.txt", "r").readlines()
    ocorrencias_comum = collections.Counter(lista_usuarios).most_common()
    open('UsuariosEstatistica.txt', 'w').writelines(str(ocorrencias_comum))
       
# New group member
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def new_member(message):
    bot.reply_to(message, 'Bem vindo! Já deu o cu hoje ?')
    print('olá '+str(message.new_chat_member.username))
    #bot.kick_chat_member(message.chat.id, message.new_chat_member.id, None)

# Removed group member
@bot.message_handler(func=lambda m: True, content_types=['left_chat_member'])
def remove_member(message):
    bot.reply_to(message, 'Bye')
    print('bye '+str(message.left_chat_member.username))
    

# Send my curriculum
#@bot.message_handler(func=lambda msg: msg.text == 'meu curriculo' or msg.text == 'meu currículo' or msg.text == 'currículo' or msg.text == 'curriculo')
@bot.message_handler(func=lambda msg: msg.text in ['currículo', 'meu currículo', 'curriculo','meu curriculo'])
def curriculo(message):
    doc = open('curriculo_luiseduardopompeu.pdf', 'rb')
    bot.send_document(message.chat.id, doc)

#------------ INLINE CODES -----------
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Manhã', types.InputTextMessageContent('Bom dia!'))
        r2 = types.InlineQueryResultArticle('2', 'Tarde', types.InputTextMessageContent('Boa tarde!'))
        r3 = types.InlineQueryResultArticle('3', 'Noite', types.InputTextMessageContent('Boa noite!'))
        bot.answer_inline_query(inline_query.id, [r, r2, r3], cache_time=1)
    except Exception as e:
        print(e)
        
@bot.inline_handler(lambda query: query.query == 'cu')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
                                         input_message_content=types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
                                         input_message_content=types.InputTextMessageContent('hi2'))
        bot.answer_inline_query(inline_query.id, [r, r2], cache_time=1)
    except Exception as e:
        print(e)
              
        
@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Já Deram o Cu Hoje', types.InputTextMessageContent('Já Deram o Cu hoje?'))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)
        

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w*prova\w*")
def handle_message(message):
    bot.reply_to(message, "Enfia a prova no cu")
    print(message.text)

# Handlers can be stacked to create a function which will be called if either message_handler is eligible
# This handler will be called if the message starts with '/hello' OR is some emoji
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text == 'testando se funciona')
def send_something(message):
    bot.reply_to(message, "Funciona sim fdp!")
    
# Working with entities - url, email
@bot.message_handler(func=lambda m: True)
def entities(message):
    try:
        if message.entities[0].type=='url':
            print(message.text)
        if message.entities[0].type=='email':
            print(message.text)
    except:
        pass
    

bot.polling()
