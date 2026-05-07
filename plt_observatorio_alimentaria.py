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

patron = r"seguridad alimentaria|inocuidad alimentaria|bioinsumos|alimentos funcionales|seguridad nutricional|biofortificacion|Nutricion|nutrition|food safety"

observa = df_busqueda[
    df_busqueda["TITULO_LIMPIO"].str.contains(patron, case=False, na=False, regex=True)
].copy()


# Considerando el dataframe df_agroindustrial se obtiene los principales resultados
# Se calcula la cantidad de subvenciones durante el periodo de análisis
observa["ID_CONTRATO"].count()

# Se calcula la suma del total de subvenciones durante el periodo de análisis
observa["MONTO"].sum()


###############################################################################
# Se realiza una gráfico de barras considerando el dataframe observa_año que
# muestra la relación entre el número de subvenciones otorgadas y el monto financiado
###############################################################################

observa_año = (observa.groupby("AÑO", as_index=False).agg({"MONTO":"sum", "ID_CONTRATO":"count"}))

df_plot = observa_año.copy()

df_plot["AÑO"] = pd.to_numeric(df_plot["AÑO"], errors="coerce")
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")
df_plot["ID_CONTRADO"] = pd.to_numeric(df_plot["ID_CONTRATO"], errors="coerce")

df_plot = df_plot.dropna(subset=["AÑO", "MONTO", "ID_CONTRATO"]).copy()
df_plot["AÑO"] = df_plot["AÑO"].astype(int)

df_plot = df_plot.sort_values("AÑO")

# ----------------------------
# Colores institucionales
# ----------------------------
color_monto = "#5FB7C6"   # celeste institucional
color_prod = "#0B4F6C"    # azul petróleo

fig, ax1 = plt.subplots(figsize=(14, 7))

color_monto = "#5FB7C6"
color_prod = "#0B4F6C"

bars = ax1.bar(
    df_plot["AÑO"],
    df_plot["MONTO"],
    color=color_monto,
    alpha=0.85,
    width=0.6,
    edgecolor="white",
    linewidth=1
)

ax1.set_xlabel("Año", fontsize=11)
ax1.set_ylabel("Monto (Millones de S/)", fontsize=11, color=color_monto)
ax1.tick_params(axis="y", labelcolor=color_monto)

años = df_plot["AÑO"].astype(int).tolist()
ax1.set_xticks(años)
ax1.set_xticklabels(años)

ax2 = ax1.twinx()

ax2.plot(
    df_plot["AÑO"],
    df_plot["ID_CONTRATO"],
    color=color_prod,
    marker="o",
    linewidth=2.6,
    markersize=6,
    zorder=5
)

ax2.set_ylabel("Número de subvenciones", fontsize=11, color=color_prod)
ax2.tick_params(axis="y", labelcolor=color_prod)

# ----------------------------
# Etiquetas de barras: dentro si son altas, fuera si son bajas
# ----------------------------
max_monto = df_plot["MONTO"].max()

for bar in bars:
    height = bar.get_height()
    x = bar.get_x() + bar.get_width() / 2
    label = f"{height / 1e6:.1f}M"

    if height > max_monto * 0.18:
        y_text = height - max_monto * 0.045
        va = "top"
        color_label = "white"
    else:
        y_text = height + max_monto * 0.018
        va = "bottom"
        color_label = color_monto

    ax1.text(
        x,
        y_text,
        label,
        ha="center",
        va=va,
        fontsize=11,
        color=color_label,
        fontweight="bold"
    )

# ----------------------------
# Etiquetas de línea: caja sutil y alternancia
# ----------------------------
max_line = df_plot["ID_CONTRATO"].max()

bbox_line = dict(
    boxstyle="round,pad=0.18",
    facecolor="white",
    edgecolor="none",
    alpha=0.80
)

