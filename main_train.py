"""
Train Ticket Search System (Task 1.3)

Finds optimal train routes using Dijkstra's shortest path algorithm
and provides a console-based and Tkinter user interface.
"""
import os
from src.railway_network import RailwayNetwork
from src.route_searcher import RouteSearcher
from src.user_interface import UserInterface

def main():
    """Load the railway network, initialize route searcher, and start the UI."""
    print("Loading railway network...")

    # Create network object FIRST
    network = RailwayNetwork()

    # Build correct CSV path
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "railway_network.csv")

    # Load CSV
    network.load_from_csv(csv_path)

    # Create route searcher
    searcher = RouteSearcher(network)

    # Run user interface
    ui = UserInterface(network, searcher)
    ui.run()

if __name__ == "__main__":
    main()