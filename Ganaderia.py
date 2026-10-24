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
df_palpacion=pd.DataFrame(supabase.table("PALPACION").select("*").execute().data)
df_palpacion=df_palpacion.drop(columns=["index"])

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
      alto_pagina= (alto_texto+alto_tabla)+60


      pdff = FPDF(unit="mm",format=(ancho_pagina,alto_pagina))
      pdff.set_font("Helvetica", size=11) 
      pdff.add_page()#format=(ancho_pagina,alto_pagina)
      pdff.image("logopdf.png", x=ancho_pagina-48, y=0, w=40)#logo
      pdff.set_y(15) 
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
      return pdff.output(nombre_archivo+".pdf")

   def generar_pdf_multiple(self,textos,dfs,nombre_archivo):
      
      
      #revisa que los dfs no esten vacios
      dfss=[]
      for df in dfs:
         df=df.dropna()
         if df.empty:
            df=pd.DataFrame(columns=["Mensaje"])
            df.loc[0]=[" ----------------- No hay datos para mostrar en este informe ----------------- "]
         else:
            df=df
         dfss.append(df)

      #texto=textos[0]
      #se marca como deberiaser la fuente 
      pdf = FPDF(unit="mm")      
      pdf.set_font("Helvetica", size=11)

      
      alto_celda = 10 
      #sedetermina el tamaño de la hoja
      lista_ancho_columnas=[]

      for df in dfss:
         ancho_columnas=[]
         for i in range(len(df.columns)):
            largo1=pdf.get_string_width(df.columns[i])+2
            largo2=pdf.get_string_width(df.iloc[:,i].astype(str).loc[df.iloc[:,i].astype(str).str.len().idxmax()])+6
            if largo1>largo2:
               ancho_columnas.append(largo1)
            else:
               ancho_columnas.append(largo2)    
         lista_ancho_columnas.append(ancho_columnas)
     
      ancho_pagina=[]
      for ancho_columnas in lista_ancho_columnas:
      #se setean los tamños d ela pagina
         ancho_pagina.append(sum(ancho_columnas)+20)
      
      ancho_pagina=max(ancho_pagina)
      ancho_texto=ancho_pagina-20
      lineas_texto=[]
      for texto in textos:
         ancho_letras = pdf.get_string_width(texto)
         lineas_texto.append( math.ceil(ancho_letras / ancho_texto))

      #print(lineas_texto,)
      alto_texto = sum(lineas_texto)*20  #*len(textos)
      alto_tabla = (sum(len(df) for df in dfs)) * alto_celda
      alto_tabla=0
      for df in dfs:
         if len(df)>0:
            alto_tabla+=(len(df)+1)*alto_celda
         else:
            alto_tabla+=2*alto_celda
         
      
      
      alto_pagina= (alto_texto+alto_tabla+60)
     

      #primera pagina
      pdff = FPDF(unit="mm",format=(ancho_pagina,alto_pagina))
      pdff.set_font("Helvetica", size=11) 
      pdff.add_page()#format=(ancho_pagina,alto_pagina)
      pdff.image("logopdf.png", x=ancho_pagina-48, y=0, w=40)#logo
      pdff.set_y(15) 
   
         
      contador=0
      for df in dfss:         
         pdff.set_font("Helvetica", size=11) 
         pdff.ln()
         pdff.multi_cell(0,8,textos[contador],align="J")
         pdff.ln()
   # 3. Dibujar el encabezado de la tabla (Negrita)
         pdff.set_font("Helvetica", style="B", size=11)
         count=0
         for i in df.columns:
            pdff.cell(lista_ancho_columnas[contador][count], alto_celda, str(i), border=1, align="C")
            count+=1
         pdff.ln()
   # 4. Dibujar las filas con los datos (Texto normal)
         pdff.set_font("Helvetica", style="B", size=11)
         
         for index, fila in df.iterrows():
            for i, celda in enumerate(fila):
               if isinstance(celda ,(datetime, pd.Timestamp)):
                  pdff.cell(lista_ancho_columnas[contador][i], alto_celda, celda.strftime("%d/%m/%Y"), border=1, align="C")
               else:
                  pdff.cell(lista_ancho_columnas[contador][i], alto_celda, str(celda), border=1, align="C")
         
            pdff.ln()
         contador+=1
         
               
