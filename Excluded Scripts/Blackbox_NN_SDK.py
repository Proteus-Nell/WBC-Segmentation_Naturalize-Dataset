"""
This program is derived from Algorithm 1 from the Coursework Assessment Sheet and was ran locally :D

Adjust the paths accordingly after unzipping the folders :P
"""

from myevalsdk import MaskQualityEvaluator
print("Import Successful")

GROUNDTRUTH_ROOT_DIR = r"C:\Users\User1\Documents\GitHub\IIP-G8\Dataset & Ground Truth\Ground Truth\Ground Truth"
PRED_ROOT_DIR        = r"C:\Users\User1\Documents\GitHub\IIP-G8\Submission Folder\student_mask"
IMAGE_ROOT_DIR       = r"C:\Users\User1\Documents\GitHub\IIP-G8\Dataset & Ground Truth\Naturalize Dataset\Naturalize Dataset"

# Initialize the evaluator
ev = MaskQualityEvaluator(
    gt_root     =    GROUNDTRUTH_ROOT_DIR,
    pred_root   =    PRED_ROOT_DIR,
    image_root  =    IMAGE_ROOT_DIR,
    output_csv  =    "results.csv",
    verbose     =    True,
)

print("EV ROOTS:")
print("GT :", ev.gt_root)
print("PRED :", ev.pred_root)
print("IMAGE :", ev.image_root)

result_path = ev.run()

print("Saved:", result_path)
