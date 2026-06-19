from typing import Any


class LineError:
    @staticmethod
    def find_line_content_and_number_line(data: dict[str, Any],
                                          loc_data: tuple[Any, ...]
                                          ) -> tuple[str, int]:
        line_content: str
        line_number: int

        if loc_data[0] == 'nb_drones':
            line_content = str(data['line'])
            line_number = int(data['line_number'])
        else:
            line_content = str(data[loc_data[0]][loc_data[1]]['line'])
            line_number = int(data[loc_data[0]][loc_data[1]]['line_number'])

        return line_content, line_number
