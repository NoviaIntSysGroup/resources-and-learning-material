# Linear regression interactive demo
# Creted by: Johan Westö (johan.westo@novia.fi)

import numpy as np
import tkinter as tk
from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# tkinter GUI
root = tk.Tk()
root.wm_title("Logistic regression example")
fig = Figure(figsize=(12, 5), dpi=100)
fig.subplots_adjust(wspace=0.3);
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

# Parameters
mu1 = -1		    # mu for class 1
mu2 = 2		   	 	# mu for class 2
sigma = 1	    	# std around mu
n = 30				# Number of data points
x_lim = [mu1-3, mu2+3] 	# +- limits for generated x-values

# Resolution and limits for the error surface
dW = 0.05
W0_lim = (-6, 4.)
W1_lim = (-1, 6)

# Generating data points
x_class1 =  sigma*np.random.randn(n, 1) + mu1
x_class2 =  sigma*np.random.randn(n, 1) + mu2
x = np.vstack([x_class1, x_class2])
X = np.hstack([np.ones([2*n, 1]), x])
y = np.vstack([np.zeros([n, 1]), np.ones([n, 1])])

# Generate linearly spaced x-values for model predictions
x_model = np.linspace(x_lim[0], x_lim[1], 101)				# Linearly spaced x-values
X_model = np.vstack( (np.ones(x_model.size), x_model) ).T 	# X matrix, [1, x]

# Creating matrices for computing the error surface
W = np.random.rand(2).reshape(1,2)			# Initial random guesss
W0 = np.arange(W0_lim[0],W0_lim[1]+dW,dW)	# Array of w0 values
W1 = np.arange(W1_lim[0],W1_lim[1]+dW,dW)	# Array of w1 values
W0, W1 = np.meshgrid(W0,W1)					# W0 nd W1 matrices
nll = np.zeros(W0.size).reshape(W0.shape)	# Emptty matrix for nll
# Average negative loglikelihood
i_max, j_max = nll.shape
for i in range(i_max):
	for j in range(j_max):
		W_tmp = np.array( [ W0[i,j], W1[i,j] ] ).reshape(1,2)	# Weight combination
		z = np.dot( W_tmp, X.T )		# Similarity score
		y_hat = 1 / (1 + np.exp(-z))	# Model outputs
		ll = y*np.log(y_hat.T) + (1-y)*np.log(1-y_hat.T)
		nll[i,j] = -ll.mean()

# Plotting data points
z = np.dot( W[-1, :], X_model.T )
y_hat = 1 / (1 + np.exp(-z))
ax1 = fig.add_subplot(1,2,1)
data1 = ax1.plot(x[y==0], y[y==0].flatten(),'o', alpha=0.5, label='Class 0')
data1 = ax1.plot(x[y==1], y[y==1].flatten(),'o', alpha=0.5, label='Class 1')
model = ax1.plot(x_model, y_hat,'k-', label='Model')[0]
model_text = r'$f(x) = 1/(1+\exp(-{:1.1f}x - {:1.1f})$'.format(W[0, 1], W[0, 0])
text = ax1.text(0.99, 0.01, model_text,
				horizontalalignment='right',
				verticalalignment='bottom', transform=ax1.transAxes)
ax1.set_xlabel('x')
ax1.set_ylabel('y; p(y=1)')
ax1.set_xlim([1.1*lim for lim in x_lim])
ax1.set_ylim([-0.1, 1.1])
ax1.set_title('Data and model')
ax1.legend(loc=2)

# Plotting the nll surface
ax2 = fig.add_subplot(1,2,2)
surf = ax2.contourf(W0, W1, nll, 50, cmap=cm.coolwarm)
surf.set_alpha(0.75)
path = ax2.plot(W[:, 0], W[:, 1], 'k:o', mfc='None', mew=2)[0]
ax2.plot([], [], gid='arrow')
ax2.set_xlabel('$w_0$')
ax2.set_ylabel('$w_1$')
ax2.set(xlim=W0_lim, ylim=W1_lim)
ax2.set_title('Objective function')

