# TelegramBOT
Tutorial rápido de como fazer um bot para telegram.

# Primeiros passos
1) Com o telegram aberto na sua conta, procure pelo "usuário" [@BotFather](https://core.telegram.org/bots#6-botfather) e digite **/newbot** para criar um novo bot de telegram.

![image](https://user-images.githubusercontent.com/56649205/77024513-80b63d00-696d-11ea-815a-67634e1a49df.png) 

2) Em seguida, o @BotFather perguntará o nome que do seu bot (exemplo: Julio Bot) e, posteriormente, um username que tem que terminar em *bot*. 

3) Depois disso você receberá um **TOKEN** (que é um código parecido com esse *110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw*) que será necessário para autorizar a comunicação do seu bot com a API do telegram. Guarde esse número que será importante para implementação do mesmo. 

4) Após receber o **TOKEN** digite o comando **/setprivacy** e envie, quando o bot responder, digite **disable**. Assim, seu bot será capaz tanto de receber comandos (*/comandos*) como receber mensagens de texto nos grupos que for inserido. 

5) É interessante habilitar também o modo **/setinline** para habilitar o modo *inline* que permite com que o código seja executado na barra de mensagem ao citar o username do bot. 

Após essas etapas, a configuração básica do bot já está concluída. No entanto, há diversas outras opções disponíveis como definir uma imagem padrão para o bot (**/setuserpic**), colocar uma descrição (**/setdescription**), dentre outros. A lista completa de comandos segue:

```
/mybots — returns a list of your bots with handy controls to edit their settings
/mygames — does the same for your games
/setname – change your bot's name.
/setdescription — change the bot's description, a short text of up to 512 characters, describing your bot. Users will see this text at the beginning of the conversation with the bot, titled ‘What can this bot do?’.
/setabouttext — change the bot's about info, an even shorter text of up to 120 characters. Users will see this text on the bot's profile page. When they share your bot with someone, this text is sent together with the link.
/setuserpic — change the bot‘s profile pictures. It’s always nice to put a face to a name.
/setcommands — change the list of commands supported by your bot. Users will see these commands as suggestions when they type / in the chat with your bot. Each command has a name (must start with a slash ‘/’, alphanumeric plus underscores, no more than 32 characters, case-insensitive), parameters, and a text description. Users will see the list of commands whenever they type ‘/’ in a conversation with your bot.
/deletebot — delete your bot and free its username.
/setinline — toggle inline mode for your bot.
/setinlinegeo - request location data to provide location-based inline results.
/setjoingroups — toggle whether your bot can be added to groups or not. Any bot must be able to process private messages, but if your bot was not designed to work in groups, you can disable this.
/setprivacy — set which messages your bot will receive when added to a group. With privacy mode disabled, the bot will receive all messages. We recommend leaving privacy mode enabled. You will need to re-add the bot to existing groups for this change to take effect.
/newgame — create a new game.
/listgames — get a list of your games.
/editgame — edit a game.
/deletegame — delete an existing game.
```

# Programando o Bot
Em python, há algumas bibliotecas que permitem ao usuário codificar o bot a partir das instruções disponíveis na [API do telegram](https://core.telegram.org/bots/api). Neste tutorial, decidiu-se utilizar a biblioteca [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) sendo uma das mais simples de implementar e ao mesmo tempo bastante completa. 

Para instalar no Jupyter Notebook basta escrever na célula:
```
!pip install pyTelegramBotAPI
```
Caso use o *pip* só tirar o ponto de exclamação. 

Inicialmente, comenta-se parte a parte do código para em seguida colocá-lo em funcionamento. 

- Para começar, importa-se a biblioteca e o TOKEN recebido (substituir o valor entre as aspas), como:

```Python
import telebot

bot = telebot.TeleBot("TOKEN")
```

- Para o bot reconhecer comandos */start* e */help* é preciso definir um "manipulador de mensagens" como:

```Python
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Oi Amigo")
```

Nesse código, ao enviar os comandos definidos o bot responde por meio de uma mensagem "Oi Amigo". 

- Uma outra forma de enviar uma mensagem ao reconhecer comandos consiste em utilizar o **send_message** como descrito em:

```Python
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'MITO!')
```
Diferentemente do **reply_to**, é preciso enviar o ID do chat em que a mensagem será enviada, sendo no caso *message.chat.id* pela [API](https://core.telegram.org/bots/api).

- O bot também pode reconhecer mensagens escritas e executar alguma ação, para isso utiliza-se uma função lambda no manipulador de mensagens. No exemplo abaixo, para qualquer mensagem enviada ao bot, a função retornará *True* e executará a função *echo_all* que tem como objetivo repetir todas as mensagens enviadas por meio *message.text*:

```Python
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)
```
- Além do método anterior, pode ser interessante que o bot reconheça quando os usuários enviarem textos específicos. Para o exemplo abaixo, quando enviar as mensagens *Good bot* ou *good bot*, ele enviará um emotion de coração:

```Python
@bot.message_handler(func=lambda msg: msg.text in ['Good bot', 'good bot'])
def goodbot(message):
    coracao=u'\u2764'
    bot.reply_to(message, coracao)
```

![image](https://user-images.githubusercontent.com/56649205/77130763-f71f7180-6a37-11ea-8f94-b8eb5a1680e4.png)

- É possível utilizar um comando OU uma mensagem específica para executar alguma função como no exemplo:

```Python
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text == 'testando se funciona')
def send_something(message):
    bot.reply_to(message, "Funciona sim!")
```

- Uma outra forma de manipulador de mensagens é por meio de *expressões regulares* (regex). No exemplo abaixo, se o usuário enviar "Contar letras PALAVRA", o bot responderá com o número de letras da expresssão "PALAVRA". Para mais informações: [regex](https://docs.python.org/3/library/re.html).

```Python
@bot.message_handler(regexp="Contar letras \w*")
def contadora(message):
    try:
        frase = message.text
        palavra = re.findall('Contar letras (\w*)', frase)[0]
        print(list(palavra))
        bot.reply_to(message, "Número de letras: " + str(len(list(palavra))))
    except:
        pass
```

- Uma opção também interessante também consiste em executar uma ação a partir de um tipo de atributo enviado (*content_type*). No exemplo abaixo, o bot reconhece todos os arquivos do tipo documento e áudio enviados e executa a função *handle_docs_audio*. 

```Python
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass
```

*content_type* pode ser: 
```
text, audio, document, photo, sticker, video, video_note, voice, location, contact, new_chat_members, 
left_chat_member, new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created, 
channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message
```
