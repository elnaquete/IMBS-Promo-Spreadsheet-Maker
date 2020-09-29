# encoding: utf-8

#por ahora así, despues vemos que dependencias se importan o si hacemos un solo archivo.
#Para que funcione el upload a Drive, hay que agregar el client_secrets.json (esta en el dropbox)


from datetime import datetime
from listMaker import IBMSlistMaker
from inputHandler import readExcel
from write2excelv2 import write2excelIBMSv2
# from gDriveUploader import gDriveUploader


feeds = ('EGSUR', 'EGNOR', 'MCLATAM', 'MCUSA', 'EE', 'AMCSUR', 'AMCNORCOL', 'AMCLATAM', 'AMCBRASIL', 
  'FALATAM', 'FABRASIL')
packs = ('ESTRENO', 'NT', 'CAPS ESTRENO', 'REP', 'GEN', 'PUNTUAL', 'CLUB', 'STUNT', 'GEN_AMC', 'BUMP', 'PELI DEL MES')

#promo1 para pruebas
promo1 = {
'showFeed': 'EGSUR',
'showName': 'BREAKING MUSIC 01',
'promoPckg': 'ESTRENO',
'duration': 30,
'premiereDate': datetime(2020,10,1,18),
'genDateStr': 'MIÉRCOLES',
'genStartDate': datetime(2020,10,1,18),
'endDate': datetime(2020,10,31,18),
'dstMex': True, 
'dstChi': True,
'crossChannel': False,
'megaCable':	False,
'a&e':	False,
'cines':	False,
'foxSports': False
} 

#Este es el nombre del Excel que leera con las promos.
inputFilename = "input.xlsx"

# Esta es la forma de darle Timestamp al nombre de archivo Excel que exportara
# para activarlo, cambiar el nombre de la variable en write2Excel
timeStamp = datetime.now()
outputFilenameTime = timeStamp.strftime("lista_IBMS %Y_%m_%d %H_%M.xlsx")
outputFilename = "lista_IBMS.xlsx"


listaPromos = readExcel(inputFilename)

write2excelIBMSv2(listaPromos, outputFilename)



#Y despues ver de subirlo al Drive / Office 365
#Chequear que el Google Auth pueda leer el client_secrets.json, si no esta en el path no lo lee
#(como por ejemplo en el VS Code, en el Thonny sí lo lee)

#gDriveUploader(outputFilename)
