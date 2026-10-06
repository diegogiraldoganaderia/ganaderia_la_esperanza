import streamlit as st
import base64
from Ganaderia import *
import os
import time
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from supabase import create_client



#objetos
buscar = Buscador()
nacimientos = Agregar_Eliminar()
generar_informe=Informes()

 
#logo
with open("logo.png", "rb") as image_file:
        logo = base64.b64encode(image_file.read()).decode()




st.markdown(f"""
<style>
.titulo-ganaderia {{
   
    color: white;
    text-align: ijust;
    display: flex;
    align-items: ijust;
    justify-content: center;
    gap: 5px;
    padding: 0px;
    border-radius: 2px;
    font-family: sans-serif;
    font-weight: bold;
    font-size: 1px;
    margin-bottom: -150px;

}}

.logo {{
    width: 1080px;      /* Cambia el tamaño del logo */
    height: 500px;
}}
</style>
<div class="titulo-ganaderia">
    <img class="logo" src="data:image/png;base64,{logo}">
</div>

""", unsafe_allow_html=True)
 
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
#fondo
set_local_bg(r"fondo.png")
#logo


#menú
st.header("MENÚ")

#FORMULARIOS GENERALES CERRADOS
if "informes" not in st.session_state:
    st.session_state.informes = False

if "reproduccion_produccion" not in st.session_state:
    st.session_state.reproduccion_produccion = False
if "registros" not in st.session_state:
    st.session_state.registros = False

#FORMULARIOS CERRADOS
if "buscar_registros" not in st.session_state:
    st.session_state.buscar_registros = False

if "registro_nacimientos" not in st.session_state:
    st.session_state.registro_nacimientos = False

if "informe_nacimientos" not in st.session_state:
    st.session_state.informe_nacimientos = False

if "informe_vacas" not in st.session_state:
    st.session_state.informe_vacas = False
if "informe_toros" not in st.session_state:
    st.session_state.informe_toros = False

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

if "palpacion" not in st.session_state:
    st.session_state.palpacion=False

if "informe_receptoras" not in st.session_state:
    st.session_state.informe_receptoras=False

def cerrar(x):
    
    if x==1:
        st.session_state.informes = True
    else:
        st.session_state.informes = False

    if x==2:
        st.session_state.informe_nacimientos = True
    else:
        st.session_state.informe_nacimientos = False
    if x==3:
        st.session_state.informe_vacas = True
    else:
        st.session_state.informe_vacas= False
    if x==4:
        st.session_state.informe_toros = True
    else:
        st.session_state.informe_toros= False
    if x==5:
        st.session_state.informe_embriones=True
    else:
        st.session_state.informe_embriones=False  
   
    if x==6:
        st.session_state.informe_ganado_puro = True
    else:
        st.session_state.informe_ganado_puro= False
   

    if x==7:
        st.session_state.reproduccion_produccion = True
    else:
        st.session_state.reproduccion_produccion = False

    if x==8:
        st.session_state.registro_nacimientos=True
    else:
        st.session_state.registro_nacimientos=False

    if x==9:
        st.session_state.tiempo_inseminacion=True
    else:
        st.session_state.tiempo_inseminacion=False

    if x==10:
        st.session_state.palpacion=True
    else:
        st.session_state.palpacion=False
    if x==11:
        st.session_state.registros=True
    else:
        st.session_state.registros=False
    if x==12:
        st.session_state.subir_pdf_registro=True
    else:
        st.session_state.subir_pdf_registro=False

    if x==13:
        st.session_state.buscar_registros=True
    else:
        st.session_state.buscar_registros=False

    if x==14:
        st.session_state.modificar_df = True
    else:
        st.session_state.modificar_df = False

    if x==15:
        st.session_state.graficos=True
    else:
        st.session_state.graficos=False

    if x==16:
        st.session_state.informe_receptoras=True
    else:
        st.session_state.informe_receptoras=False
    
