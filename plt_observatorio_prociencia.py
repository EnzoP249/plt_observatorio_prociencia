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

# Se calcula la cantidad de subvenciones durante el periodo de análisis
observa["ID_CONTRATO"].count()

# Se calcula la suma del total de subvenciones durante el periodo de análisis
observa["MONTO"].sum()


###############################################################################
# Se realiza una gráfico de barras considerando el dataframe observa_año
###############################################################################

observa_año = observa_año.sort_values("AÑO")
df_plot = observa_año.copy()

df_plot["AÑO"] = pd.to_numeric(df_plot["AÑO"], errors="coerce")
df_plot["MONTO"] = pd.to_numeric(df_plot["MONTO"], errors="coerce")
df_plot["ID_CONTRATO"] = pd.to_numeric(df_plot["ID_CONTRATO"], errors="coerce")

df_plot = df_plot.dropna(subset=["AÑO", "MONTO", "ID_CONTRATO"]).copy()
df_plot["AÑO"] = df_plot["AÑO"].astype(int)
df_plot = df_plot.sort_values("AÑO")

# Monto en millones
df_plot["MONTO_M"] = df_plot["MONTO"] / 1e6

color_monto = "#00A7B5"
color_linea = "#A3AD2C"

fig, ax1 = plt.subplots(figsize=(14, 7))

# Barras
bars = ax1.bar(
    df_plot["AÑO"],
    df_plot["MONTO_M"],
    color=color_monto,
    alpha=0.82,
    width=0.60,
    edgecolor="white",
    linewidth=1
)

ax1.set_xlabel("Año", fontsize=11)
ax1.set_ylabel("Monto (millones de S/)", fontsize=11, color=color_monto)
ax1.tick_params(axis="y", labelcolor=color_monto)

años = df_plot["AÑO"].tolist()
ax1.set_xticks(años)
ax1.set_xticklabels(años)

# Línea
ax2 = ax1.twinx()

ax2.plot(
    df_plot["AÑO"],
    df_plot["ID_CONTRATO"],
    color=color_linea,
    marker="o",
    linewidth=2.6,
    markersize=6,
    zorder=5
)

ax2.set_ylabel("N.° de subvenciones", fontsize=11, color=color_linea)
ax2.tick_params(axis="y", labelcolor=color_linea)

# ----------------------------
# Etiquetas selectivas
# ----------------------------
idx_monto_max = df_plot["MONTO_M"].idxmax()
idx_linea_max = df_plot["ID_CONTRATO"].idxmax()
idx_ultimo = df_plot.index[-1]

# Etiquetar barras solo en máximo y años relevantes
indices_barras = {idx_monto_max}

# También puedes agregar segundo mayor monto
indices_barras.add(df_plot["MONTO_M"].nlargest(2).index[-1])

for idx in indices_barras:
    row = df_plot.loc[idx]
    ax1.text(
        row["AÑO"],
        row["MONTO_M"] + df_plot["MONTO_M"].max() * 0.035,
        f"S/ {row['MONTO_M']:.1f} M",
        ha="center",
        va="bottom",
        fontsize=10,
        color=color_monto,
        fontweight="bold"
    )

# Etiquetar línea solo en máximo, primer año y último año
indices_linea = {idx_linea_max, df_plot.index[0], idx_ultimo}

for idx in indices_linea:
    row = df_plot.loc[idx]
    ax2.text(
        row["AÑO"],
        row["ID_CONTRATO"] + df_plot["ID_CONTRATO"].max() * 0.045,
        f"{int(row['ID_CONTRATO'])}",
        ha="center",
        va="bottom",
        fontsize=10,
        color=color_linea,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.18",
            facecolor="white",
            edgecolor="none",
            alpha=0.85
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

ax1.set_ylim(0, df_plot["MONTO_M"].max() * 1.18)
ax2.set_ylim(0, df_plot["ID_CONTRATO"].max() * 1.18)

plt.tight_layout()
plt.show()



observa_año = observa_año.sort_values("AÑO")

# Colores institucionales
color_principal = "#00A7B5"   # turquesa
color_secundario = "#5FB7C6"  # azul petróleo

# Tamaño más amplio (clave para separar barras)
plt.figure(figsize=(12,6))

# Crear barras con menor ancho (más espacio)
bars = plt.bar(observa_año["AÑO"], observa_año["ID_CONTRATO"], 
               color=color_principal, 
               width=0.6)

# Etiquetas
plt.xlabel("Año", fontsize=11, color="black")
plt.ylabel("Número de subvenciones", fontsize=11, color="black")

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
df_plot.columns

# Me quedo solo con un conjunto de columnas establecidas
df_plot = df_plot[["AÑO", "INVESTIGACIÓN CIENTÍFICA", "INNOVACIÓN Y TRANSFERENCIA TECNOLÓGICA", "EQUIPAMIENTO"]]
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
    "#A3AD2C",  # verde
    "#7A3E9D",  # morado
]

