import arcpy
import os


def ScriptTool(param0, param1, param2, param3):
    # Script execution code goes here

    arcpy.env.workspace = param0

    # Extract the names of the feature dataset
    points_features = arcpy.Describe(param1).name
    arcpy.AddMessage(points_features)
    processing_extents = arcpy.Describe(param2).name
    arcpy.AddMessage(processing_extents)

    outpath = param3
    #Get feature classes from feature datasets and sort them alphabetically
    points_list = arcpy.ListFeatureClasses(feature_dataset=points_features)
    points_list.sort()
    extents_list = arcpy.ListFeatureClasses(feature_dataset=processing_extents)
    extents_list.sort()

    #Confirm that there are equal number of points and processing extent
    if len(points_list) != len(extents_list):
        arcpy.AddError('Some processing_extents or Polling points_features are missing')
    else:
        for fc in points_list:
            temp_thiessen = r"memory\\outpt"
            clip_out = os.path.join(arcpy.env.workspace, fc+"Poly")

            #Get the extents of the extent feature class
            arcpy.env.extent = extents_list[points_list.index(fc)]
            xmin, ymin, xmax, ymax = arcpy.env.extent.XMin, arcpy.env.extent.YMin, arcpy.env.extent.XMax, arcpy.env.extent.YMax
            with arcpy.EnvManager(extent='{} {} {} {}'.format(xmin, ymin, xmax, ymax)):
                arcpy.analysis.CreateThiessenPolygons(fc, temp_thiessen, 'ALL')
                clipped = arcpy.analysis.Clip(
                temp_thiessen, extents_list[points_list.index(fc)], clip_out)


    arcpy.AddMessage(points_list)
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
    param3 = arcpy.GetParameterAsText(3)

    ScriptTool(param0, param1, param2, param3)
    getUnits(param1)
    getLGAs(param2)

    # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()
