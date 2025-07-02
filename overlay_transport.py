import argparse
import osmnx as ox
from shapely.affinity import translate
import matplotlib.pyplot as plt

def overlay_transport(city_a, city_b, network_type='drive', output=None):
    """Download transport networks for two cities and overlay them."""
    ox.settings.use_cache=True
    ox.settings.log_console=False
    G_a = ox.graph_from_place(city_a, network_type=network_type)
    G_b = ox.graph_from_place(city_b, network_type=network_type)
    edges_a = ox.graph_to_gdfs(G_a, nodes=False, edges=True)
    edges_b = ox.graph_to_gdfs(G_b, nodes=False, edges=True)
    a_centroid = edges_a.unary_union.centroid
    b_centroid = edges_b.unary_union.centroid
    dx = b_centroid.x - a_centroid.x
    dy = b_centroid.y - a_centroid.y
    edges_a['geometry'] = edges_a['geometry'].apply(lambda g: translate(g, xoff=dx, yoff=dy))
    fig, ax = plt.subplots(figsize=(10,10))
    edges_b.plot(ax=ax, color='black', linewidth=0.5, label=city_b)
    edges_a.plot(ax=ax, color='red', linewidth=0.5, label=city_a)
    ax.set_axis_off()
    ax.legend()
    if output:
        plt.savefig(output, bbox_inches='tight')
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Overlay transport networks of two cities")
    parser.add_argument('-a', '--city-a', required=True, help='Transport network to overlay')
    parser.add_argument('-b', '--city-b', required=True, help='Base city to overlay onto')
    parser.add_argument('-t', '--type', default='drive', help='Network type (default: drive)')
    parser.add_argument('-o', '--output', help='Output image file path')
    args = parser.parse_args()
    overlay_transport(args.city_a, args.city_b, network_type=args.type, output=args.output)

if __name__ == '__main__':
    main()
