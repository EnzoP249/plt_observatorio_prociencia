# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:59:05 2026

@author: Enzo
"""

###############################################################################
## PROYECTO PARA ANÁLISIS DE DATOS E INFORMACIÓN DEL OBSERVATORIO DE
## SUBVENCIONES DEL PROCIENCIA
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
observa = pd.read_excel("Subvenciones_20260404_prociencia.xlsx", sheet_name="Resultados", header=0)

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



# Se reformulan los tipos de datos de las columnas que integran el dataframe observa
schema = {"ID_CONTRATO":"string",
          "TÍTULO":"string",
          "LIDER_PROYECTO":"string",
          "ORGANIZACIÓN":"string",
          "AÑO":"Int64",
          "INTERVENCIÓN":"string",
          "CONVENIO":"string",
          "MONTO":"int64",
          "ESTADO":"string",
          "PUB":"int64",
          "TESIS":"int64",
          "PAT":"int64"}


observa = observa.astype(schema)

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

###############################################################################
# Se realiza una gráfico de barras considerando el dataframe observa_año
###############################################################################

observa_año = observa_año.sort_values("AÑO")

# Colores institucionales
color_principal = "#00A7B5"   # turquesa
color_secundario = "#1F6F8B"  # azul petróleo

# Tamaño más amplio (clave para separar barras)
plt.figure(figsize=(12,6))

# Crear barras con menor ancho (más espacio)
bars = plt.bar(observa_año["AÑO"], observa_año["ID_CONTRATO"], 
               color=color_principal, 
               width=0.6)

# Etiquetas
plt.xlabel("Año", fontsize=11, color="black")
plt.ylabel("Número de contratos", fontsize=11, color="black")

# Título más sobrio (tipo consultoría)
#plt.title("Evolución de contratos por año", 
          #fontsize=13, 
          #color=color_secundario, 
          #pad=15)

# Quitar bordes innecesarios
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Suavizar ejes
ax.spines["left"].set_color("#CCCCCC")
ax.spines["bottom"].set_color("#CCCCCC")

# Grid ligero (muy consultoría)
plt.grid(axis='y', linestyle='--', alpha=0.3)

años = observa_año["AÑO"].dropna().astype(int).tolist()
ax.set_xticks(años)
ax.set_xticklabels([str(a) for a in años], rotation=0)

# Etiquetas
for x, y in zip(observa_año["AÑO"], observa_año["ID_CONTRATO"]):
    #if pd.notna(x) and pd.notna(y) and y > 100:
        plt.text(
            float(x),
            float(y)+5,
            f"{int(y)}",
            ha="center",
            va="bottom",
            fontsize=9,
            color=color_secundario
        )

# Margen superior para que no choque texto
plt.ylim(0, observa_año["ID_CONTRATO"].max() * 1.15)

plt.tight_layout()
plt.show()

# se realiza una distribución de cantidad de subvenciones por año y por estado
obv_año_estado = pd.pivot_table(observa, values="ID_CONTRATO", index="AÑO", columns="ESTADO", aggfunc="count")
obv_año_estado.reset_index(inplace=True)

###############################################################################
# Se realiza una gráfico de barras agrupadas considerando el dataframe obv_año_estado
###############################################################################

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
ax.set_ylabel("Número de contratos", fontsize=11)
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
observa_convenio = observa_convenio[observa_convenio["CANTIDAD"]>=21]


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
# Se elabora un gráfico de líneas para observar la tendencia temporal de las
# subvenciones según intervención
###############################################################################

observa_inter_año = pd.pivot_table(observa, values="ID_CONTRATO", index="AÑO", columns="INTERVENCIÓN", aggfunc="count")
observa_inter_año.reset_index(inplace=True)

# Copia del dataframe
df_plot = observa_inter_año.copy()

df_plot = df_plot[df_plot["AÑO"]!=2026]

cols = [c for c in df_plot.columns if c != "AÑO"]

for c in cols:
    df_plot[c] = pd.to_numeric(df_plot[c], errors="coerce")

df_plot[cols] = df_plot[cols].fillna(0)
df_plot = df_plot.sort_values("AÑO")

# ----------------------------
# Paleta de colores (institucional + complementarios)
# ----------------------------
colors_list = [
    "#0B4F6C",  # azul petróleo
    "#5FB7C6",  # celeste
    "#A3AD2C",  # verde
    "#C4455C",  # rojo suave
    "#7A3E9D",  # morado
    "#00A7B5",  # turquesa
    "#F4A261"   # naranja (contraste)
]

# ----------------------------
# Marcadores distintos
# ----------------------------
markers = ["o", "s", "^", "D", "P", "X", "*"]

# ----------------------------
# Gráfico
# ----------------------------
plt.figure(figsize=(14, 7))
ax = plt.gca()

for i, c in enumerate(cols):
    ax.plot(
        df_plot["AÑO"],
        df_plot[c],
        color=colors_list[i % len(colors_list)],     # color único
        marker=markers[i % len(markers)],            # forma única
        linewidth=2.2,
        markersize=6,
        label=c
    )

# ----------------------------
# Estética profesional
# ----------------------------
#ax.set_title("Evolución anual de subvenciones por tipo de intervención",
             #fontsize=15, color="#0B4F6C", pad=15)

ax.set_xlabel("Año", fontsize=11)
ax.set_ylabel("Número de subvenciones", fontsize=11)

años = df_plot["AÑO"].astype(int).tolist()
ax.set_xticks(años)
ax.set_xticklabels(años)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.legend(frameon=False, loc="upper left")

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

color_monto = "#5FB7C6"
color_prod = "#0B4F6C"

fig, ax1 = plt.subplots(figsize=(12, 6))

# Barras
ax1.bar(
    df_plot["AÑO"],
    df_plot["MONTO"],
    color=color_monto,
    alpha=0.8,
    width=0.6
)

ax1.set_xlabel("Año")
ax1.set_ylabel("Monto (S/)", color=color_monto)
ax1.tick_params(axis='y', labelcolor=color_monto)

# FORZAR TODOS LOS AÑOS
años = df_plot["AÑO"].astype(int).tolist()
ax1.set_xticks(años)
ax1.set_xticklabels(años)

# Línea
ax2 = ax1.twinx()

ax2.plot(
    df_plot["AÑO"],
    df_plot["PRODUCCION"],
    color=color_prod,
    marker="o",
    linewidth=2.5
)

ax2.set_ylabel("Producción", color=color_prod)
ax2.tick_params(axis='y', labelcolor=color_prod)

# Estética
ax1.set_title("Relación entre financiamiento y producción científica",
              fontsize=14, pad=15)

ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)

ax1.grid(axis="y", linestyle="--", alpha=0.25)

plt.tight_layout()
plt.show()

# Se plantea el mismo gráfico pero con etiquetas en los valores
df_plot = observa_pre.copy()

df_plot["AÑO"] = pd.to_numeric(df_plot["AÑO"], errors="coerce")
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")
df_plot["PRODUCCION"] = pd.to_numeric(df_plot["PRODUCCION"], errors="coerce")

df_plot = df_plot.dropna(subset=["AÑO", "MONTO", "PRODUCCION"]).copy()
df_plot["AÑO"] = df_plot["AÑO"].astype(int)

df_plot = df_plot.sort_values("AÑO")

# ----------------------------
# Colores institucionales
# ----------------------------
color_monto = "#5FB7C6"   # celeste institucional
color_prod = "#0B4F6C"    # azul petróleo

# ----------------------------
# Figura
# ----------------------------
fig, ax1 = plt.subplots(figsize=(14, 7))

# ----------------------------
# Barras: MONTO
# ----------------------------
bars = ax1.bar(
    df_plot["AÑO"],
    df_plot["MONTO"],
    color=color_monto,
    alpha=0.85,
    width=0.6
)

ax1.set_xlabel("Año", fontsize=11)
ax1.set_ylabel("Monto (S/)", fontsize=11, color=color_monto)
ax1.tick_params(axis="y", labelcolor=color_monto)

# Mostrar todos los años en eje X
años = df_plot["AÑO"].tolist()
ax1.set_xticks(años)
ax1.set_xticklabels(años)

# ----------------------------
# Línea: PRODUCCION
# ----------------------------
ax2 = ax1.twinx()

ax2.plot(
    df_plot["AÑO"],
    df_plot["PRODUCCION"],
    color=color_prod,
    marker="o",
    linewidth=2.5,
    markersize=6
)

ax2.set_ylabel("Producción", fontsize=11, color=color_prod)
ax2.tick_params(axis="y", labelcolor=color_prod)

# ----------------------------
# Etiquetas en barras (MONTO)
# ----------------------------
max_monto = df_plot["MONTO"].max()

for bar in bars:
    height = bar.get_height()
    x = bar.get_x() + bar.get_width() / 2

    # Mostrar en millones para evitar saturación
    label = f"{height / 1e6:.1f}M"

    ax1.text(
        x,
        height + max_monto * 0.012,
        label,
        ha="center",
        va="bottom",
        fontsize=8,
        color=color_monto
    )

# ----------------------------
# Etiquetas en línea (PRODUCCION)
# con lógica para evitar superposición
# ----------------------------
max_prod = df_plot["PRODUCCION"].max()
prev_y = None

for i, (x, y) in enumerate(zip(df_plot["AÑO"], df_plot["PRODUCCION"])):
    if prev_y is not None and abs(y - prev_y) < max_prod * 0.08:
        # alternar arriba/abajo si están muy cerca
        if i % 2 == 0:
            offset = max_prod * 0.06
            va = "bottom"
        else:
            offset = -max_prod * 0.06
            va = "top"
    else:
        offset = max_prod * 0.035
        va = "bottom"

    ax2.text(
        x,
        y + offset,
        f"{int(y)}",
        ha="center",
        va=va,
        fontsize=9,
        color=color_prod,
        fontweight="bold"
    )

    prev_y = y

# ----------------------------
# Estética profesional
# ----------------------------
ax1.set_title(
    "Relación entre financiamiento y producción científica",
    fontsize=15,
    color=color_prod,
    pad=15
)

ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.grid(axis="y", linestyle="--", alpha=0.25)
ax1.set_axisbelow(True)

plt.tight_layout()
plt.show()

###############################################################################
# Este es el gráfico que integra mi ppt
###############################################################################

# ----------------------------
# Preparación de datos
# ----------------------------
df_plot = observa_pre.copy()

df_plot["AÑO"] = pd.to_numeric(df_plot["AÑO"], errors="coerce")
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")
df_plot["PRODUCCION"] = pd.to_numeric(df_plot["PRODUCCION"], errors="coerce")

df_plot = df_plot.dropna(subset=["AÑO", "MONTO", "PRODUCCION"]).copy()
df_plot["AÑO"] = df_plot["AÑO"].astype(int)
df_plot = df_plot.sort_values("AÑO")

# Convertir MONTO a millones
df_plot["MONTO_M"] = df_plot["MONTO"] / 1e6

# ----------------------------
# Colores
# ----------------------------
color_monto = "#5FB7C6"   # celeste institucional
color_prod = "#0B4F6C"    # azul petróleo
gris_suave = "#D9D9D9"

# ----------------------------
# Figura
# ----------------------------
fig, ax1 = plt.subplots(figsize=(14, 7))

# Barras: MONTO
bars = ax1.bar(
    df_plot["AÑO"],
    df_plot["MONTO_M"],
    color=color_monto,
    alpha=0.85,
    width=0.62,
    edgecolor="white",
    linewidth=1
)

ax1.set_xlabel("Año", fontsize=12)
ax1.set_ylabel("Monto (millones de S/)", fontsize=12, color=color_monto)
ax1.tick_params(axis="y", labelcolor=color_monto)

# Mostrar todos los años
años = df_plot["AÑO"].tolist()
ax1.set_xticks(años)
ax1.set_xticklabels(años)

# Línea: PRODUCCION
ax2 = ax1.twinx()
ax2.plot(
    df_plot["AÑO"],
    df_plot["PRODUCCION"],
    color=color_prod,
    marker="o",
    linewidth=2.8,
    markersize=7,
    zorder=3
)

ax2.set_ylabel("Producción", fontsize=12, color=color_prod)
ax2.tick_params(axis="y", labelcolor=color_prod)

# ----------------------------
# Etiquetas solo en años clave
# ----------------------------
# Año de monto máximo
idx_monto_max = df_plot["MONTO_M"].idxmax()
x_monto_max = df_plot.loc[idx_monto_max, "AÑO"]
y_monto_max = df_plot.loc[idx_monto_max, "MONTO_M"]

ax1.text(
    x_monto_max,
    y_monto_max + df_plot["MONTO_M"].max() * 0.01,
    f"{y_monto_max:.1f}M",
    ha="center",
    va="bottom",
    fontsize=10,
    color=color_monto,
    fontweight="bold"
)

# Año de producción máxima
idx_prod_max = df_plot["PRODUCCION"].idxmax()
x_prod_max = df_plot.loc[idx_prod_max, "AÑO"]
y_prod_max = df_plot.loc[idx_prod_max, "PRODUCCION"]

ax2.text(
    x_prod_max,
    y_prod_max + df_plot["PRODUCCION"].max() * 0.04,
    f"{int(y_prod_max)}",
    ha="center",
    va="bottom",
    fontsize=10,
    color=color_prod,
    fontweight="bold"
)

# Opcional: etiquetar primer y último año solo para contexto
for _, row in df_plot[df_plot["AÑO"].isin([df_plot["AÑO"].min(), df_plot["AÑO"].max()])].iterrows():
    ax2.text(
        row["AÑO"],
        row["PRODUCCION"] + df_plot["PRODUCCION"].max() * 0.03,
        f"{int(row['PRODUCCION'])}",
        ha="center",
        va="bottom",
        fontsize=9,
        color=color_prod
    )

# ----------------------------
# Título y estética
# ----------------------------
#ax1.set_title(
    #"Relación entre financiamiento y producción científica",
    #fontsize=17,
    #color=color_prod,
    #pad=18
#)

# Grilla suave
ax1.grid(axis="y", linestyle="--", alpha=0.22)
ax1.set_axisbelow(True)

# Limpiar bordes
ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Fondo blanco
ax1.set_facecolor("white")
fig.patch.set_facecolor("white")

plt.tight_layout()
plt.show()

###############################################################################
# ----------------------------
# Preparación de datos
# ----------------------------
df_plot = observa_pre.copy()

df_plot["AÑO"] = pd.to_numeric(df_plot["AÑO"], errors="coerce")
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")
df_plot["PRODUCCION"] = pd.to_numeric(df_plot["PRODUCCION"], errors="coerce")

df_plot = df_plot.dropna(subset=["AÑO", "MONTO", "PRODUCCION"]).copy()
df_plot["AÑO"] = df_plot["AÑO"].astype(int)
df_plot = df_plot.sort_values("AÑO")

df_plot["MONTO_M"] = df_plot["MONTO"] / 1e6

# ----------------------------
# Colores institucionales
# ----------------------------
color_barra = "#5FB7C6"      # celeste institucional
color_linea = "#0B4F6C"      # azul petróleo
color_barras_txt = "#6FAFBD" # tono suave para etiquetas barras

# Fondo de callout
bbox_props = dict(
    boxstyle="round,pad=0.22",
    facecolor="#F7F9E8",
    edgecolor="#B7BF10",
    linewidth=1.2
)

# ----------------------------
# Figura
# ----------------------------
fig, ax1 = plt.subplots(figsize=(14, 7))

# Barras
bars = ax1.bar(
    df_plot["AÑO"],
    df_plot["MONTO_M"],
    color=color_barra,
    alpha=0.88,
    width=0.60,
    edgecolor="white",
    linewidth=1
)

# Eje izquierdo
ax1.set_xlabel("Año", fontsize=12)
ax1.set_ylabel("Monto (millones de S/)", fontsize=12, color=color_barra)
ax1.tick_params(axis="y", labelcolor=color_barra)

# Mostrar todos los años
años = df_plot["AÑO"].tolist()
ax1.set_xticks(años)
ax1.set_xticklabels(años)

# Línea
ax2 = ax1.twinx()
ax2.plot(
    df_plot["AÑO"],
    df_plot["PRODUCCION"],
    color=color_linea,
    marker="o",
    linewidth=2.8,
    markersize=7,
    zorder=4
)

ax2.set_ylabel("Producción", fontsize=12, color=color_linea)
ax2.tick_params(axis="y", labelcolor=color_linea)

# ----------------------------
# Etiquetas en barras (discretas)
# ----------------------------
max_monto = df_plot["MONTO_M"].max()

for bar in bars:
    h = bar.get_height()
    x = bar.get_x() + bar.get_width() / 2

    ax1.text(
        x,
        h + max_monto * 0.015,
        f"{h:.1f}M",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=color_barras_txt,
        fontweight="bold"
    )

# ----------------------------
# Etiquetas de la línea en cajas
# ----------------------------
max_prod = df_plot["PRODUCCION"].max()

for i, (x, y, monto_m) in enumerate(zip(df_plot["AÑO"], df_plot["PRODUCCION"], df_plot["MONTO_M"])):
    # alternar la posición de las cajas para evitar choques
    if i % 2 == 0:
        y_offset = max_prod * 0.08
    else:
        y_offset = -max_prod * 0.10

    ax2.annotate(
        f"{int(y)}",
        xy=(x, y),
        xytext=(x, y + y_offset),
        textcoords="data",
        ha="center",
        va="center",
        fontsize=9,
        color=color_linea,
        fontweight="bold",
        bbox=bbox_props,
        arrowprops=dict(
            arrowstyle="-",
            color="#B7BF10",
            lw=0.8,
            shrinkA=5,
            shrinkB=5
        )
    )

# ----------------------------
# Estética
# ----------------------------
ax1.grid(axis="y", linestyle="--", alpha=0.22)
ax1.set_axisbelow(True)

ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.set_facecolor("white")
fig.patch.set_facecolor("white")

plt.tight_layout()
plt.show()

###############################################################################
# Se elabora una gráfica que muestra la tendencias de los componentes que
# integran la variable producción científica
###############################################################################
observa_ptp = (observa_conclu.groupby("AÑO", as_index=False).agg({"PUB":"sum", "TESIS":"sum", "PAT":"sum"}))

df_plot = observa_ptp.copy()
df_plot = df_plot.sort_values("AÑO")

fig, ax = plt.subplots(figsize=(12, 6))

# Colores institucionales
colors = {
    "PUB": "#0B4F6C",
    "TESIS": "#5FB7C6",
    "PAT": "#A3AD2C"
}

# Graficar líneas
for col in ["PUB", "TESIS", "PAT"]:
    ax.plot(
        df_plot["AÑO"],
        df_plot[col],
        marker="o",
        linewidth=2.5,
        label=col,
        color=colors[col]
    )

# Eje X completo
años = df_plot["AÑO"].tolist()
ax.set_xticks(años)

# Estética
#ax.set_title("Evolución de la producción científica por tipo",
             #fontsize=14, color="#0B4F6C", pad=15)

ax.set_xlabel("Año")
ax.set_ylabel("Número de productos")

ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(frameon=False)

plt.tight_layout()
plt.show()

###############################################################################
# Se considera el gráfico con etiquetas
###############################################################################

df_plot = observa_ptp.copy()
df_plot = df_plot.sort_values("AÑO")

fig, ax = plt.subplots(figsize=(12, 6))

# Colores
colors = {
    "PUB": "#0B4F6C",
    "TESIS": "#5FB7C6",
    "PAT": "#A3AD2C"
}

cols = ["PUB", "TESIS", "PAT"]

# ----------------------------
# Graficar líneas
# ----------------------------
for col in cols:
    ax.plot(
        df_plot["AÑO"],
        df_plot[col],
        marker="o",
        linewidth=2.5,
        label=col,
        color=colors[col]
    )

# ----------------------------
# Etiquetas dinámicas
# ----------------------------
max_y = df_plot[cols].max().max()

for j, col in enumerate(cols):
    prev_y = None
    
    for i, (x, y) in enumerate(zip(df_plot["AÑO"], df_plot[col])):
        
        if pd.isna(y):
            continue
        
        # Alternancia + ajuste si están cerca
        if prev_y is not None and abs(y - prev_y) < max_y * 0.04:
            offset = max_y * (0.05 if i % 2 == 0 else -0.05)
        else:
            offset = max_y * (0.04 if i % 2 == 0 else 0.00)
        
        ax.text(
            x,
            y + offset,
            f"{int(y)}",
            ha="center",
            va="bottom" if offset > 0 else "top",
            fontsize=9,
            color=colors[col],
            fontweight="bold" if col == "PUB" else "normal"
        )
        
        prev_y = y

# ----------------------------
# Ejes
# ----------------------------
años = df_plot["AÑO"].tolist()
ax.set_xticks(años)

#ax.set_title(
    #"Evolución de la producción científica por tipo",
    #fontsize=14,
    #color="#0B4F6C",
    #pad=15
#)

ax.set_xlabel("Año")
ax.set_ylabel("Número de productos")

# ----------------------------
# Estética
# ----------------------------
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(frameon=False)

plt.tight_layout()
plt.show()


###############################################################################
#
###############################################################################

# Considerando observa_concluido, se analiza la relación entre subvenciones y
# resultados de investigación científica

inve = observa_conclu[observa_conclu["INTERVENCIÓN"]=="INVESTIGACIÓN CIENTÍFICA"]
inve_ana = (inve.groupby("AÑO", as_index=False).agg({"INTERVENCIÓN":"count", "PUB":"sum"}))

df_plot = inve_ana.copy()
df_plot = df_plot.sort_values("AÑO")

fig, ax = plt.subplots(figsize=(12, 6))

# Colores institucionales
color_1 = "#0B4F6C"   # azul petróleo
color_2 = "#5FB7C6"   # celeste

# Líneas
ax.plot(
    df_plot["AÑO"],
    df_plot["INTERVENCIÓN"],
    marker="o",
    linewidth=2.8,
    label="Intervención",
    color=color_1
)

ax.plot(
    df_plot["AÑO"],
    df_plot["PUB"],
    marker="s",
    linewidth=2.8,
    label="Publicaciones",
    color=color_2
)

# Eje X
años = df_plot["AÑO"].tolist()
ax.set_xticks(años)

# ----------------------------
# Etiquetas SOLO al final (profesional)
# ----------------------------
for col, color, offset in [
    ("INTERVENCIÓN", color_1, 15),
    ("PUB", color_2, -10)
]:
    x_last = df_plot["AÑO"].iloc[-1]
    y_last = df_plot[col].iloc[-1]

    ax.text(
        x_last + 0.2,
        y_last + offset,
        f"{col} ({int(y_last)})",
        color=color,
        fontsize=10,
        fontweight="bold",
        va="center"
    )

# ----------------------------
# Estética
# ----------------------------
ax.set_title(
    "Evolución comparativa de Intervención y Publicaciones",
    fontsize=15,
    color=color_1,
    pad=15
)

ax.set_xlabel("Año")
ax.set_ylabel("Número")

ax.grid(axis="y", linestyle="--", alpha=0.25)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# quitar leyenda (ya etiquetas directamente)
# ax.legend()

# espacio para etiquetas finales
ax.set_xlim(df_plot["AÑO"].min(), df_plot["AÑO"].max() + 1)

plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(12, 6))

# Colores
color_1 = "#0B4F6C"   # azul petróleo
color_2 = "#5FB7C6"   # celeste

# Líneas
ax.plot(
    df_plot["AÑO"],
    df_plot["INTERVENCIÓN"],
    marker="o",
    linewidth=2.8,
    color=color_1
)

ax.plot(
    df_plot["AÑO"],
    df_plot["PUB"],
    marker="s",
    linewidth=2.8,
    color=color_2
)

# Eje X
años = df_plot["AÑO"].tolist()
ax.set_xticks(años)

# ----------------------------
# ETIQUETAS DINÁMICAS
# ----------------------------
max_y = max(
    df_plot["INTERVENCIÓN"].max(),
    df_plot["PUB"].max()
)

# INTERVENCIÓN
for i, (x, y) in enumerate(zip(df_plot["AÑO"], df_plot["INTERVENCIÓN"])):

    offset = max_y * (0.04 if i % 2 == 0 else -0.05)

    ax.text(
        x,
        y + offset,
        f"{int(y)}",
        ha="center",
        va="bottom" if offset > 0 else "top",
        fontsize=9,
        color=color_1,
        fontweight="bold"
    )

# PUB
for i, (x, y) in enumerate(zip(df_plot["AÑO"], df_plot["PUB"])):

    offset = max_y * (-0.06 if i % 2 == 0 else 0.05)

    ax.text(
        x,
        y + offset,
        f"{int(y)}",
        ha="center",
        va="bottom" if offset > 0 else "top",
        fontsize=9,
        color=color_2
    )

# ----------------------------
# Etiquetas finales (mantener)
# ----------------------------
for col, color, offset in [
    ("INTERVENCIÓN", color_1, 15),
    ("PUB", color_2, -10)
]:
    x_last = df_plot["AÑO"].iloc[-1]
    y_last = df_plot[col].iloc[-1]

    ax.text(
        x_last + 0.2,
        y_last + offset,
        f"{col} ({int(y_last)})",
        color=color,
        fontsize=10,
        fontweight="bold",
        va="center"
    )

# ----------------------------
# Estética
# ----------------------------
#ax.set_title(
    #"Evolución comparativa de Intervención y Publicaciones",
    #fontsize=15,
    #color=color_1,
    #pad=15
#)

ax.set_xlabel("Año")
ax.set_ylabel("Número")

ax.grid(axis="y", linestyle="--", alpha=0.25)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlim(df_plot["AÑO"].min(), df_plot["AÑO"].max() + 1)

plt.tight_layout()
plt.show()

###############################################################################
# Se elabora una gráfica para visualizar el top 10 de universidades involucradas
# se consideran tanto las subvenciones en condición de activo y concluido
###############################################################################
observa_uni = observa[observa["ORGANIZACIÓN"].str.contains("UNIVERSIDAD", case=False, na=False)]
observa_uni_a = observa_uni.ORGANIZACIÓN.value_counts(normalize=True).round(3)*100
observa_uni_a = observa_uni_a.to_frame()
observa_uni_a.reset_index(inplace=True)
observa_uni_a.rename(columns=({"proportion":"Porcentaje"}), inplace=True)
observa_uni_a = observa_uni_a[observa_uni_a["Porcentaje"]>=2.7]

observa_uni_a = observa_uni_a.sort_values("Porcentaje", ascending=True)

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
# Se elabora una gráfica para visualizar el top 10 de personas naturales
# Se consideran tanto las subvenciones en condición de activo y concluido
###############################################################################











##############################################################################################################################
# Se elabora una gráfica de correlación para visualizar la relación entre presupuesto y producción científica de universidades
# Se consideran las subvenciones en condición de concluido
###############################################################################
observa_pre_uni = observa_conclu[observa_conclu["ORGANIZACIÓN"].str.contains("UNIVERSIDAD", case=False, na=False)]
observa_pre_uni_a = (observa_pre_uni.groupby("ORGANIZACIÓN", as_index=False).agg({"MONTO":"sum", "PRODUCCION":"sum"}))

df_plot = observa_pre_uni_a.copy()

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
    "UNIVERSIDAD NACIONAL DE TRUJILLO":"UNT"
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
    if row["PRODUCCION"] > 90 or row["MONTO_M"] > 20:
        
        ax.text(
            row["MONTO_M"] + 1,
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
# Se elabora un NLP para considerar cuales son los tópicos más analizados
###############################################################################

# =========================================================
# 1. LIBRERÍAS
# =========================================================
import re
import unicodedata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from wordcloud import WordCloud

# =========================================================
# 2. COPIA DEL DATAFRAME Y VALIDACIÓN
# =========================================================
df_nlp = observa.copy()

# Asegúrate de que exista la columna TÍTULO
if "TÍTULO" not in df_nlp.columns:
    raise ValueError("No existe la columna 'TÍTULO' en el DataFrame.")

# Eliminar nulos y convertir a string
df_nlp = df_nlp.dropna(subset=["TÍTULO"]).copy()
df_nlp["TÍTULO"] = df_nlp["TÍTULO"].astype(str)

# =========================================================
# 3. FUNCIONES DE LIMPIEZA
# =========================================================
def quitar_acentos(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = quitar_acentos(texto)

    # Reemplazar saltos de línea
    texto = texto.replace("\n", " ").replace("\r", " ")

    # Eliminar números aislados y símbolos raros
    texto = re.sub(r"[^a-zA-Z\s]", " ", texto)

    # Eliminar espacios múltiples
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto

df_nlp["TITULO_LIMPIO"] = df_nlp["TÍTULO"].apply(limpiar_texto)

# =========================================================
# 4. STOPWORDS PERSONALIZADAS
# =========================================================
# Puedes ampliar esta lista según veas ruido en los resultados
stopwords_es_en = {
    # Español
    "de", "del", "la", "las", "el", "los", "y", "en", "para", "con", "por",
    "una", "un", "unos", "unas", "a", "al", "se", "que", "como", "su", "sus",
    "mediante", "sobre", "entre", "desde", "hacia", "uso", "usando", "basado",
    "basadas", "basados", "aplicado", "aplicada", "aplicadas", "aplicacion",
    "aplicaciones", "desarrollo", "diseno", "diseño", "evaluacion", "validacion",
    "sistema", "sistemas", "metodo", "metodos", "modelo", "modelos", "analisis",
    "estudio", "implementacion", "propuesta", "mejora", "obtencion", "caracterizacion",
    "caracterizacion", "tecnologia", "tecnologias", "proyecto", "proyectos", "ciencias",
    "doctorado", "maestria", "mencion", "mención", "programa", "ciencia", "peru", "nacionales",
    "nacional"

    # Inglés
    "and", "or", "the", "of", "for", "in", "on", "to", "with", "by", "from",
    "based", "using", "use", "system", "systems", "design", "development",
    "evaluation", "validation", "analysis", "study", "method", "methods",
    "model", "models", "application", "applications"
}

# =========================================================
# 5. TF-IDF
# =========================================================
vectorizer = TfidfVectorizer(
    stop_words=list(stopwords_es_en),
    max_df=0.90,       # elimina términos demasiado frecuentes
    min_df=2,          # elimina términos muy raros
    ngram_range=(1, 2) # unigramas y bigramas
)

X_tfidf = vectorizer.fit_transform(df_nlp["TITULO_LIMPIO"])
feature_names = np.array(vectorizer.get_feature_names_out())

print("Shape TF-IDF:", X_tfidf.shape)

# =========================================================
# 6. MODELADO DE TÓPICOS CON NMF
# =========================================================
n_topics = 6  # ajusta entre 5 y 10 y compara resultados

nmf_model = NMF(
    n_components=n_topics,
    random_state=42,
    init="nndsvda",
    max_iter=500
)

W = nmf_model.fit_transform(X_tfidf)  # documentos x tópicos
H = nmf_model.components_             # tópicos x términos

# =========================================================
# 7. MOSTRAR TÉRMINOS MÁS IMPORTANTES POR TÓPICO
# =========================================================
n_top_words = 10

topicos_resumen = []

for topic_idx, topic_weights in enumerate(H):
    top_term_indices = topic_weights.argsort()[::-1][:n_top_words]
    top_terms = feature_names[top_term_indices]
    top_pesos = topic_weights[top_term_indices]

    topicos_resumen.append({
        "TOPICO": f"Tópico {topic_idx + 1}",
        "TERMINOS_CLAVE": ", ".join(top_terms)
    })

    print(f"\nTópico {topic_idx + 1}:")
    for term, peso in zip(top_terms, top_pesos):
        print(f"  {term:<30} {peso:.4f}")

df_topicos = pd.DataFrame(topicos_resumen)

print("\nResumen de tópicos:")
print(df_topicos)

# =========================================================
# 8. ASIGNAR TÓPICO DOMINANTE A CADA TÍTULO
# =========================================================
df_nlp["TOPICO_DOMINANTE"] = W.argmax(axis=1) + 1
df_nlp["PESO_TOPICO"] = W.max(axis=1)

print("\nEjemplo de asignación de tópicos:")
print(df_nlp[["TÍTULO", "TOPICO_DOMINANTE", "PESO_TOPICO"]].head(10))

# =========================================================
# 9. FRECUENCIA DE TÓPICOS
# =========================================================
df_freq_topicos = (
    df_nlp["TOPICO_DOMINANTE"]
    .value_counts(normalize=True).round(2)
    .sort_index()
    .rename_axis("TOPICO")
    .reset_index(name="CANTIDAD")
)

print("\nFrecuencia de tópicos:")
print(df_freq_topicos)

# =========================================================
# 10. GRÁFICO DE BARRAS DE TÓPICOS
# =========================================================

map_nombres = {
    1: "Ingeniería y ambiente",
    2: "Física y energía",
    3: "Química aplicada",
    4: "Salud pública",
    5: "Nutrición y biología",
    6: "Sostenibilidad"
}


# Agregar nombres
df_freq_topicos["NOMBRE_TOPICO"] = df_freq_topicos["TOPICO"].map(map_nombres)
df_freq_topicos["CANTIDAD"] = df_freq_topicos["CANTIDAD"]*100

# Ordenar (opcional, recomendado)
df_freq_topicos = df_freq_topicos.sort_values("CANTIDAD", ascending=False)

# Gráfico
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))

bars = plt.bar(
    df_freq_topicos["NOMBRE_TOPICO"],
    df_freq_topicos["CANTIDAD"]
)

#plt.title("Distribución de proyectos por área temática")
plt.xlabel("")
plt.ylabel("Porcentaje (%)")

plt.xticks(rotation=25, ha="right")

# Etiquetas
for i, v in enumerate(df_freq_topicos["CANTIDAD"]):
    plt.text(i, v, str(v), ha="center", va="bottom")

plt.tight_layout()
plt.show()


# =========================================================
# 11. NUBE DE PALABRAS GLOBAL
# =========================================================
texto_total = " ".join(df_nlp["TITULO_LIMPIO"])

wordcloud = WordCloud(
    width=1400,
    height=800,
    background_color="white",
    stopwords=stopwords_es_en,
    collocations=False
).generate(texto_total)

plt.figure(figsize=(12, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Nube de palabras de títulos de proyectos")
plt.tight_layout()
plt.show()

# =========================================================
# 12. NUBE DE PALABRAS POR TÓPICO (OPCIONAL)
# =========================================================
for topico in sorted(df_nlp["TOPICO_DOMINANTE"].unique()):
    texto_topico = " ".join(
        df_nlp.loc[df_nlp["TOPICO_DOMINANTE"] == topico, "TITULO_LIMPIO"]
    )

    if texto_topico.strip():
        wc_topico = WordCloud(
            width=1200,
            height=700,
            background_color="white",
            stopwords=stopwords_es_en,
            collocations=False
        ).generate(texto_topico)

        plt.figure(figsize=(10, 6))
        plt.imshow(wc_topico, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Nube de palabras - Tópico {topico}")
        plt.tight_layout()
        plt.show()



