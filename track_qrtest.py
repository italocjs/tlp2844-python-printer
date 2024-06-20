import os
import qrcode
from PIL import Image

# Define label size and spacing in mm
LABEL_WIDTH_MM = 39
LABEL_HEIGHT_MM = 60
LABEL_SPACING_MM = 4

# Conversion factor from mm to dots (203 DPI -> 203 dots/inch -> 203/25.4 dots/mm ≈ 8 dots/mm)
MM_TO_DOTS = 203 / 25.4

# Define variables for placeholders
serial = "SMV_TRACK_032"
uuid = "100180"
ble = "00:00:00:00:00:00"
hw = "1.3.4"
fw = "4.4.0"
reserved = "0x000000000000"

def prepare_qr_payload(serial, uuid, ble, hw, fw, reserved):
    return f"""
SERIAL={serial}
UUID={uuid}
BLE={ble}
HW={hw} FW={fw}
RESERVED={reserved}
MARROM=GND
VERMELHO=12-32V
VERDE=CANL
AMARELO=CANH
LARANJA=IN1(32v)
AZUL=IN2(32v)
ROXO=IN3(32v)
CINZA=IN4(32v)
https://www.simova.com.br/
"""

def make_text(text, xpos_mm, ypos_mm, font='2', rotation='0', h_mult='1', v_mult='1', n_reverse='N'):
    xpos = int(xpos_mm * MM_TO_DOTS)
    ypos = int(ypos_mm * MM_TO_DOTS)
    return f"A{xpos},{ypos},{rotation},{font},{h_mult},{v_mult},{n_reverse},\"{text}\"\n"

def create_qr_code(data, size_mm, dpi, filename):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    mm_to_dots = lambda mm: int(mm * dpi / 25.4)
    size_dots = mm_to_dots(size_mm)
    
    qr_image = qr_image.resize((size_dots, size_dots), Image.LANCZOS)
    qr_image = qr_image.convert('1')  # Convert to monochrome
    qr_image.save(filename)

def convert_image_to_hex(image_path):
    image = Image.open(image_path).convert('1')
    width, height = image.size
    hex_data = bytearray()
    
    for y in range(height):
        row_data = 0
        for x in range(width):
            pixel = image.getpixel((x, y))
            row_data = (row_data << 1) | pixel
            if (x + 1) % 8 == 0:
                hex_data.append(row_data & 0xFF)
                row_data = 0
        if width % 8 != 0:
            row_data <<= (8 - width % 8)
            hex_data.append(row_data & 0xFF)
    
    return hex_data, (width, height)

def make_image(xpos_mm, ypos_mm, image_path):
    hex_data, (width, height) = convert_image_to_hex(image_path)
    xpos = int(xpos_mm * MM_TO_DOTS)
    ypos = int(ypos_mm * MM_TO_DOTS)
    print(f"Debug: Image at ({xpos_mm}mm, {ypos_mm}mm) -> ({xpos} dots, {ypos} dots)")
    return f"GW{xpos},{ypos},{(width + 7) // 8},{height},", hex_data

def main():
    # Prepare QR code payloads
    left_qr_payload = prepare_qr_payload(serial, uuid, ble, hw, fw, reserved)
    right_qr_payload = prepare_qr_payload(serial, uuid, ble, hw, fw, reserved)

    # Create the QR code images
    qr_code_size_mm = 35
    dpi = 203  # Dots per inch for Zebra TLP2844
    create_qr_code(left_qr_payload, qr_code_size_mm, dpi, 'left_qr_code.png')
    create_qr_code(right_qr_payload, qr_code_size_mm, dpi, 'right_qr_code.png')

    # Calculate the position for the graphic
    x_position = (int(LABEL_WIDTH_MM * MM_TO_DOTS) - int(qr_code_size_mm * MM_TO_DOTS)) // 2
    y_position = (int(LABEL_HEIGHT_MM * MM_TO_DOTS) - int(qr_code_size_mm * MM_TO_DOTS)) // 2

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
        
        # Add the left image
        image_cmd, hex_data = make_image(x_position / MM_TO_DOTS, y_position / MM_TO_DOTS, 'left_qr_code.png')
        f.write(image_cmd.encode() + hex_data + b"\n")

        # Add the right image
        right_label_x = LABEL_WIDTH_MM + LABEL_SPACING_MM
        image_cmd, hex_data = make_image((right_label_x + x_position / MM_TO_DOTS), y_position / MM_TO_DOTS, 'right_qr_code.png')
        f.write(image_cmd.encode() + hex_data + b"\n")
        
        # Add text labels
        f.write((make_text("Top Left", 5, 0)).encode())
        f.write((make_text("Bottom Left", 5, LABEL_HEIGHT_MM - 5)).encode())
        
        f.write((make_text("Top Right", right_label_x, 0)).encode())
        f.write((make_text("Bottom Right", right_label_x, LABEL_HEIGHT_MM - 5)).encode())
        
        f.write(b"P1\n")
        f.write(b"\n")

    # Map the printer port
    print("Mapping printer")
    # os.system('net use LPT1: \\localhost\\ZebraTLP2844 /persistent:yes')

    # Send the file to the printer
    print("Printing output.prn")
    # os.system('COPY /B output.prn LPT1')

if __name__ == "__main__":
    main()