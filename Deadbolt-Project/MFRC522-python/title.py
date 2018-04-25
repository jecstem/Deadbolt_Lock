import gspread
import gpiozero 
import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
from oauth2client.service_account import ServiceAccountCredentials

continue_reading = True
deadbolt = gpiozero.LED(17)
RFID = MFRC522.MFRC522()
    
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Creds.json', scope)
gc = gspread.authorize(credentials)

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    
wks = gc.open("Deadbolt_Lock").sheet1
  
signal.signal(signal.SIGINT, end_read)

while continue_reading:
	(status,TagType) = RFID.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	if status == RFID.MI_OK:
		
		print "Card detected."
		
	(status,uid) = RFID.MFRC522_Anticoll()
	
	if status == RFID.MI_OK:
		
		print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		RFID.MFRC522_SelectTag(uid)
		status = RFID.MFRC522_Auth(MIFAREReader.PICC_AUTHENpT1A, 8, key, uid)
		
		if status == RFID.MI_OK:
			data == RFID.MFRC522_Read(8)
			cell = wks.find(data)
			row_number = cell.row
			col_number = cell.col
			level = col_number
			dlock = wks.cell(row_number, level)
			
			if dlock >= 1:
				deadbolt.on()
				sleep(5)
				deadbolt.off
			else:
				print "Access denied"
				
			MIFAREReader.MFRC522_StopCrypto1()
        else:
			print "authentication error"
