#!/bin/python
"""
forward problem solver main class
"""
# -*- coding: utf-8 -*-

import os

from eitpylab.entities.observation_model.ObservationModel import ObservationModelCore
from eitpylab.src.EitGlobalLoader import EitInputModel


class EITbaseProblemCore:
    """
    Base class for both forward and inverse problems
    """

    def __init__(self, confFile, femMesh):
        self.confFile: EitInputModel = confFile
        self.baseDir = './'
        self.filePrefix = 'output_fw_model'
        self.femMesh = femMesh
        self.outputBaseDir = './results/foward_problem'

        # set number of cores
        self.nCoresMKL = 4
        if self.nCoresMKL == 0:
            self.nCoresMKL = 4

        self.currentConfDict = {}
        self.voltageConfDict = {}
        self.observationModel = None

    def _setCurrPattern(self):
        """
        set the current injection pattern
        """

        currentConf = self.confFile.current

        self.currentConfDict['method'] = currentConf.method.lower()

        if self.currentConfDict['method'] not in ['bipolar_skip_full', 'bipolar_pairs', 'trigonometric']:
            print('ERROR: Current pattern type not recognized:  %s' % pattern)
            return

        self.currentConfDict['direction'] = currentConf.direction

        if self.currentConfDict['method'] == 'bipolar_skip_full':
            self.currentConfDict['skip'] = currentConf.skip

        if self.currentConfDict['method'] == 'bipolar_pairs':
            # subtracts 1 because electrode numbers start from 0
            self.currentConfDict['injectionPairs'] = currentConf.injectionPairs
        if self.currentConfDict['method'] == 'trigonometric':
            self.currentConfDict['patternOrder'] = None # not implemented yet. someone will do this in the future (i hope)

        # load current value and converts to Ampere if
        value = currentConf.value
        currUnit = currentConf.unit
        if currUnit == 'mA':
            value *= 0.001

        self.currentConfDict['value'] = value

        self.freq_Hz = currentConf.frequency

    def _setVoltPattern(self):
        """
        set the voltage pattern
        """
        voltageConf =self.confFile.voltage

        self.voltageConfDict['method'] = voltageConf.method.lower()

        if self.voltageConfDict['method'] not in ['single_ended', 'differential_skip']:
            print('ERROR: voltage pattern type not recognized:  %s' % self.voltageConfDict['method'])
            return

        if self.voltageConfDict['method'] == 'differential_skip':
            self.voltageConfDict['direction'] = voltageConf.direction
            self.voltageConfDict['skip'] = voltageConf.skip


