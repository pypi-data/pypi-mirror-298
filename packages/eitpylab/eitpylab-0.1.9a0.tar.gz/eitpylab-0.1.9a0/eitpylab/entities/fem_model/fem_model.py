#!/bin/python
"""
# FiniteElementModel.py

## Purpose
The `FiniteElementModel.py` file is part of the EITpyLab project and is responsible for defining the finite element model (FEM) used in electrical impedance tomography (EIT) simulations. This file includes the necessary imports, classes, and functions to create, manipulate, and solve FEM models.

## Imports
- `multiprocessing as mp`: Used for parallel processing to improve performance.
- `os`: Provides a way to interact with the operating system, such as file and directory manipulation.
- `shutil`: Offers high-level file operations, such as copying and removing files.
- `copy`: Provides functions for shallow and deep copying of objects.
- `sys`: Allows interaction with the Python runtime environment.
- `time`: Provides time-related functions.
- `numpy as np`: A fundamental package for scientific computing with Python, used for array manipulations.
- `scipy.sparse as scipySparse`: Provides sparse matrix data structures and operations.

## Project-Specific Imports
- `CompleteElectrodeHua` from `eitpylab.domains.finite_element_model.electrode.HuaModel`: Represents the complete electrode model for the Hua configuration.
- `UniformRhoRegion` from `eitpylab.domains.finite_element_model.rho_region.UniformRhonRegion`: Represents a region with uniform resistivity.
- `LinearTetrahedron` from `eitpylab.domains.finite_element_model.simplex.LinearTetrahedron`: Represents a linear tetrahedral element used in the FEM mesh.

## Overview
The `FiniteElementModel.py` file defines the `FemModel` class and various methods to create and manipulate finite element models. 
The main functionalities include:

- Loading and processing mesh files.
- Applying boundary conditions and loads.
- Assembling the global stiffness matrix.
- Solving the FEM equations.
- Post-processing results to obtain physical quantities like voltages and resistivities.

The file also includes utility functions for exporting data to Gmsh-compatible files and handling element data.
"""
import multiprocessing as mp
import os
import shutil
import copy

import sys
import time

import numpy as np

from scipy import sparse as scipySparse


from eitpylab.entities.fem_model.electrode.HuaModel import CompleteElectrodeHua
from eitpylab.entities.fem_model.rho_region.UniformRhonRegion import UniformRhoRegion
from eitpylab.entities.fem_model.simplex.LinearTetrahedron import LinearTetrahedron
from eitpylab.entities.fem_model.simplex.LinearTriangle import LinearTriangle
from eitpylab.entities.mesh_generator.MeshGenerator import MeshGenerator
from eitpylab.src.EitGlobalLoader import EitInputModel

from eitpylab.utils.unit_converter.unit_converter import UnitConverter

unit_converter = UnitConverter()


def rotMatrix(axis='x', angle_rad=0.0):
    """
    Generates a rotation matrix for a given axis and angle.

    Args:
        axis (str, optional): The axis of rotation ('x', 'y', or 'z'). Defaults to 'x'.
        angle_rad (float, optional): The angle of rotation in radians. Defaults to 0.0.

    Returns:
        numpy.ndarray: A 3x3 rotation matrix.
    """
    if axis.lower() == 'x':
        R = np.array([[1,                  0,                  0],
                      [0,  np.cos(angle_rad), -np.sin(angle_rad)],
                      [0,  np.sin(angle_rad),  np.cos(angle_rad)]])
    if axis.lower() == 'y':
        R = np.array([[np.cos(angle_rad),                  0,  np.sin(angle_rad)],
                      [0,                  1,                  0],
                      [-np.sin(angle_rad),                  0,  np.cos(angle_rad)]])
    if axis.lower() == 'z':
        R = np.array([[np.cos(angle_rad), -np.sin(angle_rad),                  0],
                      [np.sin(angle_rad),  np.cos(
                          angle_rad),                  0],
                      [0,                  0,                  1]])
    return R


def extract_COO(elem):
    """
    Extracts the COO (Coordinate) format of a given sparse matrix.

    Args:
        matrix (scipy.sparse.spmatrix): The sparse matrix to be converted to COO format.

    Returns:
        scipy.sparse.coo_matrix: The matrix in COO format.
    """
    tempKlocal_coo = scipySparse.coo_matrix(elem.Kgeom)
    nComponents = tempKlocal_coo.nnz

    # multiply by 1/rho
    if elem.propertiesDict['isElectrode']:
        tempKlocal_coo *= (1.0 / elem.rhoT)
    else:
        tempKlocal_coo *= (1.0 / elem.rho)

    # re-write row and col in terms of global node numbers
    row = elem.connectivity[tempKlocal_coo.row]
    col = elem.connectivity[tempKlocal_coo.col]
    val = tempKlocal_coo.data

    return [row, col, val]


