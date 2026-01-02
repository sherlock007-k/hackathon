import pandas as pd
import networkx as nx
from pyvis.network import Network
import random, time, webbrowser

def simulate_attack(source=None, steps=8, csv="training_data.csv"):
    df = pd.read_csv(csv)

    G = nx.Graph()
    for i, row in df.iterrows():
        G.add_node(row["ip"], risk=row["risk_score"])

    devices = df["ip"].tolist()

    # auto-create network
    for i in range(len(devices)-1):
        G.add_edge(devices[i], devices[i+1])

    if source is None:
        source = random.choice(devices)

    infected = [source]
    print(f"\n🚨 Attack Started at {source}")

    for step in range(steps):

        net = Network(height="800px", width="100%", bgcolor="#0d1326", font_color="white")

        for node in G.nodes:
            risk = G.nodes[node]["risk"]
            color = "red" if node in infected else ("orange" if risk > 40 else "lightgreen")

            net.add_node(node,color=color,size=25,title=f"IP:{node}<br>Risk:{risk}")

        # spread to neighbors
        if len(infected) > 0:
            current = infected[-1]
            neighbors = list(G.neighbors(current))
            if neighbors:
                nxt = random.choice(neighbors)
                if nxt not in infected:
                    infected.append(nxt)

        # draw edges
        for u,v in G.edges:
            net.add_edge(u,v,color="#78aaff")

        file = f"attack_step_{step+1}.html"
        net.write_html(file)
        webbrowser.open(file)
        print(f"🟥 Attack moved → {infected[-1]}")

        time.sleep(1)

    print("\nAttack Path:", " → ".join(infected))
    print("📌 Simulation Complete")

if __name__ == "__main__":
    simulate_attack()
