# Used project structure and workflow

## Default rules for setting up a project
1. Create a separate virtual environment for each project using anaconda. This helps to avoid any dependency clashes between projects, as the environment can be set up with whatever version of python you might need and as it will only contain the packages needed for this particular project.
1. Create a separate Git repository for each project.
1. Use the [Cookiecutter data science](https://drivendata.github.io/cookiecutter-data-science/) project structure as the default template for your project. There is no need to incorporate all elements in the cookiecutter structure, but a typical project ought to have data, notebooks, and src directories as well as LICENSE, README.md, setup.py, requirements.txt and .gitignore files.
1. Install the project in editable mode using `pip install -e .` to be able to import source code in your notebooks without having to add the project to the python path.
1. Use `.env` files for storing secrets (such as keys) that should newer be made public (read the [Cookiecutter data science](https://drivendata.github.io/cookiecutter-data-science/) guide).

## Interactive work versus developing source code



## Thing to keep in mind when writing
1. The most basic rule of programming is to newer ever write the the same piece of code twice. If you have the need to do the same thing twice then write a function.
1. Read the PEP 8 style guide before...
