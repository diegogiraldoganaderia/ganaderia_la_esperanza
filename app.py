import streamlit as st
import base64
from Ganaderia import *

import streamlit as st

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


buscar = Buscador()
nacimientos = Agregar_Eliminar()
generar_informe=informes()
#


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

# Reemplaza con la ruta de tu archivo
set_local_bg(r"fondodos.png")



st.header("MENÚ")

#FORMULARIOS CERRADOS

if "registro_crias" not in st.session_state:
    st.session_state.registro_crias = False

if "informe_nacimientos" not in st.session_state:
    st.session_state.informe_nacimientos = False

if "informe_vacas" not in st.session_state:
    st.session_state.informe_vacas = False

#Botones 
col1, col2, col3 ,col4= st.columns(4)
st.html("""
    <style>
    button {
        height: 60px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    </style>
""")
#      BOTON 1
with col1:
    if st.button("REGISTRO NACIMIENTOS",use_container_width=True): 
        st.session_state.registro_crias=True
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
#      BOTON 2
with col2:
    if st.button("INFORME NACIMIENTOS",use_container_width=True):
        st.session_state.informe_nacimientos= True
        st.session_state.registro_crias=False
        st.session_state.informe_vacas = False
#      BOTON 3 
with col3:
    if st.button("INFORME VACAS",use_container_width=True):
        st.session_state.informe_vacas = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
with col4:
    if st.button("Inicio",use_container_width=True):
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False




#aplicacion 1//FORMULARIOS//que ejecutan los formularios



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

#aplicacion 2
if st.session_state.informe_nacimientos:
    
    fecha=st.date_input("A partir de que fecha desea el informe")
    fincas=[]
    for i in range(len(df_fincas)):
        fincas.append(df_fincas.iloc[i,0]) 
    finca = st.selectbox("Finca",fincas)
    tc=st.selectbox("Tipo_concepcion",["TE","CN","IA","incluir todos"])
    fecha=pd.to_datetime(fecha,format="%d/%m/%Y")
    filtros=[fecha,finca,tc]
    col1, col2= st.columns(2)
    with col1:
        if st.button("Generar informe",use_container_width=True):
            df_cria=buscar.ordenar_fecha_df(df_cria)
            informe=buscar.informe_crias(df_cria,filtros)
            texto="En este informe se muestran todas las crias nacidas a partir de la fecha: "+informe[0].strftime("%d/%m/%Y")+"\n"+ "cantidad de animales: "+str(len(informe[1]))
            nombre_pdf = ("Informe_Nacimientos")
            generar_informe.generar_pdf( texto,informe[1],nombre_pdf)
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True)

#aplicacion 3
if st.session_state.informe_vacas:
    id_vacas=[]
    for i in range(len(df_Animal)):
        id_vacas.append(df_Animal.iloc[i,0]) 
    id_vaca = st.selectbox("Vaca",id_vacas)
    col1, col2= st.columns(2)
    with col1:
        if st.button("Generar informe",use_container_width=True):
            df=buscar.informe_crias_v(df_cria,id_vaca)
            informacion=buscar.informacion("VACA",df[0],df[1]) 
            nombre_pdf = ("Informe_Vaca_"+ str(informacion[2].replace("/", "_")))
            generar_informe.generar_pdf(informacion[0],informacion[1],nombre_pdf)
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True)
        







#   py -m streamlit run app.py