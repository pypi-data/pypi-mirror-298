"""
eit_global_loader.py

This module provides data structures and utility functions for handling Electrical Impedance Tomography (EIT) data.

Classes:
    InjectionPair: A data class representing a pair of electrodes used for injection in EIT.
    CurrentProperties: A data class representing the properties of the current used in EIT.

Functions:
    set_absolute_path: A utility function to set absolute paths (imported from eitpylab.utils.os_path_pattern.os_path_pattern).
    EitParameterParser: A class or function to parse parameters related to EIT (imported from eitpylab.utils.parameter_parser.parameter_parser).

Imports:
    - dataclass: A decorator for creating data classes.
    - typing: Provides type hints for better code readability and type checking.
        - Any: Represents any type.
        - Dict: Represents a dictionary type.
        - List: Represents a list type.
        - Union: Represents a union of multiple types.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Union

from eitpylab.utils.os_path_pattern.os_path_pattern import set_absolute_path
from eitpylab.utils.parameter_parser.parameter_parser import EitParameterParser


@dataclass
class InjectionPair:
    electrodes: List[int]


@dataclass
class CurrentProperties:
    frequency: float
    value: int
    unit: str
    direction: str
    method: str
    skip: int
    injectionPairs: List[InjectionPair]


@dataclass
class ReferenceVoltageNode:
    method: str
    fixed_electrode_number: int
    node_number: int
    node: List[float]
    unit: str


@dataclass
class VoltageProperties:
    method: str
    removeInjectingPair: bool
    direction: str
    skip: int
    referenceVoltageNode: ReferenceVoltageNode


@dataclass
class Rotation:
    active: bool
    axis: str
    angle_deg: int


@dataclass
class Electrodes:
    numberElectrodes: int
    meshTag: List[int]
    model: str
    rho_t: float


@dataclass
class Region:
    label: str
    isActive: bool
    meshTag: List[int]
    dimentions: int
    rho_0: float
    isGrouped: bool


@dataclass
class FemModel:
    path: str
    unit: str
    dimentions: int
    heigthElement: str
    rotation: Rotation
    eletrodes: Electrodes
    regions: List[Region]


@dataclass
class NodalVoltages:
    active: bool
    path: str


@dataclass
class Object:
    type: str
    active: bool
    region_tag: list[int]
    unit: str
    center: list[float]
    radius: float
    rho: list[int]


@dataclass
class Atlas:
    """
    Data class representing the atlas of a forward problem model.

    Attributes:
        active (bool): Whether the atlas is active.
        frame_rate_hz (int): Frame rate in Hz.
        frames (int): Number of frames.
    """

    active: bool
    frame_rate_hz: int


@dataclass
class regions_resistivity:
    type: str
    active: bool
    mesh_tag: list[int]
    rho: list[int]


@dataclass
class ForwardProblemModel:
    frames: int
    atlas: Atlas
    nodalVoltages: NodalVoltages
    exportGmsh: bool
    measurementOutputPath: str
    regions_resistivity: List[regions_resistivity]
    objects: List[Object]


@dataclass
class VariationPercentage:
    active: bool
    value: float


@dataclass
class UpdateNorm:
    active: bool
    value: float


@dataclass
class RelaxationFactor:
    active: bool
    value: float


@dataclass
class CostFunction:
    active: bool
    value: float
    variationPercentage: VariationPercentage
    updateNorm: UpdateNorm
    relaxationFactor: RelaxationFactor


@dataclass
class StopCriteria:
    maxIterations: int
    costFunction: CostFunction


@dataclass
class StateVector:
    regionTags: List[int]


@dataclass
class StdDevination:
    unit: Union[str, None]
    value: Union[float, None]
    separateRegions: Union[bool, None]
    useAtlasAvg: Union[bool, None]


@dataclass
class PinvParam:
    normalizedSingValLimit: float


@dataclass
class WhiteNoiseParam:
    covMatrixBetaParam: float


@dataclass
class ProjectionParam:
    nComponents: int


@dataclass
class Regularization:
    type: str
    active: bool
    method: Union[str, None]
    regularizationParameter: float
    regVector: Union[str, None]
    stdDevination: StdDevination
    pinvParam: PinvParam
    whiteNoiseParam: WhiteNoiseParam
    projectionParam: ProjectionParam


@dataclass
class InverseProblemOptions:
    file: Union[str, None]
    lineNumber: Union[int, None]
    stopCriteria: StopCriteria

@dataclass
class DataFidelityTerm:
    removeMeasInjectingPair: bool
    weightMatrixType: str
    invCovAlphaNoise: float
    
@dataclass
class InverseProblemModel:
    method: str
    rho_0: str
    dataFidelityTerm: DataFidelityTerm
    measurementFrames: list[int]
    measurementFile: str
    options: InverseProblemOptions
    stateVector: StateVector
    observationModelType: str
    regularizations: List[Regularization]


@dataclass
class EitInputModel:
    version: str
    numberElectrodes: int
    current: CurrentProperties
    voltage: VoltageProperties
    femModel: FemModel
    forwardProblem: ForwardProblemModel
    # maybe we should change this piece of code
    inverseProblem: InverseProblemModel


class EitGlobalLoader:
    def __init__(self, eit_parameter_path: str) -> None:
        self.eit_parameter_path = set_absolute_path(eit_parameter_path)
        self.parser = EitParameterParser(self.eit_parameter_path)

        self.eit_parameter_input: EitInputModel = self.parser.get_eit_parameter()

        self.eit_intput_data = self.map_to_eit_input_model(self.eit_parameter_input)

    def map_to_eit_input_model(self, data: Dict[str, Any]) -> EitInputModel:
        current = data["current"]
        voltage = data["voltage"]
        fem_model = data["femModel"]
        forward_problem = data["forwardProblem"]
        inverse_problem = data["inverseProblem"]

        return EitInputModel(
            version=data["version"],
            numberElectrodes=data["numberElectrodes"],
            current=CurrentProperties(
                frequency=current["frequency"],
                value=current["value"],
                unit=current["unit"],
                direction=current["direction"],
                method=current["method"],
                skip=current["skip"],
                injectionPairs=[
                    InjectionPair(electrodes=pair) for pair in current["injectionPairs"]
                ],
            ),
            voltage=VoltageProperties(
                method=voltage["method"],
                removeInjectingPair=voltage["removeInjectingPair"],
                direction=voltage["direction"],
                skip=voltage["skip"],
                referenceVoltageNode=ReferenceVoltageNode(
                    method=voltage["referenceVoltageNode"]["method"],
                    fixed_electrode_number=voltage["referenceVoltageNode"][
                        "fixed_electrode_number"
                    ],
                    node_number=voltage["referenceVoltageNode"]["node_number"],
                    node=voltage["referenceVoltageNode"]["node"],
                    unit=voltage["referenceVoltageNode"]["unit"],
                ),
            ),
            femModel=FemModel(
                path=fem_model["path"],
                unit=fem_model["unit"],
                dimentions=fem_model["dimentions"],
                heigthElement=fem_model["heigthElement"],
                rotation=Rotation(
                    active=fem_model["rotation"]["active"],
                    axis=fem_model["rotation"]["axis"],
                    angle_deg=fem_model["rotation"]["angle_deg"],
                ),
                eletrodes=Electrodes(
                    numberElectrodes=fem_model["eletrodes"]["numberElectrodes"],
                    meshTag=fem_model["eletrodes"]["meshTag"],
                    model=fem_model["eletrodes"]["model"],
                    rho_t=fem_model["eletrodes"]["rho_t"],
                ),
                regions=[
                    Region(
                        label=region["label"],
                        isActive=region["isActive"],
                        meshTag=region["meshTag"],
                        dimentions=region["dimentions"],
                        rho_0=region["rho_0"],
                        isGrouped=region["isGrouped"],
                    )
                    for region in fem_model["regions"]
                ],
            ),
            forwardProblem=ForwardProblemModel(
                frames=forward_problem["frames"],
                atlas=Atlas(
                    active=forward_problem["atlas"]["active"],
                    frame_rate_hz=forward_problem["atlas"]["frame_rate_hz"],
                ),
                nodalVoltages=NodalVoltages(
                    active=forward_problem["nodalVoltages"]["active"],
                    path=forward_problem["nodalVoltages"]["path"],
                ),
                exportGmsh=forward_problem["exportGmsh"],
                measurementOutputPath=forward_problem["measurementOutputPath"],
                regions_resistivity=[
                    regions_resistivity(
                        type=obj["type"],
                        active=obj["active"],
                        mesh_tag=obj["mesh_tag"],
                        rho=obj["rho"],
                    )
                    for obj in forward_problem["regions_resistivity"]
                ],
                objects=[
                    Object(
                        type=obj["type"],
                        active=obj["active"],
                        region_tag=obj["region_tag"],
                        unit=obj["unit"],
                        center=obj["center"],
                        radius=obj["radius"],
                        rho=obj["rho"],
                    )
                    for obj in forward_problem["objects"]
                ],
            ),
            inverseProblem=InverseProblemModel(
                method=inverse_problem["method"],
                rho_0=inverse_problem["rho_0"],
                measurementFrames= inverse_problem["measurementFrames"],
                measurementFile = inverse_problem["measurementFile"],
                dataFidelityTerm = DataFidelityTerm(
                    removeMeasInjectingPair=inverse_problem["dataFidelityTerm"]["removeMeasInjectingPair"],
                    weightMatrixType=inverse_problem["dataFidelityTerm"]["weightMatrixType"],
                    invCovAlphaNoise=inverse_problem["dataFidelityTerm"]["invCovAlphaNoise"]
                    ),
                options=InverseProblemOptions(
                    file=inverse_problem["options"]["file"],
                    lineNumber=inverse_problem["options"]["lineNumber"],
                    stopCriteria=StopCriteria(
                        maxIterations=inverse_problem["options"]["stopCriteria"][
                            "maxIterations"
                        ],
                        costFunction=CostFunction(
                            active=inverse_problem["options"]["stopCriteria"][
                                "costFunction"
                            ]["active"],
                            value=inverse_problem["options"]["stopCriteria"][
                                "costFunction"
                            ]["value"],
                            variationPercentage=VariationPercentage(
                                active=inverse_problem["options"]["stopCriteria"][
                                    "costFunction"
                                ]["variationPercentage"]["active"],
                                value=inverse_problem["options"]["stopCriteria"][
                                    "costFunction"
                                ]["variationPercentage"]["value"],
                            ),
                            updateNorm=UpdateNorm(
                                active=inverse_problem["options"]["stopCriteria"][
                                    "costFunction"
                                ]["updateNorm"]["active"],
                                value=inverse_problem["options"]["stopCriteria"][
                                    "costFunction"
                                ]["updateNorm"]["value"],
                            ),
                            relaxationFactor=RelaxationFactor(
                                active=inverse_problem["options"]["stopCriteria"][
                                    "costFunction"
                                ]["relaxationFactor"]["active"],
                                value=inverse_problem["options"]["stopCriteria"][
                                    "costFunction"
                                ]["relaxationFactor"]["value"],
                            ),
                        ),
                    ),
                ),
                stateVector=StateVector(
                    regionTags=inverse_problem["stateVector"]["regionTags"],
                ),
                observationModelType=inverse_problem["observationModelType"],
                regularizations=[
                    Regularization(
                        type=reg["type"],
                        active=reg["active"],
                        method=reg["method"],
                        regularizationParameter=reg["regularizationParameter"],
                        regVector = reg["regVector"],
                        stdDevination=StdDevination(
                            unit=reg["stdDevination"]["unit"],
                            value=reg["stdDevination"]["value"],
                            separateRegions=reg["stdDevination"]["separateRegions"],
                            useAtlasAvg=reg["stdDevination"]["useAtlasAvg"],
                        ),
                        pinvParam=PinvParam(
                            normalizedSingValLimit=reg["pinvParam"][
                                "normalizedSingValLimit"
                            ],
                        ),
                        whiteNoiseParam=WhiteNoiseParam(
                            covMatrixBetaParam=reg["whiteNoiseParam"][
                                "covMatrixBetaParam"
                            ],
                        ),
                        projectionParam=ProjectionParam(
                            nComponents=reg["projectionParam"]["nComponents"],
                        ),
                    )
                    for reg in inverse_problem["regularizations"]
                ],
            ),
        )