# 5. Guardar el archivo final
      return pdff.output(str(nombre_archivo+".pdf"))

class Agregar_Eliminar:
   def guardar(self, dataframes):
      for tabla, df in dataframes:
        df = df.dropna()
        # Tablas que utilizan ID como identificador
        if tabla in ["ANIMAL", "RAZAS","TORO"]:
            supabase.table(tabla).delete().neq("ID", -1).execute()
        # Tablas que utilizan index
        else:
            df = df.reset_index(drop=True)
            df = df.reset_index()
            supabase.table(tabla).delete().neq("index", -1).execute()
        # Insertar nuevamente solamente esta tabla
        supabase.table(tabla).insert(
            df.to_dict(orient="records")
        ).execute()

     
   def nacimiento(self,buscar,vaca,fn,sexo,finca,observaciones,toro=None):
      puro_te=["TE_P_V","TE_F1_V","TE_P_C","TE_F1_C"]
      v_v=["CN_C_V","CN_C_C","CN_P_V","CN_F1_V"]
      ia=["IA_P_V","IA_F1_V","IA_C_V"]
      
      tc = buscar.comprobar_tc(vaca,toro,fn,finca)
      raza=tc[1]

      if tc[0] in v_v:
        toro = toro.lower()
        if tc[0]=="CN_P_V" or tc[0]=="CN_F1_V":
         id_tc="pendiente"
         registro="pendiente"
         df_ganado_puro.loc[len(df_ganado_puro)]=[id_tc,raza,sexo,registro,toro,vaca,vaca,finca,str(fn.date())]
      elif tc[0] in puro_te:
        df = df_embriones.sort_values(by='FECHA_SINCRONIZACION',ascending=False).reset_index(drop=True)
        toro = df[df["RECEPTORA"] == vaca].iloc[0, 6]
        donadora=df[df["RECEPTORA"] == vaca].iloc[0, 5]
        registro="pendiente"
        id_tc="pendiente"
        df_ganado_puro.loc[len(df_ganado_puro)]=[id_tc,raza,sexo,registro,toro,donadora,vaca,finca,str(fn.date())]

      elif tc[0] in  ia:
        
        df = df_inseminacion.sort_values(by='FECHA',ascending=False).reset_index(drop=True)
        toro = df[df["ID"] == vaca].iloc[0, 6]
        if tc[0]=="IA_P_V" or tc[0]=="IA_F1_V":
           id_tc="pendiente"
           registro="pendiente"
           df_ganado_puro.loc[len(df_ganado_puro)]=[id_tc,raza,sexo,registro,toro,vaca,vaca,finca,str(fn.date())]
      
      
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
      
      df_cria.loc[len(df_cria)] = [finca,toro,vaca,str(fn),raza,sexo,tc[0]]
      df_partos.loc[len(df_partos)] = [vaca,finca,Numero_parto,tiempo_entre_partos,observaciones]
      df_protocolo.loc[len(df_protocolo)]=[vaca,str(fn),finca,"pendiente"]

      dataframes_guardar=[]
      dataframes_guardar.append(("PARTOS", df_partos))
      dataframes_guardar.append(("CRIA", df_cria))
      dataframes_guardar.append(("PROTOCOLO", df_protocolo))
      dataframes_guardar.append(("GANADO_PURO", df_ganado_puro))
      return dataframes_guardar
  
