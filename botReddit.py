# coding: latin-1

import telebot
from telebot import types
import collections
import re
import random
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from dateutil import tz
from telebot import util

bot = telebot.TeleBot("TOKEN")

updates = bot.get_updates()

user_dic={}
count=0

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start','comandos'])
def handle_start(message):
    bot.reply_to(message, 
    """Oi, meu nome é JáDeuCu_Bot e, como você deve adivinhar, eu sou um bot (então sem nudes no privado).
Meus principais comandos são:
    /start - Informações dos comandos disponíveis
    /regras - Regras do grupo
    /top - Top 5 dos usuários com mais mensagens
    /bottom - Top 5 dos usuários com menos mensagens :(
    /admin ou /admins - Número de membros e admins
    /report - Avisar sobre mensagens infringindo as regras
    /bomdia /boatarde e /boanoite - mensagem de carinho
    /corona - Casos de coronavírus no Brasil
    /cornos - Seleciona aleatoriamente três cornos
    Contar letras PALAVRA - conta o número de letras de "PALAVRA"
    """)
    print(message.chat.username)
    # Local de casa
    #bot.send_location(message.chat.id, lat, long)
    
# Top posters
@bot.message_handler(commands=['assunto'])
def quebragelo(message):
    perguntas=['O que vocês estão fazendo?', 'O que fizeram para matar o tédio?', 'Quais os melhores memes?', 'Qual o último filme que viram?',
              'O que estão pensando ?']
    escolhido=random.randint(0,len(perguntas))
    bot.reply_to(message, perguntas[escolhido])
    
@bot.message_handler(commands=['report'])
def report(message):
    bot.reply_to(message, "@leofilips @Zanzokuken @luiseduardobr1 @Rasholnikov @trotou @1016165020")
    
@bot.message_handler(commands=['cornos'])
def cornos(message):
    # ler os usuários no txt
    lista_usuarios = open("Usuarios.txt", "r", encoding="mac_roman").readlines()
    # remover repetidos
    lista_usuarios = list(dict.fromkeys(lista_usuarios))
    # escolher aleatoriamente 3 membros
    escolhido1=random.randint(0,len(lista_usuarios))
    escolhido2=random.randint(0,len(lista_usuarios))
    escolhido3=random.randint(0,len(lista_usuarios))

    print(lista_usuarios[escolhido1] + lista_usuarios[escolhido2] + lista_usuarios[escolhido3])
    print((len(lista_usuarios)))
    bot.reply_to(message, "Os mais cornos deste grupo são: {}{}{}\n".format(lista_usuarios[escolhido1],lista_usuarios[escolhido2],lista_usuarios[escolhido3]))
        

'''
#Fonte 1
@bot.message_handler(commands=['corona'])
def corona(message):
    link = "https://www.worldometers.info/coronavirus/country/brazil/"
    r  = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    casos = soup.findAll(class_='maincounter-number')
    casos[0]=casos[0].text.strip()
    casos[1]=casos[1].text.strip()
    casos[2]=casos[2].text.strip()
    bot.reply_to(message, """COVID19-Brasil
Casos registrados: {}
Mortes: {}
Recuperados: {}
    """.format(casos[0], casos[1], casos[2]))
'''


@bot.message_handler(commands=['corona'])
def corona(message):
    html = requests.get("https://bing.com/covid/data")
    data = html.text
    soup = BeautifulSoup(data, "html.parser")

    res = json.loads(str(soup)) 

    for item in res['areas']:
        if item['id']=='brazil':
            #print(item['id'])
            
            palavra = re.search('(\d*)-(\d*)-(\d*)T(\d*):(\d*):(\d*)', item['lastUpdated'])
            # Data e Hora - LOCAL (convert UTC to LOCAL)
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('America/Fortaleza')
            utc = datetime.strptime('{}:{}:{} {}/{}/{}'.format(palavra[4], palavra[5], palavra[6], palavra[3], palavra[2], palavra[1]), '%H:%M:%S %d/%m/%Y')
            utc = utc.replace(tzinfo=from_zone)
            central = utc.astimezone(to_zone)
            ultima_atualizacao = central.strftime ("%H:%M:%S - %d/%m/%Y")
            
            print(item['totalConfirmed'])
            print(item['totalDeaths'])
            print(item['totalRecovered'])
            bot.reply_to(message, """Total de Casos Confirmados: {}
Casos fatais: {}
Casos recuperados: {}
Atualizado em: {}
Fonte: bing.com/covid
    """.format(item['totalConfirmed'], item['totalDeaths'], item['totalRecovered'], ultima_atualizacao))

