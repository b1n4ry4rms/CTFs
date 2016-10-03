## CTF.COM.UA получение флага PhParanoid (категория reverse)

В задании предлагается некий файл с расширением phb ну и конечно же тест задания:

`RU: Я настоящий параноик! Я прячу все от этого сумасшедшего мира! Я уже обфусцировал исходники своего калькулятора, сорцы javascript` `а на своем сайте, и я не намерен останавливаться! А ты никогда так и не узнаешь, что же я скрываю!`

![task](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/task.png)

Ну что ж начнем! Скачиваем файл `PhParanoid_b7fa460590b3dc2a7662dc0bb633a7d8.phb`  по [ссылке](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/files/PhParanoid_b7fa460590b3dc2a7662dc0bb633a7d8.phb) и начинаем анализ. 

Текст задания наводит на то, что нам пердстоит разобраться с некой обфусцированной страницей, в данном случае случае это php страница. Но при просмотре содержимого страницы посредством hexviewer, замечаем сигнаруту компилятора используемого для данной страницы. 

![VirtualBox_Kali2016.2_03_10_2016_20_28_35](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_Kali2016.2_03_10_2016_20_28_35.png)

Видим что используется некий **bcompiler v0.18** , значит код php скомпилирован и испольняется некую прослойку, которая умеет выполнять такой байт-код. Но теперь встает вопрос, как же можно прочитать содержимое. Google как обычно в помощь, ищем нформацию по такого рода компилятору для PHP. В ходе гугления нахожу пост на StackOverflow.

![bcompiler](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/bcompiler.png)

 На котором ответ на реальный вопрос о декомпиляции заработал всего один голос, печально. В посте ссылки на форум, в одном из постов которого люди поделились декомпилятром и похоже что это то что нужно. 

![forum1](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/forum1.png)

Иду на форум и регистрируюсь. Перехожу по ссылке на пост и вижу описание ПО для декомпиляции. Но тут есть две версии декомпилятора, для Php 5.2 и Php 5.3. Чтобы решить, какой нужно скачать, нужно снова внимательно глянуть в hex содержимое phb файла. 

![VirtualBox_Kali2016.2_03_10_2016_20_34_22](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_Kali2016.2_03_10_2016_20_34_22.png)