# ----------------------------
# Marcadores distintos
# ----------------------------
markers = ["o", "^", "*"]

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
# Etiquetas sobre cada línea
# ----------------------------
offsets = [8, 12, -10]

for i, c in enumerate(cols):

    for x, y in zip(df_plot["AÑO"], df_plot[c]):

        # Evitar mostrar etiquetas en cero
        if y == 0:
            continue

        ax.text(
            x,
            y + offsets[i],                 # separación vertical
            f"{int(y)}",
            ha="center",
            va="bottom" if offsets[i] > 0 else "top",
            fontsize=9,
            color=colors_list[i],
            fontweight="bold"
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
    colormap="Set2",
    edgecolor="white",
    linewidth=0.9
)

# ----------------------------
# 3. Estética profesional
# ----------------------------
ax.set_xlabel("Año", fontsize=11)
ax.set_ylabel("Monto adjudicado (millones de S/)", fontsize=11)

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
        fontsize=9,
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
        fontsize=9,
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
ax.set_ylabel("Número de productos científicos")

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
# Se analiza la dinámica de las subvenciones otorgadas y las publicaciones
# científicas elaboradas
###############################################################################
# =========================================================
# FIGURA
# =========================================================
fig, ax = plt.subplots(figsize=(12, 6))

# =========================================================
# COLORES
# =========================================================
color_1 = "#0B4F6C"   # azul petróleo
color_2 = "#5FB7C6"   # celeste

# =========================================================
# LÍNEAS
# =========================================================
ax.plot(
    df_plot["AÑO"],
    df_plot["INTERVENCIÓN"],
    marker="o",
    linewidth=2.8,
    markersize=6,
    color=color_1,
    label="Subvenciones en investigación científica"
)

ax.plot(
    df_plot["AÑO"],
    df_plot["PUB"],
    marker="s",
    linewidth=2.8,
    markersize=6,
    color=color_2,
    label="Producción científica"
)

# =========================================================
# EJE X
# =========================================================
años = df_plot["AÑO"].tolist()

ax.set_xticks(años)
ax.set_xticklabels(años)

# =========================================================
# ETIQUETAS INTELIGENTES
# =========================================================
for x, y1, y2 in zip(
    df_plot["AÑO"],
    df_plot["INTERVENCIÓN"],
    df_plot["PUB"]
):

    # diferencia entre ambas líneas
    diff = abs(y1 - y2)

    # si están muy cerca -> separar más
    if diff < 25:

        offset_1 = 18
        offset_2 = -22

    else:

        offset_1 = 12
        offset_2 = 12

    # ----------------------------
    # INTERVENCIÓN
    # ----------------------------
    if y1 != 0:

        ax.text(
            x,
            y1 + offset_1,
            f"{int(y1)}",
            ha="center",
            va="bottom",
            fontsize=9,
            color=color_1,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="white",
                edgecolor="none",
                alpha=0.75
            )
        )

    # ----------------------------
    # PUB
    # ----------------------------
    if y2 != 0:

        ax.text(
            x,
            y2 + offset_2,
            f"{int(y2)}",
            ha="center",
            va="bottom" if offset_2 > 0 else "top",
            fontsize=9,
            color=color_2,
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="white",
                edgecolor="none",
                alpha=0.75
            )
        )

# =========================================================
# LEYENDA PROFESIONAL
# =========================================================
legend = ax.legend(
    loc="upper right",
    frameon=True,
    fancybox=True,
    fontsize=10
)

legend.get_frame().set_facecolor("white")
legend.get_frame().set_edgecolor("#D9D9D9")
legend.get_frame().set_alpha(0.95)

# =========================================================
# ESTÉTICA
# =========================================================
# ax.set_title(
#     "Evolución comparativa de intervenciones y producción científica",
#     fontsize=15,
#     color=color_1,
#     pad=15
# )

ax.set_xlabel("Año", fontsize=11)

