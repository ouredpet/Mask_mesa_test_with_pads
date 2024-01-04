import numpy as np
import pya

def find_layer( layout, layer_name):

    for li in layout.layer_indices():
        if layout.get_info(li).name == layer_name:
            layout_number = li
            continue
    return layout_number

def find_cell( layout, cell_name):

    return layout.cell( layout.cell_by_name( cell_name))

def sub_cell_to_TOPcell( layout, top_cell, sub_cell_name, x0, y0):

    sub_cell = find_cell( layout, sub_cell_name)
    top_cell.insert(pya.DCellInstArray(sub_cell.cell_index(), pya.DCplxTrans(x0, y0)))

# def sub_cell_to_TOPcell_cellexpli( layout, top_cell, sub_cell, x0, y0):

#     top_cell.insert(pya.DCellInstArray(sub_cell.cell_index(), pya.DCplxTrans(x0, y0)))


def base_units( list_d):

    list_d = [i * 1e3 for i in list_d]
    return list_d

def shift_cell( layout, cell_name, xs, ys):

    xs, ys = base_units( ( xs, ys))
    trans = pya.Trans.new(int(xs), int(ys))
    cell = find_cell( layout, cell_name)
    cell.transform(trans)
    return


# def merge_shapes_in_cell_accros_layer_c(layout, layer_name, cell):
#     layer = find_layer( layout, layer_name)

#     mergeReg = pya.Region(cell.begin_shapes_rec(layer))
#     mergeReg.merge()
#     # cell.layout().clear_layer(layer) # why? it is lcearing everything before
#     cell.shapes(layer).insert(mergeReg)

def merge_shapes_in_cell_accros_layer(layout, layer_name, cell_name):

    cell_t = find_cell( layout, cell_name)
    layer = find_layer( layout, layer_name)


    mergeReg = pya.Region(cell_t.begin_shapes_rec(layer))
    mergeReg.merge()
    # cell_t.layout().clear_layer(layer)
    cell_t.clear_shapes()
    cell_t.shapes(layer).insert(mergeReg)

    # this would destroy all the layers
    # for lind in layout.layer_indexes():
    #     mergeReg = pya.Region(cell_t.begin_shapes_rec(lind))
    #     mergeReg.merge()
    #     cell_t.layout().clear_layer(lind)
    #     cell_t.shapes(lind).insert(mergeReg)

def insert_region(layout, cell_name, layer_name, region):

    cell = find_cell( layout, cell_name)
    layer = find_layer( layout, layer_name)
    cell.shapes( layer).insert( region)

def insert_region_c(layout, cell, layer_name, region):

    layer = find_layer( layout, layer_name)
    cell.shapes( layer).insert( region)

def rect_wh_to_xy(w, h, x0 ,y0):

    X1 = -1 * w / 2 + x0
    Y1 = -1 * h / 2 + y0
    X2 =  1 * w / 2 + x0
    Y2 =  1 * h / 2 + y0
    return X1, Y1, X2, Y2

def build_rectangle_region( W, H, x0, y0):

    rect_region = pya.Region()
    W, H, x0, y0 = base_units( ( W, H, x0, y0))
    X1, Y1, X2, Y2 = rect_wh_to_xy(W, H, x0, y0)
    rect_region.insert( pya.Box( X1, Y1, X2, Y2))
    return rect_region

def build_rectangle_region_xy( x0, y0, x1, y1):

    rect_region = pya.Region()
    x0, y0, x1, y1 = base_units( ( x0, y0, x1, y1))
    rect_region.insert( pya.Box( x0, y0, x1, y1))
    return rect_region

def build_triangle_region_xy( x0, y0, x1, y1, x2, y2):
    rect_region = pya.Region()
    x0, y0, x1, y1, x2, y2 = base_units( ( x0, y0, x1, y1, x2, y2))
    points = []
    points.append(pya.Point( x0, y0))
    points.append(pya.Point( x1, y1))
    points.append(pya.Point( x2, y2))
    rect_region.insert( pya.SimplePolygon(points))
    return rect_region

def build_arc_region(x, y, radius, angle1, angle2):

    arc_region = pya.Region()
    x, y, radius = base_units( ( x, y, radius))
    angle1 = angle1 / 180 * np.pi
    angle2 = angle2 / 180 * np.pi
    nr_points = 32
    angles = np.linspace( angle1, angle2, nr_points)
    points = []
    # for ind, angle in enumerate( angles):
    for angle in angles:
        points.append( pya.Point( radius * np.cos(angle) + x, radius * np.sin( angle) + y))
    arc_region.insert( pya.SimplePolygon(points))
    return arc_region


