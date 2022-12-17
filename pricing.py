from geopy.geocoders import Nominatim
from uszipcode import SearchEngine
from arcgis.gis import GIS
import pandas as pd

gis = GIS("http://www.arcgis.com", "vishal2725", "Vishal%2705")


def get_price(yc, xc):
    mu = 4.251  # Average gas price/gallon in illinois (taken from https://gasprices.aaa.com/state-gas-price-averages/)
    sigma = 2.5  # Roughly estimated figure
    avg_pd = 230  # Illinois average population density per sq mile
    std_dev_pd = 6128.4 # calculated using real data for IL

    geolocator = Nominatim(user_agent='myGeocoder')
    location = geolocator.reverse(str(yc) + ', ' + str(xc))
    code = None
    try:
        code = location.raw['address']['postcode']
    except KeyError:
        return mu
    engine = SearchEngine()

    info = engine.by_zipcode(code)
    try:
        den = info.population_density
    except AttributeError:
        return mu
    if den is not None:
        ci = (den - avg_pd) / std_dev_pd
        price = mu + (ci * sigma)
        price = max(2, price)   # Gas cannot be cheaper than $2 per gallon!
        # print("price= " + str(round(price, 3)))  ##displaying price --> to be removed
        # den=0; price=0
        return round(price, 3)
    else:
        return mu