#Botones
st.html("""
<style>

/* =========================
   ESTILO 1 - PRINCIPAL
   ========================= */

button[kind="primary"] {
    width: 100%;
    height: 72px !important;

    background: linear-gradient(
        90deg,
        #5C481F 0%,
        #29251C 8%,
        #15181B 100%
    ) !important;

    color: #F2E8D0 !important;

    border: 1px solid #806A35 !important;
    border-radius: 14px !important;
    
    font-size: 20px !important;
    font-weight: 1000 !important;
    letter-spacing: 0.8px;

    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}


/* =========================
   ESTILO 2 - SECUNDARIO
   ========================= */

button[kind="secondary"] {
    width: 100%;
    height: 72px !important;

    background: linear-gradient(
        90deg,
        #5C481F 0%,
        #29258C 8%,
        #15181B 100%
    ) !important;

    color: #F2E8D0 !important;

    border: 1px solid white !important;
    border-radius: 14px !important;

    font-size: 20px !important;
    font-weight: 1000 !important;

    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}
button[kind="tertiary"] {
    width: 100%;
    height: 72px !important;

    background: linear-gradient(
        90deg,
        #4A121A 0%,    /* Vino tinto profundo */
        #2D0B10 40%,   /* Vino tinto más oscuro */
        #150507 100%  
    ) !important;

    color: #F2E8D0 !important;

    border: 1px solid white !important;
    border-radius: 14px !important;

    font-size: 20px !important;
    font-weight: 1000 !important;

    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

</style>
""")

if st.button("🚀  INICIO",use_container_width=True,type="primary"):
   cerrar(0)
   
   

#INICIO INFORMES

if st.button("📋 INFORMES",use_container_width=True,type="primary"):
    cerrar(1)
    
if st.session_state.informes:

    col1, col2, col3= st.columns(3)
    with col1:
        if st.button("INFORME NACIMIENTOS",use_container_width=True):
            cerrar(2)    
    with col2:
        if st.button("INFORME VACAS",use_container_width=True):
            cerrar(3)
    with col3:
        if st.button("INFORME TOROS",use_container_width=True):
            cerrar(4)

    
    with col2:
        if  st.button("INFORME EMBRIONES",use_container_width=True):
            cerrar(5)
    with col3:
        if  st.button("INFORME GANADO PURO",use_container_width=True):
            cerrar(6)
    with col1:
        if  st.button("INFORME RECEPTORAS",use_container_width=True):
            cerrar(16)

if st.session_state.informe_nacimientos:  
    
    fecha=st.date_input("A partir de que fecha desea el informe")
    fincas=[]
    finca = st.multiselect("Finca",df_fincas["ID"])
    tc=st.multiselect("Tipo_concepcion",["TE","CN","IA"])
    fecha=pd.to_datetime(fecha,format="%d/%m/%Y")
    solo_numeros=st.selectbox("SOLO NÚMEROS:",["NO","SI"])

    col1, col2= st.columns(2)
    with col1:

        if st.button("GENERAR INFORME",use_container_width=True,type="tertiary"):
            st.session_state.informe_nacimientos=False
            st.session_state.informes = False
            informe=buscar.numeros(df_cria,df_embriones,df_ganado_puro)
            #filtro la fecha
            informe=informe[pd.to_datetime(informe["FECHA_NACIMIENTO"])>fecha]
            #filtro tc
            filtro_tc=informe["T_C"].isin(tc)
            informe=informe[filtro_tc]
            #filtro_finca
          
            if len(finca) == 1:
                txt = " en la finca " + finca[0]
            else:
                txt = " en las fincas " + ", ".join(finca[:-1]) + " y " + finca[-1]
            
            filtro_finca=informe["FINCA"].isin(finca)
            informe=informe[filtro_finca]
            
            texto=("En este informe se muestran todas las crias nacidas"+
            txt+" a partir de la fecha: "+fecha.strftime("%d/%m/%Y")+"\n"+ "cantidad de animales: "+str(len(informe)))
            nombre_pdf = ("Informe_Nacimientos")

            if solo_numeros=="NO":
                generar_informe.generar_pdf( texto,informe,nombre_pdf)
            elif solo_numeros=="SI":
                informe=informe.iloc[:,[0,3,7,1]]
                generar_informe.generar_pdf( texto,informe,nombre_pdf)

            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True,type="tertiary"):     
                    st.rerun()

