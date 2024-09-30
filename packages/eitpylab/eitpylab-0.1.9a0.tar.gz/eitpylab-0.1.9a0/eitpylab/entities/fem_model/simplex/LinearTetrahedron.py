import numpy as np

from scipy import linalg as scipyLinalg

from eitpylab.entities.fem_model.simplex.UniformRho import SimplexUniformRho


class LinearTetrahedron(SimplexUniformRho):
    """
    Represents a linear tetrahedral element in a finite element model.

    This class defines the properties and behaviors of a linear tetrahedral element, including its geometry, material properties, and interactions with the FEM model.

    Attributes:
        element_id (int): The unique identifier for the element.
        nodes (numpy.ndarray): The nodes of the tetrahedral element.
        coords (numpy.ndarray): The coordinates of the nodes.
        rho (float): The resistivity of the element.
        propertiesDict (dict): A dictionary containing the properties of the element.
        volume (float): The volume of the tetrahedral element.
        centroid (numpy.ndarray): The centroid of the tetrahedral element.
        Kgeom (numpy.ndarray): The geometric component of the local stiffness matrix.
    """

    def __init__(self, elemNbr, connectivity, coords, rho, propertiesDict=None):
        """
        Initializes the LinearTetrahedron with the given parameters.

        Args:
                element_id (int): The unique identifier for the element.
                nodes (numpy.ndarray): The nodes of the tetrahedral element.
                coords (numpy.ndarray): The coordinates of the nodes.
                rho (float): The resistivity of the element.
                propertiesDict (dict): A dictionary containing the properties of the element.
        """
        dimension = 3
        super().__init__(
            elemNbr, dimension, connectivity, coords, rho, False, propertiesDict
        )
        self.type = "4-node tetrahedron, linear".lower()
        self.volume = self.calcSimplexVolume()
        self._calc_localKgeom()

    def _calc_localKgeom(self):
        """
        Computes the geometric component of the local stiffness matrix for the tetrahedral element.

        This method calculates the local stiffness matrix based on the geometry and material properties of the tetrahedral element.

        Args:
            None

        Returns:
            numpy.ndarray: The geometric component of the local stiffness matrix.
        """
        M = np.hstack((np.ones([4, 1]), self.coords))
        F = scipyLinalg.inv(M)[1:, :]

        # does not need to divide by (6xVolume)^2 bc I am inverting M directly
        self.Kgeom = self.volume * np.dot(F.T, F)
