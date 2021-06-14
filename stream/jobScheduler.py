import threading
from stream import loaddata
from stream import data_influxdb
from stream import db_mem
from utils import hashutils, dateutils, numutils
import json

# Dados em memoria
memory_sum_valores = {}

class process():

    def __init__(self, _dados, intervalo, body, amplitude, index, acumulativo, sum_valores):
        self._dados     = _dados
        self.intervalo  = intervalo
        self.body       = body
        self.amplitude  = amplitude
        self.index      = index
        self.acumulativo= acumulativo

        try:
            self.sum_valores = memory_sum_valores[hashutils.gerarHash(json.dumps(self.body))]
        except:
            self.sum_valores = sum_valores

    def run(self):
        if self.body != None:
            self.body.pop('metric', None)
            self.body.pop('data', None)
            self.body.pop('index', None)

            outlier, indice_aplicado = db_mem.getOutlier(hashutils.gerarHash(json.dumps(self.body)), self.index)
            agora = dateutils.dateutils().dataAtual()
            valor = loaddata.getValor(self._dados, agora)
            if outlier != None:
                db_mem.removerOutlier(hashutils.gerarHash(json.dumps(self.body)), self.index)
                valor = valor * indice_aplicado * 1.0
                print('Processando outlier.... >>>><<<<< ', json.dumps(self.body), ' valor: ', str(valor))
            else:
                valor = valor + numutils.calcRandom(self.amplitude, 5)

            if self.acumulativo:
                valor = valor + self.sum_valores
                memory_sum_valores[hashutils.gerarHash(json.dumps(self.body))] = valor

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
            db.sendData(envio)

            print('Dado enviado para o InfluxDB -> ', json.dumps(envio))

def startEvent(_dados, intervalo, body, amplitude, index, acumulativo, sum_valores):
    threading.Timer(intervalo, startEvent, [_dados, intervalo, body, amplitude,
                                            index, acumulativo, sum_valores]).start() #Executa a cada um minuto
    process(_dados, intervalo, body, amplitude, index, acumulativo, sum_valores).run()

