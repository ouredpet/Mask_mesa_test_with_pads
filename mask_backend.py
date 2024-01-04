import numpy as np
import pya
import mask_pya_aip as mpa

#################################################################

def build_arc( layout, cell_name, layer_name, x, y, radius, angle1, angle2):

    arc_region = mpa.build_arc_region(x, y, radius, angle1, angle2)
    mpa.insert_region( layout, cell_name, layer_name, arc_region)

def build_rectangle( layout, cell_name, layer_name, W, H, x0, y0):

    rect_region = mpa.build_rectangle_region( W, H, x0, y0)
    mpa.insert_region( layout, cell_name, layer_name, rect_region)

def build_rectangle_xy( layout, cell_name, layer_name, x0, y0, x1, y1):

    rect_region = mpa.build_rectangle_region_xy( x0, y0, x1, y1)
    mpa.insert_region( layout, cell_name, layer_name, rect_region)

def build_triangle_xy( layout, cell_name, layer_name, x0, y0, x1, y1, x2, y2):

    rect_region = mpa.build_triangle_region_xy( x0, y0, x1, y1, x2, y2)
    mpa.insert_region( layout, cell_name, layer_name, rect_region)

def build_rectangle_with_rhole( layout, cell_name, layer_name, W, H, x0, y0, Wh, Hh, x0h, y0h):

    rect_region = mpa.build_rectangle_region( W, H, x0, y0)
    hole_region = mpa.build_rectangle_region( Wh, Hh, x0 + x0h, y0 + y0h)
    rect_region_wh = rect_region - hole_region
    mpa.insert_region( layout, cell_name, layer_name, rect_region_wh)

def write_text(layout, cell_name, layer_name, size, x0, y0, rotate, text):
    gen = pya.TextGenerator()
    gen.load_from_file("vented_font_DDJ.gds")
    region = gen.text(text, size)
    x0, y0 = mpa.base_units( ( x0, y0))
    # trans = pya.Trans.new(pya.Trans.R90)
    trans = pya.Trans.new(rotate/180*np.pi)
    region.transform(trans)
    region.move(int(x0), int(y0))
    la = mpa.find_layer(layout, layer_name)
    ce = mpa.find_cell(layout, cell_name)
    ce.shapes(la).insert(region)

#################################################################