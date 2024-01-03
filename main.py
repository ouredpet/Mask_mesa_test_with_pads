import numpy as np
import pya
import os

class mask_paramters():

    n_x_devices = 11
    n_y_devices = 11
    x_pitch = 600
    y_pitch = 600

    x_dev_size_sum = x_pitch * (n_x_devices + 1)
    y_dev_size_sum = y_pitch * (n_y_devices + 1)

    WF_size_small = 200

    mesa_off = 50

    pad_off = 5

    meas_areas = np.linspace(0.10, 0.52,22)
    mesa_under_etch = 0.1

    # Etching sizes
    island_L = 5
    island_W = 5
    island_ext = 0.5
    small_etching_area_side = 40
    large_etching_area_side = 120
    etch_overlap = 10

    # LE1 sizes
    small_LE_area_side = 40
    LE_pad = 150
    big_LE_area_side = 200

    # bridges
    Bridge_PR_island_x_trim = 0.1
    Bridge_PR_island_width = 1.5

    # LE2 sizes
    mesa_LE2_clearence_x = 3.5
    mesa_LE2_clearence_y = 3

    # WF markers size
    wf_marks_coordinates = []
    WF_marker_pitch = 20
    leg_len = 5
    leg_wid = 0.5
    flap_wid = 2
    flap_len = 2

    # Global markers size
    Global_marks_coordinates = []
    Global_marks_names = []
    Global_marker_pitch = 20
    Global_leg_len = 60
    Global_leg_wid = 5
    Global_marker_corner_pitch = ((n_x_devices+1)*x_pitch) + 400
    Global_marker_pitch = 200
    Global_marker_shift = ((n_x_devices-1)*x_pitch)/2
    Global_mark_off = 40
    Global_mark_off_x = -14
    Global_mark_text_size = 0.00005 # 14


    # shunt array
    shunt_array_w = 2
    shunt_array_l = 60
    shunt_array_pitch = 5
    shunt_array_number = 6
    shunt_array_off_beg = 5

    # shut
    g0 = 130e-3
    margin = 1.5
    ito_cond = 4e4 * 1e-6
    ito_thick = 250e-3
    ito_length = 15
    ito_pad = 50

    # SiN open
    mesa_open_margin = 0.1
    SiN_LE_open_size = 130

    # FE
    bridge_1_w = 1
    bridge_2_w = 2
    bridge_2_l = 1

    inner_w = 1

    inner_clearance = 1

    TL_extend = 10
    TL_width = 2

    FE_pad_size = 150

    # mesa fields
    mesa_fields_pitches = np.array((4,5,6,7))
    mesa_fields_areas = meas_areas
    mesa_field_x_pitch = 600
    mesa_field_y_pitch = 7200
    mesa_field_num = int(mesa_fields_areas.size/2)


#################################################################

mp = mask_paramters()

#################################################################

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

def wf_marks_coordinates_fun():
    marker_corner = (mp.WF_size_small - mp.WF_marker_pitch)/2

    for i_corner in range (4):
        row_s = np.sign(2*(i_corner%2)-1)
        column_s = np.sign(2*i_corner - 3)
        for i_row in range(3):
            for i_column in range(3 - i_row):
                x_marker_off = row_s * (marker_corner - i_column * mp.WF_marker_pitch)
                y_marker_off = column_s * (marker_corner - i_row * mp.WF_marker_pitch)
                mp.wf_marks_coordinates.append([x_marker_off, y_marker_off])

def Global_marks_coordinates_fun():
    marker_corner = mp.Global_marker_corner_pitch/2
    off = mp.Global_marker_shift
    

    for i_corner in range (4):
        row_s = np.sign(2*(i_corner%2)-1)
        column_s = np.sign(2*i_corner - 3)
        index = 0
        for i_row in range(3):
            for i_column in range(3 - i_row):
                x_marker_off = int(row_s * (marker_corner - i_column * mp.Global_marker_pitch) + off)
                y_marker_off = int(column_s * (marker_corner - i_row * mp.Global_marker_pitch) + off)
                mp.Global_marks_coordinates.append([x_marker_off, y_marker_off])
                mp.Global_marks_names.append(str(index))
                index += 1

#################################################################