for x, y in zip(df_plot["AÑO"], df_plot["ID_CONTRATO"]):

    offset = max_line * 0.055

    ax2.text(
        x,
        y + offset,
        f"{int(y)}",
        ha="center",
        va="bottom",
        fontsize=12,
        color=color_prod,
        fontweight="bold",
        bbox=bbox_line,
        zorder=6
    )

# ----------------------------
# Estética
# ----------------------------
ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.grid(axis="y", linestyle="--", alpha=0.22)
ax1.set_axisbelow(True)

ax1.set_ylim(0, max_monto * 1.15)
ax2.set_ylim(0, max_line * 1.18)


# ----------------------------
# Leyenda profesional
# ----------------------------
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements = [

    Patch(
        facecolor=color_monto,
        edgecolor="white",
        label="Monto financiado"
    ),

    Line2D(
        [0],
        [0],
        color=color_prod,
        marker="o",
        linewidth=2.6,
        markersize=6,
        label="Número de subvenciones"
    )
]

ax1.legend(
    handles=legend_elements,
    loc="upper left",
    frameon=False,
    fontsize=10
)


plt.tight_layout()
plt.show()


###############################################################################
# Se realiza una gráfico de barras agrupadas considerando el dataframe obv_año_estado
###############################################################################

# se realiza una distribución de cantidad de subvenciones por año y por estado
obv_año_estado = pd.pivot_table(observa, values="ID_CONTRATO", index="AÑO", columns="ESTADO", aggfunc="count")
obv_año_estado.reset_index(inplace=True)


obv_año_estado["Activo"] = pd.to_numeric(obv_año_estado["Activo"], errors="coerce")
obv_año_estado["Concluido"] = pd.to_numeric(obv_año_estado["Concluido"], errors="coerce")

# Reemplazar nulos por 0 (decisión lógica en este caso)
obv_año_estado["Activo"] = obv_año_estado["Activo"].fillna(0)
obv_año_estado["Concluido"] = obv_año_estado["Concluido"].fillna(0)

obv_año_estado["AÑO"] = pd.to_numeric(obv_año_estado["AÑO"], errors="coerce").astype(int)

obv_año_estado = obv_año_estado.sort_values("AÑO")

# Posiciones
x = np.arange(len(obv_año_estado))
width = 0.35

# Colores institucionales
color_activo = "#A3AD2C"     
color_concluido = "#1F6F8B"  # azul petróleo

fig, ax = plt.subplots(figsize=(12, 6))

# Barras
bars1 = ax.bar(x - width/2, obv_año_estado["Activo"], width, label="Activo", color=color_activo)
bars2 = ax.bar(x + width/2, obv_año_estado["Concluido"], width, label="Concluido", color=color_concluido)

# Ejes
ax.set_xlabel("Año", fontsize=11)
ax.set_ylabel("Número de subvenciones", fontsize=11)
#ax.set_title("Contratos por estado y año", fontsize=14, pad=15)

# Eje X con todos los años
ax.set_xticks(x)
ax.set_xticklabels(obv_año_estado["AÑO"].astype(int))

# Estética consultoría
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# Leyenda limpia
ax.legend(frameon=False)

# Etiquetas encima de barras
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height + max(obv_año_estado[["Activo","Concluido"]].max()) * 0.01,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=8
            )

# Margen superior
ax.set_ylim(0, obv_año_estado[["Activo","Concluido"]].max().max() * 1.15)

plt.tight_layout()
plt.show()


###############################################################################
#Se realiza un bubble chart para mostrar la distribución de las subvenciones
# en función del convenio
###############################################################################
observa_convenio = observa.groupby("CONVENIO")["ID_CONTRATO"].count()
observa_convenio = observa_convenio.to_frame()
observa_convenio.reset_index(inplace=True)
observa_convenio.columns

# Se renombra algunas columnas del dataframe observa_convenio
observa_convenio.rename(columns=({"ID_CONTRATO":"CANTIDAD"}), inplace=True)

# ----------------------------
# Datos
# ----------------------------
observa_convenio = observa_convenio.sort_values(
    "CANTIDAD", ascending=False).reset_index(drop=True)

