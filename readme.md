This printer is a real pain to get working, so i decided to add a few examples to anyone that may be trying to do the same.

I had to use a few workarounds to make it print over usb via command prompt (on windows), then more workarounds to print images and qrcodes (not supported directly on this printer). The end goal is to print labels for my devices, another script will connect to the device to get the information (such as mac address, ble address, etc) and printing the information on the label.

This requires you to install python, then the libs qrcode and pillow (`pip install qrcode pillow`)

### Step-by-Step Guide to Send EPL Commands to a Zebra TLP2844 Printer


This guide describes how to share a Zebra TLP2844 printer on the network and send EPL commands to it using the Windows command prompt. The solution involves sharing the printer, mapping the printer to an LPT port, and sending the EPL file.

#### Step 1: Share the Printer
1. **Open Control Panel**:
   - Press Win + R, type `control`, and press Enter.

2. **Access Devices and Printers**:
   - Go to Devices and Printers.

3. **Share the Printer**:
   - Right-click on the Zebra TLP2844 printer and select Printer properties.
   - Go to the Sharing tab.
   - Check the Share this printer option and give it a share name (e.g., ZebraTLP2844).

#### Step 2: Map the Printer to an LPT Port
1. **Open Command Prompt as Administrator**:
   - Press Win + R, type `cmd`, and press Ctrl + Shift + Enter to open as administrator.

2. **Map the Printer to LPT1**:
   - Use the `net use` command to map the shared printer to the LPT1 port:
     ```sh
     net use LPT1: \\localhost\ZebraTLP2844 /persistent:yes
     ```

#### Step 3: Send the EPL File to the Printer
1. **Save the EPL Code**:
   - Save the following EPL code in a file named `test2.epl` on your desktop. Ensure the file is saved with ANSI encoding.
     ```epl
     N
     q609
     Q203,26
     B26,26,0,UA0,2,2,152,B,"603679025109"
     A253,26,0,3,1,1,N,"SKU 6205518 MFG 6354"
     A253,56,0,3,1,1,N,"2XIST TROPICAL BEACH"
     A253,86,0,3,1,1,N,"STRIPE SQUARE CUT TRUNK"
     A253,116,0,3,1,1,N,"BRICK"
     A253,146,0,3,1,1,N,"X-LARGE"
     P1
     ```

2. **Navigate to the Desktop**:
   - In the command prompt, use the `cd` command to change the directory to the desktop:
     ```sh
     cd C:\Users\SIMOVA\Desktop
     ```

3. **Send the EPL File to the Printer**:
   - Use the `COPY` command to send the EPL file to the LPT1 port:
     ```sh
     COPY /B test2.epl LPT1
     ```

### Summary of Commands Used:
1. **Share the Printer**:
   - In Control Panel, share the Zebra TLP2844 printer with the name ZebraTLP2844.

2. **Map the Printer to LPT1**:
   ```sh
   net use LPT1: \\localhost\ZebraTLP2844 /persistent:yes
   ```

3. **Send the EPL File to the Printer**:
   ```sh
   COPY /B C:\Users\SIMOVA\Desktop\test2.epl LPT1
   ```

### EPL Code Used:
```epl
N
q609
Q203,26
B26,26,0,UA0,2,2,152,B,"603679025109"
A253,26,0,3,1,1,N,"SKU 6205518 MFG 6354"
A253,56,0,3,1,1,N,"2XIST TROPICAL BEACH"
A253,86,0,3,1,1,N,"STRIPE SQUARE CUT TRUNK"
A253,116,0,3,1,1,N,"BRICK"
A253,146,0,3,1,1,N,"X-LARGE"
P1
```

By following these steps, you will be able to send EPL commands to the Zebra TLP2844 printer and print the labels correctly.

