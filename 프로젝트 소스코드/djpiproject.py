import pifacecad
import threading
import datetime
import time
import pytz
import os
import _weather
import _gmail
import _icon
import _wifi
from pygame import mixer

#030031


NETWORK = False

now_time_flag = False
network_flag = True
lock = threading.Lock()

event = threading.Event()
ntevent = threading.Event()

alarm_flag = 0

country_index = 0
w_country_index = 0
country = ["Asia/Seoul", "Europe/London", "America/New_York",
                        "America/Vancouver", "Australia/Sydney"]
w_country = ["Seoul/kr", "London/uk", "New_York/us",
                        "Vancouver/cn", "Sydney/as"]

weatherinfo = 0

weather_temp_flag = 0;

gmail_lie = False
unread_number = 0
unread_senders = []
first_run = True


class NowTimeThreadClass(threading.Thread):
    
    utc = pytz.utc

    def __init__(self, event):
        super(NowTimeThreadClass, self).__init__()
        self.event = event
    
    def run(self):
        while(1) :
            if now_time_flag :
                now = datetime.datetime.utcnow().replace(tzinfo=self.utc)
                tz = pytz.timezone(country[country_index])
                localr = tz.normalize(now.astimezone(tz))
                with lock:
                    cad.lcd.blink_off()
                    cad.lcd.set_cursor(0,0)
                    cad.lcd.write(country[country_index].split('/')[1])
                    cad.lcd.write_custom_bitmap(find_icon(weatherinfo['weather']))
                    cad.lcd.set_cursor(0,1)
                    nt = localr.strftime('%H:%M:%S')
                    
                    if nt == '{:02d}'.format(ALARMTIME[0])+":"+'{:02d}'.format(ALARMTIME[1])+":"+'{:02d}'.format(ALARMTIME[2]):
                        global alarm_flag
                        alarm_flag = 1
                        print(alarm_flag)
                        alarm_on()
                        global CURRENTSTATUS
                        CURRENTSTATUS = 0
                        lcd_clear()
                        nowTimeThreadControl(True)
                        networkThreadControl(True)
                    else:    
                        cad.lcd.write(nt)
                        cad.lcd.home()
                time.sleep(0.1)
            else :
                self.event.wait()

class NetworkThreadClass(threading.Thread):
    
    
    def __init__(self, ntevent):
        super(NetworkThreadClass, self).__init__()
        self.ntevent = ntevent
    
    def run(self):
        global NETWORK
        while(1) :
        
            if network_flag :
                
                NETWORK = _wifi.internetcon()
                
                if NETWORK :
                    with lock : 
                        cad.lcd.set_cursor(15,0)
                        cad.lcd.write_custom_bitmap(0)
                        cad.lcd.set_cursor(0,0)
                else :
                    with lock : 
                        cad.lcd.set_cursor(15,0)
                        cad.lcd.write(" ")
                        cad.lcd.set_cursor(0,0)
                if ALARMFLAG == 1 :
                    with lock :                 
                        cad.lcd.set_cursor(14,0)
                        cad.lcd.write_custom_bitmap(1)
                        cad.lcd.set_cursor(0,0)
                else :
                    with lock : 
                        cad.lcd.set_cursor(14,0)
                        cad.lcd.write(" ")
                        cad.lcd.set_cursor(0,0)
                            
                time.sleep(1)#3301333
            else :
                
                self.ntevent.wait()
                
                
            
MAINMODE = 0
WEATHERMODE = 1
GMAILMODE = 2
ALARMMODE = 3
ONOFFBUTTON = 4
SELECT = 5
PREV = 6
NEXT = 7
NAVI = [SELECT ,PREV,NEXT]

CURRENTSTATUS = 0

ALARMFLAG = 0
LCDFLAG = 0
ALARMTIME = [0,0,0]



#################################### event function 332331233333300
def mainmode() :
    if os.system("sudo rdate -s time.bora.net") == 0 :
        with lock :
            lcd_clear()
        nowTimeThreadControl(True)
        networkThreadControl(True)
    
