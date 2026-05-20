import os 
from abc import ABC, abstractclassmethod
import pandas as pd
#para fechas
from datetime import datetime
from dateutil.relativedelta import relativedelta
#para generar pdfs
from fpdf import FPDF
import math

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print(os.path.exists("/usr/bin/chromium"))
print(os.path.exists("/usr/bin/chromium-browser"))
print(os.path.exists("/usr/bin/chromedriver"))
options = Options()

options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


df_Animal=pd.read_excel("DATA.xlsx",sheet_name=0)
df_partos=pd.read_excel("DATA.xlsx",sheet_name=1)
df_cria=pd.read_excel("DATA.xlsx",sheet_name=2)
df_embriones=pd.read_excel("DATA.xlsx",sheet_name=3)
df_inseminacion=pd.read_excel("DATA.xlsx",sheet_name=4)
df_fincas=pd.read_excel("DATA.xlsx",sheet_name=5)
df_razas=pd.read_excel("DATA.xlsx",sheet_name=6)
df_ganado_puro=pd.read_excel("DATA.xlsx",sheet_name=7)
df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])
df_informe_vaca=pd.DataFrame(columns=["INFORME"])

class informes():
 def generar_pdf(self,texto,df,nombre_archivo):
      if df.empty:
         df=pd.DataFrame(columns=["Mensaje"])
         df.loc[0]=[" ----------------- No hay datos para mostrar en este informe ----------------- "]
      pdf = FPDF(unit="mm")
      pdf.set_font("Helvetica", size=11)  
      ancho_columnas=[]
      alto_celda = 10 
      for i in range(len(df.columns)):

         largo1=pdf.get_string_width(df.columns[i])+2
         largo2=pdf.get_string_width(df.iloc[:,i].astype(str).loc[df.iloc[:,i].astype(str).str.len().idxmax()])+6
         if largo1>largo2:
            ancho_columnas.append(largo1)
         else:
            ancho_columnas.append(largo2)

      ancho_pagina=sum(ancho_columnas)+20
      ancho_texto=ancho_pagina-20
      ancho_letras = pdf.get_string_width(texto)
      lineas_texto = math.ceil(ancho_letras / ancho_texto)
      alto_texto = lineas_texto * 10
      alto_tabla = (len(df) + 1) * alto_celda
      alto_pagina= (alto_texto+alto_tabla)+40
      pdf.add_page(format=(ancho_pagina,alto_pagina))
      pdf.multi_cell(0,8,texto,align="J")
      pdf.ln()
# 3. Dibujar el encabezado de la tabla (Negrita)
      pdf.set_font("Helvetica", style="B", size=11)
      count=0
      for i in df.columns:
         pdf.cell(ancho_columnas[count], alto_celda, str(i), border=1, align="C")
         count+=1
      pdf.ln()
# 4. Dibujar las filas con los datos (Texto normal)
      pdf.set_font("Helvetica", style="B", size=11)
      for index, fila in df.iterrows():
         for i, celda in enumerate(fila):
            if isinstance(celda ,(datetime, pd.Timestamp)):
               pdf.cell(ancho_columnas[i], alto_celda, celda.strftime("%d/%m/%Y"), border=1, align="C")
            else:
                pdf.cell(ancho_columnas[i], alto_celda, str(celda), border=1, align="C")
         pdf.ln()
# 5. Guardar el archivo final
      return pdf.output(str(nombre_archivo+".pdf"))