def updateModelPrediction(*args):
	# Model Prediction
	z = np.dot( W[-1, :], X_model.T ).flatten()
	y_hat = 1 / (1 + np.exp(-z))
	# Update model
	model.set_data(x_model, y_hat)
	model_text = r'$f(x) = 1/(1+\exp(-{:1.1f}x - {:1.1f})$'.format(W[-1, 1], W[-1, 0])
	text.set_text(model_text)
	canvas.draw()

def updatePath():
	# Model Prediction
	z = np.dot( W[-1, :], X.T )
	y_hat = 1 / (1 + np.exp(-z))
	# Gradient
	e = y - y_hat[:, np.newaxis]
	dW = 1 / n * np.dot( e.T, X )
	dW = dW / np.linalg.norm(dW)
	# Update path
	path.set_data(W[:, 0], W[:, 1])
	ax2.findobj(lambda artist : artist.get_gid() == 'arrow')[0].remove()
	ax2.quiver(W[-1, 0], W[-1, 1], dW[0, 0], dW[0, 1], scale_units='inches', scale=3, gid='arrow')
	canvas.draw()

def updateWeights(*args):
	global W
	W = W[0, :].reshape(1, 2)
	W[0, 0] = slider_bias.get()
	W[0, 1] = slider_slope.get()
	updateModelPrediction()
	updatePath()

def resetPath(*args):
	global W
	W = W[0, :].reshape(1, 2)
	updateModelPrediction()
	updatePath()

def takeLearningStep():
	global W
	eta = slider_eta.get()				# Read out the learning rate
	z = np.dot( W[-1, :], X.T )			# Similarity score
	y_hat = 1 / (1 + np.exp(-z))
	e = y - y_hat[:, np.newaxis]		# error signal
	dW = - eta / n * np.dot( e.T, X )	# Gradient
	W = np.append(W, W[-1, :] - dW, 0)	# Take a step
	updateModelPrediction()
	updatePath()

# Buttons
button_frame = tk.Frame()
button_quit = tk.Button(master=button_frame,
						text="Quit",
						command=root.quit)
button_reset = tk.Button(master=button_frame,
						 text="Reset path",
						 command=resetPath)
button_step= tk.Button(master=button_frame,
					   text="Learning step",
					   command=takeLearningStep)

# Sliders
length = 150
refresh_interval = 10
slider_frame = tk.Frame()
slider_bias = tk.Scale(slider_frame,
					   label='W0',
					   length=length,
					   repeatinterval=refresh_interval,
					   from_=W0_lim[0], to=W0_lim[1], resolution=0.1,
					   orient=tk.HORIZONTAL,
					   command=updateWeights)
slider_slope = tk.Scale(slider_frame,
						label='W1',
						length=length,
						repeatinterval=refresh_interval,
						from_=W1_lim[0], to=W1_lim[1], resolution=0.1,
						orient=tk.HORIZONTAL,
						command=updateWeights)
slider_eta = tk.Scale(slider_frame,
					  label='Learning rate',
					  length=length,
					  repeatinterval=refresh_interval,
				      from_=0.2, to=4.0, resolution=0.2,
					  orient=tk.HORIZONTAL)

# Set initial values
slider_bias.set(W[0, 0])
slider_slope.set(W[0, 1])
slider_eta.set(1.0)

# Pack all elements onto the GUI
button_frame.pack(side=tk.BOTTOM)
button_quit.pack(padx=5, side=tk.LEFT)
button_reset.pack(padx=5, side=tk.LEFT)
button_step.pack(padx=5, side=tk.LEFT)
slider_frame.pack(side=tk.BOTTOM)
slider_bias.pack(padx=5, side=tk.LEFT)
slider_slope.pack(padx=5, side=tk.LEFT)
slider_eta.pack(padx=5, side=tk.LEFT)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

updateModelPrediction()
updatePath()

tk.mainloop()