'''
# Top posters
@bot.message_handler(commands=['top'])
def topmembers(message):
    i=0
    msg=''
    while i<5:
        string_edit=str(ocorrencias_comum[i])
        string_edit=string_edit.replace('(','')
        string_edit=string_edit.replace(')','')
        string_edit=string_edit.replace(r"'",r"")
        string_edit=string_edit.replace(r"\n",r"")
        string_edit=string_edit.replace(r",",r" - mensagens: ")
        print(string_edit)
        msg=msg+string_edit+'\n'
        i=i+1
    bot.reply_to(message,"As pessoas mais desocupadas e procrastinadoras do grupo são: \n" + msg)
'''

@bot.message_handler(commands=['top'])
def topmembers(message):
    usersID=[]
    usersName=[]
    combinacao = []
    top=[]
    # txt com todos usuários
    usuarios = open("Usuarios.txt", "r", encoding="latin-1").readlines()
    # remover repetidos
    usuarios_unicos = list(dict.fromkeys(usuarios))
    # Dividir em Nome - ID
    for item in usuarios:
        usersID.append(re.search('- (\d*)', item)[1])
        usersName.append(item[:item.find('-')])
    # Combinacao é uma lista que contempla Nome-ID
    combinacao.extend([list(i) for i in zip(usersName, usersID)])
    # Criar uma lista com todos usuarios
    correcao=''
    for b in collections.Counter(usersID).most_common():
        for a in range(0,len(usersID)):
            #print(str(b[0]) + '-' + str(combinacao[a][1]))
            if str(b[0])==str(combinacao[a][1]) and correcao!=str(b[0]):
                print(str(combinacao[a][0]) + ' - mensagens: '+ str(b[1]))
                correcao=str(b[0])
                top.append(str(combinacao[a][0]) + ' - mensagens: '+ str(b[1]))
                
    bot.reply_to(message,"As pessoas mais desocupadas e procrastinadoras do grupo são: \n{}\n{}\n{}\n{}\n{}".format(top[0],top[1],top[2],top[3],top[4]))


# Bottom posters
@bot.message_handler(commands=['bottom'])
def downmembers(message):
    usersID=[]
    usersName=[]
    combinacao = []
    top=[]
    # txt com todos usuários
    usuarios = open("Usuarios.txt", "r", encoding="latin-1").readlines()
    # remover repetidos
    usuarios_unicos = list(dict.fromkeys(usuarios))
    # Dividir em Nome - ID
    for item in usuarios:
        usersID.append(re.search('- (\d*)', item)[1])
        usersName.append(item[:item.find('-')])
    # Combinacao é uma lista que contempla Nome-ID
    combinacao.extend([list(i) for i in zip(usersName, usersID)])
    # Criar uma lista com todos usuarios
    correcao=''
    for b in collections.Counter(usersID).most_common():
        for a in range(0,len(usersID)):
            #print(str(b[0]) + '-' + str(combinacao[a][1]))
            if str(b[0])==str(combinacao[a][1]) and correcao!=str(b[0]):
                print(str(combinacao[a][0]) + ' - mensagens: '+ str(b[1]))
                correcao=str(b[0])
                top.append(str(combinacao[a][0]) + ' - mensagens: '+ str(b[1]))
                
    bot.reply_to(message,"Os lurkers do grupo são: \n{}\n{}\n{}\n{}\n{}".format(top[-1],top[-2],top[-3],top[-4],top[-5]))
    
# All posters
@bot.message_handler(commands=['todos'])
def total_msgs(message):
    usersID=[]
    usersName=[]
    username=[]
    combinacao = []
    top=[]
    # txt com todos usuários
    usuarios = open("Usuarios.txt", "r", encoding="latin-1").readlines()
    # remover repetidos
    usuarios_unicos = list(dict.fromkeys(usuarios))

    # Dividir em Nome - ID
    for item in usuarios:
        usersID.append(re.search('- (\d*)', item)[1])
        usersName.append(item[:item.find('-')])
        username.append(re.search('@(\w*)', item)[1])
    # Combinacao é uma lista que contempla Nome-ID
    combinacao.extend([list(i) for i in zip(usersName, usersID, username)])
    # Criar uma lista com todos usuarios
    correcao=''
    contagem=0
    for b in collections.Counter(usersID).most_common():
        for a in range(0,len(usersID)):
            #print(str(b[0]) + '-' + str(combinacao[a][1]))
            if str(b[0])==str(combinacao[a][1]) and correcao!=str(b[0]):
                #print(str(combinacao[a][0]) + ' - mensagens: '+ str(b[1]))
                correcao=str(b[0])
                contagem = contagem+1
                top.append(str(contagem) + ' : ' + str(combinacao[a][0]) + ' (@' + str(combinacao[a][2]) + ') - MSGs: '+ str(b[1]))

    splitted_text = util.split_string('\n'.join(top), 3000)
    for text in splitted_text:
        bot.reply_to(message,"Número de mensagens por membro: \n" + text)


    
