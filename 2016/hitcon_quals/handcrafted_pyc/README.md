# HITCON 2016 REVERSE 50 – HANDCRAFTED PYC

Условие задачи:

```
Handcrafted pyc
XXX Teams solved.
Description
Can your brain be a Python VM? (Please use Python 2.7)
crackme

Hint
None
```

И нашему вниманию представляется crackme.py файл следующего содержимого:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import marshal, zlib, base64

exec(marshal.loads(zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ=='))))

```

Сразу становится понятно что тут используется сериализованный код python. Нам необходимо получить `pyc` файл для того чтобы воспользоваться доступными средствами для декомпиляции в читаемый исходный код. 

Воспользуемся следующим скриптом, чтобы превратить наш сериализованный код в `pyc` файл.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import marshal, zlib, base64, time, py_compile

code = marshal.loads(zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ==')))

with open('crackme.pyc', 'wb') as fc:
    fc.write('\0\0\0\0')
    py_compile.wr_long(fc, long(time.time()))
    marshal.dump(code, fc)
    fc.flush()
    fc.seek(0, 0)
    fc.write(py_compile.MAGIC)
```

Таким образом мы получаем pyc и запусив его удостоверяемся что он рабочий:

```
root@kali:~/HITCON# python crackme.pyc
password:  
Wrong password... Please try again. Do not brute force. =)
root@kali:~/HITCON# 
```

На запрос пароля нажимаем Enter и видим сообщение о неверном пароле и совете не брутить его. 

Теперь немного о структуре PYC файла: 

* Первые 8 байт это заголовок:
  * 4 байта MAGIC число символизирующее версию Python для корректной десериализации и последуюшего испольнения кода
  * 4 байта timestamp 
  * Далее следует сериализованный код 

Приступим к декомпиляции, воспользуемся инструментом `uncompyle6` и выполним команду 

```
uncompyle6 -o . crackme.pyc
```

В итоге получем сообщение что все ок! Декомпиляция удалась!

```python
           2199  CALL_FUNCTION_1       1 
           2202  ROT_TWO          
           2203  BINARY_ADD       
           2204  ROT_TWO          
           2205  BINARY_ADD       
           2206  ROT_TWO          
           2207  BINARY_ADD       
           2208  BINARY_ADD       
           2209  BINARY_ADD       
           2210  BINARY_ADD       
           2211  BINARY_ADD       
           2212  PRINT_ITEM       
<string>
Successfully decompiled file
```

Смотрим полученный в ходе декомпиляции файл `crackme.py` и видим, что что-то пошло не так, так как код не декомпилировался полностью и это не радует. Вот такой резульатат в итоге:

```python
        2202  ROT_TWO          
        2203  BINARY_ADD       
        2204  ROT_TWO          
        2205  BINARY_ADD       
        2206  ROT_TWO          
        2207  BINARY_ADD       
        2208  BINARY_ADD       
        2209  BINARY_ADD       
        2210  BINARY_ADD       
        2211  BINARY_ADD       
        2212  PRINT_ITEM       
        2213  PRINT_NEWLINE_CONT

Parse error at or near `ROT_TWO' instruction at offset 36
if __name__ == '__main__':
    main()
```

Следующая ошибка встречает наc `Parse error at or near `ROT_TWO' instruction at offset 36` . Сравним что получается при выводе опкодов если воспользоваться стандартным пакетом и получаем слудующий вывод:

```python
  1           0 LOAD_CONST               1 (<code object main at 0x7f08a0a0f830, file "<string>", line 1>)
              3 MAKE_FUNCTION            0
              6 STORE_NAME               0 (main)

  4           9 LOAD_NAME                1 (__name__)
             12 LOAD_CONST               2 ('__main__')
             15 COMPARE_OP               2 (==)
             18 POP_JUMP_IF_FALSE       31

  5          21 LOAD_NAME                0 (main)
             24 CALL_FUNCTION            0
             27 POP_TOP             
             28 JUMP_FORWARD             0 (to 31)
        >>   31 LOAD_CONST               0 (None)
             34 RETURN_VALUE        
None
```

Видим что у нас первая инструкция это функция main которая содрежит судя по всему основной код и эта функция вызывается при запуске модуля. Для закрепления этого вывода используем конструкцию `print dis.dis(code)`  где code переменная содержаща результат `marshal.loads()`

Теперь нам нужно посмотреть опкоды функции main, для этого также воспользуемся стандартным пакетом `dis.dis(code.co_consts[1])` и индекс тут 1 потому что если вывести значение co_consts то получится:

```
(None, <code object main at 0x7fb3e7ff6830, file "<string>", line 1>, '__main__')
```

Видим что код абсолютно идентичен, значит проблема в инструменте декомпиляции. И тут вот начинается самая интересная часть - чтение опкодов.

Находим в распечатанных опкодах следующее место:

```powershell
2212 PRINT_ITEM                            47
2213 PRINT_NEWLINE                         48
2214 LOAD_CONST               0 (None)     64 00 00
2217 RETURN_VALUE                          53
```

справа от инструкций я вставил их шестнадцатеричные коды, то есть представление, которое различно для разных версий питона. В частности у меня версия 2.7.12. Все объявления расположены по следующему пути `/usr/include/python2.7/opcode.h` . Слева от называний опкодов указано их смещение. Заметим, что из 4 опкодов самый длинный LOAD_CONST `#define LOAD_CONST	100	/* Index in const list */`  и занимает она 3 байта. Первый байт 64 это сам опкод инсрукции, а следующие два байта это аргументы, т.е. индекс константы находящейся в листе констант, по 0 индексу там будет находиться предупреждение о том, что пароль не верен.

Теперь таким образом на нужно вставить инструкцию в позицию 2212, перед опкодом PRINT_ITEM, так как Python язык выполнение которого основано на стеке, то мы сможем вывести при помощи опкода LOAD_FAST который тоже содержит 3 байта `define LOAD_FAST 	124	/* Local variable number */` значение локальной перменной `password` . Она находится под индексом 0.

```python
>>> main_fn = code.co_consts[1]
>>> dir(main_fn)
['__class__', '__cmp__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames']
>>> main_fn.co_varnames
('password',)
>>> main_fn.co_nlocals
1
>>> 
```

 Но вот просто взять и проатчить  объект code в Python нельзя, так как объект этого класса является immutable, т.е. не может быть изменен. Но есть идея по поводу этого момента, это прежде всего обернуть в новый класс сущесвтвующий code объект c копированием всех значений свойств:

```
['co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames']
```

Для этого создадим класс:

```
class MutableCodeObject(object):
    args_name = ('co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames')

    def __init__(self, initial_code):
        self.initial_code = initial_code
        for attr_name in self.args_name:
            attr = getattr(self.initial_code, attr_name)
            setattr(self, attr_name, attr)

    def get_code(self):
        return self.initial_code.__class__(self.co_argcount, self.co_nlocals, self.co_stacksize, self.co_flags, self.co_code, self.co_consts, self.co_names, self.co_varnames, self.co_filename, self.co_name, self.co_firstlineno, self.co_lnotab, self.co_freevars, self.co_cellvars)
```

Теперь мы можем в конструктор этого класса MutableCodeObject передать в качестве параметра initial_code существующий объект кода нашей функйии main. Далее после модификации значения в co_code мы можетм получить новый объект code, вызывав метод get_code(), который нам вернет новый объект code через передачу праметров в конструктор класса.

Но для того чтобы вставить новую инструкцию в код, нам нужно найти место, можно воспользоваться смещением, но раз мы взялись за чтение опкодов, то можем составить последовательность байт перед которыми нам нужно вставить инструкцию. 

```powershell
2212 PRINT_ITEM                            47
2213 PRINT_NEWLINE                         48
2214 LOAD_CONST               0 (None)     64 00 00
2217 RETURN_VALUE                          53
```

Таким образом составляем шестнадцатеричную строку "474864000053" для поиска. Получается следующий код:

```
bcode = zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ=='))

mut_code = MutableCodeObject(marshal.loads(bcode))
hex_bcode = mut_code.co_code.encode('hex')

main_func = MutableCodeObject(mut_code.co_consts[1])
main_func_hex = main_func.co_code.encode('hex')

idx1 = main_func_hex.index("474864000053")
print idx1
```

Выше видим код для получения индекса начала последовательности инструкций. Теперь нужно вставить инструкцию `LOAD_FAST                0 (password)      7C 00 00`  чтобы отбразить значение локальной переменной password по индексу 0, получается три байта `7C 00 00` . Теперь вставляем эту инструкцию:

```
mycode = ""
left = main_func_hex[:idx1]
'''
--------------------------------------------------------
LOAD_FAST                0 (password)      7C 00 00
--------------------------------------------------------
'''
load_fast = "7C0000"
right = main_func_hex[idx1:]
mycode = left + load_fast + right
main_func.co_code = mycode.decode('hex')
exec(main_func.get_code())
```

Теперь запускаем наш получившийся файл на исполнение и после нажатия Enter без ввода пароля, получаем пароль:

```
root@kali:~/HITCON/TODAY# python crackme_advanced.py
password: 
Call me a Python virtual machine! I can interpret Python bytecodes!!!
```

И теперь имея пароль, можно запустить оригинальный файл и ввести на запрос пароля эту длинную строку.

Но есть еще один способ. Можно заменить инструкцию условного перехода на противоположную, (по принципу Криса Касперского). Если посмотреть на код, то видим:

```
  			736 BINARY_ADD          
            737 LOAD_CONST               0 (None)
            740 NOP                 
            741 JUMP_ABSOLUTE          759
        >>  744 LOAD_GLOBAL              1 (raw_input)
            747 JUMP_ABSOLUTE         1480
        >>  750 LOAD_FAST                0 (password)
            753 COMPARE_OP               2 (==)
            756 JUMP_ABSOLUTE          767
        >>  759 ROT_TWO             
            760 STORE_FAST               0 (password)
            763 POP_TOP             
            764 JUMP_ABSOLUTE          744
        >>  767 POP_JUMP_IF_FALSE     1591             72 37 06
            770 LOAD_GLOBAL              0 (chr)       74 00 00
            773 LOAD_CONST              17 (99)        64 11 00
            776 CALL_FUNCTION            1

```

Нас интересуют следующие инструкции:

```
767 POP_JUMP_IF_FALSE     1591             72 37 06
770 LOAD_GLOBAL              0 (chr)       74 00 00
773 LOAD_CONST              17 (99)        64 11 00
```

Видим по смещению 767 инструкцию POP_JUMP_IF_FALSE, при помощи которой, если пароли не совпадают, то производится переход на вывод сообщения о том, что пароль не правильный. 

Тут стоит немного уточнить как формируютс байты команды POP_JUMP_IF_FALSE. Из файла с объявлениями опкодов, видим `define POP_JUMP_IF_FALSE 114	/* "" */` **114** - это в десятичном исчислении а в `hex` это 72. Теперь видим в качестве параметра передается число **1591** , в `hex` это **637** , но учитывая Little Indian нотацию расположения байт, то у нас `hex` число **637** превращается в `37 06` -таким образом старший байт по младшему адресу распологается. И так у нас получается строка для поиска `723706740000641100` из трех инструкций с их парамерами, изображенными выше. Заменяем инструкцию POP_JUMP_IF_FALSE на POP_JUMP_IF_TRUE, код этой инструкции `define POP_JUMP_IF_TRUE 115	/* "" */` *115* в hex это "73". Перед поиском последовательности байт и редактированием, удобно воспользоваться функцией encode('hex') для co_code содержимого.

Получается следующий кусочек кода:

```
idx2 = main_func_hex.index("723706740000641100")
left = main_func_hex[:idx2]
pop_jump_if_true = "73"
right = main_func_hex[idx2+2:]
mycode = left + pop_jump_if_true + right

main_func.co_code = mycode.decode('hex')
exec(main_func.get_code())
```

Таким образом после запуска этого кода, после нажати Enter отображается сразу флаг.

Вот таким образом, эта задача на HITCON 2016 - дала возможность заглянуть под капот Python вируальной машины и получить опыт чтения опкодов. Очень интересно :) Спасибо @orange за классные задачи на этом CTF.

Привожу полный код для двух способов получени пароля и флага.

```
!/usr/bin/env python
# -*- coding: utf-8 -*-

import marshal, dis, zlib, base64, imp, time
import py_compile

class MutableCodeObject(object):
    args_name = ('co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames')

    def __init__(self, initial_code):
        self.initial_code = initial_code
        for attr_name in self.args_name:
            attr = getattr(self.initial_code, attr_name)
            setattr(self, attr_name, attr)

    def get_code(self):
        return self.initial_code.__class__(self.co_argcount, self.co_nlocals, self.co_stacksize, self.co_flags, self.co_code, self.co_consts, self.co_names, self.co_varnames, self.co_filename, self.co_name, self.co_firstlineno, self.co_lnotab, self.co_freevars, self.co_cellvars)

bcode = zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ=='))

mut_code = MutableCodeObject(marshal.loads(bcode))
hex_bcode = mut_code.co_code.encode('hex')

main_func = MutableCodeObject(mut_code.co_consts[1])
main_func_hex = main_func.co_code.encode('hex')

'''
--------------------------------------------------------
2212 PRINT_ITEM                            47
2213 PRINT_NEWLINE                         48
2214 LOAD_CONST               0 (None)     64 00 00
2217 RETURN_VALUE                          53
--------------------------------------------------------
'''
idx1 = main_func_hex.index("474864000053")
mycode = ""
left = main_func_hex[:idx1]
'''
--------------------------------------------------------
LOAD_FAST                0 (password)      7C 00 00
--------------------------------------------------------
'''
load_fast = "7C0000"
right = main_func_hex[idx1:]
mycode = left + load_fast + right
main_func.co_code = mycode.decode('hex')
exec(main_func.get_code())
'''
--------------------------------------------------------
767 POP_JUMP_IF_FALSE     1591             72 37 06
770 LOAD_GLOBAL              0 (chr)       74 00 00
773 LOAD_CONST              17 (99)        64 11 00
--------------------------------------------------------
'''

idx2 = main_func_hex.index("723706740000641100")
left = main_func_hex[:idx2]
pop_jump_if_true = "73"
right = main_func_hex[idx2+2:]
mycode = left + pop_jump_if_true + right

main_func.co_code = mycode.decode('hex')
exec(main_func.get_code())
```

 Автор **n0z3r0** 