from pulp import *

# --------------------------
# Dados do problema
# --------------------------

# Cidades e a produção esperada das árvores por m³/hectare
producao_esperada = {
    "Cidade_1": {"Pinus": 17, "Carvalho": 14, "Nogueira": 10, "Araucacia": 9},
    "Cidade_2": {"Pinus": 15, "Carvalho": 16, "Nogueira": 12, "Araucacia": 11},
    "Cidade_3": {"Pinus": 13, "Carvalho": 12, "Nogueira": 14, "Araucacia": 8},
    "Cidade_4": {"Pinus": 10, "Carvalho": 11, "Nogueira": 8, "Araucacia": 6}
}

# Produção mínima para cada árvore
producao_minima = {
    "Pinus": 225 * 1000,
    "Carvalho": 9 * 1000,
    "Nogueira": 4.8 * 1000,
    "Araucacia": 3.5 * 1000
}

# Área disponível para plantio em cada cidade
area_disponivel = {
    "Cidade_1": 1500,
    "Cidade_2": 1700,
    "Cidade_3": 900,
    "Cidade_4": 600
}

# Renda anual esperada em cada cidade
renda_esperada = {
    "Cidade_1": {"Pinus": 16, "Carvalho": 12, "Nogueira": 20, "Araucacia": 18},
    "Cidade_2": {"Pinus": 14, "Carvalho": 13, "Nogueira": 24, "Araucacia": 20},
    "Cidade_3": {"Pinus": 17, "Carvalho": 10, "Nogueira": 28, "Araucacia": 20},
    "Cidade_4": {"Pinus": 12, "Carvalho": 11, "Nogueira": 18, "Araucacia": 17}
}

# --------------------------
# Modelagem com PuLP
# --------------------------

# Inicializando o problema
prob = LpProblem("Reflorestamento", LpMaximize)

# Criando listas que contém as cidades e as árvores
lista_cidades = list(area_disponivel.keys())
lista_arvores = list(producao_minima.keys())

# Variáveis de decisão (áreas de plantio de cada árvore em cada cidade)
plantio = {(cidade, arvore): LpVariable(f"area {cidade}{arvore}", lowBound = 0, cat = 'Continuous') for cidade in lista_cidades for arvore in lista_arvores}

# Função objetivo (maximizar a renda)
prob += lpSum(renda_esperada[cidade][arvore] * plantio[(cidade, arvore)] for cidade in lista_cidades for arvore in lista_arvores), "Renda_Total"

# Restrição da área disponível para plantio
for cidade in lista_cidades:
    prob += (
        lpSum(plantio[(cidade, arvore)] for arvore in lista_arvores) <= area_disponivel[cidade], f"Area_Disponivel_{cidade}"
    )

# Restrição da produção mínima
for arvore in lista_arvores:
    prob += (
        lpSum(producao_esperada[cidade][arvore] * plantio[(cidade, arvore)] for cidade in lista_cidades) >= producao_minima[arvore], f"Producao_Mínima_{arvore}"
    )

# --------------------------
# Solução
# --------------------------

prob.solve()

# --------------------------
# Relatório
# --------------------------

print(f"Status: {LpStatus[prob.status]}\n")

# Encontrou uma solução ótima
if prob.status == LpStatusOptimal:
    print(f"Renda total máxima: R$ {prob.objective.value():.2f}\n")

    print("Áreas de plantio por cidade e árvore:\n")
    for cidade in lista_cidades:
        print(f"{cidade}:")
        for arvore in lista_arvores:
            valor_area = plantio[(cidade, arvore)].varValue
            # Exibe apenas as áreas que serão plantadas maior que zero
            #if valor_area > 0:
            print(f"- {arvore}: {valor_area:.2f} hectares")
        print("\n")

# Caso não encontre uma solução ótima
else:
    print("Não foi encontrada uma solução ótima")
