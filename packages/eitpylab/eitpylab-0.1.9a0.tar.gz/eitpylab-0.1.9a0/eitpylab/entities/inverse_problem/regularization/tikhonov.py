#!/bin/python
"""
regularizations module
"""

# -*- coding: utf-8 -*-
import sys
import numpy as np
from scipy import sparse as scipySparse
from scipy import linalg as scipyLinalg
from eitpylab.src.EitGlobalLoader import EitInputModel

class Tikhonov:
    """
    classical tikhonov regularization
    """

    def __init__(self, regConf: EitInputModel, atlasCore, stateElements, baseDir):
        self.baseDir = baseDir
        self.regMatrix = None
        self.regVector = None
        self.stateElements = stateElements
        self.size = [len(self.stateElements), len(self.stateElements)]
        self.setRegParam(regConf.inverseProblem.regularizations[0].regularizationParameter)

        self.atlasCore = None
        # reg vector type
        self.regVectorType = regConf.inverseProblem.regularizations[0].regVector

        self.computeRegVector()
        self.computeRegMatrix()
        self.tag = r'(x-x^*)'

    def setRegParam(self, regParam):
        """
        set regularization parameter
        """
        self.regParam = regParam

    def calcCostFunction(self, stateVector):
        if self.regVector is not None:
            return self.regParam * scipyLinalg.norm(self.regMatrix.dot(stateVector - self.regVector)) ** 2
        else:
            return self.regParam * scipyLinalg.norm(self.regMatrix.dot(stateVector)) ** 2

    def computeRegVector(self):
        """
        compute regularization vector.
        """

        if self.regVectorType.lower() == 'none':
            self.regVector = None
            return

        self.regVector = None

    def computeRegMatrix(self):
        """
        compute regularization matrix. this matrix does not contain the regularization parameter
        """
        self.regMatrix = scipySparse.identity(self.size[0], dtype='double', format='csr')

    def computeMtM(self):
        if scipySparse.issparse(self.regMatrix):
            return np.asarray(self.regMatrix.T.dot(self.regMatrix).todense())
        else:
            return self.regMatrix.T @ self.regMatrix

    def saveRegMatrixTxt(self, fileName,  # type: str
                         binary=False  # type: bool
                         ):
        """
        save regularization Matrix to a file.

        Parameters
        ----------
        fileName: str
            file path

        binary: bool, optional
            save in binary format. Default: False
        """
        if binary:
            np.save(fileName, self.regMatrix)
        else:
            np.savetxt(fileName, self.regMatrix)
