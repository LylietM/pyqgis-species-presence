# SELECT ONE LAYER BY ATTRIBUTE VALUE, THEN SELECT ANOTHER LAYER
# BY LOCATION USING THE PREVIOUSLY SELECTED FEATURES

# Locate the layer
presen_herpetos = QgsProject.instance().mapLayersByName('herpetos_presencia')[0]

# Create a selection expression
presen_herpetos.selectByExpression('\"ID\"=\'PELPER\'')

processing.run("native:selectbylocation", {'INPUT':'C:/BBDD_Confaunex/HERPETOS/Cartografia/utm10Herpetos1.shp','PREDICATE':[0],
'INTERSECT':QgsProcessingFeatureSourceDefinition('C:/Cartografia/Herpetos/herpetos_presencia.shp',
selectedFeaturesOnly=True, featureLimit=-1, geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid),'METHOD':0})

# Locate the layer
capa = QgsProject.instance().mapLayersByName('utm10Herpetos1')[0]

# UPDATE A FIELD WITH A VALUE FOR SELECTED FEATURES ONLY

nuevo_valor = '1'   # Value to assign

# Locate the layer
capa = QgsProject.instance().mapLayersByName('utm10Herpetos1')[0]

# Check whether the layer is valid
if capa.isValid():
    # Start editing the layer
    capa.startEditing()
    
    # Get the selected features
    objetos_seleccionados = capa.selectedFeatures()
    
    # Get the index of the field to update
    capa = iface.activeLayer()
    layer_fields = capa.fields()
    indice_campo = layer_fields.indexOf("PELPER")
    
    # Update the field value for each selected feature
    for objeto in objetos_seleccionados:
        capa.changeAttributeValue(objeto.id(), indice_campo, nuevo_valor)
    
#INVERTIR SELECCION

# Locate the layer
capa = QgsProject.instance().mapLayersByName('utm10Herpetos1')[0]

# Check whether the layer is valid
if capa.isValid():
    # Invert the selection
    capa.invertSelection()
else:
    print("La capa no es válida.")

# UPDATE A FIELD WITH A VALUE FOR SELECTED FEATURES ONLY

nuevo_valor = '0'  # Value to assign

# Locate the layer
capa = QgsProject.instance().mapLayersByName('utm10Herpetos1')[0]

# Check whether the layer is valid
if capa.isValid():
    # Start editing the layer
    capa.startEditing()
    
    # Get the selected features
    objetos_seleccionados = capa.selectedFeatures()
    
    # Get the index of the field to update
    capa = iface.activeLayer()
    layer_fields = capa.fields()
    indice_campo = layer_fields.indexOf("PELPER")
    
    # Update the field value for each selected feature
    for objeto in objetos_seleccionados:
        capa.changeAttributeValue(objeto.id(), indice_campo, nuevo_valor)
    
    # Stop editing and save the changes to the layer
    capa.commitChanges()
else:
    print("La capa no es válida.")