def build_arc( layout, cell_name, layer_name, x, y, radius, angle1, angle2):

    arc_region = build_arc_region(x, y, radius, angle1, angle2)
    insert_region( layout, cell_name, layer_name, arc_region)

def build_rectangle( layout, cell_name, layer_name, W, H, x0, y0):

    rect_region = build_rectangle_region( W, H, x0, y0)
    insert_region( layout, cell_name, layer_name, rect_region)

def build_rectangle_xy( layout, cell_name, layer_name, W, H, x0, y0):

    rect_region = build_rectangle_region_xy( W, H, x0, y0)
    insert_region( layout, cell_name, layer_name, rect_region)

def build_rectangle_with_rhole( layout, cell_name, layer_name, W, H, x0, y0, Wh, Hh, x0h, y0h):

    rect_region = build_rectangle_region( W, H, x0, y0)
    hole_region = build_rectangle_region( Wh, Hh, x0 + x0h, y0 + y0h)
    rect_region_wh = rect_region - hole_region
    insert_region( layout, cell_name, layer_name, rect_region_wh)


# def build_arc_c( layout, cell, layer_name, x, y, radius, angle1, angle2):

#     arc_region = build_arc_region(x, y, radius, angle1, angle2)
#     insert_region_c( layout, cell, layer_name, arc_region)

# def build_rectangle_c( layout, cell, layer_name, W, H, x0, y0):

#     rect_region = build_rectangle_region( W, H, x0, y0)
#     insert_region_c( layout, cell, layer_name, rect_region)

# def build_rectangle_with_rhole_c( layout, cell, layer_name, W, H, x0, y0, Wh, Hh, x0h, y0h):

#     rect_region = build_rectangle_region( W, H, x0, y0)
#     hole_region = build_rectangle_region( Wh, Hh, x0 + x0h, y0 + y0h)
#     rect_region_wh = rect_region - hole_region
#     insert_region_c( layout, cell, layer_name, rect_region_wh)

def write_text(layout, cell_name, layer_name, size, x0, y0, rotate, text):
    gen = pya.TextGenerator()
    gen.load_from_file("vented_font_DDJ.gds")
    region = gen.text(text, size)
    x0, y0 = base_units( ( x0, y0))
    # trans = pya.Trans.new(pya.Trans.R90)
    trans = pya.Trans.new(rotate/180*np.pi)
    region.transform(trans)
    region.move(int(x0), int(y0))
    la = find_layer(layout, layer_name)
    ce = find_cell(layout, cell_name)
    ce.shapes(la).insert(region)

#################################################################

def build_mesas( layout, cell_name, area):

    separation = mp.mesa_off
    radius = ( area / np.pi) ** (1/2)
    radius += mp.mesa_under_etch
    build_arc( layout, cell_name, "FE_mesas", -separation/2, -separation/2, radius, 0, 360)
    build_arc( layout, cell_name, "FE_mesas", -separation/2, separation/2, radius, 0, 360)
    build_arc( layout, cell_name, "FE_mesas", separation/2, -separation/2, radius, 0, 360)
    build_arc( layout, cell_name, "FE_mesas", separation/2, separation/2, radius, 0, 360)

    write_text(layout, cell_name, "FE_dev_texts", 0.00004, 150, -250, 0, str(np.round(area*100)/100))

def build_WF_marker_cell( layout, layer_name):
    cell_name = "WF_marker"
    layout.create_cell( cell_name)

    off_leg = ( mp.leg_len + mp.leg_wid) / 2
    off_flap = mp.leg_len + ( mp.leg_wid + mp.flap_wid) / 2

    build_rectangle( layout, cell_name, layer_name, mp.leg_wid, mp.leg_len, 0, off_leg)
    build_rectangle( layout, cell_name, layer_name, mp.leg_len, mp.leg_wid, off_leg, 0)
    build_rectangle( layout, cell_name, layer_name, mp.leg_wid, mp.leg_len, 0, - off_leg)
    build_rectangle( layout, cell_name, layer_name, mp.leg_len, mp.leg_wid, - off_leg, 0)

    build_rectangle( layout, cell_name, layer_name, mp.leg_wid, mp.leg_wid, 0, 0)

    build_rectangle( layout, cell_name, layer_name, mp.flap_wid, mp.flap_len, 0, off_flap)
    build_rectangle( layout, cell_name, layer_name, mp.flap_len, mp.flap_wid, off_flap, 0)
    build_rectangle( layout, cell_name, layer_name, mp.flap_wid, mp.flap_len, 0, - off_flap)
    build_rectangle( layout, cell_name, layer_name, mp.flap_len, mp.flap_wid, - off_flap, 0)

    merge_shapes_in_cell_accros_layer(layout, layer_name, cell_name)


