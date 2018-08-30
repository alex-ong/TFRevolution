TFRevolution

==========
Running
==========

1) Install python >= 3.6
2) pip install pipenv
  - This will install pip virtual environment to deal with dependancy modules
3) pipenv install 
  - This reads the file "pipfile" and installs all relevant modules.
3) pipenv run python main.py
  - Runs pip virtual environment with correct dependancies.
  
==  
Cleanup
==

When you want to "uninstall", you need to nuke the pip virtual environment
1) cd to this directory
2) pipenv --venv
   - this displays where the virtual environment is stored
   - This step is optional, just shows you where the virtual env is actually stored.
3) pipenv --rm
   - removes virtual environment