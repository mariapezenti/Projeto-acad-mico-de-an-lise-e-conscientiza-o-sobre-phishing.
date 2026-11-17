# regras_phishing.py
# Aqui ficam as regras que procuram sinais de phishing no e-mail.
import re

# ---------- Listas de palavras ----------
PALAVRAS_URGENCIA = ["imediatamente", "urgente", "bloqueada", "últimas horas", "expira hoje"]
PALAVRAS_SENHA = ["atualize sua senha", "confirme sua senha", "redefinir sua senha", "sua senha"]
PALAVRAS_BANCARIO = ["cpf", "cartão", "número do cartão", "conta bancária", "cvv"]
ENCURTADORES = ["bit.ly", "tinyurl.com", "t.co", "goo.gl"]


# ---------- Regras ----------
def verificar_urgencia(texto):
    texto = texto.lower()  # tudo minúsculo, pra maiúscula não atrapalhar
    for palavra in PALAVRAS_URGENCIA:
        if palavra in texto:
            return {
                "codigo": "URGENCIA",
                "categoria": "Engenharia social",
                "pontos": 15,
                "descricao": "Linguagem de urgência identificada.",
                "trecho": palavra,
            }
    return None  # não achou nada = regra não ativada


def verificar_pedido_senha(texto):
    texto = texto.lower()
    for palavra in PALAVRAS_SENHA:
        if palavra in texto:
            return {
                "codigo": "PEDIDO_SENHA",
                "categoria": "Dados pessoais",
                "pontos": 25,
                "descricao": "A mensagem pede ou menciona atualização de senha.",
                "trecho": palavra,
            }
    return None


def verificar_dados_bancarios(texto):
    texto = texto.lower()
    for palavra in PALAVRAS_BANCARIO:
        if palavra in texto:
            return {
                "codigo": "DADOS_BANCARIOS",
                "categoria": "Dados pessoais",
                "pontos": 30,
                "descricao": "A mensagem pede dados pessoais ou bancários.",
                "trecho": palavra,
            }
    return None


def verificar_links(texto):
    # acha todos os links que começam com http:// ou https://
    links = re.findall(r"https?://[^\s]+", texto)

    for link in links:
        # link com IP: números separados por ponto logo depois do http://
        if re.match(r"https?://\d+\.\d+\.\d+\.\d+", link):
            return {
                "codigo": "LINK_IP",
                "categoria": "Links",
                "pontos": 25,
                "descricao": "O link usa um endereço IP em vez de um nome de site.",
                "trecho": link,
            }

        # link encurtado: o nome de algum encurtador aparece no link
        for encurtador in ENCURTADORES:
            if encurtador in link:
                return {
                    "codigo": "LINK_ENCURTADO",
                    "categoria": "Links",
                    "pontos": 15,
                    "descricao": "O link é encurtado e esconde o destino real.",
                    "trecho": link,
                }

    return None


# ---------- Teste rápido (sempre por último) ----------
if __name__ == "__main__":
    print(verificar_urgencia("Atualize sua senha IMEDIATAMENTE"))
    print(verificar_pedido_senha("Atualize sua senha agora"))
    print(verificar_dados_bancarios("Informe seu CPF e cartão"))
    print(verificar_dados_bancarios("Segue o material da aula"))
    print(verificar_links("Acesse http://192.168.10.5/login agora"))