def build_Global_marker_cell( layout, layer_name):
    cell_name = "Global_marker"
    layout.create_cell( cell_name)

    off_leg = ( mp.Global_leg_len + mp.Global_leg_wid) / 2

    build_rectangle( layout, cell_name, layer_name, mp.Global_leg_wid, mp.Global_leg_len, 0, off_leg)
    build_rectangle( layout, cell_name, layer_name, mp.Global_leg_len, mp.Global_leg_wid, off_leg, 0)
    build_rectangle( layout, cell_name, layer_name, mp.Global_leg_wid, mp.Global_leg_len, 0, - off_leg)
    build_rectangle( layout, cell_name, layer_name, mp.Global_leg_len, mp.Global_leg_wid, - off_leg, 0)

    build_rectangle( layout, cell_name, layer_name, mp.Global_leg_wid, mp.Global_leg_wid, 0, 0)


    merge_shapes_in_cell_accros_layer(layout, layer_name, cell_name)




def build_WF_markers( layout, cell_name):
    cell = find_cell( layout, cell_name)

    for i_wf_coord in range(len(mp.wf_marks_coordinates)):
        sub_cell_to_TOPcell( layout, cell, "WF_marker", int(mp.wf_marks_coordinates[i_wf_coord][0]), int(mp.wf_marks_coordinates[i_wf_coord][1]))


def build_Global_markers( layout, cell_name):
    cell = find_cell( layout, cell_name)

    for i_Global_coord in range(len(mp.Global_marks_coordinates)):
        sub_cell_to_TOPcell( layout, cell, "Global_marker", int(mp.Global_marks_coordinates[i_Global_coord][0]), int(mp.Global_marks_coordinates[i_Global_coord][1]))
        write_text( layout, cell_name, "FE_big_marks_texts", mp.Global_mark_text_size,int(mp.Global_marks_coordinates[i_Global_coord][0] + mp.Global_mark_off + mp.Global_mark_off_x), int(mp.Global_marks_coordinates[i_Global_coord][1] - mp.Global_mark_off), 0, mp.Global_marks_names[i_Global_coord])

def build_p_islands( layout, cell_name, slot_w):

    island_L_e = mp.island_L + mp.island_ext
    island_off = (island_L_e + slot_w)/2 - mp.island_ext

    rect_region = build_rectangle_region( mp.small_etching_area_side, mp.small_etching_area_side, 0, 0)
    hole_region = build_rectangle_region( mp.island_W, island_L_e, 0, island_off)
    rect_region = rect_region - hole_region
    hole_region = build_rectangle_region( mp.island_W, island_L_e, 0, -island_off)
    rect_region_wh = rect_region - hole_region
    insert_region( layout, cell_name, "Islands_p", rect_region_wh)

    l_cover = ( mp.small_etching_area_side - mp.island_W) / 2
    xoff = - ( mp.island_W  + l_cover) / 2
    w_cover = 2
    yoff1 = slot_w/2 + island_L_e - w_cover/2 + mp.island_ext
    yoff2 = - slot_w/2 + mp.island_ext
    build_rectangle( layout, cell_name, "Islands_p_c", l_cover, w_cover, xoff, yoff1)
    build_rectangle( layout, cell_name, "Islands_p_c", l_cover, w_cover, xoff, yoff2)



    rect_region = build_rectangle_region( mp.large_etching_area_side, mp.large_etching_area_side, 0, 0)
    hole_region = build_rectangle_region( mp.small_etching_area_side - mp.etch_overlap, mp.small_etching_area_side - mp.etch_overlap, 0, 0)
    rect_region_wh = rect_region - hole_region
    insert_region( layout, cell_name, "Islands_p_big", rect_region_wh)

    l_cover = ( mp.large_etching_area_side - mp.small_etching_area_side + mp.etch_overlap) / 2
    xoff = -( mp.small_etching_area_side - mp.etch_overlap + mp.large_etching_area_side) / 4
    w_cover = 2
    yoff = mp.small_etching_area_side/2 - mp.etch_overlap/2
    build_rectangle( layout, cell_name, "Islands_p_big_c", l_cover, w_cover, xoff, yoff)


