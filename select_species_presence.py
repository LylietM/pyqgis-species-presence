from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsProject, QgsField, QgsProcessingFeatureSourceDefinition
import processing

# 1. Locate the layers
presen_herpetos = QgsProject.instance().mapLayersByName('herpetos_presencia')[0]
capa = QgsProject.instance().mapLayersByName('utm10Herpetos1')[0]

if not capa.isValid() or not presen_herpetos.isValid():
    raise Exception("Alguna de las capas no es válida.")

# 2. Select species PELPER
presen_herpetos.selectByExpression('"ID" = \'PELPER\'')

# 3. Select the cells that intersect with those occurrences
processing.run("native:selectbylocation", {'INPUT': capa,'PREDICATE': [0],'INTERSECT': QgsProcessingFeatureSourceDefinition(
        presen_herpetos.id(), selectedFeaturesOnly=True), 'METHOD': 0 })

# 4. Save the selected IDs
ids_con_presencia = set(capa.selectedFeatureIds())

# 5. Edit: create the PELPER field
capa.startEditing()

if capa.fields().indexOf("PELPER") == -1:
    capa.addAttribute(QgsField("PELPER", QVariant.Int))
    capa.updateFields()

indice_campo = capa.fields().indexOf("PELPER")

# 6. Assign 1 to the selected cells and 0 to the others
for objeto in capa.getFeatures():
    valor = 1 if objeto.id() in ids_con_presencia else 0
    capa.changeAttributeValue(objeto.id(), indice_campo, valor)

# 7. Save changes and clear selections
if capa.commitChanges():
    capa.removeSelection()
    presen_herpetos.removeSelection()
    print(f"Hecho: {len(ids_con_presencia)} celdas con PELPER = 1.")
else:
    print("Error al guardar:", capa.commitErrors())
