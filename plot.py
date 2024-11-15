import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as patches
import matplotlib as mpl
import math

# Plot Gx vs Gy
def plot_rings(ler_data,her_data,signx,signy):
	plt.figure(figsize=(8, 8))

	ler_coll_indices = [i for i, name in enumerate(ler_data['NAME']) if name.startswith("PMD")]
	her_coll_indices = [i for i, name in enumerate(her_data['NAME']) if name.startswith("PMD")]

	ler_coll_x = signx*np.array([ler_data['Gx'][i] for i in ler_coll_indices])
	ler_coll_y = signy*np.array([ler_data['Gy'][i] for i in ler_coll_indices])
	her_coll_x = signx*np.array([her_data['Gx'][i] for i in her_coll_indices])
	her_coll_y = signy*np.array([her_data['Gy'][i] for i in her_coll_indices])

	x_ler = signx*np.array(ler_data['Gx'])
	y_ler = signy*np.array(ler_data['Gy'])

	x_her = signx*np.array(her_data['Gx'])
	y_her = signy*np.array(her_data['Gy'])

	ox_ler = signx*np.array(ler_data['OGx'])
	oy_ler = signy*np.array(ler_data['OGy'])

	ox_her = signx*np.array(her_data['OGx'])
	oy_her = signy*np.array(her_data['OGy'])

	plt.plot(x_ler, y_ler, linestyle='-', color='r', label="LER")
	plt.plot(x_her, y_her, linestyle='-', color='b', label="HER")

	plt.plot(ox_ler, oy_ler, linestyle='--', color='r')
	plt.plot(ox_her, oy_her, linestyle='--', color='b')

	plt.plot(ler_coll_x, ler_coll_y, marker='s', linestyle='None', markerfacecolor='r', markeredgecolor='k')
	plt.plot(her_coll_x, her_coll_y, marker='s', linestyle='None', markerfacecolor='b', markeredgecolor='k')

	plt.title("SuperKEKB")
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.grid(True)
	plt.legend()

# Plot Twiss parameters
def plot_twiss(data,ring):
	s_twiss = np.array(data['S'])
	ax_twiss = np.array(data['Ax'])
	ay_twiss = np.array(data['Ay'])
	bx_twiss = np.array(data['Bx'])
	by_twiss = np.array(data['By'])
	ex_twiss = np.array(data['Ex'])
	ey_twiss = np.array(data['Ey'])
	epx_twiss = np.array(data['EPx'])
	epy_twiss = np.array(data['EPy'])
	dx_twiss = np.array(data['Dx'])
	dy_twiss = np.array(data['Dy'])
	l_twiss = np.array(data['L'])

	# Create a figure and two subplots
	fig, ax = plt.subplots(2, 3, figsize=(16, 8))

	# alpha
	ax[0, 0].plot(s_twiss, ax_twiss, color='blue', linestyle='-', label="X")
	ax[0, 0].plot(s_twiss, ay_twiss, color='red', linestyle='--', label="Y")
	ax[0, 0].set_title(f"Twiss: {ring}")
	ax[0, 0].set_xlabel(r"S [m]")
	ax[0, 0].set_ylabel(r"$\alpha$")
	ax[0, 0].legend()
	ax[0, 0].grid(True)

	# beta
	ax[1, 0].plot(s_twiss, bx_twiss, color='blue', linestyle='-', label="X")
	ax[1, 0].plot(s_twiss, by_twiss, color='red', linestyle='--', label="Y")
	ax[1, 0].set_title(f"Twiss: {ring}")
	ax[1, 0].set_xlabel(r"S [m]")
	ax[1, 0].set_ylabel(r"$\beta$ [m]")
	ax[1, 0].legend()
	ax[1, 0].grid(True)

	# eta
	ax[0, 1].plot(s_twiss, ex_twiss, color='blue', linestyle='-', label="X")
	ax[0, 1].plot(s_twiss, ey_twiss, color='red', linestyle='--', label="Y")
	ax[0, 1].set_title(f"Twiss: {ring}")
	ax[0, 1].set_xlabel(r"S [m]")
	ax[0, 1].set_ylabel(r"$\eta$ [m]")
	ax[0, 1].legend()
	ax[0, 1].grid(True)

	# eta'
	ax[1, 1].plot(s_twiss, epx_twiss, color='blue', linestyle='-', label="X")
	ax[1, 1].plot(s_twiss, epy_twiss, color='red', linestyle='--', label="Y")
	ax[1, 1].set_title(f"Twiss: {ring}")
	ax[1, 1].set_xlabel(r"S [m]")
	ax[1, 1].set_ylabel(r"$\eta'$")
	ax[1, 1].legend()
	ax[1, 1].grid(True)

	# d
	ax[0, 2].plot(s_twiss, dx_twiss * 1e3, color='blue', linestyle='-', label="X")
	ax[0, 2].plot(s_twiss, dy_twiss * 1e3, color='red', linestyle='--', label="Y")
	ax[0, 2].set_title(f"Twiss: {ring}")
	ax[0, 2].set_xlabel(r"S [m]")
	ax[0, 2].set_ylabel(r"$D$ [mm]")
	ax[0, 2].legend()
	ax[0, 2].grid(True)

	# d
	ax[1, 2].plot(s_twiss, l_twiss, color='green', linestyle='-')
	ax[1, 2].set_title(f"Twiss: {ring}")
	ax[1, 2].set_xlabel(r"S [m]")
	ax[1, 2].set_ylabel(r"$L$ [m]")
	ax[1, 2].grid(True)

	# Adjust layout to prevent overlap
	plt.tight_layout()

