# Linear regression interactive demo
# Creted by: Johan Westö (johan.westo@novia.fi)

import numpy as np
import tkinter as tk
from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# tkinter GUI
root = tk.Tk()
root.wm_title("Linear regression example")
fig = Figure(figsize=(12, 5), dpi=100)
fig.subplots_adjust(wspace=0.3);
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

# Parameters
a = 1		    	# Data generated as y = a*x + b + r
b = 1		   	 	# where r is a normally distributed random
sigma = 1	    	# number with mean 0 and std sigma
n = 50				# Number of dta points
x_lim = [-5, 5] 	# +- limits for generated x-values

# Resolution and limits for the error surface
dW = 0.05
W0_lim = (-4.5, 6.5)
W1_lim = (-2.5, 4.5)

# Generating data points
x = np.linspace(x_lim[0], x_lim[1], n)		# Linearly spaced x-values
X = np.vstack( (np.ones(n), x) )			# X matrix, [1; x1]
coeff = np.array( [b, a] ).reshape(2,1)		# Array with the parameters a and b
r = np.random.normal(0, sigma*sigma, n)		# Random noice
y = np.dot( coeff.T, X ) + r				# Observed outputs for each x value

# Creating matrices for computing the error surface
W = np.random.normal(1, 2, 2).reshape(1,2)
W0 = np.arange(W0_lim[0],W0_lim[1]+dW,dW)	# Array of w0 values
W1 = np.arange(W1_lim[0],W1_lim[1]+dW,dW)	# Array of w1 values
W0, W1 = np.meshgrid(W0,W1)					# W0 nd W1 matrices
Eav = np.zeros(W0.size).reshape(W0.shape)	# Emptty matrix for Eav
# Average error energy
iMax, jMax = Eav.shape
for i in range(iMax):
	for j in range(jMax):
		W_tmp = np.array( [ W0[i,j], W1[i,j] ] ).reshape(1,2)	# Weight combination
		y_hat = np.dot( W_tmp, X )	# Calculating model outputs
		e = y - y_hat				# Error signal
		Eav[i,j] = np.mean(e**2)

# Plotting data points
y_hat = np.dot( W[-1, :], X )
ax1 = fig.add_subplot(1,2,1)
data = ax1.plot(x,y.flatten(),'bo', alpha=0.5)
model = ax1.plot(x, y_hat,'k-')[0]
errors = ax1.plot(np.vstack([x, x]), np.vstack([y, y_hat]),'r-', zorder=1)
model_text = r'$f(x) = {:1.1f}x + {:1.1f}$'.format(W[0, 0], W[0, 1])
text = ax1.text(0.99, 0.01, model_text, horizontalalignment='right', verticalalignment='bottom', transform=ax1.transAxes)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_xlim([1.1*lim for lim in x_lim])
ax1.set_ylim(np.floor(y.min()), np.ceil(y.max()))
ax1.set_title('Data and model')
ax1.legend(['Data', 'Model'], loc=2)
#ax1.legend([data, model], ['Data', 'Model'])

# Plotting error surface
ax2 = fig.add_subplot(1,2,2)
surf = ax2.contourf(W0, W1, Eav, 50, cmap=cm.coolwarm)
surf.set_alpha(0.75)
path = ax2.plot(coeff[0],coeff[1],'k:o', mfc='None', mew=2)[0]
ax2.plot([], [], gid='arrow')
ax2.set_xlabel(r'Bias term')
ax2.set_ylabel(r'Slope')
ax2.set_title('Objective function')

def updateModelPrediction(*args):
	# Model Prediction
	y_hat = np.dot( W[-1, :], X ).flatten()
	# Update model
	model.set_data(x, y_hat)
	model_text = r'$f(x) = {:1.1f}x + {:1.1f}$'.format(W[-1, 1], W[-1, 0])
	text.set_text(model_text)
	# Update errors
	for i, e in enumerate(errors):
		if show_errors.get():
			e.set_data([x[i], x[i]], [y[0, i], y_hat[i]])
		else:
			e.set_data([], [])
	canvas.draw()

def updatePath():
	# Model Prediction
	y_hat = np.dot( W[-1, :], X )
	# Gradient
	e = y - y_hat
	dW = 1 / n * np.dot( e, X.T )
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
	y_hat = np.dot( W[-1, :], X )		# Model output on training data
	e = y - y_hat						# error signal
	dW = - eta / n * np.dot( e, X.T )	# Gradient
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

# Checkboxes
checkbox_frame = tk.Frame()
show_errors = tk.IntVar()
checkbox_error = tk.Checkbutton(checkbox_frame,
							       text="Show errors",
								   variable=show_errors,
								   command=updateModelPrediction)

# Sliders
length = 150
refresh_interval = 10
slider_frame = tk.Frame()
slider_bias = tk.Scale(slider_frame,
					   label='Bias term',
					   length=length,
					   repeatinterval=refresh_interval,
					   from_=W0_lim[0], to=W0_lim[1], resolution=0.1,
					   orient=tk.HORIZONTAL,
					   command=updateWeights)
slider_slope = tk.Scale(slider_frame,
						label='Slope',
						length=length,
						repeatinterval=refresh_interval,
						from_=W1_lim[0], to=W1_lim[1], resolution=0.1,
						orient=tk.HORIZONTAL,
						command=updateWeights)
slider_eta = tk.Scale(slider_frame,
					  label='Learning rate',
					  length=length,
					  repeatinterval=refresh_interval,
				      from_=0.01, to=0.3, resolution=0.01,
					  orient=tk.HORIZONTAL)

# Set initial values
slider_bias.set(W[0, 0])
slider_slope.set(W[0, 1])
slider_eta.set(0.1)

# Pack all elements onto the GUI
button_frame.pack(side=tk.BOTTOM)
button_quit.pack(padx=5, side=tk.LEFT)
button_reset.pack(padx=5, side=tk.LEFT)
button_step.pack(padx=5, side=tk.LEFT)
slider_frame.pack(side=tk.BOTTOM)
slider_bias.pack(padx=5, side=tk.LEFT)
slider_slope.pack(padx=5, side=tk.LEFT)
slider_eta.pack(padx=5, side=tk.LEFT)
checkbox_frame.pack(side=tk.BOTTOM)
checkbox_error.pack(padx=5, side=tk.LEFT)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

updateModelPrediction()
updatePath()

tk.mainloop()
