import os 

def make_label(text, xpos, ypos, font='2', rotation='0', h_mult='1', v_mult='1', n_reverse='N'):
    """
    Create a ZPL command for a text label.
    
    Parameters:
    text (str): The text to print.
    xpos (int): The x position in dots.
    ypos (int): The y position in dots.
    font (str): The font to use (default is '2').
    rotation (str): The rotation angle (default is '0').
    h_mult (str): Horizontal multiplication factor (default is '1').
    v_mult (str): Vertical multiplication factor (default is '1').
    n_reverse (str): Normal or reverse print (default is 'N').
    
    Returns:
    str: The ZPL command string.
    """
    return f"A{xpos},{ypos},{rotation},{font},{h_mult},{v_mult},{n_reverse},\"{text}\"\n"


def main():
    with open('output.prn', 'wb') as f:
        f.write(b"I8,A,001\n")  # Set the international character set to 'A' (USA). Other options include 'B' (British), 'C' (Canadian), etc.
        f.write(b"\n")
        f.write(b"Q480,024\n")  # Set the label length to 480 dots and the gap length to 24 dots. Adjust these values based on your label size and gap.
        f.write(b"q831\n")  # Set the width of the label to 831 dots. Adjust this value based on your label width.
        f.write(b"rN\n")  # Set the print direction to normal. Other options include 'rI' (inverted).
        f.write(b"S1\n")  # Set the print speed to 1 (slowest speed). Other options range from 'S1' (slowest) to 'S5' (fastest).
        f.write(b"D14\n")  # Set the print darkness to 14. Adjust this value based on the desired print darkness (range: 0-30).
        f.write(b"ZT\n")  # Set the print mode to tear-off. Other options include 'ZB' (batch), 'ZC' (cut), 'ZD' (delayed cut), 'ZE' (delayed batch), 'ZF' (peel-off), 'ZG' (retract), 'ZH' (rewind).
        f.write(b"JF\n")  # Set the label home position. This command is used to adjust the starting position of the label.
        f.write(b"OD\n")  # Set the print orientation to default. Other options include 'ON' (normal), 'OR' (rotated 90 degrees), 'OI' (inverted 180 degrees), 'OM' (mirrored 270 degrees).
        f.write(b"R104,0\n")  # Set the reference point for the label to (104, 0). The reference point is the origin (0,0) for the label format.
        f.write(b"f100\n")  # Set the label home position. This command is used to adjust the starting position of the label.
        f.write(b"N\n")  # Start a new label format. This command indicates the beginning of a new label definition.
        f.write((make_label("pos 2020", 20, 20) + "\n").encode())  # Add a text label with the text "label1_text" at position (20, 20).
        f.write((make_label("pos 2080", 20, 80) + "\n").encode())  # Add a text label with the text "label1_text" at position (20, 20).
        f.write((make_label("pos 10020", 100, 20) + "\n").encode())  # Add a text label with the text "label1_text" at position (20, 20).
        f.write((make_label("pos 10080", 100, 80) + "\n").encode())  # Add a text label with the text "label1_text" at position (20, 20).
        f.write(b"P1\n")  # Print one label. Adjust this value to print multiple labels (e.g., 'P5' to print 5 labels).
        f.write(b"\n")

    # Map the printer port
    print("Mapping printer")
    os.system('net use LPT1: \\localhost\\ZebraTLP2844 /persistent:yes')

    # Send the file to the printer
    print("Printing output.prn")
    os.system('COPY /B output.prn LPT1')

if __name__ == "__main__":
    main()