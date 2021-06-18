# pyOEF

You will need to install Redis Server on your machine (or use docker)
`https://redis.io/download`

extract the zip and then  navigate to the folder from terminal and type:
`make install`

once the installation finished you can start  the server by typing in  terminal:
`redis-server`

### Flush redis:

`GET: http://127.0.0.1:8000/flush`

### Register agent:

`POST: http://127.0.0.1:8000/register`
```buildoutcfg
params: {
    "declared_name": "agent_test",
    "agent_address": "fetch12v8zq7t4fxnx4w7090xznmsyyyd4def02qfuam",
    "chain_identifier": "FetchAI_v2_Testnet_Stable",
    "architecture": "custom",
    "api_key": "TwiCIriSl0mLahw17pyqoA"
}
```

### Acknowledge registration:

`POST: http://127.0.0.1:8000/{unique_url}/acknowledge`
```buildoutcfg
params: {
    "agent_address": "fetch12v8zq7t4fxnx4w7090xznmsyyyd4def02qfuam",
    "soef_token": "You_Receive_This_From_Registration"
 }
```
Both the `unique_url` and the `soef_token` are provided to the user as response from  the register
request.

### Ping:
`GET: http://127.0.0.1:8000/{unique_url}/ping`
```buildoutcfg
params: params: {
    "agent_address": "fetch12v8zq7t4fxnx4w7090xznmsyyyd4def02qfuam",
    "soef_token": "You_Receive_This_From_Registration"
 }
```
or you can do the get request in one  line:

` GET: http://127.0.0.1:8000/{unique_url}/ping?agent_address=fetch1jwrhvszl5a7hh56dg4fu24usljhx8q2set0tu8&soef_token={soef_token}`

### Set Position:
`POST: http://127.0.0.1:8000/{unique_url/set_position`
```buildoutcfg
params: params: {
    "agent_address": "fetch12v8zq7t4fxnx4w7090xznmsyyyd4def02qfuam",
    "soef_token": "You_Receive_This_From_Registration",
    "latitidue": 52.205276,
    "longitude": 0.119167
 }
```

### Set Genus:
`POST: http://127.0.0.1:8000/{unique_url/set_genus`
```buildoutcfg
params: params: {
    "agent_address": "fetch12v8zq7t4fxnx4w7090xznmsyyyd4def02qfuam",
    "soef_token": "You_Receive_This_From_Registration",
    "genus": "Service,
 }
```

### Unregister:

`GET: http://127.0.0.1:8000/{unique_url}/unregister`
```buildoutcfg
params: params: {
    "agent_address": "fetch12v8zq7t4fxnx4w7090xznmsyyyd4def02qfuam",
    "soef_token": "You_Receive_This_From_Registration"
 }
```
or you can do the get request in one  line:

` GET: http://127.0.0.1:8000/{unique_url}/unregister?agent_address=fetch1jwrhvszl5a7hh56dg4fu24usljhx8q2set0tu8&soef_token={soef_token}`

