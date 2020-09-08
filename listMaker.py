from naming import returnWeekday, properTime, properMonth, properDay
from datetime import date, datetime, timedelta


def IBMSlistMaker(promo):
    '''
    IN: dict: info a promocionar, segun claves de variables
    
    OUT: [list of lists] lista con todas las versiones de esa promo para la planilla de IBMS.
    Cada fila de la planilla es una lista. 
    '''

    #Fechas
    showFeed = [promo['showFeed']]
    premiereDate = promo['premiereDate']
    premiereJustDate = premiereDate.date()
    startDate = premiereDate.date() - timedelta(14)  #fecha inicio para avances y puntuales -solo dia
    avEndDate = premiereDate.date() - timedelta(1)  #que el avance deje de salir un día antes del estreno
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
    promoCode = premiereJustDate.strftime('%Y_%m_') + (str(promo['showName']))
        
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
            #Version Hoy (estreno)
            strHoy = "HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
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
            hoyGenIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, hoyIBMS, genIBMS, hoyGenIBMS]
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
            #Version Hoy (estreno)
            strHoy = "HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
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
            hoyGenIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [showFeed, avanceIBMS, hoyIBMS, genIBMS, hoyGenIBMS]

        elif promo['promoPckg'] == 'PUNTUAL':
            #PUNTUAL con Fecha
            strAvance = properDay(premiereDate, 'SPA') + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " PUNT " + str(
                    properDay(premiereDate, 'SPA').upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = " PUNT HOY " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' HOY', 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [showFeed, avanceIBMS, hoyIBMS]
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
    elif promo['showFeed'] == 'FALATAM' or promo['showFeed'] == 'FABRASIL':
        if promo['showFeed'] == 'FALATAM':
            feed = 'LATAM + MEXICO'
            feedLang = 'SPA'
            tomorrowStr = 'MANANA '
            todayStr = 'HOY '
        else:
            feed = 'BRASIL'
            feedLang = 'BRA'
            tomorrowStr = 'AMANHA '
            todayStr = 'HOJE '
        
        if promo['promoPckg'] == 'ESTRENO' or promo['promoPckg'] == 'NT' or promo['promoPckg'] == 'CAPS ESTRENO':
            #Avance con Fecha (como hay version mañana, se acaba un dia antes)
            strAvance = properDay(premiereDate, feedLang) + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " ESTRENO " + str(
                    properDay(premiereDate, feedLang).upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate - timedelta(1),
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Mañana -estreno
            strMan = tomorrowStr + str(
                properTime(premiereDate, promo['showFeed'],
                    promo['dstMex'], promo['dstChi']))
            manStartDate = premiereJustDate - timedelta(1)
            manIBMS = [
                promoCode.upper() + " ESTRENO " + tomorrowStr , 0, 3000, 3000,
                strMan.upper(), feed, '', 10, manStartDate, 
                manStartDate, returnWeekday(manStartDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = todayStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + ' ESTRENO ' + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + ' GEN', 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Mañana (generica)
            strManGen = tomorrowStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            manGenIBMS = [
                promoCode.upper() + ' GEN ' + tomorrowStr, 0, 3000, 3000,
                strManGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Version Hoy - GENERICA
            strHoy = todayStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyGenIBMS = [
                promoCode.upper() + ' GEN ' + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, avanceIBMS, manIBMS, hoyIBMS, genIBMS, manGenIBMS, hoyGenIBMS]
        elif promo['promoPckg'] == 'PUNTUAL': 
            #Avance con Fecha (como hay version mañana, se acaba un dia antes)
            strAvance = properDay(premiereDate, feedLang) + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " PUNT " + str(
                    properDay(premiereDate, feedLang).upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate - timedelta(1),
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Mañana -estreno
            strMan = tomorrowStr + str(
                properTime(premiereDate, promo['showFeed'],
                    promo['dstMex'], promo['dstChi']))
            manStartDate = premiereJustDate - timedelta(1)
            manIBMS = [
                promoCode.upper() + " " + tomorrowStr, 0, 3000, 3000,
                strMan.upper(), feed, '', 10, manStartDate, 
                manStartDate, returnWeekday(manStartDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = todayStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + " " + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [showFeed, avanceIBMS, manIBMS, hoyIBMS]
        elif promo['promoPckg'] == 'REP' or promo['promoPckg'] == 'GEN':
            if promo['promoPckg'] == 'REP':
                repGenString = " REP "
            else:
                repGenString = " GEN "
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + repGenString, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Mañana (generica)
            strManGen = tomorrowStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            manGenIBMS = [
                promoCode.upper() + repGenString + ' ' + tomorrowStr, 0, 3000, 3000,
                strManGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Version Hoy - GENERICA
            strHoy = todayStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyGenIBMS = [
                promoCode.upper() + repGenString + ' ' + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, genIBMS, manGenIBMS, hoyGenIBMS]
        
        elif promo['promoPckg'] == 'CLUB':
            #armo una lista con un solo item, la promo del club
            strGen = "PROMO PREMIO " + str(
                properMonth(premiereDate, feedLang))
            genClub = [
                promoCode.upper(), 0, 2500, 2500,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(startGenDate - timedelta(7))
            ]
            return [showFeed, genClub]
        elif promo['promoPckg'] == 'BUMP': #Hecho para Latam, falta Brasil
            if promo['showFeed'] == 'FALATAM':
                showFeed = 'BUMPS FA LATAM'
                #Bumps a cont
                ahoraComienzaIBMS = [
                "ACONTINUACION - " + (str(promo['showName'])).upper(),
                0, 700, 700, "NEXT", feed, " ", 10, premiereJustDate,
                bumpEndDate,
                returnWeekday(premiereJustDate - timedelta(7))
                ]
                ensegVolvemosIBMS = [
                "ENSEGUIDA REGRESAMOS - " + (str(
                promo['showName'])).upper(), 0, 700, 700,
                "STAY TUNED", feed, " ", 10, premiereJustDate,
                bumpEndDate,
                returnWeekday(premiereJustDate - timedelta(7))
                ]
                yaVolvimosIBMS = [
                "CONTINUAMOS VIENDO - " + (str(promo['showName'])).upper(), 0,
                700, 700, "NOW", feed, " ", 10, premiereJustDate,
                bumpEndDate,
                returnWeekday(premiereJustDate - timedelta(7))
                ]
                return [
                showFeed, ahoraComienzaIBMS, yaVolvimosIBMS, ensegVolvemosIBMS
                ]
            else:
                showFeed = 'BUMPS FA BRASIL'
                #Bumps a cont
                ahoraComienzaIBMS = [
                "ASEGUIR - " + (str(promo['showName'])).upper(),
                0, 700, 700, "NEXT", feed, " ", 10, premiereJustDate,
                bumpEndDate,
                returnWeekday(premiereJustDate - timedelta(7))
                ]
                ensegVolvemosIBMS = [
                "ESTAMOS APRESENTANDO - " + (str(
                promo['showName'])).upper(), 0, 700, 700,
                "STAY TUNED", feed, " ", 10, premiereJustDate,
                bumpEndDate,
                returnWeekday(premiereJustDate - timedelta(7))
                ]
                yaVolvimosIBMS = [
                "VOLTAMOS A APRESENTAR - " + (str(promo['showName'])).upper(), 0,
                700, 700, "NOW", feed, " ", 10, premiereJustDate,
                bumpEndDate,
                returnWeekday(premiereJustDate - timedelta(7))
                ]
                return [
                showFeed, ahoraComienzaIBMS, yaVolvimosIBMS, ensegVolvemosIBMS
                ]
    elif promo['showFeed'] == 'AMCSUR' or promo['showFeed'] == 'AMCNORCOL' \
    or promo['showFeed'] == 'AMCLATAM' or promo['showFeed'] == 'AMCBRASIL':
        if promo['showFeed'] == 'AMCBRASIL':
            feed = 'BRAZIL'
            feedLang = 'BRA'
            tomorrowStr = 'AMANHA '
            todayStr = 'HOJE '
        else:
            feedLang = 'SPA'
            tomorrowStr = 'MANANA '
            todayStr = 'ESTA NOCHE '
            if promo['showFeed'] == 'AMCSUR':
                feed = 'SOUTH'
            if promo['showFeed'] == 'AMCLATAM':
                feed = 'LATAM'
            if promo['showFeed'] == 'AMCNORCOL':
                feed = 'NORTH + COLOMBIA'
        #CASOS ESPECIALES: STUNT - HECHO // 
        # Faltan MARATON y  EPISODICAS 
        #(PROMO MEDIODIA SE VENDE COMO GENERICA)
        if promo['promoPckg'] == 'STUNT':
            #la gen con fechas
            strGen = str(promo['genDateStr'])
            avanceIBMS = [
                promoCode.upper() + " " + strGen.upper(), 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startDate, avEndDate,
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Esta noche / hoje
            strHoy = todayStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + " " + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [showFeed, avanceIBMS, hoyIBMS]


        elif promo['promoPckg'] == 'PUNTUAL': 
            #Avance con Fecha (como hay version mañana, se acaba un dia antes)
            strAvance = properDay(premiereDate, feedLang) + " " + str(
                premiereDate.day) + " " + str(
                    properTime(premiereDate, promo['showFeed'],
                                promo['dstMex'], promo['dstChi']))
            avanceIBMS = [
                promoCode.upper() + " PUNT " + str(
                    properDay(premiereDate, feedLang).upper()) + " " + str(
                        premiereDate.day), 0, 3000, 3000,
                strAvance.upper(), feed, '', 10, startDate, avEndDate - timedelta(1),
                returnWeekday(startDate - timedelta(7))
            ]
            #Version Mañana -estreno
            strMan = tomorrowStr + str(
                properTime(premiereDate, promo['showFeed'],
                    promo['dstMex'], promo['dstChi']))
            manStartDate = premiereJustDate - timedelta(1)
            manIBMS = [
                promoCode.upper() + " " + tomorrowStr, 0, 3000, 3000,
                strMan.upper(), feed, '', 10, manStartDate, 
                manStartDate, returnWeekday(manStartDate - timedelta(7))
            ]
            #Version Hoy (estreno)
            strHoy = todayStr + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            hoyIBMS = [
                promoCode.upper() + " " + todayStr, 0, 3000, 3000,
                strHoy.upper(), feed, '', 10, premiereJustDate, premiereJustDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            return [showFeed, avanceIBMS, manIBMS, hoyIBMS]
        elif promo['promoPckg'] == 'REP' or promo['promoPckg'] == 'GEN':
            if promo['promoPckg'] == 'REP':
                repGenString = " REP "
            else:
                repGenString = " GEN "
            #la generica
            strGen = str(promo['genDateStr']) + " " + str(
                properTime(premiereDate, promo['showFeed'],
                            promo['dstMex'], promo['dstChi']))
            genIBMS = [
                promoCode.upper() + repGenString, 0, 3000, 3000,
                strGen.upper(), feed, '', 10, startGenDate, endGenDate,
                returnWeekday(premiereJustDate - timedelta(7))
            ]
            #Sumo las filas a la lista y devuelvo lista
            return [showFeed, genIBMS]
    else:
        return []

        

  




#AMC, F&A
# Faltan las versiones Puntuales en EE y F&A
# Falta F&A Brasil

#REVISAR LA CONDUCTA CON LOS BUMPS. QUE FEEDS DEJA Y QUE FEEDS NO. OK
#QUE HACE CUANDO SE INGRESA UN BUMP A UN CANAL ERRONEO. OK con GOURMET NORTE y con MC USA, falta el resto
# agregarlo a AMC. En AMC no implementamos bumps directamente.

#importar unidecode para que le saque los tildes y caracteres raros
# ej:
# import unidecode (hay que instalarlo primero)
# string3 = 'niño NIÑO'
# unidecode.unidecode(string3)



#Y luego la version para la plani de CROSS, y dsp la de Seguimiento. Esa va en una funcion diferente.
