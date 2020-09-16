#por ahora así, despues vemos que dependencias se importan o si hacemos un solo archivo.
#Para que funcione el upload a Drive, hay que agregar el client_secrets.json (esta en el dropbox)


from datetime import date, datetime, timedelta
from listMaker import IBMSlistMaker
from inputHandler import readExcel
from write2excel import write2excelIBMS
from gDriveUploader import gDriveUploader


feeds = ['EGSUR', 'EGNOR', 'MCLATAM', 'MCUSA', 'EE', 'AMCSUR', 'AMCNORCOL', 'AMCLATAM', 'AMCBRASIL', 
  'FALATAM', 'FABRASIL', 'AMCNETWORKS', 'OFFAIR']
packs = ['ESTRENO', 'NT', 'REP', 'GEN', 'PUNTUAL', 'CLUB','GEN', 'STUNT'] 
#agregar packs = 'CAPS ESTRENO' 'EPISODICA' 'GEN_SERIES'


promo1 = {
'showFeed': 'FALATAM',
'showName': 'BREAKING MUSIC 01',
'promoPckg': 'GEN',
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

#print (resultadoIBMS)

#ACA SIGUE LA IMPLEMENTACION PARA PEGAR TODO EN UN UN EXCEL
write2excelIBMS(resultadoIBMS, outputFilename)

#Y despues ver de subirlo al Drive / Office 365
#Chequear que el Google Auth pueda leer el client_secrets.json, si no esta en el path no lo lee
#(como por ejemplo en el VS Code, en el Thonny sí lo lee)

#gDriveUploader(outputFilename)
