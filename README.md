# P01 - ArRESTed Development - Global Bites by Team Bareustoph

**Team Bareustoph** (bah-reh-us-tofh)  
Ben Rudinski, Tiffany Yang, Tim Ng, Endirt Idrizi

## Roster with Roles

- **Ben Rudinski**  
  Button-Mashing, Feature-Wrangling, and Making Sure Everything Actually Works

- **Tiffany Yang**  
  Database Whisperer (and Chief Leak Plugger)

- **Endrit Idrizi**  
  CSS Sorcery and Stylin' Shenanigans

- **Tim Ng**  
  Flask Mastery (a.k.a. Server Wizardry)

---

## Description

**Global Bites** is an interactive website that showcases traditional recipes for global holidays. Users can explore holidays worldwide, find associated recipes, and view high-quality food images for inspiration. The site features an interactive world map where users can click on countries to discover popular holidays, traditional dishes, cultural customs, and fun facts. Users can also create accounts to save favorite recipes, share experiences, and engage with a community of global food enthusiasts.

---  

## Install Guide [w.i.p]

### Prerequisites
Ensure you have the following installed on your system:
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3](https://www.python.org/downloads/)

It's recommended to run this project in a virtual environment to avoid any potential conflicts with other packages. Obviously this doesn't apply to you Topher, but if your less advanced, refer to [this guide](https://novillo-cs.github.io/apcsa/tools/).

### Steps to Install and Run
1. Clone and move into this repository
```
$ git clone git@github.com:Tuvalu23/p01.git
```
```
$ cd p01
```
3. Create a virtual environment
```
$ python3 -m venv foo
```

4. Activate the virtual environment: Linux/MacOS
```
$ . foo/bin/activate
```
4. Activate the virtual environment: Windows
```
$ foo\Scripts\activate
```
5. Install required packages
```
$ pip install -r requirements.txt
```
## Launch Codes: [w.i.p]
1. Run the database setup file
``` 
$ python3 app/setup_db.py
```
2. Locate and run the app file
``` 
$ cd app
```
``` 
$ python3 __init__.py
```
3. Access the Application: Open your browser and go to http://127.0.0.1:5000 or click the link that appears in your terminal output.
To stop the app, press CTRL + C

