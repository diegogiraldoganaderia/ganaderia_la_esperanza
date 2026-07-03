import streamlit as st
import base64
from Ganaderia import *
import os
import time
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from supabase import create_client

url ="https://soyjodguzmbiggwymfdn.supabase.co"
key ="sb_secret_bB5UAtzbkyxob7xu_8O4Mw_vwbEkb4K"

supabase = create_client(url, key)


#objetos
buscar = Buscador()
nacimientos = Agregar_Eliminar()
generar_informe=Informes()

#Alerta de correo díario

# Esto permite que GitHub ejecute la función desde la consola




#Titulo
st.markdown(
    """
    <style>
    .titulo-ganaderia {
        background-color: rgba(0, 0, 0, 0.5); /* Fondo negro 50% opacidad */
        color: white;                        /* Texto blanco */
        text-align: center;                  /* Centra el texto */
        font-family: sans-serif;             /* Letra moderna de Streamlit */
        font-weight: bold;                   /* Texto en negrita */
        padding: 20px;                       /* Espacio interno */
        border-radius: 8px;                  /* Bordes redondeados */
        font-size: 40px;                     /* Tamaño del título */
    }
    </style>
    <div class='titulo-ganaderia'>GANADERIA LA ESPERANZA</div>
    """,
    unsafe_allow_html=True
)


