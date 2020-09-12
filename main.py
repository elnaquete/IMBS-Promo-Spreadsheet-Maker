#por ahora así, despues vemos que dependencias se importan o si hacemos un solo archivo.


from datetime import date, datetime, timedelta
from listMaker import IBMSlistMaker
from inputHandler import readExcel, strToBool
from openpyxl import Workbook
from write2excel import write2excelIBMS
from gDriveUploader import gDriveUploader



feeds = ['EGSUR', 'EGNOR', 'MCLATAM', 'MCUSA', 'EE', 'AMCSUR', 'AMCNORCOL', 'AMCLATAM', 'AMCBRASIL', 
  'FALATAM', 'FABRASIL', 'AMCNETWORKS', 'OFFAIR']
packs = ['ESTRENO', 'NT', 'REP', 'GEN', 'PUNTUAL', 'CLUB','GEN', 'STUNT', 'MEDIODIA'] #agregar packs = 'CAPS_ESTRENO' (que es igual que NT, no?)



promo1 = {
'showFeed': 'FALATAM',
'showName': 'BREAKING MUSIC 01',
'promoPckg': 'GEN',
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
#Este es el nombre del archivo de Excel que exportará
outputFilename = "lista_IBMS.xlsx"

#muchasPromos = [promo1]
muchasPromos = readExcel(inputFilename)
resultadoIBMS = []
# lista de promos cross (a implementar)
# crossIBMS = [] 

#aca itero las promos para armar la plani IBMS
#TAL VEZ tenga que chequear aca el flag de Cross, para armar otra lista con los crosschannel
#seguramente acá vayan las llamadas a todas las funciones para armar todas las listas.
for promo in muchasPromos: 
    listaPromos = IBMSlistMaker(promo) 
    resultadoIBMS.append(listaPromos)
#llamada a la funcion de los CROSS, a implementar:
    # if promo['crossChannel'] == True:
    #     listaPromosCross = IBMSCrossListMaker(promo)
    #     crossIBMS.append(listaPromosCross)

print (resultadoIBMS)

#ACA SIGUE LA IMPLEMENTACION PARA PEGAR TODO EN UN UN EXCEL
write2excelIBMS(resultadoIBMS, outputFilename)

#Y despues ver de subirlo al Drive / Office 365
#Chequear que el Google Auth pueda leer el client_secrets.json, si no esta en el path no lo lee
#(como por ejemplo en el VS Code, en el Thonny sí lo lee)

gDriveUploader(outputFilename)
