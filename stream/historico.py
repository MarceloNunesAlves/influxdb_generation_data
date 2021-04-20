from stream import data_influxdb
from stream import loaddata
from utils import dateutils, hashutils, numutils
import pandas as pd
import threading
import json

class TaskHistorico(threading.Thread):

    def __init__(self, _dados, _json, _intervalo, _index, _historico_em_dias, _amplitude):
        threading.Thread.__init__(self)
        self._dados             = _dados
        self._json              = _json
        self._intervalo         = _intervalo
        self._index             = _index
        self._historico_em_dias = _historico_em_dias
        self._amplitude         = _amplitude
        self._key_model         = hashutils.key_model(self._json)
        self._key_entity        = hashutils.gerarHash(json.dumps(self._json))
        threading.Thread.name   = self._key_model
        print("Loading old data - " + str(self._json) + " - " + str(self._historico_em_dias))

    def run(self):

        if(self._historico_em_dias>0):

            freqCalc = str(self._intervalo) + 'S'

            db = data_influxdb.ManagerInfluxDB()

            envios = []
            count = 1

            for new_date in pd.date_range(end=dateutils.dateutils().dataAtual(), periods=(self._historico_em_dias*24*60), freq=freqCalc):
                valor = loaddata.getValor(self._dados, new_date)

                envios.append({"measurement": self._index,
                                    "tags": self._json,
                                    "time": new_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                    "fields": {
                                        "value": valor + numutils.calcRandom(self._amplitude, 10) # Metrica calculada
                                    }
                                })

                if count > 300:
                    print("Envio do historico -> " + new_date.strftime("%Y-%m-%d"))
                    db.sendData(envios)
                    envios = []
                    count = 0

                count += 1

            db.sendData(envios)

            print('Fim do processo de geracao do historico...')