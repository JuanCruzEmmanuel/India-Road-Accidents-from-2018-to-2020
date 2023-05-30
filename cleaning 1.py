##
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()


##
import zipfile

##
archivo_zip = "C:/Users/juanc/Desktop/proyectos/data sciences/Data analyst/Data Cleaning and transformation/road-accidents-india-2017-2020.zip"

with zipfile.ZipFile(archivo_zip,"r") as zip_file:
    for nombre_archivo in zip_file.namelist():
        print(nombre_archivo)
##
import pandas as pd

data = pd.read_csv("C:/Users/juanc/Desktop/proyectos/data sciences/Data analyst/Data Cleaning and transformation/road-accidents-india-2017-2020.zip")
data.head()

##
pd.set_option('display.expand_frame_repr', False)
print(data.head())

##
#Voy analizar cuantos accidentes de transito existe entre 2017 a 2020 por ciudad
# primero cambio algunos nombres de columnas que estan media para el ogt
data.rename(columns={" Road Accidents  during 2019":"Road Accidents  during 2019"}, inplace= True)
##
#Voy a crear una nueva columna llamada "Total accidents during 2018-2020" y este va estar formada por la suma de los valores en cada año

col = ["Road Accidents  during 2018","Road Accidents  during 2019","Road Accidents  during 2020"]
data["Total accidents during 2018-2020"] = data[col].sum(axis=1)
print(data)
##
data = data[:-1] #Elimino la ultima fila
##
#lo mejor a la hora de ver datos es mediante graficos. aca vamos a utilizar plotly

import plotly.express as px

##
fig = px.bar(data,x="State",
             y="Total accidents during 2018-2020",
             title="Total accident during 2018-2020 in India",
             color="State",
             text_auto=".2s")
fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig.show()
# En este grafico podemos ver las 3 ciudades con mas accidentes, Tamil nadu, Madhya Predesh y Uttar Predesh
##
#Ahora lo mejor es analizar las defunciones generadas por estos accidentes, si bien el df tiene muertes
#desde 2017, no tengo la cantidad de accidentes en 2017. nueva columna llamada Total kill 2018-2020

col = ["Persons Killed 2018","Persons Killed 2019","Persons Killed 2020"]
data["Total kill during 2018-2020"] = data[col].sum(axis=1)

##

fig = px.bar(data,x="State",
             y="Total kill during 2018-2020",
             color="State",
             text_auto=".2s",
             title="Total kill during 2018-2020 India")
fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig.show()
#La ciudad con mas muertes en estos años por lejos es madhya predesh
##
#Vamos a graficar tanto los accidentes como las muertes, para eso importamos el modulo go

import plotly.graph_objects as go
##
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["State"],
    y=data["Total accidents during 2018-2020"],
    name="Total Accidents",
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data["State"],
    y=data["Total kill during 2018-2020"],
    name="Total kills",
    marker_color="lightsalmon"
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()

##
#Ahora voy a analizar el % de los accidentes y muertes

fig = px.pie(data,values="Total accidents during 2018-2020",
             names="State",
             title="percentage of accidents",
             color_discrete_sequence=px.colors.qualitative.Pastel,
             hole=0.5)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
#Con esto observamos que el 13% de los accidentes totales se produjeron en Tamil Nadu

##
fig = px.pie(data,values="Total kill during 2018-2020",
             names="State",
             title="percentage of Kills",
             color_discrete_sequence=px.colors.qualitative.Pastel,
             hole=0.5)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
#Aca podemos ver que el 15% de las muertes totales fueron en Uttar, mientras que en tamil solo representa un 7%

##
#Con esto lo mejor es ver la relacion accidente-muerte por ciudad. Con esto mejor creo un nueco df

data["Ralation accident-kill"]=100*(data["Total kill during 2018-2020"]/ data["Total accidents during 2018-2020"])
##
fig = px.bar(data[data["Total kill during 2018-2020"]>10000],x="State",
             y="Ralation accident-kill",
             color="State",
             title="Relationship accidents-kill in India with kill more than 10k",
             text_auto=".2s",
             hover_data=["Total kill during 2018-2020","Total accidents during 2018-2020"])
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total ascending'})
fig.show()
##
fig = px.bar(data[data["Total kill during 2018-2020"]>20000],x="State",
             y="Ralation accident-kill",
             color="State",
             title="Relationship accidents-kill in India with kill more than 20k",
             text_auto=".2s",
             hover_data=["Total kill during 2018-2020","Total accidents during 2018-2020"])
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total ascending'})
fig.show()