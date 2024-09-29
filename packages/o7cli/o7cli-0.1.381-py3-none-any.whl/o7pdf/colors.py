


class Colors:

    @staticmethod
    def hex_to_rgb(hex_code):
        """Converts a color hex code to a dictionary with r, g, b values"""
        hex_code = hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return {'r': r, 'g': g, 'b': b}

    O7_COLOR_MAIN = hex_to_rgb('#f36c21')
    O7_COLOR_ALT = hex_to_rgb('#15317E')

    N900 = hex_to_rgb('#091E42')
    N800 = hex_to_rgb('#172B4D')
    N700 = hex_to_rgb('#253858')
    N600 = hex_to_rgb('#344563')
    N500 = hex_to_rgb('#42526E')
    N400 = hex_to_rgb('#505F79')
    N300 = hex_to_rgb('#5E6C84')
    N200 = hex_to_rgb('#6B778C')
    N100 = hex_to_rgb('#7A869A')
    N90 = hex_to_rgb('#8993A4')
    N80 = hex_to_rgb('#97A0AF')
    N70 = hex_to_rgb('#A5ADBA')
    N60 = hex_to_rgb('#B3BAC5')
    N50 = hex_to_rgb('#C1C7D0')
    N40 = hex_to_rgb('#DFE1E6')
    N30 = hex_to_rgb('#EBECF0')
    N20 = hex_to_rgb('#F4F5F7')
    N10 = hex_to_rgb('#FAFBFC')
    N0 = hex_to_rgb('#FFFFFF')


    # Blue
    B500 = hex_to_rgb('#0747A6')
    B400 = hex_to_rgb('#0052CC')
    B300 = hex_to_rgb('#0065FF')
    B200 = hex_to_rgb('#2491EB')
    B100 = hex_to_rgb('#4C9AFF')
    B75 = hex_to_rgb('#B3D4FF')
    B50 = hex_to_rgb('#DEEBFF')

