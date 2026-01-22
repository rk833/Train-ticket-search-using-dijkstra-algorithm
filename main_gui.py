"""
Train Ticket Search System (Task 1.3) - GUI Version

Finds optimal train routes using Dijkstra's shortest path algorithm
with a graphical user interface.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import difflib
from src.railway_network import RailwayNetwork
from src.route_searcher import RouteSearcher

class TrainSearchGUI:
    def __init__(self, root, network, searcher):
        self.root = root
        self.network = network
        self.searcher = searcher
        self.all_stations = sorted(list(self.network.stations))
        
        self.root.title("Train Ticket Search System")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Label(
            self.root,
            text="TRAIN TICKET SEARCH SYSTEM",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info label
        info_label = tk.Label(
            main_frame,
            text="Find the best train route between any two stations\nNote: All London stations are combined into 'London'",
            font=("Arial", 9),
            fg="#555"
        )
        info_label.pack(pady=(0, 15))
        
        # Input frame
        input_frame = tk.LabelFrame(main_frame, text="Journey Details", font=("Arial", 10, "bold"), padx=15, pady=15)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Departure station
        tk.Label(input_frame, text="Departure Station:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.departure_var = tk.StringVar()
        self.departure_combo = ttk.Combobox(
            input_frame,
            textvariable=self.departure_var,
            values=self.all_stations,
            width=30,
            font=("Arial", 10)
        )
        self.departure_combo.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Destination station
        tk.Label(input_frame, text="Destination Station:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.destination_var = tk.StringVar()
        self.destination_combo = ttk.Combobox(
            input_frame,
            textvariable=self.destination_var,
            values=self.all_stations,
            width=30,
            font=("Arial", 10)
        )
        self.destination_combo.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Optimization type
        tk.Label(input_frame, text="Optimize for:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.optimize_var = tk.StringVar(value="cost")
        optimize_frame = tk.Frame(input_frame)
        optimize_frame.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        tk.Radiobutton(
            optimize_frame,
            text="Cheapest Route",
            variable=self.optimize_var,
            value="cost",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Radiobutton(
            optimize_frame,
            text="Fastest Route",
            variable=self.optimize_var,
            value="time",
            font=("Arial", 9)
        ).pack(side=tk.LEFT)
        
        # Search button
        search_btn = tk.Button(
            main_frame,
            text="SEARCH ROUTE",
            command=self.search_route,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        search_btn.pack(pady=(0, 15))
        
        # Results frame
        results_frame = tk.LabelFrame(main_frame, text="Route Results", font=("Arial", 10, "bold"), padx=15, pady=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            width=70,
            height=15,
            font=("Courier", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=(10, 0))
        
        save_btn = tk.Button(
            btn_frame,
            text="Save Route",
            command=self.save_route,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_results,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Network info at bottom
        info_text = f"Network loaded: {len(self.network.stations)} stations, {sum(len(neighbors) for neighbors in self.network.graph.values()) // 2} connections"
        info_bottom = tk.Label(
            self.root,
            text=info_text,
            font=("Arial", 8),
            fg="#666",
            pady=8
        )
        info_bottom.pack(side=tk.BOTTOM, fill=tk.X)
    
    def validate_station(self, station_input):
        """Validate and correct station name with fuzzy matching."""
        if not station_input:
            return None
        
        # Exact match
        if self.network.station_exists(station_input):
            return station_input
        
        # Case-insensitive match
        for s in self.all_stations:
            if s.lower() == station_input.lower():
                return s
        
        # Fuzzy matching
        matches = difflib.get_close_matches(
            station_input,
            self.all_stations,
            n=3,
            cutoff=0.6
        )
        
        if matches:
            result = messagebox.askquestion(
                "Station Not Found",
                f"'{station_input}' not found.\n\nDid you mean '{matches[0]}'?",
                icon='question'
            )
            if result == 'yes':
                return matches[0]
        else:
            messagebox.showerror("Error", f"Station '{station_input}' not found in network.")
        
        return None
    
    def search_route(self):
        """Search for route and display results."""
        departure_input = self.departure_var.get().strip()
        destination_input = self.destination_var.get().strip()
        
        # Validate inputs
        departure = self.validate_station(departure_input)
        if not departure:
            return
        
        destination = self.validate_station(destination_input)
        if not destination:
            return
        
        if departure == destination:
            messagebox.showerror("Error", "Departure and destination are the same!")
            return
        
        # Update comboboxes with validated values
        self.departure_var.set(departure)
        self.destination_var.set(destination)
        
        optimize_for = self.optimize_var.get()
        
        # Search for route
        path, total_cost, total_time, connections_explored = self.searcher.find_route(
            departure, destination, optimize_for
        )
        
        if path is None:
            messagebox.showwarning("No Route", "No route found between these stations!")
            self.clear_results()
            return
        
        # Display results
        self.display_route(path, total_cost, total_time, optimize_for, connections_explored)
    
    def display_route(self, path, total_cost, total_time, optimize_for, connections_explored):
        """Display route in results text area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        output = []
        output.append("=" * 70)
        output.append("ROUTE FOUND".center(70))
        output.append("=" * 70)
        output.append("")
        output.append("Cheapest Route" if optimize_for == 'cost' else "Fastest Route")
        output.append("")
        output.append("Route (in order):")
        output.append("-" * 70)
        
        for i, station in enumerate(path, 1):
            if i == 1:
                output.append(f" {i:2d}. {station} (START)")
            elif i == len(path):
                output.append(f" {i:2d}. {station} (DESTINATION)")
            else:
                output.append(f" {i:2d}. {station}")
        
        output.append("")
        output.append("Journey Summary:")
        output.append("-" * 70)
        output.append(f" • Total Stations: {len(path)}")
        output.append(f" • Total Cost: £{total_cost}")
        output.append(f" • Total Time: {total_time} minutes ({total_time // 60}h {total_time % 60}m)")
        output.append(f" • Connections Explored: {connections_explored}")
        output.append("=" * 70)
        
        self.results_text.insert(1.0, "\n".join(output))
        self.results_text.config(state=tk.DISABLED)
        
        # Store current route for saving
        self.current_route = "\n".join(output)
    
    def save_route(self):
        """Save current route to file."""
        if not hasattr(self, 'current_route'):
            messagebox.showwarning("No Route", "No route to save. Please search for a route first.")
            return
        
        filename = "route_details.txt"
        try:
            with open(filename, 'w') as f:
                f.write(self.current_route + "\n\n")
            messagebox.showinfo("Success", f"Route successfully saved to '{filename}'")
        except IOError as e:
            messagebox.showerror("Error", f"Error saving file: {e}")
    
    def clear_results(self):
        """Clear results text area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        if hasattr(self, 'current_route'):
            del self.current_route


def main():
    """Load the railway network, initialize route searcher, and start the GUI."""
    print("Loading railway network...")
    
    # Create network object
    network = RailwayNetwork()
    
    # Build correct CSV path
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "railway_network.csv")
    
    # Load CSV
    network.load_from_csv(csv_path)
    
    # Create route searcher
    searcher = RouteSearcher(network)
    
    # Create and run GUI
    root = tk.Tk()
    app = TrainSearchGUI(root, network, searcher)
    root.mainloop()


if __name__ == "__main__":
    main()