from parsing import ParseMap
from pydantic import ValidationError
from models import Map, Zone, Connection
from graph import Graph

def main() -> None:
    ob = ParseMap("file_test.txt")

    ob.read_lines()

    keys = [D['key'] for D in ob.map['zones']]

    if 'start_hub' not in keys or 'end_hub' not in keys:
        raise ValueError("start_hub and end_hub is requred hubs \
write it in the map file")

    ob = Map(**ob.map)
    print(f"{ob.zones}\n\n\n\n")
    graph = Graph(ob.zones, ob.connections)
    graph.build_graph()
    print(graph.graph)
    


if __name__ == '__main__':

    try:

        main()

    except ValidationError as e:
        err = None
        if Map.error_nb:
            err = Map.error_nb
        elif Zone.error_zone:
            err = Zone.error_zone
        elif Connection.error_conn:
            err = Connection.error_conn
        print(f"[Error]: {e.errors()[0]['loc'][-1]} {e.errors()[0]['msg']}")
        print(f"number of line:{err['line_number']}")
        print(f"line -> {err['line']}")

    except ValueError as e:
        print(f"[Error]: {e}")
