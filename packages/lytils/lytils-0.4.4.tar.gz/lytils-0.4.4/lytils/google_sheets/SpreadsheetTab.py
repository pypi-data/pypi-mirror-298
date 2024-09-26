# Third-party libraries
from gspread import Worksheet
from gspread_formatting import batch_updater
from gspread_formatting import format_cell_range, set_data_validation_for_cell_range
from pandas import DataFrame

# Local libraries
from lytils import cprint
from lytils.google_sheets.Columns import Columns
from lytils.google_sheets.format import HeaderFormat
from lytils.google_sheets.helpers import (
    get_column_letter,
    get_column_number,
    get_data_range,
    get_header_range,
)
from lytils.regex import match


class SpreadsheetTab:
    def __init__(self, tab: Worksheet):
        self.__tab = tab
        self.__batch = batch_updater(self.__tab.spreadsheet)

    # Get path in terms of Spreadsheet > Worksheet
    def get_path(self):
        return f"{self.__tab.spreadsheet.title} > {self.__tab.title}"

    # Get all data
    def get_all_data(self) -> DataFrame:
        data = self.__tab.get_values()
        if len(data) > 1:
            return DataFrame(data[1:], columns=data[0])
        else:
            return DataFrame()

    # Get data from specific range
    def get_range(self, range: str, headers: bool = True) -> DataFrame:
        data = self.__tab.get(range)

        if data:
            if headers:
                headers_row = data.pop(0)  # Use the first row as headers
                df = DataFrame(data, columns=headers_row)
            else:
                df = DataFrame(data)
        else:
            df = DataFrame()

        df = df.fillna("")  # Replace None values with an empty string
        return df

    # Clear all data
    def clear(self) -> None:
        self.__tab.clear()

    # Clear specific ranges
    def clear_ranges(self, ranges: list[str]) -> None:
        self.__tab.batch_clear(ranges=ranges)

    # Format single column
    def format_column(self, header, format, header_row=1):
        headers = self.__tab.row_values(header_row)

        # +1 because Google Sheets is 1-indexed
        header_index = headers.index(header) + 1

        column_letter = get_column_letter(header_index)
        format_range = f"{column_letter}{header_row + 1}:{column_letter}"
        format_cell_range(self.__tab, format_range, format)

    # Apply formatting to columns
    def format_columns(
        self,
        columns: Columns,
        column_start: str = "A",
        row_start: int = 2,  # Row starts at 2 to account for headers
        row_end: int | None = None,
    ):
        col_start = get_column_number(column_start)
        formats = []
        for i, col in enumerate(columns.as_list(), start=col_start):
            column_letter = get_column_letter(i)
            row_end = "" if row_end is None else row_end
            formats.append(
                [
                    f"{column_letter}{row_start}:{column_letter}{row_end}",
                    col.get_format(),
                ]
            )
        self.__batch.format_cell_ranges(self.__tab, formats)

    # Validate single column
    def validate_column(self, header, validation, header_row=1):
        headers = self.__tab.row_values(header_row)

        # +1 because Google Sheets is 1-indexed
        header_index = headers.index(header) + 1

        column_letter = get_column_letter(header_index)
        validate_range = f"{column_letter}{header_row + 1}:{column_letter}"
        set_data_validation_for_cell_range(self.__tab, validate_range, validation)

    # Validate multiple columns
    def validate_columns(
        self,
        columns: Columns,
        column_start: str = "A",
        row_start: int = 2,  # Row starts at 2 to account for headers
        row_end: int | None = None,
    ):
        col_start = get_column_number(column_start)
        validations = []
        for i, col in enumerate(columns.as_list(), start=col_start):
            column_letter = get_column_letter(i)
            row_end = "" if row_end is None else row_end
            validations.append(
                [
                    f"{column_letter}{row_start}:{column_letter}{row_end}",
                    col.get_validation(),
                ]
            )
        self.__batch.set_data_validation_for_cell_ranges(self.__tab, validations)

    # Set desired column widths
    def set_column_widths(self, columns: Columns, column_start: int = 1):
        widths = []
        for i, col in enumerate(columns.as_list(), start=column_start):
            column_letter = get_column_letter(i)
            widths.append(
                [
                    f"{column_letter}",
                    col.get_width(),
                ]
            )
        self.__batch.set_column_widths(self.__tab, widths)

    # Clear worksheet and populate with new data. Assumes headers.
    def set_all_data(self, data_frame: DataFrame, columns: Columns) -> None:
        self.clear()

        cprint(f"Outputting data to <c>{self.get_path()}<w>...")

        # Correct column order
        order = [col.get_header() for col in columns.as_list()]
        ordered_df = data_frame[order]

        # Replace NaN with empty string, resulting in empty cells
        df = ordered_df.fillna(value="")

        headers = df.columns.tolist()
        data = df.values.tolist()

        # Format headers
        self.__batch.format_cell_range(self.__tab, "1:1", HeaderFormat())

        # * Format after setting data to include new rows in formatting
        self.format_columns(columns)
        self.validate_columns(columns)
        self.set_column_widths(columns)

        # Execute bulk request
        self.__batch.execute()

        # * Formatting has to come BEFORE updates to format correctly

        # Set headers
        self.__tab.update(values=[headers], range_name="1:1")

        # Freeze the top row
        self.__tab.freeze(rows=1)

        # Set data
        self.__tab.update(
            values=data,
            range_name="A2",
            value_input_option="USER_ENTERED",
        )

    # Clear range and set new range with data. Assumes headers.
    def set_range(
        self,
        range: str,
        data_frame: DataFrame,
        columns: Columns,
    ) -> None:
        cprint(f"Outputting data to <c>{self.get_path()} ({range})<w>...")

        # Correct column order
        order = [col.get_header() for col in columns.as_list()]
        try:
            ordered_df = data_frame[order]
        except KeyError:
            cprint(f"<y>df columns: {data_frame.columns}")
            cprint(f"<y>order: {order}")
            raise KeyError

        # Replace NaN with empty string, resulting in empty cells
        df = ordered_df.fillna(value="")

        header_range = get_header_range(range)
        data_range = get_data_range(range)

        headers = df.columns.tolist()
        data = df.values.tolist()

        self.clear_ranges(ranges=[range])

        # Format headers
        self.__batch.format_cell_range(self.__tab, header_range, HeaderFormat())

        # * Format after setting data to include new rows in formatting
        column_start = match(r"[A-Z]+", data_range, group=1)
        row_start = match(r"[0-9]+", data_range, group=1)
        self.format_columns(columns, column_start=column_start, row_start=row_start)
        self.validate_columns(columns, column_start=column_start, row_start=row_start)
        self.set_column_widths(columns, column_start=get_column_number(column_start))

        # Execute bulk request
        self.__batch.execute()

        # * Formatting has to come BEFORE updates to format correctly

        # Set headers
        self.__tab.update(header_range, [headers])

        # Set data
        self.__tab.update(
            range_name=data_range,
            values=data,
            value_input_option="USER_ENTERED",
        )
