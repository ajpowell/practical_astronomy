import logging
import math
import datetime
import astro_constants
import astro_utils


# Initialise logging module
logging.root.handlers = []
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    # datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
    # level=logging.DEBUG
    )

def precalcs_sun(D):
    N = astro_utils.alignNumber((360.0/365.2422) * D, 360)

    Ms = astro_utils.alignNumber(N + astro_constants.sun_EclipticLongitudeAtEpoch - astro_constants.sun_EclipticLongitudeOfPerigee, 360)

    Es = (360/astro_constants.pi) * astro_constants.sun_eccentricity * math.sin(math.radians(Ms))

    return (N, Ms, Es)

def intradayMotion_moon(D, Lm, Bm, t0, t_new):

    N, Ms, Es = precalcs_sun(D)

    Ls = astro_utils.alignNumber(N + Es + astro_constants.sun_EclipticLongitudeAtEpoch, 360)

    l = astro_utils.alignNumber((13.176396 * D) + astro_constants.moon_EclipticLongitudeAtEpoch, 360)

    Mm = astro_utils.alignNumber(l - (0.111404 * D) - astro_constants.moon_EclipticLongitudeOfPerigee, 360)

    Nm = astro_utils.alignNumber(astro_constants.moon_NodeLongitudeAtEpoch - (0.0529539 * D), 360)

    Ev = 1.2739 * math.sin(math.radians((2* (l - Ls)) - Mm))

    Ae = 0.1858 * math.sin(math.radians(Ms))
    A3 = 0.37 * math.sin(math.radians(Ms))

    Mmc = Mm + Ev - Ae - A3

    Ec = 6.2886 * math.sin(math.radians(Mmc))

    A4 = 0.214 * math.sin(math.radians(2 * Mmc))

    lc = l + Ev + Ec - Ae + A4

    V = 0.6583 * math.sin(math.radians(2 * (lc - Ls)))

    lcc = lc + V

    Nmc = Nm - 0.16 * math.sin(math.radians(Ms))

    logging.debug('Ls:      {}'.format(Ls))
    logging.debug('Bm:      {}'.format(Bm))
    logging.debug('lcc:     {}'.format(lcc))
    logging.debug('Nmc:     {}'.format(Nmc))
    logging.debug('Mmc:     {}'.format(Mmc))
    logging.debug('t0:      {}'.format(t0))

    dB = 0.05 * math.cos(math.radians(lcc - Nmc))
    dL = 0.55 + 0.06 * math.cos(math.radians(Mmc))

    logging.debug('dB:      {}'.format(dB))
    logging.debug('dL:      {}'.format(dL))

    dt = t_new - t0

    logging.debug('dt:      {}'.format(dt))

    B = Bm + (dB * dt)
    L = Lm + (dL * dt)

    logging.debug('B:       {}'.format(B))
    logging.debug('L:       {}'.format(L))

    return (L, B)

