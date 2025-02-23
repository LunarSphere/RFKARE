import cv2
import numpy as np
import time
import os
import pandas as pd
from IPython.display import Image, display  # For displaying images in Jupyter
import re

def preprocess_image(image_path):
    """
    Load and preprocess the aerial image
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    scale_factor = 0.5
    height, width = image.shape[:2]
    new_size = (int(width * scale_factor), int(height * scale_factor))
    image_resized = cv2.resize(image_rgb, new_size, interpolation=cv2.INTER_AREA)
    return image_resized

def segment_buildings(image):
    """
    Segment potential building areas using color and edge detection
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower_building = np.array([0, 0, 50])    
    upper_building = np.array([180, 50, 200])
    mask = cv2.inRange(hsv, lower_building, upper_building)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

def count_buildings(mask, min_area=75):
    """
    Count buildings based on contours in the segmented mask
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    building_count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) >= 4:
                building_count += 1
    return building_count

def process_image(image_path):
    """
    Process a single image and return building count (no display)
    """
    try:
        start_time = time.time()
        image = preprocess_image(image_path)
        mask = segment_buildings(image)
        building_count = count_buildings(mask)
        execution_time = time.time() - start_time
        return building_count, execution_time
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return 0, 0  # Return 0 buildings if error occurs

def process_all_images(data_folder):
    """
    Process all images in the data folder and save results to CSV
    """
    # List to store results
    results = []
    bcs = {}
    
    # Regex pattern to extract row and col from filename
    pattern = r'gee_image_row(\d+)_col(\d+)\.png'
    
    # Iterate through all files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith('.png'):
            # Extract row and col from filename
            match = re.match(pattern, filename)
            if match:
                row = int(match.group(1))
                col = int(match.group(2))
                
                # Full path to image
                image_path = os.path.join(data_folder, filename)
                
                # Process image
                building_count, _ = process_image(image_path)
                
                # Store result
                results.append({
                    'image_name': filename,
                    'row': row,
                    'col': col,
                    'building_count': building_count,
                })
                bcs[(row, col)] = building_count
            else:
                print(f"Skipping {filename}: does not match expected naming pattern")
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(results)
    output_csv = 'building_counts.csv'
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
    
    # Display the DataFrame in Jupyter
    display(df)
    
    return bcs