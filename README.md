# DriftUS
**DriftUS** is a desktop application that simulates ultrasound imaging of phantoms to study how incorrect sound speed assumptions cause apparent shifts in target positions, quantifying geometric distortion and its impact on distance and size measurements in clinical ultrasound.


## Table of Contents
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Features](#features)
- [Contributors](#contributors)

## Demo
[demo link](https://github.com/user-attachments/assets/b0b88572-7285-4047-ab31-79b8865ff35b)

## Prerequisites

- Python 3.6 or higher

## Installation

1. **Clone the repository:**

   ``````
   git clone https://github.com/AhmedAmgadElsharkawy/DriftUS.git
   ``````

2. **Install The Dependincies:**
    ``````
    pip install -r requirements.txt
    ``````

3. **Run The App:**

    ``````
    python main.py
    ``````

## Features  

- **Speed Assumption Simulation:**
    Simulate the effect of mismatch between the assumed ultrasound speed and the actual tissue speed on the reconstructed image.
- **Customizable Phantom Generation:**
    Generate phantoms with background speckle noise to simulate tissue texture and dynamically add cysts by specifying their depth, lateral position, and radius.
- **Dual Viewer Comparison:**
    Two viewers are displayed side-by-side to compare the original phantom (at true speed 1540 m/s) against the reconstructed image based on the user-entered speed.
- **Geometric Distortion Visualization:**
    Observe how assuming a speed higher than reality causes image stretching, while a lower speed causes compression of cyst dimensions (lateral and depth).
- **Quantitative Metrics:**
    - **Axial Magnification:** Calculates the distortion factor (Assumed Speed / Original Speed) to quantify the amount of stretching or compression.
    - **Mean Depth Shift:** Measures the positional error of the cysts caused by the incorrect speed assumption.
- **Interactive Controls:**
    Input fields allow users to modify the assumed speed of sound and cyst parameters with real-time updates to the visualization and metrics.


## Contributors
- **AhmedAmgadElsharkawy**: [GitHub Profile](https://github.com/AhmedAmgadElsharkawy)
- **AbdullahMahmoudHanafy**: [GitHub Profile](https://github.com/AbdullahMahmoudHanafy)
- **Youssef-Abo-El-Ela**: [GitHub Profile](https://github.com/Youssef-Abo-El-Ela)
- **Ayatullah-ahmed**: [GitHub Profile](https://github.com/Ayatullah-ahmed)
- **MostafaMousaaa**: [GitHub Profile](https://github.com/MostafaMousaaa)


