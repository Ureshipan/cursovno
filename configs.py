import math

# Параметры геометрии по умолчанию
DEFAULT_PARAMS = {
    'L': 460,        # Длина канала
    'l_top': 80,     # Длина выходного участка
    'l_bot': 70,     # Длина входного участка
    'w_top': 220,    # Ширина выходного участка
    'w_mid': 80,     # Ширина среднего участка
    'w_bot': 300,    # Ширина входного участка
    'a_top': 90,     # Угол выходной воронки
    'a_bot': 120,    # Угол входной воронки
    'D': 25,         # Диаметр цилиндров
    'endTime': 10,   # Время расчета
    'writeInterval': 1  # Интервал записи
}

# Список вершин для blockMeshDict
VERTICES = [
    (-110, 238.2457, 5),    # 0
    (110, 238.2457, 5),     # 1
    (110, 158.2457, 5),     # 2
    (40, 88.2457, 5),       # 3
    (40, 61.2457, 5),       # 4
    (40, -61.2457, 5),      # 5
    (40, -88.2457, 5),      # 6
    (150, -151.7543, 5),    # 7
    (150, -221.7543, 5),    # 8
    (-150, -221.7543, 5),   # 9
    (-150, -151.7543, 5),   # 10
    (-40, -88.2457, 5),     # 11
    (-40, -61.2457, 5),     # 12
    (-40, 61.2457, 5),      # 13
    (-40, 88.2457, 5),      # 14
    (-110, 158.2457, 5),    # 15
    (-8.8388, 83.6836, 5),  # 16
    (8.8388, 83.6836, 5),   # 17
    (8.8388, 65.9069, 5),   # 18
    (-8.8388, 65.9069, 5),  # 19
    (-8.8388, -65.9069, 5), # 20
    (8.8388, -65.9069, 5),  # 21
    (8.8388, -83.6836, 5),  # 22
    (-8.8388, -83.6836, 5), # 23
    (-110, 238.2457, -5),   # 24
    (110, 238.2457, -5),    # 25
    (110, 158.2457, -5),    # 26
    (40, 88.2457, -5),      # 27
    (40, 61.2457, -5),      # 28
    (40, -61.2457, -5),     # 29
    (40, -88.2457, -5),     # 30
    (150, -151.7543, -5),   # 31
    (150, -221.7543, -5),   # 32
    (-150, -221.7543, -5),  # 33
    (-150, -151.7543, -5),  # 34
    (-40, -88.2457, -5),    # 35
    (-40, -61.2457, -5),    # 36
    (-40, 61.2457, -5),     # 37
    (-40, 88.2457, -5),     # 38
    (-110, 158.2457, -5),   # 39
    (-8.8388, 83.6836, -5), # 40
    (8.8388, 83.6836, -5),  # 41
    (8.8388, 65.9069, -5),  # 42
    (-8.8388, 65.9069, -5), # 43
    (-8.8388, -65.9069, -5),# 44
    (8.8388, -65.9069, -5), # 45
    (8.8388, -83.6836, -5), # 46
    (-8.8388, -83.6836, -5) # 47
]


