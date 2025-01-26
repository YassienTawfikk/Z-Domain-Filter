# Digital Filter Application

### **Overview**
The Digital Filter Application is an advanced tool for designing and implementing digital filters. It allows users to interactively place zeros and poles on the z-plane, manipulate them, and observe the resultant changes in the filter's frequency response. This application is ideal for educational purposes, research, and practical applications in signal processing.

---

### **Features**

1. **Z-Plane Customization**:
   - Interactive plot of the z-plane with a unit circle for placing zeros and poles.
   - Users can modify zeros and poles by dragging, adding conjugates, or swapping zeros with poles.
   - Functionality to delete, clear all zeros or poles, and undo/redo modifications.
   - Save and load filter configurations in notepad or CSV formats.

2. **Filter Realization and Exporting**:
   - Implements filters in direct form II and cascade forms.
   - Exports designed filters to C code for use in other applications.

3. **Frequency Response Visualization**:
   - Real-time updates of magnitude and phase responses corresponding to z-plane modifications.
   - Includes both magnitude and phase response graphs.

4. **Comprehensive Filter Library**:
   - Built-in library with at least 10 famous digital filter types such as Butterworth, Chebyshev, Inverse Chebyshev, Bessel, and Elliptic.

5. **Real-time Signal Processing**:
   - Apply filters on signals with up to 10,000 points, visualizing the time progress of both original and filtered signals.
   - Control the speed/temporal resolution of the filtering process using a slider.
   - Input arbitrary real-time signals via mouse movements, influencing signal frequency based on the speed of motion.

6. **Phase Correction with All-Pass Filters**:
   - Library of all-pass filters with visualizable zero-pole combinations and phase responses.
   - Option for users to custom-build all-pass filters by providing specific coefficients.
   - Enable/disable all-pass filters through a drop-down menu or checkboxes.

---

### **Application Interface**
Key screenshots demonstrating the application capabilities:

1. **Main Interface with Filter Selection and Z-Plane**  
   ![Main Interface](file-SdBpREjjELpUtiRhy62VXP)

2. **Filter Options with Real-time Frequency Response**  
   ![Filter Options](file-19pcskkqENxLPotQWxn4BS)

3. **Chebyshev HPF and LPF Implementation**  
   ![Chebyshev Filters](file-1viKDnBcoST3reLBSjcLUU)

4. **Block Diagram for Chebyshev HPF**  
   ![Block Diagram](file-P4NYVBjMBSNFWN9iKjnrjV)

---

### **Video Demo**
Watch a detailed demonstration of the application in action here:
[Digital Filter Application Demo](https://youtube.com/yourvideolink)

---

### **Setup and Installation**
1. **Download the Application**:
   Download the latest version from the releases section of our GitHub repository.

2. **Install the Application**:
   Run the installer and follow the on-screen instructions to install the Digital Filter Application on your system.

3. **Download Required Dependencies**:
   Download the `requirements.txt` from the repository and install necessary dependencies:
   ```bash
   pip install -r requirements.txt

---

## Contributors
<div>
<table align="center">
  <tr>
        <td align="center">
      <a href="https://github.com/YassienTawfikk" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/126521373?v=4" width="150px;" alt="Yassien Tawfik"/>
        <br />
        <sub><b>Yassien Tawfik</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/madonna-mosaad" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/127048836?v=4" width="150px;" alt="Madonna Mosaad"/>
        <br />
        <sub><b>Madonna Mosaad</b></sub>
      </a>
    </td>
        <td align="center">
      <a href="https://github.com/nancymahmoud1" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/125357872?v=4" width="150px;" alt="Nancy Mahmoud"/>
        <br />
        <sub><b>Nancy Mahmoud</b></sub>
      </a>
    </td>
    </td>
        <td align="center">
      <a href="https://github.com/yousseftaha167" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/128304243?v=4" width="150px;" alt="Youssef Taha"/>
        <br />
        <sub><b>Youssef Taha</b></sub>
      </a>
    </td>    
  </tr>
</table>
</div>
