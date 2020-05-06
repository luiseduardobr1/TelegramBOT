# TelegramBOT
Tutorial "rápido" de como fazer um bot para telegram.

## Primeiros passos
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

## Programando o Bot
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
left_chat_member, new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, 
supergroup_chat_created, channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message
```

## Executando
Para iniciar o bot, é preciso que no final do código tenha a linha:

```Python
bot.polling()
```

Assim, um código funcional completo (deixando o TOKEN para o usuário inserir) consiste em:

```Python
import telebot

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	
@bot.message_handler(regexp="Contar letras \w*")
def contadora(message):
    try:
        frase = message.text
        palavra = re.findall('Contar letras (\w*)', frase)[0]
        print(list(palavra))
        bot.reply_to(message, "Número de letras: " + str(len(list(palavra))))
    except:
        pass

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
```
É importante ressaltar que todos os manipuladores de mensagens são executados em ordem, então, caso haja algum problema de execução no bot, é melhor alterar a posição das funções no código. 

Um outro exemplo de código funcional consiste em [GroupKickingBot](https://github.com/luiseduardobr1/TelegramBOT/blob/master/GroupKickingBot.py) que é um código bem simples de um bot utilizado para excluir qualquer membro novo em algum grupo no qual o mesmo é colocado como administrador. 

Para um [grupo de amizade do reddit brasil](https://t.me/joinchat/NLSAqhl4ZdiubHNwUCWwjQ) utiliza-se o bot com código-fonte: [botReddit](https://github.com/luiseduardobr1/TelegramBOT/blob/master/botReddit.py).

Para mais exemplos, pode-se estudar pelos disponíveis da página da biblioteca utilizada: [examples](https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples). 

## Funções e atributos adicionais

## Deploy do script 
Obviamente, o bot só funciona enquanto está sendo executado. Para manter sua operação sem precisar do computador ligado ininterruptamente, há diversas soluções possíveis:

### Rodando no Android
É possível rodar scripts em python no celular com sistema android. Para isso, recomendo o aplicativo **Pydroid** que já testei e cumpre bem sua função, sendo bem fácil de configurar/utilizar. 

### Raspberry Pi
Essa é uma recomendação clássica em fóruns de internet uma vez que o consumo de energia elétrica para operação de um microcontrolador é baixa, permitindo rodar scripts sem sobrecarregar seu aparelho celular ou manter o computador ligado ininterruptamente. 

### Servidores
Na internet, é possível encontrar diversos sites que oferecem uma máquina virtual ou um espaço no servidor para executar de forma *praticamente* ininterrupta códigos nas mais diversas linguagens de programação. No entanto, a maioria dos serviços gratuitos têm algumas regras que dificultam ou inviabilizam certas funções no bot, irei destacar isso em cada caso:

#### PythonAnywhere
O [PythonAnywhere](https://www.pythonanywhere.com/) te oferece uma máquina virtual gratuitamente que você pode hospedar seus scripts e rodá-los remotamente. De longe, é o sistema mais fácil de configurar. Você pode escrever seu bot em sua máquina e depois fazer upload para o site. Em seguida, basta executá-lo no *Bash Console* com o comando: `python3.8 meuscript.py` (3.8 é a versão do python que escolhi, mas pode ser outra). Pronto ! Seu script já está em execução. Caso queira instalar alguma biblioteca nova basta escrever `pip3.8 install --user BIBLIOTECA`.

**Vantagens:**
* Fácil usar e configurar
* Suporte rápido e eficiente no [fórum de discussão](https://www.pythonanywhere.com/forums/)

**Desvantagens**
* É comum o sistema ser reiniciado e o bot ficar fora do ar. Para minimizar esse problema, é possível configurar o *Scheduled tasks* na aba *Tasks* para inicializá-lo, caso esteja fora do ar, diariamente em um horário específico.
* Após alguns dias, é possível atingir o limite de utilização do site na conta gratuita o que, como consequência, reduz a velocidade de processamento do seu script, deixando-o lento. 
* Caso o script tente acessar algum site que não esteja na [whitelist](https://www.pythonanywhere.com/whitelist/), este será bloqueado para a conta gratuita. De longe, este foi o principal motivo de eu evitar utilizar o python anywhere.  

![image](https://user-images.githubusercontent.com/56649205/81192043-21999f80-8f90-11ea-9d36-c293518c3595.png)


#### Heroku
Na minha opinião, dentre os servidores gratuitos, este é o melhor para hospedar um bot. No entanto, é um pouco complicado para configurar na primeira utilização. Tentarei explicar de forma bem breve para o SO Windows, mas a informação completa está disponível no [site](https://devcenter.heroku.com/articles/getting-started-with-python). 

1) Baixe e instale [Git](https://git-scm.com/download/win) e [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

2) Crie uma pasta e coloque o script em python que vc quer enviar ao servidor (*deploy*). 

3) Na mesma pasta do item (2), coloque um arquivo de texto *requirements.txt* em que nele deve constar todas as bibliotecas "de terceiros" que devem ser instaladas no servidor do heroku. Para saber a versão da biblioteca utilizada, utilize o comando `pip freeze` no console da sua instalação python. 

Como exemplo de um bot que criei constava as seguintes bibliotecas no arquivo *requirements.txt*:
```
pyTelegramBotAPI==3.6.7
bs4==0.0.1
requests==2.22.0
requests-html==0.10.0
pytz==2019.3
python-dateutil==2.8.1
pandas==1.0.1
```
