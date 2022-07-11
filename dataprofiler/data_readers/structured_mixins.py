import pandas as pd

from .. import dp_logging

logger = dp_logging.get_child_logger(__name__)


class SpreadSheetDataMixin(object):
    """
    Mixin data class for loading datasets of type SpreadSheet. Can be specified
    Adds specialized functions for loading data from a string or file.

    :param input_file_path: path to the file being loaded or None
    :type input_file_path: str
    :param data: data being loaded into the class instead of an input file
    :type data: multiple types
    :param options: options pertaining to the data type
    :type options: dict
    :return: None
    """

    def __init__(self, input_file_path, data, options):
        self._data_formats["dataframe"] = self._get_data_as_df
        if data is not None and isinstance(data, pd.DataFrame):
            self._original_df_dtypes = data.dtypes
        else:
            self._original_df_dtypes = None
        self.SAMPLES_PER_LINE_DEFAULT = int(5e9)

    def _load_data_from_str(self, data_as_str):
        """Loads the data into memory from the str."""
        raise NotImplementedError()

    def _load_data_from_file(self, input_file_path):
        """Loads the data into memory from the file."""
        raise NotImplementedError()

    def _load_data(self, data=None):
        """Loads either the specified data or the input_file into memory."""
        if data is not None:
            if isinstance(data, pd.DataFrame):
                self._data = data
            elif data is not None and isinstance(data, str):
                self._data = self._load_data_from_str(data)
            elif data is not None:
                raise ValueError("Input data type is not string or pandas.DataFrame")
        elif self.input_file_path:
            self._data = self._load_data_from_file(self.input_file_path)
        else:
            raise ValueError("No data to load.")

    def _get_data_as_df(self, data):
        if not isinstance(data, pd.DataFrame):
            raise ValueError(
                "Data is not in a dataframe state and cannot be converted."
            )
        return data

    def _get_data_as_records(self, data):
        records_per_line = min(len(data), self.SAMPLES_PER_LINE_DEFAULT)
        data = [
            str(
                "\n".join(data[i * records_per_line : (i + 1) * records_per_line])
                .encode("UTF-8")
                .decode()
            )
            for i in range((len(data) + records_per_line - 1) // records_per_line)
        ]
        return data
