import numpy as np
import matplotlib.pyplot as plt

# Function to read the file and parse the data
def read_data(filename):
	data = {
		'NAME': [], 'S': [], 'Gx': [], 'Gy': [], 'Gz': [], 'OGx': [], 'OGy': [], 'OGz': [],
		'Ax': [], 'Bx': [], 'Nx': [], 'Ex': [], 'EPx': [], 'Ay': [], 'By': [], 'Ny': [], 'Ey': [], 'EPy': [],
		'L': [], 'Type': [], 'TypeName': [], 'Angle': [], 'K1': [], 'Rot': [], 'Dx': [], 'Dy': []
	}
	with open(filename, 'r') as file:
		next(file)  # Skip the header line
		for line in file:
			# Split the line by spaces and remove extra whitespaces
			parts = line.split()
			for index, key in enumerate(data):
				if key == "NAME" or key == "TypeName":
					data[key].append(parts[index])
				else:
					data[key].append(float(parts[index]))
	return data

# Rotate coordinates
def rotate(x_orig,y_orig,rot_ang):
	x_rot = x_orig * np.cos(rot_ang) - y_orig * np.sin(rot_ang)
	y_rot = x_orig * np.sin(rot_ang) + y_orig * np.cos(rot_ang)
	return (x_rot,y_rot)

# Plot Gx vs Gy
def plot_skb(ler_data,her_data,signx,signy):
	rot_ang = 0 #np.float64(8.5e-3)
	plt.figure(figsize=(8, 8))

	ler_coll_indices = [i for i, name in enumerate(ler_data['NAME']) if name.startswith("PMD")]
	her_coll_indices = [i for i, name in enumerate(her_data['NAME']) if name.startswith("PMD")]

	ler_coll_x_orig = signx*np.array([ler_data['Gx'][i] for i in ler_coll_indices])
	ler_coll_y_orig = signy*np.array([ler_data['Gy'][i] for i in ler_coll_indices])
	her_coll_x_orig = signx*np.array([her_data['Gx'][i] for i in her_coll_indices])
	her_coll_y_orig = signy*np.array([her_data['Gy'][i] for i in her_coll_indices])

	ler_coll_x, ler_coll_y = rotate(ler_coll_x_orig,ler_coll_y_orig,rot_ang)
	her_coll_x, her_coll_y = rotate(her_coll_x_orig,her_coll_y_orig,rot_ang)

	x_orig = signx*np.array(ler_data['Gx'])
	y_orig = signy*np.array(ler_data['Gy'])
	x_ler, y_ler = rotate(x_orig,y_orig,rot_ang)

	x_orig = signx*np.array(her_data['Gx'])
	y_orig = signy*np.array(her_data['Gy'])
	x_her, y_her = rotate(x_orig,y_orig,rot_ang)

	x_orig = signx*np.array(ler_data['OGx'])
	y_orig = signy*np.array(ler_data['OGy'])
	ox_ler, oy_ler = rotate(x_orig,y_orig,rot_ang)

	x_orig = signx*np.array(her_data['OGx'])
	y_orig = signy*np.array(her_data['OGy'])
	ox_her, oy_her = rotate(x_orig,y_orig,rot_ang)

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
	plt.show()

# Main function to run the script
if __name__ == '__main__':
	her_filename = 'sher_2021-06-16_1.0A_1x60_nb_1576_cw_40.survey'
	ler_filename = 'sler_2021-06-16_1.2A_1x80_nb_1576_cw_80.survey'
	her_data = read_data(her_filename)
	ler_data = read_data(ler_filename)
	plot_skb(ler_data,her_data,-1,-1)

