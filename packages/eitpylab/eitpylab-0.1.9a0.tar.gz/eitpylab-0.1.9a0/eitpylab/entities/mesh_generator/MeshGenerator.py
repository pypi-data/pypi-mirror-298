"""
Module: MeshGenerator
---------------------

This module defines the `MeshGenerator` class, which serves as a mimic for the original gmsh.py
module, addressing memory issues. It provides functions to handle finite element mesh data.

Attributes:
    - mesh (meshio.Mesh): Mesh data loaded from a file.
    - coords (numpy.ndarray): Array of coordinates (x, y, z) of mesh nodes.

Methods:
    - open(file: str) -> None:
        Reads mesh data from the specified file and initializes mesh and coordinate attributes.

    - getNodes() -> numpy.ndarray:
        Returns a numpy array with the coordinates of mesh nodes (columns: x, y, z).

    - getPhysical_IDnumber(physicalName: str) -> int:
        Returns the ID number of a physical group given its name.

    - getPhysical_Name(physical_IDnumber: int) -> str:
        Returns the name of a physical group given its ID number.

    - getElem(dimension: int, tagNumber: int) -> Tuple[numpy.ndarray, numpy.ndarray]:
        Returns information about elements of a given dimension and tag number.

    - _getMeshElectrodes2D(electrodeTags: List[int]) -> List[List[numpy.ndarray]]:
        Returns a list of electrode boundaries, each represented as a list of node coordinates.

    - _drawElectrodesMesh2D(plotAxis, electrodeTags: List[int]) -> None:
        Draws electrodes on the specified axis in a 2D mesh plot.

    - _getMeshBoundary2D(domainTags: List[int]) -> List[List[numpy.ndarray]]:
        Returns a list of boundary edges and their coordinates for 2D mesh.

    - _plotBoundaryMesh2D(plotAxis, domainTags: List[int]) -> None:
        Plots the boundary of the domain in a 2D mesh plot.

    - plotMesh2D(domainTags: List[int], electrodeTags: Optional[List[int]] = None,
                 title: Optional[str] = None, fileName: Optional[str] = None) -> None:
        Plots the 2D mesh with specified domain and electrode tags.

    - plotdata2D(domainTags: List[int], electrodeTags: List[int], nodeData: Optional[numpy.ndarray] = None,
                 elementData: Optional[numpy.ndarray] = None, title: Optional[str] = None,
                 fileName: Optional[str] = None, nIsopotentialLines: int = 0,
                 drawStreamLines: bool = False, drawElementEdges: bool = True,
                 drawBoundaries: bool = False, drawElectrodes: bool = True) -> None:
        Plots the 2D mesh with optional node or element data, electrodes, and additional features.

"""
import sys

import matplotlib
import matplotlib.pyplot as plt
import meshio
import numpy as np
import scipy.interpolate as scipyInterp