if st.session_state.informe_vacas:
    dfve=df_embriones
    id_vaca = st.selectbox("Vaca",df_partos["ID"].unique())
    df_vaca_embriones=buscar.informe_receptoras(dfve)
    df_vaca_embriones=df_vaca_embriones[df_vaca_embriones["RECEPTORA"]==id_vaca]
    df_vaca_servicios=df_servicios[df_servicios["VACA"]==id_vaca]
    df_vaca_inseminacion=df_inseminacion[df_inseminacion["ID"]==id_vaca]

    col1, col2= st.columns(2)
    with col1:
        if st.button("GENERAR INFORME",use_container_width=True,type="tertiary"):
            st.session_state.informe_vacas=False
            st.session_state.informes = False
            #df=buscar.informe_crias_v(df_cria,id_vaca)
            informacion_vaca = df_animal[df_animal["ID"] == id_vaca].iloc[0]
            texto_vaca = ( "La Vaca identificada " + str(id_vaca) +
                          " de la raza " + str(informacion_vaca["RAZA"]) + " " +
                            buscar.calcular_edad(informacion_vaca["FECHA_NACIMIENTO"])
                            )
            informacion_partos=buscar.numeros(df_cria,df_embriones,df_ganado_puro)
            informacion_partos=informacion_partos[informacion_partos["VACA"]==id_vaca]
            nombre_pdf = ("Informe_Vaca_"+ str(id_vaca.replace("/", "_")))
           
            if len(df_vaca_embriones)>0:
                prenez_embriones=df_vaca_embriones["# p+"].values[0]
                protocolos=df_vaca_embriones["#PROTOCOLOS"].values[0]
                
            else:
                prenez_embriones=0
                protocolos=0
            numero_prenez=(prenez_embriones
                           +len(df_vaca_inseminacion[df_vaca_inseminacion["CONFIRMACION"]=="p+"])+
                           len(df_vaca_servicios[df_vaca_servicios["ESTADO"]=="p+"]))
            numero_intentos_prenez=(protocolos+len(df_vaca_inseminacion)
                                            +len(df_vaca_servicios))
                    
            
            if numero_prenez>0:
                texto_preñez=" se requieren "+str(round(numero_intentos_prenez/numero_prenez,2))+" intentos para lograr una preñez"
            else:
                texto_preñez=" no se tienen datos suficientes para determinar cuantos intentos se necesitan para lograr una preñez"

            informe=[informacion_partos,df_vaca_embriones,df_vaca_inseminacion.drop(columns=["ID"]),df_vaca_servicios.iloc[:, 1:]]
            textos=[texto_vaca+texto_preñez+"\nHistorial de partos"
                    ,"Resumen de procesos de embrion","Historial inseminación","Historial de servicios"]
            
            generar_informe.generar_pdf_multiple(textos,informe,nombre_pdf)
           
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True,type="tertiary"):
                    st.rerun()
if st.session_state.informe_toros:
    filtro_toro=st.multiselect("TORO",df_toros)
    df_crias_toro=pd.DataFrame(columns=["TOROS","CANTIDAD DE CRÍAS","MACHOS","HEMBRAS","AÑO"])
    contar=0
    ano=pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year.unique()
    filtro_ano=st.multiselect("AÑO",ano)
    if  not filtro_toro:    
        filtro_toro=df_toros["ID"].to_list()
    for i in (filtro_toro): 
                for j in (filtro_ano):
                    df_crias_toro.loc[contar]=[i.upper(),
                          len(df_cria[(df_cria["TORO"]==i)&(pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year==j)]),
                          len(df_cria[(df_cria["TORO"]==i)&(pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year==j)&(df_cria["SEXO"]=="macho")]),
                          len(df_cria[(df_cria["TORO"]==i)&(pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year==j)&(df_cria["SEXO"]=="hembra")])
                          ,str(j)]
                    contar+=1
    col1, col2= st.columns(2)
    with col1:
        if st.button("GENERAR INFORME",use_container_width=True,type="tertiary"):
            st.session_state.informe_toros=False
            st.session_state.informes = False
            nombre_pdf = ("Informe_Toros")
            texto1="En este informe se muestan las crias del toro"
            texto2="En este informe se muestan las crias de los toros,"
            texto3="en el año"
            texto4="en los años"
            texto_toros=""
            contador_toros=1
            
            if len(filtro_toro)>1:  
                for i in filtro_toro:
                    if contador_toros-len(filtro_toro)==-1:
                        texto_toros+=i+" y "
                    elif contador_toros==len(filtro_toro):
                                            texto_toros+=i
                    else:
                        texto_toros+=i+", "
                    contador_toros+=1
                    
                
                textof=texto2
            else:
                texto_toros=filtro_toro[0]
                textof=texto1
            texto_ano=""
            contador_ano=1
            if len(filtro_ano)>1:
                for j in filtro_ano:
                    if contador_ano-len(filtro_ano)==-1:
                        texto_ano+=str(j)+" y "
                    elif contador_ano==len(filtro_ano):
                        texto_ano+=str(j)
                    else:
                        texto_ano+=str(j)+", "
                    contador_ano+=1
                textos=texto4
            else:
                texto_ano=str(filtro_ano[0])
                textos=texto3
            texto=textof+" "+texto_toros+" "+textos+" "+texto_ano
            generar_informe.generar_pdf(texto,df_crias_toro,nombre_pdf)
               
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True,type="tertiary"):
                    st.rerun()
