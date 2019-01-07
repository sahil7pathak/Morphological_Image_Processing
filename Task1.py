import numpy as np
import cv2

'''Erosion Method'''
def erosion(image, kernel):
    img_height = image.shape[0]
    img_width = image.shape[1]
    
    kernel_height = kernel.shape[0]
    kernel_width = kernel.shape[1]
    
    h = kernel_height//2
    w = kernel_width//2
    
    res = [[0 for x in range(img_width)] for y in range(img_height)] 
    res = np.array(res)
    for i in range(h, img_height-h):
        for j in range(w, img_width-w):
            a = np.array(image[(i-h):(i-h)+kernel_height, (j-w):(j-w)+kernel_width])
            if(np.array_equal(a, kernel)):
                res[i][j] = 1
            else:
                res[i][j] = 0
    return res

'''Dilation Method'''
def dilation(image, kernel):
    img_height = image.shape[0]
    img_width = image.shape[1]
    
    kernel_height = kernel.shape[0]
    kernel_width = kernel.shape[1]
    
    h = kernel_height//2
    w = kernel_width//2
    
    res = [[0 for x in range(img_width)] for y in range(img_height)] 
    res = np.array(res)
    for i in range(h, img_height-h):
        for j in range(w, img_width-w):
            a = np.array(image[(i-h):(i-h)+kernel_height, (j-w):(j-w)+kernel_width])
            if(np.max(a) == 1) :
                res[(i-h):(i-h)+kernel_height, (j-w):(j-w)+kernel_width] = 1
            else:
                res[(i-h):(i-h)+kernel_height, (j-w):(j-w)+kernel_width] = 0
    return res
    

'''Accepting image as grayscale image'''
img = cv2.imread("noise.jpg",0)
sample = img

'''Converting image to binary'''
img = img/255

'''kernel is of the order (3, 3) where the middle element is considered to be the origin'''
kernel = np.ones((3,3))
kernel.dtype

'''Operation 1: Opening then Closing, i.e. Erosion then Dilation, Dilation then Erosion'''
e1 = erosion(img, kernel)
d1 = dilation(e1, kernel)
d2  = dilation(d1, kernel)
e2 = erosion(d2, kernel)
bound_e2 = e2
e2 = e2*255
e2 = np.asarray(e2, np.uint8)
cv2.imwrite("res_noise1.jpg",e2)

'''Operation 2: Closing then Opening, i.e. Dilation then Erosion, Erosion then Dilation'''
dil1 = dilation(img, kernel)
er1 = erosion(dil1, kernel)
er2 = erosion(er1, kernel)
dil2 = dilation(er2, kernel)
bound_dil2 = dil2
dil2 = dil2*255
dil2 = np.asarray(dil2, np.uint8)
cv2.imwrite("res_noise2.jpg",dil2)

'''Boundary Detection'''
'''1. Extract the boundaries from res_noise1.jpg i.e. Output of first operation'''
kernel = np.ones((3,3))
bound1 = erosion(bound_e2, kernel)
bound_out = bound_e2 - bound1
bound_out *= 255
bound_out = np.asarray(bound_out, np.uint8)
cv2.imwrite("res_bound1.jpg",bound_out)

'''2. Extract the boundaries from res_noise2.jpg i.e. Output of second operation'''
bound2 = erosion(bound_dil2, kernel)
bound_out_ = bound_dil2 - bound2
bound_out_ *= 255
bound_out_ = np.asarray(bound_out_, np.uint8)
cv2.imwrite("res_bound2.jpg", bound_out_)

