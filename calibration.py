import cv2
import numpy as np
import glob

# Chessboard dimensions
chessboard_size = (7, 7)
square_size = 30

# Prepare object points
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

objpoints = []
imgpoints = []

# Load images
images = glob.glob(r"C:\Users\Vignesh\OneDrive\Desktop\OPENCVPROJECT\calibration_image\*.jpeg")

print("Images found:", images)

gray = None

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(
        gray, chessboard_size,
        flags=cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)

        # Resize image to fit laptop screen (e.g., 1366x768)
        screen_width = 1366
        screen_height = 768
        h, w = img.shape[:2]
        scale = min(screen_width / w, screen_height / h)
        img_resized = cv2.resize(img, (int(w * scale), int(h * scale)))

        # Show in resizable window
        cv2.namedWindow("Chessboard", cv2.WINDOW_NORMAL)
        cv2.imshow("Chessboard", img_resized)
        cv2.waitKey(1000)  # wait 1 sec to take screenshot

cv2.destroyAllWindows()

# Calibration
if gray is not None and objpoints and imgpoints:
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    np.savez("camera_calibration.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)

    print("Camera matrix:\n", camera_matrix)
    print("Distortion coefficients:\n", dist_coeffs)
else:
    print("Error: No valid images found for calibration. Check your image paths and chessboard pattern.")

