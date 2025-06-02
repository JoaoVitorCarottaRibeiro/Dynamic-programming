from fpdf import FPDF
import matplotlib.pyplot as plt
import os

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

prioridade = {"Crítico": 5, "Muito Alto": 4, "Alto": 3, "Médio": 2, "Baixo": 1}

def ordenar_por_estado(lista):
    percorrer = len(lista)
    for i in range(percorrer):
        menor = i
        for k in range(i + 1, percorrer):
            if lista[k]['estado'].lower() < lista[menor]['estado'].lower():
                menor = k
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista

def mostrar_menu():
    print("\nBem-vindo ao Firus")
    print("1. Ver todos os estados afetados")
    print("2. Buscar por estado")
    print("3. Inserir novo registro de queimada")
    print("4. Atender próxima ocorrência com maior prioridade")
    print("5. Gerar relatório de atendimento por região (PDF)")
    print("6. Sair")

def exibir_estados():
    print("\n--- Estados e Queimadas ---")
    for item in queimadas:
        print(f"{item['estado']} | Casos: {item['casos']} | Impacto: {item['impacto']} | Região: {item['regiao']}")

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

def inserir_ocorrencia():
    estado = input("Estado: ")
    casos = int(input("Número de casos: "))

    # Valores permitidos
    impactos_validos = ["Baixo", "Médio", "Alto", "Muito Alto", "Crítico"]
    regioes_validas = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

    # Validação do impacto
    while True:
        impacto = input("Impacto (Baixo, Médio, Alto, Muito Alto, Crítico): ")
        if impacto in impactos_validos:
            break
        print("Valor inválido. Digite um dos seguintes: " + ", ".join(impactos_validos))

    # Validação da região
    while True:
        regiao = input("Região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul): ")
        if regiao in regioes_validas:
            break
        print("Valor inválido. Digite uma das seguintes: " + ", ".join(regioes_validas))

    # Adiciona a nova ocorrência
    queimadas.append({
        "estado": estado,
        "casos": casos,
        "impacto": impacto,
        "regiao": regiao
    })
    print("Ocorrência registrada")


def atender_maior_prioridade():
    if not queimadas:
        print("Nenhuma ocorrência para atender.")
        return

    ocorrencia_prioritaria = max(queimadas, key=lambda x: prioridade.get(x["impacto"], 0))
    queimadas.remove(ocorrencia_prioritaria)
    print("\nOcorrência atendida:")
    print(f"{ocorrencia_prioritaria['estado']} | Casos: {ocorrencia_prioritaria['casos']} | Impacto: {ocorrencia_prioritaria['impacto']}")


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

    # Dados para o gráfico
    total_por_regiao = {regiao: sum(d["casos"] for d in dados) for regiao, dados in regioes.items()}

    for regiao, dados in regioes.items():
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=f"Região: {regiao}", ln=True)
        pdf.set_font("Arial", size=12)
        for item in dados:
            linha = f"{item['estado']} | Casos: {item['casos']} | Impacto: {item['impacto']}"
            pdf.cell(200, 10, txt=linha, ln=True)
        pdf.ln(5)

    # Criar gráfico
    plt.figure(figsize=(8, 5))
    plt.bar(total_por_regiao.keys(), total_por_regiao.values(), color='darkred')
    plt.xlabel("Região")
    plt.ylabel("Total de Casos")
    plt.title("Total de Casos de Queimadas por Região")
    plt.tight_layout()
    grafico = "grafico_queimadas.png"
    plt.savefig(grafico)
    plt.close()

    # Inserir gráfico no PDF
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Gráfico: Queimadas por Região", ln=True, align="C")
    pdf.image(grafico, x=30, y=30, w=150)

    # Gerar PDF
    pdf.output("relatorio_queimadas.pdf")
    print("Relatório com gráfico gerado: relatorio_queimadas.pdf")

    # Limpar imagem temporária
    os.remove(grafico)

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
