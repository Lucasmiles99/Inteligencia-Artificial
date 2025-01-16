import random
import matplotlib.pyplot as plt
import numpy as np

# Representação do indivíduo
class Individuo:
    def __init__(self, tipo):
        self.tipo = tipo  # "presa" ou "predador"
        if tipo == "presa":
            self.genes = np.random.randint(1, 11, size=3)  # Velocidade, Camuflagem, Reprodução
        elif tipo == "predador":
            self.genes = np.random.randint(1, 11, size=3)  # Velocidade, Eficiência, Reprodução
        self.fitness = 0

    def avaliar_fitness(self):
        if self.tipo == "presa":
            self.fitness = self.genes[0] + self.genes[1]  # Velocidade + Camuflagem
        elif self.tipo == "predador":
            self.fitness = self.genes[0] + self.genes[1]  # Velocidade + Eficiência

# Funções auxiliares para seleção, cruzamento e mutação
def selecao_torneio(populacao):
    if len(populacao) < 3:
        return max(populacao, key=lambda x: x.fitness)
    return max(random.sample(populacao, 3), key=lambda x: x.fitness)

def selecao_por_torneio(populacao):
    # Escolhe três indivíduos aleatoriamente
    torneio = random.sample(populacao, 3)
    
    # Encontra o vencedor com maior fitness
    vencedor = max(torneio, key=lambda individuo: individuo['fitness'])
    
    # Exibe informações no console
    fitness_torneio = [individuo['fitness'] for individuo in torneio]
    print(f"Subconjunto escolhido: Fitness de {fitness_torneio}")
    print(f"Vencedor: Fitness {vencedor['fitness']}")
    
    return vencedor

# Exemplo de uso
populacao = [
    {'id': 1, 'fitness': 12},
    {'id': 2, 'fitness': 15},
    {'id': 3, 'fitness': 8},
    {'id': 4, 'fitness': 20},
    {'id': 5, 'fitness': 10},
]

pai = selecao_por_torneio(populacao)

def cruzamento(pai1, pai2):
    ponto = random.randint(1, len(pai1.genes) - 1)
    filho1_genes = np.concatenate((pai1.genes[:ponto], pai2.genes[ponto:]))
    filho2_genes = np.concatenate((pai2.genes[:ponto], pai1.genes[ponto:]))
    filho1 = Individuo(pai1.tipo)
    filho2 = Individuo(pai1.tipo)
    filho1.genes = filho1_genes
    filho2.genes = filho2_genes
    return filho1, filho2

def cruzar(pai1, pai2):
    # Seleciona um ponto de cruzamento aleatório
    ponto_cruzamento = random.randint(1, len(pai1) - 1)
    
    # Realiza o cruzamento dos genes
    filho1 = pai1[:ponto_cruzamento] + pai2[ponto_cruzamento:]
    filho2 = pai2[:ponto_cruzamento] + pai1[ponto_cruzamento:]
    
    # Exibe informações no console
    print(f"Genes do Pai 1: {pai1}")
    print(f"Genes do Pai 2: {pai2}")
    print(f"Ponto de cruzamento: {ponto_cruzamento}")
    print(f"Filho 1: {filho1}")
    print(f"Filho 2: {filho2}")
    
    return filho1, filho2

# Exemplo de uso
pai1 = [8, 7, 5]
pai2 = [6, 9, 4]
filho1, filho2 = cruzar(pai1, pai2)

def mutacao(individuo, taxa=0.005):
    for i in range(len(individuo.genes)):
        if random.random() < taxa:
            individuo.genes[i] = random.randint(1, 10)

# Inicializa população
def inicializar_populacao(tamanho, tipo):
    return [Individuo(tipo) for _ in range(tamanho)]

def ciclo_evolutivo(populacao_presas, populacao_predadores, taxa_mutacao=0.005):
    nova_populacao_presas = []
    nova_populacao_predadores = []

    # Avalia fitness
    for presa in populacao_presas:
        presa.avaliar_fitness()
    for predador in populacao_predadores:
        predador.avaliar_fitness()

    # Reproduz presas
    while len(nova_populacao_presas) < len(populacao_presas):
        pai1 = selecao_torneio(populacao_presas)
        pai2 = selecao_torneio(populacao_presas)
        filho1, filho2 = cruzamento(pai1, pai2)
        mutacao(filho1, taxa_mutacao)
        mutacao(filho2, taxa_mutacao)
        nova_populacao_presas.extend([filho1, filho2])

    # Reproduz predadores
    while len(nova_populacao_predadores) < len(populacao_predadores):
        pai1 = selecao_torneio(populacao_predadores)
        pai2 = selecao_torneio(populacao_predadores)
        filho1, filho2 = cruzamento(pai1, pai2)
        mutacao(filho1, taxa_mutacao)
        mutacao(filho2, taxa_mutacao)
        nova_populacao_predadores.extend([filho1, filho2])

    # Ajusta populações para o tamanho inicial
    nova_populacao_presas = nova_populacao_presas[:len(populacao_presas)]
    nova_populacao_predadores = nova_populacao_predadores[:len(populacao_predadores)]

    return nova_populacao_presas, nova_populacao_predadores

