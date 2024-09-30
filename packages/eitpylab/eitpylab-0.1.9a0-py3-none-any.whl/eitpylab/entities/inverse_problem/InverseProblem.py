#!/bin/python
"""
inverse problem solver main class
"""
import os

# -*- coding: utf-8 -*-
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from eitpylab.entities.fem_model.fem_model import FemModel

from scipy import linalg as scipyLinalg
from scipy import sparse as scipySparse


from eitpylab.entities.forward_problem.ForwardProblem import EITbaseProblemCore

from eitpylab.entities.inverse_problem.regularization.tikhonov import Tikhonov
from eitpylab.entities.observation_model.ObservationModel import LinearObservationModel
from eitpylab.src.EitGlobalLoader import EitInputModel

# loads Qt5Agg only in my laptop

matplotlib.use("Cairo")

class EITcoreSolver:
    """
    Main EIT model class
    """

    def __init__(self, confFile: EitInputModel, buildKglobal=True  # type: str
                 ):
        """
        Parameters
        ----------
        confFile: str
            configuration file .conf

        """
        self.confFile = confFile
        self.baseDir, self.filePrefix = ['./', 'measure_mesh_voltage.txt']

        # creates the base output dir
        generalConf = self.confFile
        self.outputBaseDir = "/"

        # load FEM mesh
        self.femMesh = FemModel(self.confFile, self.outputBaseDir)
        self.femMesh.loadGmsh()
        # self.femMesh.getDomainElemQuality('lixo_elemQuality.txt')
        # self.femMesh.exportGmsh_RhoElements(self.femMesh.elements, title='Rho 1', iterNbr=0, sufixName='_rho0',mode='new')

        if buildKglobal:
            start = time.time()

            self.femMesh.buildKglobal()

            if False:
                tools.saveSparseCOO(self.femMesh.KglobalSp, 'lixo_K.txt')

            print('  -> time Kglobal: %f s' % (time.time() - start))
        else:
            print('skipping buildKglobal...')
            print('skipping buildKglobal...')
            print('skipping buildKglobal...')
            print('skipping buildKglobal...')

