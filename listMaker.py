from naming import returnWeekday, properTime, properMonth, properDay
from datetime import date, datetime, timedelta


def listMaker(promo):
    '''
    IN: promo (dict):info a promocionar, segun claves de variables
    destination (str): tipo de lista que quiere generar. opciones 'promosIBMS' , 'bumpsIBMS'.
    (coming soon: 'cross', 'seguimiento' , 'graficas', 'reporte')
    OUT: lista con todas las versiones de esa promo (para todas las planis? A CONF)
    '''

    #Fechas
    showFeed = [promo['showFeed']]
    premiereDate = promo['premiereDate']
    premiereJustDate = premiereDate.date()
    startDate = premiereDate.date() - timedelta(
        14)  #fecha inicio para avances y puntuales -solo dia
    avEndDate = premiereDate.date() - timedelta(
        1)  #que el avance deje de salir un día antes del estreno
    startGenDate = promo['genStartDate'].date(
    )  #fecha de inicio de la gen -solo dia
    endGenDate = promo['endDate'].date()  #fecha fin de las promos gen
    bumpEndDate = date(2022, 12, 31)  #fecha de fin para los bumps

    approvDeadline = returnWeekday(
        startDate - timedelta(9))  #para plani Seguimiento
    txtDeadline = returnWeekday(
        startDate - timedelta(15))  #para plani Seguimiento
    dueDate = returnWeekday(startDate - timedelta(7))  #para plani Seguimiento

    #para hacer el nombre 2020_12_etc:
    promoCode = str(premiereDate.year) + "_" + str(
        premiereDate.month) + "_" + (str(promo['showName']))
        
    if promo['showFeed'] == 'EGSUR':
        if promo['promoPckg'] == 'ESTRENO':
            #armo las listas de IBMS
            #el Avance
            strAvance = "Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV FS", 0, 3000, 3000,
                strAvance.upper(), "SOUTH", '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
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
            return [showFeed, avanceIBMS, genIBMS, reduxAContIBMS]
        elif promo['promoPckg'] == 'NT' or promo['promoPckg'] == 'CAPS ESTRENO':
            #el Avance
            strAvance = "Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV FS", 0, 3000, 3000,
                strAvance.upper(), "SOUTH", '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
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
            return [showFeed, avanceIBMS, genIBMS, reduxAContIBMS]
        elif promo['promoPckg'] == 'PUNTUAL':
            #Solo Avance y el Redux A cont. No hay Gen.
            #Calcula la fecha de venta,, segun si es o no en el mismo mes que se emite) ¿Versiones Hoy?
            strPuntualConMes = "El " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            strPuntualSinMes = properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
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
            return [showFeed, puntualIBMS, reduxAContIBMS]

        elif promo['promoPckg'] == 'REP':
            #armo las listas de IBMS - solo la generica, es un REP
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' REP FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS]
        elif promo['promoPckg'] == 'GEN':
            #armo las listas de IBMS - solo la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS]
        elif promo['promoPckg'] == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, 'SPA'))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), "SOUTH + NORTH", '', 10, startGenDate,
                endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genClub]
        elif promo['promoPckg'] == 'BUMP':
            showFeed = 'BUMPS EG SUR'
            #Bump a cont
            bumpAContIBMS = [
                'A CONT-' + (str(promo['showName'])).upper(), 0, 500,
                500, "A CONTINUACION", "SOUTH + NORTH + US", " ", 10,
                startGenDate, bumpEndDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, bumpAContIBMS]
        else:
            return []
    elif promo['showFeed'] == 'EGNOR':
        if promo['promoPckg'] == 'ESTRENO':
            #armo las listas de IBMS
            #el Avance
            strAvance = "Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV FN", 0, 3000, 3000,
                strAvance.upper(), "NORTH", '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN FN', 0, 3000, 3000,
                strGen.upper(), "NORTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, genIBMS]
        elif promo['promoPckg'] == 'NT':
            #el Avance
            strAvance = "Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV FN", 0, 3000, 3000,
                strAvance.upper(), "NORTH", '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN FN', 0, 3000, 3000,
                strGen.upper(), "NORTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, genIBMS]
        elif promo['promoPckg'] == 'PUNTUAL':
            #Solo Avance(el Redux A cont va por Feed Sur). No hay Gen.
            #Calcula la fecha de venta,, segun si es o no en el mismo mes que se emite) ¿Versiones Hoy? x ahora no
            strPuntualConMes = "El " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            strPuntualSinMes = properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
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
            return [showFeed, puntualIBMS]

        elif promo['promoPckg'] == 'REP':
            #solo la generica, es un REP
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' REP FN', 0, 3000, 3000,
                strGen.upper(), "NORTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS]
        elif promo['promoPckg'] == 'GEN':
            #armo las listas de IBMS - solo la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN FS', 0, 3000, 3000,
                strGen.upper(), "SOUTH", '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS]
        elif promo['promoPckg'] == 'BUMP':
            showFeed = ['ALERTAS']
            #Bump a cont
            bumpAContIBMS = ['LOS BUMPS SE CARGAN EN EL FEED GOURMET SUR. BUMP DE', promoCode.upper(), 'NO CARGADO.'
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, bumpAContIBMS]
            
        else:
            return []
    elif promo['showFeed'] == 'EE':
        feed = 'LATAM'
        if promo['promoPckg'] == 'ESTRENO':
            #Avance con Fecha
            strAvance = properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV " + str(
                    properDay(premiereDate, 'SPA').upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Hoy (generica)
            strHoy = "HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, genIBMS, hoyIBMS]
        elif promo['promoPckg'] == 'NT' or promo['promoPckg'] == 'CAPS ESTRENO':
            #Avance con Fecha
            strAvance = properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV " + str(
                    properDay(premiereDate, 'SPA').upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Hoy (generica)
            strHoy = "HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [showFeed, avanceIBMS, genIBMS, hoyIBMS]
        elif promo['promoPckg'] == 'REP':
            #REP - versiones GEN y HOY
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' REP', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Hoy
            strHoy = "HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS, hoyIBMS]
        elif promo['promoPckg'] == 'GEN':
            #la generica (no hay avance)
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Hoy
            strHoy = "HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS, hoyIBMS]
        elif promo['promoPckg'] == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, 'SPA'))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genClub]
        elif promo['promoPckg'] == 'BUMP':
            showFeed = 'BUMPS EE'
            #Bumps a cont
            ahoraComienzaIBMS = [
            "AHORA COMIENZA - " + (str(promo['showName'])).upper(),
            0, 700, 700, "NEXT", feed, " ", 10, premiereJustDate,
            bumpEndDate,
            returnWeekday(premiereJustDate - timedelta(7))
            ]
            ensegVolvemosIBMS = [
            "ENSEGUIDA VOLVEMOS - " + (str(
            promo['showName'])).upper(), 0, 700, 700,
            "STAY TUNED", feed, " ", 10, premiereJustDate,
            bumpEndDate,
            returnWeekday(premiereJustDate - timedelta(7))
            ]
            yaVolvimosIBMS = [
            "YA VOLVIMOS - " + (str(promo['showName'])).upper(), 0,
            700, 700, "NOW", feed, " ", 10, premiereJustDate,
            bumpEndDate,
            returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [
            showFeed, ahoraComienzaIBMS, ensegVolvemosIBMS,
            yaVolvimosIBMS
            ]
        else:
            return []
    elif promo['showFeed'] == 'MCLATAM' or promo['showFeed'] == 'MCUSA':
        if promo['showFeed'] == 'MCLATAM':
            feed = 'LATAM'
        else:
            feed = 'USA'
        if promo['promoPckg'] == 'ESTRENO':
            #armo las listas de IBMS
            #el Avance
            strAvance = "Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV " + feed, 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, genIBMS]
        elif promo['promoPckg'] == 'NT' or promo['promoPckg'] == 'CAPS ESTRENO':
            #el Avance
            strAvance = "Desde el " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " AV " + feed, 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, genIBMS]
        elif promo['promoPckg'] == 'PUNTUAL':
            #Solo Puntual
            strPuntualConMes = "El " + properDay(
                premiereDate, 'SPA') + " " + str(
                    premiereDate.day) + " de " + str(
                        properMonth(premiereDate, 'SPA')) + " " + str(
                            properTime(premiereDate, promo['showFeed'],
                                        promo['dstMex'], promo['dstChi']))
            strPuntualSinMes = properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
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
            return [showFeed, puntualIBMS]
        elif promo['promoPckg'] == 'REP':
            #solo la generica, es un REP
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            repIBMS = [
                promoCode.upper() + ' REP ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, repIBMS]
        elif promo['promoPckg'] == 'GEN':
            #armo las listas de IBMS - solo la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN ' + feed, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genIBMS]
        elif promo['promoPckg'] == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, 'SPA'))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genClub]
        elif promo['promoPckg'] == 'BUMP':
            if promo['showFeed'] == 'MCLATAM':
                showFeed = 'BUMPS MC'
                #PROMO a cont (En MC no hay bumps, son promos A Cont que duran 30 segundos)
                bumpAContIBMS = [
                'A CONT-' + (str(promo['showName'])).upper(), 0, 3000,
                3000, "A CONTINUACION", feed, " ", 10, startGenDate,
                bumpEndDate,
                returnWeekday(startGenDate - timedelta(7))
                ]
                #Sumo las filas a la lista y devuelvo lista
                return [
                [showFeed], bumpAContIBMS
                ]  #Crear version A cont de la promo - End Date en 2022
            elif promo['showFeed'] == 'MCUSA': #si es de feed USA:
                showFeed = ['ALERTAS']
                #Bump a cont
                bumpAContIBMS = ['LOS BUMPS SE CARGAN EN EL FEED MAS CHIC LATAM. BUMP DE', promoCode.upper(), 'NO CARGADO.'
                ]
                #Sumo las filas a la lista y devuelvo lista
                return [showFeed, bumpAContIBMS]
        else:
            return []

  


#Terminar señales: MC - diferencia horaria con USA. Atrasa Mex, no USA.
#AMC, F&A
#REVISAR LA CONDUCTA CON LOS BUMPS. QUE FEEDS DEJA Y QUE FEEDS NO. 
#QUE HACE CUANDO SE INGRESA UN BUMP A UN CANAL ERRONEO. OK con GOURMET NORTE y con MC USA
#CREAR UN METODO ESPECIAL PARA MANEJAR ALERTA
#Y luego la version para la plani de Seguimiento. Uff
