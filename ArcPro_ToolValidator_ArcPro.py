"""Tool validator for Arc Pro batch export tool. Returns a list of layouts for Arc tool UI.""" 


class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""

    def __init__(self):
        """Setup arcpy and the list of tool parameters."""
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Refine the properties of a tool's parameters. This method is
        called when the tool is opened."""
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        layouts = aprx.listLayouts()
        layouts_list = [x.name for x in layouts]
        self.params[1].filter.list = layouts_list
        return

    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed. This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return