def build_p_LE_1( layout, cell_name, slot_w, slot_l):

    yoff_top_WF_stitch = mp.WF_size_small/2 + mp.LE_pad/2

    rect_region = build_rectangle_region( mp.small_LE_area_side, mp.small_LE_area_side, 0, 0)
    hole_region = build_rectangle_region( slot_l, slot_w, 0, 0)
    rect_region_wh = rect_region - hole_region

    insert_region( layout, cell_name, "LE1_p_small", rect_region_wh)

    l_cover = ( mp.small_LE_area_side - slot_l) / 2
    xoff = - ( slot_l  + l_cover) / 2
    w_cover = 2
    yoff1 = slot_w/2

    build_rectangle( layout, cell_name, "LE1_p_small_c", l_cover, w_cover, xoff, yoff1)


    rect_region = build_rectangle_region( mp.big_LE_area_side, mp.big_LE_area_side, 0, 0)

    for i_wf_coord in range(len(mp.wf_marks_coordinates)):
        hole_region = build_rectangle_region( mp.WF_marker_pitch, mp.WF_marker_pitch, mp.wf_marks_coordinates[i_wf_coord][0], mp.wf_marks_coordinates[i_wf_coord][1])
        rect_region = rect_region - hole_region

    insert_region( layout, cell_name, "LE1_p_big", rect_region)


    build_rectangle( layout, cell_name, "LE1_p_big", mp.LE_pad, mp.LE_pad, 0, yoff_top_WF_stitch)
    build_rectangle( layout, cell_name, "LE1_p_big", mp.LE_pad, mp.LE_pad, 0, -yoff_top_WF_stitch)

    build_rectangle( layout, cell_name, "LE1_p_big_c", mp.WF_size_small - 2 * 3 * mp.WF_marker_pitch, 2, 0, mp.WF_size_small/2)
    build_rectangle( layout, cell_name, "LE1_p_big_c", mp.WF_size_small - 2 * 3 * mp.WF_marker_pitch, 2, 0, -mp.WF_size_small/2)

def PR_bridges( layout, cell_name, slot_w):

    x_off_island_bridge = mp.island_W/2 + mp.Bridge_PR_island_x_trim
    y_off_island_bridge = slot_w/2 + mp.island_L/2

    build_rectangle( layout, cell_name, "Bridge_PR", mp.Bridge_PR_island_width, mp.island_L, x_off_island_bridge, y_off_island_bridge)
    build_rectangle( layout, cell_name, "Bridge_PR", mp.Bridge_PR_island_width, mp.island_L, -x_off_island_bridge, y_off_island_bridge)
    build_rectangle( layout, cell_name, "Bridge_PR", mp.Bridge_PR_island_width, mp.island_L, x_off_island_bridge, -y_off_island_bridge)
    build_rectangle( layout, cell_name, "Bridge_PR", mp.Bridge_PR_island_width, mp.island_L, -x_off_island_bridge, -y_off_island_bridge)