class Buscador:
   def calcular_edad(self,fecha):
      fecha=pd.to_datetime(fecha)
      edad = relativedelta(datetime.today(),fecha)
      return f"tiene una edad de {edad.years} años, {edad.months} meses y {edad.days} dias"

   def  comprobar_tc(self,id,toro,fecha_parto,finca):
      
      #concepcon natural
      raza_vaca=df_ganado_puro[(df_ganado_puro["SEXO"]=="hembra")&(df_ganado_puro["ID"]==id)]
      raza_toro=df_toros[df_toros["ID"]==toro]
      if len(raza_vaca)>0:
         raza_vaca=raza_vaca.iloc[0,1]
      else:
         raza_vaca="comercial"

      if len(raza_toro)>0:
         raza_toro=raza_toro.iloc[0,1]
      else:
         raza_toro="comercial"

   
      if  raza_vaca==raza_toro and raza_vaca!="comercial":
      
         tc="CN_P_V"
         raza =raza_toro
      elif raza_vaca!=raza_toro and raza_vaca!="comercial" and raza_toro!="comercial":
         tc="CN_F1_V"
         raza= raza_toro+" x "+raza_vaca

      elif (raza_vaca=="comercial" or raza_toro=="comercial") and finca=="compañia":
         tc="CN_C_C"
         raza="comercial"

      elif (raza_vaca=="comercial" or raza_toro=="comercial") and finca!="compañia":
         tc="CN_C_V"
         raza="comercial"
      
      datos_embrionesV=df_embriones[(df_embriones["RECEPTORA"]==id)
                                    &(df_embriones["#PROVEEDOR"]=="vanguardia")
                                    &(df_embriones["X1"]=="p+")]
      
      datos_embrionesC=df_embriones[(df_embriones["RECEPTORA"]==id)
                                          &(df_embriones["#PROVEEDOR"]!="vanguardia")
                                          &(df_embriones["X1"]=="p+")]

      #TE_P_V AND TE_F1_V
     
      for fecha_embriones in datos_embrionesV["FECHA_TRANSFERENCIA"]:
         
         if (abs((fecha_parto-pd.to_datetime(fecha_embriones)).days-280))<45:
            
            df = datos_embrionesV.sort_values(by='FECHA_SINCRONIZACION',ascending=False).reset_index(drop=True)
            raza = df[df["RECEPTORA"] ==id].iloc[0, 7]
            grupo_genetico= df_razas.loc[df_razas["ID"] == raza, "GRUPO_GENETICO"].iloc[0]
            
            if grupo_genetico=="PURO":
               tc="TE_P_V"
            elif grupo_genetico=="F1":
               tc="TE_F1_V"
            else:
               tc="no se encontro la raza"


            
      #TE_P_C AND TE_F1_C
      for fecha_embriones in datos_embrionesC["FECHA_TRANSFERENCIA"]:
         if (abs((fecha_parto-pd.to_datetime(fecha_embriones)).days-280))<45: 
            df = datos_embrionesC.sort_values(by='FECHA_SINCRONIZACION',ascending=False).reset_index(drop=True)
            raza = df[df["RECEPTORA"] ==id].iloc[0, 7]
            grupo_genetico= df_razas.loc[df_razas["ID"] == raza, "GRUPO_GENETICO"].iloc[0]
            
            if grupo_genetico=="PURO":
               tc="TE_P_C"
            elif grupo_genetico=="F1":
               tc="TE_F1_C"
            else:
               tc="no se encontro la raza"
            
      datos_inseminacion=df_inseminacion[(df_inseminacion["ID"]==id)
                                         &(df_inseminacion["CONFIRMACION"]=="p+")]
      
      contador_IA=0
      for fecha_inseminacion in datos_inseminacion["FECHA"]:
         if (abs(fecha_parto-pd.to_datetime(fecha_inseminacion)).days-280)<45:
            raza_toro_IA= datos_inseminacion.iloc[contador_IA,2]
            contador_IA+=1
            if raza_vaca=="comercial" or raza_toro_IA=="comercial":
               tc="IA_C_V"
               raza="comercial"
            elif raza_vaca!=raza_toro_IA and raza_vaca!="comercial":
               tc="IA_F1_V"
               raza= raza_toro_IA+" x "+raza_vaca

            elif raza_vaca==raza_toro_IA and raza_vaca!="comercial":
               tc="IA_P_V"
               raza=raza_toro_IA
      
      
      return tc,raza
   
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
   
   def informe_embriones(self,df,fecha,finca):
      df= df[["PROVEEDOR", "FINCA","RECEPTORA","DONADORA","REPRODUCTOR","RAZA","TIPO_EMBRION","X1"]]
      l_finca=[]
      for i in finca:
         l_finca.append(df[df["FINCA"]==i.lower()])
      df=pd.concat(l_finca)
      total=len(df)
      total_prenadas=len(df[df["X1"]=="p+"])
      porcentaje_p=round((total_prenadas*100/total),1)
      total_vacias=len(df[df["X1"]=="v"])
      porcentaje_v=round((total_vacias*100/total),1)
      total_rp=len(df[df["X1"]=="rp"])
      porcentaje_rp=round((total_rp*100/total),1)
      return df,str(total),str(total_prenadas),str(porcentaje_p),str(total_vacias),str(porcentaje_v),str(total_rp),str(porcentaje_rp)

   def palpacion_inseminacion(df_inseminacion):
      fecha_actual=datetime.now()
      df_fecha_desde_inseminacion=pd.DataFrame(columns=["DIAS TRASNCURRIDOS"])
      df_inseminacion=df_inseminacion[df_inseminacion["CONFIRMACION"]=="pendiente"]
      for i in range(len(df_inseminacion)):
         dias=(fecha_actual-pd.to_datetime(df_inseminacion.iloc[i]["FECHA"])).days
         df_fecha_desde_inseminacion.loc[len(df_fecha_desde_inseminacion)]=["La vaca "+str(df_inseminacion.iloc[i]["ID"])+
                              " fue inseminada en la fecha "+df_inseminacion.iloc[i]["FECHA"]+" han pasado "+str(dias)
                              +" y aún no ha sido palpada"]
      cantidad=len(df_fecha_desde_inseminacion)
      return df_fecha_desde_inseminacion,cantidad

   def informe_receptoras(self,df):
      
      lista_receptoras=df["RECEPTORA"].unique().tolist()
      df_receptoras=pd.DataFrame(columns=["RECEPTORA","FINCA","#PROTOCOLOS","# p+","% p+","# v","% v","# rp","% "+"rp"])
      for j in range(len(lista_receptoras)):
         df_receptoras.loc[j]=[
            lista_receptoras[j],
            df.loc[df["RECEPTORA"] ==lista_receptoras[j], "FINCA"].values[0],
            len(df[df["RECEPTORA"]==lista_receptoras[j]]),
            len(df[(df["RECEPTORA"]==lista_receptoras[j])&(df["X1"]=="p+")]),
            round(100*len(df[(df["RECEPTORA"]==lista_receptoras[j])&(df["X1"]=="p+")])/len(df[df["RECEPTORA"]==lista_receptoras[j]])),
            len(df[(df["RECEPTORA"]==lista_receptoras[j])&(df["X1"]=="v")]),
            str(round(100*len(df[(df["RECEPTORA"]==lista_receptoras[j])&(df["X1"]=="v")])/len(df[df["RECEPTORA"]==lista_receptoras[j]])))+" %",
            len(df[(df["RECEPTORA"]==lista_receptoras[j])&(df["X1"]=="rp")]),
            str(round((100*len(df[(df["RECEPTORA"]==lista_receptoras[j])&(df["X1"]=="rp")])/len(df[df["RECEPTORA"]==lista_receptoras[j]]))))+" %",

         ]

      df_receptoras =df_receptoras.sort_values(by="% p+", ascending=False)
      df_receptoras["% p+"]=df_receptoras["% p+"].astype(str) +" %"
      return df_receptoras

   def numeros(self,df_crias,df_puro):
      df_crias=df_crias.sort_values(by="FECHA_NACIMIENTO").reset_index(drop=True)
      
      df_resultado=pd.DataFrame(columns=["ID","FINCA","TORO","VACA","FECHA_NACIMIENTO","RAZA","SEXO","TC_GG_O"]) 
         
