import streamlit as st
import base64
from Ganaderia import *
import os
import time
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
os.system ("cls")
df_animal=pd.read_excel("DATA.xlsx",sheet_name=0)
df_partos=pd.read_excel("DATA.xlsx",sheet_name=1)
df_cria=pd.read_excel("DATA.xlsx",sheet_name=2)
df_embriones=pd.read_excel("DATA.xlsx",sheet_name=3)
df_inseminacion=pd.read_excel("DATA.xlsx",sheet_name=4)
df_fincas=pd.read_excel("DATA.xlsx",sheet_name=5)
df_razas=pd.read_excel("DATA.xlsx",sheet_name=6)
df_ganado_puro=pd.read_excel("DATA.xlsx",sheet_name=7)
df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])
df_informe_vaca=pd.DataFrame(columns=["INFORME"])

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
#objetos
buscar = Buscador()
nacimientos = Agregar_Eliminar()
generar_informe=Informes()


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

if "graficos" not in st.session_state:
    st.session_state.graficos=False
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
with col1:
    if st.button("MODIFICAR DATOS",use_container_width=True):
        st.session_state.modificar_df = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
        st.session_state.graficos=False

with col2:
    if st.button("REGISTROS",use_container_width=True):
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=True
        st.session_state.subir_pdf_registro=False
        st.session_state.graficos=False

with col3:
    if st.button("AÑADIR REGISTROS",use_container_width=True):
        st.session_state.subir_pdf_registro=True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.graficos=False
      
    #   BOTON 5
if st.button("GRÁFICOS",use_container_width=True):
    st.session_state.graficos=True
    st.session_state.registro_crias=False
    st.session_state.informe_nacimientos= False
    st.session_state.informe_vacas = False
    st.session_state.modificar_df = False
    st.session_state.registros=False
    st.session_state.subir_pdf_registro=False
#boton 6
#//FORMULARIOS// QUE HACEN LOS BOTONES
if st.session_state.subir_pdf_registro:
    st.title("Subir PDF a carpeta")
# Carpeta destino
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "registros")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    archivo = st.file_uploader("Sube PDF", type=["pdf"])
    if archivo:
        ruta_guardado = os.path.join(UPLOAD_FOLDER, archivo.name)
        with open(ruta_guardado, "wb") as f:
            f.write(archivo.getbuffer())
        if st.success("Guardado correctamente"):
            st.session_state.subir_pdf_registro=False
            st.rerun()
#aplicacion 1
if st.session_state.registro_crias: 
    vaca = st.text_input("ID de la vaca").lower()
    fn = st.date_input("Fecha nacimiento")
    sexo = st.selectbox("Sexo",["macho", "hembra"])
    fincas=[]
    for i in range(len(df_fincas)):
        fincas.append(df_fincas.iloc[i,0]) 
    finca = st.selectbox("Finca",fincas)
    toro = st.text_input("Toro")
    razas=[]
    for i in range(len(df_razas)):
        razas.append(df_razas.iloc[i,0]) 
    raza = st.selectbox("Raza",razas)
    observaciones = st.text_area("Observaciones")
    
    if st.button("Guardar",use_container_width=True):
        nacimientos.nacimiento(buscar,vaca,fn,sexo,finca,observaciones,toro,raza)
        nacimientos.guardar()
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
            df_ganado_puro=buscar.ordenar_fecha_df(df_ganado_puro)
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
        nombre_pdf=generar_informe.registros(filtrado.upper())
        with open(nombre_pdf, "rb") as file:pdf_bytes = file.read()
        if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):
            st.rerun()


#aplicacion 5
if st.session_state.modificar_df:
    dato=st.selectbox("Base_Datos",["ANIMAL","PARTOS","CRIAS","EMBRIONES","INSEMINACION","FINCAS","RAZAS","GANADO PURO"])
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

    if st.button("GUARDAR CAMBIOS",use_container_width=True):
        st.success("Guardado correctamente")
        with pd.ExcelWriter("DATA.xlsx") as writer:
         df_animal.to_excel(writer,index=False, sheet_name='ANIMAL')
         df_partos.to_excel(writer,index=False, sheet_name='PARTOS')
         df_cria.to_excel(writer,index=False, sheet_name='CRIA')
         df_embriones.to_excel(writer,index=False, sheet_name='EMBRIONES')
         df_inseminacion.to_excel(writer,index=False, sheet_name='INSEMINACION')
         df_fincas.to_excel(writer,index=False, sheet_name='FINCAS')
         df_razas.to_excel(writer,index=False, sheet_name='RAZAS')
         df_ganado_puro.to_excel(writer,index=False, sheet_name='GANADO_PURO')  
        time.sleep(2)
        st.session_state.modificar_df=False
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
    filtro_año=st.multiselect("AÑO",dfg1["FECHA_NACIMIENTO"].dt.year.unique())
    dfg=df_cria
    l1=[]
    for i in range(len(filtro_año)):
        l1.append(dfg[dfg["FECHA_NACIMIENTO"].dt.year==filtro_año[i]])
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
    st.plotly_chart(sexo,use_container_width=True,config={"displayModeBar": False})

