from naming import returnWeekday, properTime, properMonth, properDay
from datetime import date, datetime, timedelta
from unidecode import unidecode

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
'''
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''





    # if showFeed == 'EGSUR':
    #     if promoPckg == 'ESTRENO':
    #         #armo las listas de IBMS
    #         #el Avance
    #         strAvance = unidecode("Desde el " + properDay(
    #             premiereDate, 'SPA') + " " + str(
    #                 premiereDate.day) + " de " + str(
    #                     properMonth(premiereDate, 'SPA')) + " " + str(
    #                         properTime(premiereDate, showFeed,
    #                                     dstMexFlag, dstChiFlag)))
    #         avanceIBMS = [
    #             promoCode.upper() + " AV FS", 0, 3000, 3000,
    #             strAvance.upper(), "SOUTH", '', 10, startDate, avEndDate,
    #             returnWeekday(startDate - timedelta(7))
    #         ]
    #         #la generica
    #         strGen = unidecode(str(genDateStr) + " " + str(
    #             properTime(premiereDate, showFeed,
    #                         dstMexFlag, dstChiFlag)))
    #         genIBMS = [
    #             promoCode.upper() + ' GEN FS', 0, 3000, 3000,
    #             strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
    #             returnWeekday(startGenDate - timedelta(7))
    #         ]
    #         #Redux a cont
    #         reduxAContIBMS = [
    #             promoCode.upper() + ' REDUX A CONT', 0, 1500, 1500,
    #             "A CONTINUACION", "SOUTH + NORTH", '', 10, startGenDate,
    #             endGenDate,
    #             returnWeekday(startGenDate - timedelta(7))
    #         ]
    #         #Sumo las filas a la lista y devuelvo lista
    #         return [showFeed, avanceIBMS, genIBMS, reduxAContIBMS]
        elif promoPckg == 'NT' or promoPckg == 'CAPS ESTRENO':
            #el Avance
            strAvance = unidecode("Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, showFeed,
                                        dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                promoCode.upper() + " AV FS", 0, 3000, 3000,
                strAvance.upper(), "SOUTH", '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Redux a cont
            reduxAContIBMS = [
                promoCode.upper() + ' REDUX A CONT', 0, 1500, 1500,
                "A CONTINUACION", "SOUTH + NORTH", '', 10, startGenDate,
                endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], avanceIBMS, genIBMS, reduxAContIBMS]
        elif promoPckg == 'PUNTUAL':
            #Solo Avance y el Redux A cont. No hay Gen.
            #Calcula la fecha de venta,, segun si es o no en el mismo mes que se emite) ¿Versiones Hoy?
            strPuntualConMes = unidecode("El " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, showFeed,
                                        dstMexFlag, dstChiFlag)))
            strPuntualSinMes = unidecode(properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            if premiereDate.month != startDate.month:  #Si la puntual sale al aire el mes anterior, decimos mes.
                puntualIBMS = [
                    promoCode.upper() + " AV FS", 0, 3000, 3000,
                    strPuntualConMes.upper(), "SOUTH", '', 10, startDate,
                    premiereJustDate,
                    returnWeekday(startDate - timedelta(7))
                ]
            else:  #Si no, no.
                puntualIBMS = [
                    promoCode.upper() + " AV FS", 0, 3000, 3000,
                    strPuntualSinMes.upper(), "SOUTH", '', 10, startDate,
                    premiereJustDate,
                    returnWeekday(startDate - timedelta(7))
                ]
            #Redux a cont
            reduxAContIBMS = [
                promoCode.upper() + ' REDUX A CONT', 0, 1500, 1500,
                "A CONTINUACION", "SOUTH + NORTH", '', 10, startGenDate,
                endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], puntualIBMS, reduxAContIBMS]

        elif promoPckg == 'REP':
            #armo las listas de IBMS - solo la generica, es un REP
            strGen = str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            genIBMS = [
                promoCode.upper() + ' REP FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS]
        elif promoPckg == 'GEN':
            #armo las listas de IBMS - solo la generica
            strGen = str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            genIBMS = [
                promoCode.upper() + ' GEN FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS]
        elif promoPckg == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, 'SPA'))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), "SOUTH + NORTH", '', 10, startGenDate,
                endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genClub]
        elif promoPckg == 'BUMP':
            # showFeed = 'BUMPS EG SUR'
            # #Bump a cont
            # bumpAContIBMS = [
            #     'A CONT-' + (str(showName)).upper(), 0, 500,
            #     500, "A CONTINUACION", "SOUTH + NORTH + US", " ", 10,
            #     startGenDate, bumpEndDate,
            #     returnWeekday(startGenDate - timedelta(7))
            # ]
            # #Sumo las filas a la lista y devuelvo lista
            # return [[showFeed], bumpAContIBMS]
        else:
            showFeed = ['ALERTAS']
            #Bump a cont
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            return [[showFeed], errorMsg]
    elif showFeed == 'EGNOR':
        # if promoPckg == 'ESTRENO':
        #     #armo las listas de IBMS
        #     #el Avance
        #     strAvance = unidecode("Desde el " + properDay(
        #         premiereDate, 'SPA') + " " + str(
        #             premiereDate.day) + " de " + str(
        #                 properMonth(premiereDate, 'SPA')) + " " + str(
        #                     properTime(premiereDate, showFeed,
        #                                 dstMexFlag, dstChiFlag)))
        #     avanceIBMS = [
        #         promoCode.upper() + " AV FN", 0, 3000, 3000,
        #         strAvance.upper(), "NORTH", '', 10, startDate, avEndDate,
        #         returnWeekday(startDate - timedelta(7))
        #     ]
        #     #la generica
        #     strGen = unidecode(str(genDateStr) + " " + str(
        #         properTime(premiereDate, showFeed,
        #                     dstMexFlag, dstChiFlag)))
        #     genIBMS = [
        #         promoCode.upper() + ' GEN FN', 0, 3000, 3000,
        #         strGen.upper(), "NORTH", '', 10, startGenDate, endGenDate,
        #         returnWeekday(startGenDate - timedelta(7))
        #     ]
        #     #Sumo las filas a la lista y devuelvo lista
        #     return [[showFeed], avanceIBMS, genIBMS]


        elif promoPckg == 'NT':
            #el Avance
            strAvance = unidecode("Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, showFeed,
                                        dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                promoCode.upper() + " AV FN", 0, 3000, 3000,
                strAvance.upper(), "NORTH", '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN FN', 0, 3000, 3000,
                strGen.upper(), "NORTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], avanceIBMS, genIBMS]
        elif promoPckg == 'PUNTUAL':
            #Solo Avance(el Redux A cont va por Feed Sur). No hay Gen.
            #Calcula la fecha de venta,, segun si es o no en el mismo mes que se emite) ¿Versiones Hoy? x ahora no
            strPuntualConMes = unidecode("El " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, showFeed,
                                        dstMexFlag, dstChiFlag)))
            strPuntualSinMes = unidecode(properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            if premiereDate.month != startDate.month:  #Si la puntual sale al aire el mes anterior, decimos mes.
                puntualIBMS = [
                    promoCode.upper() + " AV FN", 0, 3000, 3000,
                    strPuntualConMes.upper(), "SOUTH", '', 10, startDate,
                    premiereJustDate,
                    returnWeekday(startDate - timedelta(7))
                ]
            else:  #Si no, no.
                puntualIBMS = [
                    promoCode.upper() + " AV FN", 0, 3000, 3000,
                    strPuntualSinMes.upper(), "NORTH", '', 10, startDate,
                    premiereJustDate,
                    returnWeekday(startDate - timedelta(7))
                ]
            return [[showFeed], puntualIBMS]

        elif promoPckg == 'REP':
            #solo la generica, es un REP
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' REP FN', 0, 3000, 3000,
                strGen.upper(), "NORTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS]
        elif promoPckg == 'GEN':
            #armo las listas de IBMS - solo la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS]
        elif promoPckg == 'BUMP':
            showFeed = ['ALERTAS']
            #Bump a cont
            bumpAContIBMS = ['LOS BUMPS SE CARGAN EN EL FEED GOURMET SUR. BUMP DE', promoCode.upper(), 'NO CARGADO.'
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], bumpAContIBMS]
        else:
            showFeed = ['ALERTAS']
            #Bump a cont
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            return [[showFeed], errorMsg]            
    elif showFeed == 'EE':
        feed = 'LATAM'
        if promoPckg == 'ESTRENO':
            # #Avance con Fecha
            # strAvance = unidecode(properDay(premiereDate, 'SPA') + " " + str(
            #     premiereDate.day) + " " + str(
            #         properTime(premiereDate, showFeed,
            #                     dstMexFlag, dstChiFlag)))
            # avanceIBMS = [
            #     promoCode.upper() + " AV " + str(
            #         properDay(premiereDate, feedLang).upper()) + " " + str(
            #             premiereDate.day), 0, 3000, 3000,
            #     strAvance.upper(), feed, '', 10, startDate, avEndDate,
            #     returnWeekday(startDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            # strHoy = "HOY " + str(
            #     properTime(premiereDate, showFeed,
            #                 dstMexFlag, dstChiFlag))
            # hoyIBMS = [
            #     promoCode.upper() + ' ' + hoySuffix, 0, 3000, 3000,
            #     strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            # ]
            # #la generica
            # strGen = unidecode(str(genDateStr) + " " + str(
            #     properTime(premiereDate, showFeed,
            #                 dstMexFlag, dstChiFlag)))
            # genIBMS = [
            #     promoCode.upper() + ' GEN', 0, 3000, 3000,
            #     strGen.upper(), feed, '', 10, premiereJustDate, endGenDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Hoy (generica)
            # strHoy = "HOY " + str(
            #     properTime(premiereDate, showFeed,
            #                 dstMexFlag, dstChiFlag))
            # hoyGenIBMS = [
            #     promoCode.upper() + ' HOY', 0, 3000, 3000,
            #     strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            # ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], avanceIBMS, hoyIBMS, genIBMS, hoyGenIBMS]
        elif promoPckg == 'NT' or promoPckg == 'CAPS ESTRENO':
            #Avance con Fecha
            strAvance = unidecode(properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                promoCode.upper() + " AV " + str(
                    properDay(premiereDate, 'SPA').upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = "HOY " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Hoy (generica)
            strHoy = "HOY " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            hoyGenIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [[showFeed], avanceIBMS, hoyIBMS, genIBMS, hoyGenIBMS]

        elif promoPckg == 'PUNTUAL':
            #PUNTUAL con Fecha
            strAvance = unidecode(properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                promoCode.upper() + " PUNT " + str(
                    properDay(premiereDate, 'SPA').upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = " PUNT HOY " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [[showFeed], avanceIBMS, hoyIBMS]
        elif promoPckg == 'REP':
            #REP - versiones GEN y HOY
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' REP', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Hoy
            strHoy = "HOY " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS, hoyIBMS]
        elif promoPckg == 'GEN':
            #la generica (no hay avance)
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Hoy
            strHoy = "HOY " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS, hoyIBMS]
        elif promoPckg == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, 'SPA'))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genClub]
        elif promoPckg == 'BUMP':
            # showFeed = 'BUMPS EE'
            # #Bumps a cont
            # ahoraComienzaIBMS = [unidecode(
            # "AHORA COMIENZA - " + (str(showName)).upper()),
            # 0, 700, 700, "NEXT", feed, " ", 10, premiereJustDate,
            # bumpEndDate,
            # returnWeekday(premiereJustDate - timedelta(7))
            # ]
            # ensegVolvemosIBMS = [unidecode(
            # "ENSEGUIDA VOLVEMOS - " + (str(
            # showName)).upper()), 0, 700, 700,
            # "STAY TUNED", feed, " ", 10, premiereJustDate,
            # bumpEndDate,
            # returnWeekday(premiereJustDate - timedelta(7))
            # ]
            # yaVolvimosIBMS = [unidecode(
            # "YA VOLVIMOS - " + (str(showName)).upper()), 0,
            # 700, 700, "NOW", feed, " ", 10, premiereJustDate,
            # bumpEndDate,
            # returnWeekday(premiereJustDate - timedelta(7))
            # ]
            # return [
            # showFeed, ahoraComienzaIBMS, ensegVolvemosIBMS,
            # yaVolvimosIBMS
            # ]
        else:
            showFeed = ['ALERTAS']
            #Bump a cont
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            return [[showFeed], errorMsg]
    # elif showFeed == 'MCLATAM' or showFeed == 'MCUSA':
    #     if showFeed == 'MCLATAM':
    #         feed = 'LATAM'
    #     else:
    #         feed = 'USA'
        # if promoPckg == 'ESTRENO':
        #     #armo las listas de IBMS
        #     #el Avance
        #     strAvance = unidecode("Desde el " + properDay(
        #         premiereDate, 'SPA') + " " + str(
        #             premiereDate.day) + " de " + str(
        #                 properMonth(premiereDate, 'SPA')) + " " + str(
        #                     properTime(premiereDate, showFeed,
        #                                 dstMexFlag, dstChiFlag)))
        #     avanceIBMS = [
        #         promoCode.upper() + " AV " + feed, 0, 3000, 3000,
        #         strAvance.upper(), feed, '', 10, startDate, avEndDate,
        #         returnWeekday(startDate - timedelta(7))
        #     ]
        #     #la generica
        #     strGen = unidecode(str(genDateStr) + " " + str(
        #         properTime(premiereDate, showFeed,
        #                     dstMexFlag, dstChiFlag)))
        #     genIBMS = [
        #         promoCode.upper() + ' GEN ' + feed, 0, 3000, 3000,
        #         strGen.upper(), feed, '', 10, startGenDate, endGenDate,
        #         returnWeekday(startGenDate - timedelta(7))
        #     ]
        #     #Sumo las filas a la lista y devuelvo lista
        #     return [[showFeed], avanceIBMS, genIBMS]
        elif promoPckg == 'NT' or promoPckg == 'CAPS ESTRENO':
            #el Avance
            strAvance = unidecode("Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, showFeed,
                                        dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                promoCode.upper() + " AV " + feed, 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], avanceIBMS, genIBMS]
        elif promoPckg == 'PUNTUAL':
            #Solo Puntual
            strPuntualConMes = unidecode("El " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, showFeed,
                                        dstMexFlag, dstChiFlag)))
            strPuntualSinMes = unidecode(properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            if premiereDate.month != startDate.month:  #Si la puntual sale al aire el mes anterior, decimos mes.
                puntualIBMS = [
                    promoCode.upper() + " " + feed, 0, 3000, 3000,
                    strPuntualConMes.upper(), feed, '', 10, startDate,
                    premiereJustDate,
                    returnWeekday(startDate - timedelta(7))
                ]
            else:  #Si no, no.
                puntualIBMS = [
                    promoCode.upper() + " " + feed, 0, 3000, 3000,
                    strPuntualSinMes.upper(), feed, '', 10, startDate,
                    premiereJustDate,
                    returnWeekday(startDate - timedelta(7))
                ]
            return [[showFeed], puntualIBMS]
        elif promoPckg == 'REP':
            #solo la generica, es un REP
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            repIBMS = [
                promoCode.upper() + ' REP ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], repIBMS]
        elif promoPckg == 'GEN':
            #armo las listas de IBMS - solo la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genIBMS]
        elif promoPckg == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, 'SPA'))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genClub]
        # elif promoPckg == 'BUMP':
        #     if showFeed == 'MCLATAM':
        #         showFeed = 'BUMPS MC'
        #         #PROMO a cont (En MC no hay bumps, son promos A Cont que duran 30 segundos)
        #         bumpAContIBMS = [unidecode(
        #         'A CONT-' + (str(showName)).upper()), 0, 3000,
        #         3000, "A CONTINUACION", feed, " ", 10, startGenDate,
        #         bumpEndDate,
        #         returnWeekday(startGenDate - timedelta(7))
        #         ]
        #         #Sumo las filas a la lista y devuelvo lista
        #         return [
        #         [showFeed], bumpAContIBMS
        #         ]  #Crear version A cont de la promo - End Date en 2022
            elif showFeed == 'MCUSA': #si es de feed USA:
                showFeed = ['ALERTAS']
                #Bump a cont
                bumpAContIBMS = ['LOS BUMPS SE CARGAN EN EL FEED MAS CHIC LATAM. BUMP DE ' 
                    + promoCode.upper() + ' NO CARGADO.'
                ]
                #Sumo las filas a la lista y devuelvo lista
                return [[showFeed], bumpAContIBMS]
        else:
            showFeed = ['ALERTAS']
            #Bump a cont
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            return [[showFeed], errorMsg]
    elif showFeed == 'FALATAM' or showFeed == 'FABRASIL':
        # if showFeed == 'FALATAM':
        #     feed = 'LATAM + MEXICO'
        #     feedLang = 'SPA'
        #     tomorrowStr = 'MAÑANA '
        #     todayStr = 'HOY '
        # else:
        #     feed = 'BRASIL'
        #     feedLang = 'BRA'
        #     tomorrowStr = 'AMANHÃ '
        #     todayStr = 'HOJE '

        if promoPckg == 'ESTRENO' or promoPckg == 'NT' or promoPckg == 'CAPS ESTRENO':
            #Avance con Fecha (como hay version mañana, se acaba un dia antes)
            # strAvance = unidecode(properDay(premiereDate, feedLang) + " " + str(
            #     premiereDate.day) + " " + str(
            #         properTime(premiereDate, showFeed,
            #                     dstMexFlag, dstChiFlag)))
            # avanceIBMS = [
            #     promoCode.upper() + " ESTRENO " + str(
            #         properDay(premiereDate, feedLang).upper()) + " " + str(
            #             premiereDate.day), 0, 3000, 3000,
            #     strAvance.upper(), feed, '', 10, startDate, avEndDate - timedelta(1),
            #     returnWeekday(startDate - timedelta(7))
            # ]
            #Version Mañana -estreno
            strMan = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
            manStartDate = premiereJustDate - timedelta(1)
            manIBMS = [
                promoCode.upper() + " ESTRENO " + tomorrowStr , 0, 3000, 3000,
                strMan.upper(), feed, '', 10, manStartDate, 
                manStartDate, returnWeekday(manStartDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                promoCode.upper() + ' ESTRENO ' + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Mañana (generica)
            strManGen = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            manGenIBMS = [
                promoCode.upper() + ' GEN ' + tomorrowStr, 0, 3000, 3000,
                strManGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Hoy - GENERICA
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyGenIBMS = [
                promoCode.upper() + ' GEN ' + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], avanceIBMS, manIBMS, hoyIBMS, genIBMS, manGenIBMS, hoyGenIBMS]
        elif promoPckg == 'PUNTUAL': 
            #Avance con Fecha (como hay version mañana, se acaba un dia antes)
            strAvance = unidecode(properDay(premiereDate, feedLang) + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                promoCode.upper() + " PUNT " + str(
                    properDay(premiereDate, feedLang).upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate - timedelta(1),
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Mañana -estreno
            strMan = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
            manStartDate = premiereJustDate - timedelta(1)
            manIBMS = [
                promoCode.upper() + " " + tomorrowStr, 0, 3000, 3000,
                strMan.upper(), feed, '', 10, manStartDate, 
                manStartDate, returnWeekday(manStartDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                promoCode.upper() + " " + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [[showFeed], avanceIBMS, manIBMS, hoyIBMS]
        elif promoPckg == 'REP' or promoPckg == 'GEN':
            if promoPckg == 'REP':
                repGenString = " REP "
            else:
                repGenString = " GEN "
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + repGenString, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Mañana (generica)
            strManGen = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            manGenIBMS = [
                promoCode.upper() + repGenString + ' ' + tomorrowStr, 0, 3000, 3000,
                strManGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Hoy - GENERICA
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyGenIBMS = [
                promoCode.upper() + repGenString + ' ' + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], genIBMS, manGenIBMS, hoyGenIBMS]
        
        elif promoPckg == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, feedLang))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genClub]
        elif promoPckg == 'BUMP':
            # if showFeed == 'FALATAM':
            #     showFeed = 'BUMPS FA LATAM'
            #     #Bumps a cont
            #     ahoraComienzaIBMS = [unidecode(
            #     "ACONTINUACION - " + (str(showName)).upper()),
            #     0, 700, 700, "NEXT", feed, " ", 10, premiereJustDate,
            #     bumpEndDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            #     ]
            #     ensegVolvemosIBMS = [unidecode(
            #     "ENSEGUIDA REGRESAMOS - " + (str(
            #     showName)).upper()), 0, 700, 700,
            #     "STAY TUNED", feed, " ", 10, premiereJustDate,
            #     bumpEndDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            #     ]
            #     yaVolvimosIBMS = [unidecode(
            #     "CONTINUAMOS VIENDO - " + (str(showName)).upper()), 0,
            #     700, 700, "NOW", feed, " ", 10, premiereJustDate,
            #     bumpEndDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            #     ]
            #     return [
            #     showFeed, ahoraComienzaIBMS, yaVolvimosIBMS, ensegVolvemosIBMS
            #     ]
            # else:
            #     showFeed = 'BUMPS FA BRASIL'
            #     #Bumps a cont
            #     ahoraComienzaIBMS = [unidecode(
            #     "ASEGUIR - " + (str(showName)).upper()),
            #     0, 700, 700, "NEXT", feed, " ", 10, premiereJustDate,
            #     bumpEndDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            #     ]
            #     ensegVolvemosIBMS = [unidecode(
            #     "ESTAMOS APRESENTANDO - " + (str(
            #     showName)).upper()), 0, 700, 700,
            #     "STAY TUNED", feed, " ", 10, premiereJustDate,
            #     bumpEndDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            #     ]
            #     yaVolvimosIBMS = [unidecode(
            #     "VOLTAMOS A APRESENTAR - " + (str(showName)).upper()), 0,
            #     700, 700, "NOW", feed, " ", 10, premiereJustDate,
            #     bumpEndDate,
            #     returnWeekday(premiereJustDate - timedelta(7))
            #     ]
            #     return [
            #     showFeed, ahoraComienzaIBMS, yaVolvimosIBMS, ensegVolvemosIBMS
            #     ]
        else:
            showFeed = ['ALERTAS']
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            return [[showFeed], errorMsg]
    elif showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' \
    or showFeed == 'AMCLATAM' or showFeed == 'AMCBRASIL':
        if showFeed == 'AMCBRASIL':
            feed = 'BRAZIL'
            feedLang = 'BRA'
            tomorrowStr = 'AMANHÃ '
            todayStr = 'HOJE '
        else:
            feedLang = 'SPA'
            tomorrowStr = 'MAÑANA '
            todayStr = 'ESTA NOCHE '
            if showFeed == 'AMCSUR':
                feed = 'SOUTH'
            if showFeed == 'AMCLATAM':
                feed = 'LATAM'
            if showFeed == 'AMCNORCOL':
                feed = 'NORTH + COLOMBIA'
        # Faltan  SERIES GEN y SERIES EPISODICAS (VAN COMO GENERICAS)
        #(PROMO MEDIODIA SE VENDE COMO GENERICA - MARATON se vende como PUNTUAL)
        if promoPckg == 'STUNT':
            #la gen con fechas
            strGen = unidecode(str(genDateStr))
            avanceIBMS = [
                promoCode.upper() + " " + strGen.upper(), 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Esta noche / hoje
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                promoCode.upper() + " " + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [[showFeed], avanceIBMS, hoyIBMS]
        elif promoPckg == 'GEN_SERIES': 
            #GEN_SERIES es para las promos genéricas de series de AMC (con DIA, MANANA Y HOY)
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                unidecode(promoCode.upper() + ' GEN'), 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Mañana (generica)
            strManGen = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            manGenIBMS = [
                unidecode(promoCode.upper() + ' GEN ' + tomorrowStr), 0, 3000, 3000,
                strManGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7)), allowedDayTomorrow
            ]
            #Version Hoy - GENERICA
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyGenIBMS = [
                unidecode(promoCode.upper() + ' GEN ' + todayStr), 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7)), allowedDayToday
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], genIBMS, manGenIBMS, hoyGenIBMS]
        elif promoPckg == 'EPISODICA': 
            #Es igual que GEN_SERIES pero sin la palabra 'GEN'
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper(), 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Mañana (generica)
            strManGen = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            manGenIBMS = [
                unidecode(promoCode.upper() + ' ' + tomorrowStr), 0, 3000, 3000,
                strManGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7)), allowedDayTomorrow
            ]
            #Version Hoy - GENERICA
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyGenIBMS = [
                unidecode(promoCode.upper() + ' ' + todayStr), 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7)), allowedDayToday
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], genIBMS, manGenIBMS, hoyGenIBMS]
        elif promoPckg == 'PUNTUAL': 
            #Avance con Fecha (como hay version mañana, se acaba un dia antes)
            strAvance = unidecode(properDay(premiereDate, feedLang) + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            avanceIBMS = [
                unidecode(promoCode.upper() + " PUNT " + str(
                    properDay(premiereDate, feedLang).upper()) + " " + str(
                        premiereDate.day)), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate - timedelta(1),
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Mañana -estreno
            strMan = unidecode(tomorrowStr + str(
                properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
            manStartDate = premiereJustDate - timedelta(1)
            manIBMS = [
                unidecode(promoCode.upper() + " " + tomorrowStr), 0, 3000, 3000,
                strMan.upper(), feed, '', 10, manStartDate, 
                manStartDate, returnWeekday(manStartDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = unidecode(todayStr + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                unidecode(promoCode.upper() + " " + todayStr), 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [[showFeed], avanceIBMS, manIBMS, hoyIBMS]
        elif promoPckg == 'REP' or promoPckg == 'GEN':
            if promoPckg == 'REP':
                repGenString = " REP "
            else:
                repGenString = " GEN "
            #la generica
            strGen = unidecode(str(genDateStr) + " " + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
            genIBMS = [
                promoCode.upper() + repGenString, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [[showFeed], genIBMS]
        elif promoPckg == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = unidecode("PROMO PREMIO " + str(
                properMonth(premiereDate, feedLang)))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [[showFeed], genClub]
        else:
            showFeed = ['ALERTAS']
            #Bump a cont
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            return [[showFeed], errorMsg]

   

# reemplazar llamadas al dict por variables? AUN NO LO SE




#Y luego la version para la plani de CROSS, y dsp la de Seguimiento. Esas va en una funciones diferentes.
# def IBMSCrossListMaker (promo):