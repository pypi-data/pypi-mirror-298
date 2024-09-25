import os
import cv2
import csv
import math
import tifffile
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.draw import polygon
from sklearn.cluster import KMeans
from PyQt5.QtWidgets import QMessageBox
from scipy.ndimage import center_of_mass
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import warnings
warnings.filterwarnings('ignore')


def bw_correction(image, rectangle, color):
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    if color == 'black':
        image = 255 - image
        
    if rectangle != None:
        rectangle = rectangle.data
        x0 = int(rectangle[0][0][0])
        y0 = int(rectangle[0][0][1])
        x1 = int(rectangle[0][2][0])
        y1 = int(rectangle[0][2][1])

        image_patch = image[x0:x1, y0:y1]
    else:
        image_patch = image
    image_max = (image*1.0 / image_patch.max(axis=(0, 1))).clip(0, 1)
    image_max = np.asarray(image_max*255).astype('uint8')
    
    if color == 'black':
        image_max = 255 - image_max

    return image_max


def rgb_correction(image, rectangle, color):
    if color == 'red':
        index = 0
    elif color == 'green':
        index = 1
    elif color == 'blue':
        index = 2
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    if rectangle != None:
        rectangle = rectangle.data
        x0 = int(rectangle[0][0][0])
        y0 = int(rectangle[0][0][1])
        x1 = int(rectangle[0][2][0])
        y1 = int(rectangle[0][2][1])

        image_patch = image[x0:x1, y0:y1, index]
    else:
        image_patch = image[:,:,index]
    image_max = (image[:,:,index]*1.0 / image_patch.max(axis=(0, 1))).clip(0, 1)

    im_res = np.zeros(image.shape, dtype=np.uint8)
    for i in range(3):
        if i == index:
            im_res[:,:,i] = np.asarray(image_max*255).astype('uint8')
        else:
            im_res[:,:,i] = image[:,:,i]
    return im_res


def cmy_correction(image, rectangle, color):
    if color == 'yellow':
        indexes = [0, 1]
    elif color == 'magenta':
        indexes = [0, 2]
    elif color == 'cyan':
        indexes = [1, 2]
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    
    if rectangle != None:
        rectangle = rectangle.data
        x0 = int(rectangle[0][0][0])
        y0 = int(rectangle[0][0][1])
        x1 = int(rectangle[0][2][0])
        y1 = int(rectangle[0][2][1])

    im_res = np.zeros(image.shape, dtype=np.uint8)
    for index in indexes:
        image_copy = image.copy()
        if rectangle != None:
            image_patch = image[x0:x1, y0:y1, index]
        else:
            image_patch = image[:,:,index]
        image_max = (image_copy[:,:,index]*1.0 / image_patch.max(axis=(0, 1))).clip(0, 1)
        
        for i in range(3):
            if i == index:
                im_res[:,:,i] = np.asarray(image_max*255).astype('uint8')
    
    for i in range(3):
        if i not in indexes:
            im_res[:,:,i] = image[:,:,i]
        
    return im_res

################################################################

def set_cm_scale(line):
    d = math.dist(line[0][0],line[0][1])
    # Message pop-up when analysis is finished
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Information)
    msg.setText("Scale saved!")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_() 
    return d

################################################################

def classify_pixelcolor(pixel):
    # Define thresholds for black, white, and orange in RGB
    black_threshold = 100
    white_threshold = 200
    white_lower = np.array([0, 100, 200]) # which is almost blue becuase most of the time the background is light blue
    orange_lower = np.array([100, 40, 0])
    orange_upper = np.array([255, 230, 65])
    
    if np.all(pixel <= black_threshold):
        return 'black'
    elif np.all(pixel >= white_threshold):
        return 'white'
    elif np.all(pixel >= orange_lower) and np.all(pixel <= orange_upper):
        return 'orange'
    else:
        if np.all(pixel >= white_lower):
            return 'white'
        return 'black'