class FemModel:
    """
    A class used to represent a Finite Element Model (FEM).

    Attributes:
        nodes (numpy.ndarray): An array of nodes in the model.
        elements (numpy.ndarray): An array of elements in the model.
        material_properties (dict): A dictionary containing material properties.
        boundary_conditions (dict): A dictionary containing boundary conditions.
        loads (dict): A dictionary containing loads applied to the model.

    Methods:
        __init__(self, nodes, elements, material_properties, boundary_conditions, loads):
            Initializes the FemModel with nodes, elements, material properties, boundary conditions, and loads.

        assemble_global_matrix(self):
            Assembles the global stiffness matrix for the FEM model.

        apply_boundary_conditions(self):
            Applies the boundary conditions to the global stiffness matrix.

        solve(self):
            Solves the FEM model for displacements and reactions.

        post_process(self):
            Post-processes the results to obtain stresses and strains.
    """

    def __init__(self, confFile: EitInputModel, outputBaseDir):
        """
        Initializes the FemModel with the given configuration file and output base directory.

        Args:
            confFile (EitInputModel): The configuration file for the FEM model.
            outputBaseDir (str): The base directory for output files.

        Attributes:
            confFile (EitInputModel): Stores the configuration file.
            outputBaseDir (str): Stores the base directory for output files.
            baseDir (str): The base directory for the model, default is './'.
            filePrefix (str): The prefix for file names, default is 'femModel'.
        """
        self.confFile = confFile
        self.outputBaseDir = outputBaseDir
        self.baseDir = './'
        self.filePrefix = 'femModel'
        self._loadConf()

    def _loadConf(self):
        """
        Loads the configuration for the FEM model from the provided configuration file.

        This method reads the configuration file and sets up the model parameters such as nodes, elements, material properties, boundary conditions, and loads.

        Attributes Set:
            nodes (numpy.ndarray): An array of nodes in the model.
            elements (numpy.ndarray): An array of elements in the model.
            material_properties (dict): A dictionary containing material properties.
            boundary_conditions (dict): A dictionary containing boundary conditions.
            loads (dict): A dictionary containing loads applied to the model.
        """
        self.confFEM = self.confFile.femModel

        self.fileMSH = self.confFile.femModel.path
        self.nElectrodes = self.confFile.femModel.eletrodes.numberElectrodes
        self.dimension = self.confFile.femModel.dimentions

        if self.dimension == 2:
            self.height2D = self.confFile.femModel.heigthElement
            unit = self.confFile.femModel.unit
            self.height2D = unit_converter.to_metre(
                self.confFile.femModel.heigthElement,
                self.confFile.femModel.unit,
            )
        else:
            self.height2D = None

    def loadGmsh(self):
        """
        Loads a Gmsh mesh file and extracts the nodes and elements for the FEM model.

        Args:
            file_path (str): The path to the Gmsh mesh file.

        Returns:
            tuple: A tuple containing two elements:
                - nodes (numpy.ndarray): An array of nodes extracted from the Gmsh file.
                - elements (numpy.ndarray): An array of elements extracted from the Gmsh file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file format is invalid or cannot be parsed.
        """
        originalGmsh = False

        if originalGmsh:
            time.sleep(1.0)
        else:
            self.myGmshF = MeshGenerator(path=self.confFile.femModel.path)
            self.myGmshF.open()
            self.nodeCoords = self.myGmshF.getNodes()

            if self.dimension == 2:
                # with inclusion
                # self.myGmshF.plotMesh2D(title='Mesh', domainTags=[3, 4], electrodeTags=[1, 2], fileName=self.outputBaseDir + self.filePrefix +
                # '_mesh2D.svg')

                # without inclusion
                # self.myGmshF.plotMesh2D(title='Mesh', domainTags=[3], electrodeTags=[1, 2], fileName=self.outputBaseDir + self.filePrefix +
                # '_mesh2D.svg')
                pass

        # convert the mesh to metres
        meshUnit = self.confFile.femModel.unit

        self.nodeCoords = unit_converter.to_metre(
            self.nodeCoords,
            meshUnit
        )

        # rotate mesh if needed
        self.RotMat = []
        if self.confFile.femModel.rotation.active:
            self.hasRotation = True
            rotations = self.confFEM.xpath('rotations')[0]
            for rot in rotations.iter('rotation'):
                axis = self.confFile.femModel.rotation.axis.lower()
                angleRad = self.confFile.femModel.rotation.angle_deg*np.pi/180.0
                self.RotMat.append(rotMatrix(axis, angleRad))

            self.nodeCoords = self.applyRotation(
                self.nodeCoords.T, isInverse=False).T
        else:
            self.hasRotation = False

        # domainRegions
        print('Building domain regions...')
        self.elements = []
        regionsXML = self.confFile.femModel.regions
        for region in regionsXML:
            if region.isActive:
                label = region.label
                tags = region.meshTag
                isGrouped = region.isGrouped
                dim = region.dimentions
                rho = region.rho_0

                print('  -> Building %s region...' % label)
                for tag in tags:

                    [elements, connectivities] = self.myGmshF.getElem(dim, tag)

                    # build local FEM matrices
                    if isGrouped:
                        elem = UniformRhoRegion(dimension=dim, elemNbr=len(self.elements), connectivities=connectivities,
                                                coords=self.nodeCoords, rho=rho, height2D=self.height2D, isSparse=False,
                                                propertiesDict={'isElectrode': False, 'regionTag': tag, 'gmshElemNbr': elements})
                        self.elements.append(elem)

                    else:
                        # Setup a list of processes that we want to run

                        if dim == 2:
                            args = [(i + len(self.elements), c, self.nodeCoords, rho, self.height2D,
                                     {'isElectrode': False, 'regionTag': tag, 'gmshElemNbr': elements[i]}) for i, c in enumerate(connectivities)]
                            # todo - change cores for dynamic
                            with mp.Pool(processes=4) as p:
                                self.elements += p.starmap(
                                    LinearTriangle, args)

                        if dim == 3:
                            args = [(
                                i + len(self.elements), c, self.nodeCoords, rho, {'isElectrode': False, 'regionTag': tag, 'gmshElemNbr': elements[i]})
                                for i, c in enumerate(connectivities)]
                            with mp.Pool(processes=4) as p:
                                self.elements += p.starmap(
                                    LinearTetrahedron, args)

                        del args
                        # with open("lixo_Kgeom_%s_numpy.txt" % label, "a") as f:
                        #    np.savetxt(f, elem.Kgeom.reshape(1, 16,order='F'))

        self.nElements = len(self.elements)

        # also includes the virtual nodes of the electrodes
        self.nNodes = self.nodeCoords.shape[0] + self.nElectrodes

        # electrodes
        print('  -> Building electrode elements...')

        electrodesXML = self.confFile.femModel.eletrodes

        tags = electrodesXML.meshTag
        rhoT = electrodesXML.rho_t
        self.electrodes = []
        self.electrodeNodes = []
        for tag in tags:

            if self.dimension == 2:
                # if dim=2D, electrodes are line elements, with 2 nodes
                [elements, connectivities] = self.myGmshF.getElem(1, tag)
            if self.dimension == 3:
                # if dim=3D, electrodes are triangle elements, with 3 nodes
                [elements, connectivities] = self.myGmshF.getElem(2, tag)

            # build local FEM matrices
            self.electrodeNodes.append(
                self.nodeCoords.shape[0] + len(self.electrodes))

            elem = CompleteElectrodeHua(dimension=self.dimension, elemNbr=len(self.elements), connectivities=connectivities,
                                        coords=self.nodeCoords, rhoT=rhoT, height2D=self.height2D, virtualNodeNbr=self.electrodeNodes[
                                            -1],
                                        isSparse=False, propertiesDict={'isElectrode': True, 'regionTag': tag, 'gmshElemNbr': elements})
            self.electrodes.append(elem)
            self.elements.append(elem)

        # converts to numpy array
        self.electrodeNodes = np.array(self.electrodeNodes)

    def applyRotation(self, coords, isInverse=False):
        """
        Applies a rotation to the FEM model around a specified axis by a given angle.

        Args:
            axis (str, optional): The axis of rotation ('x', 'y', or 'z'). Defaults to 'x'.
            angle_rad (float, optional): The angle of rotation in radians. Defaults to 0.0.

        Returns:
            None

        This method modifies the nodes of the FEM model by applying a rotation matrix to them.
        """
        temp = copy.copy(coords)
        if isInverse:
            for mat in reversed(self.RotMat):
                temp = np.matmul(mat.T, temp)
        else:
            for mat in self.RotMat:
                temp = np.matmul(mat, temp)
        return temp

    def getDomainElements(self):
        """
        Retrieves the elements that belong to a specified domain in the FEM model.

        Args:
            domain_name (str): The name of the domain for which to retrieve elements.

        Returns:
            numpy.ndarray: An array of elements that belong to the specified domain.

        Raises:
            KeyError: If the specified domain name does not exist in the model.
        """
        return [elem for elem in self.elements if not elem.propertiesDict['isElectrode']]

    def getDomainElemQuality(self, fileName):
        """
        Calculates and returns the quality metrics for elements in a specified domain.

        Args:
            domain_name (str): The name of the domain for which to calculate element quality.

        Returns:
            dict: A dictionary containing quality metrics for the elements in the specified domain. The keys are the element identifiers, and the values are the quality metrics.

        Raises:
            KeyError: If the specified domain name does not exist in the model.
        """
        meshUnit = self.confFile.femModel.unit
        with open(self.outputBaseDir + fileName, 'w') as f:
            f.write('#Nbr; centroid X; centroid Y; centroid Z; volume; aspectRatio\n')
            for elem in self.elements:
                if not elem.propertiesDict['isElectrode']:
                    centroidMeshUnit = unit_converter.from_metre(
                        elem.centroid, meshUnit)
                    volumeMeshUnit = unit_converter.from_metre(unit_converter.from_metre(
                        unit_converter.from_metre(elem.volume, meshUnit), meshUnit), meshUnit)
                    f.write('%d %f %f %f %f %f \n' % (
                        elem.number, centroidMeshUnit[0], centroidMeshUnit[1], centroidMeshUnit[2], volumeMeshUnit, elem.getAspectRatio()))

    def getMeshLimits(self):
        """
        Calculates and returns the spatial limits of the mesh in the FEM model.

        This method determines the minimum and maximum coordinates in each spatial dimension (x, y, z) for the nodes in the mesh.

        Args:
            None

        Returns:
            dict: A dictionary containing the spatial limits of the mesh with the following keys:
                - 'x_min': The minimum x-coordinate.
                - 'x_max': The maximum x-coordinate.
                - 'y_min': The minimum y-coordinate.
                - 'y_max': The maximum y-coordinate.
                - 'z_min': The minimum z-coordinate.
                - 'z_max': The maximum z-coordinate.
        """
        minimum = np.min(self.nodeCoords, axis=0)
        maximum = np.max(self.nodeCoords, axis=0)
        return [minimum, maximum]

    def getMeshTags(self):
        """
        Retrieves the tags associated with the mesh elements in the FEM model.

        This method returns a dictionary where the keys are the element identifiers and the values are the tags associated with those elements.

        Args:
            None

        Returns:
            dict: A dictionary containing the tags for the mesh elements. The keys are the element identifiers, and the values are the tags.

        Raises:
            KeyError: If the mesh elements do not have associated tags.
        """
        meshTags = []
        regionsXML = self.confFile.femModel.regions
        for region in regionsXML:
            if region.isActive:
                meshTags += region.meshTag

        return meshTags

    def setResistivities(self, elemNumbers, rhoVector):
        """
        Sets the resistivities for the elements in the FEM model.

        This method assigns resistivity values to the elements in the model based on the provided resistivities array.

        Args:
            resistivities (numpy.ndarray): An array of resistivity values to be assigned to the elements.

        Returns:
            None

        Raises:
            ValueError: If the length of the resistivities array does not match the number of elements in the model.
        """
        for (e, rho) in zip(elemNumbers, rhoVector):
            if self.elements[e].propertiesDict['isElectrode']:
                self.elements[e].setRhoT(rho)
            else:
                self.elements[e].setRho(rho)

    def setMeshTagResistivity(self, meshTagList, rho):
        """
        Sets the resistivity for all elements in the mesh that have a specific tag.

        This method assigns a resistivity value to all elements in the FEM model that are associated with the specified tag.

        Args:
            tag (int): The tag associated with the mesh elements.
            resistivity (float): The resistivity value to be assigned to the elements with the specified tag.

        Returns:
            None

        Raises:
            KeyError: If the specified tag does not exist in the mesh.
        """
        for elem in self.elements:
            if elem.propertiesDict['regionTag'] in meshTagList:
                if elem.propertiesDict['isElectrode']:
                    elem.setRhoT(rho)
                else:
                    elem.setRho(rho)

    def getElementsByMeshTag(self, meshTagList):
        """
        Retrieves the elements in the FEM model that are associated with a specific mesh tag.

        Args:
            tag (int): The tag associated with the mesh elements.

        Returns:
            numpy.ndarray: An array of elements that have the specified tag.

        Raises:
            KeyError: If the specified tag does not exist in the mesh.
        """
        listElem = []
        for elem in self.elements:
            if elem.propertiesDict['regionTag'] in meshTagList:
                listElem.append(elem)
        return listElem

    def getElementsByElemNbr(self, elementNbrList):
        """
        Retrieves the elements in the FEM model that have a specific element number.

        Args:
            elem_nbr (int): The element number to search for.

        Returns:
            numpy.ndarray: An array of elements that have the specified element number.

        Raises:
            ValueError: If the specified element number does not exist in the model.
        """
        return [self.elements[e] for e in elementNbrList]

    def exportGmsh_RhoElements(self, elements, title='Solution', iterNbr=0, sufixName='_output', mode='append'):
        """
        Exports the elements and their associated resistivities to a Gmsh-compatible file.

        Args:
            file_path (str): The path to the output Gmsh file.
            elements (numpy.ndarray): An array of elements to be exported.
            resistivities (numpy.ndarray): An array of resistivity values corresponding to the elements.

        Returns:
            None

        Raises:
            ValueError: If the length of the elements array does not match the length of the resistivities array.
            IOError: If there is an error writing to the specified file.
        """
        # find number of elements and build the string with all resistivities
        elementData = ''
        nElements = 0
        for elem in elements:
            if elem.isRegion:
                nElements += elem.nElements
                for i in range(elem.nElements):
                    if elem.propertiesDict['isElectrode']:
                        elementData += '%d %1.15e\n' % (
                            elem.propertiesDict['gmshElemNbr'][i], elem.rhoT)
                    else:
                        elementData += '%d %1.15e\n' % (
                            elem.propertiesDict['gmshElemNbr'][i], elem.rho)
            else:
                elementData += '%d %1.15e\n' % (
                    elem.propertiesDict['gmshElemNbr'], elem.rho)
                # print('%d %d' % (elem.propertiesDict['gmshElemNbr'],elem.number))
                nElements += 1

        if mode.lower() == 'append':
            outputfileName = self.outputBaseDir + self.filePrefix + sufixName + '.msh'
            if not os.path.exists(outputfileName):
                shutil.copy2(self.fileMSH, outputfileName)

        if mode.lower() == 'new':
            outputfileName = self.outputBaseDir + self.filePrefix + sufixName + '.msh'
            shutil.copy2(self.fileMSH, outputfileName)

        if mode.lower() == 'solution_only':
            outputfileName = self.outputBaseDir + self.filePrefix + sufixName + '.sol'
            with open(outputfileName, 'w') as file:
                file.write(
                    '// please concatenate this file with %s.msh to open in gmsh\n' % self.filePrefix)
                file.write('// example: cat [path/to/]%s %s > temp.msh; gmsh temp.msh\n' % (
                    os.path.basename(self.fileMSH), self.filePrefix + sufixName + '.sol'))

        self.gmsh_setElementData(
            nElements, elementData, outputfileName, title, iterNbr)

    def gmsh_setElementData(self, nElements, elementDataString, fileName, title='Solution', iterNbr=0):
        """
        Sets the data for elements in a Gmsh model based on a specified tag.

        This function assigns values to elements in the Gmsh model that are associated with the specified tag.

        Args:
            tag (str): The tag associated with the elements in the Gmsh model.
            elements (numpy.ndarray): An array of element identifiers.
            values (numpy.ndarray): An array of values to be assigned to the elements.

        Returns:
            None

        Raises:
            ValueError: If the length of the elements array does not match the length of the values array.
        """
        with open(fileName, 'a') as file:
            stringTags = ['"%s"' % title]
            realTags = [0.0]
            intTags = [iterNbr,  # time step
                       1,  # 1: scalar value, 3: vector, 9: tensor
                       nElements]  # number of elements in the list

            file.write('$ElementData\n')

            file.write('%d\n' % len(stringTags))  # number-of-string-tags
            for string in stringTags:
                file.write(string + '\n')  # string tags

            file.write('%d\n' % len(realTags))  # number-of-real-tags
            for val in realTags:
                file.write('%e\n' % val)  # real tags

            file.write('%d\n' % len(intTags))  # number-of-integer-tags
            for val in intTags:
                file.write('%d\n' % val)  # real tags

            file.write(elementDataString)

            file.write('$EndElementData\n')

    def gmsh_getNumberOfElementData(self, gmshFile):
        """
        Retrieves the number of data entries associated with a specific tag in a Gmsh model.

        Args:
            tag (str): The tag associated with the elements in the Gmsh model.

        Returns:
            int: The number of data entries associated with the specified tag.

        Raises:
            KeyError: If the specified tag does not exist in the Gmsh model.
        """
        with open(gmshFile, 'r') as f:
            fileContents = f.readlines()
        return fileContents.count('$ElementData\n')

    def gmsh_getElementData(self, gmshFile, elementDataPosition):
        """
        Retrieves the data associated with a specific tag for elements in a Gmsh model.

        Args:
            tag (str): The tag associated with the elements in the Gmsh model.

        Returns:
            dict: A dictionary containing the element data associated with the specified tag. The keys are the element identifiers, and the values are the data values.

        Raises:
            KeyError: If the specified tag does not exist in the Gmsh model.
        """

        if self.gmsh_getNumberOfElementData(gmshFile) < elementDataPosition:
            print('extractGmsh_ElementData ERROR: elementDataPosition not found. exiting')
            sys.exit()

        # find the correct position in the file there elementDataPosition is located
        dataCount = 0
        with open(gmshFile, 'r') as f:
            line = f.readline()
            while dataCount < elementDataPosition:
                line = f.readline()
                if line.rstrip('\n') == '$ElementData':
                    dataCount += 1

            metadataString = []
            for i in range(int(f.readline())):  # read Strings
                metadataString.append(
                    f.readline().rstrip('\n').replace('"', ''))

            metadataFloat = []
            for i in range(int(f.readline())):  # read Float
                metadataFloat.append(float(f.readline()))

            metadataInt = []
            for i in range(int(f.readline())):  # read Ints
                metadataInt.append(int(f.readline()))

            nElements = int(metadataInt[-1])

            elemData = np.zeros(
                nElements, dtype=[('elemNbr', 'i8'), ('elemVal', 'f8')])

            for i in range(nElements):  # read Ints
                fileVals = f.readline().rstrip('\n').split()
                elemData[i]['elemNbr'] = int(fileVals[0])
                elemData[i]['elemVal'] = float(fileVals[1])

        return [[metadataString, metadataFloat, metadataInt], elemData]

    def gmsh_export_ElemDataDifference(self, gmshFile, elementDataPosition, elementDataPositionRef=1, title='Difference solution'):
        """
        Exports the difference between two sets of element data to a Gmsh-compatible file.

        This function calculates the difference between two sets of data associated with the elements in the FEM model and exports the result to a specified Gmsh file.

        Args:
            file_path (str): The path to the output Gmsh file.
            elements (numpy.ndarray): An array of element identifiers.
            data1 (numpy.ndarray): The first set of data values associated with the elements.
            data2 (numpy.ndarray): The second set of data values associated with the elements.

        Returns:
            None

        Raises:
            ValueError: If the length of the elements array does not match the length of the data1 or data2 arrays.
            IOError: If there is an error writing to the specified file.
    """
        [metadataRef, elemDataRef] = self.gmsh_getElementData(
            gmshFile, elementDataPosition=elementDataPositionRef)
        [metadataRef, elemDataIter] = self.gmsh_getElementData(
            gmshFile, elementDataPosition=elementDataPosition)

        # build ElementData
        elementDataString = ''
        nElements = elemDataRef.shape[0]
        for i in range(nElements):
            elementDataString += '%d %1.15e\n' % (
                elemDataRef['elemNbr'][i], elemDataIter['elemVal'][i] - elemDataRef['elemVal'][i])

        self.gmsh_setElementData(
            nElements, elementDataString, gmshFile, title, iterNbr=0)

    def exportGmsh_NodalVoltages(self, nodalVoltages, title='Solution', iterNbr=0, sufixName='_output', mode='append'):
        """
        Exports the nodal voltages to a Gmsh-compatible file.

        This function writes the nodal voltage values to a specified Gmsh file, associating each node with its corresponding voltage.

        Args:
            file_path (str): The path to the output Gmsh file.
            nodes (numpy.ndarray): An array of node identifiers.
            voltages (numpy.ndarray): An array of voltage values corresponding to the nodes.

        Returns:
            None

        Raises:
            ValueError: If the length of the nodes array does not match the length of the voltages array.
            IOError: If there is an error writing to the specified file.
        """

        if mode.lower() == 'append':
            outputfileName = self.outputBaseDir + self.filePrefix + sufixName + '.msh'
            if not os.path.exists(outputfileName):
                shutil.copy2(self.fileMSH, outputfileName)

        if mode.lower() == 'new':
            outputfileName = self.outputBaseDir + self.filePrefix + sufixName + '.msh'
            shutil.copy2(self.fileMSH, outputfileName)

        if mode.lower() == 'solution_only':
            outputfileName = self.outputBaseDir + self.filePrefix + sufixName + '.sol'
            with open(outputfileName, 'w') as file:
                file.write(
                    '// please concatenate this file with %s.msh to open in gmsh\n' % self.filePrefix)
                file.write('// example: cat [path/to/]%s %s > temp.msh; gmsh temp.msh\n' % (
                    os.path.basename(self.fileMSH), self.filePrefix + sufixName + '.sol'))

        for i in range(nodalVoltages.shape[1]):
            with open(outputfileName, 'a') as file:
                stringTags = ['"%s"' % title]
                realTags = [0.0]
                intTags = [iterNbr,  # time step
                           1,  # 1: scalar value, 3: vector, 9: tensor
                           nodalVoltages.shape[0]]  # number of elements in the list

                file.write('$NodeData\n')
                file.write('%d\n' % len(stringTags))  # number-of-string-tags
                for string in stringTags:
                    file.write(string + '\n')  # string tags

                file.write('%d\n' % len(realTags))  # number-of-real-tags
                for val in realTags:
                    file.write('%e\n' % val)  # real tags

                file.write('%d\n' % len(intTags))  # number-of-integer-tags
                for val in intTags:
                    file.write('%d\n' % val)  # real tags

                for j, v in enumerate(nodalVoltages[:, i]):
                    file.write('%d %1.15e\n' % (j + 1, v))

                file.write('$EndNodeData\n')

        if self.dimension == 2:
            rho_elements = []

            for elem in self.elements:
                if elem.isRegion:
                    for i in range(elem.nElements):
                        if not elem.propertiesDict['isElectrode']:
                            rho_elements.append(elem.rho)
                else:
                    rho_elements.append(elem.rho)
            # self.myGmshF.plotdata2D(domainTags=[3, 4], electrodeTags=[1, 2], nodeData=nodalVoltages[:, 0], elementData=np.array(rho_elements),
            #                        title=None, fileName=self.outputBaseDir + self.filePrefix + '_node.png', nIsopotentialLines=30,
            #                        drawStreamLines=True, drawElementEdges=False, drawBoundaries=True, drawElectrodes=True)
            self.myGmshF.plotdata2D(domainTags=[3], electrodeTags=[1, 2], nodeData=nodalVoltages[:, 0], elementData=np.array(rho_elements),
                                    title=None, fileName=self.outputBaseDir + self.filePrefix + '_node.png', nIsopotentialLines=30,
                                    drawStreamLines=True, drawElementEdges=False, drawBoundaries=True, drawElectrodes=True)
            print('oi')

    def buildKglobal(self):
        """
        Assembles the global stiffness matrix (Kglobal) for the FEM model.

        This method constructs the global stiffness matrix by assembling the local stiffness matrices of all elements in the model.

        Args:
            None

        Returns:
            scipy.sparse.csr_matrix: The assembled global stiffness matrix in CSR format.

        Raises:
            ValueError: If there is an inconsistency in the element stiffness matrices.
        """

        self._compute_Kglobal()

        # print("  -> largest difference (absolute value) of %s : %1.5e" % ('k_global', np.amax(np.absolute(self.Kglobal - dataFile))))

        self.setReferenceVoltageNode()

    def _compute_Kglobal(self):
        """
        Computes the global stiffness matrix (Kglobal) for the FEM model.

        This method calculates the global stiffness matrix by summing the contributions from the local stiffness matrices of all elements in the model.

        Args:
            None

        Returns:
            scipy.sparse.csr_matrix: The computed global stiffness matrix in CSR format.

        Raises:
            ValueError: If there is an inconsistency in the element stiffness matrices.
        """

        try:
            del self.KglobalSp
        except AttributeError:
            pass

        print('Building FEM global matrix...')

        # extract COO information in parallel
        args = [(e,) for e in self.elements]
        with mp.Pool(processes=4) as p:
            dataList = p.starmap(extract_COO, args)

        # find the total number of non zero elements in all local matrices
        size = 0
        for data in dataList:
            size += len(data[0])

        rows = np.empty(size, dtype=np.int64)
        cols = np.empty(size, dtype=np.int64)
        vals = np.empty(size)

        pos = 0
        for data in dataList:
            nComponents = len(data[0])

            # re-write row and col in terms of global node numbers
            rows[pos:pos + nComponents] = data[0]
            cols[pos:pos + nComponents] = data[1]
            vals[pos:pos + nComponents] = data[2]
            pos += nComponents

        self.KglobalSp = scipySparse.coo_matrix(
            (vals, (rows, cols)), shape=(self.nNodes, self.nNodes)).tocsr()

        # import pandas as pd

        # df = pd.DataFrame(data=self.KglobalSp.todense())
        # df.to_csv('kglobal_mesh_06-fem_elements_class.csv', index=False, header=False)

        del rows
        del cols
        del vals

    def saveKglobal(self, fileName,  # type: str
                    binary=False  # type: bool
                    ):
        """
        Saves the global stiffness matrix (Kglobal) to a file.

        This method writes the global stiffness matrix to a specified file in a format suitable for later retrieval and analysis.

        Args:
            file_path (str): The path to the file where the global stiffness matrix will be saved.

        Returns:
            None

        Raises:
            IOError: If there is an error writing to the specified file.
        """
        if binary:
            np.save(fileName, self.Kglobal)
        else:
            np.savetxt(fileName, self.Kglobal)

    def setReferenceVoltageNode(self):
        """
        Sets the reference voltage node for the FEM model.

        This method designates a specific node in the FEM model as the reference voltage node, which is typically used to ground the system or set a known voltage.

        Args:
            node_id (int): The identifier of the node to be set as the reference voltage node.

        Returns:
            None

        Raises:
            ValueError: If the specified node_id does not exist in the model.
        """
        confRefNode = self.confFile.voltage.referenceVoltageNode

        method = confRefNode.method.lower()

        if method == 'fixed_electrode':
            electrdeNbr = confRefNode.fixed_electrode_number
            # subtracts 1 because electrode numbers start with 0 in the code.
            self.voltageRefNode = self.electrodeNodes[electrdeNbr - 1]

        if method == 'origin':
            nodeDists = np.sum(self.nodeCoords * self.nodeCoords, axis=1)
            self.voltageRefNode = np.argmin(nodeDists)

        if method == 'nodeNbr':
            customNode = confRefNode.node_number
            # subtracts 1 because node numbers start with 0 in the code.
            self.voltageRefNode = customNode - 1

        if method == 'coords':
            coords = np.array(confRefNode.node)
            coordsUnit = confRefNode.unit
            coords = unit_converter.to_metre(coords, coordsUnit)

            coords = self.applyRotation(coords, isInverse=False)

            nodeDists = np.sum((self.nodeCoords - coords) ** 2, axis=1)
            self.voltageRefNode = np.argmin(nodeDists)

        self.KglobalSp[self.voltageRefNode, :] = 0
        self.KglobalSp[:, self.voltageRefNode] = 0
        self.KglobalSp[self.voltageRefNode, self.voltageRefNode] = 1.0

    def getElemCentroidsByMeshTag(self, meshTagList, fileName=None):
        """
        Retrieves the centroids of elements in the FEM model that are associated with a specific mesh tag.

        Args:
            tag (int): The tag associated with the mesh elements.

        Returns:
            numpy.ndarray: An array of centroids for the elements that have the specified tag. Each centroid is represented as a coordinate tuple (x, y, z).

        Raises:
            KeyError: If the specified tag does not exist in the mesh.
        """
        centroids = [[elem.centroid[0], elem.centroid[1], elem. centroid[2]]
                     for elem in self.getElementsByMeshTag(meshTagList)]
        centroids = np.array(centroids)
        if fileName is not None:
            np.savetxt(self.outputBaseDir + fileName,
                       centroids, delimiter=';', header='x;y;z')

        return centroids

    def get_kglobal(self):
        """
        Retrieves the global stiffness matrix (Kglobal) for the FEM model.

        This method returns the global stiffness matrix that has been assembled for the FEM model.

        Args:
            None

        Returns:
            scipy.sparse.csr_matrix: The global stiffness matrix in CSR format.

        Raises:
            ValueError: If the global stiffness matrix has not been assembled yet.
        """
        print("> Getting Kglobal")
        return self.KglobalSp
