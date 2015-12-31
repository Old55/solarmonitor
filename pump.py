import time
import RPi.GPIO as GPIO

class Pump:
    def __init__(self, GPIO_MODE, GPIO_INPUT, GPIO_OUTPUT, OFF_DELAY):
	#Our pin to detect an event to trigger the pump. Might be set to None if the pump is not trigger controlled
        self.GPIO_INPUT = GPIO_INPUT
	#Our pin that we are going to set to HIGH to switch the relay
        self.GPIO_OUTPUT = GPIO_OUTPUT
	#OFF_DELAY is the number of seconds we leave the pump running AFTER the falling edge is detected
	#This is OK because it only comes from add_event_detect which is threaded
	self.OFF_DELAY = OFF_DELAY
	#Some values we can return to check on pump status
	self.running = False
	self.start_time = time.time()
	self.stop_time = time.time()

        GPIO.setmode(GPIO_MODE)
	#Detecting input pin. Callback determines if we start or stop based on our pin status. This seems to be
	#the most fool proof way of making sure the pump doesn't get started and left on as reading the self.running
	#didn't work so well in my LED trials with the float switch
	if GPIO_INPUT:
            GPIO.setup(self.GPIO_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   
            GPIO.add_event_detect(self.GPIO_INPUT, GPIO.BOTH, callback = self.pump_control, bouncetime=50)

        GPIO.setup(self.GPIO_OUTPUT, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

    def pump_control(self, channel):

	if GPIO.input(self.GPIO_OUTPUT):
	    self.stop_pump()

	else:
	    self.start_pump()

    def start_pump(self):
	#This should be the only function used to start the pump
	self.running = True
	self.start_time = time.time()
        GPIO.output(self.GPIO_OUTPUT, False)

    def stop_pump(self):
	if self.OFF_DELAY:
	    GPIO.remove_event_detect(self.GPIO_INPUT)
	    time.sleep(self.OFF_DELAY)
	    GPIO.add_event_detect(self.GPIO_INPUT, GPIO.BOTH, callback = self.pump_control, bouncetime=50)
	
	self.running = False
	self.stop_time = time.time()
        GPIO.output(self.GPIO_OUTPUT, True)

    def emergency_stop(self):
	#Stop the pump and remove the event so it can't get triggered again by our input trigger
	self.running = False
	GPIO.remove_event_detect(self.GPIO_INPUT)
        GPIO.output(self.GPIO_OUTPUT, True)

    def pump_active(self):
	return self.running

    def pump_times(self):
	return self.start_time, self.stop_time