ax.set_ylabel(
    "Número de subvenciones y publicaciones",
    fontsize=11
)

ax.grid(axis="y", linestyle="--", alpha=0.25)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_axisbelow(True)

ax.set_xlim(
    df_plot["AÑO"].min(),
    df_plot["AÑO"].max() + 0.8
)

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


# =========================================================
# 2. AGRUPACIÓN
# =========================================================
observa_pre_uni_a = (
    observa_pre_uni
    .groupby("ORGANIZACIÓN", as_index=False)
    .agg({
        "MONTO": "sum",
        "PRODUCCION": "sum"
    })
)

# Menor producción
observa_pre_uni_a = (
    observa_pre_uni_a[
        observa_pre_uni_a["PRODUCCION"] <= 25
    ]
)

# =========================================================
# 3. DATAFRAME BASE
# =========================================================
df_plot = observa_pre_uni_a.copy()

df_plot["MONTO"] = pd.to_numeric(
    df_plot["MONTO"],
    errors="coerce"
)

df_plot["PRODUCCION"] = pd.to_numeric(
    df_plot["PRODUCCION"],
    errors="coerce"
)

df_plot = df_plot.dropna(
    subset=["MONTO", "PRODUCCION"]
).copy()

# Escala en millones
df_plot["MONTO_M"] = df_plot["MONTO"] / 1e6

# =========================================================
# 4. DICCIONARIO DE ABREVIACIONES
# =========================================================
map_dict = {
    "UNIVERSIDAD PRIVADA ANTENOR ORREGO": "UPAO",
    "UNIVERSIDAD ANDINA DEL CUSCO": "UAC",
    "UNIVERSIDAD NACIONAL DEL CENTRO DEL PERU": "UNCP",
    "UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO": "UNSAAC",
    "UNIVERSIDAD SAN IGNACIO DE LOYOLA S.R.L.": "USIL",
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
    "UNIVERSIDAD CESAR VALLEJO S.A.C.":"UCV"
}

# =========================================================
# 5. MAPEO
# =========================================================
df_plot["ORG_SHORT"] = (
    df_plot["ORGANIZACIÓN"]
    .map(map_dict)
)

# Mantener solo universidades del diccionario
df_plot = (
    df_plot[
        df_plot["ORG_SHORT"].notna()
    ]
    .copy()
)

# =========================================================
# 6. VARIABLES
# =========================================================
x = df_plot["MONTO_M"]
y = df_plot["PRODUCCION"]

# =========================================================
# 7. LÍNEA DE TENDENCIA
# =========================================================
coef = np.polyfit(x, y, 1)

trend = np.poly1d(coef)

# =========================================================
# 8. FIGURA
# =========================================================
fig, ax = plt.subplots(figsize=(10, 6))

# =========================================================
# 9. SCATTER
# =========================================================
ax.scatter(
    x,
    y,
    color="#5FB7C6",
    s=90,
    edgecolors="white",
    linewidth=1.5,
    zorder=3
)

# =========================================================
# 10. LÍNEA DE TENDENCIA
# =========================================================
#ax.plot(
    #x,
    #trend(x),
    #color="#0B4F6C",
    #linewidth=2.2,
    #linestyle="--",
    #zorder=2
#)

# =========================================================
# 11. ETIQUETAS
# =========================================================
for _, row in df_plot.iterrows():

    ax.text(
        row["MONTO_M"] + 0.05,
        row["PRODUCCION"],
        row["ORG_SHORT"],
        fontsize=9,
        ha="left",
        va="center",
        color="#0B4F6C",
        fontweight="bold"
    )

# =========================================================
# 12. ESTÉTICA
# =========================================================
# ax.set_title(
#     "Relación entre financiamiento y producción científica",
#     fontsize=14,
#     color="#0B4F6C",
#     pad=15
# )

ax.set_xlabel(
    "Monto (millones de S/)"
)

ax.set_ylabel(
    "Producción científica"
)

ax.grid(
    alpha=0.25,
    linestyle="--"
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_axisbelow(True)

plt.tight_layout()
plt.show()


###############################################################################
# Se analiza que universidades han invertido más en becas y programas
# durante el periodo de análisis
###############################################################################

# se considera el dataframe observa y se obtiene los registros asociados directamente con universidad
universidad = observa[observa["ORGANIZACIÓN"].str.contains("UNIVERSIDAD", case=False, na=False)]

# se considera solo el tipo de intervención becas y programas
universidad_beca = universidad[universidad["INTERVENCIÓN"]=="BECAS Y PROGRAMAS"]

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
    "UNIVERSIDAD NACIONAL DE SAN MARTIN":"UNSM",
    "UNIVERSIDAD NACIONAL DEL CENTRO DEL PERU":"UNCP",
    "UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO":"UNA",
    "UNIVERSIDAD PRIVADA ANTENOR ORREGO":"UPAO"
}