# Etiquetas abreviadas para evitar saturación
observa_convenio["LABEL"] = observa_convenio["CONVENIO"].replace({
    "Embajada EEUU": "Emb. EEUU",
    "Fondo Newton - RAENG": "Newton-RAENG",
    "Fondo Newton - British Council": "Newton-BC"
})

# ----------------------------
# Escalamiento profesional
# ----------------------------
# Raíz cuadrada para suavizar diferencias extremas
sizes_scaled = np.sqrt(observa_convenio["CANTIDAD"]) * 180

# ----------------------------
# Posiciones manuales más limpias
# ----------------------------
x = [0.0, 2.8, 5.2, 7.5, 9.8, 12.0, 14.5, 16.8, 19.0, 21.2]
y = [0.0, 0.0, -0.15, -0.10, 0.05, -0.05, 0.00, -0.03, -0.08, -0.02]

# Si tienes menos o más filas, ajusta automáticamente
x = x[:len(observa_convenio)]
y = y[:len(observa_convenio)]

# ----------------------------
# Colores institucionales
# ----------------------------
color_principal = "#0B4F6C"   # azul petróleo oscuro
color_secundario = "#5FB7C6"  # celeste institucional
color_terciario = "#A3AD2C"   # verde olivo

colors = [color_secundario] * len(observa_convenio)
if len(observa_convenio) > 0:
    colors[0] = color_principal
if len(observa_convenio) > 1:
    colors[1] = color_terciario

# ----------------------------
# Figura
# ----------------------------
fig, ax = plt.subplots(figsize=(16, 6))

ax.scatter(
    x, y,
    s=sizes_scaled,
    c=colors,
    alpha=0.9,
    edgecolors="white",
    linewidths=2
)

# ----------------------------
# Etiquetas
# ----------------------------
for i, row in observa_convenio.iterrows():
    # Etiqueta interna solo para burbujas grandes
    if row["CANTIDAD"] >= 200:
        ax.text(
            x[i], y[i],
            f"{row['LABEL']}\n{int(row['CANTIDAD']):,}".replace(",", "."),
            ha="center", va="center",
            fontsize=10,
            color="white", #if i == 0 else "#0B4F6C",
            fontweight="bold" #if i == 0 else "normal"
        )
    else:
        # Etiqueta externa para burbujas pequeñas
        ax.text(
            x[i], y[i] + 0.20,
            row["LABEL"],
            ha="center", va="bottom",
            fontsize=10,
            color="#0B4F6C"
        )
        ax.text(
            x[i], y[i] - 0.20,
            f"{int(row['CANTIDAD'])}",
            ha="center", va="top",
            fontsize=9,
            color="#0B4F6C",
            fontweight="bold"
        )

# ----------------------------
# Estética ejecutiva
# ----------------------------
#ax.set_title("Representatividad de subvenciones por convenio",
             #fontsize=20, color="#0B4F6C", pad=20)

ax.set_xlim(-1, max(x) + 1.5)
ax.set_ylim(-1.2, 1.2)

ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_facecolor("white")
fig.patch.set_facecolor("white")

plt.tight_layout()
plt.show()

###############################################################################
# Se realiza un gráfico de barras para observar la distribución de las subvenciones
# según intervención
###############################################################################
observa_inter = observa.INTERVENCIÓN.value_counts()
observa_inter = observa.INTERVENCIÓN.value_counts(normalize=True).round(2)*100
observa_inter = observa_inter.to_frame()
observa_inter.reset_index(inplace=True)
observa_inter.rename(columns=({"proportion":"porcentaje"}), inplace=True)


observa_inter = observa_inter.sort_values("porcentaje", ascending=True)

color_principal = "#0B4F6C"   # azul institucional
color_secundario = "#5FB7C6"  # celeste

colors = [color_secundario] * len(observa_inter)
colors[-1] = color_principal  # destacar el mayor

plt.figure(figsize=(12, 6))

