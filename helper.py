
#FUNCIONES Y CODIGO AUXILIAR QUE FUE LIMPIANDO DEL MAIN. 

from datetime import date, datetime, timedelta
from unidecode import unidecode
from naming import *


def secondsToTC (duration):
    '''
        IN: (int) duration in seconds
        OUT: (str) duration in TC format ('hh:mm:ss:ff')
        Won't calculate frames, they will always be 00.
    '''
    #primero, si dura mas de una hora.
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = (duration % 3600) % 60

    return ''.join([str(hours).zfill(2),':',str(minutes).zfill(2),':',str(seconds).zfill(2),':00'])


def IBMSlistMaker(promo):
    '''
    IN: dict: info a promocionar, segun claves de variables
    
    OUT: [list of lists] lista con todas las versiones de esa promo para la planilla de IBMS.
    La primera lista especifica en que solapa ira la promo, la segunda lista son los valores
    de la fila en la planilla.
    '''

    #Variables
    #no referenciar al dict dentro del código, reemplazar todo acá

    showFeed = promo['showFeed']
    showName = promo['showName']
    promoPckg = promo['promoPckg']
    duration = promo['duration']
    #dentro de cada canal, asignar variable bumpDuration ;)
    premiereDate = promo['premiereDate']
    premiereJustDate = premiereDate.date()
    genDateStr = promo['genDateStr']
    dstMexFlag = promo['dstMex']
    dstChiFlag = promo['dstChi']
    crossChannelFlag = promo['crossChannel']
    megaCableFlag = promo['megaCable']
    aeFlag = promo['a&e']
    cinesFlag = promo ['cines']
    foxSportsFlag = promo ['foxSports']


    startDate = premiereDate.date() - timedelta(14)  #fecha inicio para avances y puntuales -solo dia
    avEndDate = premiereDate.date() - timedelta(1)  #que el avance deje de salir un día antes del estreno
    startGenDate = promo['genStartDate'].date()  #fecha de inicio de la gen -solo dia
    endGenDate = promo['endDate'].date()  #fecha fin de las promos gen
    bumpEndDate = date(2022, 12, 31)  #fecha de fin para los bumps

    approvDeadline = returnWeekday(
        startDate - timedelta(9))  #para plani Seguimiento
    txtDeadline = returnWeekday(
        startDate - timedelta(15))  #para plani Seguimiento
    dueDate = returnWeekday(startDate - timedelta(7))  #para plani Seguimiento

    #para hacer el nombre 2020_12_etc:
    #esto tendría que ir luego de los IF DE promoPckg
    promoCode = unidecode(premiereJustDate.strftime('%Y_%m_') + (str(showName)))
    #para los dias de la semana del Allowed Days
    allowedDayToday = (premiereJustDate.strftime('%a')).upper()
    allowedDayTomorrow = ((premiereJustDate - timedelta(1)).strftime('%a')).upper()
    
    #primero IFS de showFeed -> defino strings

    avSuffix = 'AV'
    genSuffix = 'GEN'
    feedLang = 'SPA'
    strAvance = unidecode(properDay(premiereDate, feedLang) + " " + str(
        premiereDate.day) + " " + 
        str(properTime(premiereDate, showFeed,dstMexFlag, dstChiFlag)))


    if showFeed == 'EGSUR' or showFeed == 'EGNOR':
        strAvance = unidecode("Desde el " + properDay(
            premiereDate, feedLang) + " " + str(
                premiereDate.day) + " de " + str(
                    properMonth(premiereDate, feedLang)) + " " + str(
                        properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
        bumpDuration = 5
        bumpFeedStr = 'SOUTH + NORTH + US'
        if showFeed == 'EGSUR':
            feedStr = 'SOUTH'
            avSuffix = ' AV FS'
            genSuffix = ' GEN FS'
        else:
            feedStr = 'NORTH'
            avSuffix = ' AV FN'
            genSuffix = ' GEN FN'

    elif showFeed == 'MCLATAM' or showFeed == 'MCUSA':
        strAvance = unidecode("Desde el " + properDay(
            premiereDate, feedLang) + " " + str(
                premiereDate.day) + " de " + str(
                    properMonth(premiereDate, feedLang)) + " " + str(
                        properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
        bumpDuration = 30
        bumpFeedStr = 'LATAM + USA'
        if showFeed == 'MCUSA':
            feedStr = 'USA'
        else:
            feedStr = 'LATAM'

    elif showFeed == 'EE':
        feedStr = 'LATAM'
        avSuffix = ' AV ' + unidecode(properDay(premiereDate, feedLang) + " " + str(
            premiereDate.day))
        todayStr = 'HOY'
        strHoy = todayStr + ' ' + str(
            properTime(premiereDate, showFeed, dstMexFlag, dstChiFlag))
        bumpDuration = 7
        bumpFeedStr = 'LATAM'
        ahoraComienzaPreffix = 'AHORA COMIENZA - '
        ensegVolvemosPreffix = 'ENSEGUIDA VOLVEMOS - '
        yaVolvimosPreffix = 'YA VOLVIMOS - '


    elif showFeed == 'FALATAM':
        feedStr = 'LATAM + MEXICO'  
        tomorrowStr = 'MAÑANA'
        todayStr = 'HOY'
        bumpDuration = 7
        bumpFeedStr = 'LATAM + MEXICO'
        ahoraComienzaPreffix = 'ACONTINUACION - '
        ensegVolvemosPreffix = 'ENSEGUIDA REGRESAMOS - '
        yaVolvimosPreffix = 'CONTINUAMOS VIENDO - '

    elif showFeed == 'FABRASIL':
        feedStr = 'BRASIL'
        feedLang = 'BRA'
        tomorrowStr = 'AMANHÃ'
        todayStr = 'HOJE'
        bumpDuration = 7
        bumpFeedStr = 'BRASIL'
        ahoraComienzaPreffix = 'ASEGUIR - '
        ensegVolvemosPreffix = 'ESTAMOS APRESENTANDO - '
        yaVolvimosPreffix = 'VOLTAMOS A APRESENTAR - '

    elif showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' \
    or showFeed == 'AMCLATAM' or showFeed == 'AMCBRASIL':
        if showFeed == 'AMCBRASIL':
            feedStr = 'BRAZIL'
            feedLang = 'BRA'
            tomorrowStr = 'AMANHÃ '
            todayStr = 'HOJE '
        else:
            tomorrowStr = 'MAÑANA '
            todayStr = 'ESTA NOCHE '
            if showFeed == 'AMCSUR':
                feedStr = 'SOUTH'
            if showFeed == 'AMCLATAM':
                feedStr = 'LATAM'
            if showFeed == 'AMCNORCOL':
                feedStr = 'NORTH + COLOMBIA'
        

    #luego IFS de promoPckg -> creo lista vacía, pueblo lista y retorno 
    #ver como pongo los msj de alerta
    outputIBMS = [[showFeed]]
    if promoPckg == 'ESTRENO' or promoPckg == 'NT' \
        or promoPckg == 'CAPS ESTRENO':
        #el Avance
        avanceIBMS = [
            promoCode.upper() + avSuffix, secondsToTC(0), secondsToTC(duration), 
            secondsToTC(duration), strAvance.upper(), feedStr, '', 
            10, startDate, avEndDate,
            returnWeekday(startDate - timedelta(7))
        ]
        #la generica
        strGen = unidecode(str(genDateStr) + " " + str(
            properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
        genIBMS = [
            promoCode.upper() + ' ' + genSuffix, secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
            returnWeekday(startGenDate - timedelta(7))
        ]

        if showFeed == 'EE' or showFeed == 'FALATAM' or showFeed == 'FABRASIL' \
        or showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' or showFeed == 'AMCBRASIL':
            #Versiones HOY y Gen Hoy
            strHoy = unidecode(todayStr + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
                secondsToTC(duration), secondsToTC(duration),
                strHoy.upper(), feedStr, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            hoyGenIBMS = [
                promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
                secondsToTC(duration), secondsToTC(duration),
                strHoy.upper(), feedStr, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            if showFeed == 'FALATAM' or showFeed == 'FABRASIL' or \
            showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' \
            or showFeed == 'AMCBRASIL':
                #sobreescribo los avances (como hay version mañana,se acaban un dia antes)
                avanceIBMS = [
                    promoCode.upper() + ' ' + str(promoPckg) + ' ' + str(properDay(premiereDate, feedLang).upper())
                    + " " + str(premiereDate.day), secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strAvance.upper(), feedStr, '', 10, startDate, avEndDate - timedelta(1),
                    returnWeekday(startDate - timedelta(7))
                    ]
                #avance estreno
                strMan = unidecode(tomorrowStr + str(
                    properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
                manStartDate = premiereJustDate - timedelta(1)
                manIBMS = [
                    promoCode.upper() + ' ' + tomorrowStr , secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strMan.upper(), feedStr, '', 10, manStartDate, 
                    manStartDate, returnWeekday(manStartDate - timedelta(7))
                ]
                # #Version Hoy (estreno)  - NO HACE FALTA, YA LA HICIMOS EN EE
                # strHoy = unidecode(todayStr + str(
                #     properTime(premiereDate, showFeed,
                #                 dstMexFlag, dstChiFlag)))
                # hoyIBMS = [
                #     promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
                #     secondsToTC(duration), secondsToTC(duration),
                #     strHoy.upper(), feedStr, '', 10, premiereJustDate, premiereJustDate,
                #     returnWeekday(premiereJustDate - timedelta(7))
                # ]
                #la generica ya esta hecha en el primer if, no la hacemos de nuevo.
                #Version Mañana (generica)
                strManGen = unidecode(tomorrowStr + str(
                    properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
                manGenIBMS = [
                    promoCode.upper() + ' ' + genSuffix + ' ' + tomorrowStr, secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strManGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
                    returnWeekday(startGenDate - timedelta(7))
                ]
                # #Version Hoy - GENERICA -  YA LA HICIMOS EN EE
                # strHoy = unidecode(todayStr + str(
                #     properTime(premiereDate, showFeed,
                #                 dstMexFlag, dstChiFlag)))
                # hoyGenIBMS = [
                #     promoCode.upper() + ' ' + genSuffix + ' ' + todayStr, secondsToTC(0), 
                #     secondsToTC(duration), secondsToTC(duration),
                #     strHoy.upper(), feedStr, '', 10, startGenDate, endGenDate,
                #     returnWeekday(startGenDate - timedelta(7))
                # ]
                #Sumo las filas a la lista y devuelvo lista
                outputIBMS.extend([avanceIBMS, manIBMS, hoyIBMS, manGenIBMS, hoyGenIBMS])

        #Sumo a la lista las promos de MC y GOURMET que no habia sumado antes
        outputIBMS.append([avanceIBMS, genIBMS])

                
    if showFeed == 'EGSUR' and promoPckg == 'ESTRENO':
        #Redux a cont - caso especial para EGSUR y ESTRENO
        reduxAContIBMS = [
        promoCode.upper() + ' REDUX A CONT', secondsToTC(0), secondsToTC(15), secondsToTC(15),
        "A CONTINUACION", "SOUTH + NORTH", '', 10, startGenDate,
        endGenDate,
        returnWeekday(startGenDate - timedelta(7))
        ]
        outputIBMS[1].append(reduxAContIBMS)

   

        #if separado para los bumps
    if showFeed == 'EGSUR' or showFeed == 'MCLATAM': 
        #Aca va el bump a Cont *1
        bumpAContIBMS = [
        'A CONT-' + (str(showName)).upper(), secondsToTC(0), secondsToTC(bumpDuration),
        secondsToTC(bumpDuration), "A CONTINUACION", bumpFeedStr, " ", 10,
        startGenDate, bumpEndDate,
        returnWeekday(startGenDate - timedelta(7))
        ]
        #Sumo las filas a la lista
        outputIBMS[1].append(bumpAContIBMS)
    elif showFeed == 'EE' or showFeed == 'FALATAM' or showFeed == 'FABRASIL':
        #Bumps a cont
        ahoraComienzaIBMS = [unidecode(
        ahoraComienzaPreffix + (str(showName)).upper()),
        secondsToTC(0), secondsToTC(bumpDuration), secondsToTC(bumpDuration), 
        "NEXT", feedStr, " ", 10, premiereJustDate,
        bumpEndDate,
        returnWeekday(premiereJustDate - timedelta(7))
        ]
        ensegVolvemosIBMS = [unidecode(
        ensegVolvemosPreffix + (str(showName)).upper()), 
        secondsToTC(0), secondsToTC(bumpDuration), secondsToTC(bumpDuration),
        "STAY TUNED", feedStr, " ", 10, premiereJustDate,
        bumpEndDate,
        returnWeekday(premiereJustDate - timedelta(7))
        ]
        yaVolvimosIBMS = [unidecode(
        yaVolvimosPreffix + (str(showName)).upper()), 
        secondsToTC(0), secondsToTC(bumpDuration), secondsToTC(bumpDuration),
        "NOW", feedStr, " ", 10, premiereJustDate,
        bumpEndDate,
        returnWeekday(premiereJustDate - timedelta(7))
        ]

        outputIBMS[1].extend([ahoraComienzaIBMS, ensegVolvemosIBMS,
        yaVolvimosIBMS])


    return outputIBMS




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



print (IBMSlistMaker(promo1))









# def secondsToTC (duration):
#     '''
#         IN: (int) duration in seconds
#         OUT: (str) duration in TC format ('hh:mm:ss:ff')
#         Won't calculate frames, they will always be 00.
#     '''
#     #primero, si dura mas de una hora.
    
#     hours = duration // 3600
#     minutes = (duration % 3600) // 60
#     seconds = (duration % 3600) % 60

#     return ''.join([str(hours).zfill(2),':',str(minutes).zfill(2),':',str(seconds).zfill(2),':00'])



# print (secondsToTC(30))






# Para xonseguir ID de archivos y carpetas del Drive:

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os

# gauth = GoogleAuth()
# # Try to load saved client credentials
# gauth.LoadCredentialsFile("mycreds.txt")
# if gauth.credentials is None:
#     # Authenticate if they're not there
#     gauth.LocalWebserverAuth()
# elif gauth.access_token_expired:
#     # Refresh them if expired
#     gauth.Refresh()
# else:
#     # Initialize the saved creds
#     gauth.Authorize()
# # Save the current credentials to a file
# gauth.SaveCredentialsFile("mycreds.txt")

# drive = GoogleDrive(gauth)

# fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# for file in fileList:
#   print('Title: %s, ID: %s' % (file['title'], file['id']))
#   # Get the folder ID that you want
#   if(file['title'] == "To Share"):
#       fileID = file['id']



# from datetime import datetime


# genStartDate = datetime(2020,10,1,18)
# showName = 'BREAKING MUSIC 01'
# print (genStartDate.strftime('%Y_%m_') + showName)


#Esto lo hice para que me ayude con los horarios de Mex
#print (promo['showName'], properTime(promo['premiereDate'], 'EE', promo['dstMex'], promo['dstChi']))



# Ayuda para los parametros de properTime:
# date:datetime object
# feed (str), define am/PM format
# pack: (str) promo package (use promoPkcg variable)
# mexDst:(bool) True if +1, false if 0
# chiDst: (bool) True if +1, false if 0


#REHACER PROPER TIME PARA QUE SOLO MUESTRE LA HORA -HECHO!
# PROPER DAY PARA QUE SOLO MUESTRE LA FECHA -HECHO
#PROPER MONTH CREA SOLO EL MES -- HECHO

# listMaker es la que juntara ambas funciones

#print (showFeed)
#print (properTime(premiereDate, showFeed, dstMex, dstChi))
#print ('Esta noche', properTime(premiereDate, 'FALATAM', dstMex, dstChi))

#Ejemplos de uso de properDay y properMonth
#print(properMonth(premiereDate,'BRA'))
#print(properDay(premiereDate,'SPA'))
#print(properDay(premiereDate,'BRA'))



#este fue el destination fallido para los bumps



# ACA HAY QUE ARREGLAR EL TEMA DE LOS BUMPS Y LA DESTINATION DE LIST MAKER

# for promo in muchasPromos: #aca itero los bumps para plani IBMS
#   listaBumps = listMaker(promo, "bumpsIBMS") #bumpsIBMS
#   resultadoBumpsIBMS.append(listaBumps)
# print (resultadoBumpsIBMS)
#luego aca las iterare para generar las otras planis que quiera.



## ACA VA TODO LO QUE ESTABA EN WRITE2EXCEL, TODO LO QUE USE PARA APRENDER A ESCRIBIR .XLSX

# from openpyxl import Workbook







#PRUEBO DE PEGAR UNA LINEA EN UN EXCEL
# wb = Workbook() #creo libro nuevo
# ws1 = wb.active #hago la hoja activa
# for row in range (3):
#   ws1.append(listMaker(promo))

# dest_filename = 'prueba.xlsx'
# wb.save(filename = dest_filename)



# #para crear libro nuevo
# wb = Workbook() #creo libro nuevo
# #ws1 = wb.create_sheet("Nac2") # creo hoja nueva, insertada al final (default)
# #ws1.title = "Nac" #cambio el nombre de la hoja creada

# dest_filename = 'prueba.xlsx'
# name = 'Promo'

# lista = [showName, premiereDate, 'canal', startDate]
# ws1 = wb.active #hago la hoja activa
# ws1.title = "range names" #le pongo nombre
# #for row in range(1, 40): #itero filas 1 a 39 ;)
# #  ws1.append(range(600)) #le agrego del 0 al 599, 1 valor por celda -Esta es la que tengo que usar
# for row in range (3):
#   ws1.append(lista)

# ws2 = wb.create_sheet(title="Pi")
# ws2['F5'] = 3.14
# ws2['G5'] = '03/10/2020 20:00'
# ws2['A1'] = premiereDate 



# print(ws2['F5'].value)

# wb.save(filename = dest_filename)

##para abrir libro ya existente
#from openpyxl import load_workbook
#wb2 = load_workbook('Prueba1.xlsx')


##aca itero Libro / Filas / Valores en cada fila
#for sheet in wb2:
  #print(sheet.title)
 # for row in sheet.values:
  #  for value in row:
  #    print(value)



#for row in wb2.values:
 #  for value in row:
  #   print(value)