# Handles all text messages that match the regular expression
@bot.message_handler(commands=['universal'])
@bot.message_handler(regexp="\w* universal \w*")
def universal(message):
    bot.reply_to(message, "AMÉM IRMÃOS! Eu era ex-viado, ex-prostituto, ex-cheirador de cola, ex-traficante, tinha apenas um rim e estava morrendo de AIDS, mas tudo isso mudou quando fui ungido pelo pastor na IGREJA UNIVERSAL. ")   
    
# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['regras'])
def regras(message):
    bot.reply_to(message, """REGRAS:
- Sem flood de stickers/mensagens.
- Sem racismo, machismo, homofobia ou qualquer discriminação SÉRIA (brincamos com isso desde que as pessoas se sintam confortáveis com a brincadeira e brinquem também, nada sério ou pesado).
- Sem brigas (só de peixeira com hora marcada sem perder a amizade)
- Sobre desabafos: vamos usar o bom senso quando alguém realmente estiver querendo desabafar ou querendo ajuda. Todos temos nossos momentos de bad, então peço que se alguém quiser, deêm o espaço para desabafar e ajudem.
- Sem o compartilhamento de materiais de conteúdo sensível (pornografia, violência, etc)
- Proibido falar mal da Greta Thunberg (s2)
- Usuários com pênis > 15 cm serão banidos
- Dúvidas, sugestões ou correções no bot falar com @luiseduardobr1
- Qualquer problema só avisar os Admins. Se divirtam!""")
    
# Remove political post's
@bot.message_handler(regexp="""\w*bolsonaro\w*|\w*Lula\w*|\w*dilma\w*|\w*guedes\w*|
                     \w*Gleisi\w*|\w*maluf\w*|\w*sergio moro\w*|\w*Deodoro da Fonseca\w*""")
def political_posts_remove(message):
    #bot.delete_message(message.chat.id, message.message_id)
    global count
    count=count+1
    if count>=5:
        bot.send_message(message.chat.id, 'Por favor, sem discussões políticas no grupo!')
        count=0
        
# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w* prova \w*")
def provas(message):
    bot.reply_to(message, "Enfia a prova no cu")
    print(message.text)
    
# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w*hacker\w*")
def hacker(message):
    bot.reply_to(message, "Save Kevin Mitnick!")
    print(message.text)
    
# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w*flamengo\w*")
def gol(message):
    bot.reply_to(message, "Hoje tem gol do Gabigol!")
    print(message.text)
    
# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w*elfo\w*")
def elfo(message):
    bot.reply_to(message, "Não se pode confiar em elfos")
    print(message.text)

# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w*areia\w*")
def areia(message):
    bot.reply_to(message, "Odeio areia")
    print(message.text)
    
    
# Handles all text messages that match the regular expression
@bot.message_handler(regexp="\w*comi o cu\w*")
def comicu(message):
    bot.reply_to(message, "CARALHO BRODER VOU TE CONTAR PUTA QUE PARIU EU TENTO CONVERSAR COM VOCÊ TER UM TEMPO OCIOSO DE RECREAÇÃO PRA DESCANSAR E TROCAR UM PAPO SABE IGUAL TODO AMIGO FAZ PRA RELAXAR UM POUCO DOS ESTRESSES DA VIDA E DA ROTINA MAS AÍ VOCÊ VEM TODA VEZ TODA VEZ PORRA E COME MEU CU PARA DE COMER MEU CU CARALHO EU SÓ TO TENTANDO TER UMA CONVERSA MADURA PARA DE COMER MEU CU TODA VEZ EU VOU LER SUA MENSAGEM ACHANDO QUE É UM COMENTÁRIO INTELIGENTE QUE VAI REPERCUTIR NO MEU DIA-A-DIA MAS É SÓ VOCÊ COMENDO MEU CU ISSO TEM QUE PARAR BRODER POR FAVOR")
        
# Dom Pedro II
@bot.message_handler(regexp="""\w*Dom Pedro II\w*""")
def political_dompedro(message):
    #bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'MITO!')
    
# Remove political post's
@bot.message_handler(regexp="Contar letras \w*")
def contadora(message):
    try:
        frase = message.text
        palavra = re.findall('Contar letras (\w*)', frase)[0]
        print(list(palavra))
        bot.reply_to(message, "Número de letras: " + str(len(list(palavra))))
    except:
        pass
    