bars = plt.barh(observa_inter["INTERVENCIÓN"], observa_inter["porcentaje"], color=colors)

# Etiquetas
for i, v in enumerate(observa_inter["porcentaje"]):
    plt.text(v + 0.5, i, f"{v:.0f}%", va="center", fontsize=10)

# Estética consultoría
plt.xlabel("Porcentaje (%)")
#plt.title("Distribución de subvenciones por tipo de intervención", fontsize=13)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.grid(axis="x", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()


###############################################################################
# Se realiza un gráfico de barras apiladas para ver la concentración del
# financiamiento por intervención
###############################################################################

barra_apilada = pd.pivot_table(observa, values="MONTO", index="INTERVENCIÓN", columns="AÑO", aggfunc="sum")

# Reemplazar NaN por 0
barra_apilada = barra_apilada.fillna(0)

# Pasar a millones
barra_apilada_m = barra_apilada / 1e6

# Transponer: años en filas, categorías en columnas
barra_apilada = barra_apilada_m.T

# ----------------------------
# 2. Gráfico de columnas apiladas
# ----------------------------
fig, ax = plt.subplots(figsize=(14, 7))

barra_apilada.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    width=0.75,
    colormap="tab10",
    edgecolor="white",
    linewidth=0.9
)

# ----------------------------
# 3. Estética profesional
# ----------------------------
ax.set_xlabel("Año", fontsize=11)
ax.set_ylabel("Monto (millones de S/)", fontsize=11)

#ax.set_title(
    #"Evolución del monto adjudicado por tipo de intervención",
    #fontsize=15,
    #color="#0B4F6C",
    #pad=15
#)

ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(
    title="Intervención",
    frameon=False,
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


###############################################################################
# Se realiza un gráfico para identificar quienes investigan en anemia en el Perú
# por investigador y por universidad
################################################################################

anemia_investigador = observa.LIDER_PROYECTO.value_counts()
anemia_investigador = anemia_investigador.to_frame()
anemia_investigador.reset_index(inplace=True)
anemia_investigador.rename(columns=({"count":"Cantidad"}), inplace=True)
anemia_investigador["Cantidad"] = anemia_investigador["Cantidad"].astype(int)
anemia_investigador = anemia_investigador.head(10)
anemia_investigador.dtypes

anemia_investigador = anemia_investigador.sort_values("Cantidad", ascending=True)

color_principal = "#0B4F6C"   # azul institucional
color_secundario = "#5FB7C6"  # celeste

colors = [color_secundario] * len(anemia_investigador)
colors[-1] = color_principal  # destacar el mayor

plt.figure(figsize=(12, 6))

bars = plt.barh(anemia_investigador["LIDER_PROYECTO"], anemia_investigador["Cantidad"], color=colors)

# Etiquetas
for i, v in enumerate(anemia_investigador["Cantidad"]):
    plt.text(v+0.05, i, f"{v:.0f}", va="center", fontsize=12)

# Estética consultoría
plt.xlabel("Cantidad")
#plt.title("Distribución de subvenciones por tipo de intervención", fontsize=13)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.grid(axis="x", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()

observa_uni = observa[observa["ORGANIZACIÓN"].str.contains("UNIVERSIDAD", case=False, na=False)]
observa_uni = observa_uni.ORGANIZACIÓN.value_counts(normalize=True).round(3)*100
observa_uni = observa_uni.to_frame()
observa_uni.reset_index(inplace=True)
observa_uni.rename(columns=({"proportion":"Porcentaje"}), inplace=True)
observa_uni = observa_uni.head(10)

observa_uni_a = observa_uni.sort_values("Porcentaje", ascending=True)

color_principal = "#0B4F6C"   # azul institucional
color_secundario = "#5FB7C6"  # celeste

colors = [color_secundario] * len(observa_uni_a)
colors[-1] = color_principal  # destacar el mayor

plt.figure(figsize=(12, 6))

bars = plt.barh(observa_uni_a["ORGANIZACIÓN"], observa_uni_a["Porcentaje"], color=colors)

# Etiquetas
for i, v in enumerate(observa_uni_a["Porcentaje"]):
    plt.text(v + 0.5, i, f"{v:.0f}%", va="center", fontsize=10)

# Estética consultoría
plt.xlabel("Porcentaje (%)")
#plt.title("Distribución de subvenciones por tipo de intervención", fontsize=13)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.grid(axis="x", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()

###############################################################################
# Se elabora un gráfico que analiza la relación entre la producción científica
# y el presupuesto, a nivel temporal
###############################################################################

# Se crea la variable producción científica, que agrupa a las publicaciones, tesis y patentes
observa["PRODUCCION"] = observa["PUB"] + observa["TESIS"] + observa["PAT"]

# se consideran los proyectos que se encuentran en condición de concluido
observa_conclu = observa[observa["ESTADO"]=="Concluido"]

observa_pre = (observa_conclu.groupby("AÑO", as_index=False).agg({"MONTO":"sum", "PRODUCCION":"sum"}))
df_plot = observa_pre.copy()

df_plot["AÑO"] = pd.to_numeric(df_plot["AÑO"], errors="coerce")
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")

# Convertir a millones
df_plot["MONTO_M"] = df_plot["MONTO"] / 1e6

df_plot = df_plot.sort_values("AÑO")

# =========================================================
# FIGURA
# =========================================================
fig, ax = plt.subplots(figsize=(14, 7))

color_bar = "#0B4F6C"

bars = ax.bar(
    df_plot["AÑO"],
    df_plot["MONTO_M"],
    color=color_bar,
    width=0.65,
    alpha=0.85,
    edgecolor="white",
    linewidth=1
)

# =========================================================
# ETIQUETAS INTELIGENTES
# =========================================================
max_monto = df_plot["MONTO_M"].max()

for bar, valor_real in zip(bars, df_plot["MONTO"]):

    height = bar.get_height()

    # ----------------------------
    # Si es menor a 1 millón
    # mostrar en miles
    # ----------------------------
    if valor_real < 1_000_000:

        label = f"{valor_real/1e3:.0f} mil"

    else:

        label = f"{height:.1f}M"

    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + max_monto * 0.02,
        label,
        ha="center",
        va="bottom",
        fontsize=11,
        color=color_bar,
        fontweight="bold"
    )

