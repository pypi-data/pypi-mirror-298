# EITpyLab - An open-source education tool for Electral Impedance Tomograph learning in Python

![PyPI - License](https://img.shields.io/pypi/l/EITpyLab%20)
![PyPI - Version](https://img.shields.io/pypi/v/EITpyLab)
![GitHub repo size](https://img.shields.io/github/repo-size/barbaractong/py-eit)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2Fbarbaractong%2Fpy-eit%2Fblob%2Fmaster%2Fpyproject.toml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/EITpyLab%20)

EITpyLab is an innovative open-source project designed to serve as an educational tool for learning Electral Impedance Tomography (EIT) using the Python programming language. Developed initially for educational purposes at UFABC university, EITpyLab is poised to become a valuable resource for students, researchers, and professionals worldwide interested in the field of EIT in medical applications.

## 🔬 What is Electral Impedance Tomography (EIT)?

Electrical Impedance Tomography (EIT) is a non-invasive tomographic imaging technique that estimates the distribution of electrical properties 
within a target. EIT systems make electrical stimulations using surface electrodes and measure the resulting voltages at the surface at 
combinations of the same electrodes, from which tomographic images of electrical impeditivity distribution are generated.

Although EIT is no longer a new technology, new uses are developed all the time. Global research has drastically increased after its 
commercial availability, and has slowly begun to make its way into industry and some areas of medicine.

EIT is a promising method for the development of noninvasive diagnostic medicine, as it is able to provide functional imaging of the body without 
ionizingg radiation. EIT has several applications in medicine, including but not limited to: functional imaging of the lungs, diagnosis of 
pulmonary embolism, detection of tumors, diagnosis and distinction of normal and suspected abnormal tissue within the same 
organ, bedside monitoring of lung perfusion and respiratory function, cerebral circulation, and stroke monitoring.

## 🔎 Why EITpyLab?

EITpyLab is designed to provide an intuitive platform for learning and experimenting with EIT algorithms. By offering a user-friendly Python 
environment, EITpyLab empowers users to explore the theoretical and practical concepts behind EIT, implement algorithms, and visualize results. 
Whether you're a student gaining a foundational understanding of EIT principles or a researcher developing advanced reconstruction algorithms, 
EITpyLab  offers a flexible and customizable framework for your learning journey.

## 🦾 Key Features of EITpyLab:

- **Python-Based Environment:** EITpyLab is built entirely in Python, leveraging its simplicity, versatility, and extensive scientific libraries. Python's intuitive syntax and rich ecosystem make it an ideal choice for beginners and experienced users alike.

- **Educational Resources:** EITpyLab provides comprehensive educational resources, including documentation, tutorials, and sample datasets, to support users at every stage of their learning journey. From introductory concepts to advanced topics, EITpyLab aims to foster a supportive learning environment for users of all backgrounds.

- **Modular Design:** EITpyLa badopts a modular design, allowing users to easily extend and customize the tool according to their specific requirements. Whether you're experimenting with different reconstruction algorithms or integrating EIT into larger projects, EITLearn's modular architecture facilitates seamless integration and collaboration.

- **Real-Time Visualization:** EITpyLab offers real-time visualization capabilities, enabling users to interactively visualize and analyze EIT reconstructions as they evolve. Through dynamic visualizations, users gain deeper insights into the principles of tomographic reconstruction and the behavior of different algorithms.

- **Open-Source Community:** EITpyLab is developed as an open-source project, fostering a vibrant community of contributors, collaborators, and users. By embracing open-source principles, EITpyLab encourages knowledge sharing, collaboration, and continuous improvement, ensuring its relevance and impact in the field of EIT education.

## 💻 Getting Started 

To get started with EITpyLab, follow these steps:

1. Clone the repository: `git clone https://github.com/yourusername/EITpyLab.git`
2. Create a virtual enviroment (recommended):
    Following the guidelines provided by PEP 405, you can create a virtual enviroment by executing the command venv:

    a. Install virtualenv lib: ````pip install virtualenv````
    
    b. Run venv command in your root directory with the path name that should be created

    ````bash
    python3 -m venv ./venv/
    `````

    This command will create your virtual env in the root's project.

2. Install the required dependencies: `pip install -r requirements.txt`

> :bulb: **Tip:** This project also supports Poetry for dependence management. You can you the venv created by Poetry or crete one by yourself. After configure you enviroment, you can run ```poetry install``` in your terminal to install all dependencies needed.

> :warning: **Warning:** Do not upload your machine poetry.lock file to the repo. Our .gitignore prevents this to not happen. But, be careful :grimacing:

3. You can explore the documentation and tutorials provided in the `py_eit` branch. To run it, in development mode, you will need to use ```mkdocs``` lib (already a requirement in .toml file :smile:).
To build it in your local machine, you will need to run the command below in your terminal

````
mkdocs serve
````

> :warning: **Attention:** Check if the you're in the same directory as the mkdocs.yml. You should run the command in the root folder in the py_eit branch!

4. Experiment with the sample datasets and reconstruction algorithms included in the `examples/` directory.
5. Contribute to the project by reporting issues, submitting pull requests, or sharing your feedback with the community.

## :pushpin: Basic usage

The EITpyLab lib uses parameters file as inputs to create a <i>session</i> for your development. The files used are listed next. For a deep documentation, please access the mkdocs local version of it.

- <b>Electrical properties</b>:This file contains general information regarding voltage and input current. It defines the methods of injection, units of measurement, amplitude, and electrodes used in the injection of electrical current.

````yaml
version: '0.1'
numberElectrodes: 32
current:
  frequency: 10000
  value: 1
  unit: mA
  direction: +-
  method: bipolar_skip_full
  skip: 4
  injectionPairs: [[5, 32], [2, 32], [1, 32], [6, 32], [4, 32], [5, 31], [5, 30], [2, 27], [1, 28], [1, 25], [6, 26], [4, 29], [2, 23], [10, 30], [9, 31], [3, 32], [7, 32], [1, 24], [3, 21], [7, 18], [4, 22], [6, 17], [8, 31], [11, 30], [1, 20], [13, 31], [15, 30], [2, 19], [14, 31], [16, 18], [12, 21],]
voltage:
  method: single_ended
  removeInjectingPair: False # veriricar
  direction: -+
  skip: 4
  referenceVoltageNode:
    method: coords
    fixed_electrode_number: 1
    node_number: 3778
    node: [127.937, 123.356, 70.7998]
    unit: mm
femModel:
  path: './mesh_files/mesh_head_06.msh'
  unit: mm
  dimentions: 3
  heigthElement: None
  rotation:
    active: False
    axis: y
    angle_deg: 180
  eletrodes:
    numberElectrodes: 32
    meshTag: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    model: completeHua
    rho_t: 0.02
  regions:
    - label: scalp
      isActive: True
      meshTag: [37]
      dimentions: 3
      rho_0: 4
      isGrouped: False
    - label: skull
      isActive: True
      meshTag: [38]
      dimentions: 3
      rho_0: 12
      isGrouped: False
    - label: CSF
      isActive: True
      meshTag: [39]
      dimentions: 3
      rho_0: 0.5
      isGrouped: False
    - label: GM
      isActive: True
      meshTag: [40]
      dimentions: 3
      rho_0: 7.14
      isGrouped: False
forwardProblem:
  frames: 4
  atlas:
    active: False
    frame_rate_hz: 4
  nodalVoltages: 
    active: False
    path: ./mesh_nodal_voltages.txt
  exportGmsh: False
  measurementOutputPath: ./mesh_head_06_measurements_forwardProblem.txt
  regions_resistivity:
    - type: uniform
      mesh_tag: [39, 40]
      rho: [5]
  objects: # None or properties
    - type: sphere
      active: False
      region_tag: [39, 40]
      unit: mm
      center: [125, 50, 145]
      radius: 10
      rho: [-1, 10]
inverseProblem:
  rho_0: uniform
  method: gauss_newton
  measurementFrames: [1]
  measurementFile: ./mesh_head_07_measurements_forwardProblem.txt
  dataFidelityTerm:
    removeMeasInjectingPair: False
    weightMatrixType: identity
    invCovAlphaNoise: 1.0e-5
  options:
    file: None
    lineNumber: None
    stopCriteria:
      maxIterations: 20
      costFunction:
        active: False
        value: 0.1
        variationPercentage: 
          active: False
          value: 0.2
        updateNorm:
          active: False
          value: 0.3
        relaxationFactor:   
          active: True
          value: 0.5
  stateVector:
    regionTags: [40]
  observationModelType: Linear
  regularizations:
    - type: Tikhonov 
      active: True
      method: None
      regularizationParameter: 1.0e-8
      regVector: None
      stdDevination: 
        unit: None
        value: None
        separateRegions: None
        useAtlasAvg: None
      pinvParam:
        normalizedSingValLimit: None
      whiteNoiseParam:
        covMatrixBetaParam: None
      projectionParam: 
        nComponents: None
````

2. Starting yout EITpyLab session

````python
import eitpylab as eit

import multiprocessing
import numpy as np

mesh_05 = "./param_files/mesh_head_05.yml"
mesh_06 = "./param_files/mesh_head_06.yml"
mesh_07 = "./param_files/mesh_head_07.yml"

eit_config = eit.EitGlobalLoader(eit_parameter_path=mesh_06)

# Loads FEM mesh based on the path provided in the eit_parameter.yml file
# get domains: py2puml eitpylab/domains eitpylab.domains
fem_mesh = eit.MeshGenerator(path=eit_config.eit_intput_data.femModel.path)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    # Pyinstaller fix - run pip install pywin32 if error in ImportError: DLL load failed while importing _matfuncs_sqrtm_triu
    multiprocessing.freeze_support()

    fem_model = eit.FiniteElementModel(
        eit_config=eit_config.eit_intput_data, mesh_object=fem_mesh
    )

    fem_model.set_resistivities(frame=1)

    fem_model.compute_k_global()
    fem_model.setReferenceVoltageNode()

    k_global_sparse = fem_model.get_k_global_sparse()

    reference_voltage_node = fem_model.get_reference_voltage_node()

    print(reference_voltage_node)

    domain_elements = fem_model.get_domain_elements()
    observation_model = eit.ObservationModel(
        eit_config=eit_config.eit_intput_data,
        domain_elements=domain_elements,
        electrode_nodes=fem_model.electrode_nodes,
        electrodes_domain=fem_model.electrodes_domain,
        engine="mkl",
        k_global=k_global_sparse,
        mesh_object=fem_mesh,
        reference_voltage_node=reference_voltage_node,
    )

    forward_problem = eit.ForwardProblem(eit_config=eit_config.eit_intput_data)

    predicted_voltage = observation_model.get_electrode_voltage()

    print("predicted_voltage: ")
    print(predicted_voltage)

    jacobian = observation_model.get_jacobian_active_measures()

    # observation_model.update(Kglobal=k_global_sparse)

    # inverse_problem = eit.InverseProblem(
    #     eit_config=eit_config.eit_intput_data,
    #     jacobian=observation_model.get_jacobian_active_measures(),
    #     measWeightMatrix=observation_model.get_measure_weight_matrix(),
    #     activeMeasurementPositions=observation_model.active_measurement_positions,
    #     state_elements=domain_elements,
    #     observation_model=observation_model,
    #     kglobal=k_global_sparse
    # )

    # inverse_problem.set_inverse_problem_method()

````


## 🪄 Contributing

Contributions to EITpyLab are welcome and encouraged! Whether you're a developer, educator, or enthusiast, there are many ways to contribute to the project:

- Report issues and suggest enhancements: [Create an Issue](https://github.com/barbaractong/EITpyLab/issues)
- Submit pull requests: [Contribution Guidelines](CONTRIBUTING.md)
- Share your feedback and ideas: [Join the Discussion](https://github.com/barbaractong/EITpyLab/discussions)

## 📝 License

This project is licensed under the [MIT License](LICENSE).


Join us in our mission to democratize EIT education and empower learners worldwide with the tools and knowledge to explore the fascinating field of Electral Impedance Tomography. Whether you're a student, educator, researcher, or enthusiast, your contributions and feedback are invaluable in shaping the future of EITLearn.

Explore EITpyLab today and embark on your journey of discovery in Electral Impedance Tomography with Python!
