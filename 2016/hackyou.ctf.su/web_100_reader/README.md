## HACKYOU.CTF.SU WEB 100 READER

Перед нами условие задачи:

 ![task](imgs\task.png)

И перед нами файлик с собранным трафиком, хм и еще сопутствующая информация! Мол перехватили тут для нас кое какую информацию. Спасибо большое :) 

Приступим к анализу `pcap` файла, для этого нам поможет `Wireshark`

![WEB_100_1](imgs\WEB_100_1.png)

Видим что и вправду записан HTTP трафик, первое что приходит в голову это конечно же `Follow HTTP stream`. Если воспользоваться командой `Follow TCP steam` то gzip данные не будут декодированы, так что это надо иметь ввиду.

 ![WEB_100_2](imgs\WEB_100_2.png)

Тут много информации в выводе команды, листаем в самый низ, походу замечаем, что используется basic авторизация и человек реально пытается войти и несколько раз вводит разные пароли и вот под конец файла, у него получается наконец-то войти. Мы также видим, что пользователь проходит на страницу и видит интересное содержимое! Вроде бы кажется, что вот по этой ссылке пройдешь и получишь флаг. 

Ан нет! Для начала мы должны получить пароль. Мы знаем, что basic auth - это не надежно, несмотря на то, что логин и пароль передаются в base64, их все равно можно декодировать и увидеть. Формат записи закодированной в base64 - это `логин:пароль`  через двоеточие.  

Выполним команду `echo -e cmVhZGVyOnA0JCR3b3JkVEhOT1EwbjJEMQ== | base64 -d; echo ''`  в итоге получаем вывод:

 ![VirtualBox_Kali2016.2_29_10_2016_16_04_34](imgs\VirtualBox_Kali2016.2_29_10_2016_16_04_34.png)

Таким образом у нас есть `логин:пароль` и из дампа, а также мы видим URL по которому нужно пройти - это конечно же `http://hackyou-web100.ctf.su` 

Ну что ж, пойдем по этой ссылке и поглядим, как там будет дело обстоять.

  ![basic_auth_prompt](imgs\basic_auth_prompt.png)

И нас встречает до боли родной basic auth диалог авторизации. Пароль и логин мы знаем, входим!

 ![500_files](imgs\500_files.png)

И тут нас ждет разоварование! Очень много файлов на странице и нет даже намека, что вообще где-то расположен файл flag.txt. Поиск по его размеру ничего не дает. И вообще содержимое файлов вот такое:

 ![file_confuse](imgs\file_confuse.png)

Мда и такая картина с разлиным размером очень похожего текста, при просмотре следующих файлов из списка. Это какой-то ад :) просматривать это все вручную не реально и тут я вспомнил что есть же `scrapy`, которым можно быстренько пройтись по всем ссылкам и вытащить инфу! 

Ну что ж, создадим проект scrapy паука, выполняем следующие команды:

```
 pip install scrapy
 scrapy startproject web100
 scrapy genspider web100spider hackyou-web100.ctf.su
```

Теперь нам нужно поправить содержимое паука.

```python
# -*- coding: utf-8 -*-
import scrapy

class Web100spiderSpider(scrapy.Spider):
    http_user = 'reader'
    http_pass = 'p4$$wordTHNOQ0n2D1'    

    name = "web100spider"
    allowed_domains = ["hackyou-web100.ctf.su"]
    start_urls = (
        'http://hackyou-web100.ctf.su/',
    )

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_page)
    
    def parse_page(self, response):
        
		def extract_with_css(query):
            return response.css(query).extract_first().strip()
        
		yield { 
            'text': extract_with_css('textarea::text') 
        }

```

В данном пауке очень легко указывается логин и пароль для basic авторизации, всего две строчки

```python
http_user = 'reader'
http_pass = 'p4$$wordTHNOQ0n2D1' 
```

Касота да и только! :) Далее указываем, что за пределы `hackyou-web100.ctf.su` выходить не надо. В процедуре `parse` мы проходимся по всем ссылкам и получаем содержимое `href`, делая сразу же запрос по ссылке (ссылки отображаются сразу после успешной авторизации, нам не нужны доп. манипуляции). В процедуре `parse_page` обрабатывается каждая страница, полученная по ссылке, которая была сформирована процедурой `parse`

В итоге теперь мы можем запустить и посмотреть на результат используя команду 

```
scrapy runspider web100spider.py -o web100.json
```

Таким образом мы запустим краулинг при этом все данные будут записаны в файл `data.json` 

```
root@kali:~/CTF/hackyou.ctf.su/WEB# scrapy runspider web100spider.py -o web100.json
2016-10-29 06:29:11 [scrapy] INFO: Scrapy 1.1.2 started (bot: scrapybot)
2016-10-29 06:29:11 [scrapy] INFO: Overridden settings: {'FEED_FORMAT': 'json', 'FEED_URI': 'web100.json'}
2016-10-29 06:29:12 [scrapy] INFO: Enabled extensions:
['scrapy.extensions.feedexport.FeedExporter',
 'scrapy.extensions.logstats.LogStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.corestats.CoreStats']
2016-10-29 06:29:13 [scrapy] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2016-10-29 06:29:13 [scrapy] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2016-10-29 06:29:13 [scrapy] INFO: Enabled item pipelines:
[]
2016-10-29 06:29:13 [scrapy] INFO: Spider opened
```

После выполнения спайдер выдает нам статистику:

```
2016-10-29 06:29:21 [scrapy] INFO: Closing spider (finished)
2016-10-29 06:29:21 [scrapy] INFO: Stored json feed (337 items) in: web100.json
2016-10-29 06:29:21 [scrapy] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 123620,
 'downloader/request_count': 338,
 'downloader/request_method_count/GET': 338,
 'downloader/response_bytes': 168838,
 'downloader/response_count': 338,
 'downloader/response_status_count/200': 338,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2016, 10, 29, 10, 29, 21, 928400),
 'item_scraped_count': 337,
 'log_count/DEBUG': 676,
 'log_count/INFO': 8,
 'request_depth_max': 1,
 'response_received_count': 338,
 'scheduler/dequeued': 338,
 'scheduler/dequeued/memory': 338,
 'scheduler/enqueued': 338,
 'scheduler/enqueued/memory': 338,
 'start_time': datetime.datetime(2016, 10, 29, 10, 29, 13, 125516)}
2016-10-29 06:29:21 [scrapy] INFO: Spider closed (finished)
```

Получается что он просмотрел 337 ссылок на фалы, выполнил 338 запросов GET и все 338 запросов были со статусом 200. Замечательно! Спайдер отработал очень быстро. В итоге на выходе мы получили json файлик.

Остается проверить по слову `flag` для начала. Выполним команду:

```
cat web100.json | grep flag
```

И сразу же находится одна строка со следующим содержимым:

![flag](imgs\flag.png)

Вот такой вот текст запутывающий :) если бы не автоматизация думаю что можно было бы пропустить запросто, просматривая вручную все файлы. Вот так вот автоматизация рулит и это еще раз доказывает решение вот таких задач на CTFах. Спасибо авторам Scrapy!

**Автор n0z3r0**