# Bom dia e boa tarde 
@bot.message_handler(commands=['bomdia','boatarde','boanoite'])
def bomdiaboatardeboanoite(message):
    #bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Mermão bom dia é o caralho parcero, isso aqui é o grupo da torcida jovem, entendeu? Tu quer dar bom dia tu cria um grupo de viado, de GLS, e fica "bom dia", "boa tarde", "boa noite", ou então tu cria um grupo pra tua família, aí tu fica dando bom dia. Aqui é psicopata, ladrão, bandido, cheirador, vendedor de droga, polícia maluco, polícia assaltante, aqui tem a porra toda mermão, isso aqui é a Torcida Jovem do Reddit! Bom dia é o caralho, rapá! Toma no cu...')
    
# trabalho bot
@bot.message_handler(regexp="""\w*não trabalham\w*|\w*nao trabalham\w*|\w*nao trabalha\w*""")
def trabalho(message):
    #bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Qual é? Que mané...vai me dar trabalho por acaso?')
    
# bot fdp
#@bot.message_handler(regexp="""\w*bot fdp\w*|\w*bot filha\w*|\w*bot filho\w*""")
#def trabalho(message):
    #bot.delete_message(message.chat.id, message.message_id)
#    bot.send_message(message.chat.id, """Mas que porra é essa que você falou sobre mim, seu arrombado? Fique sabendo que eu me formei com honra no Exército Brasileiro, e estive envolvido em diversos ataques secretos ao Comando Vermelho, e tenho mais de 300 mortes confirmadas. Não só sou treinado em táticas de gorila como também sou o melhor sniper em todo o BOPE. Pra mim você num passa de mais um alvo. Vou comer esse seu cuzinho com uma precisão nunca antes vista nesse planeta, marque minhas palavras, parça. Você pensa que pode sair por aí falando merda na Internet? Pense de novo, cuzão. Enquanto você lê isso eu tô falando com minha rede secreta de espiões espalhados pelo Brasil e seu IP está sendo localizado então melhor se preparar pra treta, viado. A treta que vai acabar com essa bosta patética que vicê chama de vida. Você tá morto, moleque. Posso estar em qualquer lugar, a qualquer hora, e posso te matar de setecentas maneiras diferentes, e isso só com minhas próprias mãos. Não só eu sou treinado em capoeira e jiu jitsu brasileiro, como também tenho acesso a todo o arsenal da Marinha Brasileira e vou usar isso tudo pra expulsar esse seu cu da face do continente, seu merdinha. Se tu soubesse a maldição que seu comentário “esperto” traria sobre você, talvez você tivesse calado tua boca. Mas não, você não fechou o bico, e vai pagar por isso, seu idiota do caralho. Vou cagar fúria em cima de você até tu se afogar. Você tá fudido, moleque.""")
    
@bot.message_handler(func=lambda msg: msg.text in ['Good bot', 'good bot', 'Good fucking bot'])
def goodbot(message):
    coracao=u'\u2764'
    bot.reply_to(message, coracao)
    
@bot.message_handler(func=lambda msg: msg.text in ['Bad bot', 'bad bot'])
def badbot(message):
    triste=u'\U0001F614'
    bot.reply_to(message, triste)

@bot.message_handler(func=lambda msg: msg.text in ['Hello there', 'hello there'])
def hello_there(message):
    bot.reply_to(message, 'General Kenobi')
    
#@bot.message_handler(func=lambda msg: msg.text in ['ban', 'Ban'])
#def banlindo(message):
#    bot.reply_to(message, 'Vai dar certo ! Nada de ban aqui :)')    

'''
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
'''

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
    global ocorrencias_comum
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
    lista_usuarios = open("Usuarios.txt", "r", encoding="mac_roman").readlines()
    ocorrencias_comum = collections.Counter(lista_usuarios).most_common()
    open('UsuariosEstatistica.txt', 'w', encoding="utf-8").writelines(str(ocorrencias_comum))


       
# New group member
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def new_member(message):
    bot.reply_to(message, 'Bem vindo, ' + str(message.new_chat_member.first_name) + '! Já deu o cu ?')
    regras(message)
    print('olá '+str(message.new_chat_member.username))
    #bot.kick_chat_member(message.chat.id, message.new_chat_member.id, None)

# Removed group member
@bot.message_handler(func=lambda m: True, content_types=['left_chat_member'])
def remove_member(message):
    bot.reply_to(message, 'Bye ' + str(message.left_chat_member.first_name))
    print('bye '+str(message.left_chat_member.username))
    

# Send my curriculum
#@bot.message_handler(func=lambda msg: msg.text == 'meu curriculo' or msg.text == 'meu currículo' or msg.text == 'currículo' or msg.text == 'curriculo')
@bot.message_handler(func=lambda msg: msg.text in ['currículo', 'meu currículo', 'curriculo','meu curriculo'])
def curriculo(message):
    #doc = open('curriculo_luiseduardopompeu.pdf', 'rb')
    #bot.send_document(message.chat.id, doc)
    pass

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