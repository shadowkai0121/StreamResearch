from abc import ABC
import pandas as pd


class ConvertMixin(ABC):
    _columns: tuple
    data: dict

    def __init__(self, *args, **kwargs):
        '''
        Raises:
            NotImplementedError: If `_columns` is not defined or is empty.
            NotImplementedError: If `self.data` is not defined or is set to `None`.
        '''
        super().__init__(*args, **kwargs)
        if not isinstance(self._columns, tuple) or not self._columns:
            raise NotImplementedError(
                'ConvertMixin must define a non-empty `_columns` tuple attribute.')

        if not isinstance(self.data, dict) or not self.data:
            raise NotImplementedError(
                'ConvertMixin must define a non-empty `self.data` tuple attribute.')

    def to_dict(self) -> dict:
        '''
        Converts the instance data to a dictionary format.

        Returns:
            dict: A dictionary containing the instance's data.
        '''
        return self.data

    def to_dataframe(self) -> pd.DataFrame:
        '''
        Converts the instance data to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the instance's data, structured 
                based on the `_columns` attribute.
        '''
        missing_columns = [col for col in self._columns if col not in self.data]
        if missing_columns:
            raise ValueError(f"Missing data for columns: {missing_columns}")
        return pd.DataFrame([self.data], columns=self._columns)