def build_p_LE_2( layout, cell_name, slot_w, slot_l):

    yoff_top_WF_stitch = mp.WF_size_small/2 + mp.LE_pad/2

    rect_region = build_rectangle_region( mp.small_LE_area_side, mp.small_LE_area_side, 0, 0)
    hole_region = build_rectangle_region( slot_l, slot_w, 0, 0)
    rect_region_wh = rect_region - hole_region
    yoff_cleanrence = (slot_w + mp.mesa_LE2_clearence_y)/2
    hole_region = build_rectangle_region( mp.mesa_LE2_clearence_x, mp.mesa_LE2_clearence_y, 0, yoff_cleanrence)
    rect_region_wh = rect_region_wh - hole_region
    hole_region = build_rectangle_region( mp.mesa_LE2_clearence_x, mp.mesa_LE2_clearence_y, 0, -yoff_cleanrence)
    rect_region_wh = rect_region_wh - hole_region

    insert_region( layout, cell_name, "LE2_p_small", rect_region_wh)

    l_cover = ( mp.small_LE_area_side - mp.mesa_LE2_clearence_x ) / 2
    xoff = - ( mp.mesa_LE2_clearence_x  + l_cover) / 2
    w_cover = 2
    yoff1 = slot_w/2 + mp.mesa_LE2_clearence_y

    build_rectangle( layout, cell_name, "LE2_p_small_c", l_cover, w_cover, xoff, yoff1)


    rect_region = build_rectangle_region( mp.big_LE_area_side, mp.big_LE_area_side, 0, 0)

    for i_wf_coord in range(len(mp.wf_marks_coordinates)):
        hole_region = build_rectangle_region( mp.WF_marker_pitch, mp.WF_marker_pitch, mp.wf_marks_coordinates[i_wf_coord][0], mp.wf_marks_coordinates[i_wf_coord][1])
        rect_region = rect_region - hole_region

    insert_region( layout, cell_name, "LE2_p_big", rect_region)


    build_rectangle( layout, cell_name, "LE2_p_big", mp.LE_pad, mp.LE_pad, 0, yoff_top_WF_stitch)
    build_rectangle( layout, cell_name, "LE2_p_big", mp.LE_pad, mp.LE_pad, 0, -yoff_top_WF_stitch)

    build_rectangle( layout, cell_name, "LE2_p_big_c", mp.WF_size_small - 2*3*mp.WF_marker_pitch, 2, 0, mp.WF_size_small/2)
    build_rectangle( layout, cell_name, "LE2_p_big_c", mp.WF_size_small - 2*3*mp.WF_marker_pitch, 2, 0, -mp.WF_size_small/2)

def SiN_opening( layout, cell_name, area):

    separation = mp.mesa_off

    radius_opening = ( area / np.pi) ** (1/2) - mp.mesa_open_margin
    radius_opening += mp.mesa_under_etch
    build_arc( layout, cell_name, "SiN_mesa", -separation/2, -separation/2, radius_opening, 0, 360)
    build_arc( layout, cell_name, "SiN_mesa", -separation/2, separation/2, radius_opening, 0, 360)
    build_arc( layout, cell_name, "SiN_mesa", separation/2, -separation/2, radius_opening, 0, 360)
    build_arc( layout, cell_name, "SiN_mesa", separation/2, separation/2, radius_opening, 0, 360)

    yoff_open_pad = mp.WF_size_small/2 + mp.LE_pad/2 + mp.pad_off

    build_rectangle( layout, cell_name, "SiN_big", mp.SiN_LE_open_size, mp.SiN_LE_open_size, 0, yoff_open_pad)
    build_rectangle( layout, cell_name, "SiN_big", mp.SiN_LE_open_size, mp.SiN_LE_open_size, 0, -yoff_open_pad)


def build_shunting( layout, cell_name, slot_l, area):

    for i_shunt_array in range(mp.shunt_array_number):
        xoff_shunt_array = slot_l/2 + mp.shunt_array_off_beg + i_shunt_array * mp.shunt_array_pitch
        build_rectangle( layout, cell_name, "Shunt_array", mp.shunt_array_w, mp.shunt_array_l, xoff_shunt_array, 0)
        build_rectangle( layout, cell_name, "Shunt_array", mp.shunt_array_w, mp.shunt_array_l, -xoff_shunt_array, 0)

    ito_width = 2 * area * mp.g0 * mp.margin * mp.ito_length / (mp.ito_cond * mp.ito_thick)

    ito_length_p = mp.ito_length + 2 * mp.ito_pad

    xoff_shunt = mp.LE_pad/2 + mp.ito_length/2 - (mp.LE_pad - mp.SiN_LE_open_size)/2
    yoff_shunt =  mp.WF_size_small/2 + mp.LE_pad/2

    build_rectangle( layout, cell_name, "Shunt", ito_length_p, ito_width, xoff_shunt, yoff_shunt)