#fondo
def set_local_bg(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_local_bg(r"fondodos.png")
#menú
st.header("MENÚ")

#FORMULARIOS CERRADOS
if "registros" not in st.session_state:
    st.session_state.registros = False

if "registro_crias" not in st.session_state:
    st.session_state.registro_crias = False

if "informe_nacimientos" not in st.session_state:
    st.session_state.informe_nacimientos = False

if "informe_vacas" not in st.session_state:
    st.session_state.informe_vacas = False

if "modificar_df" not in st.session_state:
    st.session_state.modificar_df = False

if "subir_pdf_registro" not in st.session_state:
    st.session_state.subir_pdf_registro=False

if "informe_embriones" not in st.session_state:
    st.session_state.informe_embriones=False

if "informe_ganado_puro" not in st.session_state:  
    st.session_state.informe_ganado_puro=False

if "graficos" not in st.session_state:
    st.session_state.graficos=False

if "tiempo_inseminacion" not in st.session_state:
    st.session_state.tiempo_inseminacion=False

#Botones 
#estilo de botone
st.html("""
    <style>
    button {
        height: 60px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    </style>
""")
#      BOTON INICIO

if st.button("Inicio",use_container_width=True):
    st.session_state.registro_crias=False
    st.session_state.informe_nacimientos= False
    st.session_state.informe_vacas = False
    st.session_state.modificar_df = False
    st.session_state.registros=False
    st.session_state.subir_pdf_registro=False
    st.session_state.graficos=False
    st.session_state.informe_embriones=False
    st.session_state.informe_ganado_puro=False
    st.session_state.tiempo_inseminacion=False
    

#columnas para botones
col1, col2, col3= st.columns(3)     
#botones menu
#      BOTON 1
with col1:
    if st.button("REGISTRO NACIMIENTOS",use_container_width=True): 
        st.session_state.registro_crias=True
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.graficos=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
        st.session_state.tiempo_inseminacion=False

#      BOTON 2
with col2:
    if st.button("INFORME NACIMIENTOS",use_container_width=True):
        st.session_state.informe_nacimientos= True
        st.session_state.registro_crias=False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.graficos=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
        st.session_state.tiempo_inseminacion=False

#      BOTON 3 
with col3:
    if st.button("INFORME VACAS",use_container_width=True):
        st.session_state.informe_vacas = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.graficos=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
        st.session_state.tiempo_inseminacion=False
with col1:
    if st.button("MODIFICAR DATOS",use_container_width=True):
        st.session_state.modificar_df = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
        st.session_state.graficos=False
        st.session_state.tiempo_inseminacion=False

with col2:
    if st.button("REGISTROS",use_container_width=True):
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=True
        st.session_state.subir_pdf_registro=False
        st.session_state.graficos=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
        st.session_state.tiempo_inseminacion=False

with col3:
    if st.button("AÑADIR REGISTROS",use_container_width=True):
        st.session_state.subir_pdf_registro=True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.graficos=False
        st.session_state.tiempo_inseminacion=False
      
    #   BOTON 5

with col1:
    if  st.button("INFORME EMBRIONES",use_container_width=True):
        st.session_state.informe_embriones=True
        st.session_state.graficos=False
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.informe_ganado_puro=False
        st.session_state.tiempo_inseminacion=False
with col2:
    if  st.button("INFORME GANADO PURO",use_container_width=True):
        st.session_state.informe_ganado_puro=True
        st.session_state.informe_embriones=False
        st.session_state.graficos=False
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.tiempo_inseminacion=False

with col3:
    if st.button("GRÁFICOS",use_container_width=True):
        st.session_state.graficos=True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
        st.session_state.tiempo_inseminacion=False
#boton 6
if st.button("INSEMINACION PENDIENTE PALPACION",use_container_width=True):
        st.session_state.tiempo_inseminacion=True
        st.session_state.graficos=False
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.informe_embriones=False
        st.session_state.informe_ganado_puro=False
#//FORMULARIOS// QUE HACEN LOS BOTONES
if st.session_state.subir_pdf_registro:
    st.write(key[:20])
    st.title("Subir PDF a carpeta")
    archivo = st.file_uploader("Sube PDF", type=["pdf"])
    if archivo is not None:
        supabase.storage.from_("REGISTROS").upload(
        path=archivo.name,  # nombre del archivo
        file=archivo.getvalue(),  # bytes del uploader
        file_options={
            "content-type": "application/pdf",
            "upsert": "true"})
        if st.success("Guardado correctamente"):
            st.session_state.subir_pdf_registro=False
            st.rerun()
 
#aplicacion 1
if st.session_state.registro_crias: 
    vaca = st.text_input("ID de la vaca").lower()
    fn = st.date_input("Fecha nacimiento")
    fn=pd.to_datetime(fn,format="%d/%m/%Y")
    sexo = st.selectbox("Sexo",["macho", "hembra"])
    fincas=[]
    for i in range(len(df_fincas)):
        fincas.append(df_fincas.iloc[i,0]) 
    finca = st.selectbox("Finca",fincas)
    toros=[]
    for i in range(len(df_toros)):
        toros.append(df_toros.iloc[i,0])
    toro = st.selectbox("Toro",toros)
    razas=[]
    for i in range(len(df_razas)):
        razas.append(df_razas.iloc[i,0]) 
    raza = st.selectbox("Raza",razas)
    observaciones = st.text_area("Observaciones")
    
    if st.button("Guardar",use_container_width=True):
        registro_cria=nacimientos.nacimiento(buscar,vaca,fn,sexo,finca,observaciones,toro,raza)
        nacimientos.guardar(df_inseminacion,df_animal,registro_cria[1],registro_cria[0],df_embriones,df_fincas,df_razas,df_ganado_puro,df_servicios,df_protocolo)
        st.success("Guardado")
        st.session_state.registro_crias=False
        st.rerun()   
#aplicacion 2
if st.session_state.informe_nacimientos:  
    
    fecha=st.date_input("A partir de que fecha desea el informe")
    fincas=[]
    for i in range(len(df_fincas)):
        fincas.append(df_fincas.iloc[i,0]) 
    finca = st.multiselect("Finca",fincas)
    tc=st.multiselect("Tipo_concepcion",["TE","CN","IA"])
    fecha=pd.to_datetime(fecha,format="%d/%m/%Y")
    filtros=[fecha,finca,tc]

    
    col1, col2= st.columns(2)
    with col1:
        if st.button("Generar informe",use_container_width=True):
            st.session_state.informe_nacimientos=False
            df_cria=buscar.ordenar_fecha_df(df_cria)
           
            informe=buscar.informe_crias(df_cria,filtros,df_ganado_puro)
            texto="En este informe se muestran todas las crias nacidas a partir de la fecha: "+informe[0].strftime("%d/%m/%Y")+"\n"+ "cantidad de animales: "+str(len(informe[1]))
            nombre_pdf = ("Informe_Nacimientos")
            informe=buscar.ordenar_fecha_df(informe[1])
            generar_informe.generar_pdf( texto,informe,nombre_pdf)
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):     
                    st.rerun()
#aplicacion 3
if st.session_state.informe_vacas:
    id_vacas=[]
    for i in range(len(df_animal)):
        id_vacas.append(df_animal.iloc[i,0]) 
    id_vaca = st.selectbox("Vaca",id_vacas)
    col1, col2= st.columns(2)
    with col1:
        if st.button("Generar informe",use_container_width=True):
            st.session_state.informe_vacas=False
            df=buscar.informe_crias_v(df_cria,id_vaca)
            informacion=buscar.informacion("VACA",df[0],df[1])
            nombre_pdf = ("Informe_Vaca_"+ str(informacion[2].replace("/", "_")))
            generar_informe.generar_pdf(informacion[0],informacion[1],nombre_pdf)
           
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):
                    st.rerun()
