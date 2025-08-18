import cv2
import numpy as np

# Define the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)  # Using 6x6 dictionary with 250 markers
marker_size = 500  # Size of the marker in pixels

# Function to generate and save an ArUco marker
def generate_aruco_marker(marker_id, marker_size, output_file):
    marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size, marker_image, 1)
    cv2.imwrite(output_file, marker_image)
    print(f"ArUco marker with ID {marker_id} saved as {output_file}")

# Generate three ArUco markers with IDs 23, 24, and 25
generate_aruco_marker(23, marker_size, "aruco_marker_23.png")
generate_aruco_marker(24, marker_size, "aruco_marker_24.png")
generate_aruco_marker(25, marker_size, "aruco_marker_25.png")

print("All markers generated successfully!")
