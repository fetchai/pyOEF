# pyOEF


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
    "soef_token": "You_Receive_This_From_Register"
 }
```
Both the `unique_url` and the `soef_token` are provided to the user as response from  the register
request.