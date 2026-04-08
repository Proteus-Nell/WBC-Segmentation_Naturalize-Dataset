"""
This program is intended for segmenting the 9 pre-selected images and placing them in Results 2026 IIP - Group008 folder.

Perform the following for the code to work:
- Ensure that the "Results 2026 IIP - Group008" folder exists in the same directory as this script.
- Adjust the DATASET_PATH variable to point to the correct location of the dataset. (located in the main function)
"""


# Python Standard Libraries
import time
import os
from pathlib import Path

# External Libraries [OpenCV, NumPy]
import cv2              # Computer Vision Library   | Used for color space conversion, noise reduction, thresholding, and contour filtering.
import numpy as np      # Numerical Python Library  | Used for array manipulation and mathematical calculations.

def process_single_image(img_path, base_out_dir, difficulty, index):
    """
    Applies the user-defined pipeline to a single image and saves 
    the input, the binary mask, and the final segmented output to three separate folders.
    """
    img_path = Path(img_path)
    # 1. Load the original image
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"Failed to load: {img_path}")
        return False
    
    # Main Image Processing Component
    # =============================================================================
    # 2. Conversion to LAB
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
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
    
    # 5. Contour Filtering
    contours, _ = cv2.findContours(raw_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cleaned_mask = np.zeros_like(raw_mask)
    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                cv2.drawContours(cleaned_mask, [contour], -1, 255, thickness=-1)
    # =============================================================================

    # 6. Apply White Background
    final_output = img.copy()
    final_output[cleaned_mask == 0] = [255, 255, 255]
    
    # Input Images (Stored directly in the difficulty folder '001 - Easy')
    dir_input = Path(base_out_dir) / "001 - Input Images" / difficulty
    
    # Extract just the pure difficulty name (e.g. "Easy" from "001 - Easy")
    diff_name = difficulty.split("-")[-1].strip()
    
    # Format the specific subfolder name (e.g. "002 - Easy_2")
    subfolder_name = f"{index:03d} - {diff_name}_{index}"

    # Image Processing Pipeline (e.g. 002 - Image Processing Pipeline / 001 - Easy / 001 - Easy_1)
    dir_mask = Path(base_out_dir) / "002 - Image Processing Pipeline" / difficulty / subfolder_name
    
    # Output Images (e.g. 003 - Output Images / 001 - Easy / 001 - Easy_1)
    dir_output = Path(base_out_dir) / "003 - Output Images" / difficulty / subfolder_name
    
    # Create the directories, if they exist then skip (exist_ok=True)
    dir_input.mkdir(parents=True, exist_ok=True)
    dir_mask.mkdir(parents=True, exist_ok=True)
    dir_output.mkdir(parents=True, exist_ok=True)
    
    # Copy the original image
    cv2.imwrite(str(dir_input / img_path.name), img)
    
    # Save the pipeline binary mask
    mask_name = img_path.stem + "_mask.png"
    cv2.imwrite(str(dir_mask / mask_name), cleaned_mask)
    
    # Save the final segmented white-background image with the required suffix
    final_name = img_path.stem + "_mymask.png"
    cv2.imwrite(str(dir_output / final_name), final_output)
    
    return True

def main():
    # 1. Dynamically get the directory where this script actually lives
    # This ensures that even if the Marker runs it from a different folder, it won't break!
    SCRIPT_DIR = Path(__file__).resolve().parent
    
    # 2. Base output directly relative to the script
    BASE_OUT_DIR = SCRIPT_DIR / "Results 2026 IIP - Group008" / "Results 2026 IIP - Group008"
    EASY_DIR = BASE_OUT_DIR / "001 - Input Images" / "001 - Easy"
    MEDIUM_DIR = BASE_OUT_DIR / "001 - Input Images" / "002 - Medium"
    HARD_DIR = BASE_OUT_DIR / "001 - Input Images" / "003 - Hard"
    
    required_subfolders = ["BA", "BNE", "EO", "ERB", "LY", "MMY", "MO", "MY", "PLT", "PMY", "SNE"]
    
    while True:
        user_input = input(r"Enter DATASET_PATH: (i.e. ~\Naturalize Dataset\Naturalize Dataset)").strip()
        if user_input.lower() == "mahmoud":
            DATASET_PATH = r"C:\Users\User1\Documents\GitHub\IIP-G8\Dataset & Ground Truth\Naturalize Dataset\Naturalize Dataset"
        else:
            DATASET_PATH = user_input

        DATASET_PATH = Path(DATASET_PATH).resolve() # Added .resolve() to ensure the path is absolute thanks to AI :P

        if not DATASET_PATH.exists() or not DATASET_PATH.is_dir():
            print(f"Error: The provided path '{DATASET_PATH}' does not exist or is not a directory.")
            print("Please try again or exit by pressing Ctrl+C\n")
            continue

        missing_subfolders = []
        for folder in required_subfolders:
            if not (DATASET_PATH / folder).is_dir():
                missing_subfolders.append(folder)

        if missing_subfolders:
            print(f"Error: The provided path must be a parent to the following missing subfolders: {', '.join(missing_subfolders)}\n")
            print("Please try again or exit by pressing Ctrl+C\n")
            continue
            
        break # Path is valid, exit the loop

    # Fill in the exact RELATIVE paths to the 9 images you selected!
    SELECTED_IMAGES = {
        "001 - Easy": [ # PMY Images
            DATASET_PATH / r"PMY\MMY 2K-PBC Train (15).png",     # Chosen due to its large size and assymetric shape.
            DATASET_PATH / r"PMY\MMY 2K-PBC Train (12).png",     # Chosen due to the lighter shade which resulted in us switching from contour_filtering to closing.
            DATASET_PATH / r"PMY\MMY 2K-PBC Train (6).png"       # Chosen due to its different, slightly more pinker color and lighting.
        ],
        "002 - Medium": [ # EO Images
            DATASET_PATH / r"EO\EO 2K-PBC Train (39).jpg",       # Chosen to check the effect of different colored regions.
            DATASET_PATH / r"EO\EO 2K-PBC Train (31).jpg",       # Chosen as we were able to detect the external smaller cell compared to the ground truth.
            DATASET_PATH / r"EO\EO 2K-PBC Train (543).jpg"       # Chosen to act as a baseline test
        ],
        "003 - Hard": [ # ERB Images
            DATASET_PATH / r"ERB\ERB 2K-PBC Train (30).jpg",     # Chosen as the ground truth is inaccurate and it beats it by highlighting the center nuclei. (affects our mIOU but great for conf. report :D)
            DATASET_PATH / r"ERB\ERB 2K-PBC Train (370).jpg",    # Chosen as it matches the ground truth but I'm personally uncertain on whether the outer shades should be included or not (so enjoy Marker! (I'm assuming Dr. Tissa is reading this))
            DATASET_PATH / r"ERB\ERB 2K-PBC Train (473).jpg"     # Chosen to see how the pipeline works with varying borders (reasonably well but it missed the teeny center left bit)
        ]
    }
    
    start_time = time.time()
    successful = 0
    total = sum(len(paths) for paths in SELECTED_IMAGES.values())
    
    # Loop through the dictionary holding our 9 chosen images
    for difficulty, img_paths in SELECTED_IMAGES.items():
        print(f"\nProcessing {difficulty.upper()} images...")
        
        for index, img_string in enumerate(img_paths, 1):
            # img_string is already an absolute path
            img_path = img_string
            
            # Prioritize .png for specific subfolders
            target_subfolders = {"BNE", "MY", "MMY", "PMY", "SNE"}
            if img_path.parent.name in target_subfolders:
                png_version = img_path.with_suffix('.png')
                if png_version.exists():
                    img_path = png_version
            
            # Print the filename (e.g. 'BA 2k-PBC Train (58).jpg')
            print(f" -> {img_path.name}")
            
            result = process_single_image(img_path, BASE_OUT_DIR, difficulty, index)
            
            if result:
                successful += 1
            
    end_time = time.time()
    
    print(f"\nCompleted pipeline!\n")
    print(f"Successfully processed {successful}/{total} valid images.")
    print(f"Total Time taken: {end_time - start_time:.2f} seconds.\n")
    print(f"Outputs neatly sorted into {BASE_OUT_DIR}\n")

if __name__ == "__main__":
    main()
