
#FUNCIONES Y CODIGO AUXILIAR QUE FUE LIMPIANDO DEL MAIN. 

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



print (secondsToTC(30))












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