class Agregar_Eliminar:
   
   def guardar(self):
      with pd.ExcelWriter("DATA.xlsx") as writer:
         df_Animal.to_excel(writer,index=False, sheet_name='ANIMAL')
         df_partos.to_excel(writer,index=False, sheet_name='PARTOS')
         df_cria.to_excel(writer,index=False, sheet_name='CRIA')
         df_embriones.to_excel(writer,index=False, sheet_name='EMBRIONES')
         df_inseminacion.to_excel(writer,index=False, sheet_name='INSEMINACION')
         df_fincas.to_excel(writer,index=False, sheet_name='FINCAS')
         df_razas.to_excel(writer,index=False, sheet_name='RAZAS')
         df_ganado_puro.to_excel(writer,index=False, sheet_name='GANADO_PURO')
      
     
      
   
   def generar_consecutivo(self):
      consecutivo="0000"+str(df_cria["FINCA"].count()+1)
      l=len(consecutivo)
      consecutivo=str(consecutivo[l-3])+str(consecutivo[l-2])+str(consecutivo[l-1])
      return str(consecutivo)
      
   def nacimiento(self,buscar,vaca,fn,sexo,finca,observaciones,toro=None,raza=None):
      tc = buscar.comprobar_tc(vaca, fn)
      if tc == "CN":
        toro = toro.lower()
        raza = raza.lower()
      elif tc == "TE":
        df = df_embriones.sort_values(by='FECHA_SINCRONIZACION',ascending=False).reset_index(drop=True)
        toro = df[df["RECEPTORA"] == vaca].iloc[0, 6]
        donadora=df[df["RECEPTORA"] == vaca].iloc[0, 5]
        raza = df[df["RECEPTORA"] == vaca].iloc[0, 7]
        registro="pendiente"
        id_tc="pendiente"
        df_ganado_puro.loc[len(df_ganado_puro)]=[id_tc,raza,sexo,registro,toro,donadora,vaca,finca,fn]
      elif tc == "IA":
        df = df_inseminacion.sort_values(by='FECHA',ascending=False).reset_index(drop=True)
        toro = df[df["ID"] == vaca].iloc[0, 6]

   
      numero_datos= len(df_partos[df_partos["ID"] == vaca])
      df_tiempo_entre_partos=df_cria[df_cria["VACA"] == vaca].reset_index(drop=True)
      Numero_parto=0
      tiempo_entre_partos="0"
      if numero_datos==0:
         Numero_parto=1
         tiempo_entre_partos="solo ha parido una vez"
      elif numero_datos>0:
         tiempo= relativedelta(fn,df_tiempo_entre_partos.iloc[numero_datos-1,3])
         if tiempo.days==0:
            Numero_parto=numero_datos
            tiempo_entre_partos="solo ha parido una vez"
         elif abs(tiempo).days>0:
            Numero_parto=numero_datos+1
            tiempo_entre_partos="su anterior parto fue hace "+str(tiempo.years)+" años "+str(tiempo.months)+" meses "+str(tiempo.days)+" dias"
      
      df_cria.loc[len(df_cria)] = [finca,toro,vaca,fn,raza,sexo,tc]
      df_partos.loc[len(df_partos)] = [vaca,finca,Numero_parto,tiempo_entre_partos,observaciones   ]
      


#creamos un buscador que tiene variable buscada el id del animal   

class Buscador:
   

   def ordenar_fecha_df(self,df):
      df_new=df.sort_values(by='FECHA_NACIMIENTO',kind="stable")
      return df_new


