import networkx as nx
import plotly.graph_objs as go
import pandas as pd

def visualize_rules_graph(rules: pd.DataFrame, n: int = 30, max_node_size: int = 50) -> go.Figure:
    # Limit the number of rules to the top 'n'
    rules = rules.head(n)

    # Create an undirected graph
    G = nx.Graph()

    # Calculate the frequency of each item being bought
    item_supports = pd.concat([rules['antecedents'].explode(), rules['consequents'].explode()]).value_counts()
    most_bought_item = item_supports.idxmax()
    least_bought_item = item_supports.idxmin()

    # Add nodes and edges with custom attributes like size and color
    for _, row in rules.iterrows():
        antecedent = next(iter(row['antecedents']))
        consequent = next(iter(row['consequents']))
        support = row['support']
        confidence = row['confidence']

        # Calculate node size based on item frequency, capped at max_node_size
        antecedent_size = min(max(item_supports[antecedent] * 10, 20), max_node_size)
        consequent_size = min(max(item_supports[consequent] * 10, 20), max_node_size)

        # Add nodes with sizes
        G.add_node(antecedent, size=antecedent_size, color='green')
        G.add_node(consequent, size=consequent_size, color='blue')

        # Add edges with custom attributes
        G.add_edge(antecedent, consequent, weight=confidence * 10, color=f'rgba(255, {int(255 * confidence)}, 0, 0.8)')

    # Highlight the most and least bought items
    G.nodes[most_bought_item]['color'] = 'purple'
    G.nodes[least_bought_item]['color'] = 'pink'

    # Position the nodes using a force-directed layout
    pos = nx.spring_layout(G, k=0.5, seed=42)

    # Define the maximum text size and scale factor
    max_text_size = 12
    scale_factor = max_text_size / max_node_size

    # Create edge traces
    edge_trace = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=edge[2]['weight'], color=edge[2]['color']),
            hoverinfo='none',
            mode='lines'
        ))

    # Create node traces with size and text size based on frequency
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            size=[G.nodes[node]['size'] for node in G.nodes()],
            color=[G.nodes[node]['color'] for node in G.nodes()],
            line=dict(width=2)
        ),
        text=[node for node in G.nodes()],
        textposition='top center',
        textfont=dict(
            size=[min(G.nodes[node]['size'] * scale_factor, max_text_size) for node in G.nodes()],
            family="Arial",
        )
    )

    # Combine traces into a figure
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        title='Force Directed Hierarchy',
                        showlegend=False,
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    return fig