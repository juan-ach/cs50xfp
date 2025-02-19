# CS50X REVIT COST CALCULATOR
#### Video Demo:  https://www.youtube.com/watch?v=1bYURpwdiVo
#### Description: 

## Overview

This project is an integration of a **PyRevit script**, a **Flask web application**, and an **SQLite database** designed to streamline project data management for Revit users. It automates the extraction of model quantities (walls, floors, doors, and windows for example) from Revit files, stores these quantities in a database, and presents the data through a web application. 

The system is ideal for architects, engineers, and contractors who need to show different proyect prices and manage project information effectively with their clients.

---

## Features

- Extracts model data (in this case area, but could be any object parameter) directly from Revit models using a **PyRevit script**.
- Updates an **SQLite database** with model data in real-time.
- Provides a **Flask-based web interface** for:
  - Viewing project data.
  - Managing user accounts (login and registration).
  - Calculating total project costs using predefined unit prices.
  
This integration minimizes manual data handling, reduces errors, and provides a single source of truth for project data.

---

## New Things I've learned

### **Revit API - PyRevit**
As an architect, i'm looking for the crossroads between architecture and programming, so start to learn pyRevit is for me an excellent way to start handle Revit API, allowing users to automate all kind of task through the design process, in this case, taking information from a model, adding information like prices and showing the result in a client-friendly format as a webapp. 

## Design desicions

### **Local IDE**
In the begining of this proyect, i started running the flask webapp directly from cs50.dev IDE, and pushing changes in the db, having all kind of troubles with db file handeling. Then i moved the IDE to local VSCode and found information sharing so much easier between the architectural model and flask app.


## File Structure and Descriptions

### **PyRevit Script**
Following the folder structure of pyRevit, i created a button in Revit's GUI to run the script

The PyRevit script uses the **Revit API** to extract data and store it in an SQLite database. Key functionalities include:
- **Project Information Extraction:** Fetches the project name from Revit, to identify users in login with the project.
- **Wall, Floor, Door, and Window Areas:** Calculates total areas for each category and converts them to square meters.
- **Database Integration:** Updates the `const_elements` table in the SQLite database with the project name, element type, and quantity.
- **Database Sync:** Copies the updated database to the Flask application's directory for real-time web access, avoiding problems of DB file usage between applications.

### **Flask Web Application**

The Flask application provides a user-friendly interface for accessing project data. Key components:
- **Routes:**
  - `/`: Displays project data, unit prices, and total costs (requires login).
  - `/login`: Allows users to log in with their credentials.
  - `/register`: Enables new users to register an account.
  - `/logout`: Logs users out and clears session data.
- **Database Access:** Connects to the SQLite database to retrieve user and project data.
- **Templates:** Renders dynamic HTML templates for displaying data and managing user interactions.

### **Helpers**


This file contains utility functions to support the Flask application:
- **Apology Function:** Displays error messages to users.
- **Login Decorator:** Ensures certain routes are only accessible to logged-in users.
- **Formatters:** Formats currency (`usd`) and surface areas (`surface`) for display in templates.

### **SQLite Database**


The database stores project data, including:
- **`const_elements` Table:** Contains project name, element type, quantity, and timestamp.
- **`users` Table:** Stores user information (e.g., username and hashed password).
- **`single_prices` Table:** Maintains unit prices for each element type, used for cost calculations.

### **HTML Templates**


Dynamic HTML templates for the Flask app:
- **`index.html`:** Displays project data, costs, and summaries.
- **`login.html`:** Provides a login form.
- **`register.html`:** Allows new users to create an account.
- **`apology.html`:** Shows error messages.

---

## How It Works

1. **PyRevit Script Execution:**
   - Run the script in Revit.
   - The script calculates areas for walls, floors, doors, and windows, or any others parameter of model's objects, but, for the sake of simplicity, i'll keep just this four parameters.
   - Updates the `const_elements` table in `model_quant.db`.
   - Syncs the database with the Flask app directory.

2. **Flask Web Application:**
   - Start the Flask app.
   - Log in to access project data.
   - View quantities and calculate total costs based on unit prices.

3. **Database Operations:**
   - The SQLite database acts as a central hub for storing and retrieving data.
   - Flask app queries the database to fetch data dynamically.
   - Flask app write users table every time a new user registers.

## **Future Ugrades**

   - Add a 3D model visualization, with a modification tracker, to realice what have changed in the model, and its impact in the amount of elements and cost.
   - Let users interact changing the quality of different elements with a dropdown menu of element types, to find the price that fits client's budget.

