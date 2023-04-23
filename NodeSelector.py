import bpy
import time
from bpy.props import (
    StringProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    BoolProperty,
)




bl_info = {
    "name": "OJST node selector",
    "author": "OJST",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "ノードエディタ > Sidebar",
    "description": "ノードを英語/日本語で検索して追加する",
    "warning": "",
    "support": "COMMUNITY",
    "doc_url": "",
    "tracker_url": "",
    "category": "User Interface"
}

shader_node_list = [
    ["Ambient Occlusion", "アンビエントオクルージョン", "ShaderNodeAmbientOcclusion"],
    ["Attribute", "属性", "ShaderNodeAttribute"],
    ["Bevel", "ベベル", "ShaderNodeBevel"],
    ["Camera Data", "カメラデータ", "ShaderNodeCameraData"],
    ["Color Attribute", "カラー属性", "ShaderNodeVertexColor"],
    ["Curves Info", "カーブ情報", "ShaderNodeHairInfo"],
    ["Fresnel", "フレネル", "ShaderNodeFresnel"],
    ["Geometry", "ジオメトリ", "ShaderNodeNewGeometry"],
    ["Layer Weight", "レイヤーウェイト", "ShaderNodeLayerWeight"],
    ["Light Path", "ライトパス", "ShaderNodeLightPath"],
    ["Object Info", "オブジェクト情報", "ShaderNodeObjectInfo"],
    ["Particle Info", "パーティクル情報", "ShaderNodeParticleInfo"],
    ["Point Info", "ポイント情報", "ShaderNodePointInfo"],
    ["RGB", "RGB", "ShaderNodeRGB"],
    ["Tangent", "タンジェント", "ShaderNodeTangent"],
    ["Texture Coordinate", "テクスチャ座標", "ShaderNodeTexCoord"],
    ["UV Map", "UVマップ", "ShaderNodeUVMap"],
    ["Value", "値", "ShaderNodeValue"],
    ["Volume Info", "ボリューム情報", "ShaderNodeValue"],
    ["Wireframe", "ワイヤーフレーム", "ShaderNodeWireframe"],
    ["AOV Output", "AOV出力", "ShaderNodeWireframe"],
    ["Material", "マテリアル出力", "ShaderNodeWireframe"],
    ["Light", "ライト出力", "ShaderNodeOutputLight"],
    ["Workd Output", "ワールド出力", "ShaderNodeOutputWorld"],
    ["Add Shader", "シェーダー加算", "ShaderNodeAddShader"],
    ["Anisotropic BSDF", "異方性BSDF", "ShaderNodeBsdfAnisotropic"],
    ["Background", "背景", "ShaderNodeBackground"],
    ["Diffuse BSDF", "ディフューズBSDF", "ShaderNodeBsdfDiffuse"],
    ["Emission", "放射", "ShaderNodeEmission"],
    ["Glass", "グラス BSDF", "ShaderNodeBsdfGlass"],
    ["Glossy BSDF", "光沢BSDF", "ShaderNodeBsdfGlossy"],
    ["Hair BSDF", "ヘアーBSDF", "ShaderNodeBsdfHair"],
    ["Holdout", "ホールドアウト", "ShaderNodeHoldout"],
    ["Mix Shader", "シェーダーミックス", "ShaderNodeAddShader"],
    ["Principled BSDF", "プリンシプルBSDF", "ShaderNodeBsdfPrincipled"],
    ["Principled Hair BSDF", "プリンシプルヘアーBSDF", "ShaderNodeBsdfHairPrincipled"],
    ["Principled Volume", "プリンシプルボリューム", "ShaderNodeAddShader"],
    ["Refraction", "屈折 BSDF", "ShaderNodeBsdfRefraction"],
    ["ShaderNodeBsdfGlossy", "スペキュラーBSDF", "ShaderNodeEeveeSpecular"],
    ["Subsurface Scattering", "SSS", "ShaderNodeSubsurfaceScattering"],
    ["Toon BSDF", "トーンBSDF", "ShaderNodeBsdfToon"],
    ["Translucent BSDF", "半透明BSDF", "ShaderNodeBsdfTranslucent"],
    ["Transparent BSDF", "透過BSDF", "ShaderNodeBsdfTransparent"],
    ["Velvet BSDF", "ベルベットBSDF", "ShaderNodeBsdfVelvet"],
    ["Volume Absorption", "ボリュームの吸収", "ShaderNodeSubsurfaceScattering"],
    ["Volume Scatter", "ボリュームの散乱", "ShaderNodeSubsurfaceScattering"],
    ["Brick Texture", "レンガテクスチャ ", "ShaderNodeTexBrick"],
    ["Checker Texture", "チェッカーテクスチャ", "ShaderNodeTexChecker"],
    ["Environment Texture", "環境テクスチャ", "ShaderNodeTexEnvironment"],
    ["Gradient Texture", "グラデーションテクスチャ", "ShaderNodeTexGradient"],
    ["IES Texture", "IESテクスチャ", "ShaderNodeTexIES"],
    ["Image Texture", "画像テクスチャ", "ShaderNodeTexImage"],
    ["Magic Texture", "マジックテクスチャ", "ShaderNodeTexMagic"],
    ["Musgrave Texture", "マスグレイブテクスチャ", "ShaderNodeTexMusgrave"],
    ["Noise Texture", "ノイズテクスチャ", "ShaderNodeTexNoise"],
    ["Point Density", "点密度", "ShaderNodeTexPointDensity"],
    ["Sky Texture", "大気テクスチャ", "ShaderNodeTexSky"],
    ["Voronoi Texture", "ボロノイテクスチャ", "ShaderNodeTexVoronoi"],
    ["Wave Texture", "波テクスチャ", "ShaderNodeTexWave"],
    ["White Noise Texture ", "ホワイトノイズテクスチャ", "ShaderNodeTexWhiteNoise"],
    ["Bright/Contrast", "明暗コントラスト", "ShaderNodeBrightContrast"],
    ["Gamma", "ガンマ", "ShaderNodeGamma"],
    ["Hue Saturation Value", "HSV(色相/彩度/輝度)", "ShaderNodeHueSaturation"],
    ["Invert", "反転", "ShaderNodeInvert"],
    ["Light Falloff", "光の減衰", "ShaderNodeLightFalloff"],
    ["Mix", "カラーミックス", "ShaderNodeMix"],
    ["RGB Curves", "RGBカーブ", "ShaderNodeRGBCurve"],
    ["Bump", "バンプ", "ShaderNodeBump"],
    ["Displacement", "ディスプレイスメント", "ShaderNodeDisplacement"],
    ["Mapping", "マッピング", "ShaderNodeMapping"],
    ["Normal", "ノーマル", "ShaderNodeNormal"],
    ["Normal Map", "ノーマルマップ", "ShaderNodeNormalMap"],
    ["Vector Curves", "ベクターカーブ", "ShaderNodeVectorCurve"],
    ["Vector Displacement", "ベクトルディスプレイスメント", "ShaderNodeVectorDisplacement"],
    ["Vector Rotate", "ベクトル回転", "ShaderNodeVectorRotate"],
    ["Vector Transform", "ベクトル変換", "ShaderNodeVectorTransform"],
    ["Blackbody", "黒体", "ShaderNodeBlackbody"],
    ["Clamp", "範囲制限", "ShaderNodeClamp"],
    ["Color Ramp", "カラーランプ", "ShaderNodeValToRGB"],
    ["Combine Color", "カラー合成", "ShaderNodeCombineColor"],
    ["Combine XYZ", "XYZ合成", "ShaderNodeCombineXYZ"],
    ["Float Curve", "Floatカーブ", "ShaderNodeFloatCurve"],
    ["Map Range", "範囲マッピング", "ShaderNodeMapRange"],
    ["Math", "数式", "ShaderNodeMath"],
    ["Mix", "ミックス", "ShaderNodeMix"],
    ["RGB to BW", "RGBのBW化", "ShaderNodeRGBToBW"],
    ["Separate Color", "カラー分離", "ShaderNodeSeparateColor"],
    ["Separate XYZ", "XYZ分離", "ShaderNodeSeparateXYZ"],
    ["Shader To RGB", "シェーダーのRGB化", "ShaderNodeVectorMath"],
    ["Vector Math", "ベクトル演算", "ShaderNodeVectorMath"],
    ["Wavelength", "波長", "ShaderNodeScript"],
    ["Script", "スクリプト", ""],
#    ["Make Group", "グループ作成", ""],
#    ["Ungroup", "グループ解除", ""],
]
shader_name_list = []


