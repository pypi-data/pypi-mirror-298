from scipy import linalg as scipyLinalg
import numpy as np

def localRefSystem2D(v1,  
                     v2  
                     ):
    """
    given 2 non parallel vectors in R^3, returns a orthonormal local base in R^2 of the space spanned by
    the 2 vectors. The base is defined so that v1_local is parallel to v1 and v2_local has positive second component

    Parameters
    ----------

    v1,v2 : numpy 1D array
        vectors in R^3

    Returns
    -------

    v1local,v2local : numpy 1D array
        local vectors

    """
    e1 = v1 / scipyLinalg.norm(v1)
    e2 = v2 - v2.dot(e1) * e1
    e2 = e2 / scipyLinalg.norm(e2)
    base = np.hstack((e1[:, None], e2[:, None]))
    v1local = base.T.dot(v1)
    v2local = base.T.dot(v2)
    return [v1local, v2local]


def areaTriangle(node1, node2, node3):
    """
    computes the area of a triangle, given the coordinates in R3 of its nodes
    Parameters
    ----------
        node1,2,3: numpy array in R3

    Returns
    -------
        area: float
            area of the triangle
    """
    v1 = node2 - node1
    v2 = node3 - node1
    return 0.5 * scipyLinalg.norm(np.cross(v1, v2))

def affineHyperplaneProjection(x,normal,supportPoint):
    """
    Project point x onto the hyperplane defined by its normal and support point. The hyperplane can be affine if needed.

    Parameters
    ----------
    x: point to be projected
    normal: normal vector to the plane. This vector does not neet to be unitary
    supportPoint: point that belongs to the plane

    Returns
    -------
    the projected vector
    """
    # find a base for the hyperplane: Create a matrix with the given vectors as row vectors an then compute the kernel of that matrix.
    A=np.zeros((1,3))
    A[0,:]=normal
    B=scipyLinalg.null_space(A)

    # hyperplane projection matrix (vector subspace only)
    P = B @ np.linalg.inv(B.T @ B) @ B.T

    return supportPoint + P @ (x - supportPoint)

