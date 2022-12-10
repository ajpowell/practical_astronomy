import math
import astro_constants
import astro_utils

def alignNumber(n, lim):
    # where n > 360...
    while n > lim:
        n = n - lim
    # where n < 0...
    while n < 0:
        n = n + lim
    return n

def fixAtanAmbiguity(A, x, y):
    if x > 0 and y > 0:
        Amin = 0
        Amax = 90
    if x < 0 and y > 0:
        Amin = 90
        Amax = 180
    if x < 0 and y < 0:
        Amin = 180
        Amax = 270
    if x > 0 and y < 0:
        Amin = 270
        Amax = 360
    
    while A > Amax:
        A = A - 180
    while A < Amin:
        A = A + 180

    return A

def coords_EclipticToEquatorial(L, B):
    D = math.degrees(math.asin(math.sin(math.radians(B)) * math.cos(math.radians(astro_constants.obliquityOfEcliptic)) + \
          math.cos(math.radians(B)) * math.sin(math.radians(astro_constants.obliquityOfEcliptic)) * math.sin(math.radians(L))))
    
    # print(D)

    y = math.sin(math.radians(L)) * math.cos(math.radians(astro_constants.obliquityOfEcliptic)) - \
        math.tan(math.radians(B)) * math.sin(math.radians(astro_constants.obliquityOfEcliptic))
    x = math.cos(math.radians(L))
    # print(y)
    # print(x)

    A = math.degrees(math.atan(y/x))
    # print(A)

    A = fixAtanAmbiguity(A, x, y)

    # print(A)

    Ah = A/15

    # print('------')
    # print(displayTime(Ah))
    # print(displayAngle(D))

    return (Ah, D)

def displayTime(T):
    H = math.trunc(T) 
    M = math.trunc((T - H ) * 60)
    S = (((T - H ) * 60) - M) * 60

    return '{:02d}h {:02d}m {:04.1f}s'.format(H, M, S)

def displayAngle(T):
    H = math.trunc(T) 
    M = math.trunc((T - H ) * 60)
    S = (((T - H ) * 60) - M) * 60

    deg = u'\xb0'  # utf code for degree
    return '{}{} {}\' {:.1f}\"'.format(H, deg.encode('utf8'), M, S)

def convertRaDecToLST(A, D, lat):
    cosAr = math.sin(math.radians(D))/math.cos(math.radians(lat))

    if cosAr > 1 or cosAr < -1:
        print('Star/Object never rises above horizon.')
        return None, None

    # print(cosAr)

    Ar = math.degrees(math.acos(cosAr))
    As = abs(Ar - 360)

    # print(Ar)
    # print(displayAngle(Ar))
    # print(As)
    # print(displayAngle(As))

    H = (1.0/15.0) * math.degrees(math.acos(-1.0 * (math.tan(math.radians(lat))) * (math.tan(math.radians(D)))))

    # print(H)

    LSTr = alignNumber(24 + A - H, 24)
    LSTs = alignNumber(A + H, 24)

    # print(LSTr)
    # print(LSTs)

    return (LSTr, LSTs)

def convertLSTtoGST(LST, long):
    h = long/15.0
    GST = LST + h
    return GST

def convertGSTtoGMT(GST, daysSinceEpoch, year):
    A = 0.0657098
    B = 17.411472
    C = 1.002738
    D = 0.997270

    T0 = alignNumber((daysSinceEpoch * A) - B, 24)
    # print(T0)

    GMT = alignNumber(GST - T0, 24) * D

    return GMT

def parallaxCorrection(angularDiameter, horizontalParallax, atmosphericRefraction, lat, D):

    x = (angularDiameter / 2) + horizontalParallax + atmosphericRefraction

    # print(x)

    U = math.degrees( math.acos( math.sin(math.radians(lat)) / math.cos(math.radians(D)) ) )

    # print(U)

    # print('--')
    # print(math.sin(math.radians(x))/math.sin(math.radians(U)))
    # print('--')
    y = math.degrees(math.asin( math.sin(math.radians(x)) / math.sin(math.radians(U))))

    # print(y)

    Td = (240 * y)/(math.cos(math.radians(D)) * 3600)

    # print(Td)

    return Td