universidad_beca["ORG_SHORT"] = universidad_beca["ORGANIZACIÓN"].map(map_dict)

# Si alguna no está en el diccionario usar su nombre normal
universidad_beca["ORG_SHORT"] = universidad_beca["ORG_SHORT"].fillna(
    universidad_beca["ORGANIZACIÓN"]
)


# se considera el año 2015
uni_beca_2015 = universidad_beca[universidad_beca["AÑO"]==2015]
uni_beca_2015 = (uni_beca_2015.groupby("ORG_SHORT", as_index=False).agg({"MONTO":"sum"}))

# Ordenar de mayor a menor
uni_beca_2015 = uni_beca_2015.sort_values("MONTO", ascending=False)

# Si tienes muchas instituciones, agrupa las menores como "Otros"
top_n = 5
df_top = uni_beca_2015.head(top_n).copy()

otros = uni_beca_2015.iloc[top_n:]["MONTO"].sum()

if otros > 0:
    df_top = pd.concat([
        df_top,
        pd.DataFrame({
            "ORG_SHORT": ["Otros"],
            "MONTO": [otros]
        })
    ])

# Convertir a millones
df_top["MONTO_M"] = df_top["MONTO"] / 1e6

# Colores profesionales
colors = [
    "#D9D9D9", "#5FB7C6", "#A3AD2C", "#7A8C99",
    "#D9A441", "#9B6A6C", "#6FA8DC"
]

fig, ax = plt.subplots(figsize=(9, 7))

