from fontTools.ttLib import TTFont, newTable
from fontTools.fontBuilder import FontBuilder
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor

def create_minimal_ttf(output_path):
    fb = FontBuilder(unitsPerEm=1024, isTTF=True)
    
    # Define a simple horizontal metric (width) and glyph name
    glyph_name = "A"
    sinking_map = {".notdef": 0, glyph_name: 1}
    
    # Create a very simple square as the letter 'A'
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    pen = TTGlyphPen(None)
    pen.moveTo((100, 0))
    pen.lineTo((100, 700))
    pen.lineTo((600, 700))
    pen.lineTo((600, 0))
    pen.closePath()
    glyph = pen.glyph()
    
    glyphs = {".notdef": pen.glyph(), glyph_name: glyph}
    horizontal_metrics = {".notdef": (500, 0), glyph_name: (700, 50)}
    
    # Fill required tables
    fb.setupGlyphOrder([".notdef", glyph_name])
    fb.setupCharacterMap({ord('A'): glyph_name})
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(horizontal_metrics)
    fb.setupHorizontalHeader()
    fb.setupNameTable({"familyName": "MyFont", "styleName": "Regular", "uniqueFontIdentifier": "MyFont-Regular"})
    fb.setupOS2()
    fb.setupPost()
    
    fb.save(output_path)
    print(f"Font created: {output_path}")

def create_designspace(font_filename, ds_filename):
    doc = DesignSpaceDocument()
    
    # Add a Weight axis
    axis = AxisDescriptor()
    axis.maximum, axis.minimum, axis.default = 1000, 100, 400
    axis.name, axis.tag = "weight", "wght"
    doc.addAxis(axis)
    
    # Link the .ttf file as the source
    source = SourceDescriptor()
    source.path = font_filename
    source.name = "MyFont-Regular"
    source.location = {"weight": 400}
    doc.addSource(source)
    
    doc.write(ds_filename)
    print(f"Designspace created: {ds_filename}")

if __name__ == "__main__":
    font_file = "myfont.ttf"
    ds_file = "myfont.designspace"
    
    create_minimal_ttf(font_file)
    create_designspace(font_file, ds_file)
