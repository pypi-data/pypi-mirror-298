import numpy as np


def compare_matrices(
    numpyData,  # type: Array
    file,  # type: str
    label,  # type: str
    isComplex=False,  # type: bool
):
    """
    compare two matrices, one from memory and one stored in a file.

    This function is used to debug the code. The comparison is:
        max( max ( abs(M1-M2) ) )

    Parameters
    ----------
    numpyData: numpy array
        array to be compared

    file: str
        file containing the matrix to be compared. The file must be compatible with numpy.loadtxt function

    label: str
        A label to identify the matrix. This is used to help identifying the result in the output console

    isComplex: bool, optional
        use True if the matrices are complex. Use False otherwise
    """
    if isComplex:
        dataFile = np.loadtxt(file).view(complex)
    else:
        dataFile = np.loadtxt(file)

    # np.testing.assert_allclose(numpyData, dataFile,  atol=1e-14, equal_nan=True, err_msg='differenca em %s' % label , verbose=True)

    print(
        "  -> largest difference (absolute value) of %s : %1.5e"
        % (label, np.amax(np.absolute(numpyData - dataFile)))
    )
