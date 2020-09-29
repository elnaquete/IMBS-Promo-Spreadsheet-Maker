# por ahora así, despues vemos que dependencias se importan o si hacemos un solo archivo.
# Para que funcione el upload a Drive, hay que agregar el client_secrets.json (esta en el dropbox)


from datetime import date, datetime, timedelta
from listMaker import IBMSlistMaker
from inputHandler import readExcel
from write2excel import write2excelIBMS
from write2excelv2 import write2excelIBMSv2
from gDriveUploader import gDriveUploader


feeds = (
    "EGSUR",
    "EGNOR",
    "MCLATAM",
    "MCUSA",
    "EE",
    "AMCSUR",
    "AMCNORCOL",
    "AMCLATAM",
    "AMCBRASIL",
    "FALATAM",
    "FABRASIL",
)
packs = (
    "ESTRENO",
    "NT",
    "CAPS ESTRENO",
    "REP",
    "GEN",
    "PUNTUAL",
    "CLUB",
    "STUNT",
    "GEN_AMC",
    "BUMP",
    "PELI DEL MES",
)

# promo1 para pruebas
promo1 = {
    "showFeed": "EGSUR",
    "showName": "BREAKING MUSIC 01",
    "promoPckg": "ESTRENO",
    "duration": 30,
    "premiereDate": datetime(2020, 10, 1, 18),
    "genDateStr": "MIÉRCOLES",
    "genStartDate": datetime(2020, 10, 1, 18),
    "endDate": datetime(2020, 10, 31, 18),
    "dstMex": True,
    "dstChi": True,
    "crossChannel": False,
    "megaCable": False,
    "a&e": False,
    "cines": False,
    "foxSports": False,
}

# Este es el nombre del Excel que leera con las promos.
inputFilename = "input.xlsx"

# Esta es la forma de darle Timestamp al nombre de archivo Excel que exportara
# para activarlo, cambiar el nombre de la variable en write2Excel
timeStamp = datetime.now()
outputFilenameTime = timeStamp.strftime("lista_IBMS %Y_%m_%d %H_%M.xlsx")
outputFilename = "lista_IBMS.xlsx"


# listaPromos = []
listaPromos = readExcel(inputFilename)

# test para TODAS las posibilidades
# A copy of a_dictionary is appended to a_list instead of appending a_dictionary directly
# because that would produce a *reference* to a_dictionary instead of a copy.
promo2 = promo1.copy()
for feed in feeds:
    promo2["showFeed"] = feed
    for pack in packs:
        promo2["promoPckg"] = pack
        promo2Copy = promo2.copy()
        listaPromos.append(promo2Copy)


write2excelIBMSv2(listaPromos, outputFilename)


# TAL VEZ tenga que chequear aca el flag de Cross, para armar otra lista con los crosschannel
# seguramente acá vayan las llamadas a todas las funciones para armar todas las listas.


# Y despues ver de subirlo al Drive / Office 365
# Chequear que el Google Auth pueda leer el client_secrets.json, si no esta en el path no lo lee
# (como por ejemplo en el VS Code, en el Thonny sí lo lee)

# gDriveUploader(outputFilename)