# Adjust S coordinate [0;ring_length] -> [-ring_length/2;+ring_length/2]
def adjust_s(df):
	ring_length = df['S'].max() - df['S'].min()
	print(f"--> Ring length = {ring_length:.3f} [m]")
	# Replace S values greater than the half of the ring length
	df.loc[df['S'] > ring_length/2., 'S'] = df['S'] - ring_length
	# Sort the DataFrame by S in ascending order
	df_sorted = df.sort_values(by='S')
	# Reset the index if desired (optional)
	dff = df_sorted.reset_index(drop=True)
	return dff

# Draw magnets
def plot_magnets(data,title,signx,signy,signz):
	print(f"\n\n--> {title}")
	fig, ax = plt.subplots(figsize=(8, 8))
	ax.set_title(title)
	x_ler = signx*np.array(ler_data['Gx'])
	y_ler = signy*np.array(ler_data['Gy'])
	x_her = signx*np.array(her_data['Gx'])
	y_her = signy*np.array(her_data['Gy'])

	plt.plot(x_ler, y_ler, linestyle='-.', color='r', label="LER")
	plt.plot(x_her, y_her, linestyle='-.', color='b', label="HER")

	for row in data.itertuples():
		if (row.TypeName == 'BEND') & (row.L > 0.0) & (abs(row.S) < 50.0) & (abs(row.Angle) > 0.0):
			x1 = signx*row.Gx
			y1 = signy*row.Gy
			z1 = signz*row.Gz
			x0 = signx*data.iloc[row.Index+1].Gx
			y0 = signy*data.iloc[row.Index+1].Gy
			z0 = signz*data.iloc[row.Index+1].Gz
			w = 0.5 # [m]

			theta = np.arctan((y1 - y0) / (x1 - x0))
			xc = x0 + (w/2.) * np.sin(theta)
			yc = y0 - (w/2.) * np.cos(theta)

			linestyle = '-'
			edgecolor = 'black'
			linewidth = 2
			if abs(row.Rot) > 0:
				linestyle = '--'
				edgecolor = 'gray' 
				linewidth = 1

			rect = patches.Rectangle((xc, yc), row.L, w, angle=(theta*180.0/math.pi), 
				linewidth=linewidth, linestyle=linestyle, edgecolor=edgecolor, facecolor='none')

			ax.add_patch(rect)
			plt.plot([x0, x1],[y0, y1],'-');
			plt.plot([x0],[y0],marker='o',color='r');
			plt.plot([x1],[y1],marker='s',color='b');

			print(f"  {row.NAME} : length = {row.L:.6e} [m]; angle = {row.Angle:.6e} [rad]; K0 = {row.K0:.6e}; rot = {row.Rot:.6e} [rad]; (Gx;Gy;Gz)[0] = ({x0:.6e};{y0:.6e};{z0:.6e}) [m]; (Gx;Gy;Gz)[1] = ({x1:.6e};{y1:.6e};{z1:.6e}) [m]")

	ax.grid(True)
	plt.xlim(-50, 50)
	plt.ylim(-2, 2)

# Main function to run the script
if __name__ == '__main__':
	her_filename = 'sher_2021-06-16_1.0A_1x60_nb_1576_cw_40.survey'
	ler_filename = 'sler_2021-06-16_1.2A_1x80_nb_1576_cw_80.survey'

	her_data = adjust_s(pd.read_csv(her_filename, sep='\s+'))
	ler_data = adjust_s(pd.read_csv(ler_filename, sep='\s+'))

	print("\n====  HER ====")
	print(her_data.head())
	print("\n====  LER ====")
	print(ler_data.head())
	plot_rings(ler_data,her_data,-1,-1)

	plot_twiss(ler_data,'LER')
	plot_twiss(her_data,'HER')

	plot_magnets(her_data,'HER',-1,-1,-1)
	plot_magnets(ler_data,'LER',-1,-1,-1)

	plt.show()

