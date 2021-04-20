from flask import Flask
from flask import request
from stream import jobScheduler
from stream import loaddata
from stream import historico
from stream import db_mem
from utils import hashutils
import threading
import json

app = Flask(__name__)

@app.route('/')
def index():
    threads = ''
    for thread in threading.enumerate():
        threads += thread.name + '\n'
    return "Envio de dados no AR.\n\nThreads em execução:\n" + threads


@app.route('/', methods=['POST'])
def incluirElemento():
    requisicao = request.get_json(force=True)

    intervalo = 60.0
    try:
        intervalo = float(requisicao['intervalo'])
    except:
        intervalo = 60.0

    amplitude = 10.0
    try:
        amplitude = float(requisicao['amplitude'])
    except:
        amplitude = 10.0

    dados = loaddata.getDados(amplitude=amplitude)

    index = None
    try:
        index = requisicao['index']
    except:
        # Indice nao informado
        index = 'dados'

    try:
        # Execução em paralelo - Envio para o influxDB do historico
        thread = historico.TaskHistorico(dados, requisicao['chave'].copy(), intervalo, index,
                                         int(requisicao['historico_em_dias']), amplitude)
        thread.start()
    except:
        # Nao sera processado historico
        pass

    jobScheduler.startEvent(dados, intervalo, requisicao['chave'].copy(), amplitude, index)
    return "Job enviado para o InfluxDB!"


@app.route('/', methods=['PUT'])
def gerarOutlier():
    requisicao = request.get_json(force=True)

    index = None
    try:
        index = requisicao['index']
    except:
        # Indice nao informado
        index = 'dados'

    indice_aplicado = None
    try:
        indice_aplicado = requisicao['indice_aplicado']
    except:
        # Valor nao informado
        indice_aplicado = 3 # 3 vezes o valor

    chave = json.dumps(requisicao['chave'])

    db_mem.gerarOutlier(hashutils.gerarHash(chave), index, indice_aplicado)
    return "Outlier registrado: " + chave

if __name__ == '__main__':
    db_mem.initDb()
    app.run(host="0.0.0.0", port=5001)
