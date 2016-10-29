## HACKYOU.CTF.SU STEGANO 300 Gemorroy

И так перед нами задача: 

![task](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/task.png)

И кстати как потом окажется, надписи на картинке вполне себе оправданы :), но мне повезло, так как сразу выбрал нужный инструмент и с нахождением информции не замарочился.

И так видим что нас ждем в полном смысле слова "Геморрой" :). Но ничего не расстраиваемся, качаем картинку и начинаем эпопею. Просмотрев на наличине каких либо текстовых данных ничего не обнаруживаем, просмотр при помощи **stegsolve** также ничего не дает, в этот момент я вспомнил про програмку написанную на ruby и называется она **zsteg** https://github.com/zed-0xff/zsteg 

Запустив команду `zsteg steg300_where_8c7f6f7.png` на картинке получил следующий вывод:

 ![VirtualBox_Kali2016.2_29_10_2016_13_16_39](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/VirtualBox_Kali2016.2_29_10_2016_13_16_39.png)

Меня сразу же заинтересовал текст `Whoop, here's the next part! ` ну в общем то я не поверил глазам, типа стего 300 - и вдруг так вот. Но не стоит думать, что тут что-то сразу нам на блюдечке выдадут. У zsteg есть замечательная возможность извлекать нужные обнаруженные секции, чем мы и воспользуемся. 

Выполняем команду `zsteg -E extradata:imagedata steg300_where_8c7f6f7.png > part1.txt` и получаем текст скрытый в данной секции. И что мы видим! А видим мы ASCII ART которым написан URL. 

 ![ascii_art_full_url](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/ascii_art_full_url.png)

B этот url `http://ctf.su/EggNog` и так, видимо продолжение нас ждет по этому URL. Давайте посмотрим что там? Перейдя по URL, видим видео файл, состоящий из различных скомпанованных друг с другом QR кодов.

 ![ctf_su_mp4](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/ctf_su_mp4.png)

В принципе тут сразу же без колебаний пришла мысть о разбиении данного файла на составляющие jpeg картинки. И в этом нам поможет `ffmpeg` . Но для начала качаем файл и затем запускаем следующую команду (перед выполнением команды лучше создать папку и перейти в нее, потому что получится огромное кол-во файлов картинок):

```
ffmpeg -i steg300_video_375bee2.mp4 img%4d.jpg
```

В итоге у нас получается гора картинок на выходе. Я не указывал кол-во кадоров, чтобы уменьшить кол-во картинок потому получилось избыточное кол-во, но это все для того чтобы не пропустить детали.

 ![extraxted_imgs](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/extraxted_imgs.png)

Теперь встал вопрос, а как это всю гору проанализировать? Конечно же автоматизация рулит! И так нужно значит написать скрипт, который в правильном порядке сможет нам выдать информацию скрытую в этих картинках. Для этого воспользуемся библиотеками которые работают с QR кодами и позволяют указать картинку и получить на выходе данные закодированные в ней. У меня получился вот такой скрипт:

```python
import qrtools, os
import sys, io, Image
import glob

line = ""
d = list()

for idx, file in enumerate(sorted(glob.glob("*.jpg"))):
    if idx % 4 == 0:
       qr = qrtools.QR()
       qr.decode(file)
       d.append(qr.data)
       line += chr(int(qr.data.replace('\\','0'),16))

print line
```

Это окончательный вид скрипта. Перед этим я попробовал посмотреть, что же содержится в одном из QR кодов. И увидел что там набор байт, но вот тогда пришла идея собрать их воедино и посмотреть что получается. Но я просчитался в том что в питоне не гарантируется порядок элементов в массиве и нужно значения в нем отсортировать перед использованием, потому когда собрал байты воедино то не смог понять что передо мной. После того как я собрал при помощи выше представленного скрипта, передо мной сложилась правильная кратинка на основе содержимого файла.

После того как я сложил все байты понял что у меня они зачетверились, все из за того что я не указал кол-во кадров и вот как говорится что получилось:

 ![VirtualBox_Kali2016.2_29_10_2016_14_21_47](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/VirtualBox_Kali2016.2_29_10_2016_14_21_47.png) 

Это была Rar архив, его сигнатура `52 61 72 21` а тут как видно из картинки на каждый байт получилось 3 дублирующих. Для того чтобы взять каждый байт через 4 пришлось добавить условие `if idx % 4 == 0:`. В итоге у меня получилась следующая картинка:

 ![VirtualBox_Kali2016.2_29_10_2016_14_25_46](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/VirtualBox_Kali2016.2_29_10_2016_14_25_46.png)

Вот такой маленький архив. Ну теперь дело за малым, нужно поставить програмку unrar и переименовав данный дамп в out3.rar распаковать и увидеть что там лежит. Хотя тут сразу мы видим что внутри архива находится файл флага flag.txt. Вот так вот! 

Выполняем команду `unrar e out3.rar` и получаем наш заветный файл флага! 

 ![VirtualBox_Kali2016.2_29_10_2016_14_35_11](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_300_gemorroy/imgs/VirtualBox_Kali2016.2_29_10_2016_14_35_11.png)

Вот такое приключение получилось на пути получения флага, интересное и познавательное задание :)

**Автор n0z3r0**