class InverseProblemCore(EITbaseProblemCore):
    """
    inverse problem solver core class. This class has attributes and methods that should be common to many different
    solvers
    """

    def __init__(self, confFile: EitInputModel, femMesh: FemModel):
        super().__init__(confFile, femMesh)
        self.confFile = confFile
        self.confInv = self.confFile.inverseProblem
        self.filePrefix = self.femMesh.filePrefix
        self.outputFilePrefix = "output_inverse_problem"

        self.frameMeasurement = None
        self.stateElements = None
        self.notStateElements = None
        self.stateVector = None
        self.stateRegionTags = None
        self.sizeState = None
        self.measurementFile = None

        self._setMeasurementFile()

        self.defineStateVector()

        # attention observation model must run after defining the state vector when using linear model (Jacobian requires state vector)
        print("  -> Creating observation model...")
        self.createObservationModel()

        print("Setting rho0...")
        self.setRho0()
        self.currentFrame = 0

        print("  -> Setting data fidelity term...")
        self.weightMatrixType = self.confInv.dataFidelityTerm.weightMatrixType.lower()

        if self.weightMatrixType == "identity":
            self.measWeightMatrix = scipySparse.identity(
                self.observationModel.activeMeasurementPositions.shape[0],
                dtype="double",
                format="csr",
            )

        print("  -> Creating regularizations...")
        self.regularizations = []
        self.createRegularizations()

    def _setMeasurementFile(self):
        """
        Set measurement file
        """

        self.measurementFileType = "regular"
        
        if self.measurementFileType == "regular":
            self.measurementFile = os.path.abspath(
                self.baseDir
                + self.confInv.measurementFile.lower()
            )
            with open(self.measurementFile) as fp:
                for i, l in enumerate(fp):
                    line = l
            # check if file has header and reads its size
            # line = tools.readNthLine(self.measurementFile, 0).rstrip()
            # if line[0] == "#":
            #     self.measurementFileHeaderSize = int(line.split("=")[1])
            # else:
            #     self.measurementFileHeaderSize = 0

    def _readMeasurement(self, measurementFile, isBinary, measNbr, headerSize):
        """
        read one measurement set from the file

        Parameters
        ----------
        measurementFile: str
            measurement file
        isBinary: bool
            file is in binary mode?
        measNbr: int
            measurement to be read. first measurement is number 0
        headerSize: int
            number of lines in the header. If no header, set 0
        Returns
        -------
        measurements : 1d numpy array
            electrode voltages of all current patterns

        """
        if isBinary:
            print("ERROR: binary format of measurement file is not implemented.")
            exit()
        else:
            with open(measurementFile) as fp:
                for i, l in enumerate(fp):
                    measurement = l
            # measurement = tools.readNthLineData(
            #     filePath=measurementFile, lineNbr=measNbr + headerSize, separator=" "
            # )

        return np.fromstring(measurement, sep=" ")

    def setFrameMeasurement(self, frame):
        """
        load frame measurement data

        Parameters
        ----------
        frame: int
            number of the frame. first frame is number 0
        """
        self.currentFrame = frame

        
        self.frameMeasurement = self._readMeasurement(
            self.measurementFile,
            False,
            self.currentFrame,
            0,
        )

        self.frameMeasurement = self.frameMeasurement[
            self.observationModel.activeMeasurementPositions
        ]

    def exportSolutionGMSH(
        self,
        title="Solution",
        iterNbr=0,
        mode="new",
        sufixName="_output",
        addStateVector=True,
        addRestOfDomain=False,
        addElectrodes=False,
    ):
        """
        Export the solution to gmsh

        Parameters
        ----------
        title: string
            title of the view in Gmsh
        iterNbr: int
            Number of the iteration
        mode: string
            valid options: 'append', 'new', 'solution_only'
            - 'append': Appends the resistivities to an existing File. In this case, one must make sure the titles of each
            solution is unique. This option allow many solutions to be saved in a single .msh file. If the output file does not exist,
            this mode works exactly as 'new', i.e., a new file will be created and the solution will be included.
            - 'new': creates a mesh file with both geometry definition and solution in one $ElementData of the msh format.
                This is used to save a single solution to a .msh file. Obs: you can use later 'append' to the file created in this mode to add more solutions
            - 'solution_only': saves only the information about the solution, i.e., no information about the mesh is saved. In order to use this
            file in gmsh, you must concatenate a .msh file containing the geometry and the file generated with this funcions, e..,
            using 'cat' command
        sufixName: string
            suffi name of the file
        addStateVector: bool
            include state vector
        addRestOfDomain: bool
            include elements of the domain not in the state vector
        addElectrodes: bool
            include electrodes

        Returns
        -------
        """

        listElements = []

        if addStateVector:
            listElements += [self.femMesh.elements[e] for e in self.stateElements]
        if addRestOfDomain:
            listElements += [
                self.femMesh.elements[e]
                for e in self.notStateElements
                if not self.femMesh.elements[e].propertiesDict["isElectrode"]
            ]
        if addElectrodes:
            listElements += [
                self.femMesh.elements[e]
                for e in self.notStateElements
                if self.femMesh.elements[e].propertiesDict["isElectrode"]
            ]

        self.femMesh.exportGmsh_RhoElements(
            listElements, title, iterNbr, sufixName, mode
        )

    def calcCostFunction(self):
        """
        compute the cost function of the current state vector.

        Returns
        -------
        cost: numpy array
            each element of the vector is one component of the total cost function.
                - cost[0]: term related to measurement
                            ||v_meas - v_calc||^2_2
                - cost[i], i>=1:  term associated to the i-th regularization (the same order in which they are loaded from the .conf file
                            alpha*|| L*(rho - rho*)||^2_2
                - cost[end]: total cost

        """
        cost = np.zeros(2 + len(self.regularizations))

        cost[0] = (
            scipyLinalg.norm(
                self.frameMeasurement - self.getPredictedMeasurements(fileName=None)
            )
            ** 2
        )

        # add regularizations
        for i, reg in enumerate(self.regularizations):
            cost[i + 1] = reg.calcCostFunction(self.stateVector)

        cost[-1] = cost.sum()
        return cost

    def getPredictedMeasurements(self, fileName=None, append=False):
        """
        get the current measurement prediction. This function will use the current mesh resistivity,. See 'updateMeshResistivity' method on how to
        update mesh resistivity with the state vector.

        Parameters
        ----------
        fileName: str, optional
            name of the file. If None, no file will be saved
        append: bool, optional
            if True, the file will be appended with the measurements. Default: False

        Returns
        -------
        measurements : 1d numpy array
            electrode voltages of all current patterns

        """
        return self.observationModel.forwardProblemSp(
            fileName,
            append,
            singleEnded=self.voltageConfDict["method"] == "single_ended",
        )

    def defineStateVector(self):
        """
        defines the state vector. This function is automatically called by __init__()
        """

        self.stateRegionTags = self.confInv.stateVector.regionTags

        # this vector stores the number of the elements that compose the state vector.
        self.stateElements = []
        self.notStateElements = []
        self.stateVector = []
        for elem in self.femMesh.elements:
            if elem.propertiesDict["regionTag"] in self.stateRegionTags:
                self.stateElements.append(elem.number)
                if elem.propertiesDict["isElectrode"]:
                    self.stateVector.append(elem.rhoT)
                else:
                    self.stateVector.append(elem.rho)
            else:
                self.notStateElements.append(elem.number)

        self.stateElements = np.array(self.stateElements)
        self.notStateElements = np.array(self.notStateElements)
        self.stateVector = np.array(self.stateVector)
        print("State vector: defineStateVector")
        print(self.stateVector)
        self.sizeState = len(self.stateElements)

        print("State vector size: ", self.sizeState)

    def setRho0(self):
        """
        set rho0 based on the configuration file
        """
        rho0Type = self.confInv.rho_0

        if rho0Type == "uniform":
            # if uniform, then there is nothing to do here since the resistivity values were set when creating the FEM model.
            return

    def updateMeshResistivity(self, stateVector):
        """
        update the resistivity of the mesh from the state vector

        Parameters
        ----------
        stateVector: numpy.array
            state vector with the resistivities

        """
        self.femMesh.setResistivities(self.stateElements, stateVector)

    def createObservationModel(self):
        """
        build the observation model used in the solver
        """
        self._setCurrPattern()

        self._setVoltPattern()

        self.voltageConfDict["removeInjectingPair"] = self.confInv.dataFidelityTerm.removeMeasInjectingPair


        obsType = "linear"

        if obsType == "linear":
            self.observationModel = LinearObservationModel(
                self.voltageConfDict,
                self.currentConfDict,
                self.femMesh,
                self.stateElements,
                self.nCoresMKL,
            )

    def createRegularizations(self):
        """
        bulid the regularizations
        """
        regularizations = self.confInv.regularizations

        for reg in regularizations:
            if reg.type == "Tikhonov":
                self.regularizations.append(
                    Tikhonov(
                        atlasCore=None, baseDir=self.baseDir, regConf=self.confFile, stateElements=self.stateElements
                    )
                )

    def solveFrame(self, calcCost=False):
        print("ERROR: this function must be redefined in the inherited class!")

        pass
        return [None, None]


