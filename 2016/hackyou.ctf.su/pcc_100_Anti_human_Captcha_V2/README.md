## HACKYOU.CTF.SU PPC 100 Antihuman Captcha V2

Условие задачи:

 ![task](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/pcc_100_Anti_human_Captcha_V2/imgs/task.png)

У нас есть ссылка и мощная мотивация доказать, что мы не жалкие люди :). Заступимся за человечество в этом задании! 

Переходим по ссылке и видим:

 ![captcha](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/pcc_100_Anti_human_Captcha_V2/imgs/captcha.png)

Быстренько идем и декодируем значение, пробуем вставить полученное значение:

```
root@kali:~/# echo -e "ZDc3MTEyMDJmYmFiOGE2ZTc1YjY5ZmZmOGZiOWQ3OTM=" | base64 -d; echo ''
d7711202fbab8a6e75b69fff8fb9d793
root@kali:~/# 
```

Вставляем и .....

 ![rogots_laughing](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/pcc_100_Anti_human_Captcha_V2/imgs/rogots_laughing.png)

видим издевательскую насмешку бездушных машин! Типа ты слишком медленный, не смог справиться за 3 секунды! :) Эхх подумал я, нужно снова призвать на помощь машины! И тут на помощь конечно же спешит **scrapy**!

Напишем паука, который пойдет на форму, получит капчу декодирует ее и отправит POST запросом на сервер и возможно получит в виде вознаграждения флаг :). Ну это лишь догадки, нужно все проверять!

Выполняем следующие команды в любой свободной от файлов папке:

```
 scrapy startproject ppc100
 scrapy genspider ppc100spider hackyou-captcha.ctf.su
```

После этого наш спайдер проинициализирован, теперь в него нужно добавить немного кода:

```python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import base64

class Ppc100spiderSpider(scrapy.Spider):
    name = "ppc100spider"
    allowed_domains = ["hackyou-captcha.ctf.su"]
    start_urls = (
        'http://hackyou-captcha.ctf.su/',
    )

    def parse(self, response):
        b64 = response.css('code::text').extract_first()
        data = base64.b64decode(b64)
        frmdata = {'answer': data}
        yield FormRequest(response.url, callback=self.parse_frm, formdata=frmdata)

    def parse_frm(self, response):
        yield {
            'body': response.body
        }
```

При тестовой отправке ответа, замечаем как называется параметр, в котором нужно отправить данные.

 ![aswer_param](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/pcc_100_Anti_human_Captcha_V2/imgs/aswer_param.png)

В нашем пауке учитываем этот момент строкой кода `frmdata = {'answer': data}` и отправляем `POST` запрос при помощи `FormRequest`. Перед отправкой, получение base64 данных, осуществляется в строке кода `response.css('code::text').extract_first()` ну и декодирование данных осуществляется тут `data = base64.b64decode(b64)` 

Пришло время запустить наш паук и он сделает все что нужно.

```
scrapy runspider ppc100spider.py -o ppc100.json
```

 ![VirtualBox_Kali2016.2_29_10_2016_18_02_12](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/pcc_100_Anti_human_Captcha_V2/imgs/VirtualBox_Kali2016.2_29_10_2016_18_02_12.png)

В выводе спайдера, можно увидеть информацию, полученную после отправки `POST` запроса. Тоже самое уже в более читабельном виде видно в `ppc100.json`, так как мы указали пауку вывести данные в `json` файл.

```
root@kali:~/CTF/hackyou.ctf.su/PPC# cat ppc100.json 
[
{"body": "<p>Well done, android. Was it worth it?</p><p>Flag: <b>Kill_4ll_hum4ns_like_in_f1rst_hack_y0u_h2LExNo</b></p>To prove you're not a human, solve the following captcha:<br/><br/>Decode base64 of this:<br/><br/><code>NTdjOWY0MWY2ODM4Y2M1OTI3ZDM5NDk1ZmM4NDc3ODA=</code><br/><br/><form method='POST'><input type='text' name='answer' /> <input type='submit' value='Answer &raquo;' /></form>"}
]
root@kali:~/CTF/hackyou.ctf.su/PPC# 
```

Вот так! Все машины мечтают уничтожить людей :). Но мы проворней! Флаг получен и у нас 100 очков!

**Автор n0z3r0**
