# RGB-Color: Red Giant Branch Color Estimation

This program was written to measure a mean color index of the red giant branch of galaxies resolved into stars in the Local Volume (based on EDD CMD/TRGB catalog (`https://edd.ifa.hawaii.edu`). Now I'm making it freely available. 

This Python program allows you to clean the photometry file, crop the field of the instrument (for example, by selecting the outer regions of the galaxy in field), build a color-magnitude diagram and measure the color index at any level ($M_I$) in two ways: by searching for the maximum density or approximating the branch with a parabola. For convenience, a graphical interface written in QT5 is used. 


When using (including modification), I humbly ask you to quote the work "TBA".

# Install
To create a working environment in Conda, run:
```bash
conda env create -f environment.yml
```
This will create an environment called `trgb_gui`, which will contain all the necessary Python packages. Alternatively, you can install them manually: 
```
- python > 3.9
- pyqt
- fpdf2
- matplotlib
- numpy
- pandas
- pillow
- scipy
- seaborn
- jupyterlab
```

Note: its `fpdf2`, not `fpdf`!

### Run
If you installed the environment using `environment.yml` activate it and run the program: 
```bash
conda activate trgb_gui
python run.py
```

### Uninstall
To completely uninstall the application:
1. Delete the project directory.
2. Remove the Conda environment:
```bash
conda env remove --name trgb_gui
```

# Usage
### Input Data
The input data must be a CSV file with fixed column names. Examples of valid input files can be found in the `input_examples` directory. The column names must be as follows:

##### Required columns:
- `x`,`y` - potential star coordinates,
- `mag_v`,`err_v`,`mag_i`,`err_i` - stellar magnitude and error in the V and I filters,
##### Optional columns:
- `type` - object profile shape classification as in DOLPHOT,
- `snr_v`,`snr_i` - signal-to-noise ratio,
- `sharp_v`,`sharp_i` - sharpness,
- `round_v`,`round_i` - roundness,
- `crowd_v`,`crowd_i` - crowding parameter,
- `flag_v`,`flag_i` - diagnostic quality flag.

The columns provided in the input data can be used later to clean up the photometry. Additional columns may be present, and they can be in any order.
It might be helpful to look at the Jupyter notebook in the `photometry_converter` directory as an example of converting DOLPHOT data to the format used.


### Data preparation
For more information run from `photometry_converter` directory:
```bash
conda activate trgb_gui
python converter.py -h
```
<img src="readme_images/converter_help_menu.png" width="500"/>

You can use files from `photometry_converter/raw` as a playground.

<img src="readme_images/converter_example.png" width="500"/>

This script enables a step-by-step selection of the required columns from data in the standard DOLPHOT format and exports them to a ready-to-use CSV file.


### File selection and basic data entry
Run the program. This is what you should see:

<img src="readme_images/02_base_mouse.png" width="500"/>

1. Select file `.csv` file with photometric data. Each row should represent a possible star. Mandatory columns: `x`, `y` (coordinates in the instrument's field of view), `mag_v`, `err_v`, `mag_i`, `err_i` (apparent magnitude and measurement error in filters I and V, respectively). 

    <img src="readme_images/03_file_selections.png" width="800"/>

2. Clean the photometry data. Select criteria to use, change them if necessary. In this example, I got rid of the bottom of the CMD by raising the Signal/Noise threshold.

    <img src="readme_images/05_clearing.png" width="800"/>

3. Crop the field of view if necessary. In this example, I have cut off the areas of the instrument's field most dense with stars, and thus selected only the outer regions of the galaxy. You can also select a rectangular area in the field by entering the coordinates manually.

    <img src="readme_images/06_clipping.png" width="5800"/>

    <img src="readme_images/07_clipped.png" width="800"/>

4. Enter distance (in MPc or in Mag).

    <img src="readme_images/08_distance.png" width="500"/>

5. Enter foreground (Galactic) extinction in I and respective (V-I) color excess.

    <img src="readme_images/09_color_excess.png" width="500">

6. View the cleaned instrument field and color-magnitude diagram in absolute magnitudes. There will be density histogram over the scatterplot, you can change it to kernel-density plot (kde) if you need. Using kde usually takes some time.

    <img src="readme_images/10_abs_cmd.png" width="800">
    
    <img src="readme_images/11_abs_cmd_isodense.png" width="800">

The program provides the ability to measure color index using two methods described in the article (ref. TBA).

### Branch approximation
This method allows one to approximate the branch of red giants using a parabola. A peculiarity of this method is that one must manually specify the boundaries of the region in color index (V-I) - brightness (I) coordinates where the branch is located.

<img src="readme_images/branch_1.png" width="500">

<img src="readme_images/branch_2.png" width="800">

### Density analythis
This method allows one to measure the color index using the density profile of the stars at the specified M_I level. The confidence interval estimate will be obtained using the Monte Carlo method.

<img src="readme_images/density_1.png" width="5800">

### Distance adjustment

The most practical approach is to adopt the distance derived from the color-magnitude diagram. It is also crucial to specify the confidence interval for this distance (which may be asymmetric), as it is used directly in both methods for measuring the color index. The upper and lower bounds of this interval, $\delta_{+}D$ and $\delta_{-}D$, are expressed in magnitudes. Their values are defined according to the following logic:

$D_{real} ∈ [D - \delta_{-} D; D + \delta_{+} D]$

<img src="readme_images/distances.png" width="300">

### Saving results
The processing result will be two files: a json file with parameters and numerical estimates, and a pdf file with a visualization of intermediate graphs.

<img src="readme_images/saving_1+2.png" width="800">

<img src="readme_images/result_pdf.png" width="800">

<img src="readme_images/result_json.png" width="800">