def weathermode(toggle) :
    global weather_temp_flag
    with lock:
        if toggle == False :
            lcd_clear()
            cad.lcd.write(weatherinfo['location'])
            weather_temp_flag = 0
        cad.lcd.set_cursor(8,1)
        cad.lcd.write("        ")
        if weather_temp_flag == 0 :
            cad.lcd.set_cursor(0,1)
            cad.lcd.write(weatherinfo['date'][2:])
            cad.lcd.set_cursor(15-len(weatherinfo['weather']),1)
            cad.lcd.write(weatherinfo['weather'])
            cad.lcd.write_custom_bitmap(find_icon(weatherinfo['weather']))
            weather_temp_flag = 1
        else :
            cad.lcd.set_cursor(0,1)
            cad.lcd.write(weatherinfo['date'][2:])
            cad.lcd.set_cursor(15-len(weatherinfo['temp']),1)
            cad.lcd.write(weatherinfo['temp'])
            cad.lcd.write_custom_bitmap(find_icon("Celsius"))
            weather_temp_flag = 0
        
def gmailmode(first_run=True) :
    with lock:
        lcd_clear()

    global current_status
    global gmail_lie
    global unread_number
    global unread_senders
    
    if gmail_lie == False :
        unreadinfo = _gmail.get_senderinfo_from_gmail()
        unread_number = int(unreadinfo['count'])
        unread_senders = unreadinfo['senders']
    else:
        pass
    with lock:
        if (gmail_lie == False) or (first_run == True):
            lcd_clear()
            cad.lcd.write("unread : ")
            cad.lcd.write(str(unread_number))
            current_status=0
        else:
            cad.lcd.set_cursor(0,1)
            cad.lcd.write("             ")

        cad.lcd.set_cursor(0,1)
        
        if unread_number == 0:
            cad.lcd.write('no information')
            gmail_lie = True
        else:
            cad.lcd.write(str(current_status+1)+". "+unread_senders[current_status])
            gmail_lie = True

def alarmmode() :
    networkThreadControl(False)
    time.sleep(1)
    with lock:
        lcd_clear()
        cad.lcd.write("Alarm")
        cad.lcd.set_cursor(0,1)
        cad.lcd.write('{:02d}'.format(ALARMTIME[0])+":"+'{:02d}'.format(ALARMTIME[1])+":"+'{:02d}'.format(ALARMTIME[2]))
        cad.lcd.write(" SET CLR")
        cad.lcd.set_cursor(0,1)
        cad.lcd.blink_on()
        

def navi_function(button) :
    if CURRENTSTATUS == MAINMODE :
        country_change(button)
    elif CURRENTSTATUS == WEATHERMODE :
        country_change(button)
    elif CURRENTSTATUS == GMAILMODE :
        sender_change(button)
    elif CURRENTSTATUS == ALARMMODE :
        set_alarm(button)

def check_button(event):
    
    global CURRENTSTATUS
    button = event.pin_num
    if button in [WEATHERMODE, GMAILMODE,  ALARMMODE] :
        nowTimeThreadControl(False)
    if button not in NAVI:
        CURRENTSTATUS = button
        
    if button == MAINMODE :
        mainmode()
    elif button == WEATHERMODE :
        weathermode(False)
    elif button == GMAILMODE :
        gmailmode(True)
    elif button ==  ALARMMODE :
        alarmmode()
    elif button == ONOFFBUTTON:
        lcd_alarm_onoff()
    elif button in NAVI :
        navi_function(button)
        
####################################    00333332213
def lcd_init():
    cad.lcd.backlight_on()
    cad.lcd.cursor_off()
    cad.lcd.blink_off()

def lcd_clear():
    cad.lcd.blink_off()
    cad.lcd.home()
    cad.lcd.clear()
    

def nowTimeThreadStart():
    t = NowTimeThreadClass(event)
    t.start()

