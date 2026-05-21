import streamlit as st
import base64
from Ganaderia import *
import os
import time
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
generar_informe=informes()
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

#      BOTON 2
with col2:
    if st.button("INFORME NACIMIENTOS",use_container_width=True):
        st.session_state.informe_nacimientos= True
        st.session_state.registro_crias=False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False

#      BOTON 3 
with col3:
    if st.button("INFORME VACAS",use_container_width=True):
        st.session_state.informe_vacas = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False
with col1:
    if st.button("MODIFICAR DATOS",use_container_width=True):
        st.session_state.modificar_df = True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.registros=False
        st.session_state.subir_pdf_registro=False

with col2:
    if st.button("REGISTROS",use_container_width=True):
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=True
        st.session_state.subir_pdf_registro=False

with col3:
    if st.button("AÑADIR REGISTROS",use_container_width=True):
        st.session_state.subir_pdf_registro=True
        st.session_state.registro_crias=False
        st.session_state.informe_nacimientos= False
        st.session_state.informe_vacas = False
        st.session_state.modificar_df = False
        st.session_state.registros=False
        



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
   
    modificar_que=st.selectbox("Datos",["GANADO PURO","INSEMINACION"])
    if modificar_que=="GANADO PURO":
        modificar=[]
        lista_id=[]
        lista_registro=[]
        df=df_ganado_puro 
        for i in range(len(df_ganado_puro)):
            b=""
            contador=0
            for j in df_ganado_puro.iloc[i]:       
                if contador==6:
                    b=b+" | "+df_ganado_puro.columns[contador]+": "+str(j) 
                elif contador==8:
                    b=b+" | "+df_ganado_puro.columns[contador]+": "+str(j.date())  
                elif contador==0:
                    lista_id.append(j)
                elif contador==3:
                    lista_registro.append(j)
                contador+=1
            modificar.append(b)
            
    #
        filtro = st.selectbox("Animal",modificar)
        id_animal = st.text_input("ID: "+str(lista_id[modificar.index(filtro)])).lower()
        registro = st.text_input("Registro: "+str(lista_registro[modificar.index(filtro)])).lower()
        confirmacion_preñez=""
        

    elif modificar_que=="INSEMINACION":
        modificar=[]
        df=df_inseminacion
        for i in range(len(df_inseminacion)):
            b=""
            contador=0
            for j in df_inseminacion.iloc[i]: 
                if contador==0:
                
                    jj=j.date()
                    
                    b=b+" | "+df_inseminacion.columns[contador]+": "+str(jj)          
                elif (contador==1 or contador==4):
                    b=b+" | "+df_inseminacion.columns[contador]+": "+str(j)

                contador+=1             
            modificar.append(b)
            
        filtro = st.selectbox("Animal",modificar)
        confirmacion_preñez = st.selectbox("Estado",["pendiente","p+","v"])
        registro =""
        id_animal=""
    if st.button("Guardar",use_container_width=True):
        posicion=modificar.index(filtro)
        if modificar_que=="GANADO PURO":
            df_ganado_puro=buscar.modificar_df(df,id_animal,registro,posicion,confirmacion_preñez)
        elif modificar_que=="INSEMINACION":
            df_inseminacion=buscar.modificar_df(df,id_animal,registro,posicion,confirmacion_preñez)
        nacimientos.guardar()   
        st.success("Guardado") 
        st.session_state.modificar_df=False
        st.rerun()

        
#aplicacio 5
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




#   py -m streamlit run app.py