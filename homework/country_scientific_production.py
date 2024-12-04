"""Taller Presencial Evaluable"""

import os

import folium  # type: ignore
import pandas as pd  # type: ignore


def load_affiliations():
    """Carga el archivo scopus-papers.csv y retorna un dataframe con la
    columna 'Affiliations'"""

    dataframe = pd.read_csv(
        (
            "https://raw.githubusercontent.com/jdvelasq/datalabs/"
            "master/datasets/scopus-papers.csv"
        ),
        sep=",",
        index_col=None,
    )[["Affiliations"]]
    return dataframe


def remove_na_rows(affiliations):
    """Elimina las filas con valores nulos en la columna 'Affiliations'"""

    affiliations = affiliations.copy()
    affiliations = affiliations.dropna(subset=["Affiliations"])

    return affiliations


def add_countries_column(affiliations):
    """Transforma la columna 'Affiliations' a una lista de paises."""

    affiliations = affiliations.copy()
    affiliations["countries"] = affiliations["Affiliations"].copy()
    affiliations["countries"] = affiliations["countries"].str.split(";")
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y.split(",") for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y[-1].strip() for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(set)
    affiliations["countries"] = affiliations["countries"].str.join(", ")

    return affiliations

def clean_countries(affiliations):

    affiliations = affiliations.copy()
    affiliations["countries"] = affiliations["countries"].str.replace(
        "United States", "United States of America"
    )
    return affiliations


def count_country_frequency(affiliations):
    """Cuenta la frecuencia de cada país en la columna 'countries'"""

    countries = affiliations["countries"].copy()
    countries = countries.str.split(", ")
    countries = countries.explode()
    countries = countries.value_counts()
    print(countries)
    return countries



def make_worldmap():
    """Función principal"""

    if not os.path.exists("files"):
        os.makedirs("files")

    affiliations = load_affiliations()
    affiliations = remove_na_rows(affiliations)
    affiliations = add_countries_column(affiliations)
    affiliations = clean_countries(affiliations)
    countries = count_country_frequency(affiliations)

    # print(affiliations)

if __name__ == "__main__":
    make_worldmap()
    
    
    

    
    
    
    
    
    
    