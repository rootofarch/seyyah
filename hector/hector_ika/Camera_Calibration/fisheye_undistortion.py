import cv2
import numpy as np
import sys


# You should replace these 3 lines with the output in calibration step
DIM=(800, 600)
K=np.array([[337.7289115144896, 0.0, 399.713530794396], [0.0, 337.7056705555252, 298.3935207374622], [0.0, 0.0, 1.0]])
D=np.array([[0.07785624707613907], [0.03817987944876708], [-0.061388108802514295], [0.04096004118965009]])

def undistort(img_path, balance=0.0, dim2=None, dim3=None):

    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort

    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"

    if not dim2:
        dim2 = dim1

    if not dim3:
        dim3 = dim1

    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.

    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0

    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    height, width = undistorted_img.shape[:2]
    undistorted_img = cv2.resize(undistorted_img,(2*width, 2*height), interpolation = cv2.INTER_CUBIC)

    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    for p in sys.argv[1:]:
        undistort(p)