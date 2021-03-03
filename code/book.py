Пункты книги с кодом
Created: Monday, August 10, 2020 08:23:17 AM GMT Raw Modify Original

 #Quick reference for ESP32 with MicroPython:
 #https://docs.micropython.org/en/latest/esp32/quickref.html
 #==================================================================================
 import machine, utime, i2c_lcd, dht
 
 LED_PIN_LIST = [2,4,5,12,13,14,15,16,17,18,19,21,22,23,25,26,27,32,33]
 BUTTON_PIN_LIST = [2,3,4,5,12,13,14,15,16,17,18,19,21,22,23,25,26,27,32,33,34,35,36,39]
 PWM_PIN_LIST = [2,4,12,13,14,15,16,177,18,19,21,22,23,24,25,26,27,32,33,34,35,36,39]
 ADC_PIN_LIST = [32,33,34,35,36,39]
 
 #==================================================================================
 '''
 доделать систему документации
 __doc__ = {}
 
 def setdoc(thing, doc):
     __doc__[thing] = doc
 
 def doc(thing):
     print(__doc__[thing])
 
 def foo(a, b={}):
     return a,b
 
 setdoc(foo, 'foo(a, b={})\nreturns a and b')
 '''
 #==================================================================================
 #==================================================================================
 #==================================================================================
 '''
 - ### Введение
   - **---**
 '''
 #==================================================================================
 '''
 - ### Глава 1 - Кружок робототехники
 >>> print('Hello, world')
 '''
 #==================================================================================
 '''
 - ### Глава 2 - Королевство АРМа
 '''
 #==================================================================================
 '''
 - ### Глава 3 - Долина Терминала
       - **1 задание (пример для понимания)**
 >>> 2+2*2
 >>> a = 10
 >>> b = (12+5)*10
 >>> print(b)
 #      - **2 задание (пример для понимания)**
 >>> A = True
 >>> B = True
 >>> C = False
 >>> A and B
 >>> A or B
 >>> A and B or C
 >>> B and C or A
 >>> not A
 #      - **3 задание (пример для понимания)**
 >>> U = 220
 >>> R = 55
 >>> I = U/R
 >>> print(I)
 '''
 #==================================================================================
 '''
 - ### Глава 4 - Светодиодный лес
 '''
 # Function for Chapter 4 - LED control
 
 #default values:  None/0/1          0 sec           1 sec           1 sec
 def led(pin_num, resume=None, working_time=None, on_delay=1000, off_delay=1000):
     # выводы с поддержкой OUTPUT сигнала:
     assert pin_num in LED_PIN_LIST, 'Вывод указан неверно (%r)' % pin_num
     assert resume [None,0,1], 'Режим работы указан неверно (%r)' % resume
     pin = machine.Pin(pin_num, machine.Pin.OUT)
     power = {0:pin.off, 1:pin.on}
     # если не указано время мигания светодиода, то
     if working_time == None:
         # если явно не указано состояние, то
         if resume == None:
 	    # при каждом вызове функции меняем состояние светодиода на противоположное
             if pin.value() == 0:
                 pin.on()
                 print('Вкл')
             else:
                 pin.off()
                 print('Выкл')
         # если режим работы указан явно, то устанавливаем это состояние на выводе
         else:
             power[resume]()
     # если же указано время мигания, то
     else:
         now = utime.time()
         # включаем светодиод на время <on_delay> и выключаем на время <off_delay> до тех пор,
         # пока не истечёт время <working_time>
         while now+working_time > utime.time():
             pin.on()
             utime.sleep_ms(on_delay)
             pin.off()
             utime.sleep_ms(off_delay)
         # по истечении времени светодиод будет выключен
         else:
             pin.off()
 #==================================================================================
 '''
 - ### Глава 5: Старейшее дерево в королевстве
 '''
 # Functions for Chapter 5 - PWM LED control and potentiometr
 
 #default values:    50%       5kHz
 def pwm(pin_num, duty=512, freq=5000):
     '''Разрешение ШИМ-сигнала - 10-16 бит. по-умолчанию диапазон значений 0-1023, но можно указывать 1024-2047, 2048-3071, 3072-4095 и т.д.
     duty - коэффициент заполнения, задаётся в значении 0-1023 (0-100%) и отображает длительность
     высокого сигнала в каждом импульсе
     freq - частота импульсов в секунду, задаётся в значении от 1 Гц до 40 МГц
     При увеличении частоты уменьшается диапазон значений коэффициента заполнения'''
     assert pin_num in PWM_PIN_LIST, 'Вывод указан неверно'
     assert duty in range(0, 1024), 'Значение ШИМ указано неверно'
     assert freq in range(1, 40000000), 'Частота указана неверно'
     machine.PWM(machine.Pin(pin_num), freq, duty)
 
 #default values:              0-1023       0-3.6V
 def potentiometer(pin_num, width_res=10, attn_res=11):
     '''https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html
     На плате ESP32 имеется 2 Аналогово-Цифровых Преобразователя:
     -- АЦП1 (8 каналов, выводы 32-39)
     -- АЦП2 (10 каналов, выводы 0,2,4,12-15,25-27)
     Однако, АЦП2 имеет некоторые ограничения в работе: он используется при работе Wi-Fi адаптера.
     Таким образом АЦП2 может быть использован только при выключенном WiFi.
     Также ряд выводов используется для обвязки платы (выводы 0,2,15), поэтому их использование ограничено.
     С учётом вышесказанного, свободно используемыми в любой момент времени могут считаться только выводы АЦП1 (выводы 32-39)'''
     #выбираем диапазон возвращаемых значений:
     #        0-511    0-1023     0-2048     0-4095
     widths = {9:0,     10:1,      11:2,      12:3}
     #выбираем диапазон напряжения на входе:
     #        0-1V  0-1.34V     0-2V    0-3.6V    
     attns = {0:0,   2.5:1,     6:2,    11:3}
     assert pin_num in ADC_PIN_LIST, 'Вывод указан неверно'
     assert width_res in widths, 'Диапазон полученных значений задан неверно. Укажите 9[0-511],10[0-1023],11[0-2047] или 12[0-4095]'
     assert attn_res in attns, 'Диапазон считываемого напряжения задан неверно. Укажите 0[0-1В], 2.5[0-1.34В], 6[0-2В] или 11[0-3.6В]'
     adc = machine.ADC(machine.Pin(pin_num))
     adc.read()
     adc.width(widths[width_res])
     adc.atten(attns[attn_res])
     return adc.read()
 #==================================================================================
 '''
 - ### Глава 6 - Канатная дорога
 '''
 # Functions for Chapter 6 - ServoMotor and Motor control
 
 # Функция пересчёта из диапазона [fromLow, fromHigh] в диапазон [toLow, toHigh]:
 def rescale(value, in_min, in_max, out_min, out_max):
     return (value-in_min)*(out_max-out_min)//(in_max-in_min)+out_min
 
 def servomotor(pin_num, angle, freq=50):
     '''https://docs.micropython.org/en/latest/esp8266/tutorial/pwm.html#control-a-hobby-servo
     Хобби-сервомоторами можно управлять с помощью ШИМ-сигнала. Рабочая частота - 50Hz,
     а коэффициент заполнения должен иметь значения в диапазоне от 40 до 115 (центральное
     положение сервомотора будет при коэффициенте заполнения = 77)
     http://wiki.amperka.ru/articles:servo
     https://www.pololu.com/blog/17/servo-control-interface-in-detail'''
     assert pin_num in PWM_PIN_LIST, 'Вывод указан неверно'
     assert freq in range(1500), 'Частота указана неверно'
     assert angle in range(181), 'Угол задан неверно'
     if freq == 50:
         angle = rescale(angle, 0, 180, 40, 115)
     elif freq == 100:
         angle = rescale(angle, 0, 180, 80, 230)
 
     # !!!!!
     # ПЕРЕПРОВЕРИТЬ ЗНАЧЕНИЯ ПОСЫЛАЕМЫЕ НА СЕРВОМОТОР
     # !!!!!
     
     machine.PWM(machine.Pin(pin_num), freq, angle)
 
 #default values                  50%         R         100 Hz
 def motor(pin_left, pin_right, speed=50, direction=1, freq=100):
     '''Управление мотором постоянного напряжения осуществляется с помощью Н-моста.
 
                   (ТР 1)--          --(TР 2)
                          |          |
                          |---(M) ---|
                          |          |
                   (ТР 3)--          --(TР 4)
 
     example of scheme: https://content.instructables.com/ORIG/F49/AH63/IU2GYM9Z/F49AH63IU2GYM9Z.png
     
     На транзисторы 1-4 или 2-3 подаётся напряжение и на мотор подаётся питание. При смене
     направления движения необходимо подать питание на других пару транзисторов. Подавать питание
     сразу на все транзисторы нельзя, это приведёт к короткому замыканию. Именно поэтому при смене
     направления движения один вывод всегда должен быть отвязан во избежание подачи питания сразу
     на обе пары транзисторов.
     
     example of project: https://www.instructables.com/H-Bridge-Motor-Driver-for-Arduino-Using-Transistor/ '''
     assert pin_left in PWM_PIN_LIST and pin_right in PWM_PIN_LIST , 'Выводы указаны неверно'
     assert speed in range(0, 101), 'Скорость указана неверно'
     assert direction in [0,1], 'Направление указано неверно'
     assert freq in range(1, 25000000), 'Частота указана неверно'
     duty = rescale(speed, 0, 100, 0, 1023)
     if direction == 1:
         machine.PWM(machine.Pin(pin_left)).deinit()
         machine.PWM(machine.Pin(pin_right), freq, duty)
     else:
         machine.PWM(machine.Pin(pin_right)).deinit()
         machine.PWM(machine.Pin(pin_left), freq, duty)
 #==================================================================================
 '''
 - ### Глава 7 - Крепость
 '''
 #==================================================================================
 '''
 - ### Глава 8 - Королевская библиотека
 '''
 #==================================================================================
 '''
 - ### Глава 9 - Королевский сад
 '''
 # Function for Chapter 9 - Buttons and Buzzers control
 
 #                  прижата к земле
 def button(pin_num, resume=0):
     assert pin_num in BUTTON_PIN_LIST, 'Вывод указан неверно'
     assert resume in [0,1], 'Режим подтяжки указан неверно'
     #    PULL DOWN    PULL UP
     pull = {0:1,        1:2}
     return machine.Pin(pin_num, machine.Pin.IN, pull[resume]).value()
 
 #default values:                             0 sec           1 sec           1 sec
 def buzzer_active(pin_num, resume=None, working_time=None, on_delay=1000, off_delay=1000):
     led(pin_num, resume, working_time, on_delay, off_delay)
 
 #                                   50% времени
 #                                  высокий сигнал
 #                                  и 50% времени
 #                                      низкий
 def buzzer_passive(pin_num, freq=500, duty=512, delay=0):
     assert pin_num in PWM_PIN_LIST, 'Вывод указан неверно'
     assert freq in range(1, 40000000), 'Частота указана неверно'
     assert duty in range(0, 1024), 'Значение ШИМ указано неверно'
     if delay == 0:
         machine.PWM(machine.Pin(pin_num), freq, duty)
     else:
         machine.PWM(machine.Pin(pin_num), freq, duty)
         utime.sleep_ms(delay)
         machine.PWM(machine.Pin(pin_num)).deinit()
 
 '''
 Таблица частот для пианино. 1 октава:
 262 Гц - до3 - C4
 294 Гц - ре3 - D4
 330 Гц - ми3 - E4
 349 Гц - фа3 - F4
 392 Гц - соль3 - G4
 440 Гц - ля3 - A4
 494 Гц - си3 - B4
 Оптимальная длительность - 350мс
 '''
 
 # Пример готовой функции пианино:
 def piano(do,re,mi,fa,sol,la,si,b_do,b_re,b_mi,b_fa,b_sol,b_la,b_si):
     if button(do) == 1:
         buzzer_passive(b_do,freq=262,duty=512)
         utime.sleep_ms(200)
     elif button(re) == 1:
         buzzer_passive(b_re,freq=294,duty=512)
         utime.sleep_ms(200)
     elif button(mi) == 1:
         buzzer_passive(b_mi,freq=330,duty=512)
         utime.sleep_ms(200)
     elif button(fa) == 1:
         buzzer_passive(b_fa,freq=349,duty=512)
         utime.sleep_ms(200)
     elif button(sol) == 1:
         buzzer_passive(b_sol,freq=392,duty=512)
         utime.sleep_ms(200)
     elif button(la) == 1:
         buzzer_passive(b_la,freq=440,duty=512)
         utime.sleep_ms(200)
     elif button(si) == 1:
         buzzer_passive(b_si,freq=494,duty=512)
         utime.sleep_ms(200)
     else:
         buzzer_passive(b_do,freq=262,duty=0)
         buzzer_passive(b_re,freq=294,duty=0)
         buzzer_passive(b_mi,freq=330,duty=0)
         buzzer_passive(b_fa,freq=349,duty=0)
         buzzer_passive(b_sol,freq=392,duty=0)
         buzzer_passive(b_la,freq=440,duty=0)
         buzzer_passive(b_si,freq=494,duty=0)
 #==================================================================================
 '''
 - ### Глава 10 - Происшествие
 '''
 # Functions for Chapter 10 - Accident
 
 #default values              0-1023       0-3.6V
 def smoke_sensor(pin_num, width_res=10, attn_res=11):
     return potentiometer(pin_num, width_res, attn_res)
 
 #default values:     None/0/1          0 sec           1 sec           1 sec
 def relay(pin_num, resume=None, working_time=None, on_delay=1000, off_delay=1000):
     return led(pin_num, resume, working_time, on_delay, off_delay)
 #==================================================================================
 '''
 - ### Глава 11 - Схватка
 '''
 #==================================================================================
 '''
 - ### Глава 12 - На горной дороге
 '''
 # Function for Chapter 12 - Cave
 
 def distance_sensor(trigger_pin, echo_pin, echo_timeout_us=50000):
     '''https://sho0.neocities.org/downloads/8c65ac1b85b79ef3fed8c9a9fa699147.pdf'''
     # Инициируем работу вывода trigger (out)
     trigger = machine.Pin(trigger_pin, mode=machine.Pin.OUT, pull=None)
     # Инициируем работу вывода echo (in)
     echo = machine.Pin(echo_pin, mode=machine.Pin.IN, pull=None)
     # Стабилизируем значения датчика
     trigger.value(0)
     utime.sleep_us(5)
     # Посылаем импульс длительностью 10мкрс
     trigger.value(1)
     utime.sleep_us(10)
     trigger.value(0)
     # Функция `machine.time_pulse_us()` нужна, чтобы вычислить время с момента отправки
     # до момента получения сигнала на выводе echo
     try:
         pulse_time = machine.time_pulse_us(echo, machine.Pin.IN, echo_timeout_us)
     except OSError as ex:
         if ex.args[0] == 110: # 110 = ETIMEDOUT
             raise OSError('Out of range')
         raise ex
     # Для рассчёта расстояния берём значение <pulse_time> в микросекундах и делим его на 2,
     # (так как сигнал прошёл расстояние до препятствия, отразился и вернулся,
     # то есть прошёл расстояние дважды) и делим ещё раз на 29.1, так как скорость
     # звука в воздухе при температуре 20 градусов Цельсия равна 343 м/с, что при
     # пересчёте даёт значение 0.0343 см/мкрс или 1 см за 29.1 микросекунды и
     # в результате получим число сантиметров от сенсора до препятствия.
     # При работе в других температурных условиях см. таблицу скоростей звука!
     cms = (pulse_time/2) / 29.1
     # Если надо ограничить количество знаков после запятой, раскомментируйте следующую строку:
     #return float('{:.Nf}'.format(cms)) # where N - number of decimal points
     # и закомментируйте строку ниже
     return cms
 
 # Пример кода парктроника:
 def parktronic():
     resume = {a:0 for a in range(6)}
     pins = {0:12,1:13,2:14,3:25,4:26,5:27}
     dist = distance_sensor(23,22)
     if dist < 10:
         resume[0]=1
     if dist >= 10 and dist < 50:
         resume[0]=1
         resume[1]=1
     if dist >= 50 and dist < 100:
         resume[0]=1
         resume[1]=1
         resume[2]=1
     if dist >= 100 and dist < 150:
         resume[0]=1
         resume[1]=1
         resume[2]=1
         resume[3]=1
     if dist >= 150 and dist < 200:
         resume[0]=1
         resume[1]=1
         resume[2]=1
         resume[3]=1
         resume[4]=1
     if dist >= 200:
         resume[0]=1
         resume[1]=1
         resume[2]=1
         resume[3]=1
         resume[4]=1
         resume[5]=1
     for i in range(6):
         pin_module_2.led(pins[i],resume[i])
     utime.sleep_ms(10)
 #==================================================================================
 '''
 - ### Глава 13 - Свободные земли
 '''
 # Functions for Chapter 13 - Village
 
 # аппаратный i2c на выводах: SDA-21, SCL-22; программный i2c на выводах: любые OUTPUT выводы
 def LCD(scl_pin, sda_pin, addr=39, height=4, width=20):
     '''https://github.com/dhylands/python_lcd/blob/master/lcd/i2c_lcd.py - library
     https://docs.micropython.org/en/latest/library/machine.I2C.html - i2c doc'''
     i2c = machine.I2C(1, scl=machine.Pin(scl_pin),sda=machine.Pin(sda_pin))
     #для сканирования устройст на шине I2C использовать функцию:
     #i2c.scan()
     return i2c_lcd.I2cLcd(i2c, addr, height, width)
 
 # !!!! как-то надо объяснить использование функции с точкой: lcd.* !!!!
 
 # пример готового кода змейки:
 def game(right_pin, left_pin):
     import random
     random.seed(utime.time())
 
     # display
     lcd = LCD(22,21)
     width, height = 20,4
 
     #symbols:
     lcd.custom_char(0, [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F]) # chr(0) - body
     lcd.custom_char(1, [0x04, 0x08, 0x04, 0x0E, 0x11, 0x11, 0x11, 0x0E]) # chr(1) - apple
 
     # game settings
     MENU, PLAY, LOSE, WIN = 0,1,2,3
     game_state = MENU
     m = [(1,0), (0,-1),(-1,0),(0,1)] # RIGHT, DOWN, LEFT, UP
     md = 0 # m[md]
     now = 0 # timer
     
     # Меняя значение переменной refresh_rate можно менять скорость игры (меньше значение - выше скорость)
     # Так же в игру можно добавить уровни сложности, меняя скорость по мере увеличения длины змейки
     refresh_time = 500000000 # nanosecond  (1sec = 1.000.000.000 nsec)
 
     RpushFlag,LpushFlag = False,False
     xd,yd = 0,0
     xA,yA = 0,0
 
     # snake settings
     lenS = [[0,0]] # start position of snake, len = 1
     xHead,yHead = lenS[-1] # head coordinate
     xEnd,yEnd = lenS[0] # tail coordinate
 
     # apple settings
     newApple = True
 
     def snake_move():
         nonlocal m, md, lenS, width, height, xHead, yHead, xd, yd, xEnd, yEnd
         xEnd,yEnd = lenS[0]
         for i in range(len(lenS)-1):
             lenS[i] = lenS[i+1]
 
         xd,yd = m[md]
         xHead,yHead = lenS[-1]
 
         xHead += xd
         if xHead > width-1:
             xHead = 0
         elif xHead < 0:
             xHead = width-1
 
         yHead += yd
         if yHead > height-1:
             yHead = 0
         elif yHead < 0:
             yHead = height-1
 
         lenS[-1] = [xHead,yHead]
 
         lcd.move_to(xEnd,yEnd)
         lcd.putchar(' ')
 
         for xS,yS in lenS:
             lcd.move_to(xS,yS)
             lcd.putchar(chr(0))
 
     def apple():
         nonlocal lenS, xA, yA, newApple
         while True:
             if newApple == True:
                 newApple = False
                 xA, yA = random.randint(0,width-1), random.randint(0,height-1)
                 if [xA,yA] not in lenS:
                     break
                 else:
                     newApple = True
         lcd.move_to(xA,yA)
         lcd.putchar(chr(1))
 
     def button_check(right_pin, left_pin):
         nonlocal md, RpushFlag, LpushFlag
         if button(right_pin) == 1 and RpushFlag == False:
             md += 1
             if md > 3:
                 md = 0
         elif button(left_pin) == 1 and LpushFlag == False:
             md -= 1
             if md < 0:
                 md = 3
         RpushFlag = button(right_pin)
         LpushFlag = button(left_pin)
         # !!!!!!!
         # на выходе состояние флага будет True, значит для
         # смены его состояния надо пройти цикл ещё раз. Если
         # в это время кнопка будет нажата, то флаг будет True
         # и нажатие будет проигнорировано. Решить этот момент
         # !!!!!!!
 
     def check_pos():
         nonlocal xHead, yHead, lenS, game_state
         for i in range(len(lenS)-1):
             xS,yS = lenS[i]
             if [xHead,yHead] == [xS,yS]:
                 game_state = LOSE
 
     # Начало игры
     while True:
         if game_state == PLAY:
             button_check(right_pin, left_pin)
             # если змейка имеет максимальную длину
             if len(lenS) == 79:
                 game_state = WIN
             # функция создания яблока
             if [xA,yA] == [xHead,yHead]:
                 lenS.insert(0, [xEnd-xd, yEnd-yd])
                 newApple = True
                 apple()
             # обновление экрана
             if now + refresh_time < utime.time_ns():
                 snake_move()
                 check_pos()
                 now = utime.time_ns()
         elif game_state == LOSE:
             game_state = MENU
             lcd.clear()
             lcd.move_to(5,0)
             lcd.putstr('Game over!')
             lcd.move_to(0,2)
             lcd.putstr('Your score: ')
             lcd.putstr(str(len(lenS)))
             utime.sleep_ms(3000)
         elif game_state == WIN:
             game_state = MENU
             lcd.clear()
             lcd.move_to(5,0)
             lcd.putstr('You win!')
             lcd.move_to(2,2)
             lcd.putstr('Your score: ')
             lcd.putstr(str(len(lenS)))
             utime.sleep_ms(3000)
         else:
             lcd.clear()
             lcd.move_to(2,1)
             lcd.putstr('Snake: The Game')
             lcd.move_to(2,3)
             lcd.putstr('Push any button')
             while True:
                 if button(right_pin) == 1 or button(left_pin) == 1:
                     game_state = PLAY
                     now = utime.time_ns()
                     lenS = [[0,0]]
                     xHead,yHead = lenS[-1]
                     newApple = True
                     lcd.clear()
                     apple()
                     lcd.move_to(xHead,yHead)
                     lcd.putchar(chr(0))
                     break
 #==================================================================================
 '''
 - ### Глава 14 - Предпраздничная суета
 '''
 # Fuctions for chapter 14 - smart greenhouse
