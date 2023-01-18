import math
import datetime
# import astro_constants
import astro_utils
import astro_moon

def test_alignNumber():
    assert(astro_utils.alignNumber(180, 360) == 180)
    assert(astro_utils.alignNumber((180+360), 360) == 180)
    assert(astro_utils.alignNumber(-90, 360) == 270)
    assert(astro_utils.alignNumber((-90-360), 360) == 270)

    assert(astro_utils.alignNumber(12, 24) == 12)
    assert(astro_utils.alignNumber(36, 24) == 12)

def test_coords_EclipticToEquatorial():
    A, D = astro_utils.coords_EclipticToEquatorial(124.108828, 0)
    assert(round(A, 10) ==  8.4289927665)
    assert(round(D, 10) == 19.2313605764)

    A, D = astro_utils.coords_EclipticToEquatorial(139.686111, 4.875278)
    assert(round(A, 6) ==  9.581551)
    assert(round(D, 6) == 19.537269)

def test_displayTime():
    assert(astro_utils.displayTime(9.581551) == '09h 34m 53.6s')

def test_displayAngle():
    deg = u'\xb0'  # utf code for degree
    assert(astro_utils.displayAngle(19.537269) == '19' + deg.encode('utf8') + ' 32\' 14.2\"')

def test_convertRaDecToLST():
    Lr, Ls = astro_utils.convertRaDecToLST(11.003687, 6.380389, 52.0)
    assert(round(Lr,6) ==  4.455106)
    assert(round(Ls,6) == 17.552268)

def test_convertLSTtoGST():
    assert(round(astro_utils.convertLSTtoGST(0.401436, 64), 6) == 4.668103)

def test_convertGSTtoGMT():
    assert(round(astro_utils.convertGSTtoGMT(4.668103, 113, 1980), 6) == 14.614361)

def test_geocentricParallax():
    rho_sin_phi, rho_cos_phi = astro_utils.geocentricParallax(50.0, 60.0)

    assert(round(rho_sin_phi, 6) == 0.762422)
    assert(round(rho_cos_phi, 6) == 0.644060)

def test_distanceMoon():
    Pc = astro_moon.distanceMoon(-359.735278, 0.029055)

    assert(round(Pc, 6) == 0.945101)