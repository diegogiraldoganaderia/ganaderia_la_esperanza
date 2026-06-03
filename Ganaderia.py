import os 
from abc import ABC, abstractclassmethod
import pandas as pd
#para fechas
from datetime import datetime
from dateutil.relativedelta import relativedelta
#para generar pdfs
from fpdf import FPDF
import math
from supabase import create_client
import streamlit as st
import time




url ="https://soyjodguzmbiggwymfdn.supabase.co"
key ="sb_publishable_2rsYfiqDckypRhCIgUgG0Q__6DJkp-c"
supabase = create_client(url, key)

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
df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])
df_informe_vaca=pd.DataFrame(columns=["INFORME"])

class Informes():
 def registros(self,registro):
   pdf_path  = "registros/"+str(registro)+".pdf"
   return pdf_path
 
 def generar_pdf(self,texto,df,nombre_archivo):
      df=df.dropna()
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
      alto_pagina= (alto_texto+alto_tabla)+50


      pdff = FPDF(unit="mm",format=(ancho_pagina,alto_pagina))
      pdff.set_font("Helvetica", size=11) 
      pdff.add_page()#format=(ancho_pagina,alto_pagina)
      pdff.multi_cell(0,8,texto,align="J")
      pdff.ln()
# 3. Dibujar el encabezado de la tabla (Negrita)
      pdff.set_font("Helvetica", style="B", size=11)
      count=0
      for i in df.columns:
         pdff.cell(ancho_columnas[count], alto_celda, str(i), border=1, align="C")
         count+=1
      pdff.ln()
# 4. Dibujar las filas con los datos (Texto normal)
      pdff.set_font("Helvetica", style="B", size=11)
      
      for index, fila in df.iterrows():
         for i, celda in enumerate(fila):
            if isinstance(celda ,(datetime, pd.Timestamp)):
               pdff.cell(ancho_columnas[i], alto_celda, celda.strftime("%d/%m/%Y"), border=1, align="C")
            else:
                pdff.cell(ancho_columnas[i], alto_celda, str(celda), border=1, align="C")
        
         pdff.ln()
      
# 5. Guardar el archivo final
      return pdff.output(str(nombre_archivo+".pdf"))
 


class Agregar_Eliminar:
   def guardar(self,df_inseminacion,df_animal,df_partos,df_cria,df_embriones,df_fincas,df_razas,df_ganado_puro):
      df_animal=df_animal.dropna()
      supabase.table("ANIMAL").delete().neq("ID",-1).execute()
      supabase.table("ANIMAL").insert(df_animal.to_dict(orient="records")).execute()
      df_partos=df_partos.reset_index()
      df_partos=df_partos.dropna()
      supabase.table("PARTOS").delete().neq("index",-1).execute()
      supabase.table("PARTOS").insert(df_partos.to_dict(orient="records")).execute()
      df_cria=df_cria.reset_index()
      df_cria=df_cria.dropna()
      
      supabase.table("CRIA").delete().neq("index",-1).execute()
      supabase.table("CRIA").insert(df_cria.to_dict(orient="records")).execute()
      df_embriones=df_embriones.reset_index()
      df_embriones=df_embriones.dropna()
      supabase.table("EMBRIONES").delete().neq("index",-1).execute()
      supabase.table("EMBRIONES").insert(df_embriones.to_dict(orient="records")).execute()
      df_inseminacion=df_inseminacion.reset_index()
      df_inseminacion=df_inseminacion.dropna()
      supabase.table("INSEMINACION").delete().neq("index",-1).execute()
      supabase.table("INSEMINACION").insert(df_inseminacion.to_dict(orient="records")).execute()
      df_fincas=df_fincas.reset_index()
      df_fincas=df_fincas.dropna()
      supabase.table("FINCAS").delete().neq("index",-1).execute()
      supabase.table("FINCAS").insert(df_fincas.to_dict(orient="records")).execute()
      df_razas=df_razas.dropna()
      supabase.table("RAZAS").delete().neq("ID",-1).execute()
      supabase.table("RAZAS").insert(df_razas.to_dict(orient="records")).execute()
      df_ganado_puro=df_ganado_puro.reset_index()
      df_ganado_puro=df_ganado_puro.dropna()
      supabase.table("GANADO_PURO").delete().neq("index",-1).execute()
      supabase.table("GANADO_PURO").insert(df_ganado_puro.to_dict(orient="records")).execute()

      df_servicios=df_servicios.reset_index()
      df_servicios=df_servicios.dropna()
      supabase.table("SERVICIO").delete().neq("index",-1).execute()
      supabase.table("SERVICIO").insert(df_servicios.to_dict(orient="records")).execute()



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
         
         tiempo= relativedelta(pd.to_datetime(fn),pd.to_datetime(df_tiempo_entre_partos.iloc[numero_datos-1,3]))
         
         if tiempo.days==0:
            Numero_parto=numero_datos
            tiempo_entre_partos="solo ha parido una vez"
         elif abs(tiempo).days>0:
            Numero_parto=numero_datos+1
            tiempo_entre_partos="su anterior parto fue hace "+str(tiempo.years)+" años "+str(tiempo.months)+" meses "+str(tiempo.days)+" dias"
      fn=fn.date()
      df_cria.loc[len(df_cria)] = [finca,toro,vaca,str(fn),raza,sexo,tc]
      
      df_partos.loc[len(df_partos)] = [vaca,finca,Numero_parto,tiempo_entre_partos,observaciones]
      return df_cria,df_partos

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
            fecha=pd.to_datetime(fecha)
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
               df_informe_crias.loc[i]=[id,df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],pd.to_datetime(df.iloc[i,3]).date(),edad,df.iloc[i,4],df.iloc[i,5],df.iloc[i,6]]
      
      return df_informe_crias,id_vaca
   
   def informe_crias(self,df,filtros,dfgp): 
      
