## ONBOARDING US TO UPDATE DATA RELATED TO BROKER MEMBERS
#### _FISSION PARA ATUALIZAÇÃO DOS DADOS RELACIONADOS A MEMBROS DE CORRETORA
___
### Esse projeto refere-se a rota do Sphinx:

```
UserService.update_exchange_member_us
```
&nbsp; 
### 1.1. `update_exchange_member_us`
&nbsp; 
#### MODELO DE REQUISIÇÃO:

```http://127.0.0.1:9000/update-exchange-member```

&nbsp; 
##### BODY REQUEST
```
{
    "time_experience": "10"
}
```
&nbsp;

#### MODELO DE RESPOSTA:

```
{
    "result": true,
    "message": "XXXXXX",
    "success": true,
    "code": 200
}

```
&nbsp;
#### RODAR SCRIPT DE TESTS:

- No mesmo nível da pasta root, rodar o seguinte comando no terminal: `bash tests.sh`

&nbsp;