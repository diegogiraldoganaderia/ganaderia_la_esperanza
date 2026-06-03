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
    remitente = "diegogiraldo1304@gmail.com"
    destinatario = "andres-1304@hotmail.com"
    contrasenia = os.environ.get("EMAIL_PASSWORD")

# 2. Creación del mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = "Reporte Diario Palpación animales por monta natural 🚀"
    fecha_actual=datetime.now()
    cuerpo=""
    contador_servicios=0
    
    for i in range(len(df)):
        if((fecha_actual-pd.to_datetime(df.iloc[i]["FECHA_SERVICIO"])).days)>=30:
            contador_servicios+=1   
            cuerpo="La vaca "+df.iloc[i]["VACA"]+" Tuvo un servicio del el toro "+df.iloc[i]["TORO"]+" el día "+str(df.iloc[i]["FECHA_SERVICIO"])+" ya han pasado "+str(((fecha_actual-pd.to_datetime(df.iloc[i]["FECHA_SERVICIO"])).days))+" días y aún está pendiente la palpación.\n\n"+cuerpo
    mensaje.attach(MIMEText(cuerpo, "plain"))
    
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