# =========================================================
# MOSTRAR TODOS LOS AÑOS
# =========================================================
años = df_plot["AÑO"].astype(int).tolist()

ax.set_xticks(años)
ax.set_xticklabels(años)

# =========================================================
# ESTÉTICA
# =========================================================
ax.set_xlabel("Año", fontsize=11)

ax.set_ylabel(
    "Monto (S/)",
    fontsize=11,
    color=color_bar
)

ax.tick_params(axis="y", labelcolor=color_bar)

ax.grid(axis="y", linestyle="--", alpha=0.25)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_axisbelow(True)

ax.set_title(
    "Evolución anual del financiamiento",
     fontsize=15,
     color="black",
     pad=15
)

plt.tight_layout()
plt.show()

# =========================================================
# FIGURA
# =========================================================
fig, ax = plt.subplots(figsize=(14, 7))

color_line = "#0B4F6C"

ax.plot(
    df_plot["AÑO"],
    df_plot["PRODUCCION"],
    color=color_line,
    marker="o",
    linewidth=2.5,
    markersize=6
)


# =========================================================
# ETIQUETAS (todas arriba)
# =========================================================
max_prod = df_plot["PRODUCCION"].max()

for x, y in zip(df_plot["AÑO"], df_plot["PRODUCCION"]):

    ax.text(
        x,
        y + max_prod * 0.03, # todas arriba
        f"{int(y)}",
        ha="center",
        va="bottom",
        fontsize=11,
        color=color_line,
        fontweight="bold"
    )

# =========================================================
# MOSTRAR TODOS LOS AÑOS
# =========================================================
años = df_plot["AÑO"].astype(int).tolist()

