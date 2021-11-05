# KMeans interactive demo
# Creted by: Johan Westö (johan.westo@novia.fi)

import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.spatial import Voronoi, voronoi_plot_2d

# tkinter GUI
root = tk.Tk()
root.wm_title("K-means example")
fig = Figure(figsize=(7, 5), dpi=100)
ax1 = fig.add_axes([0.1, 0.1, 0.65, 0.8])
ax2 = fig.add_axes([0.825, 0.1, 0.075, 0.8])
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

# Parameters
variance = 0.25
n_per_cluster = 200
cluster_means = np.array([[-1, 1], [1, 1], [0, -1]])
covariance = variance*np.eye(2)
color_clusters = False				# grey or colored clusters
ax_lim = 2.5 						# +- limits for generated x-values
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
colors = [colors[np.mod(i, 10)] for i in range(100)]

# Generating data points
X = []
for i in range(cluster_means.shape[0]):
	X.append(np.random.multivariate_normal(cluster_means[i, :], covariance, n_per_cluster))
X = np.vstack(X)

def getLabels():
	# Compute the distance from each data point to every centroid
    X - centroids[0, :]
    distances = []
    for i in range(centroids.shape[0]):
        distances.append(np.sqrt(np.sum((X - centroids[i, :])**2, axis=1, keepdims=True)))
    distances = np.hstack(distances)
	# Assign labels based on the centroid closest to each data point
    labels = np.argmin(distances, axis=1)
    return labels

def getVorEdges():
	vor = Voronoi(centroids)
	vor_edges = []
	# Figure out how to draw lines based on ridge edges and vertices
	# Save start and end point for each ridge
	for i in range(len(vor.ridge_vertices)):
	    edges_tmp = []
	    for j in [0, 1]:
	        if vor.ridge_vertices[i][j] >= 0:
	            edges_tmp.append(vor.vertices[vor.ridge_vertices[i][j], :])
	        else:
	            mid_point = np.mean(centroids[vor.ridge_points[i, :]], axis=0, keepdims=True)
	            vor_vertice = vor.vertices[vor.ridge_vertices[i][1-j], :]
				# diff = line from the vor vertice to the mid point
	            diff = mid_point - vor_vertice
				# Figure out in which direction to draw the line from the vor vertice
	            closest_centroids = np.argsort(np.sqrt(np.sum((centroids-mid_point)**2, axis=1)))
	            if not np.array_equal(np.unique(closest_centroids[0:2]), np.unique(vor.ridge_points[i, :])):
	                diff *= -1
				# Make the vector super long so that it will always be outside of the axes limits
	            diff = 1e6*diff/np.linalg.norm(diff)
	            edges_tmp.append( vor_vertice + diff)
	    vor_edges.append(np.vstack(edges_tmp))
	return vor_edges

def updateClusters():
	# Update the cluster colors and centroid positions
	data_colors = [colors[i] for i in labels]
	path_data.set_facecolor(data_colors)
	path_centroids.set_data(centroids[:, 0], centroids[:, 1])
	path_centroids.set_alpha(1)
	# Update distances
	for i, path in enumerate(path_distances):
		path.set_data([centroids[labels[i], 0], X[i, 0]], [centroids[labels[i], 1], X[i, 1]])
		path.set_alpha(show_distances.get()*0.25)
	# Remove old gradient and old vor lines
	for artist in ax1.get_children():
		if (artist.get_gid() == 'vor') or (artist.get_gid() == 'arrow'):
			artist.remove()
	# Plot the new gradient
	gradient = getGradient()
	for i in range(centroids.shape[0]):
		ax1.quiver(centroids[i, 0], centroids[i, 1], -gradient[i, 0], -gradient[i, 1], units='xy', scale=1, minlength=1, minshaft=0.2, gid='arrow')
	# Plot the new vor lines
	vor_edges = getVorEdges()
	for i in range(len(vor_edges)):
		ax1.plot(vor_edges[i][:, 0], vor_edges[i][:, 1], 'k:', gid='vor')
	# Update the objective function
	obj_fun_val = getObjFunVal()
	obj_fun_bar.set_xy(np.array([[0, 1, 1, 0],[0, 0, obj_fun_val, obj_fun_val]]).T)
	ax2.plot([0, 1], [obj_fun_val, obj_fun_val], 'r-', gid='obj_fun_progress')
	canvas.draw()

