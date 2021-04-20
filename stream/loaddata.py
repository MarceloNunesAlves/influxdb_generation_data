import pandas as pd
import math
import json
from datetime import datetime

def getDados(amplitude):
    periodo = (2*math.pi)/1440 # 1440=Quantidade de minutos no dia
    data_file =  pd.DataFrame(data={"tempo":[val for val in range(1,1441)],
                                    "valor":[((amplitude*math.sin(val*periodo))+(amplitude*1.5)) for val in range(1,1441)]})
    return data_file

def getValor(df, agora):
    index = calcIndex(agora)
    return int(df.loc[index:index]['valor'])

def calcIndex(agora):
    dia = datetime(agora.year, agora.month, agora.day)
    index = 0
    try:
        index = int(abs(((agora - dia).seconds) / 60))
    except:
        # Intervalo de segundos no minuto ZERO
        pass

    return index