#  ---------------PUROS CON NUMEROS FUERA DE LA FINCA------------
      n_cria=0
      df_datos_puros_c=df_crias[(df_crias["TC_GG_O"]=="TE_P_C")|(df_crias["TC_GG_O"]=="TE_F1_C")]
      for fila_df in range(len(df_datos_puros_c)):
         vaca=df_datos_puros_c.iloc[fila_df]["VACA"]
         
         if fila_df>0 and df_datos_puros_c.iloc[fila_df-1]["VACA"]==vaca:
            n_cria+=1
         else:
            n_cria=0
         fecha_nacimiento=pd.to_datetime(df_datos_puros_c.iloc[fila_df]["FECHA_NACIMIENTO"])
         datos=df_puro[(df_puro["RECEPTORA"]==vaca)&(pd.to_datetime(df_puro["FECHA_NACIMIENTO"])==fecha_nacimiento)]
         if len(datos)>0:
            df_resultado.loc[len(df_resultado)]=[datos.iloc[n_cria,0]]+df_datos_puros_c.iloc[fila_df].tolist()
#  ---------------PUROS CON NUMEROS DENTRO DE LA FINCA------------
      df_datos_puros_v=df_crias[(df_crias["TC_GG_O"]=="TE_P_V")
                        |(df_crias["TC_GG_O"]=="TE_F1_V")
                        |(df_crias["TC_GG_O"]=="IA_P_V")
                        |(df_crias["TC_GG_O"]=="IA_F1_V")
                        |(df_crias["TC_GG_O"]=="CN_P_V")
                        |(df_crias["TC_GG_O"]=="CN_F1_V")]
      
      for contador_puros in range(len(df_datos_puros_v)):#cambio
      
         anno=str(df_datos_puros_v.iloc[contador_puros]["FECHA_NACIMIENTO"])#cambio   
         mes={"01":"1","02":"2","03":"3","04":"4"
            ,"05":"5","06":"6","07":"7","08":"8"
            ,"09":"9","10":"0","11":"N","12":"D"}.get(anno[5:7])
         tc_gg_o=df_datos_puros_v.iloc[contador_puros]["TC_GG_O"]
         if tc_gg_o=="TE_P_V" or tc_gg_o=="IA_P_V" or tc_gg_o=="CN_P_V":
            
            id=(("000"+str(contador_puros+51))[-3:])+"/"+anno[3]
            df_resultado.loc[len(df_resultado)]=[id]+df_datos_puros_v.iloc[contador_puros].tolist()
         elif tc_gg_o=="TE_F1_V" or tc_gg_o=="IA_F1_V" or tc_gg_o=="CN_F1_V":
            id=(("000"+str(contador_puros+51))[-3:])+"/"+mes+anno[3]
            df_resultado.loc[len(df_resultado)]=[id]+df_datos_puros_v.iloc[contador_puros].tolist()
   
