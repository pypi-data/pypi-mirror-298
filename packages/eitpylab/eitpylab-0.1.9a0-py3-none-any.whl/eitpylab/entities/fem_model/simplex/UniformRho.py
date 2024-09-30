import sys
import numpy as np

from scipy import linalg as scipyLinalg
from scipy import sparse as scipySparse

from eitpylab.entities.fem_model.utils import affineHyperplaneProjection, areaTriangle

class SimplexUniformRho:
    """
    A class to represent a uniform distribution over a simplex element.
    
    Attributes
    ----------
    dimensions : int
        The number of dimensions of the simplex.
    connectivity: int   
        The nodes of the element, in global terms. The local order of the nodes will be the same of connectivity input.
    coords: 2D numpy array
        Each row is composed by 3 columns, X, Y and Z of the node. This matrix should contain all nodes of the FemModel. The function will extract only the needed lines.
    rho: float
        The resistivity of the element.
    isSparse: bool
        Computes Local matrix as sparse.
    propertiesDict: dictionary
        A dictionary containing the properties of the simplex:
            'physical': physical entity group
            'region': region of the element

    """

    def __init__(self, elemNbr,  
                 dimension,  
                 connectivity,  
                 coords,  
                 rho,  
                 isSparse=False,  
                 propertiesDict=None  
                 ):
        """
        
        Parameters
        ----------
        elemNbr: int
                number of the element
        
        dimension: int {1,2,3}
                dimension of the simplex
        
        connectivity: 1D numpy array
                nodes of the element, in global terms. the local order of the nodes will be
                the same of connectivity input
                
        coords: 2D numpy array
                each row is composed by 3 columns, X, Y and Z of the node. this matrix should contain all
                nodes of the FemModel. The function will extract only the needed lines
                
        rho: float
                resistivity of the element

        isSparse: bool, optional
                computes Local matrix as sparse

        propertiesDict: dictionary, optional
                dictionary containing the properties of the simplex:
                'physical': physical entity group
                'region': region of the element
        """
        self.number = elemNbr
        self.dim = dimension
        self.type = 'simplex'.lower()
        self.nNodes = connectivity.shape[0]
        self.connectivity = connectivity.astype(int)
        self.coords = coords[connectivity, :]
        self.centroid = np.mean(self.coords, axis=0)
        self.propertiesDict = propertiesDict
        self.rho = rho
        self.Kgeom = np.array([])  
        self.isSparse = isSparse
        self.isRegion = False

    def saveKgeom(self, fileName,  # type: str
                  binary=False  # type: bool
                  ):
        """
        save geometric component of the matrix to a text file.

        Parameters
        ----------
        fileName: str
            file path
        binary: bool, optional
            save in binary format. Used only if matrix is not sparse. Default: False
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
        set the resistivity

        Parameters
        ----------
        rho: float
            resistivity value
        """
        self.rho = rho

    def calcSimplexVolume(self):
        """
        Compute the volume of the simplex. 1D: Length, 2D: area, 3D: volume
        """
        vol = -1

        if self.dim == 1:
            vol = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :])
        if self.dim == 2:
            vol = areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[2, :])
        if self.dim == 3:
            v1 = self.coords[1, :] - self.coords[0, :]
            v2 = self.coords[2, :] - self.coords[0, :]
            v3 = self.coords[3, :] - self.coords[0, :]

            vol = (1.0 / 6.0) * scipyLinalg.norm(np.dot(np.cross(v1, v2), v3))

            # V2 = np.hstack((self.coords,np.ones((4,1))))  # vol = (1.0 / 6.0) * abs(scipyLinalg.det(V2))

        if vol < 1e-12:
            print("Warning: element %d with small volume: %e (GmshElmNbr %d)" % (self.number,vol,self.propertiesDict['gmshElemNbr']))
            print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

        if vol < 0:
            print("Warning: element %d with negative volume: %e  (GmshElmNbr %d)" % (self.number,vol,self.propertiesDict['gmshElemNbr']))
            print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

        return vol

    def getBbox(self):
        """
        Retuns the boundingbox of the element

        Returns
        -------
        listLimits: list of np arrays
            list of limits in the form   [ [minX, minY, min Z] , [maxX, maxY, maxZ] ]

        """
        minimum = np.min(self.coords, axis=0)
        maximum = np.max(self.coords, axis=0)
        return [minimum, maximum]

    def getAspectRatio(self):
        """
        Retuns the aspect ratio of the simplex

        Returns
        -------
        aspect ratio: float
            value between 0.0 and 1.0
                0.0: zero-volume element
                1.0: equilateral simplex (equilateral triangle or regular tetrahedron)
        """
        if self.dim == 1:
            L = scipyLinalg.norm(self.coords[0, :] - self.coords[1, :])
            if L == 0:
                ratio = 0.0
            else:
                ratio = 1.0

        if self.dim == 2:
            a = scipyLinalg.norm(self.coords[0, :] - self.coords[1, :])
            b = scipyLinalg.norm(self.coords[0, :] - self.coords[2, :])
            c = scipyLinalg.norm(self.coords[1, :] - self.coords[2, :])
            area = areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[2, :])
            semiPerimeter = (a + b + c)/2.0

            if area == 0:
                ratio = 0.0
            else:
                if area < 1e-12:
                    print("Warning: element %d with small area: %e (GmshElmNbr %d)" % (self.number,area,self.propertiesDict['gmshElemNbr']))
                    print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

                # https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
                Circumradius = a * b * c / (4.0 * area)
                # https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-incircle
                Inradius = area / semiPerimeter

                ratio = 2.0 * Inradius / Circumradius

        if self.dim == 3:

            # Inradius:   https://en.wikipedia.org/wiki/Tetrahedron#Inradius
            # area of each face
            A1 = areaTriangle(self.coords[1, :], self.coords[2, :], self.coords[3, :])
            A2 = areaTriangle(self.coords[0, :], self.coords[2, :], self.coords[3, :])
            A3 = areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[3, :])
            A4 = areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[2, :])
            volume = self.calcSimplexVolume()

            if volume == 0:
                ratio = 0.0
            else:
                if volume < 1e-12:
                    print("Warning: element %d with small volume: %e (GmshElmNbr %d)" % (self.number,volume,self.propertiesDict['gmshElemNbr']))
                    print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

                Inradius = 3.0 * volume / (A1 + A2 + A3 + A4)

                # Circumradius    https://en.wikipedia.org/wiki/Tetrahedron#Circumradius
                # Lenghts
                a = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :])
                A = scipyLinalg.norm(self.coords[2, :] - self.coords[3, :])
                b = scipyLinalg.norm(self.coords[2, :] - self.coords[0, :])
                B = scipyLinalg.norm(self.coords[1, :] - self.coords[3, :])
                c = scipyLinalg.norm(self.coords[3, :] - self.coords[0, :])
                C = scipyLinalg.norm(self.coords[1, :] - self.coords[2, :])

                Circumradius = np.sqrt((A * a + B * b + C * c) * (-A * a + B * b + C * c) * (A * a - B * b + C * c) * (A * a + B * b - C * c)) / (
                      24 * volume)

                # http://support.moldex3d.com/r15/en/modelpreparation_reference-pre_meshqualitydefinition.html
                ratio = 3.0 * Inradius / Circumradius

        return ratio

    def isInside(self, point):
        """
        determines if a point lies inside  the simplex

        2D: based on baricentric coordinates https://people.cs.clemson.edu/~dhouse/courses/404/notes/barycentric.pdf
        3D: based on  https://github.com/ncullen93/mesh2nifti/blob/master/msh2nifti.py


        Parameters
        ----------
        point: numpy array
            coordinates of the point

        Returns
        -------
            out: boolean
                True: inside, False, outside

        """

        if self.dim ==1:
            print('isInside ERROR: this function was not implemented for 1D simplexes')
            sys.exit()

        if self.dim ==2:
            #projects the point onto the plane of the triangles and checks if it is not too far
            P0=self.coords[0]
            P1=self.coords[1]
            P2=self.coords[2]

            normal = np.cross(P1-P0,P2-P0)
            normal=normal/np.linalg.norm(normal)
            x = affineHyperplaneProjection(point,normal,self.centroid)

            #normal and area
            Vn=np.cross(P1-P0,P2-P1)
            A=scipyLinalg.norm(Vn)
            n=Vn/A

            #baricentric coords
            u=np.dot(np.cross(P2-P1,x-P1),n)/A
            v=np.dot(np.cross(P0-P2,x-P2),n)/A
            w=1-u-v
            return u>0 and v>0 and w>0


        if self.dim == 3:
            vals = np.ones((5, 4))
            vals[0, :3] = point
            vals[1:, :3] = self.coords

            idxs = [[1, 2, 3, 4], [0, 2, 3, 4], [1, 0, 3, 4], [1, 2, 0, 4], [1, 2, 3, 0]]

            dets = np.linalg.det(vals[idxs, :])
            return np.all(dets > 0) if dets[0] > 0 else np.all(dets < 0)
