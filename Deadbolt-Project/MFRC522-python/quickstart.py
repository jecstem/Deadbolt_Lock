import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Creds.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Deadbolt_Lock").sheet1
Question = 'answer'
Cell = 'C1'
val = wks.acell(Cell).value
print 
if Question == val:
	print True
else:
	print False

