# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 09:33:49 2026

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
observa = pd.read_excel("Subvenciones_20260428_anemia.xlsx", sheet_name="Resultados", header=0)

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
    df_plot["ID_CONTRATO"],
    color=color_prod,
    marker="o",
    linewidth=2.5,
    markersize=6
)

ax2.set_ylabel("N de Subvenciones", fontsize=11, color=color_prod)
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
max_prod = df_plot["ID_CONTRATO"].max()
prev_y = None

for i, (x, y) in enumerate(zip(df_plot["AÑO"], df_plot["ID_CONTRATO"])):
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
#ax1.set_title(
    #"Relación entre financiamiento y producción científica",
    #fontsize=15,
    #color=color_prod,
    #pad=15
#)

ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.grid(axis="y", linestyle="--", alpha=0.25)
ax1.set_axisbelow(True)

plt.tight_layout()
plt.show()










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
            float(y),
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
#ax1.set_title(
    #"Relación entre financiamiento y producción científica",
    #fontsize=15,
    #color=color_prod,
    #pad=15
#)

ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.grid(axis="y", linestyle="--", alpha=0.25)
ax1.set_axisbelow(True)

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

#plt.gca().spines["top"].set_visible(False)
#plt.gca().spines["right"].set_visible(False)

plt.grid(axis="x", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()



observa_uni = observa[observa["ORGANIZACIÓN"].str.contains("UNIVERSIDAD", case=False, na=False)]
observa_uni_a = observa_uni.ORGANIZACIÓN.value_counts(normalize=True).round(3)*100
observa_uni_a = observa_uni_a.to_frame()
observa_uni_a.reset_index(inplace=True)
observa_uni_a.rename(columns=({"proportion":"Porcentaje"}), inplace=True)
observa_uni_a = observa_uni_a.head(10)

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
# Se analiza que se ha investigado sobre anemia en el Perú
###############################################################################







