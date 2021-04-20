import threading
from stream import loaddata
from stream import data_influxdb
from stream import db_mem
from utils import hashutils, dateutils, numutils
import json

class process():
    def __init__(self, _dados, intervalo, body, amplitude, index):
        self._dados     = _dados
        self.intervalo  = intervalo
        self.body       = body
        self.amplitude  = amplitude
        self.index      = index

    def run(self):
        if self.body != None:
            self.body.pop('metric', None)
            self.body.pop('data', None)
            self.body.pop('index', None)

            outlier, indice_aplicado = db_mem.getOutlier(hashutils.gerarHash(json.dumps(self.body)), self.index)
            agora = dateutils.dateutils().dataAtual()
            valor = loaddata.getValor(self._dados, agora)
            if outlier != None:
                print('Processando outlier.... >>>><<<<< ' + json.dumps(self.body))
                db_mem.removerOutlier(hashutils.gerarHash(json.dumps(self.body)), self.index)
                valor = valor * indice_aplicado
            else:
                valor = valor + numutils.calcRandom(self.amplitude, 0.05)

            db = data_influxdb.ManagerInfluxDB()

            envio = [
                        {
                            "measurement": self.index,
                            "tags": self.body,
                            "time": agora.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "fields": {
                                "value": valor  # Metrica calculada
                            }
                        }
                    ]
            # TODO: Arrumar o json de envio
            res = db.sendData(envio)

            print('Status do InfluxDB -> ' + str(res))

def startEvent(_dados, intervalo, body, amplitude, index):
    threading.Timer(intervalo, startEvent, [_dados, intervalo, body, amplitude, index]).start() #Executa a cada um minuto
    process(_dados, intervalo, body, amplitude, index).run()

