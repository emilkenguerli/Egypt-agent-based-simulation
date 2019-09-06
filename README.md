CONFIGURE PROJECT
1. pip install virtualenv
2. mkdir venv
3. cd venv
4. cd venv/Scripts
5. source activate      <!-- Linux -->
   activate             <!-- Windows -->
6. cd path/to/egypt-simulation
7. pip install -r requirements.txt
8. deactivate

RUNNING THE PROGRAM
1. cd path/to/venv/Scripts
2. source activate      <!-- Linux -->
   activate             <!-- Windows -->
3. cd path/to/egypt-simulation
4. export PYTHONPATH=path/to/egypt-simulation/src       <!-- Linux -->
   set PYTHONPATH=path/to/egypt-simulation/src          <!-- Windows -->
5. cd path/to/egypt-simulation/src/simulation
6. python simulation_driver.py
7. deactivate

NOTE
* When specifying path directories in Windows use a \ instead of a /
