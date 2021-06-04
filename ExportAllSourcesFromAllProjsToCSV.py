"""
Exports a CSV of all data sources from all maps in an ArcGIS Pro Project

Requires: Python 3.x, ArcGIS license of for arcpy library


Authors: Langdon Sanders

Core looping logic adapted from Thomas Zuberbuehler
    https://gis.stackexchange.com/a/318006
    CC-BY-4.0
"""
__author__ = "City of Dublin"
__version__ = "0.1.0"
__license__ = "MIT"


import arcpy
import pandas as pd

aprx = arcpy.mp.ArcGISProject("CURRENT")
maps = aprx.listMaps()

proFilePath = aprx.filePath
proName = aprx.filePath.split("\\")[-1]

mapSourcesDFs = []


for map in maps:
    print ('--------------------------------------------------------------')
    print (map.name)
    print ('--------------------------------------------------------------')
    layers = map.listLayers()
    
    pro_doc_name = []
    pro_fp = []
    map_names = []
    layer_names = []    
    layer_sources = []
    layer_sources_short = []
    
    for layer in layers:
        if layer.supports('NAME') and layer.supports('LONGNAME') \
                    and layer.supports('DATASOURCE'):
            pro_doc_name.append(proName)
            pro_fp.append(proFilePath)
            map_names.append(map.name)
            layer_names.append(layer.longName)
            layer_sources.append(layer.dataSource)
            print (layer.longName + ' ---> ' + layer.dataSource)
            short_source = layer.dataSource.split(",")[-1].replace("Dataset=", "")
            layer_sources_short.append(short_source)
    mapSourcesDFs.append(pd.DataFrame(list(zip(pro_doc_name, pro_fp, map_names, layer_names, layer_sources, layer_sources_short)), columns = ["ProDocName", "ProFilePath", "MapName", "LayerName", "LayerSourceLong", "LayerSourceShort"]))
    
mapSourcesDFs

merged_dfs = pd.concat(mapSourcesDFs)
merged_dfs

Outfile = "MapSources_{}.csv".format(proName)

merged_dfs.to_csv(Outfile)