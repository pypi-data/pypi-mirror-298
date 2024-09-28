"""abheader.py"""


class AbHeader:
    """Python class to store and manipulate AB Matrix header data"""

    # Initialize AB Sample data structure
    def __init__(self):
        self._data = {}

    def set(self, field, value):
        """Set value of header field

        Parameters
        ----------

        field : string
            header field name

        Returns
        -------

        None

        """
        self._data[field] = value

    def get(self, field):
        """Get value from specified header field

        Returns
        -------

        Value of specified header field or None if field does not exist

        """
        try:
            value = self._data[field]
        except KeyError:
            return None
        else:
            return value

    def iter_items(self):
        """Iterate through header items

        Returns
        -------

        Header item

        """
        for item in self._data.items():
            yield item