ax.set_xticks(años)
ax.set_xticklabels(años)

# =========================================================
# ESTÉTICA
# =========================================================
ax.set_xlabel("Año", fontsize=11)

ax.set_ylabel(
    "Producción científica",
    fontsize=11,
    color=color_line
)

ax.grid(axis="y", linestyle="--", alpha=0.25)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_axisbelow(True)

ax.set_title(
    "Evolución anual de la producción científica",
    fontsize=15,
     color="black",
     pad=15
)

plt.tight_layout()
plt.show()

###############################################################################
# Se gráfica la evolución de la producción científica vinculada a la anemia en
# el Perú
###############################################################################
observa_ptp = (observa_conclu.groupby("AÑO", as_index=False).agg({"PUB":"sum", "TESIS":"sum", "PAT":"sum"}))


df_plot = observa_ptp.copy()
df_plot = df_plot.sort_values("AÑO")

# ----------------------------
# Figura
# ----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# ----------------------------
# Colores institucionales
# ----------------------------
colors = {
    "PUB": "#0B4F6C",    # azul petróleo
    "TESIS": "#5FB7C6",  # celeste
    "PAT": "#A3AD2C"     # verde oliva
}

markers = {
    "PUB": "o",
    "TESIS": "s",
    "PAT": "^"
}

cols = ["PUB", "TESIS", "PAT"]

# ----------------------------
# Líneas
# ----------------------------
for col in cols:
    ax.plot(
        df_plot["AÑO"],
        df_plot[col],
        marker=markers[col],
        linewidth=2.8 if col != "PAT" else 2,
        markersize=6,
        color=colors[col],
        label=col,
        alpha=1 if col != "PAT" else 0.75
    )

# ----------------------------
# Escala para offsets
# ----------------------------
max_y = df_plot[cols].max().max()

offsets = {
    "PUB": max_y * 0.04,
    "TESIS": max_y * 0.07,
    "PAT": -max_y * 0.04
}

# ----------------------------
# Etiquetas (limpias)
# ----------------------------
for col in cols:
    for x, y in zip(df_plot["AÑO"], df_plot[col]):

        if pd.isna(y) or y == 0:
            continue

        # Reducir ruido en PAT
        if col == "PAT" and y < 2:
            continue

        ax.text(
            x,
            y + offsets[col],
            f"{int(y)}",
            ha="center",
            va="bottom" if offsets[col] > 0 else "top",
            fontsize=9,
            color=colors[col],
            fontweight="bold" if col == "PUB" else "normal"
        )

# ----------------------------
# Ejes
# ----------------------------
años = df_plot["AÑO"].astype(int).tolist()
ax.set_xticks(años)
ax.set_xticklabels(años)

ax.set_xlabel("Año", fontsize=11)
ax.set_ylabel("Número de productos científicos", fontsize=11)

# ----------------------------
# Leyenda (CORRECTA)
# ----------------------------
ax.legend(
    frameon=False,
    loc="upper right",
    ncol=3
)

# ----------------------------
# Estética profesional
# ----------------------------
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Límites
ax.set_xlim(df_plot["AÑO"].min() - 0.4, df_plot["AÑO"].max() + 0.4)
ax.set_ylim(0, max_y * 1.15)

# Fondo blanco
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# ----------------------------
# Título opcional
# ----------------------------
# ax.set_title(
#     "Evolución de la producción científica por tipo",
#     fontsize=14,
#     color="#0B4F6C",
#     pad=15
# )

plt.tight_layout()
plt.show()


###############################################################################
# Se elabora una gráfica de correlación para visualizar la relación entre presupuesto y producción científica de universidades
# Se consideran las subvenciones en condición de concluido
###############################################################################
observa_uni_pre = observa_conclu[observa_conclu["ORGANIZACIÓN"].str.contains("UNIVERSIDAD", case=False, na=False)]
observa_uni_pre = (observa_uni_pre.groupby("ORGANIZACIÓN", as_index=False).agg({"MONTO":"sum", "PRODUCCION":"sum"}))

