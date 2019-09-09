CONFIGURE PROJECT
1. pip install virtualenv
2. mkdir venv
3. virtualenv venv
6. cd venv/Scripts
7. source activate      <!-- Linux -->
   activate             <!-- Windows -->
8. cd path/to/egypt-simulation
9. pip install -r requirements.txt
10. deactivate
11. In logging_config.conf, line 34, you should change the path to your matching directory of logs\logs\

RUNNING THE PROGRAM
1. cd path/to/venv/Scripts
2. source activate      <!-- Linux -->
   activate             <!-- Windows -->
4. export PYTHONPATH=path/to/egypt-simulation/src       <!-- Linux -->
   set PYTHONPATH=path/to/egypt-simulation/src          <!-- Windows -->
5. cd path/to/egypt-simulation/src/simulation
6. python simulation_driver.py
7. deactivate

NOTE
* When specifying path directories in Windows use a \ instead of a /
* You can also set up a virtual environment using the command 'python -m venv env'
* You don't need to set up a virtual environment if you don't want to.