def positionMoon(D):
    # Section 61 - Calculating the Moon's position

    # Need suns position too
    N, Ms, Es = precalcs_sun(D)

    Ls = astro_utils.alignNumber(N + Es + astro_constants.sun_EclipticLongitudeAtEpoch, 360)

    # print(Ls)
    # print(Ms)

    l = astro_utils.alignNumber((13.176396 * D) + astro_constants.moon_EclipticLongitudeAtEpoch, 360)

    # print(l)

    Mm = astro_utils.alignNumber(l - (0.111404 * D) - astro_constants.moon_EclipticLongitudeOfPerigee, 360)

    # print(Mm)

    Nm = astro_utils.alignNumber(astro_constants.moon_NodeLongitudeAtEpoch - (0.0529539 * D), 360)

    # print(Nm)

    # step 7
    Ev = 1.2739 * math.sin(math.radians((2* (l - Ls)) - Mm))

    # print(Ev)

    # step 8
    Ae = 0.1858 * math.sin(math.radians(Ms))
    A3 = 0.37 * math.sin(math.radians(Ms))

    # print(Ae)
    # print(A3)

    # step 9
    Mmc = Mm + Ev - Ae - A3

    # print(Mmc)

    # step 10
    Ec = 6.2886 * math.sin(math.radians(Mmc))

    # print(Ec)

    A4 = 0.214 * math.sin(math.radians(2 * Mmc))
    # print(A4)

    lc = l + Ev + Ec - Ae + A4

    # print(lc)

    V = 0.6583 * math.sin(math.radians(2 * (lc - Ls)))

    # print(V)

    lcc = lc + V

    # print(lcc)

    Nmc = Nm - 0.16 * math.sin(math.radians(Ms))

    # print(Nmc)

    y = math.sin(math.radians(lcc - Nmc)) * math.cos(math.radians(astro_constants.moon_OrbitInclination))
    x = math.cos(math.radians(lcc - Nmc))

    # print(y)
    # print(x)

    A = math.degrees(math.atan(y/x))
    # print(A)

    A = astro_utils.fixAtanAmbiguity(A, x, y)

    # print(A)

    Lm = A + Nmc
    Bm = math.degrees(math.asin(math.sin(math.radians(lcc - Nmc)) * math.sin(math.radians(astro_constants.moon_OrbitInclination))))

    # Calculate phase of the moon - Section 63
    Dm = lcc - Ls

    phase = 0.5 * ( 1 - math.cos(math.radians(Dm)))
    distance = distanceMoon(Mmc, Ec)

    

    return (Lm, Bm, phase, distance)

def moonRiseSet(year, month, day, lat, long):
    # Section 66
    days = astro_utils.daysSinceEpoch(year, month, day)

    Lm1, Bm1, phase, distance = positionMoon(days)
    print('Lm1:      {}'.format(Lm1))
    print('Bm1:      {}'.format(Bm1))

    Rm1, Dm1 = astro_utils.coords_EclipticToEquatorial(Lm1, Bm1)

    print('Rm1:      {}'.format(Rm1))
    print('Dm1:      {}'.format(Dm1))

    print('')

    Lm2, Bm2 = intradayMotion_moon(days, Lm1, Bm1, 0, 12)

    # Lm2, Bm2, F = positionMoon(days + 0.5)
    print('Lm2:      {}'.format(Lm2))
    print('Bm2:      {}'.format(Bm2))

    Rm2, Dm2 = astro_utils.coords_EclipticToEquatorial(Lm2, Bm2)

    print('Rm2:      {}'.format(Rm2))
    print('Dm2:      {}'.format(Dm2))

    print('')

    rho_sin_phi, rho_cos_phi = astro_utils.geocentricParallax(lat, 0.0)

    print('rho_sin_phi:{}'.format(rho_sin_phi))
    print('rho_cos_phi:{}'.format(rho_cos_phi))

    r = 60.268322 * distance

    print('r:          {}'.format(r))
    # Part complete...


def distanceMoon(Mmc, Ec):
    Pc = (1 - (astro_constants.moon_eccentricity * astro_constants.moon_eccentricity)) / (1 + (astro_constants.moon_eccentricity * math.cos(math.radians(Mmc + Ec))))

    print('Pc:       {}'.format(Pc))

    return Pc


def main():
    print('')
    print('Moon position')
    print('')

    days = astro_utils.daysSinceEpoch(1979, 2, 26)
    days = -307.332755
    Lm, Bm, phase, distance = positionMoon(days)

    Rm, Dm = astro_utils.coords_EclipticToEquatorial(Lm, Bm)

    print('RA:  {}'.format(astro_utils.displayTime(Rm)))
    print('Dec: {}'.format(astro_utils.displayAngle(Dm)))
    print('Moon phase: {:01.1f}'.format(phase))

    print('--------')
    moonRiseSet(1979, 9, 6, 52, 0)

    print('--------')
    # hourlymotion_moon(-307.332755, 337.011006, 0.991990, 16, 17)

    # rho_sin_phi, rho_cos_phi = astro_utils.geocentricParallax(50.0, 60.0)

    # Pc = distanceMoon(-359.735278, 0.029055)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.debug('****** Debug mode enabled ******')

    main()