class InverseProblem_GaussNewton(InverseProblemCore):
    def __init__(self, confFile, femMesh):
        super().__init__(confFile, femMesh)

        # stop criteria
        self.stopCriteriaDict = {}
        self.relaxationFactor = 1.0
        self._setIterationConfiguration()

    def _setIterationConfiguration(self):
        stopCriteria = self.confInv.options.stopCriteria

        self.stopCriteriaDict["maxIter"] = stopCriteria.maxIterations

        if stopCriteria.costFunction.active:
            self.stopCriteriaDict["costFuncVal"] = stopCriteria.costFunction.value

        if stopCriteria.costFunction.variationPercentage.active:
            self.stopCriteriaDict["costFuncVarPerc"] = stopCriteria.costFunction.variationPercentage.value

        if stopCriteria.costFunction.updateNorm.active:
            self.stopCriteriaDict["solutionUpdateNorm"] = stopCriteria.costFunction.updateNorm.value

        if stopCriteria.costFunction.relaxationFactor.active:
            self.relaxationFactor = stopCriteria.costFunction.relaxationFactor.value

    def _iteration(self):
        """
        runs one iteration of the gauss-newton algorithm.

        See equation C.37, Ericks thesis, pg 100
        """

        """
        # compute right hand side vector of equation C.37 Erick's thesis.  J^T.W (v_m-v_c) - vReg
        vector1 = self.observationModel.jacobian.T @ self.measWeightMatrix @ (self.frameMeasurement - self.getPredictedMeasurements()) - vReg

        if False:
            deltaRho = np.matmul(np.linalg.inv(GNmatrix), vector1)
        else:
            deltaRho = np.linalg.solve(GNmatrix, vector1)

        return deltaRho
        """

        # update Kglobal and observation model
        self.femMesh.buildKglobal()
        self.observationModel.update()
        self.observationModel.calcJacobian()

        print("Compting Gauss-Newton step...")
        # ------------------------------------
        # compute left hand matrix  (J^T.W.J + Regularizations)
        # ------------------------------------

        # calc temp = J^T.W
        print("Gauss jac shape: ", self.observationModel.jacobian.shape)
        print("Gauss meas weight shape: ", self.measWeightMatrix.shape)

        temp = self.observationModel.jacobian.T @ self.measWeightMatrix
        GNmatrix = temp @ self.observationModel.jacobian

        # add regularizations
        regVec = np.zeros(GNmatrix.shape[0])
        for reg in self.regularizations:
            alphaMtM = reg.regParam * reg.computeMtM()
            GNmatrix += alphaMtM

            # compute sum of regularization terms vReg = \sum \lambda * MTM (x-x^*)
            if reg.regVector is not None:
                regVec += alphaMtM @ (self.stateVector - reg.regVector)
            else:
                regVec += alphaMtM @ self.stateVector

        # ------------------------------------
        # compute right hand side vector of equation C.37 Erick's thesis.  J^T.W (v_m-v_c) - vReg
        # ------------------------------------
        GNvector = (
            temp @ (self.frameMeasurement - self.getPredictedMeasurements()) - regVec
        )

        # solve equation C.37 Erick's thesis. GNvector * x = GNvector
        deltaRho = np.linalg.solve(GNmatrix, GNvector)

        return deltaRho

    def solveFrame(self):
        costFunction = np.empty(shape=[0, 2 + len(self.regularizations)])
        nIter = 0

        # initializes plot
        # plt.ion()  # interaction on

        fig, ax = plt.subplots(nrows=1, ncols=costFunction.shape[1], figsize=(21, 7))

        ax = ax.flatten()
        iteration = []
        # 0:y data 1:title
        plotData = [[[], r"Data fidelity term $||v_m-v(\rho)||^2$"]]
        for reg in self.regularizations:
            plotData.append([[], r"Prior $\alpha||%s||^2$" % reg.tag])

        plotData.append([[], "Total cost"])

        linePlots = []
        for i, p in enumerate(plotData):
            line = ax[i].semilogy(iteration, plotData[i][0])
            linePlots.append(line[0])
            ax[i].set_title(plotData[i][1])
            ax[i].set_xlabel("Iteration")
            ax[i].set_ylabel("Value")
            ax[i].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

        # fig.tight_layout()
        
        self.exportSolutionGMSH(
            title="initial guess",
            iterNbr=0,
            mode="new",
            sufixName="%sframe_%d_GN_iterations"
            % (self.outputFilePrefix, self.currentFrame),
            addStateVector=True,
            addRestOfDomain=True,
            addElectrodes=False,
        )

        for i in range(self.stopCriteriaDict["maxIter"]):
            print("State vector")
            print(self.stateVector)

            start = time.time()

            print("\n")
            print(
                "-------------- Frame %03d - Iteration %03d --------------"
                % (self.currentFrame, i + 1)
            )
            deltaRho = self._iteration()
            self.stateVector += self.relaxationFactor * deltaRho

            # forces resistivity to be positive
            rhoMin = 0.2
            self.stateVector[self.stateVector < rhoMin] = rhoMin

            nIter += 1
            iteration.append(nIter)
            costFunction = np.vstack((costFunction, self.calcCostFunction()))

            self.updateMeshResistivity(self.stateVector)

            
            self.exportSolutionGMSH(
                title="iteration %0.3d" % i,
                iterNbr=i,
                mode="append",
                sufixName="%sframe_%d_GN_iterations"
                % (self.outputFilePrefix, self.currentFrame),
                addStateVector=True,
                addRestOfDomain=True,
                addElectrodes=False,
            )

            # updating plots
            for j, line in enumerate(linePlots):
                line.set_data(iteration, costFunction[:, j])
                ax[j].relim()
                # update ax.viewLim using the new dataLim
                ax[j].autoscale_view()

            # plt.draw()
            plt.pause(0.1)

            # stop criteria
            if "costFuncVal" in self.stopCriteriaDict:
                if np.sum(costFunction[-1]) <= self.stopCriteriaDict["costFuncVal"]:
                    break

            if "costFuncVarPerc" in self.stopCriteriaDict:
                if (
                    abs(np.sum(costFunction[-1]) - np.sum(costFunction[-2]))
                    / np.sum(costFunction[-1])
                    <= self.stopCriteriaDict["costFuncVarPerc"]
                ):
                    break

            if "solutionUpdateNorm" in self.stopCriteriaDict:
                if (
                    scipyLinalg.norm(deltaRho)
                    <= self.stopCriteriaDict["solutionUpdateNorm"]
                ):
                    break

            print("  -> Iteration cost function components: ", costFunction[-1])
            print("  -> time Gauss-Newton iteration: %f s" % (time.time() - start))

        outputfile_noExtension = (
            self.outputBaseDir
            + self.filePrefix
            + "%scostFunction_frame_%04d" % (self.outputFilePrefix, self.currentFrame)
        )
        # plt.subplots_adjust(
        #     left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.5
        # )
        # plt.savefig(
        #     outputfile_noExtension + ".png",
        #     dpi=None,
        #     facecolor="w",
        #     edgecolor="w",
        #     format="png",
        #     transparent=True,
        #     bbox_inches="tight",
        #     pad_inches=0.1,
        # )
        # plt.savefig(
        #     outputfile_noExtension + ".svg",
        #     facecolor="w",
        #     edgecolor="w",
        #     format="svg",
        #     transparent=True,
        #     bbox_inches="tight",
        #     pad_inches=0.1,
        # )
        # plt.close(fig)

        np.savetxt(
            "./cost_func.txt",
            costFunction,
            header=" ; ".join([x[1] for x in plotData]),
        )

        return [np.array(costFunction), len(costFunction)]

