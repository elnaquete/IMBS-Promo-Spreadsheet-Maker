from datetime import date, timedelta, datetime


def returnWeekday(date):
    """
    in: date object
    out: same date object is its weekday, earliest weekday available if not (if Sunday,
    will return the Friday before)
    Note: I use weekday method, where Monday is 0 and Sunday is 6
    """
    oneDay = timedelta(1)
    if date.weekday() == 5:
        date -= oneDay
    elif date.weekday() == 6:
        date -= 2 * oneDay
    return date


def properDay(date, lang):
    """
    IN:
    date:datetime object
    lang: (str) 'SPA' or 'BRA'
    OUT: string - date properly formatted for LatinAmerican Spanish or Portuguese
    """
    dias = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo",
    }
    diasBRA = {
        0: "segunda",
        1: "terça",
        2: "quarta",
        3: "quinta",
        4: "sexta",
        5: "sábado",
        6: "domingo",
    }
    if lang == "SPA":
        return dias[date.weekday()]
    elif lang == "BRA":
        return diasBRA[date.weekday()]


def properMonth(date, lang):
    """
    IN:
    date:datetime object
    lang: (str) 'SPA' or 'BRA'
    OUT: string - date.month in Spanish or Portuguese
    """
    meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }
    mesesBRA = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "avril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }
    if lang == "SPA":
        return meses[date.month]
    elif lang == "BRA":
        return mesesBRA[date.month]