def recalculate_vertices(params):
    global VERTICES
    L = params['L']
    l_top = params['l_top']
    l_bot = params['l_bot']
    w_top = params['w_top']
    w_mid = params['w_mid']
    w_bot = params['w_bot']
    a_top = params['a_top']
    a_bot = params['a_bot']
    D = params['D']

    vor_top = abs(1/math.tan(a_top / 2 * math.pi / 180) * (w_top - w_mid) / 2)
    vor_bot = abs(1/math.tan(a_bot / 2 * math.pi / 180) * (w_bot - w_mid) / 2)
    l_mid = L - l_top - l_bot - vor_top - vor_bot
    sq_crcl = D / math.sqrt(2) / 2

    height = 30

    VERTICES = [
        (-w_top/2, l_top + vor_top + l_mid / 2, height/2),    # 0
        (w_top/2, l_top + vor_top + l_mid / 2, height/2),     # 1
        (w_top/2, vor_top + l_mid / 2, height/2),     # 2
        (w_mid/2, l_mid/2, height/2),       # 3
        (w_mid/2, l_mid/2 - w_mid, height/2),       # 4
        (w_mid/2, -(l_mid/2 - w_mid), height/2),      # 5
        (w_mid/2, -l_mid/2, height/2),      # 6
        (w_bot/2, -(l_mid/2 + vor_bot), height/2),    # 7
        (w_bot/2, -(l_bot + vor_bot + l_mid / 2), height/2),    # 8
        (-w_bot/2, -(l_bot + vor_bot + l_mid / 2), height/2),   # 9
        (-w_bot/2, -(l_mid/2 + vor_bot), height/2),   # 10
        (-w_mid/2, -l_mid/2, height/2),     # 11
        (-w_mid/2, -(l_mid/2 - w_mid), height/2),     # 12
        (-w_mid/2, l_mid/2 - w_mid, height/2),      # 13
        (-w_mid/2, l_mid/2, height/2),      # 14
        (-w_top/2, vor_top + l_mid / 2, height/2),    # 15
        (-sq_crcl, l_mid/2 - w_mid / 2 + sq_crcl, height/2),  # 16
        (sq_crcl, l_mid/2 - w_mid / 2 + sq_crcl, height/2),   # 17
        (sq_crcl, l_mid/2 - w_mid / 2 - sq_crcl, height/2),   # 18
        (-sq_crcl, l_mid/2 - w_mid / 2 - sq_crcl, height/2),  # 19
        (-sq_crcl, -(l_mid/2 - w_mid / 2 - sq_crcl), height/2), # 20
        (sq_crcl, -(l_mid/2 - w_mid / 2 - sq_crcl), height/2),  # 21
        (sq_crcl, -(l_mid/2 - w_mid / 2 + sq_crcl), height/2),  # 22
        (-sq_crcl, -(l_mid/2 - w_mid / 2 + sq_crcl), height/2), # 23
        (-w_top/2, l_top + vor_top + l_mid / 2, -height/2),   # 24
        (w_top/2, l_top + vor_top + l_mid / 2, -height/2),    # 25
        (w_top/2, vor_top + l_mid / 2, -height/2),    # 26
        (w_mid/2, l_mid/2, -height/2),      # 27
        (w_mid/2, (l_mid/2 - w_mid), -height/2),      # 28
        (w_mid/2, -(l_mid/2 - w_mid), -height/2),     # 29
        (w_mid/2, -l_mid/2, -height/2),     # 30
        (w_bot/2, -(l_mid/2 + vor_bot), -height/2),   # 31
        (w_bot/2, -(l_bot + vor_bot + l_mid / 2), -height/2),   # 32
        (-w_bot/2, -(l_bot + vor_bot + l_mid / 2), -height/2),  # 33
        (-w_bot/2, -(l_mid/2 + vor_bot), -height/2),  # 34
        (-w_mid/2, -l_mid/2, -height/2),    # 35
        (-w_mid/2, -(l_mid/2 - w_mid), -height/2),    # 36
        (-w_mid/2, (l_mid/2 - w_mid), -height/2),     # 37
        (-w_mid/2, l_mid/2, -height/2),     # 38
        (-w_top/2, vor_top + l_mid / 2, -height/2),   # 39
        (-sq_crcl, (l_mid/2 - w_mid / 2 + sq_crcl), -height/2), # 40
        (sq_crcl, (l_mid/2 - w_mid / 2 + sq_crcl), -height/2),  # 41
        (sq_crcl, (l_mid/2 - w_mid / 2 - sq_crcl), -height/2),  # 42
        (-sq_crcl, (l_mid/2 - w_mid / 2 - sq_crcl), -height/2), # 43
        (-sq_crcl, -(l_mid/2 - w_mid / 2 - sq_crcl), -height/2),# 44
        (sq_crcl, -(l_mid/2 - w_mid / 2 - sq_crcl), -height/2), # 45
        (sq_crcl, -(l_mid/2 - w_mid / 2 + sq_crcl), -height/2), # 46
        (-sq_crcl, -(l_mid/2 - w_mid / 2 + sq_crcl), -5) # 47
    ]


def get_vertices_string():
    """Возвращает строку с вершинами для blockMeshDict"""
    vertices_str = "vertices\n(\n"
    for i, (x, y, z) in enumerate(VERTICES):
        vertices_str += f" ({x} {y} {z}) //{i}\n"
    vertices_str += ");\n"
    return vertices_str

def get_control_dict(params):
    """Возвращает controlDict с подставленными параметрами"""
    return f'''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

application     pisoFoam;

startFrom       latestTime;

startTime       0;

stopAt          endTime;

endTime         {params['endTime']};

deltaT          0.001;

writeControl    adjustableRunTime;

writeInterval   {params['writeInterval']};

purgeWrite      0;

writeFormat     ascii;

writePrecision  6;

writeCompression off;

timeFormat      general;

timePrecision   6;

runTimeModifiable yes;

adjustTimeStep  yes;

maxCo           0.5;

// ************************************************************************* //
'''