#Se crea el data frame que se va a retornar para que se limpie al ejecutar la funcion
      df_informe_crias=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","EDAD","RAZA","SEXO","T_C"])  
#Se crean los ID 
      contador_te=0
      contador_antes_2026=0
      # pide filtros para el informe
      contador_total=0
      contador_TE_antes_2026=0
      for i in range(len(df)):
         consecutivo="0000"
         fecha=df.iloc[i]["FECHA_NACIMIENTO"]
         fecha=pd.to_datetime(fecha)
         mes=str(fecha.month)
         año=str(fecha.year)
         if mes=="12":
            mes="D"
         elif mes=="11":
            mes="N"
         else:
            mes=mes
         #como se empezaron los numeros a partir del 2026 debo restar los animales anteriores a este año
         if int(año)<2026 and df.iloc[i]["T_C"]=="CN" :
            contador_antes_2026+=1 
            #se crea para restar al consecutivo las crias antes del 2026
         
         if df.iloc[i]["T_C"]=="TE" and contador_te<len(dfgp):
            id=dfgp.iloc[contador_te]["ID"]
            contador_te+=1 #se crea para restar al consecutivo las crias por TE
         elif (df.iloc[i]["T_C"]=="CN" and int(año)>=2026) or (df.iloc[i]["T_C"]=="IA" and int(año)>=2026):
            contador_total+=1
            consecutivo=consecutivo+str(i+1-contador_antes_2026-contador_te)
            consecutivo=consecutivo[-3]+consecutivo[-2]+consecutivo[-1]
            id=consecutivo+"/"+mes+año[-1]
         elif(df.iloc[i]["T_C"]=="CN" and int(año)<2026) or (df.iloc[i]["T_C"]=="IA" and int(año)<2026):
            id="No_Aplica"
         else:
            id="error_revisa el codigo aqui nunca deberia entrar"
