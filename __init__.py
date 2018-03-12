bl_info = {
    "name": "LiberTeeth3D",
    "author": "Cicero Moraes e Graziane Olimpio",
    "version": (1, 0, 0),
    "blender": (2, 75, 0),
    "location": "View3D",
    "description": "Ortodontia no Blender",
    "warning": "",
    "wiki_url": "",
    "category": "liber",
    }


import bpy
import fnmatch
import operator
import tempfile
from os.path import expanduser
import platform
import shutil
import subprocess
from math import sqrt


def liberGeraModelosTomoArcDef(self, context):
    
    scn = context.scene
    
    tmpdir = tempfile.gettempdir()
    tmpSTLarcada = tmpdir+'/Arcada.stl'

    homeall = expanduser("~")

    try:


        if platform.system() == "Linux":


            dicom2DtlPath = homeall+'/Programs/OrtogOnBlender/Dicom2Mesh/dicom2mesh'
#            dicom2DtlPath = get_dicom2stl_filepath(context)


            subprocess.call([dicom2DtlPath, '-i',  scn.my_tool.path, '-r', '0.5', '-s', '-t', '226', '-o', tmpSTLarcada])
	      

            bpy.ops.import_mesh.stl(filepath=tmpSTLarcada, filter_glob="*.stl",  files=[{"name":"Arcada.stl", "name":"Arcada.stl"}], directory=tmpdir)
      


        if platform.system() == "Windows":

            dicom2DtlPath = 'C:/OrtogOnBlender/DicomToMeshWin/dicom2mesh.exe'


            subprocess.call([dicom2DtlPath, '-i',  scn.my_tool.path, '-r', '0.5', '-s', '-t', '226', '-o', tmpSTLarcada])
	      

            bpy.ops.import_mesh.stl(filepath=tmpSTLarcada, filter_glob="*.stl",  files=[{"name":"Arcada.stl", "name":"Arcada.stl"}], directory=tmpdir)


        if platform.system() == "Darwin":


            dicom2DtlPath = homeall+'/OrtogOnBlender/DicomToMeshMAC/dicom2mesh'

#            dicom2DtlPath = get_dicom2stl_filepath(context)


            subprocess.call([dicom2DtlPath, '-i',  scn.my_tool.path, '-r', '0.5', '-s', '-t', '226', '-o', tmpSTLarcada])
	      

            bpy.ops.import_mesh.stl(filepath=tmpSTLarcada, filter_glob="*.stl",  files=[{"name":"Arcada.stl", "name":"Arcada.stl"}], directory=tmpdir)

  
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        bpy.ops.view3d.view_all(center=False)

    except RuntimeError:
        bpy.context.window_manager.popup_menu(ERROruntimeDICOMDef, title="Atenção!", icon='INFO')


