from dict_format import ParsedMap, ZoneDict, ConnectionDict
from typing import cast, Any, List, Tuple


class ParseMap:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.map: ParsedMap = {
            "zones": [],
            "connections": [],
            "nb_drones": "",
            'key': '',
            'line': '',
            "line_number": 0
            }

    def read_lines(self) -> None:
        first_line: bool = False

        start_times: int = 0

        nb_times: int = 0

        end_times: int = 0

        with open(self.filename, 'r') as f:

            for line_number, line_raw in enumerate(f, 1):

                line: str = line_raw.strip()

                star: int = line.find(':')
                if star != -1:
                    i: int = star
                    while star > 0 and line[star - 1] == " ":
                        star -= 1
                    line = line[:star] + ":" + line[i + 1:]

                if not line or line.startswith("#"):
                    continue

                elif (line.startswith("nb_drones:")):

                    if first_line or nb_times:
                        raise ValueError(
                            "Error: 'nb_drones' must be the very first line "
                            "of the file."
                            )
                    if nb_times:
                        raise ValueError(
                            "Error: 'nb_drones' cannot be declared"
                            "more than once."
                            )

                    nb_times += 1

                    _: str
                    v: str
                    _, v = line.split(':', 1)
                    v = v.strip()

                    if not v:
                        raise ValueError(
                            "Parse Error: Missing value for 'nb_drones' at "
                            f"line {line_number}.\n[{line_number}] {line}\n"
                            f"Reason: You must provide a valid integer after "
                            "'nb_drones:' (e.g., 'nb_drones: 5')."
                            )

                    self.map['nb_drones'] = v
                    self.map['line'] = line
                    self.map['line_number'] = line_number

                elif (
                    line.startswith("start_hub:")
                    or line.startswith("hub:")
                    or line.startswith("end_hub:")
                      ):

                    first_line = True

                    if line.startswith("start_hub:"):

                        if start_times:
                            raise ValueError(
                                "Error: 'start_hub' must be defined exactly "
                                "once. Multiple declarations are not allowed."
                                )

                        else:
                            start_times += 1

                    elif line.startswith("end_hub"):

                        if end_times:
                            raise ValueError(
                                "Error: 'end_hub' must be defined exactly "
                                "once. Multiple declarations are not allowed."
                                )

                        else:
                            end_times += 1

                    self.parse_zone(line, line_number)

                elif (line.startswith("connection:")):

                    first_line = True

                    self.parse_connection(line, line_number)

                else:
                    raise ValueError(
                        f"Syntax Error: Unrecognized format at line "
                        f"{line_number}\n[{line_number}] {line}"
                        )

    def parse_zone(self, line: str, line_number: int) -> None:

        res: dict[str, Any] = {}

        key: str
        val: str
        key, val = line.split(':', 1)

        data: List[str] = val.split(maxsplit=3)

        if (len(data) < 3):
            raise ValueError(
                f"Parse Error: Missing required attributes at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                f"Expected format: {key}: <name> <x> <y> [metadata]"
                )

        if ('-' in data[0]):
            raise ValueError(
                f"Parse Error: Invalid zone name at line {line_number}.\n"
                f"[{line_number}] {line}\n"
                f"Reason: Zone names cannot contain dashes ('-')."
                )

        last_zones: List[str] = [str(z['name']) for z in self.map['zones']]

        if data[0] in last_zones:
            raise ValueError(
                f"Parse Error: Duplicate zone name detected at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                f"Reason: The zone name '{data[0]}' "
                "has already been declared. Zone names must be unique."
                )

        res['key'] = key.strip()

        res['name'] = data[0]

        res['x'] = data[1]

        res['y'] = data[2]
        res['line'] = line
        res['line_number'] = line_number

        if len(data) == 4:

            metadata: str = data[-1].strip()

            if metadata[0] != '[' or metadata[-1] != ']' or len(metadata) < 6:
                raise ValueError(
                    f"Syntax Error: Invalid metadata format at line "
                    f"{line_number}.\n[{line_number}] {line}\n"
                    f"Reason: Metadata must be enclosed "
                    "in brackets (e.g., [color=red zone=normal])."
                    )

            res_data: dict[str, str] = (self.parse_zone_metadata(
                data[-1][1:-1], line_number, line))

            res.update(res_data)
        re: ZoneDict = cast(ZoneDict, res)
        self.map['zones'].append(re)

    def parse_zone_metadata(self, metadata: str, line_number: int,
                            line: str) -> dict[str, str]:

        res: dict[str, str] = {}

        data: List[str] = metadata.strip().split()

        if (len(data) > 3 or len(data) == 0):
            raise ValueError(
                f"Parse Error: Invalid number of metadata attributes at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                "Reason: Metadata must contain between "
                "1 and 3 valid attributes (zone, color, max_drones)."
                )

        for d in data:

            if '=' not in d:
                raise ValueError(
                    f"Parse Error: Malformed metadata attribute at line "
                    f"{line_number}.\n[{line_number}] {line}\n"
                    "Reason: Each attribute must follow the 'key=value' "
                    f"format (missing '=' in '{d}')."

                )

            key: str
            value: str
            key, value = d.split('=', 1)

            key = key.strip()

            value = value.strip()

            if (
                not key or not value
                or key not in ["color", "zone", "max_drones"]
               ):
                raise ValueError(
                    f"Parse Error: Invalid metadata key or empty value at line"
                    f" {line_number}.\n[{line_number}] {line}\n"
                    f"Reason: Key '{key}' is unknown or missing a value. "
                    "Allowed keys are: 'color', 'zone', 'max_drones'."

                )
            if key == 'zone':
                key = 'type'
            res[key] = value

        return res

    def parse_connection(self, line: str, line_number: int) -> None:
        res: dict[str, Any] = {}

        _: str
        val: str
        _, val = line.split(':', 1)

        data: List[str] = val.strip().split(maxsplit=1)

        if len(data) < 1 or len(data) > 2:
            raise ValueError(
                f"Parse Error: Invalid connection format at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                f"Expected format: connection: <zone1>-<zone2> [metadata]"
            )

        if '-' not in data[0]:
            raise ValueError(
                f"Syntax Error: Missing dash ('-') in connection definition "
                f"at line {line_number}.\n[{line_number}] {line}\n"
                "Reason: Connection must link two zones "
                "separated by a dash (e.g., zoneA-zoneB)."
                )

        zones_connection: List[str] = data[0].strip().split('-')

        if (len(zones_connection) != 2):
            raise ValueError(
                "Parse Error: Invalid connection linkage at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                "Reason: A connection must link exactly two valid zones "
                "separated by a single"
                )

        zon1: str
        zon2: str
        zon1, zon2 = zones_connection

        past_connections: List[Tuple[str, str]] = (
            [(str(c['zon1']), str(c['zon2'])) for c in self.map['connections']]
                            )

        if (
            (zon1, zon2) in past_connections
            or (zon2, zon1) in past_connections
             ):
            raise ValueError(
                "Parse Error: Duplicate connection detected at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                f"Reason: The connection between '{zon1}' and '{zon2}' "
                "has already been defined. "
                "Bidirectional duplicates "
                "(e.g., A-B and B-A) are strictly forbidden."
            )

        if zon1 == zon2:
            raise ValueError(
                f"Parse Error: Self-loop detected at line {line_number}.\n"
                f"[{line_number}] {line}\n"
                "Reason: A zone cannot be connected to itself. "
                "Both ends of the connection must be distinct."

            )

        res['zon1'] = zon1

        res['zon2'] = zon2

        res['line'] = line

        res['line_number'] = line_number
        zones_exist: List[str] = [str(z['name']) for z in self.map['zones']]

        if zon1 not in zones_exist or zon2 not in zones_exist:
            invalid_zone: str = zon1 if zon1 not in zones_exist else zon2
            raise ValueError(
                "Parse Error: Undefined zone in connection at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                "Reason: Attempted to link a zone named "
                f"'{invalid_zone}' which has not been declared previously."
                )

        if len(data) == 2:
            if (
                data[-1][0] != '['
                or data[-1][-1] != ']'
                or len(data[-1]) < 6
                 ):
                raise ValueError(
                    "Syntax Error: Invalid metadata format at line "
                    f"{line_number}.\n[{line_number}] {line}\n"
                    "Reason: Metadata must be enclosed in brackets "
                    "(e.g., [max_link_capacity=2])."
                    )

            me_data: dict[str, str] = (self.parse_connection_metadata(
                data[-1][1:-1], line_number, line))

            res.update(me_data)
        re: ConnectionDict = cast(ConnectionDict, res)
        self.map['connections'].append(re)

    def parse_connection_metadata(self, metadata: str, line_number: int,
                                  line: str) -> dict[str, str]:

        if '=' not in metadata:
            raise ValueError(
                f"Parse Error: Malformed metadata attribute at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                f"Reason: The attribute must follow the 'key=value' format "
                "(e.g., [max_link_capacity=2])."
                )
        k: str
        v: str
        k, v = metadata.strip().split('=')

        if not k or not v:
            raise ValueError(
                f"Parse Error: Missing key or value in metadata at line "
                f"{line_number}.\n[{line_number}] {line}\n"
                "Reason: Both the key and "
                "the value must be provided around the '=' sign"
                "(e.g., [max_link_capacity=2])."
                    )

        return {k: v}
