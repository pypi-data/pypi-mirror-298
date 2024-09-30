import numpy as np
from scipy import sparse as scipySparse
import multiprocessing as mp

from eitpylab.entities.fem_model.simplex.LinearTetrahedron import LinearTetrahedron
from eitpylab.entities.fem_model.simplex.LinearTriangle import LinearTriangle
from eitpylab.utils.proc_cores import CPUCores

CpuCores = CPUCores()

cores_usage = CpuCores.get_half_cores()

class UniformRhoRegion:
    """
    Represents a uniform resistivity region element in a finite element model.

    This class defines the properties and behaviors of a region with uniform resistivity, including its geometry, material properties, and interactions with the FEM model.

    Attributes:
        number (int): The unique identifier for the element.
        dim (int): The dimension of the element (2 or 3).
        type (str): The type of the region, set to 'uniform region, linear'.
        propertiesDict (dict): A dictionary containing the properties of the simplex.
        rho (float): The resistivity of the element.
        isSparse (bool): Indicates whether the local matrix is computed as sparse.
        isRegion (bool): Indicates that this is a region element.
        height2D (float or None): The associated height of the triangular element, used only if dim=2.
        connectivity (numpy.ndarray): The unique nodes of the elements in global terms.
        connectivityElementsLocal (numpy.ndarray): The local connectivity of each element.
        nNodes (int): The total number of nodes in the region.
        nElements (int): The total number of elements in the region.
        coords (numpy.ndarray): The coordinates of the nodes in the region.
        centroid (numpy.ndarray): The centroid of the region.
        elements (list): The elements composing the region.
        Kgeom (numpy.ndarray or scipy.sparse.coo_matrix): The geometric component of the local stiffness matrix.
    """

    def __init__(self, dimension,  
                 elemNbr,  
                 connectivities,  
                 coords,  
                 rho,  
                 height2D,  
                 isSparse=False, 
                 propertiesDict=None 
                 ):
        """
        Initializes the UniformRhoRegion with the given parameters.

        Parameters
        ----------
        dimension : int {2,3}
            Dimension of the element.
        elemNbr : int
            Number of the element.
        connectivities : 2D numpy array
            Nodes of the elements in global terms. The local order of the nodes will be the same as the connectivity input.
            - lines: elements that compose the region.
            - cols: connectivity of each element.
        coords : 2D numpy array
            Each line is composed of 3 columns: X, Y, and Z of the node. This matrix should contain all nodes of the FemModel. The function will extract only the needed lines.
        rho : float
            Resistivity of the element.
        height2D : float
            Associated height of the triangular element. Used only if dim=2.
        isSparse : bool, optional
            Computes the local matrix as sparse. Default is False.
        propertiesDict : dict, optional
            Dictionary containing the properties of the simplex:
            - 'physical': physical entity group.
        """
        self.number = elemNbr
        self.dim = dimension
        self.type = 'uniform region, linear'.lower()
        self.propertiesDict = propertiesDict
        self.rho = rho
        self.isSparse = isSparse
        self.isRegion = True

        if self.dim == 2:
            self.height2D = height2D
        else:
            self.height2D = None

        # build local connectivity
        self.connectivity, connectivityLocal = np.unique(connectivities, return_inverse=True)
        self.connectivity = self.connectivity.astype(int)
        self.connectivityElementsLocal = connectivityLocal.reshape(len(connectivityLocal) // connectivities.shape[1], connectivities.shape[1])

        # total number of elements and nodes of the region
        self.nNodes = self.connectivity.shape[0]
        self.nElements = self.connectivityElementsLocal.shape[0]

        self.coords = coords[self.connectivity, :]

        self.centroid = np.mean(self.coords, axis=0)

        self.elements = None
        self.appendElements()

        # calc centroid of the contact Area
        if self.dim ==2:
            weights = np.array([e.area for e in self.elements])
        if self.dim ==3:
            weights = np.array([e.volume for e in self.elements])

        centroids = np.array([e.centroid for e in self.elements])
        self.centroid=np.average(centroids, axis=0, weights=weights)

        if self.isSparse:
            self._calc_localKgeom_Sparse()
        else:
            self._calc_localKgeom()

    def saveKgeom(self, fileName,  # type: str
                  binary=False  # type: bool
                  ):
        """
        Saves the geometric component of the matrix to a text file.

        Parameters
        ----------
        fileName : str
            File path.
        binary : bool, optional
            Save in binary format. Used only if the matrix is not sparse. Default is False.
        """
        if self.isSparse:
            scipySparse.save_npz(fileName, self.Kgeom, compressed=True)

        else:
            if binary:
                np.save(fileName, self.Kgeom)
            else:
                np.savetxt(fileName, self.Kgeom)

    def setRho(self, rho  # type: float
               ):
        """
        Sets the resistivity of the region and all sub-elements.

        Parameters
        ----------
        rho : float
            Resistivity value.
        """
        self.rho = rho
        for e in self.elements:
            e.rho = rho

    def appendElements(self):
        """
        Create elements composing the region.
        """

        if self.dim == 2:
            args = [(i, c, self.coords, self.rho, self.height2D, self.propertiesDict.copy()) for i, c in enumerate(self.connectivityElementsLocal)]
            for c in args:
                c[5]['gmshElemNbr'] = c[5]['gmshElemNbr'][c[0]]
            with mp.Pool(processes=cores_usage) as p:
                self.elements = p.starmap(LinearTriangle, args)

        if self.dim == 3:
            args = [(i, c, self.coords, self.rho, self.propertiesDict.copy()) for i, c in enumerate(self.connectivityElementsLocal)]
            for c in args:
                c[4]['gmshElemNbr'] = c[4]['gmshElemNbr'][c[0]]
            with mp.Pool(processes=cores_usage) as p:
                self.elements = p.starmap(LinearTetrahedron, args)

    def _calc_localKgeom(self):
        """
        Compute the geometric component of the local stiffness matrix
        """
        self.Kgeom = np.zeros([self.nNodes, self.nNodes])
        for e in self.elements:
            self.Kgeom[np.ix_(e.connectivity, e.connectivity)] += e.Kgeom

    def _calc_localKgeom_Sparse(self):
        """
        Compute the geometric component of the local stiffness matrix in sparse form.
        """
        # find total number of elements
        count = 0
        for e in self.elements:
            temp = scipySparse.coo_matrix(e.Kgeom)
            count += temp.nnz

        data = np.zeros(count)
        rowIdx = np.zeros(count)
        colIdx = np.zeros(count)

        position = 0
        for e in self.elements:
            temp = scipySparse.coo_matrix(e.Kgeom)
            data[position:position + temp.nnz] = temp.data
            rowIdx[position:position + temp.nnz] = e.connectivity[temp.row]
            colIdx[position:position + temp.nnz] = e.connectivity[temp.col]
            position += temp.nnz

        self.KgeomSp = scipySparse.coo_matrix((data, (rowIdx, colIdx)), shape=(self.nNodes, self.nNodes))
