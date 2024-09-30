import numpy as np
import multiprocessing as mp

from scipy import linalg as scipyLinalg

from eitpylab.entities.fem_model.rho_region.UniformRhonRegion import UniformRhoRegion
from eitpylab.entities.fem_model.utils import areaTriangle
from eitpylab.utils.proc_cores import CPUCores

CpuCores = CPUCores()

n_cores = CpuCores.get_half_cores()


class CoreElectrodeHua:
    """
    CoreElectrodeHua class represents the core functionality of an electrode in Hua's model.

    This class handles both 2D and 3D models:
    - 2D: rectangular region, compressed into 3 nodes.
    - 3D: hexahedron region, compressed into 4 nodes.
    The virtual node is the last one in the connectivity array.

    Attributes:
        number (int): Number of the element.
        dim (int): Dimension of the model (2 or 3).
        type (str): Type of the electrode.
        connectivity (numpy.ndarray): Nodes of the element in global terms.
        coords (numpy.ndarray): Coordinates of the nodes.
        centroid (numpy.ndarray): Centroid of the element.
        isSparse (bool): Indicates if the element is sparse.
        isRegion (bool): Indicates if the element is a region.
        nNodes (int): Number of nodes in the element.
        height2D (float or None): Height of the triangular element (used only if dim=2).
        contactArea (float): Contact area of the electrode.
        propertiesDict (dict or None): Dictionary containing the properties of the simplex.
        rhoT (float): Electrode parameter (rho * t).
        Kgeom (numpy.ndarray or None): Geometric component of the local stiffness matrix.

    Methods:
        _calc_localKgeom(): Computes the geometric component of the local stiffness matrix.
    """ 
    def __init__(self, dimension,  
                 elemNbr,  
                 connectivity,  
                 coords,  
                 rhoT, 
                 height2D=1.0,  
                 propertiesDict=None  
                 ):
        """
        Initializes the CoreElectrodeHua with the given attributes.

        Parameters
        ----------
        dimension : int {2, 3}
            Dimension of the model.
        elemNbr : int
            Number of the element.
        connectivity : numpy.ndarray
            Nodes of the element in global terms. The local order of the nodes will be the same as the connectivity input.
            The last node is the number of the virtual node.
        coords : numpy.ndarray
            Each row is composed of 3 columns (X, Y, and Z) of the node. This matrix should contain all nodes of the FemModel, except the virtual node.
            The function will extract only the needed rows.
        rhoT : float
            Electrode parameter (rho * t) from Hua's model.
        height2D : float, optional
            Associated height of the triangular element (used only if dim=2). Default is 1.0.
        propertiesDict : dict, optional
            Dictionary containing the properties of the simplex. Default is None.
        """
        self.number = elemNbr
        self.dim = dimension
        self.type = 'completeElectrode core Hua'.lower()
        self.connectivity = connectivity.astype(int)
        self.coords = coords[connectivity[:-1], :]
        self.centroid = np.mean(self.coords, axis=0)
        self.isSparse = False
        self.isRegion = False

        if self.dim == 2:
            self.nNodes = 3
            self.height2D = height2D
            self.contactArea = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :]) * self.height2D
        else:
            self.nNodes = 4
            self.height2D = None
            self.contactArea = areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[2, :])

        self.propertiesDict = propertiesDict
        self.rhoT = rhoT

        self.Kgeom = None
        self._calc_localKgeom()

    def _calc_localKgeom(self):
        """
        Compute the geometric component of the local stiffness matrix.

        For 2D models:
        - Calculates the length of the edge between the first two nodes.
        - Computes the local stiffness matrix using the length and height of the triangular element.

        For 3D models:
        - Calculates the area of the triangle formed by the first three nodes.
        - Computes the local stiffness matrix using the area of the triangle.

        The resulting local stiffness matrix is stored in the `Kgeom` attribute.
        """
        if self.dim == 2:
            length = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :])
            self.Kgeom = (length * self.height2D / 6.0) * np.array([[2.0, 1.0, -3.0], [1.0, 2.0, -3.0], [-3.0, -3.0, 6.0]])
        else:
            v1 = self.coords[1, :] - self.coords[0, :]
            v2 = self.coords[2, :] - self.coords[0, :]
            area = 0.5 * scipyLinalg.norm(np.cross(v1, v2))
            self.Kgeom = (area / 3.0) * np.array([[1.0, 0.0, 0.0, -1.0], [0.0, 1.0, 0.0, -1.0], [0.0, 0.0, 1.0, -1.0], [-1.0, -1.0, -1.0, 3.0]])


