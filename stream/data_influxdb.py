from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
'''
    Exemplo de envio
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 127
        }
    }
'''
class ManagerInfluxDB():

    def __init__(self):
        self._client = InfluxDBClient(host='localhost', port=8086, username='myuser', password='mypass')

    def sendData(self, envio):
        try:
            res = self._client.write_points(envio, database='data-test', time_precision="s")
        except InfluxDBClientError as e:
            if "database not found" in str(e):
                res = self._client.create_database('data-test')

        return res