def build_FE( layout, cell_name):
    subcell_name = "FE_inners"
    sub_cell = layout.create_cell( subcell_name)
    subcell_name = sub_cell.name
    separation = mp.mesa_off

    arm_size = 10
    temp = separation/2 - arm_size/2

    build_rectangle_xy( layout, subcell_name, "FE_small", -temp, -temp, -120, -(temp + arm_size))
    build_rectangle_xy( layout, subcell_name, "FE_small", -120, -temp, -280, -200)

    build_rectangle_xy( layout, subcell_name, "FE_small", -temp, temp, -120, (temp + arm_size))
    build_rectangle_xy( layout, subcell_name, "FE_small", -120, temp, -280, 200)

    build_rectangle_xy( layout, subcell_name, "FE_small", temp, -temp, 120, -(temp + arm_size))
    build_rectangle_xy( layout, subcell_name, "FE_small", 120, -temp, 280, -200)

    build_rectangle_xy( layout, subcell_name, "FE_small", temp, temp, 120, (temp + arm_size))
    build_rectangle_xy( layout, subcell_name, "FE_small", 120, temp, 280, 200)

    merge_shapes_in_cell_accros_layer(layout, "FE_small", subcell_name)

    sub_cell_to_TOPcell( layout, find_cell( layout, cell_name), subcell_name, 0, 0)

def build_pads(layout, cell_name):

    yoff_open_pad = mp.WF_size_small/2 + mp.LE_pad/2 + mp.pad_off

    build_rectangle( layout, cell_name, "FE_dev_pads", mp.LE_pad, mp.LE_pad, 0, yoff_open_pad)
    build_rectangle( layout, cell_name, "FE_dev_pads", mp.LE_pad, mp.LE_pad, 0, -yoff_open_pad)

def mesa_fields(layout, cell_name):
    meas_fields_areas = mp.mesa_fields_areas
    mesa_fields_radiuses = (meas_fields_areas/np.pi)**(1/2)
    mesa_fields_radiuses += mp.mesa_under_etch


    for i_mesa_field_row in range(2):
        for i_mesa_field in range(mp.mesa_field_num):
            rad = mesa_fields_radiuses[i_mesa_field_row * mp.mesa_field_num + i_mesa_field]

            x_off_mesa_text = i_mesa_field * mp.mesa_field_x_pitch - 100 + 20
            y_off_mesa_text = -mp.mesa_field_x_pitch + i_mesa_field_row * mp.mesa_field_y_pitch - 100 - 30

            write_text(layout, cell_name, "FE_mesa_fields_texts", 0.00004, x_off_mesa_text, y_off_mesa_text, 0, str(np.round(meas_fields_areas[i_mesa_field_row * mp.mesa_field_num + i_mesa_field]*100)/100))

            x_off = 200 + i_mesa_field * mp.mesa_field_x_pitch
            y_off = -600 + i_mesa_field_row * mp.mesa_field_y_pitch
            size_pad = 180

            build_rectangle( layout, cell_name, "FE_mesa_fields_pads", size_pad, size_pad, x_off,y_off)

            build_rectangle( layout, cell_name, "SiN_big", 200, 200, x_off,y_off)
            build_rectangle( layout, cell_name, "SiN_big", 200, 200, x_off-200,y_off)


            for i_mesa_row_q in range(2):
                for i_mesa_column_q in range(2):
                    pitch = mp.mesa_fields_pitches[i_mesa_row_q * 2 + i_mesa_column_q ] + 2 * rad
                    pitch_n = int((100)/pitch)
                    for i_mesa_row in range(pitch_n):
                        for i_mesa_column in range(pitch_n):
                            x_off_mesa = pitch/2 + i_mesa_field * mp.mesa_field_x_pitch - 100 + i_mesa_row_q * 100 + i_mesa_row * pitch
                            y_off_mesa = pitch/2 + -600 + i_mesa_field_row * mp.mesa_field_y_pitch - 100 + i_mesa_column_q * 100 + i_mesa_column * pitch
                            
                            build_arc( layout, cell_name, "FE_mesa_fields", x_off_mesa, y_off_mesa, rad, 0, 360)


#################################################################

def build_device( layout, cell_name, area):

    build_mesas( layout, cell_name, area)
    build_WF_markers( layout, cell_name)
    build_pads( layout, cell_name)
    # build_p_islands( layout, cell_name, slot_w)
    # build_p_LE_1( layout, cell_name, slot_w, slot_l)
    # PR_bridges( layout, cell_name, slot_w)
    # build_p_LE_2( layout, cell_name, slot_w, slot_l)
    SiN_opening( layout, cell_name, area)
    # build_shunting( layout, cell_name, slot_l, area)
    build_FE( layout, cell_name)