class CompleteElectrodeHua(UniformRhoRegion):
    """
    Hua's complete electrode model.
    A class used to represent the complete electrode model for the Hua configuration in electrical impedance tomography (EIT).

    This class defines the properties and behaviors of the complete electrodes used in the Hua model, including their geometry, material properties, boundary conditions, and interactions with the FEM model.
    """

    def __init__(self, dimension,  
                 elemNbr,  
                 connectivities,  
                 coords,  
                 rhoT,  
                 height2D,  
                 virtualNodeNbr,  
                 isSparse=False,  
                 propertiesDict=None  
                 ):
        """
        Initializes the CompleteElectrodeHua with the given attributes.

        Parameters
        ----------
        dimension : int {2, 3} Dimension of the electrode model.
            
        elemNbr : int Number of the element, considering the elements of the domain.
        connectivities : numpy.ndarray
            Nodes of the elements in global terms. The local order of the nodes will be the same as the connectivity input.
            This array must not contain the virtual node.
            - lines: elements that compose the electrode
            - cols: connectivity of each element
        coords : numpy.ndarray
            Each row is composed of 3 columns (X, Y, and Z) of the node. This matrix should contain all nodes of the FemModel.
            The function will extract only the needed rows.
        rhoT : float
            Electrode parameter (rho * t) from Hua's model.
        height2D : float
            Associated height of the triangular element (used only if dim=2).
        virtualNodeNbr : int
            Virtual node of the electrode in global terms. This node will be the last.
        isSparse : bool, optional
            Computes local matrix as sparse. Default is False.
        propertiesDict : dict, optional
            Dictionary containing the properties of the element. Default is None.
        """

        self.number = elemNbr
        self.dim = dimension
        self.type = 'completeElectrode Hua'.lower()
        self.propertiesDict = propertiesDict
        self.rhoT = rhoT
        self.isSparse = isSparse
        self.isRegion = True

        if self.dim == 2:
            self.height2D = height2D
        else:
            self.height2D = None

        # register the virtual node
        self.virtualNodeNbr = virtualNodeNbr
        connectivities = np.hstack((connectivities, self.virtualNodeNbr * np.ones([connectivities.shape[0], 1])))

        # build local connectivity
        self.connectivity, connectivityLocal = np.unique(connectivities, return_inverse=True)
        self.connectivity = self.connectivity.astype(int)
        self.connectivityElementsLocal = connectivityLocal.reshape(len(connectivityLocal) // connectivities.shape[1], connectivities.shape[1])

        # total number of elements and nodes of the region
        self.nNodes = self.connectivity.shape[0]
        self.nElements = self.connectivityElementsLocal.shape[0]

        self.coords = coords[self.connectivity[:-1], :]  # does not contain the coords of the virtual node!

        self.elements = None
        self.appendElements()

        # calc centroid of the contact Area
        areas = np.array([e.contactArea for e in self.elements])
        centroids = np.array([e.centroid for e in self.elements])
        self.centroid=np.average(centroids, axis=0, weights=areas)

        if self.isSparse:
            self._calc_localKgeom_Sparse()
        else:
            self._calc_localKgeom()

    def setRhoT(self, rhoT  
               ):
        """
        Sets the resistivity (rho_t) for the electrode.

        This method assigns a resistivity value to the electrode, which is used in the FEM model to calculate electrical properties.

        Args:
            rho_t (float): The resistivity value to be assigned to the electrode.

        Returns:
            None

        Raises:
            ValueError: If the provided resistivity value is not a positive number.
        """
        self.rhoT = rhoT
        for e in self.elements:
            e.rhoT = rhoT

    def appendElements(self):
        """
        Appends elements to the electrode model.

        This method adds new elements to the existing set of elements associated with the electrode.

        Args:
            elements (numpy.ndarray): An array of elements to be appended to the electrode.

        Returns:
            None

        Raises:
            ValueError: If the provided elements are not of the same dimension as the electrode.
        """
        self.elements=[]
        for i, c in enumerate(self.connectivityElementsLocal):
            proPDict = self.propertiesDict.copy()
            proPDict['gmshElemNbr'] = proPDict['gmshElemNbr'][i]
            self.elements.append(CoreElectrodeHua(self.dim,i,c,self.coords, self.rhoT, self.height2D, proPDict))

        self.nElements = len(self.elements)
