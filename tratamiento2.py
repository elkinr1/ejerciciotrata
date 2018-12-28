import pandas as pd

df = pd.read_csv("entrrada.csv",sep="|")   #carga el archivo separado por pipe
lista = ['Call type','Service observed / Traffic sampled',
'Sensor_Type',
'Sensor_ID',
'Recording Office_Type',
'Recording Office_ID',
'Date',
'Timing indicator',
'Study indicator',
'Operator action',
'Service feature code',
'Overseas indicator',
'Time',
'IC / INC indicator',
'Carrier connect date',
'Carrier connect time',
'Carrier elapsed time',
'IC/INC call event status',
'Trunk Group Number',
'IC / INC Routing Indicator',
'Dialing and presubscription indicator',
'ANI / CPN indicator'
]# armo la lista con los campos comunes entre los dos archivos entrada y salida
def functiontime(a):
    if ':' in a:                    # pregunto si tiene esa estructuracon los dospuntos
        min= a.split(':',1)[0]
        seg = a.split(':',1)[1]
        return min*60*1000+seg*1000
    return a                                     #funcion para convertir de minutos a segundos

exportar=df[lista].copy() #  copia del archivo de entrada mas la lista de los comunes
diccionario = {5:"Local message rate call",110:"Interlata call",119:"Incoming CDR",90:None}  #para buscar contenido dentro de uncampo se usa el diccionario en este caso numerico
exportar['Type']= df["Call type"].apply(lambda  x : diccionario[(x)])   # contenido a buscar en el campo call type
#print (exportar.head())
df['trunk'], df['trunk1'] = df["Trunk Identification_Routing Indicator"].str.split(",").str  # separa por coma el contenido de la columna Trunk Identification_Routing Indicator
df['trunk2'], df['trunk3'] = df["Trunk Identification_Trunk Group Number"].str.split(",").str  # separa por coma el contenido de la columna Trunk Identification_Routing Indicator
df['trunk4'], df['trunk5'] = df["Trunk Identification_Trunk Member Number"].str.split(",").str
#############################################################
exportar["m104.trunkid"]=df['trunk'] +":"+df['trunk2']+":"+df['trunk4']   #concateno los campos y los exportoy coloco en m104.trunkid
exportar["m104.trunkid1"]=df['trunk1']+":"+df['trunk3']+":"+df['trunk5']  #concateno los campos y los exportoy coloco en m104.trunkid1
################################
exportar["m119"]=df["Trunk Group_Trunk Group Number - Interoffice"] #asigno campo igual
################################################################################
exportar["originatingnpa"]= df["Calling number"].str[:3]# asigno elcampo callin a originatingnpa  desde la posicion 0 a la 3
exportar["originatingnumber"]=df["Calling number"].str[4:12] # asigno elcampo callin a originatingnumber  desde la posicion 4 a la 12
##############################################################################
exportar["terminatingnpa"]= df["Called number"].str[:3]
exportar["terminatingnumber"]= df["Called number"].str[4:12]
###########################################################################
exportar["elapsedtime"]=df["Length of call"].apply(lambda x: functiontime(str(x)))

###############################################

print (exportar["m104.trunkid"])
print (exportar["m104.trunkid1"])
print  (exportar["m119"])
#print (df['trunk3'])
#####################################################
exportar.to_csv("salidatratamiento2.csv",index=False ,sep="|")#####################  exporta el arcchioseparado por pipe

############################################################



#df["Cabin"] = df["Cabin"].fillna("Desconocido")

#sex = {"male":"M","female":"F"}

#df["Sex"] = df["Sex"].apply(lambda x: sex[x])

#print(df.shape)
#print(df.count())
#print(df.describe())
#print(df["Sex"].head())
#print(df["Sex"].value_counts())
#print(df.groupby(["Sex"])["Survived"].mean()*100)

#print(df)  # imprme todo el archivo