def get_block_mesh_dict(params):
    """Возвращает blockMeshDict с подставленными параметрами"""
    vertices_str = get_vertices_string()
    return f'''/*--------------------------------*- C++ -*------------------*\\
        =========              |
        \\\\      / F ield      | OpenFOAM: The Open Source CFD Toolbox
         \\\\    / O peration   | Website: https://openfoam.org
          \\\\  / A nd          | Version: 11
           \\\\/ M anipulation  |
\\*---------------------------------------------------------------------------*/

FoamFile
{{
    format ascii;
    class dictionary;
    object blockMeshDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 0.01;

{vertices_str}

blocks
(
    hex (24 39 26 25 0 15 2 1) (10 10 1) simpleGrading (1 1 1) // 1
    hex (39 38 27 26 15 14 3 2) (10 10 1) simpleGrading (1 1 1) // 2
    
    hex (38 40 41 27 14 16 17 3) (10 10 1) simpleGrading (1 1 0.1) // 3
    hex (38 37 43 40 14 13 19 16) (10 10 1) simpleGrading (1 1 0.1) // 4
    hex (41 42 28 27 17 18 4 3) (10 10 1) simpleGrading (1 1 0.1) // 5
    hex (43 37 28 42 19 13 4 18) (10 10 1) simpleGrading (1 1 0.1) // 6
    
    hex (37 36 29 28 13 12 5 4) (10 10 1) simpleGrading (1 1 1) // 7
    
    hex (36 44 45 29 12 20 21 5) (10 10 1) simpleGrading (1 1 0.1) // 8
    hex (36 35 47 44 12 11 23 20) (10 10 1) simpleGrading (1 1 0.1) // 9
    hex (45 46 30 29 21 22 6 5) (10 10 1) simpleGrading (1 1 0.1) // 10
    hex (47 35 30 46 23 11 6 22) (10 10 1) simpleGrading (1 1 0.1) // 11
    
    hex (35 34 31 30 11 10 7 6) (10 10 1) simpleGrading (1 1 1) // 12
    hex (34 33 32 31 10 9 8 7) (10 10 1) simpleGrading (1 1 1) // 13
);

edges
(
    // top circle
 arc 16 17 (0 {(VERTICES[18][1]+VERTICES[17][1]) / 2 + params["D"]/2} {VERTICES[0][2]})
 arc 40 41 (0 {(VERTICES[18][1]+VERTICES[17][1]) / 2 + params["D"]/2} -{VERTICES[0][2]})
 arc 17 18 ({params["D"]/2} {(VERTICES[17][1]+VERTICES[18][1])/2} {VERTICES[0][2]})
 arc 41 42 ({params["D"]/2} {(VERTICES[17][1]+VERTICES[18][1])/2} -{VERTICES[0][2]})
 arc 18 19 (0 {(VERTICES[18][1]+VERTICES[17][1]) / 2 - params["D"]/2} {VERTICES[0][2]})
 arc 42 43 (0 {(VERTICES[18][1]+VERTICES[17][1]) / 2 - params["D"]/2} -{VERTICES[0][2]})
 arc 19 16 (-{params["D"]/2} {(VERTICES[17][1]+VERTICES[18][1])/2} {VERTICES[0][2]})
 arc 43 40 (-{params["D"]/2} {(VERTICES[17][1]+VERTICES[18][1])/2} -{VERTICES[0][2]})
    // bot circle
 arc 22 23 (0 -{(VERTICES[18][1]+VERTICES[17][1]) / 2 + params["D"]/2} {VERTICES[0][2]})
 arc 46 47 (0 -{(VERTICES[18][1]+VERTICES[17][1]) / 2 + params["D"]/2} -{VERTICES[0][2]})
 arc 21 22 ({params["D"]/2} -{(VERTICES[17][1]+VERTICES[18][1])/2} {VERTICES[0][2]})
 arc 45 46 ({params["D"]/2} -{(VERTICES[17][1]+VERTICES[18][1])/2} -{VERTICES[0][2]})
 arc 20 21 (0 -{(VERTICES[18][1]+VERTICES[17][1]) / 2 - params["D"]/2} {VERTICES[0][2]})
 arc 44 45 (0 -{(VERTICES[18][1]+VERTICES[17][1]) / 2 - params["D"]/2} -{VERTICES[0][2]})
 arc 23 20 (-{params["D"]/2} -{(VERTICES[17][1]+VERTICES[18][1])/2} {VERTICES[0][2]})
 arc 47 44 (-{params["D"]/2} -{(VERTICES[17][1]+VERTICES[18][1])/2} -{VERTICES[0][2]})
);

boundary
(
    inlet
    {{
        type patch;
        faces
        (
            (9 33 32 8)
        );
    }}
    outlet
    {{
        type patch;
        faces
        (
            (0 24 25 1)
        );
    }}
    wall
    {{
        type wall;
        faces
        (
            (0 24 39 15)
            (15 39 38 14)
            (14 38 37 13)
            (13 37 36 12)
            (12 36 35 11)
            (11 35 34 10)
            (10 34 33 9)
            (8 32 31 7)
            (7 31 30 6)
            (6 30 29 5)
            (5 29 28 4)
            (4 28 27 3)
            (3 27 26 2)
            (2 26 25 1)
        );
    }}
    cylinder_1
    {{
        type wall;
        faces
        (
            (17 41 40 16)
            (18 42 41 17)
            (19 43 42 18)
            (16 40 43 19)
        );
    }}
    cylinder_2
    {{
        type wall;
        faces
        (
            (21 45 44 20)
            (22 46 45 21)
            (23 47 46 22)
            (20 44 47 23)
        );
    }}
    frontAndBack
    {{
        type empty;
        faces
        (
        //front
            (0 15 2 1)
            (15 14 3 2)

            (14 16 17 3)
            (14 13 19 16)
            (17 18 4 3)
            (19 13 4 18)
            
            (13 12 5 4)

            (12 20 21 5)
            (21 22 6 5)
            (23 11 6 22)
            (12 11 23 20)

            (11 10 7 6)
            (10 9 8 7)
            
         //back
            (25 26 39 24)  
            (26 27 38 39)  

            (27 41 40 38)  
            (40 43 37 38)  
            (27 28 42 41)  
            (42 28 37 43)  

            (28 29 36 37)  

            (29 45 44 36)  
            (29 30 46 45)  
            (46 30 35 47)  
            (44 47 35 36)  

            (30 31 34 35)  
            (31 32 33 34)
        );
    }}
);

mergePatchPairs
(
);
checkGeometry true;
'''

