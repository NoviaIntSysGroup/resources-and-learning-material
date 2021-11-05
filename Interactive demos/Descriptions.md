# Interactive demos

## LinearRegression.py
**Required python packages:**
- numpy,
- matplotlib,
- tkinter.

These are all already included in your base environment if you installed anaconda (i.e. not miniconda).  
**Usage:**  
```console
$ python LinearRegression.py
```
**Purpose:** Intended to convey basics concepts related to learning.
1. Show how parameters change the input-output mapping of a model (linear model in this case).
1. Introduce the notion of an objective function, and how it spans a surface over the space of parameter values.
1. Illustrate that every parameter combination correspond to one point on the surface.
1. Introduce the concept of gradients.
1. Show how learning can take place even if one only knows the current gradient.

## KMeans.py
**Required python packages:**
- numpy,
- matplotlib,
- scipy,
- tkinter.

These are all already included in your base environment if you installed anaconda (i.e. not miniconda).  
**Usage:**  
```console
$ python KMeans.py
```
**Purpose:** Intended to highlight that you can still define objective functions to accomplish tasks without labels, that is, unsupervised learning.
1. Highlight that performance on a clustering task can be quantified by checking how far each data point is from its closest centroid.
1. Show that the gradient of an objective function that minimizes the squared distances  indicates in which direction to move each centroid and how far.
1. Highlight how easily objective functions become non-convex and what it means in practice. Learning will in this case lead to different solutions as soon as more than 3 centroids are used.  