#genera un informe sobre las crias apartir de una fecha ingresada por el usuario


   def informe_crias_v(self,df,id_vaca):
      df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])#Se crea el data frame que se va a retornar para que se limpie al ejecutar la funcion
      prueba_datos=df[df["VACA"]==id_vaca]

      if prueba_datos.empty==False:
         contador_te=0
         contador_antes_2026=0
         for i in range(len(df)):
            consecutivo="0000"
            fecha=df.iloc[i]["FECHA_NACIMIENTO"]
            mes=str(fecha.month)
            año=str(fecha.year)
            if mes=="12":
               mes="D"
            elif mes=="11":
               mes="N"
            else:
               mes=mes
         #como se empezaron los numeros a partir del 2026 debo restar los animales anteriores a este año
            if int(año)<2026 and (df.iloc[i]["T_C"]=="CN" or df.iloc[i]["T_C"]=="CN"):
               contador_antes_2026+=1 #se crea para restar al consecutivo las crias antes del 2026

            if df.iloc[i]["T_C"]=="TE":
               id="id_pendiente"
               contador_te+=1 #se crea para restar al consecutivo las crias por TE
            elif (df.iloc[i]["T_C"]=="CN" and int(año)>=2026) or (df.iloc[i]["T_C"]=="IA" and int(año)>=2026):
               consecutivo=consecutivo+str(i+1-contador_te-contador_antes_2026)
               consecutivo=consecutivo[-3]+consecutivo[-2]+consecutivo[-1]
               id=consecutivo+"/"+mes+año[-1]
            elif(df.iloc[i]["T_C"]=="CN" and int(año)<2026) or (df.iloc[i]["T_C"]=="IA" and int(año)<2026):
               id="No_Aplica"
            else:
               id="error_revisa el codigo aqui nunca deberia entrar"
            if df_cria.iloc[i]["VACA"]==id_vaca:
            
               edad=self.calcular_edad(df.iloc[i,3])
               df_informe_crias.loc[i]=[id,df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],edad,df.iloc[i,4],df.iloc[i,5],df.iloc[i,6]]
      
      return df_informe_crias,id_vaca
   
   def informe_crias(self,df,filtros):
#Se crea el data frame que se va a retornar para que se limpie al ejecutar la funcion
      df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])  
#Se crean los ID 
      contador_te=0
      contador_antes_2026=0
      # pide filtros para el informe
      for i in range(len(df)):
         consecutivo="0000"
         fecha=df.iloc[i]["FECHA_NACIMIENTO"]
         mes=str(fecha.month)
         año=str(fecha.year)
         if mes=="12":
            mes="D"
         elif mes=="11":
            mes="N"
         else:
            mes=mes
         #como se empezaron los numeros a partir del 2026 debo restar los animales anteriores a este año
         if int(año)<2026 and (df.iloc[i]["T_C"]=="CN" or df.iloc[i]["T_C"]=="CN"):
            contador_antes_2026+=1 #se crea para restar al consecutivo las crias antes del 2026

         if df.iloc[i]["T_C"]=="TE":
            id="id_pendiente"
            contador_te+=1 #se crea para restar al consecutivo las crias por TE
         elif (df.iloc[i]["T_C"]=="CN" and int(año)>=2026) or (df.iloc[i]["T_C"]=="IA" and int(año)>=2026):
            consecutivo=consecutivo+str(i+1-contador_te-contador_antes_2026)
            consecutivo=consecutivo[-3]+consecutivo[-2]+consecutivo[-1]
            id=consecutivo+"/"+mes+año[-1]
         elif(df.iloc[i]["T_C"]=="CN" and int(año)<2026) or (df.iloc[i]["T_C"]=="IA" and int(año)<2026):
            id="No_Aplica"
         else:
            id="error_revisa el codigo aqui nunca deberia entrar"
