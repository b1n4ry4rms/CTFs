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