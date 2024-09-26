from typing import List

from commonlib_reader.utils import attributes_list_to_dict, get_code


class Facility:
    """
    Facility class to encapsulate information.

    Attributes:
        identity (str)         : A unique identifier for the facility (read from the data source).
        name (str)             : The name of the facility (read from the data source).
        description (str)      : A description of the facility (read from the data source).
        SAPPlant (str)         : SAP Plant code (if available).
        Field (str)            : Field identifier associated with the facility (if available).
        ParentFacility (str)   : Parent facility identifier (if available).
        NPDID (str)            : NPD ID (if available).

    _cache (list of dict, optional):
        Class level cache to store facility data, to minimize data source access.

    """

    _cache = None

    def __init__(self, code):
        """
        Initializes the Facility instance by retrieving data related to the given STID plant code.

        Parameters:
            code (str): The code used to retrieve facility data from the data source.

        Raises:
            ValueError: If no data is found for the provided code.
        """
        self._data = Facility._get_facility(code=code)
        self._attributes = attributes_list_to_dict(self._data["attributes"])

        self.identity = self._data["identity"]
        self.name = self._data["name"]
        self.description = self._data["description"]

        common_attributes = ["SAPPlant", "Field", "ParentFacility", "NPDID"]
        for attr in common_attributes:
            self.__setattr__(attr, "")

        for key, val in self._attributes.items():
            if key in common_attributes:
                self.__setattr__(key, val)

    def isSTID(self):
        """
        Checks if the facility is marked for STID.

        Returns:
            bool: True if the facility is marked for STID, False otherwise.
        """
        if "IsForSTID" in self._attributes.keys():
            if self._attributes["IsForSTID"] == "True":
                return True

        return False

    @classmethod
    def get_all_facilities(cls) -> List["Facility"]:
        """
        Retrieves and returns a list of Facility instances for all known facilities.

        Returns:
            List[Facility]: A list of Facility instances.
        """
        f = Facility._get_all_facilities()
        return [Facility(x["identity"]) for x in f]

    @classmethod
    def _get_all_facilities(cls) -> List[dict]:
        """
        Retrieves all facility data, using a class level cache.

        Returns:
            List[dict]: A list of dictionaries, each representing facility data.
        """
        if cls._cache is None:
            cls._cache = get_code("Facility")

        return cls._cache

    @classmethod
    def _get_facility(cls, code) -> dict:
        """
        Retrieves the facility data for the given code.

        Parameters:
            code (str): The STID plant code corresponding to the facility.

        Returns:
            dict: A dictionary containing data related to the facility.

        Raises:
            ValueError: If no data is found for the provided code.
        """
        for f in cls._get_all_facilities():
            if f["identity"] == code or f["name"] == code or f["description"] == code:
                return f
        raise ValueError(f"No data found for {code}")
