import numpy as np

from scipy import linalg as scipyLinalg

from eitpylab.entities.fem_model.simplex.UniformRho import SimplexUniformRho
from eitpylab.entities.fem_model.utils import localRefSystem2D


class LinearTriangle(SimplexUniformRho):
    """
    Represents a linear triangular element in a finite element model.

    This class defines the properties and behaviors of a linear triangular element, including its geometry, material properties, and interactions with the FEM model.

    Attributes:
        element_id (int): The unique identifier for the element.
        nodes (numpy.ndarray): The nodes of the triangular element.
        coords (numpy.ndarray): The coordinates of the nodes.
        rho (float): The resistivity of the element.
        propertiesDict (dict): A dictionary containing the properties of the element.
        area (float): The area of the triangular element.
        centroid (numpy.ndarray): The centroid of the triangular element.
        Kgeom (numpy.ndarray): The geometric component of the local stiffness matrix.
    """

    def __init__(self, elemNbr,  
                 connectivity,  
                 coords,  
                 rho,  
                 height2D=1.0,  
                 propertiesDict=None  
                 ):
        """
        Initializes the LinearTriangle with the given parameters.

        Args:
                elemNbr: int
                        number of the element
                
                connectivity: 1D numpy array
                        nodes of the element, in global terms. the local order of the nodes will be the same of
                        connectivity input
                        
                coords: 2D numpy array
                        each row is composed by 3 columns, X, Y and Z of the node. this matrix should contain all nodes
                        of the FemModel. The function will extract only the needed lines
                        
                rho: float
                        resistivity of the element
                        
                height2D: float
                        associated height of the triangular element
                propertiesDict: dictionary, optional
                        dictionary containing the properties of the simplex:
                        'physical': physical entity group
                        ''
        """
        dimension = 2
        super().__init__(elemNbr, dimension, connectivity, coords, rho, False, propertiesDict)
        self.type = '3-node triangle, linear'.lower()
        self.height2D = height2D
        self.area = self.calcSimplexVolume()
        self._calc_localKgeom()

    def _calc_localKgeom(self):
        """
        Computes the geometric component of the local stiffness matrix for the triangular element.

        This method calculates the local stiffness matrix based on the geometry and material properties of the triangular element.

        Args:
            None

        Returns:
            numpy.ndarray: The geometric component of the local stiffness matrix.
        """
        v2 = self.coords[1, :] - self.coords[0, :]
        v3 = self.coords[2, :] - self.coords[0, :]
        v1local = np.array([0, 0])
        [v2local, v3local] = localRefSystem2D(v2, v3)

        M = np.ones([3, 3])
        M[:, 1:] = np.vstack([v1local, v2local, v3local])

        F = scipyLinalg.inv(M)[1:, :]

        # does not need to divide by (2xArea)^2 bc I am inverting M directly
        self.Kgeom = self.height2D * self.area * np.dot(F.T, F)