def properTime(date, feed, mexDst, chiDst):
    """
    IN:
    date:datetime object
    feed (str), define am/PM format
    pack: (str) promo package (use promoPkcg variable)
    mexDst:(bool) True if +1, false if 0
    chiDst: (bool) True if +1, false if 0
    destination (int): 1=Seguimiento, 2=IBMS, 3=Asana, 4=Reporte
    OUT: string - date properly formatted for LatinAmerican Spanish
    """
    if feed == "EGSUR":
        return date.strftime("%H:%M")
    elif feed == "EGNOR":
        # calculo dif horarias (podria ir a funcion aparte?)
        mexTime = date
        if mexDst == True and chiDst == True:
            colTime = mexTime
            chiTime = mexTime + timedelta(0, 7200)  # sumo 2 h
        elif mexDst == False and chiDst == True:
            colTime = mexTime + timedelta(0, 3600)  # sump 1 h
            chiTime = mexTime + timedelta(0, 10800)  # sumo 3 h
        elif mexDst == True and chiDst == False:
            colTime = mexTime
            chiTime = mexTime + timedelta(0, 3600)  # sumo 2 h
        elif mexDst == False and chiDst == False:
            colTime = mexTime + timedelta(0, 3600)  # sump 1 h
            chiTime = mexTime + timedelta(0, 7200)  # sumo 2 h
        # devuelvo string
        dateItems = [
            mexTime.strftime("%-I:%M %p Méx"),
            colTime.strftime("%-I:%M %p Col"),
            chiTime.strftime("%-I:%M %p Chi"),
        ]
        return " ".join(dateItems)

    elif feed == "MCLATAM":
        colTime = date
        if chiDst == True:
            chiTime = colTime + timedelta(0, 7200)  # sumo 2 h
            argTime = colTime + timedelta(0, 7200)  # sumo 2 h
        else:
            chiTime = colTime + timedelta(0, 3600)  # sumo 1 h
            argTime = colTime + timedelta(0, 7200)  # sumo 2 h
        dateItems = [
            colTime.strftime("%-I:%M %p Col"),
            chiTime.strftime("%-I:%M %p Chi"),
            argTime.strftime("%-I:%M %p Arg"),
        ]
        return " ".join(dateItems)

    elif feed == "MCUSA":
        # El horario que marca la pauta es el de USA. Cuando Mex atrasa, cambia Mex, no usa.
        eastTime = date
        if mexDst == True:
            mexTime = eastTime - timedelta(0, 3600)  # resto 1 h
            dateItems = [
                mexTime.strftime("%-I:%M %p Méx"),
                eastTime.strftime("%-I:%M %p Este"),
            ]
            return " ".join(dateItems)
        else:
            mexTime = eastTime - timedelta(0, 7200)  # resto 1 h
            dateItems = [
                mexTime.strftime("%-I:%M %p Méx"),
                eastTime.strftime("%-I:%M %p Este"),
            ]
            return " ".join(dateItems)

    elif feed == "EE":
        argTime = date
        if mexDst == True and chiDst == True:  # 3 horarios, CHi con Arg
            mexTime = argTime - timedelta(0, 7200)  # resto 2 h
            venTime = argTime - timedelta(0, 3600)  # resto 1 h
            dateItems = [
                mexTime.strftime("%-I:%M %p Méx/Col"),
                venTime.strftime("%H:%M Ven"),
                argTime.strftime("%H:%M Arg/Chi"),
            ]
            return " ".join(dateItems)
        elif mexDst == False and chiDst == True:  # 4 horarios, Chi con Arg
            mexTime = argTime - timedelta(0, 10800)  # resto 3 h
            colTime = argTime - timedelta(0, 7200)  # resto 2 h
            venTime = argTime - timedelta(0, 3600)  # resto 1 h
            chiTime = argTime

            dateItems = [
                mexTime.strftime("%-I:%M %p Méx"),
                colTime.strftime("%-I:%M %p Col"),
                venTime.strftime("%H:%M Ven"),
                argTime.strftime("%H:%M Arg/Chi"),
            ]
            return " ".join(dateItems)
        elif mexDst == True and chiDst == False:  # 3 horarios, Chi con Ven
            mexTime = argTime - timedelta(0, 7200)  # resto 2 h
            venTime = argTime - timedelta(0, 3600)  # resto 1 h

            dateItems = [
                mexTime.strftime("%-I:%M %p Méx/Col"),
                venTime.strftime("%H:%M Ven/Chi"),
                argTime.strftime("%H:%M Arg"),
            ]
            return " ".join(dateItems)

        elif mexDst == False and chiDst == False:
            mexTime = argTime - timedelta(0, 10800)  # resto 3 h
            colTime = argTime - timedelta(0, 7200)  # resto 2 h
            venTime = argTime - timedelta(0, 3600)  # resto 1 h

            dateItems = [
                mexTime.strftime("%-I:%M %p Méx"),
                colTime.strftime("%-I:%M %p Col"),
                venTime.strftime("%H:%M Ven/Chi"),
                argTime.strftime("%H:%M Arg"),
            ]
            return " ".join(dateItems)
    elif feed == "AMCSUR":
        if date.minute == 0:
            return date.strftime("%Hhs")
        else:
            return date.strftime("%H:%Mhs")
    elif feed == "AMCNORCOL":
        if date.minute == 0:
            return date.strftime("%I%p").replace("AM", "am").replace("PM", "pm")
        else:
            return date.strftime("%I:%M%p").replace("AM", "am").replace("PM", "pm")
    elif feed == "AMCLATAM":
        argTime = date
        venTime = argTime - timedelta(0, 3600)  # resto 1 h
        perTime = argTime - timedelta(0, 7200)  # resto 1 h
        if chiDst == True:
            argString = "Arg/Chi"
            venString = "Ven"
            perString = "Per"
        else:
            argString = "Arg"
            venString = "Chi/Ven"
            perString = "Per"
        if date.minute == 0:
            dateItems = [
                argTime.strftime(argString + " %Hhs"),
                venTime.strftime(venString + " %Hhs"),
                perTime.strftime(perString + " %-I%p")
                .replace("AM", "am")
                .replace("PM", "pm"),
            ]
        else:
            dateItems = [
                argTime.strftime(argString + " %H:%Mhs"),
                venTime.strftime(venString + " %H:%Mhs"),
                perTime.strftime(perString + " %-I:%M%p")
                .replace("AM", "am")
                .replace("PM", "pm"),
            ]

        return " ".join(dateItems)

    elif feed == "AMCBRASIL":
        if date.minute == 0:
            return date.strftime("%Hh")
        else:
            return date.strftime("%Hh%M")
    elif feed == "FABRASIL":
        if date.minute == 0:
            return date.strftime("%Hh")
        else:
            return date.strftime("%Hh%M")
    elif feed == "FALATAM":
        argTime = date  # Mex tambien es este horario
        chiTime = argTime - timedelta(0, 3600)  # resto 2 h
        colTime = argTime - timedelta(0, 7200)  # resto 2 h
        if chiDst == True:
            dateItems = [
                argTime.strftime("%H:%M Méx/Arg/Chi"),
                colTime.strftime("%H:%M Col"),
            ]
            return " ".join(dateItems)
        else:
            dateItems = [
                argTime.strftime("%H:%M Méx/Arg"),
                chiTime.strftime("%H:%M Chi"),
                colTime.strftime("%H:%M Col"),
            ]
            return " ".join(dateItems)