geometory_node_list = [
["Attribute Statistic", "属性統計", "GeometryNodeAttributeStatistic"],
["Domain Size", "ドメインサイズ", "GeometryNodeAttributeDomainSize"],
["Blur Attribute", "属性ブラー", "GeometryNodeBlurAttribute"],
["Capture Attribute", "属性キャプチャ", "GeometryNodeCaptureAttribute"],
["Remove Named Attribute", "名前付き属性削除", "GeometryNodeRemoveAttribute"],
["Store Named Attribute", "名前付き属性格納", "GeometryNodeStoreNamedAttribute"],
["Boolean", "ブーリアン", "FunctionNodeInputBool"],
["Color", "カラー", "FunctionNodeInputColor"],
["Image", "画像", "GeometryNodeInputImage"],
["Integer", "整数", "FunctionNodeInputInt"],
["Material", "マテリアル", "GeometryNodeInputMaterial"],
["String", "文字列", "FunctionNodeInputString"],
["Value", "値", "ShaderNodeValue"],
["Vector", "ベクトル", "FunctionNodeInputVector"],
["Group Input", "グループ入力", "NodeGroupInput"],
["Collection Info", "コレクション情報", "GeometryNodeCollectionInfo"],
["Image Info", "画像情報", "GeometryNodeImageInfo"],
["Is Viewport", "ビューポートフラグ", "GeometryNodeIsViewport"],
["Object Info", "オブジェクト情報", "GeometryNodeObjectInfo"],
["Self Object", "オブジェクト自身", "GeometryNodeSelfObject"],
["Scene Time", "シーンタイム", "GeometryNodeInputSceneTime"],
["Group Output", "グループ出力", "NodeGroupOutput"],
["Viewer", "ビューアー", "GeometryNodeViewer"],
["ID", "ID", "GeometryNodeInputID"],
["Index", "インデックス", "GeometryNodeInputIndex"],
["Named Attribute", "名前付き属性", "GeometryNodeInputNamedAttribute"],
["Normal", "ノーマル", "GeometryNodeInputNormal"],
["Position", "位置", "GeometryNodeInputPosition"],
["Radius", "半径", "GeometryNodeInputRadius"],
["Geometry Proximity", "ジオメトリ近接", "GeometryNodeProximity"],
["Raycast", "レイキャスト", "GeometryNodeRaycast"],
["Sample Index ", "インデックスサンプル", "GeometryNodeSampleIndex"],
["Sample Nearest ", "最近接サンプル", "GeometryNodeSampleNearest"],
["Set ID", "ID設定", "GeometryNodeSetID"],
["Set Position", "位置設定", "GeometryNodeSetPosition"],
["Bounding Box", "バウンディングボックス", "GeometryNodeBoundBox"],
["Convex Hull", "凸包", "GeometryNodeConvexHull"],
["Delete Geometry", "ジオメトリ削除", "GeometryNodeDeleteGeometry"],
["Duplicate Elements", "要素コピー", "GeometryNodeDuplicateElements"],
["Merge by Distance", "距離でマージ", "GeometryNodeMergeByDistance"],
["Transform", "ジオメトリをトランスフォーム", "GeometryNodeTransform"],
["Separate Components", "成分分離", "GeometryNodeSeparateComponents"],
["Separate Geometry", "ジオメトリ分離", "GeometryNodeSeparateGeometry"],
["Join Geometry", "ジオメトリ統合", "GeometryNodeJoinGeometry"],
["Geometry to Instance", "ジオメトリのインスタンス化", "GeometryNodeGeometryToInstance"],
["Curve Handle Position", "カーブハンドル位置", "GeometryNodeInputCurveHandlePositions"],
["Curve Length", "カーブ長", "GeometryNodeCurveLength"],
["Curve Tangent", "カーブタンジェント", "GeometryNodeInputTangent"],
["Curve Tilt", "カーブ傾き", "GeometryNodeInputCurveTilt"],
["Endpoint Selection", "端を選択", "GeometryNodeCurveEndpointSelection"],
["Handle Type Selection", "ハンドルタイプ選択", "GeometryNodeCurveHandleTypeSelection"],
["Is Spline Cyclic", "スプラインループフラグ", "GeometryNodeInputSplineCyclic"],
["Spline Length", "スプライン長さ", "GeometryNodeSplineLength"],
["Spline Parameter", "スプラインパラメーター", "GeometryNodeSplineParameter"],
["Spline Resolution", "スプライン解像度", "GeometryNodeInputSplineResolution"],
["Sample Curve", "カーブサンプル", "GeometryNodeSampleCurve"],
["Set Curve Normal ", "カーブ法線設定", "GeometryNodeSetCurveNormal"],
["Set Curve Radius", "カーブ半径設定", "GeometryNodeSetCurveRadius"],
["Set Curve Tilt", "カーブ傾き設定", "GeometryNodeSetCurveTilt"],
["Set Handle Positions", "ハンドル位置設定", "GeometryNodeCurveEndpointSelection"],
["Set Handle Type", "ハンドルタイプ設定", "GeometryNodeCurveHandleTypeSelection"],
["Set Spline Cyclic", "スプラインループ設定", "GeometryNodeSetSplineCyclic"],
["Set Spline Resolution", "スプライン解像度設定", "GeometryNodeSetSplineResolution"],
["Set Spline Type", "スプラインタイプ設定", "GeometryNodeCurveSplineType"],
["Curve to Mesh", "カーブのメッシュ化", "GeometryNodeCurveToMesh"],
["Curve to Points", "カーブのポイント化", "GeometryNodeCurveToPoints"],
["Deform Curves on Surface ", "表面のカーブ変形", "GeometryNodeDeformCurvesOnSurface"],
["Fill Curve", "カーブフィル", "GeometryNodeFillCurve"],
["Fillet Curve", "カーブ角丸", "GeometryNodeFilletCurve"],
["Fill Curve", "カーブ補完", "GeometryNodeInterpolateCurves"],
["Resample Curve", "カーブりサンプル", "GeometryNodeResampleCurve"],
["Reverse Curve", "カーブ反転", "GeometryNodeReverseCurve"],
["Subdivide Curve", "カーブ細分化", "GeometryNodeSubdivideCurve"],
["Trim Curve", "カーブトリム", "GeometryNodeTrimCurve"],
["Arc", "弧", "GeometryNodeCurveArc"],
["Bézier Segment", "ベジエセグメント", "GeometryNodeCurvePrimitiveBezierSegment"],
["Curve Circle", "カーブ円", "GeometryNodeCurvePrimitiveCircle"],
["Curve Line", "カーブライン", "GeometryNodeCurvePrimitiveLine"],
["Curve Spiral", "カーブスパイラル", "GeometryNodeCurveSpiral"],
["Quadratic Bézier", "二次ベジエ", "GeometryNodeCurveQuadraticBezier"],
["Quadrilateral", "四角形", "GeometryNodeCurvePrimitiveQuadrilateral"],
["Star", "スター", "GeometryNodeCurveStar"],
["Curve of Point ", "カーブ内ポイントオフセット", "GeometryNodeOffsetPointInCurve"],
["Offset Point in Curve ", "ポイントのカーブ", "GeometryNodeCurveOfPoint"],
["Points of Curve ", "カーブのポイント", "GeometryNodePointsOfCurve"],
["Instance on Points", "ポイントにインスタンス作成", "GeometryNodeInstanceOnPoints"],
["Instances to Points", "インスタンスのポイント化", "GeometryNodeInstancesToPoints"],
["Realize Instances", "インスタンス実体化", "GeometryNodeRealizeInstances"],
["Rotate Instances", "インスタンス回転", "GeometryNodeRotateInstances"],
["Scale Instances", "インスタンス拡大縮小", "GeometryNodeScaleInstances"],
["Translate Instances", "インスタンスを移動", "GeometryNodeTranslateInstances"],
["Instance Rotation", "インスタンスの回転", "GeometryNodeInputInstanceRotation"],
["Instance Scale", "インスタンスのスケール", "GeometryNodeInputInstanceScale"],
["Edge Angle ", "辺の角度", "GeometryNodeInputMeshEdgeAngle"],
["Edge Neighbors ", "辺の共有面数", "GeometryNodeInputMeshEdgeNeighbors"],
["Edge Vertices ", "辺の頂点", "GeometryNodeInputMeshEdgeVertices"],
["Edges to Face Groups", "辺の面グループ化", "GeometryNodeEdgesToFaceGroups"],
["Face Area ", "面積", "GeometryNodeInputMeshFaceArea"],
["Face Neighbors ", "面情報", "GeometryNodeInputMeshFaceNeighbors"],
["Face Group Boundaries", "面グループ境界", "GeometryNodeMeshFaceSetBoundaries"],
["Is Face Planar ", "平面判定", "GeometryNodeInputMeshFaceIsPlanar"],
["Is Shade Smooth ", "スムーズシェードフラグ", "GeometryNodeInputShadeSmooth"],
["Mesh Island ", "メッシュアイランド", "GeometryNodeInputMeshIsland"],
["Shortest Edge Paths ", "最短辺パス", "GeometryNodeInputShortestEdgePaths"],
["Vertex Neighbors ", "頂点情報", "GeometryNodeInputMeshVertexNeighbors"],
["Shortest Edge Paths ", "最短辺パス", "GeometryNodeSampleNearestSurface"],
["Sample UV Surface ", "UV表面サンプル", "GeometryNodeSampleUVSurface"],
["Set Shade Smooth ", "スムーズシェード設定", "GeometryNodeSetShadeSmooth"],
["Dual Mesh ", "デュアルメッシュ", "GeometryNodeDualMesh"],
["Edge Paths to Curves ", "辺パスのカーブ化", "GeometryNodeEdgePathsToCurves"],
["Edge Paths to Selection ", "辺パスの選択化", "GeometryNodeEdgePathsToSelection"],
["Extrude Mesh ", "メッシュ押し出し", "GeometryNodeExtrudeMesh"],
["Flip Faces ", "面反転", "GeometryNodeFlipFaces"],
["Mesh Boolean ", "メッシュブーリアン", "GeometryNodeMeshBoolean"],
["Mesh to Curve ", "メッシュのカーブ化", "GeometryNodeMeshToCurve"],
["Mesh to Points ", "メッシュのポイント化", "GeometryNodeMeshToPoints"],
["Mesh to Volume ", "メッシュのボリューム化", "GeometryNodeMeshToVolume"],
["Scale Elements ", "要素スケール", "GeometryNodeScaleElements"],
["Split Edges ", "辺分離", "GeometryNodeSplitEdges"],
["Subdivide Mesh ", "メッシュ細分化", "GeometryNodeSubdivideMesh"],
["Subdivision Surface ", "サブディビジョンサーフェス", "GeometryNodeSubdivisionSurface"],
["Triangulate ", "三角面化", "GeometryNodeTriangulate"],
["Cone ", "円錐", "GeometryNodeMeshCone"],
["Cube ", "立方体", "GeometryNodeMeshCube"],
["Cylinder ", "円柱", "GeometryNodeMeshCylinder"],
["Grid ", "グリッド", "GeometryNodeMeshGrid"],
["Icosphere ", "ICO球", "GeometryNodeMeshIcoSphere"],
["Mesh Circle ", "メッシュ円", "GeometryNodeMeshCircle"],
["Mesh Line ", "メッシュライン", "GeometryNodeMeshLine"],
["UV Sphere ", "UV球", "GeometryNodeMeshUVSphere"],
["Corners of Face Node", "面のコーナー", "GeometryNodeCornersOfFace"],
["Corners of Vertex Node", "頂点のコーナー", "GeometryNodeCornersOfVertex"],
["Edges of Corner Node", "コーナーの両辺", "GeometryNodeEdgesOfCorner"],
["Edges of Vertex Node", "頂点の辺", "GeometryNodeEdgesOfVertex"],
["Face of Corner Node", "コーナーの面", "GeometryNodeFaceOfCorner"],
["Offset Corner in Face Node", "面内コーナーオフセット", "GeometryNodeOffsetCornerInFace"],
["Vertex of Corner Node", "コーナーの頂点", "GeometryNodeVertexOfCorner"],
["Pack UV Islands ", "UVアイランド梱包", "GeometryNodeUVPackIslands"],
["UV Unwrap ", "UV展開", "GeometryNodeUVUnwrap"],
["Distribute Points in Volume", "ボリュームにポイント配置", "GeometryNodeDistributePointsInVolume"],
["Distribute Points on Faces", "面にポイント配置", "GeometryNodeDistributePointsOnFaces"],
["Points ", "ポイント", "GeometryNodePoints"],
["Points to Vertices ", "ポイントの頂点化", "GeometryNodePointsToVertices"],
["Points to Volume ", "ポイントのボリューム化", "GeometryNodePointsToVolume"],
["Set Point Radius ", "ポイント半径設定", "GeometryNodeSetPointRadius"],
["Volume Cube ", "ボリューム立方体", "GeometryNodeVolumeCube"],
["Volume to Mesh ", "ボリュームのメッシュ化", "GeometryNodeVolumeToMesh"],
["Replace Material ", "マテリアル置換", "GeometryNodeReplaceMaterial"],
["Material Index ", "マテリアルインデックス", "GeometryNodeInputMaterialIndex"],
["Material Selection ", "マテリアルで選択", "GeometryNodeMaterialSelection"],
["Set Material ", "マテリアル設定", "GeometryNodeSetMaterial"],
["Set Material Index ", "マテリアルインデックス設定", "GeometryNodeSetMaterialIndex"],
["Brick Texture", "レンガテクスチャ ", "ShaderNodeTexBrick"],
["Checker Texture", "チェッカーテクスチャ", "ShaderNodeTexChecker"],
["Gradient Texture", "グラデーションテクスチャ", "ShaderNodeTexGradient"],
["Image Texture", "画像テクスチャ", "GeometryNodeImageTexture"],
["Magic Texture", "マジックテクスチャ", "ShaderNodeTexMagic"],
["Musgrave Texture", "マスグレイブテクスチャ", "ShaderNodeTexMusgrave"],
["Noise Texture", "ノイズテクスチャ", "ShaderNodeTexNoise"],
["Voronoi Texture", "ボロノイテクスチャ", "ShaderNodeTexVoronoi"],
["Wave Texture", "波テクスチャ", "ShaderNodeTexWave"],
["White Noise Texture ", "ホワイトノイズテクスチャ", "ShaderNodeTexWhiteNoise"],
["Color Ramp", "カラーランプ", "ShaderNodeValToRGB"],
["RGB Curves", "RGBカーブ", "ShaderNodeRGBCurve"],
["Combine Color", "カラー合成", "FunctionNodeCombineColor"],
["MixRGB", "カラーミックス", "ShaderNodeMix"],
["Separate Color", "カラー分離", "FunctionNodeSeparateColor"],
["Join Strings ", "文字列結合", "GeometryNodeStringJoin"],
["Replace String ", "文字列置換", "FunctionNodeReplaceString"],
["Slice String ", "文字列スライス", "FunctionNodeSliceString"],
["String Length ", "文字列長", "FunctionNodeStringLength"],
["String to Curves ", "文字列のカーブ化", "GeometryNodeStringToCurves"],
["Value to String ", "値の文字列化", "FunctionNodeValueToString"],
["Special Characters ", "特殊文字", "FunctionNodeInputSpecialCharacters"],
["Vector Curves", "ベクターカーブ", "ShaderNodeVectorCurve"],
["Vector Math", "ベクトル演算", "ShaderNodeVectorMath"],
["Vector Rotate", "ベクトル回転", "ShaderNodeVectorRotate"],
["Combine XYZ", "XYZ合成", "ShaderNodeCombineXYZ"],
["Mix", "ベクトルミックス", "ShaderNodeMix"],
["Separate XYZ", "XYZ分離", "ShaderNodeSeparateXYZ"],
["Accumulate Field ", "フィールド蓄積", "GeometryNodeAccumulateField"],
["Evaluate at Index Node", "インデックスでの強化", "GeometryNodeFieldAtIndex"],
["Evaluate on Domain Node", "ドメインでの評価", "GeometryNodeFieldOnDomain"],
["Boolean Math ", "ブール演算", "FunctionNodeBooleanMath"],
["Clamp", "範囲制限", "ShaderNodeClamp"],
["Compare ", "比較", "FunctionNodeCompare"],
["Field at Index ", "インデックスからフィールド", ""],
["Float Curve", "Floatカーブ", "ShaderNodeFloatCurve"],
["Float To Integer ", "Floatの整数化", "ShaderNodeFloatCurve"],
["Interpolate Domain ", "ドメイン補完", "FunctionNodeFloatToInt"],
["Map Range", "範囲マッピング", "ShaderNodeMapRange"],
["Math", "数式", "ShaderNodeMath"],
["Mix", "ミックス", "ShaderNodeMix"],
["Align Euler to Vector ", "オイラーをベクトルに整列", "FunctionNodeAlignEulerToVector"],
["Rotate Euler ", "オイラー回転", "FunctionNodeRotateEuler"],
["Random Value", "ランダム値", "FunctionNodeRandomValue"],
["Switch", "スイッチ", "GeometryNodeSwitch"],
]

