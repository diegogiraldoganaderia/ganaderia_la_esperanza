import streamlit as st
import base64
from Ganaderia import *
import os
import time
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
        

    st.session_state.tablas_de_datos=True
    


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
        df_fincas=st.data_editor(fincas,num_rows="dynamic")
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
        st.session_state.tablas_de_datos=False
        st.rerun()

       
        
    

#   py -m streamlit run app.py