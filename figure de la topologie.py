import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import random

# Création du graphe
G = nx.DiGraph()

# Nombre de nœuds pour le groupe A
nNodes = 5
nodesA = [f'A{i}' for i in range(1, nNodes + 1)]

# Nœuds B et C
nodesBC = ['B', 'C']

# Ajout des nœuds au graphe
G.add_nodes_from(nodesA)
G.add_nodes_from(nodesBC)
G.add_node('Internet')

# Ajout des arêtes pour le réseau CSMA entre les nœuds A
for i in range(nNodes):
    for j in range(i + 1, nNodes):
        G.add_edge(nodesA[i], nodesA[j], bandwidth='100 Mbps', delay='6560 ns')

# Ajout des arêtes pour le réseau CSMA entre les nœuds B et C
G.add_edge('B', 'C', bandwidth='100 Mbps', delay='6560 ns')

# Ajout des arêtes pour la pile Internet (protocole OLSR)
for node in nodesA:
    G.add_edge(node, 'Internet')

G.add_edge('B', 'Internet')

# Assignation des adresses IP aux nœuds A et B/C
ip_addresses = {f'A{i}': f'10.1.1.{i}' for i in range(1, nNodes + 1)}
ip_addresses.update({'B': '10.1.2.1', 'C': '10.1.2.2'})
nx.set_node_attributes(G, ip_addresses, 'ip')

# Position initiale des nœuds A en rectangle
positions = {f'A{i}': (i * 100, 100) for i in range(1, nNodes + 1)}

# Position initiale aléatoire des nœuds B et C dans la zone rectangulaire définie
boundary_x = (-500, 500)
boundary_y = (-500, 500)
positions.update({'B': (random.uniform(*boundary_x), random.uniform(*boundary_y)),
                  'C': (random.uniform(*boundary_x), random.uniform(*boundary_y))})

# Fonction pour mettre à jour les positions des nœuds à chaque itération de l'animation
def update_positions(frame):
    for node in nodesA:
        x, y = positions[node]
        # Déplacement aléatoire dans la zone rectangulaire définie
        new_x = x + random.uniform(-20, 20)  # Déplacement dans les deux directions X et Y
        new_y = y + random.uniform(-20, 20)
        # Limiter les nœuds dans la zone rectangulaire
        new_x = max(boundary_x[0], min(boundary_x[1], new_x))
        new_y = max(boundary_y[0], min(boundary_y[1], new_y))
        positions[node] = (new_x, new_y)
    
    # Mettre à jour les positions des nœuds B et C avec un déplacement aléatoire
    for node in ['B', 'C']:
        x, y = positions[node]
        new_x = x + random.uniform(-20, 20)
        new_y = y + random.uniform(-20, 20)
        new_x = max(boundary_x[0], min(boundary_x[1], new_x))
        new_y = max(boundary_y[0], min(boundary_y[1], new_y))
        positions[node] = (new_x, new_y)
    
    # Retourner une liste d'objets "artists" à redessiner pour cette frame
    nodes.set_offsets([(positions[node][0], positions[node][1]) for node in G.nodes()])
    return nodes,

# Initialisation de la figure et du graphe
fig, ax = plt.subplots(figsize=(12, 8))

# Dessin du graphe initial avec positions initiales
nodes = nx.draw_networkx_nodes(G, positions, nodelist=nodesA, node_color='skyblue', node_size=3000, label='Nodes A')
nodes = nx.draw_networkx_nodes(G, positions, nodelist=['B', 'C'], node_color='lightgreen', node_size=3000, label='Nodes B/C')
nodes = nx.draw_networkx_nodes(G, positions, nodelist=['Internet'], node_color='coral', node_size=3000, label='Internet')

edges = nx.draw_networkx_edges(G, positions, edgelist=G.edges(), width=2, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=20)
labels = nx.draw_networkx_labels(G, positions, labels=nx.get_node_attributes(G, 'ip'), font_color='black', font_size=10, font_weight='bold')

# Titre et légende
plt.title('Topologie réseau avec modèle de mobilité rectangulaire')

plt.xlim(-600, 600)
plt.ylim(-200, 600)  # Ajustement pour montrer les nœuds A en rectangle
plt.legend()

# Désactiver les axes
plt.axis('off')

# Animation avec FuncAnimation
ani = FuncAnimation(fig, update_positions, frames=100, interval=200, blit=True)

# Afficher l'animation
plt.show()