geometory_name_list = []


# ノード名の入力確定
def update_text_input(self, context):
        input_text = bpy.context.scene.ojst_prop_nodename
        print(f"Input text = {input_text}")

        name = bpy.context.scene.ojst_prop_nodename
        print(f"Add!  {name}")


        name_list = None
        node_list = None
        if (context.area.ui_type == "GeometryNodeTree"):
            name_list = geometory_name_list
            node_list = geometory_node_list
        elif (context.area.ui_type == "ShaderNodeTree"):
            name_list = shader_name_list
            node_list = shader_node_list
        else:
            return []

        # 選択されている名前を探す
        node_name = None
        for i in range(len(name_list)):
            if (name_list[i] == name):
                node_name = node_list[i][2]

                new_node = bpy.ops.node.add_node(type=node_name, use_transform=True)
                active_node = context.active_node
                pos = (active_node.location.x - active_node.width - 100, active_node.location.y)
                return bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')
                break
        return 'FINISHED'



# search= で指定できる
# 自動的にreturn のリストから選択する。
# ただし、
def search_text_input(self, context,edit_text):
        print(f"Edit text = {edit_text}")
        print(f"ui_type = {context.area.ui_type}")

        if (context.area.ui_type == "GeometryNodeTree"):
            return geometory_name_list
        elif (context.area.ui_type == "ShaderNodeTree"):
            return shader_name_list
        else:
            return []



