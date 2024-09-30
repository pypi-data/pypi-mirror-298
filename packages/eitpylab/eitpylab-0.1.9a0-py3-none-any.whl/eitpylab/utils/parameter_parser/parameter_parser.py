import os
from ruamel.yaml import YAML


class EitParameterParser(YAML):
    """
    Class responsible for parsing and managing parameter files.

    This class is responsible for reading and managing parameter files.

    Attributes:
        None
    """

    def __init__(self, eit_parameter_path):
        """
        Initialize the EitParameterParser.

        :param eit_parameter_path: (str) The path to the EIT parameter file.
        """
        super().__init__()
        self.eit_parameter_path = eit_parameter_path
        self.__set_parameter()

    def __set_parameter(self):
        """
        Set the parameter for the EIT parameter file.

        :raises ValueError: If the file is not found or if there is an error while loading the parameters.
        """
        if not os.path.exists(self.eit_parameter_path):
            raise ValueError("ERROR - File not found.")
        with open(self.eit_parameter_path, "r") as params:
            try:
                self.eit_parameter = self.load(params)
            except Exception as exc:
                raise exc

    def get_eit_parameter(self):
        """
        Get the EIT parameter object.

        :return: EitInputModel: An instance of the corresponding model.

        :raises ValueError: If the specified parameter file is missing.
        """
        try:
            return self.eit_parameter
        except KeyError:
            raise ValueError("ERROR - Missing EIT parameter file.")