class MeshGenerator:
    """
    class that serves as a mimic for the original gmsh.py that causes memory problems.. This class is intented to mimic a few functions from gmsh
    module that I use.

    """

    def __init__(self, path) -> None:
        self.path = path

    def open(self):
        """
        Reads mesh data from the specified path and initializes mesh and coordinate attributes.

        Args:
            path (str): Path to the mesh path.
        """

        self.mesh = meshio.read(self.path)

        """
        self.mesh.field_data   ->  Dict: {'physical Name' : [physical_Id_number , dimension (2d, 3D, etc)]}
            Contains the id numbers of the physical regions
        
        self.mesh.cells_dict  -> Dict: { elem_type_string : [numpy 2D array with the connectivity of elements of a given type ]}. 
            Gives the connectivity of of the elements of a given type. Does not have any information about neither physical 
            entities nor global element numbers.
            Ex:   'triangle' : [ [1,2,3],[5,7,12],...]
                  'tetra' : [ [1,2,3,4],[5,7,12,14],...]

        self.mesh.cells -> list of Cellblocks (named tuples). The elements of the list follow the (physical_Id_number-1) order
            each element of the list is a named tuple:  ( type=elem_type_string, data=connectivity_2D_Numpy_array)
            This element has all information about the mesh: physical_Id (position in list), type of element and connectivity
                                       
        self.mesh.cell_sets_dict -> Dict: {'physical Name' : Dict{ elem_type_string: 1Dnumpy array with [number of the elements in global terms ]}}
            Ex: 'scalp' : {'tetra',[100, 130, 440,...] }
            This element has information about the number of the element in global terms of each physical groups
        
        self.cell_sets: does not have much utility in practice
        
        self.mesh.cell_data_dict  -> Dict: { 'gmsh:physical' : { Dict: { elem_type_string : [physical_Id_number]} }}. 
            Has information about the physical Ids of each element of a given type 
                  
        self.cell_sets: does not have much utility in practice
        
        """
        # read coords
        print("set fem mesh")
        self.coords = self.mesh.points
        print("set mesh coords")

    def getNodes(self):
        """
        Returns a numpy array with the coordinates of mesh nodes (columns: x, y, z).

        Returns:
            numpy.ndarray: Array of coordinates (x, y, z) of mesh nodes.
        """
        return self.coords

    def getPhysical_IDnumber(self, physicalName):
        """
        Returns the ID number of a physical group given its name.

        Args:
            physicalName (str): Name of the physical group.

        Returns:
            int: ID number of the physical group.
        """
        try:
            Id = self.mesh.field_data[physicalName][0]
        except KeyError:
            print("ERROR: phsycal group name %s not found. Exiting..." % physicalName)
            Id = None
        return Id

    def getPhysical_Name(self, physical_IDnumber):
        """
        Returns the name of a physical group given its ID number.

        Args:
            physical_IDnumber (int): ID number of the physical group.

        Returns:
            str: Name of the physical group.
        """
        for regName, value in self.mesh.field_data.items():
            if value[0] == physical_IDnumber:
                return regName
        print("ERROR: physical ID number %d not found. Exiting..." % physical_IDnumber)
        exit(-1)

    def getElem_OLD(self, dimension, tagNumber):
        """
        Returns information about elements of a given dimension and tag number.

        Args:
            dimension (int): Dimension of the elements (1, 2, or 3).
            tagNumber (int): Tag number of the physical group.

        Returns:
            Tuple[numpy.ndarray, numpy.ndarray]: Tuple containing the element indices and their connectivities.
        """
        if dimension == 1:
            elemType = "line"
        if dimension == 2:
            elemType = "triangle"
        if dimension == 3:
            elemType = "tetra"

        physicalName = self.getPhysical_Name(tagNumber)

        connectivities = self.mesh.cells[
            tagNumber - 1
        ].data  # - 1 bc numbers start in zero

        previousElementNumber = 0
        for r in range(tagNumber - 1):
            previousElementNumber += self.mesh.cells[r].data.shape[0]

        # +1 bc we need numbers starting in one.
        elementIdx = (
            previousElementNumber
            + np.array(range(self.mesh.cells[tagNumber - 1].data.shape[0]))
            + 1
        )
        return elementIdx, connectivities

    def getElem(self, dimension, tagNumber):
        """
        Returns information about elements of a given dimension and tag number.

        Args:
            dimension (int): Dimension of the elements (1, 2, or 3).
            tagNumber (int): Tag number of the physical group.

        Returns:
            Tuple[numpy.ndarray, numpy.ndarray]: Tuple containing the element indices and their connectivities.
        """

        # numero de elementos 1D
        if "line" in self.mesh.cell_data_dict["gmsh:physical"].keys():
            nLineElem = self.mesh.cell_data_dict["gmsh:physical"]["line"].shape[0]
        else:
            nLineElem = 0

        # numero de elementos 2D
        if "triangle" in self.mesh.cell_data_dict["gmsh:physical"].keys():
            nTriElem = self.mesh.cell_data_dict["gmsh:physical"]["triangle"].shape[0]
        else:
            nTriElem = 0

        # numero de elementos 3D
        if "tetra" in self.mesh.cell_data_dict["gmsh:physical"].keys():
            nTetraElem = self.mesh.cell_data_dict["gmsh:physical"]["tetra"].shape[0]
        else:
            nTetraElem = 0

        if dimension == 1:
            previousElementNumber = 0
            elemType = "line"
        if dimension == 2:
            previousElementNumber = nLineElem
            elemType = "triangle"
        if dimension == 3:
            previousElementNumber = nLineElem + nTriElem
            elemType = "tetra"

        physicalName = self.getPhysical_Name(tagNumber)

        tetraNum = self.mesh.cell_sets_dict[physicalName][elemType]
        connectivities = self.mesh.cells_dict[elemType][tetraNum]

        # +1 bc we need numbers starting in one.
        elementIdx = previousElementNumber + tetraNum + 1
        return elementIdx, connectivities

    def _getMeshElectrodes2D(self, electrodeTags=[]):
        """
        Returns a list of electrode boundaries, each represented as a list of node coordinates.

        Args:
            electrodeTags (List[int]): List of electrode tags.

        Returns:
            List[List[numpy.ndarray]]: List of electrode boundaries.
        """
        boundaries = []
        for eTag in electrodeTags:
            _, connectivity = self.getElem(dimension=1, tagNumber=eTag)
            x = [self.coords[connectivity[0][0], 0]]
            y = [self.coords[connectivity[0][0], 1]]
            for elem in connectivity:
                x.append(self.coords[elem[1], 0])
                y.append(self.coords[elem[1], 1])
            boundaries.append([np.array(x), np.array(y)])
        return boundaries

    def _drawElectrodesMesh2D(self, plotAxis, electrodeTags=[]):
        """
        Draws electrodes on the specified axis in a 2D mesh plot.

        Args:
            plotAxis: Axis object to draw on.
            electrodeTags (List[int]): List of electrode tags.
        """
        boundaries = self._getMeshElectrodes2D(electrodeTags)

        for region in boundaries:
            x, y = region
            plotAxis.plot(x, y, color=(1.0, 0.8, 0.0), lw=3.0)

    def _getMeshBoundary2D(self, domainTags=[]):
        """
        Returns a list of boundary edges and their coordinates for 2D mesh.

        Args:
            domainTags (List[int]): List of domain tags.

        Returns:
            List[List[numpy.ndarray]]: List of boundary edges and their coordinates.
        """
        boundaries = []
        for eTag in domainTags:
            _, connectivity = self.getElem(dimension=2, tagNumber=eTag)

            x = self.coords[:, 0]
            y = self.coords[:, 1]
            triangles = matplotlib.tri.Triangulation(x, y, connectivity)

            edges = [
                [sorted([x[0], x[1]]), sorted([x[1], x[2]]), sorted([x[2], x[0]])]
                for x in triangles.triangles
            ]
            flat_list = sorted([item for sublist in edges for item in sublist])

            # find edges on the boundary. They appear only once
            boundaryEdges = []
            while len(flat_list) > 0:
                if flat_list[0] == flat_list[1]:
                    flat_list.pop(0)
                    flat_list.pop(0)
                else:
                    boundaryEdges.append(flat_list.pop(0))

            # reorder the edges to make an ordered sequence of nodes
            orderedNodes = boundaryEdges.pop(0)
            endNode = orderedNodes[-1]
            while len(boundaryEdges) > 0:
                for i, edge in enumerate(boundaryEdges):
                    if endNode == edge[0]:
                        endNode = edge[1]
                        break
                    if endNode == edge[1]:
                        endNode = edge[0]
                        break
                orderedNodes.append(endNode)
                boundaryEdges.pop(i)

            coords = self.coords[orderedNodes, :]

            boundaries.append([orderedNodes, coords])

        return boundaries

    def _plotBoundaryMesh2D(self, plotAxis, domainTags=[]):
        """
        Plots the boundary of the domain in a 2D mesh plot.

        Args:
            plotAxis: Axis object to draw on.
            domainTags (List[int]): List of domain tags.
        """
        """
        plot the boundary of the domain. ONLY FOR 2D meshes!
        """
        boundaries = self._getMeshBoundary2D(domainTags)

        for region in boundaries:
            _, coords = region
            plotAxis.plot(coords[:, 0], coords[:, 1], color="0.3", lw=1.2)

    def plotMesh2D(self, domainTags, electrodeTags=None, title=None, fileName=None):
        """
        Plots the 2D mesh with optional node or element data, electrodes, and additional features.

        Args:
            domainTags (List[int]): List of domain tags.
            electrodeTags (List[int]): List of electrode tags.
            nodeData (Optional[numpy.ndarray]): Nodal property data. Defaults to None.
            elementData (Optional[numpy.ndarray]): Element property data. Defaults to None.
            title (Optional[str]): Title of the plot. Defaults to None.
            fileName (Optional[str]): Name of the file to save the plot. Defaults to None.
            nIsopotentialLines (int): Number of isopotential lines. Defaults to 0.
            drawStreamLines (bool): Whether to draw streamlines. Defaults to False.
            drawElementEdges (bool): Whether to draw element edges. Defaults to True.
            drawBoundaries (bool): Whether to draw boundaries. Defaults to False.
            drawElectrodes (bool): Whether to draw electrodes. Defaults to True.
        """
        x = self.coords[:, 0]
        y = self.coords[:, 1]
        triangles = matplotlib.tri.Triangulation(x, y, self.mesh.cells_dict["triangle"])

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        ax.set_axis_off()

        self._plotBoundaryMesh2D(ax, domainTags)
        ax.triplot(triangles, "k-", lw=0.5)

        if electrodeTags is not None:
            self._drawElectrodesMesh2D(ax, electrodeTags)

        if title is not None:
            ax.set_title(title)

        if fileName is None:
            plt.show()
        else:
            plt.savefig(fileName, bbox_inches="tight")
        plt.close(fig)

    def plotdata2D(
        self,
        domainTags,
        electrodeTags,
        nodeData=None,
        elementData=None,
        title=None,
        fileName=None,
        nIsopotentialLines=0,
        drawStreamLines=False,
        drawElementEdges=True,
        drawBoundaries=False,
        drawElectrodes=True,
    ):
        """
        Plots the 2D mesh with optional node or element data, electrodes, and additional features.

        Args:
            domainTags (List[int]): List of domain tags.
            electrodeTags (List[int]): List of electrode tags.
            nodeData (Optional[numpy.ndarray]): Nodal property data. Defaults to None.
            elementData (Optional[numpy.ndarray]): Element property data. Defaults to None.
            title (Optional[str]): Title of the plot. Defaults to None.
            fileName (Optional[str]): Name of the file to save the plot. Defaults to None.
            nIsopotentialLines (int): Number of isopotential lines. Defaults to 0.
            drawStreamLines (bool): Whether to draw streamlines. Defaults to False.
            drawElementEdges (bool): Whether to draw element edges. Defaults to True.
            drawBoundaries (bool): Whether to draw boundaries. Defaults to False.
            drawElectrodes (bool): Whether to draw electrodes. Defaults to True.
        """
        x = self.coords[:, 0]
        y = self.coords[:, 1]
        triangles = matplotlib.tri.Triangulation(x, y, self.mesh.cells_dict["triangle"])

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        ax.set_axis_off()

        # plot element edges

        if drawBoundaries:
            self._plotBoundaryMesh2D(ax, domainTags)

        if drawElementEdges:
            ax.triplot(triangles, "k-", lw=0.5, color="white")

        if drawElectrodes:
            self._drawElectrodesMesh2D(ax, electrodeTags)

        if nodeData is None:
            # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tripcolor.html#matplotlib.axes.Axes.tripcolor
            tpc = ax.tripcolor(
                triangles, shading="flat", cmap="Spectral_r", facecolors=elementData
            )
            # ax.tricontourf(tri, nodeData, levels=levels, cmap=cmap)
            fig.colorbar(tpc, orientation="horizontal")

        if nodeData is not None:
            # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tripcolor.html#matplotlib.axes.Axes.tripcolor
            tpc = ax.tripcolor(
                triangles, nodeData, shading="gouraud", cmap="Spectral_r"
            )
            fig.colorbar(tpc, orientation="horizontal")

            if nIsopotentialLines > 0:
                # refines the solution for a better interpolation
                # https://matplotlib.org/gallery/images_contours_and_fields/tricontour_smooth_user.html#sphx-glr-gallery-images-contours-and-fields-tricontour-smooth-user-py
                ax.tricontour(
                    triangles,
                    nodeData,
                    levels=nIsopotentialLines,
                    colors="0.35",
                    linewidths=[0.5, 0.5, 0.5, 0.5, 0.5],
                )

            if drawStreamLines:
                # interpolates nodal voltages to a grid
                SizeX = max(x) - min(x)
                SizeY = max(y) - min(y)
                maxSize = max(SizeX, SizeY)
                Npoints = 40
                x_samples = np.linspace(min(x), max(x), int(Npoints * SizeX / maxSize))
                y_samples = np.linspace(min(y), max(y), int(Npoints * SizeY / maxSize))

                deltaX = x_samples[1] - x_samples[0]
                deltaY = y_samples[1] - y_samples[0]
                grid_x, grid_y = np.meshgrid(x_samples, y_samples)
                nodeData_grid = scipyInterp.griddata(
                    self.coords[:, 0:2],
                    nodeData,
                    (grid_x, grid_y),
                    method="linear",
                    fill_value=np.nan,
                )

                # compute J  = -(1/rho) grad (v)
                [dvdx, dvdy] = np.gradient(-nodeData_grid, deltaX, deltaY)
                magnitude = np.sqrt(dvdx**2 + dvdy**2)

                # interpolates rho to compute current density
                trifinder = triangles.get_trifinder()
                triangleNumber = trifinder(grid_x, grid_y)
                rho = elementData[triangleNumber]

                jx = np.divide(dvdx, rho)
                jy = np.divide(dvdy, rho)

                # seed points for the streamplot
                electrodeNodes = self._getMeshElectrodes2D(electrodeTags)[0]
                nPoints = electrodeNodes[0].shape[0]
                nLines = 20
                seedX = np.interp(
                    np.linspace(0, nPoints, nLines), range(nPoints), electrodeNodes[0]
                )
                seedY = np.interp(
                    np.linspace(0, nPoints, nLines), range(nPoints), electrodeNodes[1]
                )

                seedPoints = np.column_stack((seedX, seedY))
                quiverPlot = False
                streamPlot = True
                if streamPlot:
                    ax.streamplot(
                        x_samples,
                        y_samples,
                        jy / np.max(magnitude),
                        jx / np.max(magnitude),
                        density=2 * nLines,
                        start_points=seedPoints,
                        arrowsize=0.5,
                        color=(0.0, 0.0, 0.0),
                        linewidth=0.5,
                        maxlength=10,
                    )

                if quiverPlot:
                    ax.quiver(
                        x_samples,
                        y_samples,
                        jy / np.max(magnitude),
                        jx / np.max(magnitude),
                        magnitude,
                        units="xy",
                        scale=10,
                    )

        if title is not None:
            ax.set_title(title)

        if fileName is not None:
            plt.savefig(fileName, bbox_inches="tight", dpi=300)
            plt.close(fig)
        else:
            plt.show()