class ForwardProblemCore(EITbaseProblemCore):
    """
    forward problem solver core class.
    """

    def __init__(self, confFile, femMesh):
        super().__init__(confFile, femMesh)
        self.confForward = self.confFile.forwardProblem

        self.f = 0
        self.nFrames = self.confForward.frames
        self.frameRate = self.confForward.atlas.frame_rate_hz
        self.framePeriod = 1.0 / self.frameRate

        self.outputFile = None
        self.outputIsBinary = None

        self._setOutputFile()
        print('  -> Creating observation model...')
        self.createObservationModel()

        # load Atlas
        confAtlas = self.confFile.forwardProblem.atlas.active

        # if tools.isActiveElement(confAtlas, xpath='.'):
        #     self.atlasCore = anatomicalAtlas.AnatomicalAtlasCore(confAtlas, self.freq_Hz, self.femMesh)
        # else:
        #     self.atlasCore = None

    def _setOutputFile(self):
        """
        Set output file
        """
        self.outputFile = os.path.abspath('./results/')
        self.outputIsBinary = False

    def createObservationModel(self):
        """
        build the observation model used in the solver
        """
        self._setCurrPattern()
        self._setVoltPattern()

        # forward problem always considers all measurements.
        self.voltageConfDict['removeInjectingPair'] = False

        self.observationModel = ObservationModelCore(self.voltageConfDict, self.currentConfDict, self.femMesh, self.nCoresMKL)

    def exportGMSH(self, title='Forward Problem', iterNbr=0, mode='new', sufixName='_forwardProblem', addDomain=True, addElectrodes=False):
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
            file in gmsh, you must concatenate a .msh file containing the geometry and the file generated with this funcions, eg.,
            using 'cat' command
        sufixName: string
            suffi name of the file
        addDomain: bool
            include elements of the domain
        addElectrodes: bool
            include electrodes

        """

        listElements = []

        if addDomain:
            listElements += [elem for elem in self.femMesh.elements if not elem.propertiesDict['isElectrode']]
        if addElectrodes:
            listElements += [elem for elem in self.femMesh.elements if elem.propertiesDict['isElectrode']]

        self.femMesh.exportGmsh_RhoElements(listElements, title, iterNbr, sufixName, mode)

    def setFrameResistivitiesManual(self, frameNbr, elementVector, rhoValues):
        """
        set the resistivity of the domain manually, i.e., it does not follow the .conf instructions. Preferebly use setFrameResistivities() method
        Parameters
        ----------
        frameNbr: number of the frame
        elementNumber: numpy array of mesh elements
            number of the elements. if an element is not present here, then the resistivity of the element is that present in the FEMmodel
            segment of this file. usually good to use for the electrodes
        rhoValues: numpy array
            resistivity values. The array must contain the resistivites of all elements of the mesh, except the electrodes
        """
        self.currentFrame = frameNbr
        destinationElementNumbers = [elem.number for elem in elementVector]
        self.femMesh.setResistivities(destinationElementNumbers, rhoValues)

    def setFrameResistivities(self, frameNbr):
        """
        set the resistivity of the domain
        Parameters
        ----------
        frameNbr: number of the frame
        """
        self.currentFrame = frameNbr
        self.currentTime = frameNbr * self.framePeriod

        regions = self.confForward.regions_resistivity
        for region in regions:
            if region.active:
                meshTagList = region.mesh_tag
                typeRegion = region.type.lower()
                if typeRegion == 'uniform':
                    rhoList = region.rho

                    if self.currentFrame >= len(rhoList):  # uses the last value of rhoList if frameNbr is larger and the length of rhoList
                        RhoValue = rhoList[-1]
                    else:
                        RhoValue = rhoList[self.currentFrame]

                    self.femMesh.setMeshTagResistivity(meshTagList, RhoValue)

        # TODO - NEED TO ADD OBJECTS TO EIT CONFIGFILE
        # for obj in self.confForward.objects:
        #     if obj.active:
        #         nObjects = tools.getElemValueXpath(obj, xpath='nObjects', valType='int')
        #         meshTagList = tools.getElemValueXpath(obj, xpath='regionTags', valType='list_int')

        #         # read position
        #         support = tools.getElemValueXpath(obj, xpath='position/support', valType='str').lower()
        #         unit = tools.getElemAttrXpath(obj, xpath='position', attrName='unit', attrType='str')

        #         origin = np.array(tools.getElemValueXpath(obj, xpath='position/supportOpts/origin', valType='list_float'))
        #         origin = tools.convToMetre(origin, unit)

        #         if support in ['plane', 'volume', 'line']:
        #             e1 = np.array(tools.getElemValueXpath(obj, xpath='position/supportOpts/e1', valType='list_float'))
        #             e1 = e1 / np.linalg.norm(e1)
        #             e1ValGenerator = tools.randomParam(obj.xpath('position/e1Interval/randomVar')[0])
        #             e1ValGenerator.interval = tools.convToMetre(e1ValGenerator.interval, unit)

        #         if support in ['plane', 'volume']:
        #             e2 = np.array(tools.getElemValueXpath(obj, xpath='position/supportOpts/e2', valType='list_float'))
        #             e2 = e2 / np.linalg.norm(e2)
        #             e2ValGenerator = tools.randomParam(obj.xpath('position/e2Interval/randomVar')[0])
        #             e2ValGenerator.interval = tools.convToMetre(e2ValGenerator.interval, unit)

        #         if support in ['volume']:
        #             e3 = np.array(tools.getElemValueXpath(obj, xpath='position/supportOpts/e3', valType='list_float'))
        #             e3 = e3 / np.linalg.norm(e3)
        #             e3ValGenerator = tools.randomParam(obj.xpath('position/e3Interval/randomVar')[0])
        #             e3ValGenerator.interval = tools.convToMetre(e3ValGenerator.interval, unit)

        #         rhoValGenerator = tools.randomParam(obj.xpath('rho/randomVar')[0])
        #         rhoMode =  tools.getElemValueXpath(obj, xpath='rho/mode', valType='str').lower()

        #         typeObj = tools.getElemValueXpath(obj, xpath='type', valType='str').lower()

        #         if typeObj == 'sphere':
        #             # radius
        #             radiusValGenerator = tools.randomParam(obj.xpath('radius/randomVar')[0])
        #             radiusValGenerator.interval = tools.convToMetre(radiusValGenerator.interval,
        #                                                             tools.getElemAttrXpath(obj, xpath='radius', attrName='unit', attrType='str'))

        #             for i in range(nObjects):
        #                 RhoValue = rhoValGenerator.generateSample(nSamples=1, valIdx=self.currentFrame)

        #                 # load coordinates and convert to metres
        #                 if support in ['volume']:
        #                     center = origin + e1ValGenerator.generateSample(1) * e1 + e2ValGenerator.generateSample(
        #                         1) * e2 + e3ValGenerator.generateSample(1) * e3
        #                 if support in ['plane']:
        #                     while True:
        #                         center = origin + e1ValGenerator.generateSample(1) * e1 + e2ValGenerator.generateSample(1) * e2
        #                         distCenter = np.linalg.norm(center - origin)
        #                         if distCenter < 0.1:
        #                             break
        #                 if support in ['line']:
        #                     center = origin + e1ValGenerator.generateSample(1) * e1

        #                 radius = radiusValGenerator.generateSample(nSamples=1)

        #                 if self.femMesh.hasRotation:
        #                     center = self.femMesh.applyRotation(center, isInverse=False)

        #                 for elem in self.femMesh.elements:
        #                     if elem.propertiesDict['regionTag'] in meshTagList:
        #                         if scipyLinalg.norm(elem.centroid - center) < radius:
        #                             if elem.propertiesDict['isElectrode']:
        #                                 if rhoMode == 'replace':
        #                                     rhoVal = RhoValue
        #                                 if rhoMode == 'add':
        #                                     rhoVal = RhoValue+elem.rhoT

        #                                 if rhoVal < 1e-4:
        #                                     print('warning. negative Resistivity. changing to 1e-4...')
        #                                     rhoVal=1e-4
        #                                 elem.setRhoT(rhoVal)
        #                             else:
        #                                 if rhoMode == 'replace':
        #                                     rhoVal = RhoValue
        #                                 if rhoMode == 'add':
        #                                     rhoVal = RhoValue+elem.rho

        #                                 if rhoVal < 1e-4:
        #                                     print('warning. negative Resistivity. changing to 1e-4...')
        #                                     rhoVal=1e-4
        #                                 elem.setRho(rhoVal)

    def solve(self):
        """
        solve the forward problem. This function will use the current mesh resistivity. See 'setFrameResistivities' method on how to
        update mesh resistivity.

        Returns
        -------
        measurements : 1d numpy array
            electrode voltages of all current patterns

        """

        if self.currentFrame == 0:
            appendFile = False
            mode = 'new'
        else:
            appendFile = True
            mode = 'append'
            
        return self.observationModel.forwardProblemSp(self.outputFile, append=appendFile,
                                                          singleEnded=self.voltageConfDict['method'] == 'single_ended')

        # if self.saveNodalVoltages:
        #     voltages = self.observationModel.forwardProblemSp_allNodes(fileName=self.fileNodalVoltages, append=appendFile)
        #     if self.exportGmshNodalVoltages:
        #         self.observationModel.femMesh.exportGmsh_NodalVoltages(voltages, title='Solution', iterNbr=0, sufixName='_outputNodalVoltages',
        #                                                                mode=mode)

        # if self.outputIsBinary:
        #     print('ERROR: binary format of measurement file is not implemented.')
        #     return None
        # else:
        #     return self.observationModel.forwardProblemSp(self.outputFile, append=appendFile,
        #                                                   singleEnded=self.voltageConfDict['method'] == 'single_ended')
