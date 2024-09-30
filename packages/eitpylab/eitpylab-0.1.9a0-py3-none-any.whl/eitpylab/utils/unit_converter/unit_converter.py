class UnitConverter:
    @staticmethod
    def to_metre(inputVal, inputUnit):
        """
        convert the input (scalar or numpy array) to metres

        Parameters
        ----------
        inputVal: scalar or numpy array
            input values
        inputUnit: string
            unit of the input. Implemented units: 'mm', 'cm', 'm', 'in'
        Returns
        -------
        outputVal: scalar or numpy array
            values converted to metres
        """
        if inputUnit.lower() == "mm":
            return inputVal * 0.001
        if inputUnit.lower() == "cm":
            return inputVal * 0.01
        if inputUnit.lower() == "m":
            return inputVal
        if inputUnit.lower() == "in":
            return inputVal * 0.0254

    @staticmethod
    def from_metre(inputVal, outputUnit):
        """
        convert the input em metres (scalar or numpy array) to output unit

        Parameters
        ----------
        inputVal: scalar or numpy array
            input values
        outputUnit: string
            unit of the output. Implemented units: 'mm', 'cm', 'm', 'in'
        Returns
        -------
        outputVal: scalar or numpy array
            values converted to specified unit

        """
        if outputUnit.lower() == "mm":
            return inputVal / 0.001
        if outputUnit.lower() == "cm":
            return inputVal / 0.01
        if outputUnit.lower() == "m":
            return inputVal
        if outputUnit.lower() == "in":
            return inputVal / 0.0254
