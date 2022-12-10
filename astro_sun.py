import math
import datetime
import astro_constants
import astro_utils


def positionSun(D):
    N = astro_utils.alignNumber((360.0/365.2422) * D, 360)

    M = astro_utils.alignNumber(N + astro_constants.sun_EclipticLongitudeAtEpoch - astro_constants.sun_EclipticLongitudeOfPerigee, 360)

    Ec = (360/astro_constants.pi) * astro_constants.sun_eccentricity * math.sin(math.radians(M))

    Lc = astro_utils.alignNumber(N + Ec + astro_constants.sun_EclipticLongitudeAtEpoch, 360)

    return (Lc, 0)


def sunRiseSet(year, month, day, lat, long):

    days = astro_utils.daysSinceEpoch(year, month, day)

    Lc1, Bc1 = positionSun(days)

    Ah1, D1 = astro_utils.coords_EclipticToEquatorial(Lc1, Bc1)
    
    Lc2 = Lc1 + 0.985647
    Bc2 = Bc1
    Ah2, D2 = astro_utils.coords_EclipticToEquatorial(Lc2, Bc2)

    # long = 0.0
    # lat = 52.0

    LST1r, LST1s = astro_utils.convertRaDecToLST(Ah1, D1, lat)

    LST2r, LST2s = astro_utils.convertRaDecToLST(Ah2, D2, lat)

    Tr = (24.07 * LST1r)/(24.07 + LST1r - LST2r)
    Ts = (24.07 * LST1s)/(24.07 + LST1s - LST2s)

    Dp = (D1 + D2)/2.0

    # lat = 52
    Td = astro_utils.parallaxCorrection(astro_constants.sun_angularDiameter, astro_constants.sun_horizontalParallax, astro_constants.atmosphericRefraction, lat, Dp)

    # print(Td)
    # print('')

    Tr_corrected = Tr - Td
    Ts_corrected = Ts + Td

    print('Tr  {} -> {} UTC'.format(Tr_corrected, astro_utils.displayTime(astro_utils.convertGSTtoGMT(Tr_corrected, days, year))))
    print('Ts  {} -> {} UTC'.format(Ts_corrected, astro_utils.displayTime(astro_utils.convertGSTtoGMT(Ts_corrected, days, year))))
    


