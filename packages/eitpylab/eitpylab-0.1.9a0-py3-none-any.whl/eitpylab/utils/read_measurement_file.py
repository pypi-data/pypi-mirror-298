import numpy as np


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
            print('ERROR: binary format of measurement file is not implemented.')
            exit()
        else:
            measurement = readNthLineData(filePath=measurementFile, lineNbr=measNbr+headerSize, separator=' ')

        return measurement
    
def readNthLine(filePath,  # type: str
                lineNbr=0  # type: int
                ):
    """
    Parameters
    ----------
    filePath: str
        path of the file

    lineNbr: int
        number of the line. this number starts at 0 (first line)
    Returns
    -------
    line : string
        nth line of the file. If the file has less lines than lineNbr, then line = None
    """
    with open(filePath) as fp:
        for i, line in enumerate(fp):
            if i == lineNbr:
                return line
    return None
    
def readNthLineData(filePath,  # type: str
                    lineNbr=0,  # type: int
                    separator=' '  # type: str
                    ):
    """
    read one line of a file containing an array

    Parameters
    ----------
    filePath: str
        path of the file
    lineNbr: int
        number of the line. this number starts at 0 (first line)
    separator: string
        string used as separator
    Returns
    -------
    values : numpy array
        data contained in the line. If the file has less lines than lineNbr, then line = None
    """
    temp = readNthLine(filePath, lineNbr)
    if temp is not None:
        return np.fromstring(temp, sep=separator)
    else:
        return None