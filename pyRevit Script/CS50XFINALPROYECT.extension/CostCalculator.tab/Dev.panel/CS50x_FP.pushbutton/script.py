# -*- coding: utf-8 -*-
__title__ = "CS50x Cost Calculator"
__doc__ = "Version = 1.0"

# IMPORTS
from Autodesk.Revit.DB import *
from pyrevit import revit, forms

# .NET Imports
import clr
clr.AddReference("System")
from System.Diagnostics import Process
import sys
import sqlite3
import os
import shutil
import subprocess
import time

# REVIT MODEL VARIABLES
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# GETTING PROJECT INFORMATION
project_info = FilteredElementCollector(doc).OfClass(ProjectInfo).FirstElement()
building_name_param = project_info.LookupParameter("Building Name").AsString()

if not building_name_param:
    print("Project has no name")
    sys.exit(1)

# ---------------------------------------------------------------------------------
# GET ELEMENTS OF WALL CATEGORY IN MODEL AND MAKING SUM
Walls = (FilteredElementCollector(doc)
                  .OfCategory(BuiltInCategory.OST_Walls)
                  .WhereElementIsNotElementType()
                  .ToElements())

total_square_feets_walls = 0.0

for wall in Walls:
    area_param = wall.LookupParameter("Area")
    if area_param:
        total_square_feets_walls += area_param.AsDouble()
    else:
        print("Area parameter doesn't exist for this Element")

total_square_meters_walls = total_square_feets_walls * 0.092903
area_total_muros = round(total_square_meters_walls)

# ---------------------------------------------------------------------------------
# CONNECT WITH DB

db_path = r"C:\Users\estag\Desktop\Local DB\model_quant.db"

conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

cursor.execute('''
INSERT OR REPLACE INTO const_elements (Proyect, Element, Quantity)
VALUES (?, ?, ?);
''', (building_name_param, "Walls", area_total_muros))

conexion.commit()
conexion.close()

# ---------------------------------------------------------------------------------
# GET ELEMENTS OF FLOOR CATEGORY IN MODEL AND MAKING SUM
Floors = (FilteredElementCollector(doc)
                  .OfCategory(BuiltInCategory.OST_Floors)
                  .WhereElementIsNotElementType()
                  .ToElements())

total_square_feets_floors = 0.0

for floor in Floors:
    area_param = floor.LookupParameter("Area")
    if area_param:
        total_square_feets_floors += area_param.AsDouble()
    else:
        print("Area parameter doesn't exist for this Element")

total_square_meters_floors = total_square_feets_floors * 0.092903
area_total_floors = round(total_square_meters_floors)

# ---------------------------------------------------------------------------------
# CONNECT WITH DB
db_path = r"C:\Users\estag\Desktop\Local DB\model_quant.db"

conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

cursor.execute('''
INSERT OR REPLACE INTO const_elements (Proyect, Element, Quantity)
VALUES (?, ?, ?);
''', (building_name_param, "Floors", area_total_floors))

conexion.commit()
conexion.close()

# ---------------------------------------------------------------------------------
# GET ELEMENTS OF DOOR CATEGORY IN MODEL AND MAKING SUM
Doors = (FilteredElementCollector(doc)
                  .OfCategory(BuiltInCategory.OST_Doors)
                  .WhereElementIsNotElementType()
                  .ToElements())

total_square_feets_doors = 0.0

for door in Doors:
    area_param = door.LookupParameter("Area")
    if area_param:
        total_square_feets_doors += area_param.AsDouble()
    else:
        print("Area parameter doesn't exist for this Element")

total_square_meters_doors = total_square_feets_doors * 0.092903
area_total_doors = round(total_square_meters_doors)
#-------------------------------------------------------------------
# CONNECT WITH DB
db_path = r"C:\Users\estag\Desktop\Local DB\model_quant.db"

conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

cursor.execute('''
INSERT OR REPLACE INTO const_elements (Proyect, Element, Quantity)
VALUES (?, ?, ?);
''', (building_name_param, "Doors", area_total_doors))

conexion.commit()
conexion.close()

# ---------------------------------------------------------------------------------
# GET ELEMENTS OF WINDOW CATEGORY IN MODEL AND MAKING SUM
Windows = (FilteredElementCollector(doc)
                  .OfCategory(BuiltInCategory.OST_Windows)
                  .WhereElementIsNotElementType()
                  .ToElements())

total_square_feets_windows = 0.0

for window in Windows:
    area_param = window.LookupParameter("Area")
    if area_param:
        total_square_feets_windows += area_param.AsDouble()
    else:
        print("Area parameter doesn't exist for this Element")

total_square_meters_windows = total_square_feets_windows * 0.092903
area_total_windows = round(total_square_meters_windows)

# ---------------------------------------------------------------------------------
# CONNECT WITH DB
db_path = r"C:\Users\estag\Desktop\Local DB\model_quant.db"

conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

cursor.execute('''
INSERT OR REPLACE INTO const_elements (Proyect, Element, Quantity)
VALUES (?, ?, ?);
''', (building_name_param, "Windows", area_total_windows))

conexion.commit()
conexion.close()

# CHECKING DB IS ACTUALIZED AND CONNECTION WITH REVIT IS CLOSED
time.sleep(1)
print("DB up to date and connection closed")

# COPYING DB
# ROUTES
original_db = r"C:\Users\estag\Desktop\Local DB\model_quant.db"
flask_dir = r"C:\Users\estag\Desktop\CS50xfplocal"
flask_db_path = os.path.join(flask_dir, "model_quant.db")

# CHECKING FILE IS UNBLOCKED
print("THE FILE IS UNBLOCKED")
time.sleep(1)

# COPYING UP TO DATE FILE TO FLASK FOLDER
print("COPYING DB TO FLASK APP FOLDER")
shutil.copy(original_db, flask_db_path)

# CHANGING TO FLASK FOLDER
os.chdir(flask_dir)
print("Directorio actual:", os.getcwd())

print("SCRIPT DONE")


