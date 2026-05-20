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

#Botones 

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

if st.button("Inicio",use_container_width=True):
    st.session_state.registro_crias=False
    st.session_state.informe_nacimientos= False
    st.session_state.informe_vacas = False
    st.session_state.modificar_df = False
    st.session_state.registros=False

col1, col2, col3 ,col4,col5= st.columns(5)     

with col1:
    if st.button("REGISTRO NACIMIENTOS",use_container_width=True): 
        st.session_state.registro_crias=True
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False

#      BOTON 2
with col2:
    if st.button("INFORME NACIMIENTOS",use_container_width=True):
        st.session_state.informe_nacimientos= True
        st.session_state.registro_crias=False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False

#      BOTON 3 
with col3:
    if st.button("INFORME VACAS",use_container_width=True):
        st.session_state.informe_vacas = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.modificar_df = False
        st.session_state.registros=False
with col4:
    if st.button("AÑADIR REGISTRO",use_container_width=True):
        st.session_state.modificar_df = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.registros=False

with col5:
    if st.button("REGISTROS",use_container_width=True):
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=True

    


#//FORMULARIOS//que ejecutan los formularios
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def prueba():

    try:
        wait = WebDriverWait(driver, 20)

        options = Options()

        options.binary_location = "/usr/bin/chromium"

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")

        st.write("antes driver")

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

        st.write("driver iniciado")

        driver.get("https://google.com")

        st.write(driver.title)

        driver.quit()

    except Exception as e:

        st.write("ERROR:")
        st.write(str(e))
    st.write("1")

    driver.get("https://sir.asocebu.com.co/Genealogias/")

    st.write("2")

    input_texto = wait.until(
        EC.presence_of_element_located(
        (By.XPATH, '//input[@formcontrolname="Registro"]')
    )
)

    st.write("3")

    input_texto.send_keys(registro)

    st.write("4")

    boton = wait.until(
        EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(),"Consultar")]')
    )
)

    st.write("5")

    boton.click()

    st.write("6")


prueba()
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
    finca = st.selectbox("Finca",fincas)
    tc=st.selectbox("Tipo_concepcion",["TE","CN","IA","incluir todos"])
    fecha=pd.to_datetime(fecha,format="%d/%m/%Y")
    filtros=[fecha,finca,tc]
    col1, col2= st.columns(2)
    with col1:
        if st.button("Generar informe",use_container_width=True):
            st.session_state.informe_nacimientos=False
            df_cria=buscar.ordenar_fecha_df(df_cria)
            informe=buscar.informe_crias(df_cria,filtros)
            texto="En este informe se muestran todas las crias nacidas a partir de la fecha: "+informe[0].strftime("%d/%m/%Y")+"\n"+ "cantidad de animales: "+str(len(informe[1]))
            nombre_pdf = ("Informe_Nacimientos")
            generar_informe.generar_pdf( texto,informe[1],nombre_pdf)
            with open(nombre_pdf + ".pdf", "rb") as file:pdf_bytes = file.read()
            with col2:
                if st.download_button("Descargar PDF",pdf_bytes,file_name=nombre_pdf + ".pdf",mime="application/pdf",use_container_width=True):     
                    st.rerun()

#aplicacion 3
if st.session_state.informe_vacas:
    id_vacas=[]
    for i in range(len(df_Animal)):
        id_vacas.append(df_Animal.iloc[i,0]) 
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

if st.session_state.modificar_df:
    modificar=[]

    for i in range(len(df_ganado_puro)):
        b=""
        contador=0
        for j in df_ganado_puro.iloc[i]:       
            if contador<(len(df_ganado_puro.iloc[i])):
                b=b+" | "+df_ganado_puro.columns[contador]+": "+str(j)
            contador+=1

        modificar.append(b)
    filtro = st.selectbox("Animal",modificar)
    id_animal = st.text_input("ID nuevo").lower()
    registro = st.text_input("Registro nuevo").lower()
    if st.button("Guardar",use_container_width=True):
        posicion=modificar.index(filtro)
        df_ganado_puro=buscar.modificar_df(df_ganado_puro,id_animal,registro,posicion)
        nacimientos.guardar()   
        st.success("Guardado") 
        st.session_state.modificar_df=False
        st.rerun()

        
            
        
        
   

    

    #df_ganado_puro=buscar.modificar_df(df_ganado_puro)

if st.session_state.registros:
    df_ganado_puro=df_ganado_puro[df_ganado_puro.iloc[:,3]!="pendiente"]
    registro=[]
    for i in df_ganado_puro.iloc[:,0]:
        registro.append(i)
    filtro = st.selectbox("Animal",registro)
    posicion=registro.index(filtro)
    filtrado=df_ganado_puro.iloc[posicion]["REGISTRO"]
    if st.button("BUSCAR REGISTRO",use_container_width=True):
        registros(filtrado)
        st.session_state.registros=False






#   py -m streamlit run app.py