#  ---------------COMERCIALES ANTES DE 2026------------
      df_cn_antes_2026=df_crias[(pd.to_datetime(df_crias["FECHA_NACIMIENTO"]).dt.year<2026)&
                           (df_crias["TC_GG_O"]=="CN_C_V")]

      for antes_2026 in range(len(df_cn_antes_2026)):
         id="no aplica"
         df_resultado.loc[len(df_resultado)]=[id]+df_cn_antes_2026.iloc[antes_2026].tolist()

# ---------------COMERCIALES DESPUES DE 2026------------
      df_c_v=df_crias[(pd.to_datetime(df_crias["FECHA_NACIMIENTO"]).dt.year>=2026)&(
         (df_crias["TC_GG_O"]=="CN_C_V")
         |(df_crias["TC_GG_O"]=="CN_C_C")
         |(df_crias["TC_GG_O"]=="IA_C_V"))]

      for contador_comercial in range(len(df_c_v)):
         fecha_parto=pd.to_datetime(df_c_v["FECHA_NACIMIENTO"].values[contador_comercial])
         consecutivo="000"
         consecutivo=consecutivo+str(contador_comercial+1)
         anno=str(fecha_parto)
         mes={"01":"1","02":"2","03":"3","04":"4"
            ,"05":"5","06":"6","07":"7","08":"8"
            ,"09":"9","10":"0","11":"N","12":"D"}.get(anno[5:7])
      
         id=consecutivo[-3:]+"/"+mes+anno[3]
         df_resultado.loc[len(df_resultado)]=[id]+df_c_v.iloc[contador_comercial].tolist()

      df_resultado=df_resultado.sort_values(by="FECHA_NACIMIENTO").reset_index(drop=True)
      df_resultado.insert(5,'EDAD',df_resultado["FECHA_NACIMIENTO"].apply(self.calcular_edad))
      return df_resultado