def maincolors_analysis(masked_image, background_px):
    black_px_withbackground = 0
    white_px = 0
    orange_px = 0

    res_image = masked_image.copy()

    for x in range(masked_image.shape[1]):
        for y in range(masked_image.shape[0]):
            pixel = masked_image[y,x,:]
            color_class = classify_pixelcolor(pixel)
            if color_class == 'black':
                res_image[y,x,:] = (0,0,0)
                black_px_withbackground += 1
            elif color_class == 'white':
                res_image[y,x,:] = (255,255,255)
                white_px += 1
            elif color_class == 'orange':
                res_image[y,x,:] = (255,140,0)
                orange_px += 1
            elif color_class == 'other':
                res_image[y,x,:] = (0,140,255)
                orange_px += 1
    
    black_px = black_px_withbackground - background_px
    tot_px = black_px + white_px + orange_px
    
    return res_image, tot_px, black_px, white_px, orange_px

################################################################

def color_analysis(image, mask_init, landmarks, output_path, image_name, scale):
    support_dir = os.path.join(output_path, 'support_images')
    if not os.path.exists(support_dir):
        os.mkdir(support_dir)
    resized_dir = os.path.join(output_path, 'images_samesize')
    if not os.path.exists(resized_dir):
        os.mkdir(resized_dir)
    boxes_dir = os.path.join(output_path, 'images_boxes')
    if not os.path.exists(boxes_dir):
        os.mkdir(boxes_dir)

    ## CSV CREATION
    if not 'color_analysis.csv' in os.listdir(output_path):
        with open(os.path.join(output_path, 'color_analysis.csv'), "w") as file:
            writer = csv.writer(file)
            writer.writerow(['Image', 'len fish [px]', 'len fish [cm]',
                             'mask area', 'black[%]', 'white[%]', 'orange[%]',
                             'box1 area', 'box1 black[%]', 'box1 white[%]', 'box1 orange[%]',
                             'box2 area', 'box2 black[%]', 'box2 white[%]', 'box2 orange[%]',
                             'box3 area', 'box3 black[%]', 'box3 white[%]', 'box3 orange[%]'])
    
    
    ## DATA PREPARATION
    # Read the image and the mask correctly and find contour
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    mask_init = mask_init.astype('uint8')
    landmarks = landmarks.astype('uint8')
    # Keep only the bigger contour found
    contours, _ = cv2.findContours(mask_init, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    max_contour = max(contours, key=cv2.contourArea)
    out = np.zeros(mask_init.shape, np.uint8)
    mask_fish = cv2.drawContours(out, [max_contour], -1, 255, cv2.FILLED)
    # Mask the image with the mask
    masked_image = cv2.bitwise_and(image, image, mask=mask_fish)

    ## SAVE SUPPORT IMAGE
    save_support_image(masked_image, mask_fish, support_dir, image_name)
    
    ## MEASURE FISH LENGTH
    fish_len_px, fish_len_cm, rectangle = measure_length(max_contour, scale)

    ## MEASURE COLORS IN FISH LANDMARKS BOXES
    csv_line_boxes = boxes_analysis(image, mask_fish, landmarks, boxes_dir, image_name)

    ## ROTATE THE FISH
    masked_image_rotated, mask_rotated = fish_rotation(mask_fish, masked_image, rectangle)

    ## CROP FISH
    gray_rotated = cv2.cvtColor(masked_image_rotated, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = cv2.boundingRect(contours[0])
    masked_image_rotated_cropped = masked_image_rotated[y:y+h,x:x+w]
    mask_rotated_cropped = mask_rotated[y:y+h,x:x+w]
    # Number of black pixels in the background (out of the mask)
    background_pixels = np.count_nonzero(mask_rotated_cropped == 0)

    ## SAVE RESIZED FISH
    save_resized(masked_image_rotated_cropped, resized_dir, image_name)
    
    ## COLOR ANALYSIS (save independently the figures)
    try: 
        colors_plot(masked_image_rotated_cropped, output_path, image_name, background_pixels)
        csv_line_image = colors_distribution_pie(masked_image_rotated_cropped, mask_rotated_cropped, output_path, image_name, background_pixels)
    except Exception as e: 
        print(e)
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Finished with error(s)\nsee the command prompt for details.")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()
    
    # Write csv complete line
    csv_line = [image_name, fish_len_px, fish_len_cm]
    csv_line.extend(csv_line_image)
    csv_line.extend(csv_line_boxes)
    with open(os.path.join(output_path, 'color_analysis.csv'), "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_line)
        
    # Pop-up message when the analysis is finished
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Information)
    msg.setText("Analysis saved!")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()


def save_support_image(image, masktosave, support_dir, image_name):
    composite = np.zeros((2, image.shape[0], image.shape[1], image.shape[2]), dtype=np.uint8)
    composite[0] = image
    composite[1,:,:,0] = masktosave
    composite[1,:,:,1] = masktosave
    composite[1,:,:,2] = masktosave
    tifffile.imwrite(os.path.join(support_dir, image_name+'.tif'), composite, imagej=True)


def measure_length(max_contour, scale):
    rectangle = cv2.minAreaRect(max_contour)
    _, (width,height), _ = rectangle
    fish_len_px = np.max([width,height])
    fish_len_cm = round(fish_len_px/scale, 2) if scale else None # scale = pixels per cm
    return round(fish_len_px, 2), fish_len_cm, rectangle


def fish_rotation(mask_fish, masked_image, rectangle):
    (center), (width,height), angle = rectangle
    box = cv2.boxPoints(rectangle)
    box = np.intp(box)
    if width < height:
        angle += 90  # Ensure the longest side is horizontal
    # Rotate the image to make the fish horizontal
    (h, w) = mask_fish.shape
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    masked_image_rotated = cv2.warpAffine(masked_image, M, (w, h))
    mask_rotated = cv2.warpAffine(mask_fish, M, (w, h))
    # After rotation, find contours again to determine the correct orientation
    gray_rotated = cv2.cvtColor(masked_image_rotated, cv2.COLOR_BGR2GRAY)
    contours_rotated, _ = cv2.findContours(gray_rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_rotated = max(contours_rotated, key=cv2.contourArea)
    # Get the extreme points of the contour (leftmost and rightmost points)
    leftmost = tuple(contour_rotated[contour_rotated[:, :, 0].argmin()][0])
    rightmost = tuple(contour_rotated[contour_rotated[:, :, 0].argmax()][0])
    # If the mouth is on the right, flip the image horizontally
    if leftmost[0] > rightmost[0]:
        masked_image_rotated = cv2.flip(masked_image_rotated, 1)
        mask_rotated = cv2.flip(mask_rotated, 1)
    return masked_image_rotated, mask_rotated


def save_resized(masked_image_rotated_cropped, output_path, image_name):
    tosave = cv2.resize(masked_image_rotated_cropped, (2000,1000))
    resized_image = Image.fromarray(tosave)
    resized_image.save(os.path.join(output_path, image_name+'.jpg'))


def boxes_analysis(image, mask_fish, landmarks_image, output_path, image_name):
    landmarks = {}
    for num in range(1,29):
        com = center_of_mass(landmarks_image, labels=landmarks_image, index=num)
        landmarks[num] = com
    
    boxes_image = image.copy()
    boxes = [[3,14,15,26,27,6], [16,17,18,19,22,23,24,25], [19,20,21,22]]

    csv_line_boxes = []
    for i, box_nums in enumerate(boxes):
        # Find coordinates of the box
        r = [landmarks[num][0] for num in box_nums]
        c = [landmarks[num][1] for num in box_nums]
        # Draw the box
        box = np.zeros(mask_fish.shape, dtype=np.uint8)
        rr, cc = polygon(r, c, box.shape)
        box[rr, cc] = 1
        contours, _ = cv2.findContours(box.astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if i==0: boxes_image = cv2.drawContours(boxes_image, contours, -1, (255,0,0), 4)
        elif i==1: boxes_image = cv2.drawContours(boxes_image, contours, -1, (255,255,0), 4)
        elif i==2: boxes_image = cv2.drawContours(boxes_image, contours, -1, (0,255,0), 4)

        # Exclude pixels that are out of the fish mask
        box[mask_fish == 0] = 0
        # Mask the image and anlyse the colors
        masked_image = cv2.bitwise_and(image, image, mask=box)
        # Classify each pixel in the image
        background_px = np.count_nonzero(box == 0)
        _, tot_px, black_px, white_px, orange_px = maincolors_analysis(masked_image, background_px)
        # area, black[%], white[%], orange[%]
        csv_line_boxes.append(np.count_nonzero(box == 1))
        csv_line_boxes.append(round((black_px)/tot_px*100, 2))
        csv_line_boxes.append(round((white_px)/tot_px*100, 2))
        csv_line_boxes.append(round((orange_px)/tot_px*100, 2))
    
    Image.fromarray(boxes_image).save(os.path.join(output_path, image_name+'-boxes.jpg'))
    return csv_line_boxes
        
    
def colors_plot(masked_image, output_path, image_name, background_pixels):
    def find_minimum_color(colors):
        # Function to calculate the sum of RGB components
        def rgb_sum(color):
            return sum(color)

        # Use the min function with a key parameter to find the color with the smallest sum of components
        min_color = min(colors, key=rgb_sum)
        return min_color
    
    # Preprocess the image
    masked_image = masked_image.reshape((masked_image.shape[0] * masked_image.shape[1], 3))
    # Apply K-means clustering
    num_colors = 5  # Number of colors to extract
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(masked_image)

    # Get the colors
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # Create a histogram of the color labels
    label_counts = np.bincount(labels)
    
    # Sort colors by frequency
    sorted_indices = np.argsort(label_counts)[::-1]
    colors = colors[sorted_indices]
    label_counts = label_counts[sorted_indices]
    
    # Create a figure
    plt.figure(figsize=(8, 6))
    
    # Plot each color as a bar
    black = find_minimum_color(colors)
    tosave_colors = []
    for i, color in enumerate(colors):
        tosave_colors.append([int(c) for c in color])
        color = [abs(c) for c in color]
        if np.sum(color) == np.sum(black):
            plt.barh(i, label_counts[i]-background_pixels, color=np.array(color)/255, edgecolor='black')
        else:
            plt.barh(i, label_counts[i], color=np.array(color)/255, edgecolor='black')
    
    
    plt.xlabel('Pixel Count')
    plt.ylabel('Color')
    plt.title('Colors in Image')
    plt.yticks(np.arange(0, num_colors), tosave_colors)
    plt.savefig(os.path.join(output_path, image_name+'-colors'), bbox_inches='tight', dpi=200)
    plt.close()


def colors_distribution_pie(masked_image, mask, output_path, image_name, background_pixels):
    res_image, tot_px, black_px, white_px, orange_px = maincolors_analysis(masked_image, background_pixels)
    
    # Plot the results as a donut chart
    #labels = ['Black', 'White', 'Orange']
    sizes = [black_px, white_px, orange_px]
    colors = ['#000000', '#FFFFFF', '#FF8C00']
    
    fig, ax = plt.subplots()
    _,_,m = ax.pie(sizes, autopct='%1.1f%%', pctdistance=0.9, colors=colors, startangle=90, wedgeprops=dict(width=0.3, edgecolor='gray'))
    m[0].set_color('white')
    # Draw a circle at the center to make it look like a donut
    center_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(center_circle)

    # Add the image to the center of the donut
    res_image[mask == 0] = (255,255,255)
    res_image = cv2.medianBlur(res_image, 7)
    contours, _ = cv2.findContours(mask.astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    res_image = cv2.drawContours(res_image, contours, -1, (255,0,0), 4)
    imagebox = OffsetImage(res_image, zoom=0.05)
    ab = AnnotationBbox(imagebox, (0, 0), frameon=False)
    ax.add_artist(ab)

    ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Dominant Colors Distribution')
    plt.savefig(os.path.join(output_path, image_name+'-colors_distribution.png'), bbox_inches='tight', dpi=200)
    plt.close()

    # 'mask area', 'black[%]', 'white[%]', 'orange[%]'
    return [tot_px, round((black_px)/tot_px*100, 2), round((white_px)/tot_px*100, 2), round((orange_px)/tot_px*100, 2)]


################################################################

def lock_controls(layer, viewer, widget_list, locked=True):
    qctrl = viewer.window.qt_viewer.controls.widgets[layer]
    for wdg in widget_list:
        getattr(qctrl, wdg).setEnabled(not locked)
        # or setVisible() if you want to just hide them completely

################################################################

if __name__ == '__main__':
    comp_image = tifffile.imread('/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/results/support_images/1123a.tif')
    landmarks_mask = tifffile.imread('/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/results/support_images/landmarks_1123a.tif')
    mask = cv2.cvtColor(comp_image[1], cv2.COLOR_BGR2GRAY)
    
    color_analysis(comp_image[0], mask, landmarks_mask, '/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/results', 'test-1123a', 1)
    #print(boxes_analysis(comp_image[0], mask, landmarks_mask))