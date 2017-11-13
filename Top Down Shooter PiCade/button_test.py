import RPi.GPIO as GPIO

button = 21
button_led = 16

GPIO.setmode(GPIO.BCM)

# setup button pin
GPIO.setup(button, GPIO.IN,pull_up_down=GPIO.PUD_UP)
# button led
GPIO.setup(button_led, GPIO.OUT)



while(True):
    if (GPIO.input(button) == 0):
        GPIO.output(button_led, False)
        print ("LED on")
    else:
        GPIO.output(button_led, True)
        print ("LED off")