def resetCentroids():
	global centroids, labels, color_clusters
	color_clusters = True
	# Generate new centroids by picking random data points
	centroids = X[np.random.permutation(X.shape[0])[0:slider_k.get()], :]
	# Compute new labels
	labels = getLabels()
	# Reset the progress lines on the bar graph for the objective function
	for artist in ax2.get_children():
		if artist.get_gid() == 'obj_fun_progress':
			artist.remove()
	updateClusters()

def getObjFunVal():
	squarred_distance = 0
	for i in range(centroids.shape[0]):
		squarred_distance += np.sum((X[labels==i, :] - centroids[i, :])**2)
	return squarred_distance

def getGradient():
	global centroids, labels
	eta = slider_eta.get()				# Read out the learning rate
	gradient = []
	# eta = 1 corresponds to one step with Newton's method
	# Slight abuse of the gradient term
	for i in range(centroids.shape[0]):
		gradient.append(-np.mean(X[labels==i, :] - centroids[i, :], axis=0))
	gradient = eta*np.vstack(gradient)
	return gradient

def takeLearningStep():
	global centroids, labels
	gradient = getGradient()
	centroids = centroids - gradient
	labels = getLabels()
	updateClusters()

def changeNumberOfClusters(*args):
	if color_clusters:
		resetCentroids()

def changeLearningRate(*args):
	if color_clusters:
		updateClusters()

def showDistances(*args):
	if color_clusters:
		updateClusters()

# Buttons
button_frame = tk.Frame()
button_quit = tk.Button(master=button_frame,
						text="Quit",
						command=root.quit)
button_reset = tk.Button(master=button_frame,
						 text="Reset centroids",
						 command=resetCentroids)
button_step= tk.Button(master=button_frame,
					   text="Learning step",
					   command=takeLearningStep)

# Checkboxes
checkbox_frame = tk.Frame()
show_distances = tk.IntVar()
checkbox_distances = tk.Checkbutton(checkbox_frame,
							        text="Show distances",
								    variable=show_distances,
									command=showDistances)

# Sliders
length = 150
refresh_interval = 10
slider_frame = tk.Frame()
slider_k = tk.Scale(slider_frame,
		 		    label='Number of clusters',
					length=length,
					repeatinterval=refresh_interval,
					from_=3, to=10, resolution=1,
					orient=tk.HORIZONTAL,
					command=changeNumberOfClusters)
slider_eta = tk.Scale(slider_frame,
					  label='Learning rate',
					  length=length,
					  repeatinterval=refresh_interval,
				      from_=0.2, to=2, resolution=0.2,
					  orient=tk.HORIZONTAL,
					  command=changeLearningRate)

# Set initial values
slider_k.set(3)
slider_eta.set(1)

# Pack all elements onto the GUI
button_frame.pack(side=tk.BOTTOM)
button_quit.pack(padx=5, side=tk.LEFT)
button_reset.pack(padx=5, side=tk.LEFT)
button_step.pack(padx=5, side=tk.LEFT)
slider_frame.pack(side=tk.BOTTOM)
slider_k.pack(padx=5, side=tk.LEFT)
slider_eta.pack(padx=5, side=tk.LEFT)
checkbox_frame.pack(side=tk.BOTTOM)
checkbox_distances.pack(padx=5, side=tk.LEFT)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Randomly pick n centroids from all data ppints
centroids = X[np.random.permutation(X.shape[0])[0:slider_k.get()], :]
labels = getLabels()

# Initialize
path_distances = ax1.plot([centroids[labels, 0], X[:, 0]], [centroids[labels, 1], X[:, 1]], 'r-', alpha=0)
path_data = ax1.scatter(X[:, 0], X[:, 1], 40, 'k', alpha=0.25, label='data_raw')
path_centroids = ax1.plot(centroids[:, 0], centroids[:, 1], 'ko', alpha=0)[0]
ax1.set(xlim=[-ax_lim, ax_lim], ylim=[-ax_lim, ax_lim], xlabel='$x_1$', ylabel='$x_2$', title='Data')
ax2.set(xlim=[-0.25, 1.25], ylim=[0, 2e3], xticks=[], yticks=[], ylabel='Objective function value')
obj_fun_bar = ax2.fill([],[], 'r', alpha=0.5)[0]

tk.mainloop()
