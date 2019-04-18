#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:59:24 2019

@author: katerina
"""

from libtiff import TIFF
import cv2
import matplotlib.pyplot as plt


# read all images in a TIFF file:
count = 0
count_list = []
area_list = []
area_changes_list = []
prev_contour_area = 0

for j in range (15,16): #boundary value
    
    tif = TIFF.open('ant1.tif') # open tiff file in read mode

    for image in tif.iter_images(): #for one image in all tif images
        count += 1 #counts the number of images
        str_count=str(count) # transfrom int to str
        
        im = image
        img_one_shape = image
        
        #boundary value
        boundary = j
        str_boundary = str(boundary)
        
        ret, thresh= cv2.threshold(im,boundary,255,cv2.THRESH_BINARY)
        im, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        
        if (0 <= count <= 300): #select a region without blinks
            for i in range (1, len(contours)) : #skip first contour since it is the hole image
                contour = contours[i]
                contour_area = cv2.contourArea(contour)
                rep = 0 #counts the number 
                if contour_area > 80000: #min contour area - determined by the user
                    rep += 1
                    count_list.append(count)
                    area_list.append(contour_area)
                    area_changes_list.append(contour_area - prev_contour_area)
                    cv2.drawContours(img_one_shape, contours, i, (55,255,0), 1)
                    cv2.imwrite(str_count + '_one_shape_boundary_' + str_boundary + '.jpg', img_one_shape) #initial img with contours
        
                    with open('pupil_area_ant1_boundary_' + str_boundary + '.txt', 'a+') as f:
                        print (" img = ",count," number of contours= ", len(contours),"rep = " ,rep, " pupil_area ",contour_area, file=f)
                    f.close()  
                    
                    with open('pupil_area_changes_ant1_boundary_' + str_boundary + '.txt', 'a+') as f:
                        print (" img = ",count, " pupil_area_changes ",contour_area - prev_contour_area, file=f)
                    f.close() 
                    
                    prev_contour_area = contour_area

    #plot results
    plt.plot(count_list ,area_list ,'go-',label="line 1")
    plt.xlabel('Image')
    plt.ylabel('Pupil area')
    plt.title('Pupil area with boundary' + str_boundary) 
    plt.savefig('pupil-area_ant1_boundary_' + str_boundary + '.jpg')
    plt.close("all")
    
    plt.plot(count_list[1:] ,area_changes_list[1:],'go-',label="line 1")
    plt.xlabel('Image ')
    plt.ylabel('Pupil area changes')
    plt.title('Pupil area changes with boundary'  + str_boundary) 
    plt.savefig('pupil-area-changes_ant1_boundary_' + str_boundary + '.jpg')
    plt.close("all")