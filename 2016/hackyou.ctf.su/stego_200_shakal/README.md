## HACKYOU.CTF.SU STEGANO 200 SHAKAL

Перед нами задача:

 ![task](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_200_shakal/imgs/task.png)

И сразу же наводящий вопрос над картинкой, который немного сбивает с толку. Просмотр через **stegsolve** не дает результата, ибо ничего не находится при смещении и в дополнительных данных, потому пробуем просмотреть содержимое при помощи **strings** утилиты, чтобы найти что нибудь четаемое. Выполняем команду `strings steg200_a086e0c.jpeg`  и получаем следующий вывод:

```
JFIF
http://futureboy.us/
$3br
%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
	#3R
&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
^Gko
NS?7\W
@=Fx
5\<in
wATu$db
	3OM
```

Какая-то ссылка! - подумал я, когда ее увидел и перейдя по ней увидел сайт:

![futureboy](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_200_shakal/imgs/futureboy.png)

Возможно, этот файл был взят с этого сайт, возможно это просто автор решил оставить в метаданных информацию о себе. Но таких совпадений не бывает в CTF и нужно проверять догадки. И тут меня осенила мысль, поискать по слову Stenography и о чудо! На сайте этого человека Alan Eliasen - есть различные инструменты, не только для стенографии. 

Перейдя по ссылке `Stenography` открылась следующая страница:

![futureboy_stegano](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_200_shakal/imgs/futureboy_stegano.png)

Хм ухмыльнулся я! Неужели что-то получится вытащить с использованием его онлайн декодера. Как говорится - нужно пробовать.

Переходим по ссылке `Decode an image` и видим:

![futureboy_decode](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_200_shakal/imgs/futureboy_decode.png)

Форму на котрой нужно загрузить файл, указать пароль (не обязательно), выбрать какой тип данных получиться должен при выводе и нажать на кнопку `Отправить`

Что ж проделываем это! 

 ![flag](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hackyou.ctf.su/stego_200_shakal/imgs/flag.png)

И получаем флаааг! У нас 200 очков в кармане! Вот так вот иногда вроде бы незначащая ссылка с самого начала и большое кол-во информации на странице, может показаться не связной, но как показывает практика, необходимо присматриваться к любой мелочи и проверять все, что было найдено.

**Автор n0z3r0**
