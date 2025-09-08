import json
import time
import mysql.connector
from dotenv import load_dotenv
import os
from mysql.connector import Error


load_dotenv()
try:
    db_config = {
        "host": os.getenv("HOST"),
        "user": os.getenv("USER"),
        "password": os.getenv("PW"),
        "database": os.getenv("DB")
    }

except Error as e:
    print("Erro de conexão com o banco:")
    print(3)
    raise


def cliente_existe(cursor, cliente_id):
    cursor.execute("SELECT 1 FROM clientessgc WHERE clientesgc_id = %s", (cliente_id,))
    return cursor.fetchone() is not None


def to_decimal(valor):
    if valor is None or valor == "":
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    return float(str(valor).replace(",", "."))

def inserir_dados(dados_json, batch_size=100):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO pedidosdiariossgc_crc 
        (pedido, clientesgc_id, razao_social, produto, data_pedido, data_credito, 
        tipo, fase, valor, taxa, desconto, estorno, emissao, outros, faturas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Abrir log para registrar clientes inexistentes
        with open("clientes_nao_encontrados.txt", "a", encoding="utf-8") as log_file:

            for i in range(0, len(dados_json), batch_size):
                lote = dados_json[i:i+batch_size]
                valores = []

                for item in lote:
                    cliente_id = item.get("clientesgc_id")

                    # Verifica se o cliente existe no banco
                    if not cliente_existe(cursor, cliente_id):
                        log_file.write(f"Pedido {item.get('pedido')} ignorado - cliente_id {cliente_id} não encontrado\n")
                        continue  # ignora este registro

                    valores.append((
                        item.get("pedido"),
                        cliente_id,
                        item.get("razao_social"),
                        item.get("produto"),
                        item.get("data_pedido"),
                        item.get("data_credito"),
                        item.get("tipo"),
                        item.get("fase"),
                        to_decimal(item.get("valor")),
                        to_decimal(item.get("taxa")),
                        to_decimal(item.get("desconto")),
                        to_decimal(item.get("estorno")),
                        to_decimal(item.get("emissao")),
                        to_decimal(item.get("outros")),
                        item.get("faturas"))
                    )

                if valores:
                    cursor.executemany(sql, valores)
                    conn.commit()
                    print(f"{len(valores)} registros inseridos (até índice {i + len(lote)})")

                time.sleep(5)

    except Exception as e:
        print("Erro ao inserir dados:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
   with open(r"C:\Users\Guilherme.Silva\Desktop\gns\GIMAVE\erp\dados.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

    inserir_dados(dados)
