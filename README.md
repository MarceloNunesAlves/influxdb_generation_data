# Geração de dados de series temporais (InfluxDB)

#Criação do ambiente

Para este teste simples é importante que o ambiente do python possua todos os pacotes necessários.

Para criar um ambiente python com os pacotes necessários.

Criar o ambiente no Anaconda

```
conda create -n influx_env
conda activate influx_env
conda install python
pip install influxdb
pip install flask
```


Para subir a aplicação (Porta: 5001)

```
python main_api.py
```

## Exemplos de chamada da API

Inclusão de dados no influxDB

Metodo: POST

```
{
	"historico_em_dias": "15",
	"intervalo": "60",
	"index": "serie",
	"amplitude": 30,
	"chave":
	{
		"campo_1": "Valor X",
		"campo_2": "Valor Y"
	}
}
```

Inclusão de dados no influxDB (Acumulativo)

Metodo: POST

```
{
	"historico_em_dias": "15",
	"intervalo": "60",
	"index": "serie",
	"amplitude": 30,
	"acumulativo": "True",
	"chave":
	{
		"campo_1": "Valor X",
		"campo_2": "Valor Y"
	}
}
```

Inclusão de anomalia

Metodo: PUT

```
{
	"index": "serie",
	"indice_aplicado": 1.5,
	"chave":
	{
		"campo_1": "Valor X",
		"campo_2": "Valor Y"
	}
}
```

Verificar threads em execução

Metodo: GET

```
{}
```