+from esp32 import hall_sensor
+
+#hall_sensor() - возвращает сырое значение с датчика Холла в виде int-значения
 
 def dht_temperature(pin_num):
     assert pin_num in BUTTON_PIN_LIST, 'Вывод указан неверно'
     utime.sleep(2)
     sensor = dht.DHT11(machine.Pin(pin_num))
     try:
         sensor.measure()
         temp = sensor.temperature()
         return temp
     except OSError as e:
         print('Ошибка чтения данных датчика. Повторите попытку.')
         return -1
 
 def dht_humidity(pin_num):
     assert pin_num in BUTTON_PIN_LIST, 'Вывод указан неверно'
     utime.sleep(2)
     sensor = dht.DHT11(machine.Pin(pin_num))
     try:
         sensor.measure()
         hum = sensor.humidity()
         return hum
     except OSError as e:
         print('Ошибка чтения данных датчика. Повторите попытку.')
         return -1
 
 #default values:             0-1023       0-3.6V
 def light_sensor(pin_num, width_res=10, attn_res=11):
     return potentiometer(pin_num, width_res, attn_res)
 
 #default values:                 0-1023       0-3.6V
 def ground_humidity(pin_num, width_res=10, attn_res=11):
     '''https://wiki.iarduino.ru/page/capacitive-soil-moisture-sensor - тут были описаны условия работы'''
     return potentiometer(pin_num, width_res, attn_res)
 
 # пример кода умной оранжереи:
 def smart_greenhouse():
     # выводы указаны для тестовой сборки
     PUMP_RELAY_PIN=2
     FAN_RELAY_PIN=18
     BUZZER_PIN=12
     LED_PIN=14
     AIR_TEMP_SENS_PIN=23
     AIR_HUM_SENS_PIN=23
     LIGHT_SENS_PIN=35
     GND_HUM_SENS_PIN=39
 
     lcd = LCD(22,21)
 
     air_temp, air_hum, light, gnd_hum = 0,0,0,0
     fan_state, pump_state, led_state = '-','-','-'
 
     def menu():
         lcd.move_to(0,0)
         lcd.putstr('AIR T:')
         lcd.move_to(0,1)
         lcd.putstr('AIR H:')
         lcd.move_to(0,2)
         lcd.putstr('LIGHT:')
         lcd.move_to(0,3)
         lcd.putstr('GND H:')
         lcd.move_to(12,0)
         lcd.putstr('FAN:')
         lcd.move_to(12,1)
         lcd.putstr('PUMP:')
         lcd.move_to(12,2)
         lcd.putstr('LED:')
 
     def measure():
         nonlocal AIR_TEMP_SENS_PIN, AIR_HUM_SENS_PIN, LIGHT_SENS_PIN, GND_HUM_SENS_PIN, air_temp, air_hum, light, gnd_hum
 
         air_temp = dht_temperature(AIR_TEMP_SENS_PIN)
         air_hum = dht_humidity(AIR_HUM_SENS_PIN)
         light = light_sensor(LIGHT_SENS_PIN)
         gnd_hum = ground_humidity(GND_HUM_SENS_PIN)
         
     def control():
         nonlocal FAN_RELAY_PIN, PUMP_RELAY_PIN, BUZZER_PIN, LED_PIN, air_temp, air_hum, light, gnd_hum, fan_state, pump_state, led_state
 
         if air_temp <= 15 or air_hum <= 20:
             relay(FAN_RELAY_PIN, 0)
             buzzer_active(BUZZER_PIN,1)
             utime.sleep_ms(200)
             buzzer_active(BUZZER_PIN,0)
             fan_state = '-'
         elif air_temp >= 35 or air_hum > 80:
             relay(FAN_RELAY_PIN, 1)
             fan_state = '+'
 
         if gnd_hum > 600:
             relay(PUMP_RELAY_PIN, 1)
             buzzer_active(BUZZER_PIN,1)
             utime.sleep_ms(200)
             buzzer_active(BUZZER_PIN,0)
             pump_state = '+'
         elif gnd_hum < 400:
             relay(PUMP_RELAY_PIN, 0)
             pump_state = '-'
 
         if light < 200:
             led(LED_PIN,1)
             buzzer_active(BUZZER_PIN,1)
             utime.sleep_ms(200)
             buzzer_active(BUZZER_PIN,0)
             led_state = '+'
         elif light > 700:
             led(LED_PIN,0)
             led_state = '-'
 
     menu()
 
     while True:
         if len(str(air_temp)) < 2:
             lcd.move_to(7,0)
             lcd.putstr(str(air_temp)+'   ')
         elif len(str(air_temp)) < 3:
             lcd.move_to(7,0)
             lcd.putstr(str(air_temp)+'  ')
 
         if len(str(air_hum)) < 2:
             lcd.move_to(7,1)
             lcd.putstr(str(air_hum)+'   ')
         elif len(str(air_hum)) < 3:
             lcd.move_to(7,1)
             lcd.putstr(str(air_hum)+'  ')
 
         if len(str(light)) < 2:
             lcd.move_to(7,2)
             lcd.putstr(str(light)+'   ')
         elif len(str(light)) < 3:
             lcd.move_to(7,2)
             lcd.putstr(str(light)+'  ')
         elif len(str(light)) < 4:
             lcd.move_to(7,2)
             lcd.putstr(str(light)+' ')
         elif len(str(light)) < 5:
             lcd.move_to(7,2)
             lcd.putstr(str(light))
 
         lcd.move_to(7,3)
         lcd.putstr(str(gnd_hum))
 
         lcd.move_to(17,0)
         lcd.putstr(fan_state)
 
         lcd.move_to(18,1)
         lcd.putstr(pump_state)
 
         lcd.move_to(17,2)
         lcd.putstr(led_state)
 
         measure()
         control()
 #==================================================================================
 '''
 - ### Глава 15 - Долгая дорога назад
 '''
 # Fuctions for chapter 15 - Long-long road
 '''
 Basic WiFi configuration:
 
 import network
 sta_if = network.WLAN(network.STA_IF)
 sta_if.active(True)
 sta_if.scan()                             # Scan for available access points
 sta_if.connect("<AP_name>", "<password>") # Connect to an AP
 sta_if.isconnected()                      # Check for successful connection
 '''
 # возможно, вместо редактирования boot.py стоит сказать про создание main-файла и записей в нём
 def wifi(wifi_name=None, wifi_pass=None):
     '''https://micropython.org/resources/docs/en/latest/library/network.html
     https://micropython.org/resources/docs/en/latest/library/network.WLAN.html'''
     wifi = network.WLAN(network.STA_IF)
     assert wifi.active(True) is True, 'Модуль Wi-Fi не был запущен'
     if wifi.isconnected() is True:
         print("Соединение уже установлено")
         answ = input('Разорвать соединение? y/n\n')
         
         # Возможно, стоит добавить вывод адреса устройства?
         #answ = input('Получить установленные настройки подключения? y/n')
         #if answ == 'y':
         #    # вывод кортежа (ip, subnet, gateway, dns)
         #    wifi.ifconfig()
         #else:
         #    return
 
         # Либо сделать возможность разрывать соединение при повторном вызове функции?
         #wifi.disconnect()
 
         if answ == 'y':
             wifi.disconnect()
             print("Соединение разорвано")
             return
         else:
             return
         
     if wifi_name is None or wifi_pass is None:
         # если имя сети не указано, то выводим список всех доступных сетей
         
         # Возвращает кортеж: имя сети, MAC-адрес сети, канал, уровень сигнала, режим аутентификации, статус сети(видимая/скрытая)
         # Режим аутентификации принимает один из 5 значений: 0 – открытая сеть, 1 – WEP-шифрование, 2 – WPA-PSK-шифрование, 3 – WPA2-PSK-шифрование, 4 – WPA/WPA2-PSK-шифрование
         # print('  Имя сети   |   MAC-адрес   |   Канал   |   Сигнал   |   Режим шифрования   |   Статус сети')
         for i in wifi.scan():
             print(i)
         return
     elif wifi_name is not None and wifi_pass is not None:
         # подключаемся к нужной сети, проверяем статус подключения, вот это всё
         wifi.connect(wifi_name, wifi_pass)
         utime.sleep(5)
         if wifi.isconnected() is True:
             print('Соединение установлено')
             print('Параметры вашего подключения:')
             print(wifi.ifconfig())
             return
         else:
             print('Соединение не установлено. Укажите правильные имя и пароль сети.')
             return
 
 # WEBREPL FILES: https://github.com/micropython/webrepl
 def webrepl_setup():
     print('Сейчас будет выполнена настройка web-редактора.')
     print('В появившемся окне введите Y, после чего задайте пароль и дождитесь перезагрузки модуля.')
     print('После этого установите wifi-соединение и запустите функцию webrepl_start()')
     import webrepl_setup
 
 def webrepl_start():
     print('Сейчас будет выполнен запуск работы с платой через web-редактор')
     print('Ниже будет выведен адрес для соединения с платой вида: ws://192.168.0.104:8266')
     print('Его надо будет указать в окне web-редактора для соединения с платой и ввести ранее созданный пароль')
     print('Для прекращения работы с web-редактором воспользуйтесь функцией webrepl_stop()')
     import webrepl
     webrepl.start()
 
 def webrepl_stop():
     import webrepl
     webrepl.stop()
 #==================================================================================
