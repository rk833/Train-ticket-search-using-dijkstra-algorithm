# src/route_searcher.py

import heapq

class RouteSearcher:
    """
    Finds routes in a railway network using Dijkstra's algorithm.
    """
    def __init__(self, network):
        """
        Initialize with a RailwayNetwork instance.
        """
        self.network = network
    
    def find_route(self, start, end, optimize_for='cost'):
        """
        Find best route from start to end.

        Returns path, total cost, total time, and edges explored.
        """
        # Prevent search if graph is empty
        if not self.network.graph:
            print("Railway network is empty!")
            return None, None, None
        
        # Run Dijkstra's algorithm
        distances, parents, connections_explored = self._dijkstra(start, end, optimize_for)
        
        # Check if destination is reachable
        if end not in parents:
            return None, None, None, connections_explored
        
        # Reconstruct path
        path = self._reconstruct_path(parents, start, end)
        
        # Calculate total cost and time for the path
        total_cost, total_time = self._calculate_route_details(path)
        
        return path, total_cost, total_time, connections_explored
    
    def _dijkstra(self, start, end, optimize_for):
        """
        Internal Dijkstra algorithm to compute shortest paths.
        """

        # counts explored edges
        connections_explored = 0 

        # Stop if invalid optimization choice
        if optimize_for not in ['cost', 'time']:
            return {}, {}
        
        # Initialize data structures
        distances = {station: float('infinity') for station in self.network.stations}
        distances[start] = 0
        
        parents = {start: None}
        visited = set()
        
        # Min-heap to always pick smallest distance
        priority_queue = [(0, start)]
        
        while priority_queue:
            # Get station with minimum distance
            current_distance, current_station = heapq.heappop(priority_queue)
            
            # Skip if already visited (handles duplicate entries in queue)
            if current_station in visited:
                continue
            
            # Mark as visited
            visited.add(current_station)
            
            # Early termination: found destination
            if current_station == end:
                break
            
            # Explore neighbors
            for neighbor, cost, time in self.network.get_neighbors(current_station):
                connections_explored += 1

                if neighbor not in visited:
                    # Choose weight based on optimization criterion
                    weight = cost if optimize_for == 'cost' else time
                    
                    # Calculate new distance
                    new_distance = current_distance + weight
                    
                    # Relaxation step: update if found a shorter path
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parents[neighbor] = current_station
                        heapq.heappush(priority_queue, (new_distance, neighbor))
        
        return distances, parents, connections_explored
    
    def _reconstruct_path(self, parents, start, end):
        """
        Reconstruct path from start to end using parent pointers.
        """

        # Builds route from end to start
        path = []
        current = end
        
        # Backtrack from end to start
        while current is not None:
            path.append(current)
            current = parents.get(current)
        
        # Reverse to get start → end order
        path.reverse()
        
        return path
    
    def _calculate_route_details(self, path):
        """
        Calculate total cost and travel time for a given path.
        """
        total_cost = 0
        total_time = 0
        
        # Iterate through consecutive station pairs
        for i in range(len(path) - 1):
            current = path[i]
            next_station = path[i + 1]
            
            # Find the edge between current and next station
            for neighbor, cost, time in self.network.get_neighbors(current):
                if neighbor == next_station:
                    total_cost += cost
                    total_time += time
                    break
        
        return total_cost, total_time
