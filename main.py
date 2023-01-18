import logging
import math
import datetime
import astro_constants
import astro_utils
import astro_sun

# Initialise logging module
logging.root.handlers = []
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    # datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
    # level=logging.DEBUG
    )

def main():
    print('')
    print('Sunrise/Sunset')
    print('')

    year = 1979
    month = 9
    day = 7

    lat = 51.860435
    long = -1.596303

    astro_sun.sunRiseSet(year, month, day, lat, long)


if __name__ == "__main__":
    main()
