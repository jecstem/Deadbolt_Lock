import gpiozero 
import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True
MIFAREReader = MFRC522.MFRC522()

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    
while continue_reading:
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	if status == MIFAREReader.MI_OK:
		
		print "Card detected."
		
	(status,uid) = MIFAREReader.MFRC522_Anticoll()
	
	if status == MIFAREReader.MI_OK:
		
		print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		MIFAREReader.MFRC522_SelectTag(uid)
		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENpT1A, 8, key, uid)
		
		if status == MIFAREReader.MI_OK:
			data == MIFAREReader.MFRC522_Read(8)
			print data
			MIFAREReader.MFRC522_StopCrypto1()
		else
			print "error"
