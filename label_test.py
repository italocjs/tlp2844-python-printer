import os

# Define label size and spacing in mm
LABEL_WIDTH_MM = 39
LABEL_HEIGHT_MM = 60
LABEL_SPACING_MM = 4

# Conversion factor from mm to dots (203 DPI -> 203 dots/inch -> 203/25.4 dots/mm ≈ 8 dots/mm)
MM_TO_DOTS = 203 / 25.4

def make_text(text, xpos_mm, ypos_mm, font='2', rotation='0', h_mult='1', v_mult='1', n_reverse='N'):
    """
    Create a ZPL command for a text label, converting mm to dots.
    
    Parameters:
    text (str): The text to print.
    xpos_mm (int): The x position in mm.
    ypos_mm (int): The y position in mm.
    font (str): The font to use (default is '2').
    rotation (str): The rotation angle (default is '0').
    h_mult (str): Horizontal multiplication factor (default is '1').
    v_mult (str): Vertical multiplication factor (default is '1').
    n_reverse (str): Normal or reverse print (default is 'N').
    
    Returns:
    str: The ZPL command string.
    """
    xpos = int(xpos_mm * MM_TO_DOTS)
    ypos = int(ypos_mm * MM_TO_DOTS)
    print(f"Debug: {text} at ({xpos_mm}mm, {ypos_mm}mm) -> ({xpos} dots, {ypos} dots)")
    return f"A{xpos},{ypos},{rotation},{font},{h_mult},{v_mult},{n_reverse},\"{text}\"\n"

def main():
    with open('output.prn', 'wb') as f:
        f.write(b"I8,A,001\n")
        f.write(b"\n")
        f.write(b"Q480,024\n")
        f.write(b"q831\n")
        f.write(b"rN\n")
        f.write(b"S1\n")
        f.write(b"D14\n")
        f.write(b"ZT\n")
        f.write(b"JF\n")
        f.write(b"OD\n")
        f.write(b"R104,0\n")
        f.write(b"f100\n")
        f.write(b"N\n")

        # Left label positions
        f.write((make_text("Top Left", 5, 0) + "\n").encode())
        f.write((make_text("Middle Left", 5,( LABEL_HEIGHT_MM / 2) -5 ) + "\n").encode())
        f.write((make_text("Bottom Left", 5, LABEL_HEIGHT_MM - 5) + "\n").encode())

        # Right label positions
        right_label_x = LABEL_WIDTH_MM + LABEL_SPACING_MM
        f.write((make_text("Top Right", right_label_x, 0) + "\n").encode())
        f.write((make_text("Middle Right", right_label_x, (LABEL_HEIGHT_MM / 2) -5) + "\n").encode())
        f.write((make_text("Bottom Right", right_label_x, LABEL_HEIGHT_MM - 5) + "\n").encode())

        f.write(b"P1\n")
        f.write(b"\n")

    print("Mapping printer")
    os.system('net use LPT1: \\localhost\\ZebraTLP2844 /persistent:yes')

    print("Printing output.prn")
    os.system('COPY /B output.prn LPT1')

if __name__ == "__main__":
    main()