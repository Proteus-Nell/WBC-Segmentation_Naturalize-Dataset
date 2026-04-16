# IIP-G8

## How to Run the Segmentation Pipeline

To run the segmentation pipeline for the 9 pre-selected images (`pipeline_SegmentationPart_9imgs.py`), please follow the instructions below. 

### Prerequisites
1. Install the required Python libraries (`opencv-python` and `numpy`):
   ```
   pip install opencv-python numpy
   ```
2. Make sure you have the **Naturalize Dataset** downloaded and extracted on your machine. The target dataset path you provide must directly contain the cell class subfolders (e.g., `BA`, `BNE`, `EO`, `ERB`, `LY`, `MMY`, `MO`, `MY`, `PLT`, `PMY`, `SNE`).

### Execution
1. Open the file and run it or open the terminal and navigate to the directory containing the script (e.g., `Submission Folder`):
   ```
   cd "Submission Folder"
   ```
2. Execute the Python script:
   ```
   python pipeline_SegmentationPart_9imgs.py
   ```
3. When prompted:
   ```
   Enter DATASET_PATH: (i.e. ~\Naturalize Dataset\Naturalize Dataset)
   ```
   Enter the absolute path to your target dataset folder. The script will resolve this path and verify the presence of the required subfolders before proceeding.

4. The pipeline will automatically segment the pre-selected 9 images (3 Easy, 3 Medium, 3 Hard) and log progress in the terminal.
5. Once completed, the outputs will be saved in subdirectories relative to the script's location, matching the assessment structure:
   ```
   Results 2026 IIP - Group008/Results 2026 IIP - Group008/
   ├── 001 - Input Images/               # Copies of the original images
   ├── 002 - Image Processing Pipeline/  # Intermediate binary masks
   └── 003 - Output Images/              # Final segmented cell with white background
   ```

---

### Members of Group 8:
| Name                              | Student ID |
| --------------------------------- | ---------- |
| Ralph Matthew Tay Rivera          | 20718385   |
| Zhi Jian Tsen                     | 20703544   |
| Mirza Zahin Khan Tasneem Ahmad    | 20673433   |
| Mahmoud Yasser Mokhtar Sallam     | 20574289   |

### Dataset, SDK, Ground Truth Folder
- [SDK](https://numcmy-my.sharepoint.com/:u:/g/personal/kgztc_nottingham_edu_my/IQD9mmf33QhrS59_Q43ikhSOAYQQPvwBqKuXwz9gI_4bVjk?e=6OZFAs)
- [Ground Truth Folder](https://numcmy-my.sharepoint.com/:u:/g/personal/kgztc_nottingham_edu_my/IQD0h_7sgLUcTJLkRT41UYTwAbrzea8tg29cY_OsAA9UheM?e=CyRpXm) - Already Included in Repo
- [Naturalize Dataset](https://numcmy-my.sharepoint.com/:u:/g/personal/kgztc_nottingham_edu_my/IQBiVyS-x1B1RLZYHkQEbcrvAVmzz8cQ7j6kTjR-E8HpDZc?e=nVAPPA)

### Submission Forms:
- [AI Declaration Form](https://forms.office.com/r/NyYm1vFuTr) - 15% Deduction if not submitted (Individually).
- [Peer Assessment Form](https://moodle.nottingham.ac.uk/mod/peerwork/view.php?id=8769015) - 10% Deduction if not submitted (Individually).

### Submission Guidelines & Deadline:
- Python code should be zipped.
- 6-Page Conference Paper in PDF form, each additional pages result in a 5% deduction group-wide.
- Official submission date is Friday (24/04/2026), however we have until Sunday (26/04/2026) to submit without any deduction in grades.
- References are to be made in IEEE, use the provided IEEE reference or a [BibTeX > IEEE Converter](https://www.bibtex.com/c/bibtex-to-ieee-converter/) after acquiring the BibTeX format. 

### Notes & Reference Links:
- Hematopoiesis = Process for Blood Cell Formation.
- Granulopoiesis = Process for Granulocytes in Bone Marrow (WBC Subset).
- White Bood Cells (WBC): Neutrophils, Eosinophils, Basophils, Lymphocytes, Andmonocytes.
- Promyelocyte > Myelocyte > Metamyelocyte > Band > 
---
- [Naturalize Dataset | GitHub](https://github.com/Mohamad-AbouAli/BloodCellDataset_11Types_Contains26534BloodCellImages)
- [Naturalize Dataset | Kaggle](https://www.kaggle.com/datasets/mohamadabouali1/blood-cells-dataset-11-classes-26534-images)
- [Methodology](https://docs.google.com/document/d/1VenZA1XjZP3SekQ-6iAjmpiX-FknLspF6BAyd0LLF2o/edit?usp=sharing)
- [Google Colab](https://colab.research.google.com/drive/1OnA-ZAt7diH8c398zmSrJKD1T0nzfjgT?usp=sharing)