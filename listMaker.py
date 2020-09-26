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
    startGenDateTime = promo['genStartDate']  #fecha de inicio de la gen -dia y hora, para la peli del mes de EE
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
    
    #CASOS ESPECIALES: CLUBES, REDUX A CONT
    casosClub = ('EGSUR', 'MCLATAM', 'EE', 'FALATAM', 'AMCSUR')
    casosRedux = ('ESTRENO', 'NT', 'CAPS ESTRENO') #casos en lo que aplica hacer un redux a cont
    
    #primero las condiciones de showFeed -> defino strings
    avSuffix = 'AV'
    genSuffix = 'GEN'
    repSuffix = 'REP'
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
        clubFeedStr = 'SOUTH + NORTH'
        if showFeed == 'EGSUR':
            feedStr = 'SOUTH'
            avSuffix = 'AV FS'
            genSuffix = 'GEN FS'
            repSuffix = 'REP FS'
        else:
            feedStr = 'NORTH'
            avSuffix = 'AV FN'
            genSuffix = 'GEN FN'
            repSuffix = 'REP FN'
    elif showFeed == 'MCLATAM' or showFeed == 'MCUSA':
        strAvance = unidecode("Desde el " + properDay(
            premiereDate, feedLang) + " " + str(
                premiereDate.day) + " de " + str(
                    properMonth(premiereDate, feedLang)) + " " + str(
                        properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
        bumpDuration = 30
        bumpFeedStr = 'LATAM + USA'
        clubFeedStr = 'LATAM'
        if showFeed == 'MCUSA':
            feedStr = 'USA'
            avSuffix = 'AV USA'
            genSuffix = 'GEN USA'
            repSuffix = 'REP USA'

        else:
            feedStr = 'LATAM'
            avSuffix = 'AV LATAM'
            genSuffix = 'GEN LATAM'
            repSuffix = 'REP LATAM'
    elif showFeed == 'EE':
        feedStr = 'LATAM'
        avSuffix = ' ' + unidecode(properDay(premiereDate, feedLang) + " " + str(
            premiereDate.day)).upper()
        todayStr = 'HOY'
        strHoy = todayStr + ' ' + str(
            properTime(premiereDate, showFeed, dstMexFlag, dstChiFlag))
        bumpDuration = 7
        bumpFeedStr = 'LATAM'
        clubFeedStr = 'LATAM'
        ahoraComienzaPreffix = 'AHORA COMIENZA - '
        ensegVolvemosPreffix = 'ENSEGUIDA VOLVEMOS - '
        yaVolvimosPreffix = 'YA VOLVIMOS - '
    elif showFeed == 'FALATAM':
        feedStr = 'LATAM + MEXICO'  
        tomorrowStr = 'MAÑANA'
        todayStr = 'HOY'
        bumpDuration = 7
        bumpFeedStr = 'LATAM + MEXICO'
        clubFeedStr = 'LATAM + MEXICO'
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
            tomorrowStr = 'AMANHÃ'
            todayStr = 'HOJE'
        else:
            tomorrowStr = 'MAÑANA '
            todayStr = 'ESTA NOCHE '
            clubFeedStr = 'SOUTH NORTH LATAM COLOMBIA'
            if showFeed == 'AMCSUR':
                feedStr = 'SOUTH'
            if showFeed == 'AMCLATAM':
                feedStr = 'LATAM'
            if showFeed == 'AMCNORCOL':
                feedStr = 'NORTH + COLOMBIA'
        

    #luego IFS de promoPckg -> creo lista vacía, pueblo lista y retorno 
    outputIBMS = []
    if promoPckg == 'ESTRENO' or promoPckg == 'NT' \
        or promoPckg == 'CAPS ESTRENO':
        #el Avance
        avanceIBMS = [
            promoCode.upper() + ' ' + str(promoPckg) + ' ' + avSuffix, secondsToTC(0), secondsToTC(duration), 
            secondsToTC(duration), strAvance.upper(), feedStr, '', 
            10, startDate, avEndDate,
            returnWeekday(startDate - timedelta(7))
        ]
        #la generica
        strGen = unidecode(str(genDateStr) + " " + str(
            properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
        genIBMS = [
            promoCode.upper() + ' ' + str(promoPckg) + ' ' + genSuffix, secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
            returnWeekday(startGenDate - timedelta(7))
        ]

        if showFeed == 'EE' or showFeed == 'FALATAM' or showFeed == 'FABRASIL' \
        or showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' or showFeed == 'AMCBRASIL':
            #Versiones HOY y Gen Hoy
            strHoy = unidecode(todayStr + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
                secondsToTC(duration), secondsToTC(duration),
                strHoy.upper(), feedStr, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            hoyGenIBMS = [
                promoCode.upper() + ' ' + todayStr + " " + genSuffix, secondsToTC(0), 
                secondsToTC(duration), secondsToTC(duration),
                strHoy.upper(), feedStr, '', 10, startGenDate, endGenDate,
                returnWeekday((startGenDate - timedelta(7))), allowedDayToday
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
                #avance mañana
                strMan = unidecode(tomorrowStr + " " + str(
                    properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
                manStartDate = premiereJustDate - timedelta(1)
                manIBMS = [
                    promoCode.upper() + ' ' + unidecode(tomorrowStr) , secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strMan.upper(), feedStr, '', 10, manStartDate, 
                    manStartDate, returnWeekday(manStartDate - timedelta(7))
                ]
                #Version Mañana (generica)
                strManGen = unidecode(tomorrowStr + " " + str(
                    properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
                manGenIBMS = [
                    promoCode.upper() + ' ' + genSuffix + ' ' + unidecode(tomorrowStr), secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strManGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
                    returnWeekday((startGenDate - timedelta(7))), allowedDayTomorrow
                    ]
        #Sumo a la lista las promos
        if showFeed == 'EGSUR' or showFeed == 'EGNOR' or showFeed == 'MCLATAM' or showFeed == 'MCUSA':
            outputIBMS.extend([avanceIBMS, genIBMS])
        elif showFeed == 'EE':
            outputIBMS.extend([avanceIBMS, hoyIBMS, genIBMS, hoyGenIBMS])
        elif showFeed == 'FALATAM' or showFeed == 'FABRASIL' or \
            showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' \
            or showFeed == 'AMCBRASIL':
            outputIBMS.extend([avanceIBMS, manIBMS, hoyIBMS, genIBMS, manGenIBMS, hoyGenIBMS])

    elif promoPckg == 'PUNTUAL':
        #Calcula la fecha de venta, segun si es o no en el mismo mes que se emite
        if premiereDate.month != startDate.month:  #Si la puntual sale al aire el mes anterior, decimos mes.
            strPuntual = unidecode(properDay(
                        premiereDate, feedLang) + " " + str(
                        premiereDate.day) + " de " + str(
                                properMonth(premiereDate, feedLang)) + " " + str(
                                    properTime(premiereDate, showFeed,
                                                dstMexFlag, dstChiFlag)))
        else:  #Si no, no.
            strPuntual = unidecode(properDay(premiereDate, feedLang) + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
        puntualIBMS = [
            promoCode.upper() + " " + str(properDay(premiereDate, feedLang).upper())
            + " " + str(premiereDate.day), 
            secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strPuntual.upper(), feedStr, '', 10, startDate,
            premiereJustDate,
            returnWeekday(startDate - timedelta(7))
            ]
        #versions con fecha, HOY y mañana para EE, F&A, AMC
        if showFeed == 'EE' or showFeed == 'FALATAM' or showFeed == 'FABRASIL' \
        or showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' or showFeed == 'AMCBRASIL':
            #Versiones HOY
            strHoy = unidecode(todayStr + " " + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
            hoyIBMS = [
                promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
                secondsToTC(duration), secondsToTC(duration),
                strHoy.upper(), feedStr, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            if showFeed == 'FALATAM' or showFeed == 'FABRASIL' or \
            showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' \
            or showFeed == 'AMCBRASIL':
                #sobreescribo los avances (como hay version mañana,se acaban un dia antes)
                puntualIBMS = [
                    promoCode.upper() + ' ' + str(properDay(premiereDate, feedLang).upper())
                    + " " + str(premiereDate.day), secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strAvance.upper(), feedStr, '', 10, startDate, avEndDate - timedelta(1),
                    returnWeekday(startDate - timedelta(7))
                    ]
                #avance mañana
                strMan = unidecode(tomorrowStr + str(
                    properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
                manStartDate = premiereJustDate - timedelta(1)
                manIBMS = [
                    promoCode.upper() + ' ' + unidecode(tomorrowStr) , secondsToTC(0), 
                    secondsToTC(duration), secondsToTC(duration),
                    strMan.upper(), feedStr, '', 10, manStartDate, 
                    manStartDate, returnWeekday(manStartDate - timedelta(7))
                ]
        #Sumo a la lista las promos
        if showFeed == 'EGSUR' or showFeed == 'EGNOR' or showFeed == 'MCLATAM' or showFeed == 'MCUSA':
            outputIBMS.append(puntualIBMS)
        elif showFeed == 'EE':
            outputIBMS.extend([puntualIBMS, hoyIBMS])
        elif showFeed == 'FALATAM' or showFeed == 'FABRASIL' or \
            showFeed == 'AMCSUR' or showFeed == 'AMCNORCOL' or showFeed == 'AMCLATAM' \
            or showFeed == 'AMCBRASIL':
            outputIBMS.extend([puntualIBMS, manIBMS, hoyIBMS])


        #Sumo a la lista las promos de MC y GOURMET que no habia sumado antes
        

    elif promoPckg == 'REP' or promoPckg == 'GEN':
        #replaqueos y genericas
        if promoPckg == 'REP':
            suffix = repSuffix 
        else:
            suffix = genSuffix
        strGen = unidecode(str(genDateStr) + " " + str(
        properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
        genIBMS = [
        promoCode.upper() + ' ' + suffix, secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
        strGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
        returnWeekday(startGenDate - timedelta(7))
        ]
        #Sumo las filas a la lista y devuelvo lista
        outputIBMS.append(genIBMS)

    elif promoPckg == 'CLUB' and showFeed in casosClub:
        #armo una lista con un solo item, la promo del club
        strGen = unidecode("PROMO PREMIO " + str(
        properMonth(premiereDate, feedLang)))
        genClub = [
        promoCode.upper(), secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
        strGen.upper(), clubFeedStr, '', 10, startGenDate, endGenDate,
        returnWeekday(startGenDate - timedelta(7))
        ]
        outputIBMS.append(genClub)
        
    elif promoPckg == 'STUNT' and 'AMC' in showFeed:
        #la gen con fechas
        strGen = unidecode(str(genDateStr))
        avanceIBMS = [
            promoCode.upper() + " " + strGen.upper(), 
            secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strGen.upper(), feedStr, '', 10, startDate, avEndDate,
            returnWeekday(startDate - timedelta(7))
        ]
        #Version Esta noche / hoje
        strHoy = unidecode(todayStr + str(
            properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
        hoyIBMS = [
            promoCode.upper() + " " + todayStr, 
            secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strHoy.upper(), feedStr, '', 10, premiereJustDate, endGenDate,
            returnWeekday(premiereJustDate - timedelta(7))
        ]
        outputIBMS.extend([avanceIBMS, hoyIBMS])

    elif promoPckg == 'GEN_AMC' and 'AMC' in showFeed: 
        #GEN_SERIES es para las promos genéricas de series de AMC (con DIA, MANANA Y HOY)
        #la generica
        strGen = unidecode(str(genDateStr) + " " + str(
            properTime(premiereDate, showFeed,
                        dstMexFlag, dstChiFlag)))
        genIBMS = [
            promoCode.upper() + ' ' + genSuffix, secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
            returnWeekday(startGenDate - timedelta(7))
        ]
        #Version Mañana (generica)
        strManGen = unidecode(tomorrowStr + str(
            properTime(premiereDate, showFeed,
                dstMexFlag, dstChiFlag)))
        manGenIBMS = [
        promoCode.upper() + ' ' + genSuffix + ' ' + unidecode(tomorrowStr), secondsToTC(0), 
        secondsToTC(duration), secondsToTC(duration),
        strManGen.upper(), feedStr, '', 10, startGenDate, endGenDate,
        returnWeekday(startGenDate - timedelta(7)), allowedDayTomorrow
        ]
        #Version Hoy - GENERICA
        strHoy = unidecode(todayStr + str(
                    properTime(premiereDate, showFeed,
                                dstMexFlag, dstChiFlag)))
        hoyGenIBMS = [
            promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
            secondsToTC(duration), secondsToTC(duration),
            strHoy.upper(), feedStr, '', 10, startGenDate, endGenDate,
            returnWeekday(startGenDate - timedelta(7)), allowedDayToday
        ]
        #Sumo las filas a la lista y devuelvo lista
        outputIBMS.extend([genIBMS, manGenIBMS, hoyGenIBMS])

    elif showFeed == 'EE' and promoPckg == 'PELI DEL MES':
        #Puntual para la primera pasada
        strPuntual1 = unidecode(properDay(premiereDate, feedLang) + " " + str(
            premiereDate.day) + " " + str(
                properTime(premiereDate, showFeed,
                    dstMexFlag, dstChiFlag)))
        puntualIBMS1 = [
            promoCode.upper() + " " + str(properDay(premiereDate, feedLang).upper())
            + " " + str(premiereDate.day), 
            secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strPuntual1.upper(), feedStr, '', 10, startDate,
            (premiereJustDate - timedelta(1)),
            returnWeekday(startDate - timedelta(7))
            ]
        strHoy1 = unidecode(todayStr + ' ' + str(
                properTime(premiereDate, showFeed,
                            dstMexFlag, dstChiFlag)))
        hoyIBMS1 = [
            promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
            secondsToTC(duration), secondsToTC(duration),
            strHoy1.upper(), feedStr, '', 10, premiereJustDate, premiereJustDate,
            returnWeekday(premiereJustDate - timedelta(7))
        ]
        #Puntual para la segunda pasada (menos dias al aire)
        #Uso el startGenDateTime como fecha y hora de aire de la segunda pasada
        strPuntual2 = unidecode(properDay(startGenDateTime, feedLang) + " " + str(
            startGenDateTime.day) + " " + str(
                properTime(startGenDateTime, showFeed,
                    dstMexFlag, dstChiFlag)))
        puntualIBMS2 = [
            promoCode.upper() + " " + str(properDay(startGenDateTime, feedLang).upper())
            + " " + str(startGenDateTime.day), 
            secondsToTC(0), secondsToTC(duration), secondsToTC(duration),
            strPuntual2.upper(), feedStr, '', 10, (premiereJustDate + timedelta(1)),
            (startGenDate - timedelta(1)),
            returnWeekday(premiereJustDate - timedelta(7))
            ]
        strHoy2 = unidecode(todayStr + ' ' +str(
                properTime(startGenDateTime, showFeed,
                            dstMexFlag, dstChiFlag)))
        hoyIBMS2 = [
            promoCode.upper() + ' ' + todayStr, secondsToTC(0), 
            secondsToTC(duration), secondsToTC(duration),
            strHoy2.upper(), feedStr, '', 10, startGenDate, startGenDate,
            returnWeekday(startGenDate - timedelta(7))
        ]
        outputIBMS.extend([puntualIBMS1, hoyIBMS1, puntualIBMS2, hoyIBMS2])
   
    elif promoPckg == 'BUMP':
        if showFeed == 'EGSUR' or showFeed == 'MCLATAM': 
            #Aca va el bump a Cont *1
            bumpAContIBMS = [
            'A CONT-' + (str(showName)).upper(), secondsToTC(0), secondsToTC(bumpDuration),
            secondsToTC(bumpDuration), "A CONTINUACION", bumpFeedStr, " ", 10,
            startGenDate, bumpEndDate,
            returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista
            outputIBMS.extend([bumpAContIBMS])
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

            outputIBMS.extend([ahoraComienzaIBMS, ensegVolvemosIBMS,
            yaVolvimosIBMS])
        else:
            errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
                + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
            ]
            outputIBMS.extend([errorMsg])

    else:
        errorMsg = ['Disculpe, el tipo de promo ' + str(promoPckg) + ' solicitado para la promo ' 
            + promoCode.upper() + ' no esta disponible para la señal ' + str(showFeed)
        ]
        outputIBMS.extend([errorMsg])

    # If de casos especiales
    if showFeed == 'EGSUR' and promoPckg in casosRedux: #Redux a cont - caso especial para EGSUR y ESTRENO
        reduxAContIBMS = [
        promoCode.upper() + ' REDUX A CONT', secondsToTC(0), secondsToTC(15), secondsToTC(15),
        "A CONTINUACION", "SOUTH + NORTH", '', 10, startGenDate,
        endGenDate,
        returnWeekday(startGenDate - timedelta(7))
        ]
        outputIBMS.extend([reduxAContIBMS])

        #falta refinar y definir el formato de output
        #Y luego la version para la plani de CROSS, y dsp la de Seguimiento. Esas va en una funciones diferentes.
    return outputIBMS

feeds = ['EGSUR', 'EGNOR', 'MCLATAM', 'MCUSA', 'EE', 'AMCSUR', 'AMCNORCOL', 'AMCLATAM', 'AMCBRASIL', 
  'FALATAM', 'FABRASIL']
packs = ['ESTRENO', 'NT', 'CAPS ESTRENO', 'REP', 'GEN', 'PUNTUAL', 'CLUB', 'STUNT', 'GEN_AMC', 'BUMP', 'PELI DEL MES'] 



promo1 = {
'showFeed': 'EGSUR',
'showName': 'BREAKING MUSIC 01',
'promoPckg': 'ESTRENO',
'duration': 30,
'premiereDate': datetime(2020,10,2,22),
'genDateStr': 'MIÉRCOLES',
'genStartDate': datetime(2020,10,1,22,35),
'endDate': datetime(2020,10,31,18),
'dstMex': True, 
'dstChi': True,
'crossChannel': False,
'megaCable':	False,
'a&e':	False,
'cines':	False,
'foxSports': False
} 

# test para TODAS las posibilidades
# promo2 = promo1.copy()
# for feed in feeds:
#     promo2['showFeed'] = feed
#     for pack in packs:
#         promo2['promoPckg'] = pack
#         print('FEED: ', feed, 'promoPckg: ', pack)
#         print (IBMSlistMaker(promo2))



# feed = promo1['showFeed']
# pack = promo1['promoPckg']
# print('FEED: ', feed, 'promoPckg: ', pack)
# print (IBMSlistMaker(promo1))