#se  llena un nuevo df ya filtrado con todos los valores requeridos
         
         if pd.to_datetime(df.iloc[i]["FECHA_NACIMIENTO"])>=filtros[0]:
            edad=self.calcular_edad(df.iloc[i,3])
            df_informe_crias.loc[i]=[id,df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],pd.to_datetime(df.iloc[i,3]).date(),edad,df.iloc[i,4],df.iloc[i,5],df.iloc[i,6]]
      l1=[]
      for j in range(len(filtros[1])):
         l1.append(df_informe_crias[df_informe_crias["FINCA"]==filtros[1][j]])
      df_informe_crias=pd.concat(l1)
      l2=[]
      for k in range(len(filtros[2])):
         l2.append(df_informe_crias[df_informe_crias["T_C"]==filtros[2][k]])
      df_informe_crias=pd.concat(l2)
    
      return filtros[0],df_informe_crias

   def calcular_edad(self,fecha):
      fecha=pd.to_datetime(fecha)
      edad = relativedelta(datetime.today(),fecha)
      return f"tiene una edad de {edad.years} años, {edad.months} meses y {edad.days} dias"

   def  comprobar_tc(self,id,fecha_parto):
      datos_embriones=df_embriones[df_embriones["RECEPTORA"]==id]
      datos_inseminacion=df_inseminacion[df_inseminacion["ID"]==id]
      if datos_embriones.empty and datos_inseminacion.empty:
         tc="CN"

      elif not datos_embriones.empty and not datos_inseminacion.empty:
         if abs((fecha_ia - fecha_parto).days)<=45:
            tc="IA"
         elif abs((fecha_te - fecha_parto).days)<=45:
            tc="TE"
         else:
            tc="CN"

      elif not datos_embriones.empty:
         fecha_ia=df_inseminacion[df_inseminacion["ID"]==id].iloc[:,0].max()+pd.Timedelta(days=285)
         fecha_ia=fecha_ia.date()
         if abs((fecha_ia - fecha_parto).days)<=45:
            tc="IA"
         else:
            tc="CN"
      
      elif not datos_inseminacion.empty:
         fecha_te=df_embriones[df_embriones["RECEPTORA"]==id].iloc[:,2].max()+pd.Timedelta(days=285)
         fecha_te=fecha_te.date()
         if abs((fecha_te - fecha_parto).days)<=45:
            tc="TE"
         else:
            tc="CN"
      
      

      return tc

   #aqui se van a realizar diferentes funciones dependienod que se busca
   def informacion(self,tipo_animal,df_entrada,id):
      if tipo_animal=="VACA":   
         show_id = df_partos[df_partos["ID"] == id]
         
         show_raza = df_animal[df_animal["ID"] == id].iloc[0, 3]
         show_edad=self.calcular_edad(df_animal[df_animal["ID"] == id].iloc[0, 2])

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

   def modificar_df(self,df,id,registro,posicion,confirmacion_preñez):
      nuevo_id=id
      nuevo_registro=registro 
      nueva_confirmacion=confirmacion_preñez 
      
      if  not nuevo_id:
         df.iloc[posicion,0]=df.iloc[posicion,0]
      else:
         df.iloc[posicion,0]=[nuevo_id]

      if not nuevo_registro :
         df.iloc[posicion,3]=df.iloc[posicion,2]
      else:
         df.iloc[posicion,3]=[nuevo_registro]
      
      if not nueva_confirmacion :
         df.iloc[posicion][4]=df.iloc[posicion,4]
      else:
         df.iloc[posicion,4]=[nueva_confirmacion]
      return df
   
   def informe_embriones(df,raza,fecha,finca,compania,x1,x3):
      if x1=="x1":
         df=df[pd.to_datetime(df["FECHA_NACIMIENTO"])>=pd.to_datetime(fecha)]
      else:
         df=df[pd.to_datetime(df["FECHA_SINCRONIZACION"])>=pd.to_datetime(fecha)]
      
      l_finca=[]
      for i in finca:
         l_finca.append(df[df["FINCA"]==i])
      df=pd.concat(l_finca)
      
      if compania!="compania":
         l_compania=[]
         for i in compania:
            l_compania.append(df[df["COMPANIA"]==i])
         df=pd.concat(l_compania)
      if x1!="x1":
         l_x1=[]
         for i in x1:
            l_x1.append(df[df["X1"]==i])
         df=pd.concat(l_x1)

      if x3!="x3":
         l_x3=[]
         for i in x3:
            l_x3.append(df[df["X3"]==i])
         df=pd.concat(l_x3)

      l_raza=[]
      
      for i in raza:
         l_raza.append(df[df["RAZA"]==i])
      df=pd.concat(l_raza)
      return df
   