#aplicacio 4
if st.session_state.registros:
    df_ganado_puro=df_ganado_puro[df_ganado_puro.iloc[:,3]!="pendiente"]
    registro=[]
    for i in df_ganado_puro.iloc[:,0]:
        registro.append(i)
    filtro = st.selectbox("Animal",registro)
    posicion=registro.index(filtro)
    filtrado=df_ganado_puro.iloc[posicion]["REGISTRO"]
    
    if st.button("BUSCAR REGISTRO",use_container_width=True):
        st.session_state.registros=False
        nombre_bucket ="REGISTROS"
        ruta_en_storage =filtrado.upper()+".pdf"
        pdf_bytes=supabase.storage.from_(nombre_bucket).download(ruta_en_storage)
        with open(ruta_en_storage, "wb") as f:
            f.write(pdf_bytes)
        if st.download_button("Descargar PDF",pdf_bytes,file_name=ruta_en_storage,mime="application/pdf",use_container_width=True):
            st.rerun()          
#aplicacion 5
if st.session_state.modificar_df:

    df_animal=pd.DataFrame(supabase.table("ANIMAL").select("*").execute().data)
    df_partos=pd.DataFrame(supabase.table("PARTOS").select("*").execute().data)
    df_partos=df_partos.drop(columns=["index"])
    df_cria=pd.DataFrame(supabase.table("CRIA").select("*").execute().data)
    df_cria=df_cria.drop(columns=["index"])
    df_embriones=pd.DataFrame(supabase.table("EMBRIONES").select("*").execute().data)
    df_embriones=df_embriones.drop(columns=["index"])
    df_inseminacion=pd.DataFrame(supabase.table("INSEMINACION").select("*").execute().data)
    df_inseminacion=df_inseminacion.drop(columns=["index"])
    df_fincas=pd.DataFrame(supabase.table("FINCAS").select("*").execute().data)
    df_fincas=df_fincas.drop(columns=["index"])
    df_razas=pd.DataFrame(supabase.table("RAZAS").select("*").execute().data)
    df_ganado_puro=pd.DataFrame(supabase.table("GANADO_PURO").select("*").execute().data)
    df_ganado_puro=df_ganado_puro.drop(columns=["index"])
    df_servicios=pd.DataFrame(supabase.table("SERVICIO").select("*").execute().data)
    df_servicios=df_servicios.drop(columns=["index"])
    df_protocolo=pd.DataFrame(supabase.table("PROTOCOLO").select("*").execute().data)
    df_protocolo=df_protocolo.drop(columns=["index"])
    df_protocolo=df_protocolo[df_protocolo["PROTOCOLO"]=="pendiente"]
    
    fecha_actual=datetime.now()
    dias=[]
    for i in range(len(df_protocolo)):
        dias.append((fecha_actual-pd.to_datetime(df_protocolo.iloc[i]["FECHA_PARTO"])).days)
    df_protocolo["DIAS DE PARIDA"]=dias






    dato=st.selectbox("Base_Datos",["ANIMAL","PARTOS","CRIAS","EMBRIONES","INSEMINACION","FINCAS","RAZAS","GANADO PURO","REPORTE SERVICIOS","PROTOCOLO REPRODUCCION"])
    if dato =="ANIMAL":
        df_animal=st.data_editor(df_animal,num_rows="dynamic")
    elif dato =="PARTOS":
        df_partos=st.data_editor(df_partos,num_rows="dynamic")
    elif dato =="CRIAS":
        df_cria=st.data_editor(df_cria,num_rows="dynamic")
    elif dato =="EMBRIONES":
        df_embriones=st.data_editor(df_embriones,num_rows="dynamic")
    elif dato =="INSEMINACION":
        df_inseminacion=st.data_editor(df_inseminacion,num_rows="dynamic")
    elif dato =="FINCAS":
        df_fincas=st.data_editor(df_fincas,num_rows="dynamic")
    elif dato =="RAZAS":
        df_razas=st.data_editor(df_razas,num_rows="dynamic")
    elif dato =="GANADO PURO":
        df_ganado_puro=st.data_editor(df_ganado_puro,num_rows="dynamic")
    elif dato =="REPORTE SERVICIOS":
        df_servicios=st.data_editor(df_servicios,num_rows="dynamic")
    elif dato =="PROTOCOLO REPRODUCCION":
        df_protocolo=st.data_editor(df_protocolo,num_rows="dynamic")

    if st.button("GUARDAR CAMBIOS",use_container_width=True):
        df_protocolo=df_protocolo.drop(columns=["DIAS DE PARIDA"])
        nacimientos.guardar(df_inseminacion,df_animal,df_partos,df_cria,df_embriones,df_fincas,df_razas,df_ganado_puro,df_servicios,df_protocolo)
        time.sleep(1)
        st.success("Guardado correctamente")
        st.session_state.modificar_df=False
        st.rerun()
