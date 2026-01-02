# ========================= ADVANCED NETWORK VISUALIZER ==========================
import pandas as pd
import networkx as nx
from pyvis.network import Network
import webbrowser

def visualize_advanced_network(csv_file="training_data.csv"):

    df = pd.read_csv(csv_file)

    G = nx.Graph()

    # ------------------- Add Nodes --------------------
    for _, row in df.iterrows():
        
        if row["risk_score"] >= 70: color = "red"
        elif row["risk_score"] >= 40: color = "orange"
        else: color = "lightgreen"

        G.add_node(
            row["ip"],
            title=f"<b>{row['ip']}</b><br>Vendor:{row['vendor']}<br>Risk:{row['risk_score']}",
            color=color,
            value=row["ports_count"]+1
        )

    # ------------------- Auto connect nodes --------------------
    devices = df["ip"].tolist()
    for i in range(len(devices)-1):
        G.add_edge(devices[i], devices[i+1], color="#88c3ff")

    # ============= Centrality & Attack Influence ============
    central = nx.betweenness_centrality(G)
    pagerank = nx.pagerank(G)

    critical = max(central, key=central.get)
    important = max(pagerank, key=pagerank.get)

    print(f"\n🔥 Critical Network Node → {critical}")
    print(f"👑 High Influence Device → {important}")

    # ------------------- Visualization ------------------------
    net = Network(
        height="800px",
        width="100%",
        bgcolor="#0a0f1f",
        font_color="white",
        heading="Cyber Network Graph"
    )

    net.from_nx(G)
    file = "attack_network_map.html"
    net.write_html(file)     # ← FIXES TEMPLATE ERROR

    print(f"\n📌 Graph Exported → {file}")
    print("👉 Open the file manually or use command below\n")

    webbrowser.open(file)  # Auto opens graph

if __name__ == "__main__":
    visualize_advanced_network()