class OJSTSNS_OT_Add_Callback(bpy.types.Operator):

    bl_idname = "object.ojst_sns_add_callback"
    bl_label = "Add"
    bl_description = "Add node"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        name = bpy.context.scene.ojst_prop_nodename
        print(f"Add!  {name}")

        name_list = None
        node_list = None
        if (context.area.ui_type == "GeometryNodeTree"):
            name_list = geometory_name_list
            node_list = geometory_node_list
        elif (context.area.ui_type == "ShaderNodeTree"):
            name_list = shader_name_list
            node_list = shader_node_list
        else:
            return []

        # チェック
        # for i in range(len(node_list)):
        #     try:
        #         node_name = node_list[i][2]
        #         new_node = bpy.ops.node.add_node(type=node_name, use_transform=False)

        #     except Exception:
        #         print(f"{node_name} not found.  {node_list[i][1]}")


        # 選択されている名前を探す
        node_name = None
        for i in range(len(name_list)):
            if (name_list[i] == name):
                node_name = node_list[i][2]

                new_node = bpy.ops.node.add_node(type=node_name, use_transform=True)
                active_node = context.active_node
                pos = (active_node.location.x - active_node.width - 100, active_node.location.y)
                break
        return bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')
        #return {'FINISHED'}


class OJSTSNS_OT_Fab_Callback(bpy.types.Operator):

    bl_idname = "object.ojst_sns_fab_callback"
    bl_label = "Add"
    bl_description = "Add node"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print(f"Fab!  {bpy.context.scene.ojst_prop_nodename}")
        return {'FINISHED'}



