from stream import data_influxdb
from stream import loaddata
from utils import dateutils, hashutils, numutils
import pandas as pd
import json

def TaskHistorico(_dados, _json, _intervalo, _index, _historico_em_dias, _amplitude, acumulativo):
        _key_model         = hashutils.key_model(_json)
        _key_entity        = hashutils.gerarHash(json.dumps(_json))
        print("Loading old data - " + str(_json) + " - " + str(_historico_em_dias))

        sum_valores = 0

        if(_historico_em_dias>0):

            freqCalc = str(_intervalo) + 'S'

            db = data_influxdb.ManagerInfluxDB()

            envios = []
            count = 1
            end_date = dateutils.dateutils().dataAtual()
            end_date = dateutils.dateutils().addMinutes(end_date, -1)

            for new_date in pd.date_range(end=end_date, periods=(_historico_em_dias*24*60), freq=freqCalc):
                valor = loaddata.getValor(_dados, new_date)
                valor = valor + numutils.calcRandom(_amplitude, 15)
                sum_valores += valor

                dict_envio = {"measurement": _index,
                                    "tags": _json,
                                    "time": new_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                    "fields": {
                                        "value": valor # Metrica calculada
                                    }
                                }

                if acumulativo:
                    dict_envio['fields']['value'] = sum_valores

                envios.append(dict_envio)

                if count > 300:
                    print("Envio do historico -> " + new_date.strftime("%Y-%m-%d"))
                    db.sendData(envios)
                    envios = []
                    count = 0

                count += 1

            db.sendData(envios)

            print('Fim do processo de geracao do historico...')

        return sum_valores