wedges, texts, autotexts = ax.pie(
    df_top["MONTO_M"],
    labels=df_top["ORG_SHORT"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors[:len(df_top)],
    pctdistance=0.78,
    labeldistance=1.08,
    wedgeprops={
        "width": 0.42,
        "edgecolor": "white",
        "linewidth": 1
    },
    textprops={
        "fontsize": 9,
        "color": "#1F1F1F"
    }
)

# Centro del donut
total_m = df_top["MONTO_M"].sum()

ax.text(
    0, 0.05,
    f"S/ {total_m:,.1f} M",
    ha="center",
    va="center",
    fontsize=16,
    fontweight="bold",
    color="#0B4F6C"
)

ax.text(
    0, -0.12,
    "Monto total",
    ha="center",
    va="center",
    fontsize=10,
    color="#555555"
)

#ax.set_title(
    #"Distribución del monto adjudicado por institución",
    #fontsize=14,
    #color="#0B4F6C",
    #pad=18
#)

plt.tight_layout()
plt.show()


# se considera el año 2023
uni_beca_2023 = universidad_beca[universidad_beca["AÑO"]==2023]
uni_beca_2023 = (uni_beca_2023.groupby("ORG_SHORT", as_index=False).agg({"MONTO":"sum"}))

# Ordenar de mayor a menor
uni_beca_2023 = uni_beca_2023.sort_values("MONTO", ascending=False)

# Si tienes muchas instituciones, agrupa las menores como "Otros"
top_n = 5
df_top = uni_beca_2023.head(top_n).copy()

otros = uni_beca_2023.iloc[top_n:]["MONTO"].sum()

if otros > 0:
    df_top = pd.concat([
        df_top,
        pd.DataFrame({
            "ORG_SHORT": ["Otros"],
            "MONTO": [otros]
        })
    ])

# Convertir a millones
df_top["MONTO_M"] = df_top["MONTO"] / 1e6

# Colores profesionales
colors = [
    "#D9D9D9", "#5FB7C6", "#A3AD2C", "#7A8C99",
    "#D9A441", "#9B6A6C", "#6FA8DC"
]

fig, ax = plt.subplots(figsize=(9, 7))

wedges, texts, autotexts = ax.pie(
    df_top["MONTO_M"],
    labels=df_top["ORG_SHORT"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors[:len(df_top)],
    pctdistance=0.78,
    labeldistance=1.08,
    wedgeprops={
        "width": 0.42,
        "edgecolor": "white",
        "linewidth": 1
    },
    textprops={
        "fontsize": 9,
        "color": "#1F1F1F"
    }
)

# Centro del donut
total_m = df_top["MONTO_M"].sum()

ax.text(
    0, 0.05,
    f"S/ {total_m:,.1f} M",
    ha="center",
    va="center",
    fontsize=16,
    fontweight="bold",
    color="#0B4F6C"
)

ax.text(
    0, -0.12,
    "Monto total",
    ha="center",
    va="center",
    fontsize=10,
    color="#555555"
)

#ax.set_title(
    #"Distribución del monto adjudicado por institución",
    #fontsize=14,
    #color="#0B4F6C",
    #pad=18
#)

plt.tight_layout()
plt.show()



# =========================================================
# 1. FUNCIÓN PARA PREPARAR DATA POR AÑO
# =========================================================
def preparar_donut_data(data, year, top_n=5):
    df_year = data[data["AÑO"] == year].copy()

    df_year = (
        df_year.groupby("ORG_SHORT", as_index=False)
        .agg(MONTO=("MONTO", "sum"))
        .sort_values("MONTO", ascending=False)
    )

    df_top = df_year.head(top_n).copy()
    otros = df_year.iloc[top_n:]["MONTO"].sum()

    if otros > 0:
        df_top = pd.concat([
            df_top,
            pd.DataFrame({"ORG_SHORT": ["Otros"], "MONTO": [otros]})
        ], ignore_index=True)

    df_top["MONTO_M"] = df_top["MONTO"] / 1e6
    return df_top


# =========================================================
# 2. PREPARAR DATA
# =========================================================
df_2015 = preparar_donut_data(universidad_beca, 2015, top_n=5)
df_2023 = preparar_donut_data(universidad_beca, 2023, top_n=5)


# =========================================================
# 3. MAPA GLOBAL DE COLORES POR INSTITUCIÓN
# =========================================================
palette = [
    "#0B4F6C",  # azul petróleo
    "#5FB7C6",  # celeste
    "#A3AD2C",  # verde
    "#7A8C99",  # gris azulado
    "#D9A441",  # dorado
    "#E07A5F",  # coral
    "#6FA8DC",  # azul suave
    "#C6D166"   # verde claro
]

orgs_global = pd.concat([
    df_2015["ORG_SHORT"],
    df_2023["ORG_SHORT"]
]).drop_duplicates().tolist()

color_map = {
    org: palette[i % len(palette)]
    for i, org in enumerate(orgs_global)
}

# Colores manuales para evitar confusión
color_map["UNI"] = "#0B4F6C"
color_map["UNIVERSIDAD NACIONAL DEL SANTA"] = "#E07A5F"
color_map["Otros"] = "#D9D9D9"


# =========================================================
# 4. FUNCIÓN PARA GRAFICAR DONUT
# =========================================================
def graficar_donut(df_top, year, ax):
    colors = [color_map.get(org, "#D9D9D9") for org in df_top["ORG_SHORT"]]

    wedges, texts, autotexts = ax.pie(
        df_top["MONTO_M"],
        labels=df_top["ORG_SHORT"],
        autopct=lambda p: f"{p:.1f}%" if p >= 3 else "",
        startangle=90,
        colors=colors,
        pctdistance=0.76,
        labeldistance=1.10,
        wedgeprops={
            "width": 0.42,
            "edgecolor": "white",
            "linewidth": 1.2
        },
        textprops={
            "fontsize": 9,
            "color": "#1F1F1F"
        }
    )

    # Mejorar visibilidad de porcentajes según color del segmento
    for wedge, autotext in zip(wedges, autotexts):
        r, g, b, _ = wedge.get_facecolor()
        luminance = 0.299*r + 0.587*g + 0.114*b

        autotext.set_color("#1F1F1F" if luminance > 0.62 else "white")
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    total_m = df_top["MONTO_M"].sum()

    ax.text(
        0, 0.06,
        f"S/ {total_m:,.1f} M",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#0B4F6C"
    )

    ax.text(
        0, -0.12,
        "Monto total",
        ha="center",
        va="center",
        fontsize=9,
        color="#555555"
    )

    ax.set_title(
        f"{year}",
        fontsize=17,
        fontweight="bold",
        color="#0B4F6C",
        pad=14
    )


# =========================================================
# 5. GRAFICAR DONUTS COMPARATIVOS
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

graficar_donut(df_2015, 2015, axes[0])
graficar_donut(df_2023, 2023, axes[1])

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



