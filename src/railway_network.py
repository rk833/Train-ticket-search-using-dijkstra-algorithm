# src/railway_network.py

import csv
import os

class RailwayNetwork:
    """
    Represents a railway network as a graph with stations and connections.
    """
    def __init__(self):
        """
        Initialize an empty railway network.
        """

        # Graph structure: {station: [(neighbor, cost, time), ...]}
        self.graph = {}

        # Stores all station names
        self.stations = set()
    
    def load_from_csv(self, filename):
        """
        Load railway stations and connections from a CSV file.

        Each row in CSV should be: station1, station2, cost, time
        """
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                
                for row in csv_reader:

                    # Skip invalid or broken rows
                    if len(row) != 4:
                        continue

                    # Skip if row looks like header
                    if row[0].lower() == 'station1' or not row[2].isdigit():
                        continue
                    
                    # Parse each line
                    station1 = row[0].strip()
                    station2 = row[1].strip()
                    cost = int(row[2].strip())
                    time = int(row[3].strip())
                    
                    # Store station names
                    self.stations.add(station1)
                    self.stations.add(station2)
                    
                    # Create empty list if station not seen before
                    if station1 not in self.graph:
                        self.graph[station1] = []
                    if station2 not in self.graph:
                        self.graph[station2] = []
                    
                    # Add bidirectional edges
                    # Each edge stores: (neighbor_station, cost, time)
                    self.graph[station1].append((station2, cost, time))
                    self.graph[station2].append((station1, cost, time))
            
            print(f" Network loaded: {len(self.stations)} stations, "
                  f"{sum(len(neighbors) for neighbors in self.graph.values()) // 2} connections")
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found!")
            exit(1)
        except Exception as e:
            print(f"Error loading network: {e}")
            exit(1)
    
    def get_neighbors(self, station):
        """
        Return a list of neighboring stations with cost and time.
        """
        return self.graph.get(station, [])
    
    def station_exists(self, station):
        """
        Check if a station exists in the network.
        """
        return station in self.stations
