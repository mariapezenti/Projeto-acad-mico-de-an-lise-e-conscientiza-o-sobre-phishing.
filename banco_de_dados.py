import sqlite3
from pathlib import Path

# Caminho relativo: funciona em qualquer computador (não usamos C:/Users/...)
PASTA_DADOS = Path(__file__).parent / "dados"
CAMINHO_BANCO = PASTA_DADOS / "phishlab.db"

def conectar():
    PASTA_DADOS.mkdir(exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_BANCO)
    # Permite acessar colunas pelo nome: linha["assunto"]
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabelas():
    conexao = conectar()

    # IF NOT EXISTS: o programa pode iniciar várias vezes sem dar erro nem apagar dados
    # Guardamos o HASH da senha, nunca a senha em texto puro
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            criado_em TEXT NOT NULL
        )
    """)

    # eh_phishing é o gabarito (1 = golpe, 0 = legítimo), usado no treinamento e nos testes
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY,
            remetente_nome TEXT,
            remetente_email TEXT NOT NULL,
            destinatario TEXT,
            assunto TEXT NOT NULL,
            corpo TEXT NOT NULL,
            data_envio TEXT,
            eh_phishing INTEGER NOT NULL
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem_id INTEGER,
            data_hora TEXT NOT NULL,
            pontuacao INTEGER NOT NULL,
            classificacao TEXT NOT NULL,
            indicadores_json TEXT NOT NULL
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS treinamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem_id INTEGER NOT NULL,
            resposta_usuario INTEGER NOT NULL,
            acertou INTEGER NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)

    conexao.commit()  # salva as mudanças
    conexao.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado em:", CAMINHO_BANCO)