"""
This program is intended for segmenting the entire dataset and running them through the Black Box NN SDK.
We prioritize processing .png files natively in BNE, MY, MMY, PMY, & SNE to ensure highest mask quality,
and fall back to .jpg variants if a .png equivalent isn't found. The remaining folders heavily rely on .jpg.

Perform the following for the code to work:
- Adjust the DATASET_PATH variable to point to the correct location of the dataset. (located in the main function)
- Outputs will be saved in a subfolder of the folder containing the scripts called: "student_mask".
- Adjust the multiprocessing part, specifically the variable "cores_to_use" depending on your device specifications, by default it uses half your CPU cores.
"""



# Python Standard Libraries
import os
import time
from pathlib import Path
from multiprocessing import Pool, cpu_count

# External Libraries [OpenCV, NumPy, tqdm]
import cv2              # Computer Vision Library   | Used for color space conversion, noise reduction, thresholding, and contour filtering.
import numpy as np      # Numerical Python Library  | Used for array manipulation and mathematical calculations.
from tqdm import tqdm   # Progress Bar              | Used to display the progress of the pipeline.

def process_single_image(args):
    """
    Applies the user-defined pipeline to a single image:
    LAB -> Bilateral Filter -> K-Means (k=3) -> Contour Filtering -> White Background
    """
    img_path, out_dir = args
    img_path = Path(img_path)
    
    # 1. Load the original image
    img = cv2.imread(str(img_path))
    if img is None:
        return False
        
    # Main Image Processing Component
    # =============================================================================
    # 2. Conversion to LAB
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    
    # 3. Bilateral Noise Reduction
    denoised_img = cv2.bilateralFilter(lab_image, 55, 150, 150)
    
    # 4. K-Means Thresholding (k=3)
    pixel_values = denoised_img.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.7)
    _, labels, centers = cv2.kmeans(pixel_values, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Stained cell nuclei are the darkest, so we check the Luminance (L) channel (index 0 in LAB)
    center_brightness = np.sum(centers, axis=1)
    fg_cluster = np.argmin(center_brightness)
    
    labels_flat = labels.flatten()
    mask = np.where(labels_flat == fg_cluster, 255, 0).astype(np.uint8)
    raw_mask = mask.reshape(img.shape[:2])
    
    # 5. Contour Filtering or Closing
    # contours, _ = cv2.findContours(raw_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 
    # cleaned_mask = np.zeros_like(raw_mask)
    # if contours:
    #     for contour in contours:
    #         area = cv2.contourArea(contour)
    #         if area > 1000:
    #             cv2.drawContours(cleaned_mask, [contour], -1, 255, thickness=-1)
    
    # Applying Binary Closing instead
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    cleaned_mask = cv2.morphologyEx(raw_mask, cv2.MORPH_CLOSE, kernel)
    # =============================================================================
    # 6. Save the Black & White Mask to disk maintaining folder structure and adding _mymask
    class_name = img_path.parent.name 
    save_dir = Path(out_dir) / class_name
    save_dir.mkdir(parents=True, exist_ok=True)
    
    new_name = img_path.stem + "_mymask.png"
    save_path = save_dir / new_name
    
    # Suppress output to prevent terminal from freezing when processing 16k files
    cv2.imwrite(str(save_path), cleaned_mask)
    return True

def main():
    # 1. Dynamically get the directory where this script resides
    SCRIPT_DIR = Path(__file__).resolve().parent
    
    # 2. Define Dataset and Output locations
    OUTPUT_DIR = SCRIPT_DIR / "student_mask"
    required_subfolders = ["BA", "BNE", "EO", "ERB", "LY", "MMY", "MO", "MY", "PLT", "PMY", "SNE"]
    
    while True:
        user_input = input(r"Enter DATASET_PATH: (i.e. ~\Naturalize Dataset\Naturalize Dataset)").strip()
        if user_input.lower() == "mahmoud":
            DATASET_PATH = r"C:\Users\User1\Documents\GitHub\IIP-G8\Dataset & Ground Truth\Naturalize Dataset\Naturalize Dataset"
        else:
            DATASET_PATH = user_input
            
        INPUT_DIR = Path(DATASET_PATH).resolve()        # Added the .resolve() thanks to AI while looking for possible issues after bug testing :P
        
        if not INPUT_DIR.exists() or not INPUT_DIR.is_dir():
            print(f"Error: The provided path '{DATASET_PATH}' does not exist or is not a directory.")
            print("Please try again or exit by pressing Ctrl+C\n")
            continue

        missing_subfolders = []
        for folder in required_subfolders:
            if not (INPUT_DIR / folder).is_dir():
                missing_subfolders.append(folder)

        if missing_subfolders:
            print(f"Error: The provided path must be a parent to the following missing subfolders: {', '.join(missing_subfolders)}\n")
            print("Please try again or exit by pressing Ctrl+C\n")
            continue
            
        break # Path is valid, exit the loop
        
    print(f"Scanning {INPUT_DIR} for images...")
    
    target_subfolders = {"BNE", "MY", "MMY", "PMY", "SNE"}
    image_files = []
    
    for folder in required_subfolders:
        folder_path = INPUT_DIR / folder
        if folder in target_subfolders:
            # Prioritize .png over .jpg
            png_files = list(folder_path.glob("*.png"))
            jpg_files = list(folder_path.glob("*.jpg"))
            
            # Enforce priority: if .png exists, don't use the equivalent .jpg
            png_stems = {p.stem for p in png_files}
            
            image_files.extend(png_files)
            image_files.extend([p for p in jpg_files if p.stem not in png_stems])
        else:
            # Fall back to .jpg for the remaining class folders
            image_files.extend(list(folder_path.glob("*.jpg")))
    
    if not image_files:
        print("No images found! Check the path.")
        return
        
    print(f"Found {len(image_files)} images. Setting up processing pool...")
    
    # Calculate half the available cores (ensure at least 1 is used)
    cores_to_use = max(1, cpu_count() // 2)
    print(f"Your computer has {cpu_count()} CPU cores. We are using {cores_to_use} cores so your computer doesn't freeze!")
    
    # Prepare arguments for the processing pool
    job_args = [(img, OUTPUT_DIR) for img in image_files]
    
    start_time = time.time()
    
    # Process using multiprocessing to rapidly chew through the 16k dataset without hanging
    with Pool(cores_to_use) as pool:
        # imap combined with tqdm gives us a beautiful progress bar
        results = list(tqdm(pool.imap(process_single_image, job_args), total=len(job_args), desc="Segmenting Cells"))
        
        # Usage of pool.imap was recommended by AI to prevent the terminal from freezing :P
        
    successful = sum(1 for r in results if r)
    end_time = time.time()
    
    print(f"\nCompleted Full Dataset Pipeline!\n")
    print(f"Successfully processed {successful}/{len(image_files)} images.")
    print(f"Total Time taken: {end_time - start_time:.2f} seconds.\n")
    print(f"All outputs are located neatly inside: {OUTPUT_DIR}\n")

if __name__ == "__main__":
    main()