def networkThreadStart():
    t = NetworkThreadClass(event)
    t.start()

def button_init():
    button_listener = pifacecad.SwitchEventListener(chip = cad)
    for i in range(8):        
        button_listener.register(i, pifacecad.IODIR_FALLING_EDGE, check_button)
    button_listener.activate()

def  nowTimeThreadControl(boolean):
    global now_time_flag
    now_time_flag = boolean
    
    if boolean :
        event.set()

def  networkThreadControl(boolean):
    global network_flag
    network_flag = boolean
    
    if boolean :
        ntevent.set()
    
def country_change(button):
    global country_index
    global w_country_index
    global weatherinfo
    
    if button == PREV :
        with lock:
            lcd_clear()
        if CURRENTSTATUS == MAINMODE :
            if country_index > 0 :
                country_index -= 1
            else :
                country_index = len(country)-1
            weatherinfo = _weather.get_weather_from_place(w_country[country_index])
        elif CURRENTSTATUS == WEATHERMODE :
            if w_country_index > 0 :
                w_country_index -= 1
            else :
                w_country_index = len(w_country)-1
            weatherinfo = _weather.get_weather_from_place(w_country[w_country_index])
            weathermode(False)
    elif button == NEXT :
        with lock:
            lcd_clear()
        if CURRENTSTATUS == MAINMODE :
            if country_index < len(country)-1 :
                country_index+=1
            else :
                country_index = 0
            weatherinfo = _weather.get_weather_from_place(w_country[country_index])
        elif CURRENTSTATUS == WEATHERMODE :
            if w_country_index < len(w_country)-1 :
                w_country_index+=1
            else :
                w_country_index = 0
            weatherinfo = _weather.get_weather_from_place(w_country[w_country_index])
            weathermode(False)
    elif button == SELECT :
        if CURRENTSTATUS == MAINMODE :
            pass
        elif CURRENTSTATUS == WEATHERMODE :
            weathermode(True)
                
def sender_change(button):
        global current_status
        global unread_number

        if button == PREV :
                if current_status<=0:
                    current_status = 0
                    pass
                else:
                    current_status-=1
                    gmailmode(False)
        elif button == NEXT :
            current_status+=1
            if current_status>=unread_number:
                current_status-=1
                pass
            else :
                gmailmode(False)
        elif button == SELECT :
                pass

