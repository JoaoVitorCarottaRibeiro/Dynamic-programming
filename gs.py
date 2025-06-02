# Global Solution - Dynamic Programming 

from fpdf import FPDF
import matplotlib.pyplot as pl  
import os

# Criação de uma lista de dicionários denominada de queimadas tendo alguns atributos em seus dicionários, sendo eles: estado, casos, impacto e região, que serão utilizados para determinadas funcionalidades da aplicação. 
queimadas = [
    {"estado": "Acre", "casos": 120, "impacto": "Alto", "regiao": "Norte"},
    {"estado": "Amazonas", "casos": 300, "impacto": "Muito Alto", "regiao": "Norte"},
    {"estado": "Bahia", "casos": 90, "impacto": "Médio", "regiao": "Nordeste"},
    {"estado": "Goiás", "casos": 45, "impacto": "Baixo", "regiao": "Centro-Oeste"},
    {"estado": "Mato Grosso", "casos": 410, "impacto": "Crítico", "regiao": "Centro-Oeste"},
    {"estado": "Pará", "casos": 250, "impacto": "Muito Alto", "regiao": "Norte"},
    {"estado": "Rondônia", "casos": 150, "impacto": "Alto", "regiao": "Norte"},
    {"estado": "Tocantins", "casos": 75, "impacto": "Médio", "regiao": "Norte"}
]

# Criação de um outro dicionário para saber a prioridade de cada caso em cada estado, podendo ter até 5 valores, sendo eles: Crítico, muito alto, alto, médio e baixo.
prioridade = {"Crítico": 5, "Muito Alto": 4, "Alto": 3, "Médio": 2, "Baixo": 1}

# Função de selection sort que irá organizar os estados em ordem alfabética, acessando o atributo "estado" em cada um dos dicionários acima. Primeiramente utilizamos um len() para percorrer o tamanho da lista, depois fizemos um loop com for para percorrer todos os elementos da lista, onde o "i" representa o elemento atual ao qual será comparado com os seguintes. Após isso, adicionamos o menor elemento para a variável "menor" e depois temos um novo loop para percorrer o restante dos elementos da lista, onde o "i + 1" vai encontrar o menor valor. Após isso temos a verificação com o if, se o estado for menor alfabeticamente do que o atual ele passa a ser o menor, sendo jogado a variável "menor". Para finalizar temos a troca de posição "i" com o elemento que possui menor valor, garantindo que o elemento fique na frente, retornando a nova lista organizada.
def ordenar_por_estado(lista):
    percorrer = len(lista)
    for i in range(percorrer):
        menor = i
        for k in range(i + 1, percorrer):
            if lista[k]['estado'].lower() < lista[menor]['estado'].lower():
                menor = k
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista

# Função que exibe visualmente qual opção o usuário terá na hora de entrar em nossa aplicação
def mostrar_menu():
    print("\nBem-vindo ao Firus")
    print("1. Ver todos os estados afetados")
    print("2. Buscar por estado")
    print("3. Inserir novo registro de queimada")
    print("4. Atender próxima ocorrência com maior prioridade")
    print("5. Gerar relatório de atendimento por região (PDF)")
    print("6. Sair")

# Função que exibe todos os estados com base em um for, pegando todas as informações sobre todos os estados presentes na lista de dicionários denominada de queimadas.
def exibir_estados():
    print("\n--- Estados e Queimadas ---")
    for item in queimadas:
        print(f"{item['estado']} | Casos: {item['casos']} | Impacto: {item['impacto']} | Região: {item['regiao']}")

# Função que faz a busca binária dos estados a serem procurados. Primeiramente definimos o início equivalente a 0 e o fim sendo o último elemento da lista. Depois, atribuimos um loop com o while dizendo que enquanto houver elementos para verificar, o loop vai estar funcionando. Após isso, calculamos o índice do elemento central, pois a busca binária sempre analisa o meio do intervalo atual, colocamos ele como o estado atual e depois fazemos uma verificação com if para achar o estado procurado. Caso ele encontre ele vai retornar o estado com o dicionário correspondente, se o estado procurado vier antes do estado atual em ordem alfabética, atualiza o fim da busca para a metade anterior, senão ele atualiza o início da musca para a metade posterior. Por fim, se o loop terminar sem encontrar nenhum estado, ele não retorna nada, indicando que o estado não está presente na lista.
def busca_binaria(estado_procurado):
    inicio = 0
    fim = len(queimadas) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        estado_atual = queimadas[meio]["estado"]

        if estado_atual.lower() == estado_procurado.lower():
            return queimadas[meio]
        elif estado_procurado.lower() < estado_atual.lower():
            fim = meio - 1
        else:
            inicio = meio + 1

    return None

# Função que faz a busca dos estados que estão listados por meio de um input do usuário, retornando o resultado correto trazendo todas as informações ou informando que o estado pesquisado não foi encontrado
def buscar_estado():
    estado = input("\nDigite o nome do estado para buscar: ")
    resultado = busca_binaria(estado)

    if resultado:
        print(f"\nEstado: {resultado['estado']}")
        print(f"Casos de queimadas: {resultado['casos']}")
        print(f"Nível de impacto: {resultado['impacto']}")
        print(f"Região: {resultado['regiao']}")
    else:
        print("Estado não encontrado.")

