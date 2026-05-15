from dict_format import ParsedMap, ZoneDict, ConnectionDict
from typing import cast


class ParseMap:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.map: ParsedMap = {
            "zones": [],
            "connections": [],
            "nb_drones": ""
            }

    def read_lines(self) -> None:
        first_line = False

        st_times = 0

        nb_times = 0

        end_times = 0

        with open(self.filename, 'r') as f:

            for line_number, line in enumerate(f, 1):

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                elif (line.startswith("nb_drones")):

                    if first_line or nb_times:
                        raise ValueError(
                            "nb_drones must write once time not repeat it,"
                            " and it have find the first line!!!!"
                            )

                    if ':' not in line:
                        raise ValueError(
                            "you must include ':' in line hub ->"
                            f" [{line_number}] {line}"
                            )

                    nb_times += 1

                    _, v = line.split(':', 1)

                    self.map['nb_drones'] = v
                    self.map['line'] = line
                    self.map['line_number'] = line_number

                elif (
                    line.startswith("start_hub")
                    or line.startswith("hub:")
                    or line.startswith("end_hub:")
                      ):

                    first_line = True

                    if line.startswith("start_hub"):

                        if st_times:
                            raise ValueError("start_hub must write once time \
                                             not repeat it!!!")

                        else:
                            st_times += 1

                    elif line.startswith("end_hub"):

                        if end_times:
                            raise ValueError("end_hub must write once \
                                             time not repeat it!!!")

                        else:
                            end_times += 1

                    self.parse_zone(line, line_number)

                elif (line.startswith("connection")):

                    first_line = True

                    self.parse_connection(line, line_number)

                else:
                    raise ValueError(f"this line is not correct --> \
                                     \n[{line_number}] {line}")

    def parse_zone(self, line: str, line_number: int) -> None:

        res = {}

        if ':' not in line:
            raise ValueError(f"you must include ':' in line hub ->\
                             \n[{line_number}] {line}")

        key, val = line.split(':', 1)

        data = val.split(maxsplit=3)

        if (len(data) < 3):
            raise ValueError(f"[Error] this format is not valid:\
                             \n[{line_number}] {line}\n use this format->\
                               {key}: <name> <x> <y> [metadata]")

        if ('-' in data[0]):
            raise ValueError(f"dont use dashes '-' in name of zones:\
                             \n[{line_number}] {line}")

        last_zones = [z['name'] for z in self.map['zones']]

        if data[0] in last_zones:
            raise ValueError(f"this zone in this line it was found before: \
[{line_number}] {line}")

        res['key'] = key.strip()

        res['name'] = data[0]

        res['x'] = data[1]

        res['y'] = data[2]
        res['line'] = line
        res['line_number'] = line_number

        if len(data) == 4:

            metadata = data[-1].strip()

            if metadata[0] != '[' or metadata[-1] != ']' or len(metadata) < 6:
                raise ValueError(f"metadata is not valid in this line: \
                                 [{line_number}] {line}")

            res_data = (self.
                        parse_zone_metadata(data[-1][1:-1], line_number, line)
                        )

            res.update(res_data)
        re = cast(ZoneDict, res)
        self.map['zones'].append(re)

    def parse_zone_metadata(self, metadata: str, line_number: int,
                            line: str) -> dict[str, str]:

        res = {}

        data = metadata.strip().split()

        if (len(data) > 3 or len(data) == 0):
            raise ValueError(f"metadata is not valid in this line: \
                             [{line_number}] {line}")

        for d in data:

            if '=' not in d:
                raise ValueError(f"metadata is not correct in this line must \
                                 include '=' : [{line_number}] {line}")

            key, value = d.split('=', 1)

            key = key.strip()

            value = value.strip()

            if (
                not key or not value
                or key not in ["color", "zone", "max_drones"]
               ):
                raise ValueError(f"metadata is not valid in this line : \
[{line_number}] {line}")
            if key == 'zone':
                key = 'type'
            res[key] = value

        return res

    def parse_connection(self, line: str, line_number: int) -> None:

        res = {}

        if ':' not in line:
            raise ValueError(f"you must include ':' in line connection -> \
[{line_number}] {line}")

        _, val = line.split(':', 1)

        data = val.strip().split()

        if len(data) > 2 or len(data) < 1 or '-' not in data[0]:
            raise ValueError(f"this format is not valid in this line: \
                             [{line_number}] {line}")

        zones_connection = data[0].strip().split('-')

        if not (len(zones_connection) == 2):
            raise ValueError(f"this format is not valid, zones \
                             connections must split it by just one\
                              '-':\n[{line_number}] {line}")

        zon1, zon2 = zones_connection

        past_connections = (
            [(c['zon1'], c['zon2']) for c in self.map['connections']]
                            )

        if (
            (zon1, zon2) in past_connections
            or (zon2, zon1) in past_connections
             ):
            raise ValueError(f"the connection in this line is repeat find it \
two times -->\n[{line_number}] {line}")
        if zon1 == zon2:
            raise ValueError(f"the connection can't have one zone linked to \
itself !  -->\n[{line_number}] {line}")

        res['zon1'] = zon1

        res['zon2'] = zon2

        res['line'] = line

        res['line_number'] = line_number
        zones_exist = [z['name'] for z in self.map['zones']]

        if zon1 not in zones_exist or zon2 not in zones_exist:
            raise ValueError(f"in this line connection there \
                             a zone not find before:\n[{line_number}] {line}")

        if len(data) == 2:
            if (
                data[-1][0] != '['
                or data[-1][-1] != ']'
                or len(data[-1]) < 6
                 ):
                raise ValueError(f"metadata is not valid in this line:\
                                  [{line_number}] {line}")

            me_data = (self.parse_connection_metadata
                       (data[-1][1:-1], line_number, line))

            res.update(me_data)
        re = cast(ConnectionDict, res)
        self.map['connections'].append(re)

    def parse_connection_metadata(self, metadata: str, line_number: int,
                                  line: str) -> dict[str, str]:

        if '=' not in metadata:
            raise ValueError(f"metadata is not valid in this line:\
                              [{line_number}] {line}")

        k, v = metadata.strip().split('=')

        if not k or not v:
            raise ValueError(f"connection metadata is not valid in this line\
                              -> [{line_number}] {line}")

        return {k: v}
