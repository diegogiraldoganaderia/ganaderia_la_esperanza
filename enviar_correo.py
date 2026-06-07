import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from supabase import create_client
import pandas as pd

url ="https://soyjodguzmbiggwymfdn.supabase.co"
key ="sb_secret_bB5UAtzbkyxob7xu_8O4Mw_vwbEkb4K"
from datetime import datetime
supabase = create_client(url, key)
def enviar_correo_diario():
    df=pd.DataFrame(supabase.table("SERVICIO").select("*").execute().data)
    df=df.drop(columns=["index"])
    df=df[df["ESTADO"]=="pendiente"]

    df2=pd.DataFrame(supabase.table("PROTOCOLO").select("*").execute().data)
    df2=df2.drop(columns=["index"])
    df2=df2[df2["PROTOCOLO"]=="pendiente"]


    remitente = "diegogiraldo1304@gmail.com"
    destinatario ="andres-1304@hotmail.com"     #"andres-1304@hotmail.com"
    contrasenia = os.environ.get("EMAIL_PASSWORD")

# 2. Creación del mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = "Reporte Diario De Reproducción 🚀"
    fecha_actual=datetime.now()
    Encabezado1="VACAS SERVIDAS POR EL TORO PENDIENTE DE PLAPACIÓN\n\n"
    contador_servicios=0
    cuerpo=""
    for i in range(len(df)):
        if((fecha_actual-pd.to_datetime(df.iloc[i]["FECHA_SERVICIO"])).days)>=30:
            contador_servicios+=1   
            cuerpo="La vaca "+df.iloc[i]["VACA"]+" Tuvo un servicio del toro "+df.iloc[i]["TORO"]+" el día "+str(df.iloc[i]["FECHA_SERVICIO"])+" ya han pasado "+str(((fecha_actual-pd.to_datetime(df.iloc[i]["FECHA_SERVICIO"])).days))+" días y aún está pendiente la palpación.\n\n"+cuerpo
    
    encabezado2="\nVACAS PARIDAS PENDIENTES DEL PROTOCOLO DE REPRODUCCIÓN\n\n"
    cuerpo2=""
    for i in range(len(df2)):
        if((fecha_actual-pd.to_datetime(df2.iloc[i]["FECHA_PARTO"])).days)>=35:
            contador_servicios+=1   
            cuerpo2="La vaca "+df2.iloc[i]["ID"]+" parió el día "+str(df2.iloc[i]["FECHA_PARTO"])+" ya han pasado "+str(((fecha_actual-pd.to_datetime(df2.iloc[i]["FECHA_PARTO"])).days))+" días y aún está pendiente del protocolo de reprodución.\n\n"+cuerpo2
    



    cuerpototal=Encabezado1+cuerpo+encabezado2+cuerpo2
    mensaje.attach(MIMEText(cuerpototal, "plain"))

    if contador_servicios>0:
        try:
    # 3. Conexión con el servidor de Gmail (SMTP)
            servidor = smtplib.SMTP("smtp.office365.com", 587)#smtp.office365.com smtp.gmail.com
            servidor.starttls() # Conexión segura
    # Iniciar sesión y enviar
            servidor.login(remitente, contrasenia)
            servidor.sendmail(remitente, destinatario, mensaje.as_string())
        except Exception as e:
            print(f"Hubo un error: {e}")
        finally:
            servidor.quit() # Cerrar la conexión
    else:
        pass


if __name__ == "__main__":
    enviar_correo_diario()