## Maria Eduarda Rodrigues da Silva

# Simulador de Redes de Filas
Este simulador implementa uma simulação de eventos discretos para redes de filas genéricas, utilizando Python. Ele é capaz de modelar filas com múltiplos servidores, capacidades finitas e roteamento probabilístico entre filas.

## Funcionalidades
- Suporte a redes de filas com topologia genérica
- Filas com número variável de servidores
- Capacidades finitas para filas
- Tempos de serviço e chegada com distribuições uniformes
- Roteamento probabilístico entre filas
- Coleta de estatísticas: distribuições de estados, tempos acumulados, perdas de clientes

## Sintaxe de Entrada
O simulador lê um arquivo de configuração texto com o seguinte formato:

```
<num_queues>
<servers_q0> <capacity_q0> <service_min_q0> <service_max_q0>
<servers_q1> <capacity_q1> <service_min_q1> <service_max_q1>
...
arrivals <queue_id> <arrival_min> <arrival_max>
routing <from_queue> <to_queue> <probability>
...
num_simulations <number>
seed <seed_value>
first_arrival <time>
```

### Exemplo para duas filas em tandem:
```
2
2 3 3.0 4.0
1 5 2.0 3.0
arrivals 0 1.0 4.0
routing 0 1 1.0
num_simulations 100000
seed 100000
first_arrival 1.5
```

- `2`: Número de filas
- Primeira fila: 2 servidores, capacidade 3, serviço entre 3.0 e 4.0
- Segunda fila: 1 servidor, capacidade 5, serviço entre 2.0 e 3.0
- Chegadas externas na fila 0 entre 1.0 e 4.0
- Roteamento da fila 0 para fila 1 com probabilidade 1.0
- 100000 simulações (chegadas)
- Semente aleatória 100000
- Primeira chegada em 1.5

## Como Usar
1. Crie um arquivo de configuração (ex: `config.txt`) seguindo a sintaxe acima.
2. Execute o simulador: `python simulador_filas.py config.txt`
3. O simulador irá imprimir os resultados: tempo global, perdas por fila, e para cada fila, as probabilidades e tempos acumulados por estado.

## Extensibilidade
Para adicionar mais filas ou alterar a topologia:
- Aumente `num_queues`
- Adicione linhas para cada fila adicional
- Defina chegadas externas com `arrivals`
- Defina roteamentos com `routing` (múltiplas linhas por fila de origem, probabilidades devem somar 1.0)

## Dependências
- Python 3.x
- Módulos padrão: `heapq`, `random`, `collections`, `sys`

## Resultados da Validação
Para a configuração de exemplo:

Tempo Global da Simulação: 249883.181584
Perdas na Fila 1: 249
Perdas na Fila 2: 1552

Fila 1 (G/G/2/3):
  Estado 0: Probabilidade 0.019592, Tempo Acumulado 4895.586426
  Estado 1: Probabilidade 0.563621, Tempo Acumulado 140839.358617
  Estado 2: Probabilidade 0.383610, Tempo Acumulado 95857.581903
  Estado 3: Probabilidade 0.033178, Tempo Acumulado 8290.654638

Fila 2 (G/G/1/5):
  Estado 0: Probabilidade 0.017598, Tempo Acumulado 4397.406994
  Estado 1: Probabilidade 0.177243, Tempo Acumulado 44290.085586
  Estado 2: Probabilidade 0.263713, Tempo Acumulado 65897.562090
  Estado 3: Probabilidade 0.253765, Tempo Acumulado 63411.629592
  Estado 4: Probabilidade 0.219987, Tempo Acumulado 54971.172765
  Estado 5: Probabilidade 0.067693, Tempo Acumulado 16915.324556