#aplicacion 6
if st.session_state.informe_embriones:
    fecha=st.date_input("A partir de que fecha desea el informe")
    finca=st.multiselect("finca",df_fincas)
    compania=st.multiselect("Compañia",df_embriones["COMPANIA"].unique())
    x1=st.multiselect("X1",df_embriones["X1"].unique())
    x3=st.multiselect("X3",df_embriones["X3"].unique())
    raza=st.multiselect("raza",df_embriones["RAZA"].unique())
    if st.button("Generar informe",use_container_width=True):
        st.session_state.informe_embriones=False
        informe=Buscador.informe_embriones(df_embriones,raza,fecha,finca,compania,x1,x3)
        
        texto="En este informe se muestran todos los procesos de embrion a partir de la fecha: "+str(fecha.strftime("%d/%m/%Y"))
        nombre_pdf = ("Informe_Embriones")
        generar_informe.generar_pdf(texto,informe,nombre_pdf)
        with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
        if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):
            st.rerun()     
#aplicacion 7       
if st.session_state.informe_ganado_puro:
    fecha=st.date_input("A partir de que fecha desea el informe")
    finca=st.multiselect("finca",df_fincas)
    raza=st.multiselect("raza",df_ganado_puro["RAZA"].unique())
    if st.button("Generar informe",use_container_width=True):
        
        st.session_state.informe_embriones=False
        informe=Buscador.informe_embriones(df_ganado_puro,raza,fecha,finca,"compania","x1","x3")
        informe=buscar.ordenar_fecha_df(informe)
        texto="En este informe se muestran todos los animales puros nacidos apartir de la fecha: "+str(fecha.strftime("%d/%m/%Y"))
        nombre_pdf = ("Informe_Ganado_Puro")
        generar_informe.generar_pdf(texto,informe,nombre_pdf)
        with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
        if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):
            st.rerun()     
#graficos
if st.session_state.graficos:
    st.markdown(
    """
    <style>
    .titulo-ganaderia {
        background-color: rgba(0, 0, 0, 0.5); /* Fondo negro 80% opacidad */
        color: white;                        /* Texto blanco */
        text-align: center;                  /* Centra el texto */
        font-family: sans-serif;             /* Letra moderna de Streamlit */
        font-weight: bold;                   /* Texto en negrita */
        padding: 20px;                       /* Espacio interno */
        border-radius: 8px;                  /* Bordes redondeados */
        font-size: 30px;                     /* Tamaño del título */
    }
    </style>
    <div class='titulo-ganaderia'>SEXO DE LAS CRIAS</div>
    """,
    unsafe_allow_html=True
)
    st.markdown("<br>", unsafe_allow_html=True)  
    dfg1=df_cria
    filtro_finca=st.multiselect("FINCA",df_fincas)    
   
    filtro_año=st.multiselect("AÑO",pd.to_datetime(dfg1["FECHA_NACIMIENTO"]).dt.year.unique())
    dfg=df_cria
    l1=[]
    for i in range(len(filtro_año)):
        l1.append(dfg[pd.to_datetime(dfg["FECHA_NACIMIENTO"]).dt.year==filtro_año[i]])
    if l1:   
        dfg=pd.concat(l1)
    l2=[]
    for i in range(len(filtro_finca)):
        l2.append(dfg[dfg["FINCA"]==filtro_finca[i]])
    if l2:
        dfg=pd.concat(l2)
    
    sexo=px.pie(dfg,values=dfg["SEXO"].replace({"macho":1,"hembra":1}),
                names="SEXO",title="HAY UN TOTAL DE "+str(len(dfg))+" ANIMALES",hole=0.3,color_discrete_sequence=px.colors.qualitative.Set1)
    sexo.update_traces(texttemplate="<br>%{value}<br>%{percent:.0%}", textfont_size=25,
                  marker=dict( line=dict(color="#FFFFFF", width=2)),textfont=dict(color="white")) 
    sexo.update_layout(legend=dict(font=dict(size=25)))
    sexo.update_layout(title={"x":0.38,"xanchor":"center"})
    st.plotly_chart(sexo,use_container_width=True,config={"displayModeBar": False,"staticPlot": True})