# Função que permite o usuário inserir uma nova ocorrência de queimada. Nela temos alguns inputs e algumas validações a serem feitas. Primeiramente, temos o input de colocar o estado ao qual a queimada está acontecendo, depois, temos o número de casos. Após esses dois inputs, o usuário terá que informar o impacto e as regiões da queimada apenas com os itens válidos respectivamente, para que não tenha informações incoerentes no final do relatório. Por fim, adicionamos as informações a lista de queimadas por meio de um append()
def inserir_ocorrencia():
    estado = input("Estado: ")
    casos = int(input("Número de casos: "))

    impactos_validos = ["Baixo", "Médio", "Alto", "Muito Alto", "Crítico"]
    regioes_validas = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

    while True:
        impacto = input("Impacto (Baixo, Médio, Alto, Muito Alto, Crítico): ")
        if impacto in impactos_validos:
            break
        print("Valor inválido. Digite um dos seguintes: " + ", ".join(impactos_validos))

    while True:
        regiao = input("Região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul): ")
        if regiao in regioes_validas:
            break
        print("Valor inválido. Digite uma das seguintes: " + ", ".join(regioes_validas))

    queimadas.append({
        "estado": estado,
        "casos": casos,
        "impacto": impacto,
        "regiao": regiao
    })
    print("Ocorrência registrada")


# Função que atende a maior prioridade de queimada. Primeiramente verificamos se a lista de queimadas está vazia, depois usamos a função max() para encontrar o maior valor dentro de uma função lambda para pegar o maior número de impacto nos dicionários que estão dentro da variável queimadas. Após isso utilizamos a função remove() para remover a ocorrência que acabou de ser atendida, para que não haja repetições. Por fim, mostramos ao usuário a ocorrência ao qual foi atendida como prioridade por meio do print.
def atender_maior_prioridade():
    if not queimadas:
        print("Nenhuma ocorrência para atender.")
        return

    ocorrencia_prioritaria = max(queimadas, key=lambda x: prioridade.get(x["impacto"], 0))
    queimadas.remove(ocorrencia_prioritaria)
    print("\nOcorrência atendida:")
    print(f"{ocorrencia_prioritaria['estado']} | Casos: {ocorrencia_prioritaria['casos']} | Impacto: {ocorrencia_prioritaria['impacto']}")

#Função que gera um relatório em PDF com os dados das queimadas por região. Primeiramente, criamos o objeto PDF utilizando a biblioteca FPDF, adicionamos uma nova página e definimos a fonte do documento. Em seguida, escrevemos o título centralizado na primeira linha do relatório. Depois disso, organizamos as ocorrências de queimadas por região utilizando um dicionário, onde a chave é a região e o valor é uma lista de dicionários com os dados de cada estado. Depois, calculamos o total de casos por região utilizando a função sum() dentro de um dicionário por compreensão. Na sequência, percorremos sobre cada região e seus dados para escrever as informações no PDF, destacando o nome da região e listando os estados com seus respectivos casos e níveis de impacto. Após isso, criamos um gráfico de barras com o total de casos por região usando a biblioteca matplotlib, salvamos a imagem e a adicionamos como uma nova página no PDF. Por fim, o relatório é salvo como “relatorio_queimadas.pdf”, exibimos uma mensagem ao usuário informando que o relatório foi gerado com sucesso, e removemos o gráfico do sistema para evitar arquivos temporários desnecessários.
def gerar_relatorio_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Queimadas por Região", ln=True, align='C')
    pdf.ln(10)

    regioes = {}
    for item in queimadas:
        reg = item["regiao"]
        regioes.setdefault(reg, []).append(item)

    total_por_regiao = {regiao: sum(d["casos"] for d in dados) for regiao, dados in regioes.items()}

    for regiao, dados in regioes.items():
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=f"Região: {regiao}", ln=True)
        pdf.set_font("Arial", size=12)
        for item in dados:
            linha = f"{item['estado']} | Casos: {item['casos']} | Impacto: {item['impacto']}"
            pdf.cell(200, 10, txt=linha, ln=True)
        pdf.ln(5)

    plt.figure(figsize=(8, 5))
    plt.bar(total_por_regiao.keys(), total_por_regiao.values(), color='darkred')
    plt.xlabel("Região")
    plt.ylabel("Total de Casos")
    plt.title("Total de Casos de Queimadas por Região")
    plt.tight_layout()
    grafico = "grafico_queimadas.png"
    plt.savefig(grafico)
    plt.close()

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Gráfico: Queimadas por Região", ln=True, align="C")
    pdf.image(grafico, x=30, y=30, w=150)

    pdf.output("relatorio_queimadas.pdf")
    print("Relatório com gráfico gerado: relatorio_queimadas.pdf")

    os.remove(grafico)

#Função principal que controla o menu do sistema. Ela entra em um loop infinito com while True para manter o programa funcionando até o usuário decidir sair. De acordo com o que o usuário escolher, o sistema vai entender e executar a determinada função. Caso o usuário digite "6" o programa se encerra.
def main():
    while True:
        ordenar_por_estado(queimadas)
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_estados()
        elif opcao == "2":
            buscar_estado()
        elif opcao == "3":
            inserir_ocorrencia()
        elif opcao == "4":
            atender_maior_prioridade()
        elif opcao == "5":
            gerar_relatorio_pdf()
        elif opcao == "6":
            print("Até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
