'''
Tool that generates Thiessen polygons from
a given point feature class and extent polygon feature class
and then clips the result polygon using the specified extent layer
Finally, the output is stored in the specified output feature class
'''

import arcpy
import os


def ScriptTool(param0, param1, param2):
    fc = param0
    extent = param1
    outfc = param2
    temp_thiessen = r"memory\\output"

    final_out = outfc
    arcpy.env.extent = extent
    xmin, ymin, xmax, ymax = arcpy.env.extent.XMin, arcpy.env.extent.YMin, arcpy.env.extent.XMax, arcpy.env.extent.YMax
    with arcpy.EnvManager(extent='{} {} {} {}'.format(xmin, ymin, xmax, ymax)):
        arcpy.analysis.CreateThiessenPolygons(fc, temp_thiessen, 'ALL')
        arcpy.analysis.Clip(temp_thiessen, extent, final_out)
    # Delete the temporary output
    arcpy.Delete_management(temp_thiessen)
    return


def getUnits(dataset):
    arcpy.env.workspace = dataset
    return arcpy.ListFeatureClasses()


def getLGAs(dataset):
    arcpy.env.workspace = dataset
    return arcpy.ListFeatureClasses()


# This is used to execute code if the file was run but not imported
if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    param2 = arcpy.GetParameterAsText(2)

    ScriptTool(param0, param1, param2)

    # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()
