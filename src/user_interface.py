# src/user_interface.py
import difflib


class UserInterface:
    """
    Handles user input, route selection, and output display.
    """

    def __init__(self, network, searcher):
        """Initialize with a railway network and route searcher."""
        self.network = network
        self.searcher = searcher
        # Pre-process station list for quick case-insensitive lookups
        self.all_stations = list(self.network.stations)

    def get_station_input(self, prompt):
        """Prompt user for a station name with fuzzy matching."""
        while True:
            station_input = input(prompt).strip()

            if not station_input:
                print(" Station name cannot be empty!")
                continue

            # Exact match
            if self.network.station_exists(station_input):
                return station_input

            # Case-insensitive match
            for s in self.all_stations:
                if s.lower() == station_input.lower():
                    print(f" Assuming you meant: '{s}'")
                    return s

            # Fuzzy matching suggestions
            matches = difflib.get_close_matches(
                station_input,
                self.all_stations,
                n=3,
                cutoff=0.6
            )

            print(f" Station '{station_input}' not found in network.")

            if matches:
                while True:
                    print("\n Did you mean one of these stations?")
                    for i, match in enumerate(matches, 1):
                        print(f" {i}. {match}")
                    print(" X. Enter a new name")

                    choice = input(" Enter choice (1, 2, 3 or X): ").strip().upper()

                    if choice == 'X':
                        break

                    try:
                        index = int(choice) - 1
                        if 0 <= index < len(matches):
                            return matches[index]
                        else:
                            print(" Invalid choice. Try again.")
                    except ValueError:
                        print(" Invalid input. Enter 1, 2, 3 or X.")
            else:
                print(" No close matches found. Please try again.")

    def get_search_type(self):
        """Ask user whether to optimise for cost or time."""
        while True:
            print("\nOptimize for:")
            print("  1. Cheapest route (minimum cost)")
            print("  2. Fastest route (minimum time)")
            choice = input("Enter choice (1 or 2): ").strip()

            if choice == '1':
                return 'cost'
            elif choice == '2':
                return 'time'
            else:
                print(" Invalid choice! Please enter 1 or 2.")

    def save_route_to_file(self, content):
        """Save route details to a file."""
        filename = "route_details.txt"
        try:
            with open(filename, 'w') as f:
                f.write(content + "\n\n")
            print(f"\n Route successfully saved to '{filename}'")
        except IOError as e:
            print(f" Error saving file: {e}")

    def display_route(self, path, total_cost, total_time, optimize_for, connections_explored):
        """Display route and journey summary."""
        output = []

        output.append("ROUTE FOUND\n".center(70))

        output.append(" Cheapest Route" if optimize_for == 'cost' else " Fastest Route")

        output.append("\nRoute (in order):")
        for i, station in enumerate(path, 1):
            if i == 1:
                output.append(f" {i}. {station} (START)")
            elif i == len(path):
                output.append(f" {i}. {station} (DESTINATION)")
            else:
                output.append(f" {i}. {station}")


        output.append("\nJourney Summary:")
        output.append(f" • Total Stations: {len(path)}")
        output.append(f" • Total Cost: £{total_cost}")
        output.append(f" • Total Time: {total_time} minutes ({total_time // 60}h {total_time % 60}m)")
        output.append(f" • Connections Explored: {connections_explored}")

        route_text = "\n".join(output)
        print(route_text)

        self.save_route_to_file(route_text)

    def run(self):
        """Main program loop for interacting with the user."""
        print("TRAIN TICKET SEARCH SYSTEM".center(70))
        print("\nWelcome! Find the best train route between any two stations.")
        print("Note: All London stations are combined into 'London'\n")

        while True:
            departure = self.get_station_input("\nEnter departure station: ")
            destination = self.get_station_input("Enter destination station: ")

            if departure == destination:
                print("\n Departure and destination are the same!")
                continue

            search_type = self.get_search_type()

            print(f"\n Searching for {'cheapest' if search_type == 'cost' else 'fastest'} route...")

            path, total_cost, total_time, connections_explored = self.searcher.find_route(
                departure, destination, search_type
            )

            if path is None:
                print("\n No route found between these stations!")
            else:
                self.display_route(
                    path,
                    total_cost,
                    total_time,
                    search_type,
                    connections_explored
                )

            again = input("\nSearch another route? (Y/N): ").strip().upper()
            if again != 'Y':
                break
