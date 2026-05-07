# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:38:12 2026

@author: Enzo
"""

###############################################################################
## PROYECTO PARA ELABORAR UN SCRIPT QUE AUTOMATICE EL ANÁLISIS DE TÓPICOS
## CONSIDERANDO EL OBSERVATORIO DE SUBVENCIONES DEL PROCIENCIA
###############################################################################

###############################################################################
# El proyecto sigue un enfoque de librerias integradas
###############################################################################

# Se importan las librerias que serán usadas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import re
import unicodedata

###############################################################################
# Se describen los colores que integran la paleta institucional para mis gráficos
###############################################################################

#1. Celeste claro
#HEX: #5FB7C6
#Nombre descriptivo: Celeste muy claro
#Uso: fondos, áreas suaves, mapas base

#2. Verde olivo
#HEX: #A3AD2C
#Nombre descriptivo: Verde olivo institucional
#Uso: color principal de datos (barras, líneas)

#3. Azul petróleo
#HEX: #0B4F6C
#Nombre descriptivo: Azul petróleo
#Uso: énfasis, títulos, bordes

###############################################################################
###############################################################################

# Se carga el archivo xlsx y se convierte en un objeto dataframe
observa = pd.read_excel("Subvenciones_20260505.xlsx", sheet_name="Resultados", header=0)

# Se analiza la estructura del dataframe observa
observa.shape
observa.columns
observa.info()
observa.dtypes
observa.head(10)

# Se renombran variables del dataframe observa
observa.rename(columns=({"N° CONTRATO":"ID_CONTRATO",
                         "LÍDER DEL PROYECTO":"LIDER_PROYECTO",
                         "MONTO (S/)":"MONTO",
                         "PUB.":"PUB",
                         "PAT.":"PAT"}), inplace=True)



# Se identifica la presencia de duplicados en el dataframe observa
duplicado = observa.duplicated(subset=["ID_CONTRATO"])
print("¿Existe la presencia de duplicados?:", duplicado.any())


# Se identifica la presencia de nulos en el dataframe observa
nulo = observa["ID_CONTRATO"].isna().sum()
print(f"la columna ID_CONTRATO contiene {nulo} valores nulos")

# se realiza una distribución de cantidad de subvenciones por año
observa_año = observa.groupby("AÑO")["ID_CONTRATO"].count()
observa_año = observa_año.to_frame()
observa_año.reset_index(inplace=True)

# Se analiza los tipos de datos de las columnas que conforman el dataframe observa_año
observa_año.info()

# Se cambian los atributos a tipo númerico
observa_año["AÑO"] = pd.to_numeric(observa_año["AÑO"], errors="coerce")
observa_año["ID_CONTRATO"] = pd.to_numeric(observa_año["ID_CONTRATO"], errors="coerce")

# Se calcula la cantidad de subvenciones durante el periodo de análisis
observa["ID_CONTRATO"].count()

# Se calcula la suma del total de subvenciones durante el periodo de análisis
observa["MONTO"].sum()


###############################################################################
# Se implementa un algoritmo de búsqueda para construir un suset del dataframe
# observa
###############################################################################

df_busqueda = observa.copy()

def normalizar_texto(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

df_busqueda["TITULO_LIMPIO"] = df_busqueda["TÍTULO"].apply(normalizar_texto)

patron = r"seguridad alimentaria|inocuidad alimentaria|bioinsumos|alimentos funcionales|seguridad nutricional/biofortificacion"

observa = df_busqueda[
    df_busqueda["TITULO_LIMPIO"].str.contains(patron, case=False, na=False, regex=True)
].copy()


# Considerando el dataframe df_agroindustrial se obtiene los principales resultados
# Se calcula la cantidad de subvenciones durante el periodo de análisis
observa["ID_CONTRATO"].count()

# Se calcula la suma del total de subvenciones durante el periodo de análisis
observa["MONTO"].sum()