df_plot = observa_uni_pre.copy()

# Conversión de tipos
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")
df_plot["PRODUCCION"] = pd.to_numeric(df_plot["PRODUCCION"], errors="coerce")

# Limpieza
df_plot = df_plot.dropna(subset=["MONTO", "PRODUCCION"]).copy()

# Escala en millones
df_plot["MONTO_M"] = df_plot["MONTO"] / 1e6

# =========================================================
# 3. ABREVIACIÓN DE INSTITUCIONES
# =========================================================
map_dict = {
    "PONTIFICIA UNIVERSIDAD CATOLICA DEL PERU": "PUCP",
    "UNIVERSIDAD ANDINA DEL CUSCO": "UAC",
    "UNIVERSIDAD CATOLICA DE SANTA MARIA": "UCSM",
    "UNIVERSIDAD CATOLICA SAN PABLO": "UCSP",
    "UNIVERSIDAD ANTONIO RUIZ DE MONTOYA": "UARM",
    "UNIVERSIDAD CATOLICA LOS ANGELES DE CHIMBOTE": "ULADECH",
    "ASOCIACION CIVIL UNIVERSIDAD DE CIENCIAS Y HUMANIDADES UCH": "UCH",
    "UNIVERSIDAD PERUANA CAYETANO HEREDIA": "UPCH",
    "UNIVERSIDAD NACIONAL DE INGENIERIA UNI":"UNI",
    "UNIVERSIDAD NACIONAL AGRARIA LA MOLINA":"UNALM",
    "UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS":"UNMSM",
    "UNIVERSIDAD NACIONAL TORIBIO RODRIGUEZ DE MENDOZA DE AMAZONAS":"UNTRM",
    "UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA":"UTEC",
    "UNIVERSIDAD NACIONAL DE SAN AGUSTIN":"UNSA",
    "UNIVERSIDAD DE PIURA":"UDEP",
    "UNIVERSIDAD NACIONAL DE TRUJILLO":"UNT",
    "UNIVERSIDAD DE SAN MARTIN DE PORRES":"USMP",
    "UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS S.A.C.":"UPC",
    "UNIVERSIDAD CIENTIFICA DEL SUR S.A.C.":"UCSUR",
    "UNIVERSIDAD SEÑOR DE SIPAN S.A.C.":"USS",
    "UNIVERSIDAD NACIONAL MICAELA BASTIDAS DE APURIMAC":"MB Apurimac",
    "UNIVERSIDAD NACIONAL DEL CALLAO":"UNAC",
    "UNIVERSIDAD NACIONAL DE SAN AGUSTIN":"UNSA",
    "UNIVERSIDAD NACIONAL AGRARIA DE LA SELVA":"UNAS",
    "UNIVERSIDAD NACIONAL AGRARIA LA MOLINA": "UNALM",
    "UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS": "UNMSM",
    "UNIVERSIDAD NACIONAL TORIBIO RODRIGUEZ DE MENDOZA DE AMAZONAS": "UNTRM",
    "UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA": "UTEC",
    "UNIVERSIDAD NACIONAL DE SAN AGUSTIN": "UNSA",
    "UNIVERSIDAD DE PIURA": "UDEP",
    "UNIVERSIDAD NACIONAL DE TRUJILLO": "UNT",
    "UNIVERSIDAD DE SAN MARTIN DE PORRES": "USMP",
    "UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS S.A.C.": "UPC",
    "UNIVERSIDAD CIENTIFICA DEL SUR S.A.C.": "UCSUR",
    "UNIVERSIDAD SEÑOR DE SIPAN S.A.C.": "USS",
    "UNIVERSIDAD NACIONAL MICAELA BASTIDAS DE APURIMAC": "MB Apurimac",
    "UNIVERSIDAD NACIONAL DEL CALLAO": "UNAC",
    "UNIVERSIDAD NACIONAL AGRARIA DE LA SELVA": "UNAS",
    "UNIVERSIDAD NACIONAL DEL SANTA": "UNS",
    "ASOCIACION CIVIL UNIVERSIDAD DE CIENCIAS Y HUMANIDADES UCH": "UCH",
    "UNIVERSIDAD DE LIMA": "ULIMA",
    "UNIVERSIDAD DE SAN MARTIN DE PORRES": "USMP",
    "UNIVERSIDAD NACIONAL AGRARIA LA MOLINA": "UNALM",
    "UNIVERSIDAD NACIONAL DE SAN CRISTOBAL DE HUAMANGA": "UNSCH",
    "UNIVERSIDAD CATOLICA SEDES SAPIENTIAE": "UCSS",
    "UNIVERSIDAD CIENTIFICA DEL PERU": "UCP",
    "UNIVERSIDAD NACIONAL DE LA AMAZONIA PERUANA": "UNAP",
    "UNIVERSIDAD PRIVADA DEL NORTE SAC": "UPN",
    "UNIVERSIDAD CESAR VALLEJO S.A.C.":"UCV",
    "UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO":"UNA-PUNO"
    
}

