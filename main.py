#por ahora así, despues vemos que dependencias se importan o si hacemos un solo archivo.


from datetime import date, datetime, timedelta
from listMaker import listMaker
from inputHandler import readExcel, strToBool
from openpyxl import Workbook
from write2excel import write2excelIBMS



feeds = ['EGSUR', 'EGNOR', 'MCLATAM', 'MCUSA', 'EE', 'AMCSUR', 'AMCNORCOL', 'AMCLATAM', 'AMCBRASIL', 
  'FALATAM', 'FABRASIL', 'AMCNETWORKS', 'OFFAIR']
packs = ['ESTRENO', 'NT', 'REP', 'GEN', 'PUNTUAL', 'CLUB','GEN', 'STUNT', 'MEDIODIA'] #agregar packs = 'CAPS_ESTRENO' (que es igual que NT, no?)


filename = 'input.xlsx'

promo1 = {
'showFeed': 'MCLATAM',
'showName': 'la vaca lola',
'promoPckg': 'BUMP',
'premiereDate': datetime(2020,10,1,18),
'genDateStr': 'MARTES Y JUEVES',
'genStartDate': datetime(2020,10,1,18),
'endDate': datetime(2020,10,31,18),
'dstMex': True, 
'dstChi': True,
'crossChannel:': False,
'megaCable':	False,
'a&e':	False,
'cines':	False,
'foxSports': False
} 

#muchasPromos = [promo1]
muchasPromos = readExcel(filename)
resultadoIBMS = []

#aca itero las promos para armar la plani IBMS
for promo in muchasPromos: 
  listaPromos = listMaker(promo) 
  resultadoIBMS.append(listaPromos)

#print (resultadoIBMS)

#ACA SIGUE LA IMPLEMENTACION PARA PEGAR TODO EN UN UN EXCEL
write2excelIBMS(resultadoIBMS, "listaIBMS.xlsx")
