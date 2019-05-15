import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import time
camera=PiCamera()
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import time, datetime
import telepot
from telepot.loop import MessageLoop
now = datetime.datetime.now()
trail=414539289        #comment this initially print chat_id(you will find below)  for your telebot id
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)   #GPIO setup based on Board Pin configuration
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
servoPIN=19                  #choose any GPIO pin 
GPIO.setup(servoPIN,GPIO.OUT)
pwm=GPIO.PWM(servoPIN,50)
pwm.start(60)
MATRIX=[[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]
ROW=[7,11,13,15]
COL=[12,16,18,22]
password=[2,2,2,2]  #choose password
test=[]
ch=['*','*','*','*']
wrong_count=0
s_mode=0
DC=1./18.*(50)+2
pwm.ChangeDutyCycle(DC)
for j in range(4):
        GPIO.setup(COL[j],GPIO.OUT)
        GPIO.output(COL[j],1)

for i in range(4):
    GPIO.setup(ROW[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
def keypad():
    c=0
    while(True and c<4):
        for j in range(4):
                GPIO.output(COL[j],0)
                    
                for i in range(4):
                        if(GPIO.input(ROW[i])==0):
                                print(MATRIX[i][j])
                                c=c+1
                                test.append(MATRIX[i][j])
                                while(GPIO.input(ROW[i])==0):
                                        pass
                                time.sleep(0.25)
                GPIO.output(COL[j],1)

def fprint():
    ## Search for a finger##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
    

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')

        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            return True
            '''if(s_mode==0):
                s_mode=1
                DC=1./18.*(120)+2
                pwm.ChangeDutyCycle(DC)
            else:
                s_mode=0
                DC=1./18.*(60)+2
                pwm.ChangeDutyCycle(DC)'''

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))


def action(msg):
    chat_id = msg['chat']['id']
    print(chat_id)    #print chat_id 
    trail=chat_id
    command = msg['text']
    print 'Received: %s' % command    #python 2  
    #print(command)                    
    if command=='/status':
        telegram_bot.sendMessage (chat_id, str("INTRUDER DETECTED"))
    elif command == '/unlock':
        DC=1./18.*(180)+2
        pwm.ChangeDutyCycle(DC)
        s_mode=1
        telegram_bot.sendMessage (chat_id, str("DOOR UNLOCKED"))
    elif command == '/lock':
        DC=1./18.*(50)+2
        pwm.ChangeDutyCycle(DC)
        s_mode=0
        telegram_bot.sendMessage (chat_id, str("DOOR LOCKED"))
    
    elif command == '/photo':
        telegram_bot.sendDocument(chat_id, document=open('/home/pi/Desktop/image.png')) #choose location of image captured
    elif command == '/off':
        telegram_bot.sendMessage (chat_id, str("SYSTEM TURNED OFF"))
        exit()
    else:
        telegram_bot.sendMessage (trail, str("INTRUDER DETECTED"))
        
                               
telegram_bot = telepot.Bot('*******************************')  #use your telegram chat_id
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')
s_mode=0
while(True):
        keypad()
        ans=fprint()
        print("Current stored VALUE ",test)
        if(password==test or ans):
                if(s_mode==0):
                        print("Door unlocked ")
                        DC=1./18.*(180)+2
                        pwm.ChangeDutyCycle(DC)
                        s_mode=1
                else:
                        print("Door locked ")
                        DC=1./18.*(50)+2
                        pwm.ChangeDutyCycle(DC)
                        s_mode=0
                wrong_count=0
        elif(test==ch and s_mode==1):
            print("Enter new password : ")
            pas=keypad()
            password=pas
            print("Password Changed : ")
        else:
            print("Access Denied : ")
            wrong_count=wrong_count+1
            if(wrong_count==3):
                wrong_count=0
                i=0
                while(i<=5):
                        GPIO.output(5,0)
                        time.sleep(0.2)
                        GPIO.output(5,1)
                        time.sleep(0.2)
                        i=i+1
                print("Sending Message to the owner")
                sleep(1)
                camera.capture('/home/pi/Desktop/image.png')   #you can choose different location
                telegram_bot.sendMessage (trail, str("INTRUDER DETECTED"))
                telegram_bot.sendDocument(trail, document=open('/home/pi/Desktop/image.png'))  
        test=[]
    
