import heapq
import random
from collections import deque, defaultdict
import sys

def load_config(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    num_queues = int(lines[i].strip())
    i += 1
    
    queues = []
    for _ in range(num_queues):
        parts = lines[i].strip().split()
        servers = int(parts[0])
        capacity = int(parts[1])
        service_min = float(parts[2])
        service_max = float(parts[3])
        queues.append({
            'servers': servers,
            'capacity': capacity,
            'service_min': service_min,
            'service_max': service_max
        })
        i += 1
    
    arrivals = {}
    routing = defaultdict(list)
    num_simulations = 100000
    seed = 100000
    first_arrival_time = 1.5
    
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('arrivals'):
            parts = line.split()
            qid = int(parts[1])
            min_t = float(parts[2])
            max_t = float(parts[3])
            arrivals[qid] = (min_t, max_t)
        elif line.startswith('routing'):
            parts = line.split()
            from_q = int(parts[1])
            to_q = int(parts[2])
            prob = float(parts[3])
            routing[from_q].append((to_q, prob))
        elif line.startswith('num_simulations'):
            num_simulations = int(line.split()[1])
        elif line.startswith('seed'):
            seed = int(line.split()[1])
        elif line.startswith('first_arrival'):
            first_arrival_time = float(line.split()[1])
        i += 1
    
    return num_queues, queues, arrivals, routing, num_simulations, seed, first_arrival_time

def simulate(num_queues, queues, arrivals, routing, num_simulations, seed, first_arrival_time):
    random.seed(seed)
    
    event_queue = []
    if 0 in arrivals:
        heapq.heappush(event_queue, (first_arrival_time, 'arrival', 0, None))
    
    states = [0] * num_queues
    busies = [0] * num_queues
    queues_list = [deque() for _ in range(num_queues)]
    state_times = [defaultdict(float) for _ in range(num_queues)]
    losses = [0] * num_queues
    last_time = 0
    num_arrivals = {qid: 0 for qid in arrivals}
    
    while event_queue:
        time, typ, qid, _ = heapq.heappop(event_queue)
        time_diff = time - last_time
        for q in range(num_queues):
            state_times[q][states[q]] += time_diff
        last_time = time
        
        if typ == 'arrival':
            num_arrivals[qid] += 1
            if states[qid] < queues[qid]['capacity']:
                states[qid] += 1
                if busies[qid] < queues[qid]['servers']:
                    busies[qid] += 1
                    serv = random.uniform(queues[qid]['service_min'], queues[qid]['service_max'])
                    heapq.heappush(event_queue, (time + serv, 'departure', qid, None))
                else:
                    queues_list[qid].append(1)
            else:
                losses[qid] += 1
            if num_arrivals[qid] < num_simulations:
                inter = random.uniform(arrivals[qid][0], arrivals[qid][1])
                heapq.heappush(event_queue, (time + inter, 'arrival', qid, None))
        
        elif typ == 'departure':
            busies[qid] -= 1
            states[qid] -= 1
            if queues_list[qid]:
                queues_list[qid].popleft()
                busies[qid] += 1
                serv = random.uniform(queues[qid]['service_min'], queues[qid]['service_max'])
                heapq.heappush(event_queue, (time + serv, 'departure', qid, None))
            if qid in routing:
                r = random.random()
                cum_prob = 0
                for next_q, prob in routing[qid]:
                    cum_prob += prob
                    if r <= cum_prob:
                        if states[next_q] < queues[next_q]['capacity']:
                            states[next_q] += 1
                            if busies[next_q] < queues[next_q]['servers']:
                                busies[next_q] += 1
                                serv = random.uniform(queues[next_q]['service_min'], queues[next_q]['service_max'])
                                heapq.heappush(event_queue, (time + serv, 'departure', next_q, None))
                            else:
                                queues_list[next_q].append(1)
                        else:
                            losses[next_q] += 1
                        break
    
    total_time = last_time
    return total_time, losses, state_times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python simulador_filas.py <arquivo_config>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    num_queues, queues, arrivals, routing, num_simulations, seed, first_arrival_time = load_config(config_file)
    
    total_time, losses, state_times = simulate(num_queues, queues, arrivals, routing, num_simulations, seed, first_arrival_time)
    
    print("Resultados da Simulação para Rede de Filas")
    print("=" * 50)
    print(f"Tempo Global da Simulação: {total_time:.6f}")
    for q in range(num_queues):
        print(f"Perdas na Fila {q+1}: {losses[q]}")
    print()
    
    for q in range(num_queues):
        cap = queues[q]['capacity']
        print(f"Fila {q+1} (G/G/{queues[q]['servers']}/{cap}):")
        for k in range(cap + 1):
            prob = state_times[q][k] / total_time if total_time > 0 else 0
            print(f"  Estado {k}: Probabilidade {prob:.6f}, Tempo Acumulado {state_times[q][k]:.6f}")
        print()