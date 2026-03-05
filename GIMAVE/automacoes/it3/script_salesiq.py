import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

# Configurações
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
PORTAL_NAME = "gimave"
DATACENTER = "https://salesiq.zoho.com"  
USUARIO_ATENDENTE = "carolina.procopio@gimave.com.br"  
DATA_INICIO = "2026-02-23"
DATA_FIM = "2026-02-23"

PASTA_SAIDA = "C:/Users/Guilherme.Silva/Desktop/gns/GIMAVE/automacoes/it3"
os.makedirs(PASTA_SAIDA, exist_ok=True)

#1. GERAR ACCESS TOKEN
def gerar_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

#2️. LISTAR CONVERSAS NO PERÍODO
def listar_conversas(access_token, inicio, fim):
    url = f"{DATACENTER}/api/v2/{PORTAL_NAME}/conversations"

    inicio_ts = int(
        datetime.strptime(inicio, "%Y-%m-%d")
        .replace(tzinfo=timezone.utc)
        .timestamp() * 1000
    )

    fim_ts = int(
        datetime.strptime(fim, "%Y-%m-%d")
        .replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
        .timestamp() * 1000
    )

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    todas_conversas = []
    page = 1
    limit = 20

    while True:
        params = {
            "from_time": inicio_ts,
            "to_time": fim_ts,
            "page": page,
            "limit": limit
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json().get("data", [])

        if not data:
            break

        todas_conversas.extend(data)

        print(f"Página {page} carregada ({len(data)} registros)")

        if len(data) < limit:
            break

        page += 1

    return todas_conversas

#2.1 BUSCAR MENSAGENS
def buscar_mensagens_conversa(access_token, conversation_id):
    url = f"{DATACENTER}/api/v2/{PORTAL_NAME}/conversations/{conversation_id}/messages"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    todas_mensagens = []
    cursor = None

    while True:
        params = {
            "limit": 200
        }

        if cursor:
            params["cursor"] = cursor

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ Erro ao buscar mensagens da conversa {conversation_id}")
            print(response.text)
            return None

        response_json = response.json()
        data = response_json.get("data", [])

        if not data:
            break

        todas_mensagens.extend(data)

        info = response_json.get("info", {})
        more_records = info.get("more_records")
        cursor = info.get("next_cursor")

        print(f"   📄 Lote carregado ({len(data)})")

        if not more_records:
            break

    return todas_mensagens

#3. EXPORTAR CONVERSA EM JSON
def salvar_conversas_json(conversas_filtradas):
    caminho_arquivo = os.path.join(PASTA_SAIDA, "conversas_filtradas.json")

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(conversas_filtradas, f, indent=4, ensure_ascii=False)

    print(f"\n✅ JSON salvo em: {caminho_arquivo}")


def main():
    try:
        print("Gerando access token...")
        access_token = gerar_access_token()
        print("✅ Token gerado com sucesso.")

        print("📋 Buscando conversas...")
        conversas = listar_conversas(access_token, DATA_INICIO, DATA_FIM)

        print(f"🔎 Total encontradas (geral): {len(conversas)}")


        resultado_final = []
        for conversa in conversas:

            atendente = conversa.get("attender", {}).get("email")

            #Apenas conversas atribuídas a ela
            if not (atendente and atendente.lower() == USUARIO_ATENDENTE.lower()):
                continue

            conversation_id = conversa.get("id")

            print(f"\n Buscando mensagens da conversa {conversation_id}...")

            mensagens = buscar_mensagens_conversa(access_token, conversation_id)

            if mensagens is None:
                continue

            resultado_final.append({
                "conversation_id": conversation_id,
                "attender": atendente,
                "status": conversa.get("status"),
                "messages": mensagens
            })

            
        print(f"\n📄 Total encerradas no período: {len(resultado_final)}")

        if not resultado_final:
            print("⚠ Nenhuma conversa encerrada encontrada no período.")
            return

        caminho_arquivo = os.path.join(PASTA_SAIDA, "conversas_encerradas.json")

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado_final, f, indent=4, ensure_ascii=False)

        print(f"\n✅ JSON salvo em: {caminho_arquivo}")
        print("\n🎉 Processo finalizado!")

    except Exception as e:
        print("\n💥 Erro geral:")
        print(e)

if __name__ == "__main__":
    main()