if st.session_state.informe_ganado_puro:
    
    fecha=st.date_input("A partir de que fecha desea el informe")
    fecha=pd.to_datetime(fecha,format="%d/%m/%Y")
    finca=st.multiselect("finca",df_ganado_puro["FINCA"].unique())
    raza=st.multiselect("raza",df_ganado_puro["RAZA"].unique())
    col1, col2= st.columns(2)
    with col1:
        if st.button("GENERAR INFORME",use_container_width=True,type="tertiary"):
            df=df_ganado_puro
            df=df[pd.to_datetime(df["FECHA_NACIMIENTO"])>=fecha]
        
            filtro_raza=df["RAZA"].isin(raza)
            df=df[filtro_raza]
            filtro_finca=df["FINCA"].isin(finca)
            df=df[filtro_finca]
            st.session_state.informe_ganado_puro=False
            st.session_state.informes = False
            texto="En este informe se muestran todos los animales puros nacidos apartir de la fecha: "+str(fecha.strftime("%d/%m/%Y"))
            nombre_pdf = ("Informe_Ganado_Puro")
            generar_informe.generar_pdf(texto,df,nombre_pdf)
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True,type="tertiary"):
                    st.rerun() 
if st.session_state.informe_embriones:
    fecha=st.selectbox("FECHA SINCRONIZACIÓN Y PROVEEDOR",
                       (df_embriones["FECHA_SINCRONIZACION"]+" // "+
                        df_embriones["PROVEEDOR"].astype(str).str.upper()).unique())
    fecha=fecha[0:10]
    df=df_embriones[df_embriones["FECHA_SINCRONIZACION"]==fecha]
    finca=st.multiselect("FINCA",df["FINCA"].astype(str).str.upper().unique())

    col1, col2= st.columns(2)
    with col1:
        if st.button("GENERAR INFORME",use_container_width=True,type="tertiary"):
            st.session_state.informe_embriones=False
            st.session_state.informes = False
            informe=buscar.informe_embriones(df,fecha,finca)
            texto=("En este informe se muestran todos los procesos de embrion realizados en la la fecha: "+fecha
                    +", se sincronizaron "+informe[1]+" vacas de las cuales hubo un total de "+informe[2]+" vacas preñadas "+
                    "equivalente al "+informe[3]+"%, un total de "+informe[4]+" vacas vacias equivalente al " 
                    +informe[5]+"%, un total de "+informe[6]+" rechazaron el protocolo, equivalente al "+informe[7]+"%"
            )

            nombre_pdf = ("Informe_Embriones")
            generar_informe.generar_pdf(texto,informe[0],nombre_pdf)
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True,type="tertiary"):
                    st.rerun() 