Видим интересный путь в значении которого есть упоминание о версии `php` и это `php5.2`. Качаем версию для php5.2 - это [ModeBIphp52ts.rar](http://board.deioncube.in/attachment.php?aid=3868). Далее, следуя из описания, нам нужна будет Windows. Благо у меня есть различные виртуалки c виндой и я выбрал виртуалку с Windows XP. 

![forum2](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/forum2.png)

Скачиваем архив в виртуалку с WinXP, а также сам файл phb для того чтобы декомпилировать его. 

![VirtualBox_WinXPVLx86_Guest_03_10_2016_20_37_36](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_WinXPVLx86_Guest_03_10_2016_20_37_36.png)

После скачивания архива с декомпилятором, распаковываем его и видим файлы представленные на скриншоте выше. У нас имеется версия php.exe интерпретатора PHP под Windows.  В итоге после нескольких проб и ошибок - понял как запускать декомпиляцию, при помощи следущей команды:

`php.exe phpdc.phpr PhParanoid_b7fa460590b3dc2a7662dc0bb633a7d8.phb`

![VirtualBox_WinXPVLx86_Guest_03_10_2016_20_41_51](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_WinXPVLx86_Guest_03_10_2016_20_41_51.png)

В итоге если не перенаправлять ввод в файл, то можно увидет следующую картину в консоле:

![VirtualBox_WinXPVLx86_Guest_03_10_2016_20_42_23](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_WinXPVLx86_Guest_03_10_2016_20_42_23.png)

Оххх класс! Видим что декомпилятор сработал отлично и мы видим обычный PHP код, который можно прочитать и выполнить. В итоге после декомпиляции получаем слудующий кусок кода страницы:

```php
<?php

do {
	$is_secret_exists = false;

	if (isset($secret)) {
		$is_secret_exists = true;
	}
	else {
		break;
	}

	$is_secret_valid = false;
	if (strstr($secret, "The") && (strpos($secret, "The") == 0)) {
		$is_secret_valid = true;
	}

	$c0 = chr(ord($secret[0]) + 20);

	if ((ord($c0) + (-20)) != 84) {
		unset($"c0");
		break;
	}

	$c1 = chr(ord($secret[1]) + (-52));

	if ((ord($c1) + 52) != 104) {
		unset($"c1");
		break;
	}

	$c2 = chr(ord($secret[2]) + (-2));

	if ((ord($c2) + 2) != 101) {
		unset($"c2");
		break;
	}

	$c3 = chr(ord($secret[3]) + (-7));

	if ((ord($c3) + 7) != 114) {
		unset($"c3");
		break;
	}

	$c4 = chr(ord($secret[4]) + (-52));

	if ((ord($c4) + 52) != 101) {
		unset($"c4");
		break;
	}

	$c5 = chr(ord($secret[5]) + 43);

	if ((ord($c5) + (-43)) != 73) {
		unset($"c5");
		break;
	}

	$c6 = chr(ord($secret[6]) + 8);

	if ((ord($c6) + (-8)) != 115) {
		unset($"c6");
		break;
	}

	$c7 = chr(ord($secret[7]) + 1);

	if ((ord($c7) + (-1)) != 78) {
		unset($"c7");
		break;
	}

	$c8 = chr(ord($secret[8]) + (-63));

	if ((ord($c8) + 63) != 111) {
		unset($"c8");
		break;
	}

	$c9 = chr(ord($secret[9]) + 22);

	if ((ord($c9) + (-22)) != 82) {
		unset($"c9");
		break;
	}

	$c10 = chr(ord($secret[10]) + (-10));

	if ((ord($c10) + 10) != 105) {
		unset($"c10");
		break;
	}

	$c11 = chr(ord($secret[11]) + (-55));

	if ((ord($c11) + 55) != 103) {
		unset($"c11");
		break;
	}

	$c12 = chr(ord($secret[12]) + 8);

	if ((ord($c12) + (-8)) != 104) {
		unset($"c12");
		break;
	}

	$c13 = chr(ord($secret[13]) + (-49));

	if ((ord($c13) + 49) != 116) {
		unset($"c13");
		break;
	}

	$c14 = chr(ord($secret[14]) + (-17));

	if ((ord($c14) + 17) != 65) {
		unset($"c14");
		break;
	}

	$c15 = chr(ord($secret[15]) + (-42));

	if ((ord($c15) + 42) != 110) {
		unset($"c15");
		break;
	}

	$c16 = chr(ord($secret[16]) + (-49));

	if ((ord($c16) + 49) != 100) {
		unset($"c16");
		break;
	}

	$c17 = chr(ord($secret[17]) + (-34));

	if ((ord($c17) + 34) != 87) {
		unset($"c17");
		break;
	}

	$c18 = chr(ord($secret[18]) + (-19));

	if ((ord($c18) + 19) != 114) {
		unset($"c18");
		break;
	}

	$c19 = chr(ord($secret[19]) + (-40));

	if ((ord($c19) + 40) != 111) {
		unset($"c19");
		break;
	}

	$c20 = chr(ord($secret[20]) + (-62));

	if ((ord($c20) + 62) != 110) {
		unset($"c20");
		break;
	}

	$c21 = chr(ord($secret[21]) + 13);

	if ((ord($c21) + (-13)) != 103) {
		unset($"c21");
		break;
	}

	$c22 = chr(ord($secret[22]) + 49);

	if ((ord($c22) + (-49)) != 46) {
		unset($"c22");
		break;
	}

	$c23 = chr(ord($secret[23]) + (-35));

	if ((ord($c23) + 35) != 84) {
		unset($"c23");
		break;
	}

	$c24 = chr(ord($secret[24]) + (-26));

	if ((ord($c24) + 26) != 104) {
		unset($"c24");
		break;
	}

	$c25 = chr(ord($secret[25]) + (-48));

	if ((ord($c25) + 48) != 101) {
		unset($"c25");
		break;
	}

	$c26 = chr(ord($secret[26]) + (-65));

	if ((ord($c26) + 65) != 114) {
		unset($"c26");
		break;
	}

	$c27 = chr(ord($secret[27]) + (-33));

	if ((ord($c27) + 33) != 101) {
		unset($"c27");
		break;
	}

	$c28 = chr(ord($secret[28]) + (-28));

	if ((ord($c28) + 28) != 79) {
		unset($"c28");
		break;
	}

	$c29 = chr(ord($secret[29]) + (-15));

	if ((ord($c29) + 15) != 110) {
		unset($"c29");
		break;
	}

	$c30 = chr(ord($secret[30]) + (-31));

	if ((ord($c30) + 31) != 108) {
		unset($"c30");
		break;
	}

	$c31 = chr(ord($secret[31]) + (-16));

	if ((ord($c31) + 16) != 121) {
		unset($"c31");
		break;
	}

	$c32 = chr(ord($secret[32]) + 8);

	if ((ord($c32) + (-8)) != 70) {
		unset($"c32");
		break;
	}

	$c33 = chr(ord($secret[33]) + (-66));

	if ((ord($c33) + 66) != 117) {
		unset($"c33");
		break;
	}

	$c34 = chr(ord($secret[34]) + (-15));

	if ((ord($c34) + 15) != 110) {
		unset($"c34");
		break;
	}

	$c35 = chr(ord($secret[35]) + (-12));

	if ((ord($c35) + 12) != 65) {
		unset($"c35");
		break;
	}

	$c36 = chr(ord($secret[36]) + (-61));

	if ((ord($c36) + 61) != 110) {
		unset($"c36");
		break;
	}

	$c37 = chr(ord($secret[37]) + (-33));

	if ((ord($c37) + 33) != 100) {
		unset($"c37");
		break;
	}

	$c38 = chr(ord($secret[38]) + 9);

	if ((ord($c38) + (-9)) != 66) {
		unset($"c38");
		break;
	}

	$c39 = chr(ord($secret[39]) + (-16));

	if ((ord($c39) + 16) != 111) {
		unset($"c39");
		break;
	}

	$c40 = chr(ord($secret[40]) + (-37));

	if ((ord($c40) + 37) != 114) {
		unset($"c40");
		break;
	}

	$c41 = chr(ord($secret[41]) + (-56));

	if ((ord($c41) + 56) != 105) {
		unset($"c41");
		break;
	}

	$c42 = chr(ord($secret[42]) + 0);

	if ((ord($c42) + 0) != 110) {
		unset($"c42");
		break;
	}

	$c43 = chr(ord($secret[43]) + (-35));

	if ((ord($c43) + 35) != 103) {
		unset($"c43");
		break;
	}

	$c44 = chr(ord($secret[44]) + 79);

	if ((ord($c44) + (-79)) != 46) {
		unset($"c44");
		break;
	}
} while (false);

?>
```

Но получив код, видно что просто так нам не дадут флаг организаторы CTF. Видим кучу if конструкций из которых следует что тут проверяется наличие некого секрета, который начинается с "The". 

Значит нам следует понять как получить строку `$secret` . Из листинга кода видно что идет проверка кодов символов на соответсвие определенному значению, к примеру `if ((ord($c44) + (-79)) != 46) {` . Значит у нас имеются коды символов секрета! Так превратим же их в читаемую строку, при помощи bash скрипта и python.

![VirtualBox_Kali2016.2_03_10_2016_21_08_53](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_Kali2016.2_03_10_2016_21_08_53.png)

Выполним вот эту команду `python -c "print ''.join([chr(x) for x in $(echo "[$(cat decoded.txt | grep -o -P '(?<=\!\=).*(?=\))' | tr '\n' ',' | sed 's/,$//')]")])"`  которая парсит значения между `!=` и `)` , а затем при помощи python получаем строку из этих кодов символов секрета. В итоге у нас получается значение секрета: 

`ThereIsNoRightAndWrong.ThereOnlyFunAndBoring. `

Но это еще не флаг, а всего лишь секрет которым проверяется значение каждого символа ключа. Теперь нам предстоит получить значение флага и тут снова приходит на помощь bash и  python. Для этого нам нужно применить другой способ для парсинга, теперь нам нужны все значения в следующих строках `$c41 = chr(ord($secret[41]) + (-56))`  то есть нас интересует число -56, а таже есть еще один вариант `$c44 = chr(ord($secret[44]) + 79);` где число `+79` не в скобках. Но для этого мы будем использовать другое выражение и будем искать все что находится между `]) + ` и скобкой `)` . В итоге получается следующее выражение:

`python -c "print ''.join([chr(ord('ThereIsNoRightAndWrong.ThereOnlyFunAndBoring.'[i]) + x) for i, x in enumerate($(echo "[$(cat decoded.txt | grep -o -P '(?<=\]\)\s\+\s).*(?=\))' | tr -d '()' | tr '\n' ',' | sed 's/,$//')]"))])"`

Таким образом мы проходимся по каждому символу нашего секрета и производим операцию сложени для каждого кода символа и числом, которое используется для проверки соответствия с секретом. Таким образом мы восставновим строку с флагом. 

![VirtualBox_Kali2016.2_03_10_2016_21_35_45](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/ctf.com.ua/PhParanoid/imgs/VirtualBox_Kali2016.2_03_10_2016_21_35_45.png)

Урааа у нас получилось! Вот он - `h4ck1t{O0h_0pC0D35_G0t_1N51D3_MiN3_51CK_M1nD}` !!! 

И таким образом получаем +250 поинтов к счету команды b1n4ry4rms! 

**Автор: n0z3r0**