class EITinverseSolver(EITcoreSolver):
    """
    Main EIT inverse problem class
    """

    def __init__(self, confFile: EitInputModel  # type: str
                 ):
        """
        Parameters
        ----------
        confFile: str
            configuration file .conf

        """
        super().__init__(confFile)

        # create inverse problem
        print('Creating inverse problem environment...')
        self.invProblemConf = self.confFile.inverseProblem


        self.inverseProblem = InverseProblem_GaussNewton(self.confFile, self.femMesh)

    def solveFrames(self):

        measurementFrames = self.invProblemConf.measurementFrames

        # builds the inverse problem: absolute image

        for i, frame in enumerate(measurementFrames):
            print('Solving frame %d' % frame)
            self.inverseProblem.setFrameMeasurement(frame)
            start = time.time()
            self.inverseProblem.solveFrame()
            print('time GaussNewton convergence: %f s' % (time.time() - start))

            if i == 0:
                mode = 'new'
            else:
                mode = 'append'

            sufixName = '%sinverseProblemSolution' % self.inverseProblem.outputFilePrefix

            self.inverseProblem.exportSolutionGMSH(title='Solution frame %03d (ohm.m)' % frame, iterNbr=frame, sufixName=sufixName, mode=mode,
                                                    addStateVector=True, addRestOfDomain=True, addElectrodes=False)

            if i > 0:
                gmshFile = self.outputBaseDir + self.filePrefix + sufixName + '.msh'
                nElementData = self.inverseProblem.femMesh.gmsh_getNumberOfElementData(gmshFile)
                self.inverseProblem.femMesh.gmsh_export_ElemDataDifference(gmshFile, elementDataPosition=nElementData, elementDataPositionRef=1,
                                                                            title='Difference solution: Frame %03d - Frame %03d (ohm.m)' % (
                                                                                frame, measurementFrames[0]))