#vacas por parir
   def prennez(self,df_cria,df_embriones,df_inseminacion,df_servicios,df_palpacion):
      #se sacan las preñadas
      df_prennez=pd.DataFrame(columns=["VACA","FINCA","FEACHA_PREÑEZ","DIAS_DE_PREÑADA","TC"])
      df_embriones=df_embriones[(df_embriones["X1"]=="p+")&(df_embriones["X3"]!="v")&((df_embriones["FINCA"]=="la esperanza")|(df_embriones["FINCA"]=="la lucha"))]
      df_embriones= df_embriones.sort_values("FECHA_TRANSFERENCIA").drop_duplicates("RECEPTORA", keep="last")
      df_inseminacion=df_inseminacion[df_inseminacion["CONFIRMACION"]=="p+"]
      df_inseminacion=df_inseminacion.sort_values("FECHA").drop_duplicates("ID", keep="last")
      df_servicios=df_servicios[df_servicios["ESTADO"]=="p+"][["VACA", "FINCA", "FECHA_SERVICIO","ESTADO"]]
      df_servicios= df_servicios.rename(columns={"FECHA_SERVICIO": "FECHA"})
      df_palpacion=df_palpacion[df_palpacion["ESTADO"]=="p+"][["VACA", "FINCA", "FECHA","DIAS_DE_PREÑEZ","ESTADO"]]
      #print(df_palpacion)
      for i in range(len(df_palpacion)):
         df_palpacion.iloc[0,2]=str(pd.to_datetime(df_palpacion.iloc[i,2])- relativedelta(days=int(df_palpacion.iloc[i,3])))
      df_palpacion=df_palpacion.drop('DIAS_DE_PREÑEZ', axis=1, inplace=True)
      df_natural=pd.concat([df_servicios, df_palpacion], ignore_index=True)
      df_natural=df_natural[df_natural["ESTADO"]=="p+"].sort_values("FECHA").drop_duplicates("VACA", keep="last")
      
      hoy = pd.to_datetime(datetime.today())
      for contar_embriones in range(len(df_embriones)):
         vaca=df_embriones.iloc[contar_embriones,4]
         finca=df_embriones.iloc[contar_embriones,1]
         
         df_partos=df_cria[df_cria["VACA"]==vaca]
         fecha_prennez=pd.to_datetime(df_embriones.iloc[contar_embriones,2])
         confirmar=0
         if len(df_partos)>0:
            for contar_crias in range(len(df_partos)):     
               fecha_parto=pd.to_datetime(df_partos.iloc[contar_crias]["FECHA_NACIMIENTO"])
               if abs((fecha_parto-fecha_prennez).days-280)<45:
                  confirmar+=1
            if confirmar==0:
               df_prennez.loc[len(df_prennez)]=[vaca,finca,fecha_prennez.date(),(hoy-fecha_prennez).days,"TE"]   
         elif len(df_partos)==0:
            df_prennez.loc[len(df_prennez)]=[vaca,finca,fecha_prennez.date(),(hoy-fecha_prennez).days,"TE"]

   #INSEMINACION
      for contar_IA in range(len(df_inseminacion)):
         vaca=df_inseminacion.iloc[contar_IA,1]
         finca=df_inseminacion.iloc[contar_IA,5]
         
         df_partos=df_cria[df_cria["VACA"]==vaca]
         fecha_prennez=pd.to_datetime(df_inseminacion.iloc[contar_IA,0])
         confirmar=0
         if len(df_partos)>0:
            for contar_crias in range(len(df_partos)):     
               fecha_parto=pd.to_datetime(df_partos.iloc[contar_crias]["FECHA_NACIMIENTO"])
               if abs((fecha_parto-fecha_prennez).days-280)<45:
                  confirmar+=1
            if confirmar==0:
               df_prennez.loc[len(df_prennez)]=[vaca,finca,fecha_prennez.date(),(hoy-fecha_prennez).days,"IA"]   
         elif len(df_partos)==0:
            df_prennez.loc[len(df_prennez)]=[vaca,finca,fecha_prennez.date(),(hoy-fecha_prennez).days,"IA"]
   #MONTA NATURAL
      for contar_MN in range(len(df_natural)):
         vaca=df_natural.iloc[contar_MN,0]
         finca=df_natural.iloc[contar_MN,1]
         
         df_partos=df_cria[df_cria["VACA"]==vaca]
         fecha_prennez=pd.to_datetime(df_natural.iloc[contar_MN,2])
         confirmar=0
         if len(df_partos)>0:
            for contar_crias in range(len(df_partos)):     
               fecha_parto=pd.to_datetime(df_partos.iloc[contar_crias]["FECHA_NACIMIENTO"])
               if abs((fecha_parto-fecha_prennez).days-280)<45:
                  confirmar+=1
            if confirmar==0:
               df_prennez.loc[len(df_prennez)]=[vaca,finca,fecha_prennez.date(),(hoy-fecha_prennez).days,"MN"]   
         elif len(df_partos)==0:
            df_prennez.loc[len(df_prennez)]=[vaca,finca,fecha_prennez.date(),(hoy-fecha_prennez).days,"MN"]
      df_prennez=df_prennez.sort_values(by="DIAS_DE_PREÑADA", ascending=False).reset_index(drop=True)
      return df_prennez
      