def build_AUX( layout, cell_name):
    build_Global_markers( layout, cell_name)
    write_text(layout, cell_name, "FE_text", 0.000004, -600, 4000, 90, "MESA_TEST_N8")
    # write_text(layout, cell_name, "FE_text", 0.000004, -600, 4000, 90, "MESA_TEST_N9")
    # write_text(layout, cell_name, "FE_text", 0.000004, -600, 4000, 90, "MESA_TEST_N12")
    # write_text(layout, cell_name, "FE_text", 0.000004, -600, 4000, 90, "MESA_TEST_N13")
    mesa_fields(layout, cell_name)


def init():

    layout = pya.Layout()
    build_layers( layout)
    top_cell = layout.create_cell( "TOP")
    build_WF_marker_cell( layout, "FE_WF_marks")
    build_Global_marker_cell( layout, "FE_big_marks")
    wf_marks_coordinates_fun()
    Global_marks_coordinates_fun()
    return layout, top_cell

def post_mortem(layout, top_cell):

    top_cell.flatten(1)

    # shift to final
    shiftx = mp.Global_marker_shift - 5000
    shifty = mp.Global_marker_shift - 5000
    trans = pya.Trans.new(int(-shiftx*1000),int(-shifty*1000))
    top_cell.transform(trans)

    path = os.path.join( "..", "gds", "mask_mesa_with_pads_1", "mesa_test_N8.gds")
    layout.write( path)


def build_layers( layout):

    layout.layer( 110, 0, "FE_mesas")
    layout.layer( 111, 0, "FE_WF_marks")
    layout.layer( 112, 0, "FE_dev_pads")
    layout.layer( 113, 0, "FE_dev_texts")
    layout.layer( 114, 0, "FE_big_marks")
    layout.layer( 115, 0, "FE_big_marks_texts")
    layout.layer( 116, 0, "FE_mesa_fields")
    layout.layer( 117, 0, "FE_mesa_fields_pads")
    layout.layer( 118, 0, "FE_mesa_fields_texts")
    layout.layer( 119, 0, "FE_text")
    # layout.layer( 120, 0, "Islands_p")
    # layout.layer( 121, 0, "Islands_p_c")
    # layout.layer( 122, 0, "Islands_p_big")
    # layout.layer( 123, 0, "Islands_p_big_c")
    # layout.layer( 130, 0, "LE1_p_small")
    # layout.layer( 131, 0, "LE1_p_small_c")
    # layout.layer( 132, 0, "LE1_p_big")
    # layout.layer( 133, 0, "LE1_p_big_c")
    # layout.layer( 140, 0, "Bridge_PR")
    # layout.layer( 150, 0, "LE2_p_small")
    # layout.layer( 151, 0, "LE2_p_small_c")
    # layout.layer( 152, 0, "LE2_p_big")
    # layout.layer( 153, 0, "LE2_p_big_c")
    layout.layer( 160, 0, "SiN_mesa")
    layout.layer( 161, 0, "SiN_big")
    # layout.layer( 170, 0, "Shunt_array")
    # layout.layer( 171, 0, "Shunt")
    layout.layer( 180, 0, "FE_small")
    layout.layer( 181, 0, "FE_big")

#################################################################

def main():

    layout, top_cell = init()

    

    for row_index in range(mp.n_x_devices):
        for column_index in range(mp.n_y_devices):

            mesa_radius_index = (row_index * mp.n_y_devices + column_index)%(mp.n_x_devices + mp.n_y_devices)

            active_cell_name = "D_" + str(column_index) + "_" + str(row_index)
            active_cell = layout.create_cell( active_cell_name)
            build_device( layout, active_cell_name, mp.meas_areas[mesa_radius_index])
            shift_cell( layout, active_cell_name, column_index * mp.x_pitch, row_index * mp.y_pitch)
            sub_cell_to_TOPcell( layout, top_cell, active_cell_name, 0, 0)

    build_AUX( layout, top_cell.name)

    post_mortem(layout, top_cell)


if __name__ == "__main__":
    main()