if st.session_state.informe_receptoras:
    df=df_embriones
    finca=st.multiselect("FINCA",df["FINCA"].astype(str).str.upper().unique())
    finca = [texto.lower() for texto in finca] #se convirten los datos  aminuscula
    filtro_finca=df["FINCA"].isin(finca)
    df1=df[filtro_finca]
    receptora=st.multiselect("RECEPTORA",df1["RECEPTORA"].unique())
    col1, col2= st.columns(2)
    with col1:
        if st.button("GENERAR INFORME",use_container_width=True,type="tertiary"):
            st.session_state.informe_receptoras=False
            st.session_state.informes = False
            informe=buscar.informe_receptoras(df)
            filtro_finca=informe["FINCA"].isin(finca)
            informe=informe[filtro_finca]
            if not receptora:
                informe=informe
            else:
                filtro_receptora=informe["RECEPTORA"].isin(receptora)
                informe=informe[filtro_receptora]
            
            texto=("Se muestran todas las receptoras que hay en la ganadería\n"
                   "p+: Preñada\n v: Vacia\n rp: No respondío al protocolo"
            )
            nombre_pdf=("informe_receptoras")
            generar_informe.generar_pdf(texto,informe,nombre_pdf)
            
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("DESCARGAR PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True,type="tertiary"):
                    st.rerun()           
#FINAL INFORMES
#-------------------------------------------------------------------------
#INICIO REPRODUCCIÓN Y PRODUCIÓN

if st.button("🤰🐄  REPRODUCCIÓN Y PRODUCCIÓN",use_container_width=True,type="primary"):
    cerrar(7)   
if st.session_state.reproduccion_produccion:

    col1, col2, col3= st.columns(3)
    with col1:
        if st.button("REGISTRO NACIMIENTOS",use_container_width=True): 
           cerrar(8)
    with col2:
        if st.button("INSEMINACION",use_container_width=True):
            cerrar(9)
    with col3:
        if st.button("PALPACION",use_container_width=True):
            cerrar(10)
if st.session_state.registro_nacimientos: 
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
        nacimientos.guardar(registro_cria)
        if st.success("Guardado"):
            cerrar(0)
            st.rerun()
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

#FINAL REPRODUCCIÓN Y PRODUCCIÓN
#-------------------------------------------------------------------------
#INICIO REGISTROS

if st.button("🧬🐂  REGISTRO DE ANIMALES",use_container_width=True,type="primary"):
    cerrar(11)

if st.session_state.registros:  
    col1, col2= st.columns(2)
    with col1:
        if st.button("AÑADIR REGISTROS",use_container_width=True):
            cerrar(12)
    with col2:
        if st.button("BUSCAR REGISTROS",use_container_width=True):
            cerrar(13)
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
if st.session_state.buscar_registros:
    df_ganado_puro=df_ganado_puro[df_ganado_puro.iloc[:,3]!="pendiente"]
    registro=[]
    for i in df_ganado_puro.iloc[:,0]:
        registro.append(i)
    filtro = st.selectbox("Animal",registro)
    posicion=registro.index(filtro)
    filtrado=df_ganado_puro.iloc[posicion]["REGISTRO"]
    
    if st.button("BUSCAR REGISTRO",use_container_width=True):
        st.session_state.buscar_registros=False
        nombre_bucket ="REGISTROS"
        ruta_en_storage =filtrado.upper()+".pdf"
        pdf_bytes=supabase.storage.from_(nombre_bucket).download(ruta_en_storage)
        with open(ruta_en_storage, "wb") as f:
            f.write(pdf_bytes)
        if st.download_button("Descargar PDF",pdf_bytes,file_name=ruta_en_storage,mime="application/pdf",use_container_width=True):
            st.rerun()  

#FINAL REGISTROS
#------------------------------------------------------------------------
#INICIO MODIFICAR BASE DE DATOS

if st.button("🗃️ MODIFICAR BASE DATOS",use_container_width=True,type="primary"):
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
    df_toros=pd.DataFrame(supabase.table("TORO").select("*").execute().data)
    df_razas=pd.DataFrame(supabase.table("RAZAS").select("*").execute().data)
    df_ganado_puro=pd.DataFrame(supabase.table("GANADO_PURO").select("*").execute().data)
    df_ganado_puro=df_ganado_puro.drop(columns=["index"])
    df_servicios=pd.DataFrame(supabase.table("SERVICIO").select("*").execute().data)
    df_servicios=df_servicios.drop(columns=["index"])
    df_protocolo=pd.DataFrame(supabase.table("PROTOCOLO").select("*").execute().data)
    df_protocolo=df_protocolo.drop(columns=["index"])
    df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])
    df_informe_vaca=pd.DataFrame(columns=["INFORME"])
    
    cerrar(14) 
    