TRANSPORT_PROPERTIES = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "constant";
    object      transportProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

transportModel  Newtonian;

nu              [0 2 -1 0 0 0 0] 1.5e-5;

// ************************************************************************* //
'''

TURBULENCE_PROPERTIES = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "constant";
    object      RASProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

simulationType  laminar;

// ************************************************************************* //
'''

PRESSURE_FIELD = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       volScalarField;
    location    "0";
    object      p;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    inlet
    {
        type            zeroGradient;
    }
    outlet
    {
        type            fixedValue;
        value           $internalField;
    }
    wall
    {
        type            zeroGradient;
    }
    cylinder_1
    {
        type            zeroGradient;
    }
    cylinder_2
    {
        type            zeroGradient;
    }
    frontAndBack
    {
        type            empty;
    }
}

// ************************************************************************* //
'''

U_FIELD = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/    

FoamFile
{
    format ascii;
    class volVectorField;
    location "0";
    object U;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform (0 1 0);
    }
    outlet
    {
        type            zeroGradient;
    }
    wall
    {
        type            noSlip;
    }
    cylinder_1
    {
        type            noSlip;
    }
    cylinder_2
    {
        type            noSlip;
    }
    frontAndBack
    {
        type            empty;
    }
}

// ************************************************************************* //
'''

TRACER_FIELD = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/

FoamFile
{
    format ascii;
    class volScalarField;
    location "0";
    object tracer;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform 0;
    }
    outlet
    {
        type            zeroGradient;
    }
    wall
    {
        type            zeroGradient;
    }
    cylinder_1
    {
        type            zeroGradient;
    }
    cylinder_2
    {
        type            zeroGradient;
    }
    frontAndBack
    {
        type            empty;
    }
}

// ************************************************************************* //
'''
FV_SOLUTION = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

solvers
{
    p
    {
        solver           GAMG;
        smoother         DICGaussSeidel;
        tolerance        1e-6;
        relTol           0.01;
    }

    pFinal
    {
        $p;
        relTol          0;
    }

    "(U|tracer)"
    {
        solver          PBiCGStab;
        preconditioner  DILU;
        tolerance       1e-05;
        relTol          0.1;
    }

    "(U|tracer)Final"
    {
        $U;
        relTol          0;
    }
}

PIMPLE
{
    nNonOrthogonalCorrectors 1;
    nCorrectors         2;
}


// ************************************************************************* //
'''

FV_SCHEMES = '''/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
    limited         cellLimited Gauss linear 1;
}

divSchemes
{
    default             none;

    div(phi,U)          Gauss linearUpwind limited;
    div(phi,tracer)     Gauss linearUpwind limited;
    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear corrected;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         corrected;
}


// ************************************************************************* //
'''