# Sidebarのタブ [カスタムタブ] に、パネル [カスタムパネル] を追加
class OJSTSNS_PT_CustomPanel(bpy.types.Panel):

    bl_label = "Node selector"         # パネルのヘッダに表示される文字列
    bl_space_type = 'NODE_EDITOR'           # パネルを登録するスペース
    bl_region_type = 'UI'               # パネルを登録するリージョン
    bl_category = "Node selector"        # パネルを登録するタブ名
    bl_context = "objectmode"           # パネルを表示するコンテキスト

    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # オブジェクトが選択されているときのみメニューを表示させる
        for o in bpy.data.objects:
            if o.select_get():
                return True
        return False

    # ヘッダーのカスタマイズ
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PLUGIN')


    # メニューの描画処理
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # 検索用テキストボックスを追加
        layout.prop(scene, "ojst_prop_nodename", text="")

        # ノード追加
        layout.operator(OJSTSNS_OT_Add_Callback.bl_idname, text="Add")


# プロパティの初期化
def init_props():

    print("init")
    scene = bpy.types.Scene
    scene.ojst_prop_nodename = StringProperty(
        name="NodeName",
        description="Node name",
        default="",
        options= {"TEXTEDIT_UPDATE"},
        update=update_text_input,
        search=search_text_input
    )

# プロパティを削除
def clear_props():
    scene = bpy.types.Scene


classes = [
    OJSTSNS_OT_Add_Callback,
    OJSTSNS_PT_CustomPanel
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    init_props()

    # シェーダーノードリスト初期化
    for sd in shader_node_list:
        n = f"{sd[0]} / {sd[1]}"
        shader_name_list.append(n)

    # ジオメトリノードリスト初期化
    for sd in geometory_node_list:
        n = f"{sd[0]} / {sd[1]}"
        geometory_name_list.append(n)

    print("OJST Node selector activated.")


def unregister():
    clear_props()
    for c in classes:
        bpy.utils.unregister_class(c)
    print("OJST Node selector deactivated.")


if __name__ == "__main__":
    register()