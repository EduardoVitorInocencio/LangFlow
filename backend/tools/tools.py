import requests
from time import sleep
from datetime import datetime, UTC
from langchain.agents import tool
from pydantic import BaseModel, Field
import wikipedia

wikipedia.set_lang('en')

class RetornaTempArgs(BaseModel):
    latitude: float = Field(description="Latitude of location where we are looking for the temperature")
    longitude: float = Field(description="Longitude of location where we are looking for the temperature")

@tool(args_schema=RetornaTempArgs)
def actual_temperature_seach(latitude: float, longitude: float):
    '''RETURN THE ACTUAL TEMPERATURE FOR EACH COORDINATE'''
    URL = "https://api.open-meteo.com/v1/forecast"

    PARAMS = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1
    }

    answer = requests.get(URL, params=PARAMS)
    print(answer.status_code)

    if answer.status_code == 200:
        results = answer.json()
        time_now = datetime.now(UTC).replace(tzinfo=None)

        hours_list = [datetime.fromisoformat(temp_str) for temp_str in results['hourly']['time']]
        index_closer = min(range(len(hours_list)), key=lambda x: abs(hours_list[x]-time_now))
        temp_atual = results['hourly']['temperature_2m'][index_closer]
        return temp_atual
    else:
        raise Exception(f'The API request to {URL} failed CODE: {answer.status_code}.')

@tool
def busca_wikipedia(query: str):
    """Faz busca no wikipedia e retorna resumos de páginas para a query"""
    titulos_paginas = wikipedia.search(query)
    resumos = []
    for titulo in titulos_paginas[:3]:
        try:
            wiki_page = wikipedia.page(title=titulo, auto_suggest=True)
            resumos.append(f'Título da página: {titulo}\nResumo: {wiki_page.summary}')
        except:
            pass
    if not resumos:
        return 'Busca não teve retorno'
    else:
        return '\n\n'.join(resumos)

@tool
def find_cep(cep: str):
    """
    Função find_cep:
    Esta função consulta a API de busca de CEP (OpenCEP) para retornar informações de endereço com base no código postal fornecido. 
    Ela aceita um CEP como argumento e retorna um dicionário contendo as seguintes informações:

    - cep: O código postal solicitado.
    - logradouro: O nome da rua ou avenida correspondente ao CEP.
    - complemento: Informações adicionais sobre o endereço, caso existam.
    - bairro: O bairro correspondente ao CEP.
    - localidade: A cidade ou município associado ao CEP.
    - uf: A unidade federativa (estado) relacionada ao CEP.
    - ibge: O código IBGE da cidade ou município.
    - erro: Caso haja algum erro (como um CEP inválido ou falha na conexão), a chave "erro" será preenchida com uma mensagem apropriada.

    A função lida com erros de conexão e falhas na API, retornando informações padrão ou de erro quando necessário. 
    Além disso, inclui uma pausa de 400ms entre as requisições para evitar sobrecarregar a API.
    """
    URL_VIA_CEP = f'https://viacep.com.br/ws/{cep}/json/'
    # URL_VIA_CEP = f'https://opencep.com/v1/{cep}'
    answer = requests.get(URL_VIA_CEP, timeout=5)
    try:
        if answer.ok:
            address_ = answer.json()
            if "erro" in address_:
                resultado = {
                    "cep":"",
                    "logradouro":"",
                    "complemento":"",
                    "bairro":"",
                    "localidade": "",
                    "uf":"",
                    "ibge":"",
                    "erro":"INVALID CEP",
                }
            else:
                resultado={
                    "cep": address_.get("cep",""),
                    "logradouro":address_.get("logradouro",""),
                    "complemento":address_.get("complemento",""),
                    "bairro":address_.get("bairro",""),
                    "localidade":address_.get("localidade",""),
                    "uf":address_.get("uf",""),
                    "ibge":address_.get("ibge",""),
                    "erro":"",
                }
        else:
            resultado = {
                    "cep":"",
                    "logradouro":"",
                    "complemento":"",
                    "bairro":"",
                    "localidade": "",
                    "uf":"",
                    "ibge":"",
                    "erro":f"Erro HTTP {answer.status_code}",
                        }
    except Exception as e:
        resultado = {
            "cep":"",
                    "logradouro":"",
                    "complemento":"",
                    "bairro":"",
                    "localidade": "",
                    "uf":"",
                    "ibge":"",
            "erro": "Erro de conexão",
        }

    # Aguardar para evitar sobrecarregar a API
    sleep(0.4) #900 ms    
    return resultado


@tool
def currency_search(moeda: str):
    """
    Função currency_seach:
    Esta função consulta a API de câmbio para obter a cotação de uma moeda (como 'USD' para o dólar ou 'EUR' para o euro). Ao receber uma pergunta sobre a cotação de uma moeda (ex: "Qual a cotação do dólar?"), a LLM deve identificar o código da moeda (como 'USD') e passar esse código para a função. Ela retorna um dicionário com informações sobre a moeda, incluindo o preço de compra, venda, variação, entre outros dados financeiros.

    A função retorna:
    - 'currency_code': código da moeda (ex: 'USD').
    - 'currency_in': moeda de conversão (ex: 'BRL').
    - 'currency_name': nome completo da moeda (ex: 'Dólar Americano/Real Brasileiro').
    - 'highest_bid', 'lowest_bid', 'bid_price', 'ask_price', 'variation', 'percentage_change', 'timestamp', 'created_at'.

    Exemplo de uso:
    currency_seach(moeda='USD')
    """


    URL = f'https://economia.awesomeapi.com.br/all/{moeda}'
    answer = requests.get(URL, timeout=5)

    if answer.ok:
        currency_info = answer.json()
        if moeda in currency_info:
            # Mapeamento de campos para nomes mais intuitivos
            mapped_info = {
                'currency_code': currency_info[moeda]['code'],       # 'code' -> 'currency_code'
                'currency_in': currency_info[moeda]['codein'],       # 'codein' -> 'currency_in'
                'currency_name': currency_info[moeda]['name'],       # 'name' -> 'currency_name'
                'highest_bid': currency_info[moeda]['high'],         # 'high' -> 'highest_bid'
                'lowest_bid': currency_info[moeda]['low'],           # 'low' -> 'lowest_bid'
                'variation': currency_info[moeda]['varBid'],         # 'varBid' -> 'variation'
                'percentage_change': currency_info[moeda]['pctChange'],  # 'pctChange' -> 'percentage_change'
                'bid_price': currency_info[moeda]['bid'],            # 'bid' -> 'bid_price'
                'ask_price': currency_info[moeda]['ask'],            # 'ask' -> 'ask_price'
                'timestamp': currency_info[moeda]['timestamp'],      # 'timestamp' -> 'timestamp'
                'created_at': currency_info[moeda]['create_date']   # 'create_date' -> 'created_at'
            }
            return mapped_info
        else:
            return {"erro": "Moeda não encontrada ou inválida"}
    else:
        return {"erro": f"Erro HTTP {answer.status_code}"}