def set_alarm(button) :
    global ALARMFLAG
    global ALARMTIME
    
    if button == NEXT :
        with lock:
            x = list(cad.lcd.get_cursor())[0]
            if x == 1 or x == 4 :
                cad.lcd.set_cursor(x+2,1)
            elif x == 7 :
                cad.lcd.set_cursor(10,1)
            elif x == 10 or x == 14:
                cad.lcd.set_cursor(14,1)
            else :
                cad.lcd.set_cursor(x+1,1)
    elif button == PREV :
        with lock:
            x = list(cad.lcd.get_cursor())[0]
            if x == 3 or x == 6 :
                cad.lcd.set_cursor(x-2,1)
            elif x == 14 :
                cad.lcd.set_cursor(10,1)
            elif x == 10:
                cad.lcd.set_cursor(7,1)
            elif x == 0 :
                pass
            else :
                cad.lcd.set_cursor(x-1,1)
    elif button == SELECT :
        with lock:
            cad.lcd.blink_off()
            x = list(cad.lcd.get_cursor())[0]
        if x == 0 :
            if int(ALARMTIME[0]/10) == 2 :
                ALARMTIME[0] %= 10
            elif ALARMTIME[0]%10 > 3 and int(ALARMTIME[0]/10) == 1:
                pass
            else :
                ALARMTIME[0] += 10
            with lock:
                cad.lcd.write(str(int(ALARMTIME[0]/10)))
                
        elif x == 1 :
            if int(ALARMTIME[0]/10) == 2 :
                if ALARMTIME[0]%10 == 3 :
                    ALARMTIME[0] -= 3
                else :
                    ALARMTIME[0] += 1
            elif int(ALARMTIME[0]/10) == 1 :
                if ALARMTIME[0]%10 == 9 :
                    ALARMTIME[0] -= 9
                else :
                    ALARMTIME[0] += 1
            else :
                ALARMTIME[0] += 1
            with lock:
                cad.lcd.write(str(int(ALARMTIME[0]%10)))
                
        elif x == 3 :
            if int(ALARMTIME[1]/10) == 5 :
                ALARMTIME[1] -= 50
            else :
                ALARMTIME[1] += 10
            with lock:
                cad.lcd.write(str(int(ALARMTIME[1]/10)))
                
        elif x == 4 :
            if ALARMTIME[1]%10 == 9 :
                ALARMTIME[1] -= 9
            else :
                ALARMTIME[1] += 1
            with lock:
                cad.lcd.write(str(int(ALARMTIME[1]%10)))
                
        elif x == 6 :
            if int(ALARMTIME[2]/10) == 5 :
                ALARMTIME[2] -= 50
            else :
                ALARMTIME[2] += 10
            with lock:
                cad.lcd.write(str(int(ALARMTIME[2]/10)))
                
        elif x == 7 :
            if ALARMTIME[2]%10 == 9 :
                ALARMTIME[2] -= 9
            else :
                ALARMTIME[2] += 1
            with lock:
                cad.lcd.write(str(int(ALARMTIME[2]%10)))
                
        elif x == 10 :
            ALARMFLAG = 1
            global CURRENTSTATUS
            CURRENTSTATUS = 0
            mainmode()
            
        elif x == 14 :
            ALARMFLAG = 0
            ALARMTIME = [0,0,0]
            with lock:
                cad.lcd.set_cursor(0,1)
                cad.lcd.write('{:02d}'.format(ALARMTIME[0])+":"+'{:02d}'.format(ALARMTIME[1])+":"+'{:02d}'.format(ALARMTIME[2]))
        with lock:
            cad.lcd.set_cursor(x,1)
            cad.lcd.blink_on()

def store_icon() :
    for i in range(7):
        cad.lcd.store_custom_bitmap(i, _icon.get_icon(i))

def find_icon(status):
    starr = ["wifi","alarm","Rain","Clear","Wind","Clouds","Celsius"]
    return starr.index(status)#333330302133100333232

def alarm_on():
    global alarm_flag
    nowTimeThreadControl(False)
    networkThreadControl(False)
    mixer.init()
    #with lock :01
    lcd_clear()

    mixer.music.load("/home/pi/test.mp3")
    mixer.music.play()
    cad.lcd.set_cursor(0,0)
    cad.lcd.write("ALARM!!!!!")
    cad.lcd.set_cursor(0,1)
    cad.lcd.write("PRESS BUTTON 4")

    print(alarm_flag)
    
    while(1) :
        if alarm_flag == 0:
            mixer.music.stop()
            print("music stop")
            break
#0`013313
    
    
LCD_FLAG = True

def lcd_alarm_onoff():
    global alarm_flag
    global LCD_FLAG
    if alarm_flag == 0 :
        if LCD_FLAG :
            with lock:
                cad.lcd.backlight_off()
                cad.lcd.display_off()
            LCD_FLAG = False
        else :
            with lock:            
                cad.lcd.backlight_on()
                cad.lcd.display_on()
            LCD_FLAG = True
    else :
        alarm_flag = 0

    
if __name__ == '__main__' :
    cad = pifacecad.PiFaceCAD()
    store_icon()
    lcd_init()

    cad.lcd.set_cursor(0,0)
    cad.lcd.write("D & J PI PROJECT")
    cad.lcd.set_cursor(0,1)
    cad.lcd.write("CONNECTING...")

    while _wifi.internetcon() == False :
        os.system("sudo service networking reload")
    weatherinfo = _weather.get_weather_from_place(w_country[country_index])
    button_init()
    networkThreadStart()
    nowTimeThreadStart()
    mainmode()
    