def variação_ambiental(geracao):
    if geracao % 10 == 0:  # A cada 10 gerações, muda o ambiente
        return np.random.choice(["visibilidade_alta", "velocidade_alta"])
    return None

def ajustar_fitness_por_ambiente(individuos, ambiente):
    for individuo in individuos:
        if ambiente == "visibilidade_alta" and individuo.tipo == "presa":
            individuo.fitness += individuo.genes[1]  # Camuflagem se torna mais importante
        elif ambiente == "velocidade_alta":
            individuo.fitness += individuo.genes[0] 

# Interações diretas: Captura de presas
def interagir(presas, predadores):
    capturas = 0
    sobreviventes_presas = []

    for presa in presas:
        capturado = False
        for predador in predadores:
            if predador.genes[0] >= presa.genes[0]:  # Velocidade do predador >= Velocidade da presa
                chance_de_fuga = random.uniform(0, 1)
                if chance_de_fuga < 0.3:  # 30% de chance de escapar
                    capturado = False
                else:
                    capturado = True
                    capturas += 1
                    break
            if not capturado:
                sobreviventes_presas.append(presa)

    return sobreviventes_presas

# Gráficos
def plotar_graficos(historico_presas, historico_predadores):
    geracoes = range(1, len(historico_presas) + 1)

    plt.figure(figsize=(12, 8))

    # População total ao longo das gerações
    plt.subplot(2, 1, 1)
    plt.plot(geracoes, historico_presas, label="Presas", color="green", marker="o")
    plt.plot(geracoes, historico_predadores, label="Predadores", color="red", marker="x")
    plt.xlabel("Geração")
    plt.ylabel("População Total")
    plt.title("Evolução das Populações (Presas x Predadores)")
    plt.legend()
    plt.grid()

    # Variação de populações ao longo das gerações
    plt.subplot(2, 1, 2)
    plt.bar(geracoes, historico_presas, color="lightgreen", alpha=0.7, label="Presas")
    plt.bar(geracoes, historico_predadores, color="lightcoral", alpha=0.7, label="Predadores")
    plt.xlabel("Geração")
    plt.ylabel("Tamanho da População")
    plt.title("Distribuição de Populações por Geração")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

def calcular_atributos_medios(populacao):
    if not populacao:
        return [4, 8, 5]
    soma_atributos = np.sum([individuo.genes for individuo in populacao], axis=0)
    return soma_atributos / len(populacao)

if __name__ == "__main__":
    # Parâmetros
    tamanho_presas = 100  
    tamanho_predadores = 34  
    geracoes = 5
    taxa_mutacao = 0.005
    capacidade_reproducao = 0.005

    # Inicializa populações
    presas = inicializar_populacao(tamanho_presas, "presa")
    predadores = inicializar_populacao(tamanho_predadores, "predador")

    historico_presas = []
    historico_predadores = []
    taxas_sobrevivencia = []

    # Executa gerações
    for geracao in range(geracoes):
        print(f"\nGeração {geracao + 1}")
        tamanho_inicial_presas = len(presas)

        presas, predadores = ciclo_evolutivo(presas, predadores, taxa_mutacao)
        presas = interagir(presas, predadores)

        # Calcula atributos médios
        atributos_presas = calcular_atributos_medios(presas)
        atributos_predadores = calcular_atributos_medios(predadores)

        historico_presas.append(len(presas))
        historico_predadores.append(len(predadores))

        taxa_sobrevivencia = (len(presas) / tamanho_presas) * 100
        taxas_sobrevivencia.append(taxa_sobrevivencia)

        if tamanho_inicial_presas > 0:
            taxa_sobrevivencia = (len(presas) / tamanho_inicial_presas) * 100
        else:
            taxa_sobrevivencia = 0.0

        taxas_sobrevivencia.append(taxa_sobrevivencia)

        print(f"População de presas: {len(presas)}")
        print(f"  Atributos médios (Velocidade, Camuflagem, Taxa de Reprodução): {atributos_presas}")
        print(f"População de predadores: {len(predadores)}")
        print(f"  Atributos médios (Velocidade, Eficiência, Capacidade de Reprodução): {atributos_predadores}")
        print(f"Taxa de sobrevivência das presas: {taxa_sobrevivencia:.2f}%")

    plotar_graficos(historico_presas, historico_predadores)