# Prophet

## Synopsis
Aplicacion que captura tweets con python y envia a un topic de Kafka
Un KafkaConsumer se encarga de enviar los tweets a ElasticSearch y los clasifica con Watson
en ElasticSearch se guarda el id del tweet, texto, tags y la informacion del usuario

## Instalacion

### 1 Crear un entorno virtual
```virtualenv -p /usr/bin/python3.5 env ```

### 2 Activar el entorno
```source env/bin/activate```

### 3 Instalar las bibliotecas
```pip install -r requirements.txt```

### 4 Crear tokens.py
```python
import os

os.environ['CONSUMER_KEY']      = "YOUR_CONSUMER_KEY"
os.environ['CONSUMER_SECRET']   = "YOUR_CONSUMER_SECRET"
os.environ['ACCESS_TOKEN']      = "YOUR_ACCESS_TOKEN"
os.environ['ACCESS_TOKEN_SECRET'] = "YOUR_ACCESS_TOKEN_SECRET"
```

### 5 Correr el contenedor [spotify/kafka](https://hub.docker.com/r/spotify/kafka/)
```docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka```

### 6 Correr el contenedor de ElasticSearch
```
docker run -d -p 9200:9200 -e "http.host=0.0.0.0" -e "transport.host=127.0.0.1" -e "xpack.security.enabled=false" \
-e "network.bind_host=0.0.0.0"  docker.elastic.co/elasticsearch/elasticsearch:5.3.1
```

### 7 Ejecutar el [TweetStream.py](https://github.com/OswaldoCuzSimon/ETL_tweet/blob/master/TweetStream.py) y [TweetConsumer.py](https://github.com/OswaldoCuzSimon/ETL_tweet/blob/master/TweetConsumer.py)
```shell
python TweetStream.py
```
```shell
python TweetConsumer.py
```

### Good Luck
