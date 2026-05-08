"""
ANALISADOR DE SENTIMENTOS - PROJETO EDUCACIONAL
Programa que analisa se uma frase é positiva, negativa ou neutra
Autor: Turma de Projeto Integrador
"""

import os


# =============================================================================
# PARTE 1: CARREGAR O SENTILEX
# =============================================================================

def carregar_sentilex(caminho_arquivo):
    sentimentos = {}

    if not os.path.exists(caminho_arquivo):
        print(f"⚠️ Arquivo {caminho_arquivo} não encontrado!")
        return sentimentos

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(";")

            if len(partes) > 1:
                # Extrai a palavra principal
                palavra = partes[0].split(",")[0].lower().strip()

                polaridade_final = 0
                
                # Percorre todas as partes da linha (N0, N1, etc.)
                for p in partes:
                    if "POL:" in p:
                        try:
                            # Extrai o número após o '='
                            valor = int(p.split("=")[1].strip())
                            # Se acharmos um valor diferente de zero, esse é o real!
                            if valor != 0:
                                polaridade_final = valor
                                break # Encontrou o sentimento, pode parar
                        except:
                            continue
                
                # Só adiciona se a palavra tiver algum sentimento (diferente de 0)
                if polaridade_final != 0:
                    sentimentos[palavra] = polaridade_final

    return sentimentos


# =============================================================================
# PARTE 2: LIMPAR TEXTO
# =============================================================================

def limpar_texto(texto):
    pontuacoes = ".,!?;:()-\"'…"
    texto = texto.lower()

    for p in pontuacoes:
        texto = texto.replace(p, "")

    return texto


# =============================================================================
# PARTE 3: ANÁLISE
# =============================================================================

def analisar_sentimento(frase, lexico):
    frase = limpar_texto(frase)
    palavras = frase.split()

    score = 0
    positivas = []
    negativas = []

    for palavra in palavras:
        if palavra in lexico:
            polaridade = lexico[palavra]

            if polaridade > 0:
                positivas.append(palavra)
            elif polaridade < 0:
                negativas.append(palavra)

            score += polaridade

    return score, positivas, negativas


# =============================================================================
# PARTE 4: INTERFACE
# =============================================================================

def linha():
    print("=" * 50)


def mostrar_resultado(frase, score, pos, neg):
    linha()
    print("RESULTADO")
    linha()

    print(f"Frase: {frase}\n")

    print(f"Score total: {score}")
    print(f"Positivas ({len(pos)}): {', '.join(pos) if pos else '-'}")
    print(f"Negativas ({len(neg)}): {', '.join(neg) if neg else '-'}")

    if score > 0:
        print("\n😊 Sentimento: POSITIVO")
    elif score < 0:
        print("\n😞 Sentimento: NEGATIVO")
    else:
        print("\n😐 Sentimento: NEUTRO")

    linha()


# =============================================================================
# PARTE 5: MENU PRINCIPAL
# =============================================================================

def main():
    lexico_flex = carregar_sentilex("SentiLex-flex-PT02.txt")
    lexico_lem = carregar_sentilex("SentiLex-lem-PT02.txt")

    lexico = {**lexico_lem, **lexico_flex}

    print(f"Polaridade de 'odeio': {lexico.get('odeio')}")

    if not lexico:
        print("Erro ao carregar o léxico. Encerrando...")
        return

    while True:
        linha()
        print("ANALISADOR DE SENTIMENTOS")
        linha()
        print("1 - Analisar frase")
        print("2 - Estatísticas")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        if opcao == "1":
            frase = input("\nDigite uma frase: ").strip()

            if not frase:
                print("⚠️ Frase vazia!")
                continue

            score, pos, neg = analisar_sentimento(frase, lexico)
            mostrar_resultado(frase, score, pos, neg)

        elif opcao == "2":
            positivos = sum(1 for v in lexico.values() if v > 0)
            negativos = sum(1 for v in lexico.values() if v < 0)

            linha()
            print("ESTATÍSTICAS")
            linha()
            print(f"Total de palavras: {len(lexico)}")
            print(f"Positivas: {positivos}")
            print(f"Negativas: {negativos}")
            linha()

        elif opcao == "0":
            print("\n👋 Encerrando programa...")
            break

        else:
            print("⚠️ Opção inválida!")


# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()