df_plot["ORG_SHORT"] = df_plot["ORGANIZACIÓN"].map(map_dict)

# Si alguna no está en el diccionario, usar nombre original corto
df_plot["ORG_SHORT"] = df_plot["ORG_SHORT"].fillna(
    df_plot["ORGANIZACIÓN"].str[:15]
)

# =========================================================
# 4. CÁLCULO DE TENDENCIA
# =========================================================
x = df_plot["MONTO_M"]
y = df_plot["PRODUCCION"]

coef = np.polyfit(x, y, 1)
trend = np.poly1d(coef)

# =========================================================
# 5. GRÁFICO
# =========================================================
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter
ax.scatter(
    x,
    y,
    color="#5FB7C6",
    s=90,
    edgecolors="white",
    linewidth=1.5
)

# Línea de tendencia
ax.plot(
    x,
    trend(x),
    color="#0B4F6C",
    linewidth=2.2)

# =========================================================
# 6. ETIQUETAS INTELIGENTES
# =========================================================
for _, row in df_plot.iterrows():
    
    # Mostrar solo instituciones relevantes (evita saturación)
    if row["PRODUCCION"] >= 8 or row["MONTO_M"]>=0.5:
        
        ax.text(
            row["MONTO_M"],
            row["PRODUCCION"],
            row["ORG_SHORT"],
            fontsize=9,
            ha="left",
            va="center",
            color="#0B4F6C",
            fontweight="bold"
        )

# =========================================================
# 7. ESTÉTICA
# =========================================================
#ax.set_title(
   # "Relación entre financiamiento y producción científica por institución",
    #fontsize=14,
    #color="#0B4F6C",
    #pad=15
#)

ax.set_xlabel("Monto (millones de S/)")
ax.set_ylabel("Producción científica")

ax.grid(alpha=0.25)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()


###############################################################################
# Se analiza que se ha investigado sobre anemia en el Perú
###############################################################################

# Se obtiene un suset denominado investigación a partir del dataframe observa
observa.columns
investigacion = observa[observa["INTERVENCIÓN"] =="INVESTIGACIÓN CIENTÍFICA"]
investigacion.columns

# se consideran un conjunto de columnas
investigacion = investigacion[["ID_CONTRATO", "TÍTULO", "ORGANIZACIÓN", "AÑO"]]
investigacion.to_excel("listado_inv_alimenta.xlsx")


###############################################################################
# Se analiza los desarrollos tecnológicos que se han elaborado
###############################################################################
tecnologia = observa[observa["INTERVENCIÓN"]=="INNOVACIÓN Y TRANSFERENCIA TECNOLÓGICA"]
tecnologia = tecnologia[["ID_CONTRATO", "TÍTULO", "ORGANIZACIÓN", "AÑO"]]
tecnologia.to_excel("listado_tec_alimenta.xlsx")







