# analisador.py
# Parte do Integrante 2 (análise de phishing)
# Giovanna: é só chamar analisar_mensagem(mensagem) e usar o que ela devolver.

from regras_phishing import verificar_urgencia, verificar_pedido_senha, verificar_dados_bancarios, verificar_links

def analisar_mensagem(mensagem):
    # mensagem é um dicionário com: remetente_nome, remetente_email, assunto, corpo
    # .get(..., "") evita erro se algum campo não vier
    assunto = mensagem.get("assunto", "")
    corpo = mensagem.get("corpo", "")
    texto = assunto + " " + corpo

    # Chama cada regra. Se ela achou algo, vem uma ficha. Se não, vem None.
    resultados = [
        verificar_urgencia(texto),
        verificar_pedido_senha(texto),
        verificar_dados_bancarios(texto),
        verificar_links(texto),
    ]

    # Fica só com as regras que acharam algo (tira os None)
    indicadores = []
    for r in resultados:
        if r is not None:
            indicadores.append(r)

    # Soma os pontos de todos os indicadores
    pontuacao = 0
    for ind in indicadores:
        pontuacao = pontuacao + ind["pontos"]

    if pontuacao > 100:
        pontuacao = 100  # a nota nunca passa de 100

    # Define o nível de risco pela pontuação
    if pontuacao >= 60:
        classificacao = "ALTO"
    elif pontuacao >= 30:
        classificacao = "MEDIO"
    else:
        classificacao = "BAIXO"

    return {
        "pontuacao": pontuacao,
        "classificacao": classificacao,
        "indicadores": indicadores,
        "recomendacoes": ["Não clique em links desta mensagem."],
        "links_analisados": [],
    }


# Teste rápido
if __name__ == "__main__":
    golpe = {
        "assunto": "Sua conta será bloqueada",
        "corpo": "Atualize sua senha imediatamente. Informe seu CPF.",
    }
    normal = {
        "assunto": "Material da aula",
        "corpo": "Oi pessoal, segue o material.",
    }
    for m in [golpe, normal]:
        r = analisar_mensagem(m)
        print(r["classificacao"], r["pontuacao"])