if st.session_state.modificar_df:
    dataframes_guardar = []
    dato=st.selectbox("Base_Datos",["ANIMAL","PARTOS","CRIAS","EMBRIONES"
    ,"INSEMINACION","FINCAS","RAZAS","GANADO PURO"
    ,"REPORTE SERVICIOS","PROTOCOLO REPRODUCCION"])
    if dato == "ANIMAL":
        df_animal = st.data_editor(
        df_animal,
        num_rows="dynamic",
        key="editor_animal")
        dataframes_guardar.append(("ANIMAL", df_animal))

    elif dato == "PARTOS":
        df_partos = st.data_editor(
            df_partos,
            num_rows="dynamic",
            key="editor_partos"
        )
        dataframes_guardar.append(("PARTOS", df_partos))

    elif dato == "CRIAS":
        df_cria = st.data_editor(
            df_cria,
            num_rows="dynamic",
            key="editor_cria"
        )
        dataframes_guardar.append(("CRIA", df_cria))

    elif dato == "EMBRIONES":
        df_embriones = st.data_editor(
            df_embriones,
            num_rows="dynamic",
            key="editor_embriones"
        )
        dataframes_guardar.append(("EMBRIONES", df_embriones))

    elif dato == "INSEMINACION":
        df_inseminacion = st.data_editor(
            df_inseminacion,
            num_rows="dynamic",
            key="editor_inseminacion"
        )
        dataframes_guardar.append(("INSEMINACION", df_inseminacion))

    elif dato == "FINCAS":
        df_fincas = st.data_editor(
            df_fincas,
            num_rows="dynamic",
            key="editor_fincas"
        )
        dataframes_guardar.append(("FINCAS", df_fincas))

    elif dato == "RAZAS":
        df_razas = st.data_editor(
            df_razas,
            num_rows="dynamic",
            key="editor_razas"
        )
        dataframes_guardar.append(("RAZAS", df_razas))

    elif dato == "GANADO PURO":
        df_ganado_puro = st.data_editor(
            df_ganado_puro,
            num_rows="dynamic",
            key="editor_ganado_puro"
        )
        dataframes_guardar.append(("GANADO_PURO", df_ganado_puro))

    elif dato == "REPORTE SERVICIOS":
        df_servicios = st.data_editor(
            df_servicios,
            num_rows="dynamic",
            key="editor_servicios"
        )
        dataframes_guardar.append(("SERVICIO", df_servicios))

    elif dato == "PROTOCOLO REPRODUCCION":
        df_protocolo = st.data_editor(
            df_protocolo,
            num_rows="dynamic",
            key="editor_protocolo"
        )
        dataframes_guardar.append(("PROTOCOLO", df_protocolo))
    if st.button("GUARDAR CAMBIOS", use_container_width=True):

        if dataframes_guardar:

            nacimientos.guardar(dataframes_guardar)

            if st.success("Guardado correctamente"):
                cerrar(0)
                st.rerun()

            

        #FINAL MODIFICAR BASE DE DATOS
#------------------------------------------------------------------------
#INICO GRACIFICOS
if st.button("📊   GRÁFICOS",use_container_width=True,type="primary"):
    cerrar(15)
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
    
     margin-bottom: 40px;
     }
    </style>
    <div class='titulo-ganaderia'>SEXO DE LAS CRIAS</div>
    """,
    unsafe_allow_html=True
)
    #st.markdown("<br>", unsafe_allow_html=True)  
    dfg1=df_cria
    filtro_finca=st.multiselect("FINCA",df_fincas)    
    ano=pd.to_datetime(dfg1["FECHA_NACIMIENTO"]).dt.year.unique()
    filtro_año=st.multiselect("AÑO",ano)
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
            dfg5.loc[contar]=[i.upper(),
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

    #crias por toro
    
    #filtro_finca=st.multiselect("FINCA",df_fincas)
    #filtro_ano_crias_toro=st.multiselect("AÑO ",ano)
    filtro_toro=st.multiselect("TORO",df_toros)
    df_crias_toro=pd.DataFrame(columns=["TOROS","CANTIDAD DE CRÍAS","AÑO"])
    contar=0
    if  not filtro_toro:
        
        filtro_toro=df_toros["ID"].to_list()
    for i in (filtro_toro): 
            for j in (ano):
                df_crias_toro.loc[contar]=[i.upper(),
                      len(df_cria[(df_cria["TORO"]==i)&(pd.to_datetime(df_cria["FECHA_NACIMIENTO"]).dt.year==j)])
                      ,str(j)]
                contar+=1

    #grfico de crias por toro
    recuento_crias_toro= px.bar(df_crias_toro,x="TOROS",y="CANTIDAD DE CRÍAS",color="AÑO",barmode="group",title="RECUENTO CRIAS POR TORO",color_discrete_sequence=px.colors.qualitative.Set1)
    recuento_crias_toro.update_layout(title={"x":0.5,"xanchor":"center"})
    recuento_crias_toro.update_traces(texttemplate="%{value}",textangle=0,marker=dict(line=dict(color="#FFFFFF", width=2)),textfont=dict(color="white",size=25), insidetextanchor="middle")
    recuento_crias_toro.update_layout(uniformtext_minsize=15,uniformtext_mode='show')
    recuento_crias_toro.update_layout(legend=dict(font=dict(size=15)))
    recuento_crias_toro.update_layout(xaxis=dict(tickfont=dict(size=15)))
    recuento_crias_toro.update_yaxes( title_font=dict(size=15),showticklabels=False,showgrid=True,visible=True)
    st.plotly_chart(recuento_crias_toro, use_container_width=True,config={"displayModeBar": False,"staticPlot": True})    
    
#FINAL GRAFICOS 
    
# FINAL DEL CÓDIGO
#------------------------------------------------------------------------

#   py -3.12 -m streamlit run app.py