# grafico de barras
    meses_espanol={1:"ENERO",2:"FEBRERO",3:"MARZO",4:"ABRIL",
                   5:"MAYO",6:"JUNIO",7:"JULIO",8:"AGOSTO",
                   9:"SEPTIEMBRE",10:"OCTUBRE",11:"NOVIEMBRE",12:"DICIEMBRE"}
    dfg3=pd.DataFrame(columns=["MES","CANTIDAD","AÑO"])
    contar=0
    for i in (df_cria["FECHA_NACIMIENTO"].dt.month.unique()): 
        for j in (df_cria["FECHA_NACIMIENTO"].dt.year.unique()):
            dfg3.loc[contar]=[meses_espanol[i],
                  len(df_cria[(df_cria["FECHA_NACIMIENTO"].dt.month==i)&(df_cria["FECHA_NACIMIENTO"].dt.year==j)])
                  ,str(j)]
            contar+=1  
   
    nacimientos = px.bar(dfg3,x="MES",y="CANTIDAD",color="AÑO",title="HISTORIAL NACIMIENTOS",color_discrete_sequence=px.colors.qualitative.Set1)
    nacimientos.update_layout(title={"x":0.5,"xanchor":"center"})
    nacimientos.update_traces(texttemplate="%{value}",textangle=0,marker=dict(line=dict(color="#FFFFFF", width=2)),textfont=dict(color="white",size=25), insidetextanchor="middle")
    nacimientos.update_layout(uniformtext_minsize=15, height=600,uniformtext_mode='show')
    nacimientos.update_layout(legend=dict(font=dict(size=15)))
    nacimientos.update_layout(xaxis=dict(tickfont=dict(size=15)))
    nacimientos.update_yaxes( title_font=dict(size=15),showticklabels=False,showgrid=True,visible=True)
    st.plotly_chart(nacimientos, use_container_width=True,config={"displayModeBar": False})

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
        l3.append(dfg4[dfg4["FECHA_NACIMIENTO"].dt.month==numeros[i]])
    if l3:
        dfg4=pd.concat(l3)

    dfg5=pd.DataFrame(columns=["FINCA","CANTIDAD","AÑO"])
    for i in (dfg4["FINCA"].unique()):
        for j in (dfg4["FECHA_NACIMIENTO"].dt.year.unique()):
            dfg5.loc[contar]=[i,
                  len(dfg4[(dfg4["FINCA"]==i)&(dfg4["FECHA_NACIMIENTO"].dt.year==j)])
                  ,str(j)]
            contar+=1
   
    
    recuento_nacimientos = px.bar(dfg5,x="FINCA",y="CANTIDAD",color="AÑO",barmode="group",title="RECUENTO NACIMIENTOS POR MES",color_discrete_sequence=px.colors.qualitative.Set1)
    recuento_nacimientos.update_layout(title={"x":0.5,"xanchor":"center"})
    recuento_nacimientos.update_traces(texttemplate="%{value}",textangle=0,marker=dict(line=dict(color="#FFFFFF", width=2)),textfont=dict(color="white",size=25), insidetextanchor="middle")
    recuento_nacimientos.update_layout(uniformtext_minsize=15,uniformtext_mode='show')
    recuento_nacimientos.update_layout(legend=dict(font=dict(size=15)))
    recuento_nacimientos.update_layout(xaxis=dict(tickfont=dict(size=15)))
    recuento_nacimientos.update_yaxes( title_font=dict(size=15),showticklabels=False,showgrid=True,visible=True)
    st.plotly_chart(recuento_nacimientos, use_container_width=True,config={"displayModeBar": False})
    

#   py -m streamlit run app.py