# grafico de barras
    meses_espanol={1:"ENERO",2:"FEBRERO",3:"MARZO",4:"ABRIL",
                   5:"MAYO",6:"JUNIO",7:"JULIO",8:"AGOSTO",
                   9:"SEPTIEMBRE",10:"OCTUBRE",11:"NOVIEMBRE",12:"DICIEMBRE"}
    dfg3=pd.DataFrame(columns=["MES","CANTIDAD","AÑO"])
    contar=0
    for i in (pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.month.unique()): 
        for j in (pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year.unique()):
            dfg3.loc[contar]=[meses_espanol[i],
                  len(df_cria[(pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.month==i)&(pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year==j)])
                  ,str(j)]
            contar+=1  
   
    nacimientos = px.bar(dfg3,x="MES",y="CANTIDAD",color="AÑO",title="HISTORIAL NACIMIENTOS",color_discrete_sequence=px.colors.qualitative.Set1)
    nacimientos.update_layout(title={"x":0.5,"xanchor":"center"})
    nacimientos.update_traces(texttemplate="%{value}",textangle=0,marker=dict(line=dict(color="#FFFFFF", width=2)),textfont=dict(color="white",size=25), insidetextanchor="middle")
    nacimientos.update_layout(uniformtext_minsize=15, height=600,uniformtext_mode='show')
    nacimientos.update_layout(legend=dict(font=dict(size=15)))
    nacimientos.update_layout(xaxis=dict(tickfont=dict(size=15)))
    nacimientos.update_yaxes( title_font=dict(size=15),showticklabels=False,showgrid=True,visible=True)
    st.plotly_chart(nacimientos, use_container_width=True,config={"displayModeBar": False,"staticPlot": True})

#  recuento nacimientos
    
    contar=0
    mes_filtrado=st.multiselect("MES",dfg3["MES"].unique())
    meses_a_numeros = {
    'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4,
    'MAYO': 5, 'JUNIO': 6, 'JULIO': 7, 'AGOSTO': 8,
    'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
}
    numeros = [meses_a_numeros[mes] for mes in mes_filtrado]
    dfg4=df_cria
    l3=[]
    for i in range(len(mes_filtrado)):
        l3.append(dfg4[pd.to_datetime(dfg4["FECHA_NACIMIENTO"]).dt.month==numeros[i]])
    if l3:
        dfg4=pd.concat(l3)

    dfg5=pd.DataFrame(columns=["FINCA","CANTIDAD","AÑO"])
    for i in (dfg4["FINCA"].unique()):
        for j in (pd.to_datetime(dfg4["FECHA_NACIMIENTO"]).dt.year.unique()):
            dfg5.loc[contar]=[i,
                  len(dfg4[(dfg4["FINCA"]==i)&(pd.to_datetime(dfg4["FECHA_NACIMIENTO"]).dt.year==j)])
                  ,str(j)]
            contar+=1
   
    
    recuento_nacimientos = px.bar(dfg5,x="FINCA",y="CANTIDAD",color="AÑO",barmode="group",title="RECUENTO NACIMIENTOS POR MES",color_discrete_sequence=px.colors.qualitative.Set1)
    recuento_nacimientos.update_layout(title={"x":0.5,"xanchor":"center"})
    recuento_nacimientos.update_traces(texttemplate="%{value}",textangle=0,marker=dict(line=dict(color="#FFFFFF", width=2)),textfont=dict(color="white",size=25), insidetextanchor="middle")
    recuento_nacimientos.update_layout(uniformtext_minsize=15,uniformtext_mode='show')
    recuento_nacimientos.update_layout(legend=dict(font=dict(size=15)))
    recuento_nacimientos.update_layout(xaxis=dict(tickfont=dict(size=15)))
    recuento_nacimientos.update_yaxes( title_font=dict(size=15),showticklabels=False,showgrid=True,visible=True)
    st.plotly_chart(recuento_nacimientos, use_container_width=True,config={"displayModeBar": False,"staticPlot": True})
    
if st.session_state.tiempo_inseminacion:
    if st.button("Generar informe",use_container_width=True):
        st.session_state.tiempo_inseminacion=False
        informe=Buscador.palpacion_inseminacion(df_inseminacion)
        texto="En este informe se muestran todos las vacas inseminadas pendientes por palpacion\n"+"Cantidad de animales: "+str(informe[1])
        nombre_pdf = ("Informe_Timpo_inseminacion")
        generar_informe.generar_pdf(texto,informe[0],nombre_pdf)
        with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
        if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):
            st.rerun()  
    
#   py -3.12 -m streamlit run app.py