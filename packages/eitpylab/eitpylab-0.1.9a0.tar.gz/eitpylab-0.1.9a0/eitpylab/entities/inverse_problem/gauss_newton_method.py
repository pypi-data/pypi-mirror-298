
from eitpylab.entities.fem_model import fem_model

from eitpylab.entities.inverse_problem.regularization.tikhonov import Tikhonov

from eitpylab.entities.observation_model import ObservationModel
from eitpylab.src.EitGlobalLoader import EitInputModel

import numpy as np
from scipy import sparse as scipySparse
from scipy import linalg as scipyLinalg



class GaussNewtonMethod:
    def __init__(
        self,
            eit_config: EitInputModel,
            observation_model: object,
            kglobal: object,
            regularization: object,
            state_vector: object,
            frame_measurement: object,
            fem_model: fem_model,
            state_elements

    ) -> None:
        self.state_elements = state_elements
        self.fem_model = fem_model
        self.relaxationFactor = 1
        self.eit_confg = eit_config
        self.observation_model: ObservationModel = observation_model
        self.kglobal = kglobal
        self.measWeightMatrix = self.set_measure_weight_matrix()

        self.regularization: Tikhonov = regularization

        self.state_vector = state_vector

        self.frame_measurement = frame_measurement
        

    def set_interation(self):
        self.observation_model.update(
            Kglobal=self.kglobal
        )  # Updates jacobian and kglobal

        # ------------------------------------
        # compute left hand matrix  (J^T.W.J + Regularizations)
        # ------------------------------------
        # calc temp = J^T.W
        # print("jac shape", self.observation_model.get_jacobian_active_measures().shape)
        # print("jac measWeightMatrix", self.measWeightMatrix)

        temp = (
            self.observation_model.get_jacobian_active_measures().T
            @ self.measWeightMatrix
        )

        GNmatrix = temp @ self.observation_model.get_jacobian_active_measures()

        print("> Gauss Newton Method: compute regularization")

        alphaMtM = (
            self.regularization.regularization_param * self.regularization.set_MtM()
        )
        GNmatrix += alphaMtM

        # compute sum of regularization terms vReg = \sum \lambda * MTM (x-x^*)
        regVec = np.zeros(GNmatrix.shape[0])
        if self.regularization.regularization_vector is not None:
            regVec += alphaMtM @ (
                self.state_vector - self.regularization.regularization_vector
            )
        else:
            regVec += alphaMtM @ self.state_vector

        # ------------------------------------
        # compute right hand side vector of equation C.37 Erick's thesis.  J^T.W (v_m-v_c) - vReg
        # ------------------------------------
        print("> Gauss Newton Method: compute GNvector")
        GNvector = (
            temp
            @ (self.frame_measurement - self.observation_model.get_electrode_voltage())
            - regVec
        )

        # solve equation C.37 Erick's thesis. GNvector * x = GNvector
        print("> Gauss Newton Method: compute deltaRho")
        deltaRho = np.linalg.solve(GNmatrix, GNvector)

        print(deltaRho)

        return deltaRho

    def solve_frame(self):
        print("> Inverse problem - updating k global")
        self.fem_model.compute_k_global()
        
        print("> Inverse problem - update observation model")
        self.observation_model.update(Kglobal=self.fem_model.get_k_global_sparse())
        
        print("> Inverse problem - set jacobian")
        self.observation_model.set_jacobian()
        
        costFunction = np.empty(shape=[0, 2 + 1]) # fix len = 1
        nIter = 0
        iteration = []

        print("> Gauss Newton Method: State vector")
        print(self.state_vector)

        for i in range(3):  # TODO - ADD MAX INT IN PARAM FILES
            print(f"> Gauss Newton Method: Iteration {i+1}")
            print("\n")
            # print(
            #     "-------------- Frame %03d - Iteration %03d --------------"
            #     % (self.currentFrame, i + 1)
            # )

            deltaRho = self.set_interation()
            self.state_vector += (
                self.relaxationFactor * deltaRho
            )  # TODO - ADD SETTER FOR STATE VECTOR

            # forces resistivity to be positive
            rhoMin = 0.2
            self.state_vector[
                self.state_vector < rhoMin
            ] = rhoMin  # TODO - ADD SETTER FOR STATE VECTOR

            nIter += 1
            iteration.append(nIter)
            
            costFunction = np.vstack((costFunction, self.calcCostFunction()))
            
            print("> Inverse problem: update elements resistivity")
            
            self.fem_model.set_mesh_tag_resistivity(mesh_tag = self.state_elements, rho=self.state_vector)
            
            print("  -> Iteration cost function components: ", costFunction[-1])

    def set_measure_weight_matrix(self):
        if (
            self.eit_confg.inverseProblem.dataFidelityTerm.weightMatrixType
            == "identity"
        ):
            return scipySparse.identity(
                self.observation_model.active_measurement_positions.shape[0],
                dtype="double",
                format="csr",
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
        
        cost = np.zeros(2 + 1) # fix len = 1
        
        cost[0] = scipyLinalg.norm(self.frame_measurement - self.observation_model.get_electrode_voltage()) ** 2

        # add regularizations
        
        cost[1] = self.regularization.calcCostFunction(self.state_vector)

        cost[-1] = cost.sum()
        return cost
