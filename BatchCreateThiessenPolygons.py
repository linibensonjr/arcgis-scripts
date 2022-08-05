import arcpy, os
def ScriptTool(param0, param1, param2, param3):
    # Script execution code goes here

    arcpy.env.workspace = param0
    #Extract the names of the feature dataset
    units = arcpy.Describe(param1).name
    arcpy.AddMessage(units)
    lgas = arcpy.Describe(param2).name
    arcpy.AddMessage(lgas)
    # ds = arcpy.ListDatasets()
    
    outpath = param3
    unit_list = arcpy.ListFeatureClasses(feature_dataset=units)
    unit_list.sort()
    lga_list = arcpy.ListFeatureClasses(feature_dataset=lgas)
    lga_list.sort()
    if len(unit_list) != len(lga_list):
        arcpy.AddError('Some LGAs or Polling units are missing')
    else:
    
        for fc in unit_list:
            temp_thiessen = r"memory\\outpt"
            clip_out = os.path.join(arcpy.env.workspace, fc)+'Units'
            arcpy.AddMessage(clip_out)
            arcpy.env.extent = lga_list[unit_list.index(fc)]
            xmin, ymin, xmax, ymax = arcpy.env.extent.XMin, arcpy.env.extent.YMin, arcpy.env.extent.XMax, arcpy.env.extent.YMax
            with arcpy.EnvManager(extent='{} {} {} {}'.format(xmin, ymin, xmax, ymax)):
                arcpy.analysis.CreateThiessenPolygons(fc, temp_thiessen, 'ALL')
            arcpy.analysis.Clip(temp_thiessen, lga_list[unit_list.index(fc)] ,clip_out)
        
        arcpy.AddMessage(unit_list)
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
