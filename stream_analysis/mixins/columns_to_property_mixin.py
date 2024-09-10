from abc import ABC


class ColumnsToPropertyMixin(ABC):
    """
    Mixin that dynamically generates the `_columns` attribute by collecting
    all attributes from the class that are defined with type annotations.
    """
    _columns: tuple
    data: dict = {}

    def __init_subclass__(cls, **kwargs):
        """
        properties for each column in `_columns` are dynamically generated.
        """
        super().__init_subclass__(**kwargs)

        if not isinstance(cls._columns, tuple) or not cls._columns:
            raise NotImplementedError(
                "ColumnsToPropertyMixin must define a non-empty '_columns' attribute.")

        for column in cls._columns:
            if not hasattr(cls, column):
                setattr(cls, column, property(
                    lambda self, col=column: self.data.get(col)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'data') or self.data is None:
            raise NotImplementedError(
                "ColumnsToPropertyMixin must define 'self.data' and ensure it's not None.")
