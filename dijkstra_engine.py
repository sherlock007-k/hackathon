import pandas as pd
import networkx as nx
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import heapq

print("🚀 Launching Extraordinary Routing & Hunting Engine...")

def load_graph(mock_if_large=True):
    print("   Loading dataset – Forging network graph...")
    try:
        df = pd.read_csv("training_dataset.csv")
        print(f"   Dataset loaded: {len(df)} rows – Building graph...")
        if len(df) > 50000 and mock_if_large:  # Too large = slow; fallback mock for fast demo
            print("   Large dataset detected – Switching to fast mock mode for instant launch!")
            df = pd.DataFrame({
                'ip': ['Router-1', 'Camera-A', 'Smart-TV', 'Phone-X', 'Laptop-Y'],
                'ports_count': [2, 5, 3, 1, 4],
                'risk_score': [20, 80, 50, 10, 60],
                'risk_label': ['Low', 'High', 'Medium', 'Low', 'Medium'],
                'vendor': ['TP-Link', 'Hikvision', 'Samsung', 'Apple', 'Unknown'],
                'attack_cat': ['Normal', 'Exploits', 'DoS', 'Normal', 'Recon']
            })
    except FileNotFoundError:
        print("   training_dataset.csv not found – Creating innovative mock graph for demo!")
        df = pd.DataFrame({
            'ip': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5'],
            'ports_count': [1, 4, 2, 5, 3],
            'risk_score': [10, 70, 30, 90, 50],
            'risk_label': ['Low', 'High', 'Low', 'High', 'Medium'],
            'vendor': ['Router', 'Hikvision', 'TP-Link', 'Dahua', 'ESP32'],
            'attack_cat': ['Normal', 'Exploits', 'Normal', 'DoS', 'Recon']
        })

    G = nx.Graph()
    a, b, c = 0.5, 0.3, 0.2

    for i, row in df.iterrows():
        risk = {"Low": 0.2, "Medium": 0.6, "High": 1.0}.get(row['risk_label'], 0.5)
        vuln = 0.8 if any(k.lower() in str(row.get('vendor', '')).lower() for k in ["unknown", "hikvision", "dahua", "esp"]) else 0.3
        base_weight = a * row['ports_count'] + b * risk + c * vuln

        time_factor = 1.5 if 0 <= datetime.now().hour < 6 or 18 <= datetime.now().hour < 24 else 1.0
        congestion = row['ports_count'] * 0.1
        attack_density = (df['risk_label'] == 'High').mean()

        kill_stage = {'Normal': 'None', 'Exploits': 'Exploit', 'DoS': 'Exploit', 'Recon': 'Recon'}.get(row.get('attack_cat', 'Normal'), 'None')
        stage_factor = 2.0 if kill_stage in ['Exploit', 'Lateral Movement'] else 1.0

        impact = (1.5 if row['ports_count'] > 3 else 1.0) * (2.0 if row['risk_label'] == 'High' else 1.0)
        final_weight = base_weight * time_factor * (1 + congestion) * (1 + attack_density) * stage_factor * impact

        G.add_node(row["ip"], risk=row['risk_score'], label=row['risk_label'], kill_chain=kill_stage, impact=impact)
        if i > 0:
            prev = df.iloc[i-1]["ip"]
            G.add_edge(prev, row["ip"], weight=final_weight, trans_prob=0.2)

    for u, v in G.edges:
        G.edges[u, v]['trans_prob'] = G.edges[u, v].get('trans_prob', 0.2)

    print(f"   Graph forged: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges – Ready for hunt!")
    return G, df

def find_safest_path(start, end):
    print(f"   Hunting safest path from {start} to {end} with A*...")
    G, _ = load_graph()
    if start not in G or end not in G:
        print("   Start/end not in graph – Check IPs.")
        return None, None

    def heuristic(u):
        return G.nodes[u]['risk'] + G.nodes[u]['impact']

    open_set = []
    heapq.heappush(open_set, (heuristic(start), 0, start))
    came_from = {}
    g_score = {node: float('inf') for node in G.nodes}
    g_score[start] = 0

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            print(f"   🛡️ Safest Path Found: {' -> '.join(path)} (Cost: {current_g:.2f})")
            return path, current_g

        for neighbor in G.neighbors(current):
            tentative_g = current_g + G.edges[current, neighbor].get('weight', 1)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    print("   No path found – Network isolated.")
    return None, None

def attack_spread_probability(start_node, target_node, steps=5):
    print(f"   Calculating MDP spread probability over {steps} steps...")
    G, _ = load_graph()
    if start_node not in G or target_node not in G:
        return 0.0

    adj = nx.to_numpy_array(G, weight='trans_prob')
    adj /= (adj.sum(axis=1, keepdims=True) + 1e-6)

    nodes = list(G.nodes())
    prob = np.zeros(len(nodes))
    prob[nodes.index(start_node)] = 1.0

    for _ in range(steps):
        prob = np.dot(prob, adj)

    spread_prob = prob[nodes.index(target_node)] * 100
    print(f"   ⚠️ Breach Probability: {spread_prob:.2f}%")
    return spread_prob

def suggest_quarantine():
    print("   Analyzing for quarantine recommendation...")
    G, df = load_graph()
    pagerank = nx.pagerank(G, weight='weight')
    high_risk = [n for n in G.nodes if G.nodes[n]['label'] == "High"]
    if high_risk:
        central = max(high_risk, key=lambda n: pagerank.get(n, 0) * G.nodes[n]['impact'])
        print(f"   🔒 Quarantine {central} (High centrality + impact)")
        return central
    print("   No immediate quarantine needed.")
    return None

if __name__ == "__main__":
    G, df = load_graph()
    if len(df) < 2:
        print("   Small dataset – Demo complete!")
    else:
        start = df['ip'].iloc[0]
        end = df['ip'].iloc[-1]
        find_safest_path(start, end)
        attack_spread_probability(start, end)
        suggest_quarantine()

    # Extraordinary Viz
    print("\n   🎨 Generating routing visualization PNG...")
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42)
    node_colors = [G.nodes[n]['risk'] for n in G.nodes]
    nx.draw(G, pos, node_color=node_colors, cmap='RdYlGn_r', node_size=1000, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v): f"{d['weight']:.1f}" for u,v,d in G.edges(data=True)})
    plt.title("E-Raksha Network – Safe Path Hunt Visualization")
    plt.savefig("routing_example.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   routing_example.png generated – Open for stunning view!")
    print("\n🏆 Engine Launch Complete – Ready for Cyber Fortress!")