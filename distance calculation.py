import cv2
import numpy as np

# Camera intrinsic parameters (Replace with actual calibration data)
camera_matrix = np.array([[4.16204732e+04, 0.00000000e+00, 4.98561925e+02],
                          [0.00000000e+00, 7.10592438e+04, 5.91107184e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Example camera matrix

dist_coeffs = np.array([[1.90104775e+02], [-1.79426321e+01], [-5.71391780e-02], 
                        [-1.21884114e+00], [-1.19207076e-02]])  # Example distortion coefficients

# Load ArUco dictionary and detector parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

# Pixel-to-mm conversion factor (Modify based on your setup)
PIXEL_TO_MM = 0.5  # Example: 1 pixel = 0.5 mm (needs calibration)

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()  # Exit if the camera is not accessible

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if frame is not captured

    # Detect ArUco markers
    corners, ids, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if ids is not None and len(ids) >= 2:  # Ensure at least two markers are detected
        # Define colors for the markers
        colors = [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 165, 255)]  # Yellow, Pink, Cyan, Orange

        # Get the centers of the first two detected markers
        center1 = np.mean(corners[0][0], axis=0).astype(int)
        center2 = np.mean(corners[1][0], axis=0).astype(int)

        # Draw circles on detected markers
        cv2.circle(frame, tuple(center1), 10, colors[0], -1)
        cv2.circle(frame, tuple(center2), 10, colors[1], -1)

        # Draw a line between the two markers
        cv2.line(frame, tuple(center1), tuple(center2), (0, 0, 255), 2)  # Red line

        # Draw X and Y axes at each marker position
        cv2.line(frame, (center1[0], 0), (center1[0], frame.shape[0]), (255, 0, 0), 2)  # Blue Y-axis (marker 1)
        cv2.line(frame, (0, center1[1]), (frame.shape[1], center1[1]), (0, 255, 0), 2)  # Green X-axis (marker 1)

        cv2.line(frame, (center2[0], 0), (center2[0], frame.shape[0]), (255, 0, 0), 2)  # Blue Y-axis (marker 2)
        cv2.line(frame, (0, center2[1]), (frame.shape[1], center2[1]), (0, 255, 0), 2)  # Green X-axis (marker 2)

        # Compute Euclidean pixel distance
        pixel_distance = np.linalg.norm(center2 - center1)

        # Convert pixel distance to real-world mm using scaling factor
        distance_mm = pixel_distance * PIXEL_TO_MM

        print(f"Pixel Distance: {pixel_distance:.2f} px, Real Distance: {distance_mm:.2f} mm")

        # Draw detected markers
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Display distance in bottom-right corner
        cv2.putText(frame, f"Distance: {distance_mm:.2f} mm", (frame.shape[1] - 300, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        # Display message if less than 2 markers are detected
        cv2.putText(frame, "At least 2 markers required", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Exit cleanly when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Break out of the loop

# Cleanup
cap.release()
cv2.destroyAllWindows()