class liberGeraModelosTomoArc(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.gera_modelos_tomo_arc"
    bl_label = "Prepara Impressao"
    
    def execute(self, context):
        liberGeraModelosTomoArcDef(self, context)
        return {'FINISHED'}


# IMPORTA CORTE

def ImportaCorteDef(self, context):

    context = bpy.context
    obj = context.active_object
    scn = context.scene

    if platform.system() == "Linux" or platform.system() == "Darwin":
        dirScript = bpy.utils.user_resource('SCRIPTS')
        
        blendfile = dirScript+"addons/LiberTeeth3D-master/objetos.blend"
        section   = "\\Group\\"
        object    = "ArcadaCorta"
        
    if platform.system() == "Windows":
        dirScript = 'C:/OrtogOnBlender/Blender/2.78/scripts/' 

        blendfile = dirScript+"addons/LiberTeeth3D-master/objetos.blend"
        section   = "\\Group\\"
        object    = "Group"

    filepath  = blendfile + section + object
    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(
        filepath=filepath, 
        filename=filename,
        directory=directory)

    bpy.context.space_data.show_relationship_lines = False


class ImportaCorte(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.importa_arcada_corte"
    bl_label = "Importa Arcada Corte"
    
    def execute(self, context):
        ImportaCorteDef(self, context)
        return {'FINISHED'}

# IMPORTA CORTE

def ImportaAlinhaArcadaDef(self, context):

    context = bpy.context
    obj = context.active_object
    scn = context.scene

    if platform.system() == "Linux" or platform.system() == "Darwin":
        dirScript = bpy.utils.user_resource('SCRIPTS')
        
        blendfile = dirScript+"addons/LiberTeeth3D-master/objetos.blend"
        section   = "\\Group\\"
        object    = "ArcadaReferencia"
        
    if platform.system() == "Windows":
        dirScript = 'C:/OrtogOnBlender/Blender/2.78/scripts/' 

        blendfile = dirScript+"addons/LiberTeeth3D-master/objetos.blend"
        section   = "\\Group\\"
        object    = "Group"

    filepath  = blendfile + section + object
    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(
        filepath=filepath, 
        filename=filename,
        directory=directory)

    bpy.context.space_data.show_relationship_lines = False


class ImportaAlinhaArcada(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.importa_alinha_arcada"
    bl_label = "Importa Arcada Corte"
    
    def execute(self, context):
        ImportaAlinhaArcadaDef(self, context)
        return {'FINISHED'}

# ALINHA ARCADA 2

def liberPosicionaEmpties():

    context = bpy.context    
    obj = context.active_object
    v0 = obj.data.vertices[0]
    v1 = obj.data.vertices[1]
    v2 = obj.data.vertices[2]

    co_final0 = obj.matrix_world * v0.co
    co_final1 = obj.matrix_world * v1.co
    co_final2 = obj.matrix_world * v2.co

    # now we can view the location by applying it to an object
    obj_empty0 = bpy.data.objects.new("Dist0", None)
    context.scene.objects.link(obj_empty0)
    obj_empty0.location = co_final0

    obj_empty1 = bpy.data.objects.new("Dist1", None)
    context.scene.objects.link(obj_empty1)
    obj_empty1.location = co_final1

    obj_empty2 = bpy.data.objects.new("Dist2", None)
    context.scene.objects.link(obj_empty2)
    obj_empty2.location = co_final2

def liberMedidaAtual():

    liberPosicionaEmpties()
    
    """ Retorna Média de Três Pontos """
    bpy.ops.object.select_all(action='DESELECT')
    a = bpy.data.objects['Dist0']
    b = bpy.data.objects['Dist1']
    c = bpy.data.objects['Dist2']
    a.select = True
    b.select = True
    c.select = True
    l = []
    for item in bpy.context.selected_objects:
        l.append(item.location)

    distancia1 = sqrt( (l[0][0] - l[2][0])**2 + (l[0][1] - l[2][1])**2 + (l[0][2] - l[2][2])**2)
    distancia2 = sqrt( (l[1][0] - l[2][0])**2 + (l[1][1] - l[2][1])**2 + (l[1][2] - l[2][2])**2)
    distancia3 = sqrt( (l[1][0] - l[0][0])**2 + (l[1][1] - l[0][1])**2 + (l[1][2] - l[0][2])**2)

    print(distancia1)
    print(distancia2)
    print(distancia3)
    
    medidaAtual = max(distancia1, distancia2, distancia3)
#    medidaAtual = min(distancia1, distancia2, distancia3)
    print("A distância menor é:")
    print(medidaAtual)

    medidaReal = float(bpy.context.scene.medida_real)
    print(medidaReal)

    global fatorEscala 
    fatorEscala = medidaReal / medidaAtual
    print(fatorEscala)


# Alinha 2

def AlinhaArcada2Def(self, context):

    liberMedidaAtual()
    
    bpy.ops.object.select_all(action='DESELECT')
    c = bpy.data.objects['Rosto.001']
    bpy.context.scene.objects.active = c
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.object.editmode_toggle() #entra edit mode 
    bpy.ops.view3d.snap_cursor_to_selected() # posiciona o cursor ao centro da seleção
#    bpy.ops.mesh.delete(type='EDGE_FACE') # deleta apenas a face e edges selecionadas
    bpy.ops.object.editmode_toggle() #sai edit mode
    
    bpy.ops.object.select_all(action='DESELECT') # desseleciona todos os objetos
    bpy.ops.object.add(radius=1.0, type='EMPTY', view_align=True)
#    bpy.ops.object.empty_add(type='SINGLE_ARROW', view_align=True) # cria um empty single arrow apontando para o view
    bpy.context.object.name = "Alinhador" #renomeia de alinhador

#    bpy.context.object.rotation_euler[0] = 1.5708

# Parenteia objetos
    a = bpy.data.objects['Rosto']
    b = bpy.data.objects['Alinhador']
    c = bpy.data.objects['Rosto.001']


    bpy.ops.object.select_all(action='DESELECT')
    a.select = True
    b.select = True 
    bpy.context.scene.objects.active = b
    bpy.ops.object.parent_set()
    
    bpy.ops.object.select_all(action='DESELECT')
    c.select = True
    b.select = True 
    bpy.context.scene.objects.active = b
    bpy.ops.object.parent_set() 

# Reseta rotações
    bpy.ops.object.rotation_clear(clear_delta=False)
    
    bpy.ops.object.select_all(action='DESELECT')
    a.select = True
    bpy.context.scene.objects.active = a        
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    bpy.ops.object.select_all(action='DESELECT')
    b.select = True
    bpy.context.scene.objects.active = b
    bpy.ops.object.delete(use_global=False)

    bpy.ops.object.select_all(action='DESELECT')
    c.select = True
    bpy.context.scene.objects.active = c
    bpy.ops.object.delete(use_global=False)

    bpy.ops.object.select_all(action='DESELECT')
    a.select = True 
    bpy.context.scene.objects.active = a
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
#    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


    objRedimensionado = bpy.data.objects['Rosto']
    objRedimensionado.scale = ( fatorEscala, fatorEscala, fatorEscala )

   
    bpy.ops.view3d.viewnumpad(type='FRONT')
    bpy.ops.view3d.view_selected(use_all_regions=False)
    
    
    bpy.context.object.name = "Rosto_OK"
    
    bpy.ops.object.select_all(action='DESELECT')
    a = bpy.data.objects['Dist0']
    b = bpy.data.objects['Dist1']
    c = bpy.data.objects['Dist2']
    a.select = True
    b.select = True
    c.select = True

    bpy.ops.object.delete(use_global=False)


class AlinhaArcada2(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.alinha_arcada2"
    bl_label = "Prepara Impressao"
    
    def execute(self, context):
        AlinhaArcada2Def(self, context)
        return {'FINISHED'}  

# ROTACIONA/FLIP Z

#def liberRotacionaYDef(self, context):
    
#    context = bpy.context
#    obj = context.active_object
#    scn = context.scene

#    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0))

#class liberRotacionaY(bpy.types.Operator):
#    """Tooltip"""
#    bl_idname = "object.liber_rotaciona_y"
#    bl_label = "Rotaciona Z"
    
#    def execute(self, context):
#        liberRotacionaYDef(self, context)
#        return {'FINISHED'}
    
def liberFlipYDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0))

class liberFlipY(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.liber_flip_y"
    bl_label = "Flip Y"
    
    def execute(self, context):
        liberFlipYDef(self, context)
        return {'FINISHED'}

# FOTOGRAMETRIA

def liberGeraModeloFotoDef(self, context):
    
    scn = context.scene
    tmpdir = tempfile.gettempdir()
    homeall = expanduser("~")

    try:

        OpenMVGtmpDir = tmpdir+'/OpenMVG'
        tmpPLYface = tmpdir+'/MVS/meshlabDec.ply'
#        tmpOBJface = tmpdir+'/MVS/scene_dense_mesh_texture2.obj'

        
        if platform.system() == "Linux":
            OpenMVGPath = homeall+'/Programs/OrtogOnBlender/openMVG/software/SfM/SfM_SequentialPipeline.py'
            OpenMVSPath = homeall+'/Programs/OrtogOnBlender/openMVS/OpenMVSarcada.sh'
            
        if platform.system() == "Windows":
            OpenMVGPath = 'C:/OrtogOnBlender/openMVGWin/software/SfM/SfM_SequentialPipeline.py' 
            OpenMVSPath = 'C:/OrtogOnBlender/openMVSWin/OpenMVSarcada.bat' 

        if platform.system() == "Darwin":
            OpenMVGPath = homeall+'/OrtogOnBlender/openMVGMAC/SfM_SequentialPipeline.py' 
            OpenMVSPath = homeall+'/OrtogOnBlender/openMVSMAC/openMVSarcadaMAC.sh'


        shutil.rmtree(tmpdir+'/OpenMVG', ignore_errors=True)
        shutil.rmtree(tmpdir+'/MVS', ignore_errors=True)


        if platform.system() == "Linux":
            subprocess.call(['python', OpenMVGPath , scn.my_tool.path ,  OpenMVGtmpDir])
            
        if platform.system() == "Windows":
            subprocess.call(['C:/OrtogOnBlender/Python27/python', OpenMVGPath , scn.my_tool.path ,  OpenMVGtmpDir])

        if platform.system() == "Darwin":
            subprocess.call(['python', OpenMVGPath , scn.my_tool.path ,  OpenMVGtmpDir])

        subprocess.call(OpenMVSPath ,  shell=True)

    #    subprocess.call([ 'meshlabserver', '-i', tmpdir+'scene_dense_mesh_texture.ply', '-o', tmpdir+'scene_dense_mesh_texture2.obj', '-om', 'vn', 'wt' ])


        bpy.ops.import_mesh.ply(filepath=tmpPLYface, filter_glob="*.ply")
        meshlabDec = bpy.data.objects['meshlabDec']
        
#        bpy.ops.import_scene.obj(filepath=tmpOBJface, filter_glob="*.obj;*.mtl")

#        scene_dense_mesh_texture2 = bpy.data.objects['scene_dense_mesh_texture2']

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = meshlabDec
        bpy.data.objects['meshlabDec'].select = True


#        bpy.context.object.data.use_auto_smooth = False
#        bpy.context.object.active_material.specular_hardness = 60
#        bpy.context.object.active_material.diffuse_intensity = 0.6
#        bpy.context.object.active_material.specular_intensity = 0.3
#        bpy.context.object.active_material.specular_color = (0.233015, 0.233015, 0.233015)
    #    bpy.ops.object.modifier_add(type='SMOOTH')
    #    bpy.context.object.modifiers["Smooth"].factor = 2
    #    bpy.context.object.modifiers["Smooth"].iterations = 3
    #    bpy.ops.object.convert(target='MESH')
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        bpy.ops.view3d.view_all(center=False)
        bpy.ops.file.pack_all()
        
    except RuntimeError:
        bpy.context.window_manager.popup_menu(ERROruntimeFotosDef, title="Atenção!", icon='INFO')


class liberGeraModeloFoto(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.liber_gera_modelo_foto"
    bl_label = "Liber Gera Modelos Foto"

    def execute(self, context):
        liberGeraModeloFotoDef(self, context)
        return {'FINISHED'}
        
# SEPARA DENTES E NOMEIA

def arcadaCortaSupDef(self, context):
    
    #Arcada Superior

    a1 = bpy.data.objects['BaseCorteArcada']
    a2 = bpy.data.objects['BaseCorteDentes']
    b = bpy.data.objects['FaceMalha.001']

    # Faz cópia da arcada cortada

    bpy.ops.object.select_all(action='DESELECT')
    b.select = True
    bpy.context.scene.objects.active = b

    bpy.ops.object.duplicate_move()
    
    # Corta arcada geral

    bpy.ops.object.select_all(action='DESELECT')

    a1.select = True
    b.select = True

    bpy.context.scene.objects.active = b

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action = 'DESELECT')

    bpy.ops.mesh.knife_project(cut_through=True)
    bpy.ops.mesh.separate(type='SELECTED')

    bpy.ops.object.editmode_toggle()

    bpy.ops.object.select_all(action='DESELECT')

    # Apaga resto

    b.select = True
    bpy.context.scene.objects.active = b

    bpy.ops.object.delete(use_global=False)

    # Corta dentes

    bpy.ops.object.select_all(action='DESELECT')
    d = bpy.data.objects['FaceMalha.002']
    a2.select = True
    d.select = True
    bpy.context.scene.objects.active = d

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.mesh.knife_project(cut_through=True)
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='DESELECT')

    # Separa dentes

    e = bpy.data.objects['FaceMalha.001']
    e.select = True
    bpy.ops.mesh.separate(type='LOOSE')

    bpy.ops.object.select_all(action='DESELECT')

    d.select = True
    bpy.ops.mesh.separate(type='LOOSE')


        # Muda nome de FaceMalha.000

    bpy.ops.object.select_all(action='DESELECT')
    c = bpy.data.objects['FaceMalha.000']
    c.select = True
    bpy.context.scene.objects.active = c
    bpy.context.object.name = "ArcadaCortada"
    bpy.ops.object.hide_view_set(unselected=False)
    
# Joga o centro nos dentes

    scene = bpy.context.scene
    foo_objs = [obj for obj in scene.objects if fnmatch.fnmatchcase(obj.name, "FaceMalh*")]
    foo_objs

    elemento = len(foo_objs)
    numero = 0

    while numero < elemento:
        objNome = foo_objs[numero].name
        objeto = bpy.data.objects[objNome]
        objeto.select = True
        bpy.context.scene.objects.active = objeto
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        numero += 1

# Nomeia dentes

    scene = bpy.context.scene
    foo_objs = [obj for obj in scene.objects if fnmatch.fnmatchcase(obj.name, "FaceMalh*")]
    foo_objs

    elemento = len(foo_objs)
    numero = 0

    menosX ={}
    maisX = {}
    menosXordenada = {}
    maisXordenada = {}


    while numero < elemento:
        coordenadaX = foo_objs[numero].location[0]
        if coordenadaX < 0:
            menosX[foo_objs[numero].name] = foo_objs[numero].location[0]
            menosXordenada = sorted(menosX.items(), key=operator.itemgetter(1), reverse=True)


        if coordenadaX > 0:
            maisX[foo_objs[numero].name] = foo_objs[numero].location[0]
            maisXordenada = sorted(maisX.items(), key=operator.itemgetter(1))

        numero += 1

    print(menosXordenada)
    print("------------")
    print(maisXordenada)

    print(type(menosXordenada))
    print(type(maisXordenada))

    numMenos = 0
    lenMenos = len(menosXordenada)
    nomeMenos = 11

    while numMenos < lenMenos:
        objDenteMenos = menosXordenada[numMenos][0]
        bpy.ops.object.select_all(action='DESELECT')
        a = bpy.data.objects[objDenteMenos]
        bpy.context.scene.objects.active = a
        bpy.context.object.name = str(nomeMenos)

        
        numMenos += 1
        nomeMenos += 1
        
    numMais = 0
    lenMais = len(maisXordenada)
    nomeMais = 21

    while numMais < lenMais:
        objDenteMais = maisXordenada[numMais][0]
        bpy.ops.object.select_all(action='DESELECT')
        a = bpy.data.objects[objDenteMais]
        bpy.context.scene.objects.active = a
        bpy.context.object.name = str(nomeMais)
        
        numMais += 1
        nomeMais += 1
    

class arcadaCortaSup(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.arcada_corta_sup"
    bl_label = "Arcada Corta"
    
    def execute(self, context):
        arcadaCortaSupDef(self, context)
        return {'FINISHED'}

def arcadaCortaInfDef(self, context):
    
    #Arcada Superior

    a1 = bpy.data.objects['BaseCorteArcada']
    a2 = bpy.data.objects['BaseCorteDentes']
    b = bpy.data.objects['FaceMalha.001']

    # Faz cópia da arcada cortada

    bpy.ops.object.select_all(action='DESELECT')
    b.select = True
    bpy.context.scene.objects.active = b

    bpy.ops.object.duplicate_move()
    
    # Corta arcada geral

    bpy.ops.object.select_all(action='DESELECT')

    a1.select = True
    b.select = True

    bpy.context.scene.objects.active = b

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action = 'DESELECT')

    bpy.ops.mesh.knife_project(cut_through=True)
    bpy.ops.mesh.separate(type='SELECTED')

    bpy.ops.object.editmode_toggle()

    bpy.ops.object.select_all(action='DESELECT')

    # Apaga resto

    b.select = True
    bpy.context.scene.objects.active = b

    bpy.ops.object.delete(use_global=False)

    # Corta dentes

    bpy.ops.object.select_all(action='DESELECT')
    d = bpy.data.objects['FaceMalha.002']
    a2.select = True
    d.select = True
    bpy.context.scene.objects.active = d

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.mesh.knife_project(cut_through=True)
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='DESELECT')

    # Separa dentes

    e = bpy.data.objects['FaceMalha.001']
    e.select = True
    bpy.ops.mesh.separate(type='LOOSE')

    bpy.ops.object.select_all(action='DESELECT')

    d.select = True
    bpy.ops.mesh.separate(type='LOOSE')


        # Muda nome de FaceMalha.000

    bpy.ops.object.select_all(action='DESELECT')
    c = bpy.data.objects['FaceMalha.000']
    c.select = True
    bpy.context.scene.objects.active = c
    bpy.context.object.name = "ArcadaCortada"
    bpy.ops.object.hide_view_set(unselected=False)
    
# Joga o centro nos dentes

    scene = bpy.context.scene
    foo_objs = [obj for obj in scene.objects if fnmatch.fnmatchcase(obj.name, "FaceMalh*")]
    foo_objs

    elemento = len(foo_objs)
    numero = 0

    while numero < elemento:
        objNome = foo_objs[numero].name
        objeto = bpy.data.objects[objNome]
        objeto.select = True
        bpy.context.scene.objects.active = objeto
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        numero += 1

# Nomeia dentes

    scene = bpy.context.scene
    foo_objs = [obj for obj in scene.objects if fnmatch.fnmatchcase(obj.name, "FaceMalh*")]
    foo_objs

    elemento = len(foo_objs)
    numero = 0

    menosX ={}
    maisX = {}
    menosXordenada = {}
    maisXordenada = {}


    while numero < elemento:
        coordenadaX = foo_objs[numero].location[0]
        if coordenadaX < 0:
            menosX[foo_objs[numero].name] = foo_objs[numero].location[0]
            menosXordenada = sorted(menosX.items(), key=operator.itemgetter(1), reverse=True)


        if coordenadaX > 0:
            maisX[foo_objs[numero].name] = foo_objs[numero].location[0]
            maisXordenada = sorted(maisX.items(), key=operator.itemgetter(1))

        numero += 1

    print(menosXordenada)
    print("------------")
    print(maisXordenada)

    print(type(menosXordenada))
    print(type(maisXordenada))

    numMenos = 0
    lenMenos = len(menosXordenada)
    nomeMenos = 41

    while numMenos < lenMenos:
        objDenteMenos = menosXordenada[numMenos][0]
        bpy.ops.object.select_all(action='DESELECT')
        a = bpy.data.objects[objDenteMenos]
        bpy.context.scene.objects.active = a
        bpy.context.object.name = str(nomeMenos)

        
        numMenos += 1
        nomeMenos += 1
        
    numMais = 0
    lenMais = len(maisXordenada)
    nomeMais = 31

    while numMais < lenMais:
        objDenteMais = maisXordenada[numMais][0]
        bpy.ops.object.select_all(action='DESELECT')
        a = bpy.data.objects[objDenteMais]
        bpy.context.scene.objects.active = a
        bpy.context.object.name = str(nomeMais)
        
        numMais += 1
        nomeMais += 1
    

class arcadaCortaInf(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.arcada_corta_inf"
    bl_label = "Arcada Corta"
    
    def execute(self, context):
        arcadaCortaInfDef(self, context)
        return {'FINISHED'}


# FOTOGRAMETRIA

class liberCriaFotogrametria(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Gera/Importa Arcadas"
    bl_idname = "liber_cria_fotogrametria"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Liber"


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.object 
        

        row = layout.row()
        row.label(text="Digitalização Feita Por Scanner:")

        row = layout.row()
        row.operator("import_mesh.stl", text="Importa STL", icon="IMPORT")


        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.label(text="Digitalização por Fotos:")

        col = layout.column(align=True)
        col.prop(scn.my_tool, "path", text="")
 
        row = layout.row()
        row.operator("object.liber_gera_modelo_foto", text="Iniciar Fotogrametria", icon="IMAGE_DATA")

        row = layout.row()
        row.label(text=" ")

        row = layout.row()        
        row.label(text="Alinhamento e Redimensionamento:")
        layout.operator("object.alinha_rosto", text="1 - Alinha com a Camera", icon="MANIPUL")
        col = self.layout.column(align = True)
        col.prop(context.scene, "medida_real")
        
        layout.operator("object.alinha_arcada2", text="2 - Alinha e Redimensiona", icon="LAMP_POINT")
        
#        row = layout.row()
#        row.operator("object.liber_rotaciona_y", text="Rotaciona Y", icon="FORCE_MAGNETIC")
        
        row = layout.row()
        row.operator("object.liber_flip_y", text="Flip Y", icon="FILE_REFRESH")

        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.label(text="Reconstrução da Tomografia:")

        col = layout.column(align=True)
        col.prop(scn.my_tool, "path", text="")
 
        row = layout.row()
        row.operator("object.gera_modelos_tomo_arc", text="Gera Arcada", icon="SNAP_FACE")

#        col = layout.column(align=True)
#        col.prop(scn.my_tool, "path", text="")





class liberBotoesArcada(bpy.types.Panel):
    """LiberTeeth 3D"""
    bl_label = "Configura Arcada"
    bl_idname = "liber_configura_arcada"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Liber"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.label(text="Segmenta Área de Interesse:")


        row = layout.row()
        circle=row.operator("mesh.primitive_circle_add", text="Círculo de Corte", icon="MESH_CIRCLE")
        circle.radius=52.5
        circle.vertices=100
        circle.location=(0,0,0)
        circle.rotation=(1.5708,0,0)

        row = layout.row()
        knife=row.operator("object.corta_face", text="Cortar!", icon="META_PLANE")

        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.operator("object.importa_arcada_corte", text="Adiciona Plano de Corte", icon="BORDER_LASSO")

        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.label(text="Configuração das Arcadas:")

        row = layout.row()
        row.operator("object.arcada_corta_sup", text="Configura Arcada Superior", icon="TRIA_UP")

        row = layout.row()
        row.operator("object.arcada_corta_inf", text="Configura Arcada Inferior", icon="TRIA_DOWN")

        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.label(text="Configuração Manual:")


        row = layout.row()
        row.operator("cut_mesh.polytrim", text="Desenha Cortes", icon="OUTLINER_DATA_MESH")


        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.label(text="Setup dos Dentes:")

        row = layout.row()
        row.operator("object.importa_alinha_arcada", text="Referências de Alinhamento", icon="CURVE_PATH")
        
        row = layout.row()
        row.label(text=" ")

        row = layout.row()
        row.label(text="Dinâmica dos Dentes:")
        row = layout.row()
        row.operator("screen.frame_jump", text="Inicio", icon="REW").end=False
        row.operator("screen.animation_play", text="", icon="PLAY_REVERSE").reverse=True
        row.operator("anim.animalocrot", text="", icon="CLIP")
        row.operator("screen.animation_play", text="", icon="PLAY")
        row.operator("screen.frame_jump", text="Final", icon="FF").end=True        
        
    
def register():
    bpy.utils.register_class(liberGeraModelosTomoArc)
    bpy.utils.register_class(ImportaCorte)
    bpy.utils.register_class(AlinhaArcada2)
    bpy.utils.register_class(ImportaAlinhaArcada)
#    bpy.utils.register_class(liberRotacionaY)
    bpy.utils.register_class(liberFlipY)    
    bpy.utils.register_class(liberGeraModeloFoto)
    bpy.utils.register_class(arcadaCortaSup)
    bpy.utils.register_class(arcadaCortaInf)
    bpy.utils.register_class(liberCriaFotogrametria)
    bpy.utils.register_class(liberBotoesArcada)

    
def unregister():
    bpy.utils.unregister_class(liberGeraModelosTomoArc)
    bpy.utils.unregister_class(ImportaCorteSup)
    bpy.utils.register_class(arcadaCortaInf)
    bpy.utils.unregister_class(AlinhaArcada2)
    bpy.utils.unregister_class(ImportaAlinhaArcada)
#    bpy.utils.unregister_class(liberRotacionaY)
    bpy.utils.unregister_class(liberFlipY)    
    bpy.utils.unregister_class(liberGeraModeloFoto)
    bpy.utils.unregister_class(arcadaCorta)
    bpy.utils.unregister_class(liberCriaFotogrametria)
    bpy.utils.unregister_class(liberBotoesArcada)
        
if __name__ == "__main__":
    register()