#se  llena un nuevo df ya filtrado con todos los valores requeridos
         
         if df.iloc[i]["FECHA_NACIMIENTO"]>=filtros[0] and (df.iloc[i]["FINCA"]==filtros[1] or filtros[1]=="incluir todos") and (df.iloc[i]["T_C"]==filtros[2]or filtros[2]=="incluir todos"):
            edad=self.calcular_edad(df_cria.iloc[i,3])
            df_informe_crias.loc[i]=[id,df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],edad,df.iloc[i,4],df.iloc[i,5],df.iloc[i,6]]
      return filtros[0],df_informe_crias




   def calcular_edad(self,fecha):
      edad = relativedelta(datetime.today(),fecha)
      return f"tiene una edad de {edad.years} años, {edad.months} meses y {edad.days} días"

   def  comprobar_tc(self,id,fecha_parto):
      p_embriones=df_embriones[df_embriones["RECEPTORA"]==id]
      fecha_ia=df_inseminacion[df_inseminacion["ID"]==id].iloc[:,0].max()+pd.Timedelta(days=285)
      fecha_ia=fecha_ia.date()
      fecha_te=df_embriones[df_embriones["RECEPTORA"]==id].iloc[:,2].max()+pd.Timedelta(days=285)
      fecha_te=fecha_te.date()
      if p_embriones.empty or abs((fecha_te - fecha_parto).days)>45:
         p_inseminacion=df_inseminacion[df_inseminacion["ID"]==id]
         if p_inseminacion.empty:
            tc="CN"
         elif abs((fecha_ia - fecha_parto).days)<=45:
            tc="IA"
         else:
            tc="CN"
      elif abs((fecha_te - fecha_parto).days)<=45:
         tc="TE"
      return tc


   #aqui se van a realizar diferentes funciones dependienod que se busca
   def informacion(self,tipo_animal,df_entrada,id):
      if tipo_animal=="VACA":   
         show_id = df_partos[df_partos["ID"] == id]
         
         show_raza = df_Animal[df_Animal["ID"] == id].iloc[0, 3]
         show_edad=self.calcular_edad(df_Animal[df_Animal["ID"] == id].iloc[0, 2])

         if show_id.empty==False:
            
            show_partos=df_partos[df_partos["ID"]==id]
            df_l1=df_entrada[df_entrada["VACA"]==id].iloc[:,0:3]#muestra Id cria y finca
            df_l2=df_entrada[df_entrada["VACA"]==id].iloc[:,4]#muestra la fecha del nacimiento    
            df_l4=df_entrada[df_entrada["VACA"]==id].iloc[:,6:]#muestra la raza y sexo
            df_l3=df_partos[df_partos["ID"]==id].iloc[:,2:4]
#se crea un nuevo df con las columnas deseadas  
            df=pd.concat([df_l1,df_l2,df_l4,df_l3],axis=1)
            show_partos=show_partos[show_partos.columns[2]].max()
            texto="La Vaca identificada "+str(id)+" de la raza "+str(show_raza)+" "+str(show_edad)+" ha parido "+str(show_partos)+" veces, en la tabla verá toda la informacion de sus partos"
         else:
            df=pd.DataFrame()
            texto="La Vaca identificada "+str(id)+" de la raza "+str(show_raza)+" "+str(show_edad)+" no tiene partos registrados"
         
      return texto,df,id

   def modificar_df(self,df,id,registro,posicion):
      nuevo_id=id
      nuevo_registro=registro  
      salir=1    
      if  not nuevo_id:
         df.iloc[posicion,0]=df.iloc[posicion,0]
      else:
         df.iloc[posicion,0]=[nuevo_id]

      if not nuevo_registro :
         df.iloc[posicion,3]=df.iloc[posicion,2]
      else:
         df.iloc[posicion,3]=[nuevo_registro]
      return df
   #def buscar_registro():
 

# Entrar a la página

def registros(registro):

  def registros(registro):

   options = Options()

   options.binary_location = "/usr/bin/chromium"

   options.add_argument("--headless=new")
   options.add_argument("--no-sandbox")
   options.add_argument("--disable-dev-shm-usage")

   service = Service("/usr/bin/chromedriver")

   driver = webdriver.Chrome(
        service=service,
        options=options
    )

   wait = WebDriverWait(driver, 20)

   driver.get("https://sir.asocebu.com.co/Genealogias/")

    # Input
   input_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@formcontrolname="Registro"]')))

   input_texto.send_keys(registro)

    # Botón consultar
   boton = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Consultar")]')))

   boton.click()

   time.sleep(3)

    # Botón search
   icono = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//mat-icon[contains(@fonticon,"search")]]')))

   icono.click()
   
"""def registros(registro):
   
   driver = webdriver.Chrome(options=options)
   wait = WebDriverWait(driver, 20)
# Input
   input_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@formcontrolname="Registro"]')))

   input_texto.send_keys(registro)

# Botón consultar
   boton = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Consultar")]')))
   boton.click()
# Esperar que cargue
   time.sleep(3)
   icono = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//mat-icon[contains(@fonticon,"search")]]')))
   icono.click()
   input("Presiona Enter para cerrar...")
   driver.quit()"""


