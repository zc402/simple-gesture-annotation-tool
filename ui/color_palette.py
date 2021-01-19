class ColorPalette:
    __rainbow = [{"name": "Sizzling Red", "hex": "ff595e", "rgb":[255, 89, 94], "cmyk":[0, 65, 63, 0], "hsb":[358, 65, 100], "hsl":[358, 100, 67], "lab":[61, 63, 32]}, {"name": "Mango Tango", "hex": "ff924c", "rgb":[255, 146, 76], "cmyk":[0, 43, 70, 0], "hsb":[23, 70, 100], "hsl":[23, 100, 65], "lab":[71, 36, 54]}, {"name": "Sunglow", "hex": "ffca3a", "rgb":[255, 202, 58], "cmyk":[0, 21, 77, 0], "hsb":[44, 77, 100], "hsl":[44, 100, 61], "lab":[84, 6, 74]}, {"name": "Acid Green", "hex": "c5ca30", "rgb":[197, 202, 48], "cmyk":[2, 0, 76, 21], "hsb":[62, 76, 79], "hsl":[62, 62, 49], "lab":[79, -19, 70]}, {"name": "Yellow Green", "hex": "8ac926", "rgb":[138, 201, 38], "cmyk":[31, 0, 81, 21], "hsb":[83, 81, 79], "hsl":[83, 68, 47], "lab":[74, -43, 68]}, {"name": "Viridian Green", "hex": "36949d", "rgb":[54, 148, 157], "cmyk":[66, 6, 0, 38], "hsb":[185, 66, 62], "hsl":[185, 49, 41], "lab":[56, -24, -13]}, {"name": "Green Blue Crayola", "hex": "1982c4", "rgb":[25, 130, 196], "cmyk":[87, 34, 0, 23], "hsb":[203, 87, 77], "hsl":[203, 77, 43], "lab":[52, -4, -42]}, {"name": "True Blue", "hex": "4267ac", "rgb":[66, 103, 172], "cmyk":[62, 40, 0, 33], "hsb":[219, 62, 67], "hsl":[219, 45, 47], "lab":[44, 9, -41]}, {"name": "Liberty", "hex": "565aa0", "rgb":[86, 90, 160], "cmyk":[46, 44, 0, 37], "hsb":[237, 46, 63], "hsl":[237, 30, 48], "lab":[41, 18, -39]}, {"name": "Royal Purple", "hex": "6a4c93", "rgb":[106, 76, 147], "cmyk":[28, 48, 0, 42], "hsb":[265, 48, 58], "hsl":[265, 32, 44], "lab":[38, 28, -35]}]

    @staticmethod
    def get_rgb(label: str):
        if label == ' ':
            return [220, 220, 220]
        try:
            n = int(label)
        except ValueError:
            n_ascii = ord(label)
            return ColorPalette.__rainbow[n_ascii % 10]["rgb"]

        if n == 0:
            return [220, 220, 220]
        else:
            return ColorPalette.__rainbow[n]["rgb"]