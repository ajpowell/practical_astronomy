import math
import datetime
import astro_constants
import astro_utils


def positionMoon(D):
    # Section 61 - Calculating the Moon's position
    N = astro_utils.alignNumber((360.0/365.2422) * D, 360)

    Ms = astro_utils.alignNumber(N + astro_constants.sun_EclipticLongitudeAtEpoch - astro_constants.sun_EclipticLongitudeOfPerigee, 360)

    Es = (360/astro_constants.pi) * astro_constants.sun_eccentricity * math.sin(math.radians(Ms))

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

    # print(Dm)

    F = 0.5 * ( 1 - math.cos(math.radians(Dm)))
    # print(F)

    return (Lm, Bm, F)

def moonRiseSet(year, month, day, lat, long):
    # Section 66
    days = astro_utils.daysSinceEpoch(year, month, day)

    Lm1, Bm1, F = positionMoon(days)
    print(Lm1)
    print(Bm1)

    Rm1, Dm1 = astro_utils.coords_EclipticToEquatorial(Lm1, Bm1)

    print(Rm1)
    print(Dm1)

    Lm2, Bm2, F = positionMoon(days + 0.5)
    print(Lm2)
    print(Bm2)

    Rm2, Dm2 = astro_utils.coords_EclipticToEquatorial(Lm2, Bm2)

    print(Rm2)
    print(Dm2)

    # Part complete...

def main():
    print('')
    print('Moon position')
    print('')

    days = astro_utils.daysSinceEpoch(1979, 2, 26)
    days = -307.332755
    Lm, Bm, F = positionMoon(days)

    Rm, Dm = astro_utils.coords_EclipticToEquatorial(Lm, Bm)

    print('RA:  {}'.format(astro_utils.displayTime(Rm)))
    print('Dec: {}'.format(astro_utils.displayAngle(Dm)))
    print('Moon phase: {:01.1f}'.format(F))

    print('--------')
    moonRiseSet(1979, 9, 6, 52, 0)

if __name__ == "__main__":
    main()