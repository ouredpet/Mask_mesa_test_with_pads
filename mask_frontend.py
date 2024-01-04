import numpy as np
import pya
import mask_backend as mask_b
import mask_pya_aip as mpa

def wf_marks_coordinates_fun(mask_inst):
    marker_corner = (mask_inst.WF_size_small - mask_inst.WF_marker_pitch)/2

    for i_corner in range (4):
        row_s = np.sign(2*(i_corner%2)-1)
        column_s = np.sign(2*i_corner - 3)
        for i_row in range(3):
            for i_column in range(3 - i_row):
                x_marker_off = row_s * (marker_corner - i_column * mask_inst.WF_marker_pitch)
                y_marker_off = column_s * (marker_corner - i_row * mask_inst.WF_marker_pitch)
                mask_inst.wf_marks_coordinates.append([x_marker_off, y_marker_off])

def Global_marks_coordinates_fun(mask_inst):
    marker_corner = mask_inst.Global_marker_corner_pitch/2
    off = mask_inst.Global_marker_shift
    

    for i_corner in range (4):
        row_s = np.sign(2*(i_corner%2)-1)
        column_s = np.sign(2*i_corner - 3)
        index = 0
        for i_row in range(3):
            for i_column in range(3 - i_row):
                x_marker_off = int(row_s * (marker_corner - i_column * mask_inst.Global_marker_pitch) + off)
                y_marker_off = int(column_s * (marker_corner - i_row * mask_inst.Global_marker_pitch) + off)
                mask_inst.Global_marks_coordinates.append([x_marker_off, y_marker_off])
                mask_inst.Global_marks_names.append(str(index))
                index += 1


######################################################################

def build_mesas_pads( mask_inst, cell_name, area):

    separation = mask_inst.mesa_off_pads
    radius = ( area / np.pi) ** (1/2)
    radius += mask_inst.mesa_under_etch
    mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesas", -separation/2, -separation/2, radius, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesas", -separation/2, separation/2, radius, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesas", separation/2, -separation/2, radius, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesas", separation/2, separation/2, radius, 0, 360)

    mask_b.write_text(mask_inst.layout, cell_name, "FE_dev_texts", 0.00004, 150, -250, 0, "T" + str(np.round(area*100)/100))

def build_mesas( mask_inst, cell_name, slot_w, slot_l, area):

    separation = slot_w + 2 * mask_inst.mesa_off
    radius = ( area / np.pi) ** (1/2)
    radius += mask_inst.mesa_under_etch
    mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesas", 0, -separation/2, radius, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesas", 0, separation/2, radius, 0, 360)

    mask_b.write_text(mask_inst.layout, cell_name, "FE_dev_texts", 0.00004, 150, -250, 0, str(np.round(area*100)/100) + "/" + str(slot_w) + "/" + str(slot_l))

def build_WF_marker_cell( mask_inst, layer_name):
    cell_name = "WF_marker"
    mask_inst.layout.create_cell( cell_name)

    off_leg = ( mask_inst.leg_len + mask_inst.leg_wid) / 2
    off_flap = mask_inst.leg_len + ( mask_inst.leg_wid + mask_inst.flap_wid) / 2

    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.leg_wid, mask_inst.leg_len, 0, off_leg)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.leg_len, mask_inst.leg_wid, off_leg, 0)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.leg_wid, mask_inst.leg_len, 0, - off_leg)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.leg_len, mask_inst.leg_wid, - off_leg, 0)

    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.leg_wid, mask_inst.leg_wid, 0, 0)

    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.flap_wid, mask_inst.flap_len, 0, off_flap)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.flap_len, mask_inst.flap_wid, off_flap, 0)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.flap_wid, mask_inst.flap_len, 0, - off_flap)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.flap_len, mask_inst.flap_wid, - off_flap, 0)

    mpa.merge_shapes_in_cell_accros_layer(mask_inst.layout, layer_name, cell_name)


def build_Global_marker_cell( mask_inst, layer_name):
    cell_name = "Global_marker"
    mask_inst.layout.create_cell( cell_name)

    off_leg = ( mask_inst.Global_leg_len - mask_inst.Gobal_taper_len) / 2 + mask_inst.Gobal_taper_len

    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.Global_leg_wid, mask_inst.Global_leg_len - mask_inst.Gobal_taper_len, 0, off_leg)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.Global_leg_len - mask_inst.Gobal_taper_len, mask_inst.Global_leg_wid, off_leg, 0)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.Global_leg_wid, mask_inst.Global_leg_len - mask_inst.Gobal_taper_len, 0, - off_leg)
    mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.Global_leg_len - mask_inst.Gobal_taper_len, mask_inst.Global_leg_wid, - off_leg, 0)

    # mask_b.build_rectangle( mask_inst.layout, cell_name, layer_name, mask_inst.Global_leg_wid, mask_inst.Global_leg_wid, 0, 0)


    mask_b.build_triangle_xy( mask_inst.layout, cell_name, layer_name, 0, 0, -mask_inst.Global_leg_wid/2, mask_inst.Gobal_taper_len, mask_inst.Global_leg_wid/2, mask_inst.Gobal_taper_len)
    mask_b.build_triangle_xy( mask_inst.layout, cell_name, layer_name, 0, 0, -mask_inst.Global_leg_wid/2, -mask_inst.Gobal_taper_len, mask_inst.Global_leg_wid/2, -mask_inst.Gobal_taper_len)

    mask_b.build_triangle_xy( mask_inst.layout, cell_name, layer_name, 0, 0, mask_inst.Gobal_taper_len, -mask_inst.Global_leg_wid/2, mask_inst.Gobal_taper_len, mask_inst.Global_leg_wid/2)
    mask_b.build_triangle_xy( mask_inst.layout, cell_name, layer_name, 0, 0, -mask_inst.Gobal_taper_len, -mask_inst.Global_leg_wid/2, -mask_inst.Gobal_taper_len, mask_inst.Global_leg_wid/2)
    

    mpa.merge_shapes_in_cell_accros_layer(mask_inst.layout, layer_name, cell_name)



def build_WF_markers( mask_inst, cell_name):
    cell = mpa.find_cell( mask_inst.layout, cell_name)

    for i_wf_coord in range(len(mask_inst.wf_marks_coordinates)):
        mpa.sub_cell_to_TOPcell( mask_inst.layout, cell, "WF_marker", int(mask_inst.wf_marks_coordinates[i_wf_coord][0]), int(mask_inst.wf_marks_coordinates[i_wf_coord][1]))


def build_Global_markers( mask_inst, cell_name):
    cell = mpa.find_cell( mask_inst.layout, cell_name)

    for i_Global_coord in range(len(mask_inst.Global_marks_coordinates)):
        mpa.sub_cell_to_TOPcell( mask_inst.layout, cell, "Global_marker", int(mask_inst.Global_marks_coordinates[i_Global_coord][0]), int(mask_inst.Global_marks_coordinates[i_Global_coord][1]))
        mask_b.write_text( mask_inst.layout, cell_name, "FE_big_marks_texts", mask_inst.Global_mark_text_size,int(mask_inst.Global_marks_coordinates[i_Global_coord][0] + mask_inst.Global_mark_off + mask_inst.Global_mark_off_x), int(mask_inst.Global_marks_coordinates[i_Global_coord][1] - mask_inst.Global_mark_off), 0, mask_inst.Global_marks_names[i_Global_coord])

def build_p_islands( mask_inst, cell_name, slot_w):

    island_L_e = mask_inst.island_L + mask_inst.island_ext
    island_off = (island_L_e + slot_w)/2 - mask_inst.island_ext

    rect_region = mpa.build_rectangle_region( mask_inst.small_etching_area_side, mask_inst.small_etching_area_side, 0, 0)
    hole_region = mpa.build_rectangle_region( mask_inst.island_W, island_L_e, 0, island_off)
    rect_region = rect_region - hole_region
    hole_region = mpa.build_rectangle_region( mask_inst.island_W, island_L_e, 0, -island_off)
    rect_region_wh = rect_region - hole_region
    mpa.insert_region( mask_inst.layout, cell_name, "Islands_p", rect_region_wh)

    l_cover = ( mask_inst.small_etching_area_side - mask_inst.island_W) / 2
    xoff = - ( mask_inst.island_W  + l_cover) / 2
    w_cover = 2
    yoff1 = slot_w/2 + island_L_e - w_cover/2 + mask_inst.island_ext
    yoff2 = - slot_w/2 + mask_inst.island_ext
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Islands_p_c", l_cover, w_cover, xoff, yoff1)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Islands_p_c", l_cover, w_cover, xoff, yoff2)



    rect_region = mpa.build_rectangle_region( mask_inst.large_etching_area_side, mask_inst.large_etching_area_side, 0, 0)
    hole_region = mpa.build_rectangle_region( mask_inst.small_etching_area_side - mask_inst.etch_overlap, mask_inst.small_etching_area_side - mask_inst.etch_overlap, 0, 0)
    rect_region_wh = rect_region - hole_region
    mpa.insert_region( mask_inst.layout, cell_name, "Islands_p_big", rect_region_wh)

    l_cover = ( mask_inst.large_etching_area_side - mask_inst.small_etching_area_side + mask_inst.etch_overlap) / 2
    xoff = -( mask_inst.small_etching_area_side - mask_inst.etch_overlap + mask_inst.large_etching_area_side) / 4
    w_cover = 2
    yoff = mask_inst.small_etching_area_side/2 - mask_inst.etch_overlap/2
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Islands_p_big_c", l_cover, w_cover, xoff, yoff)


def build_p_LE_1( mask_inst, cell_name, slot_w, slot_l):

    yoff_top_WF_stitch = mask_inst.WF_size_small/2 + mask_inst.LE_pad/2

    rect_region = mpa.build_rectangle_region( mask_inst.small_LE_area_side, mask_inst.small_LE_area_side, 0, 0)
    hole_region = mpa.build_rectangle_region( slot_l, slot_w, 0, 0)
    rect_region_wh = rect_region - hole_region

    mpa.insert_region( mask_inst.layout, cell_name, "LE1_p_small", rect_region_wh)

    l_cover = ( mask_inst.small_LE_area_side - slot_l) / 2
    xoff = - ( slot_l  + l_cover) / 2
    w_cover = 2
    yoff1 = slot_w/2

    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE1_p_small_c", l_cover, w_cover, xoff, yoff1)


    rect_region = mpa.build_rectangle_region( mask_inst.big_LE_area_side, mask_inst.big_LE_area_side, 0, 0)

    for i_wf_coord in range(len(mask_inst.wf_marks_coordinates)):
        hole_region = mpa.build_rectangle_region( mask_inst.WF_marker_pitch, mask_inst.WF_marker_pitch, mask_inst.wf_marks_coordinates[i_wf_coord][0], mask_inst.wf_marks_coordinates[i_wf_coord][1])
        rect_region = rect_region - hole_region

    mpa.insert_region( mask_inst.layout, cell_name, "LE1_p_big", rect_region)


    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE1_p_big", mask_inst.LE_pad, mask_inst.LE_pad, 0, yoff_top_WF_stitch)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE1_p_big", mask_inst.LE_pad, mask_inst.LE_pad, 0, -yoff_top_WF_stitch)

    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE1_p_big_c", mask_inst.WF_size_small - 2 * 3 * mask_inst.WF_marker_pitch, 2, 0, mask_inst.WF_size_small/2)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE1_p_big_c", mask_inst.WF_size_small - 2 * 3 * mask_inst.WF_marker_pitch, 2, 0, -mask_inst.WF_size_small/2)

def PR_bridges( mask_inst, cell_name, slot_w):

    x_off_island_bridge = mask_inst.island_W/2 + mask_inst.Bridge_PR_island_x_trim
    y_off_island_bridge = slot_w/2 + mask_inst.island_L/2

    mask_b.build_rectangle( mask_inst.layout, cell_name, "Bridge_PR", mask_inst.Bridge_PR_island_width, mask_inst.island_L, x_off_island_bridge, y_off_island_bridge)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Bridge_PR", mask_inst.Bridge_PR_island_width, mask_inst.island_L, -x_off_island_bridge, y_off_island_bridge)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Bridge_PR", mask_inst.Bridge_PR_island_width, mask_inst.island_L, x_off_island_bridge, -y_off_island_bridge)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Bridge_PR", mask_inst.Bridge_PR_island_width, mask_inst.island_L, -x_off_island_bridge, -y_off_island_bridge)


def build_p_LE_2( mask_inst, cell_name, slot_w, slot_l):

    yoff_top_WF_stitch = mask_inst.WF_size_small/2 + mask_inst.LE_pad/2

    rect_region = mpa.build_rectangle_region( mask_inst.small_LE_area_side, mask_inst.small_LE_area_side, 0, 0)
    hole_region = mpa.build_rectangle_region( slot_l, slot_w, 0, 0)
    rect_region_wh = rect_region - hole_region
    yoff_cleanrence = (slot_w + mask_inst.mesa_LE2_clearence_y)/2
    hole_region = mpa.build_rectangle_region( mask_inst.mesa_LE2_clearence_x, mask_inst.mesa_LE2_clearence_y, 0, yoff_cleanrence)
    rect_region_wh = rect_region_wh - hole_region
    hole_region = mpa.build_rectangle_region( mask_inst.mesa_LE2_clearence_x, mask_inst.mesa_LE2_clearence_y, 0, -yoff_cleanrence)
    rect_region_wh = rect_region_wh - hole_region

    mpa.insert_region( mask_inst.layout, cell_name, "LE2_p_small", rect_region_wh)

    l_cover = ( mask_inst.small_LE_area_side - mask_inst.mesa_LE2_clearence_x ) / 2
    xoff = - ( mask_inst.mesa_LE2_clearence_x  + l_cover) / 2
    w_cover = 2
    yoff1 = slot_w/2 + mask_inst.mesa_LE2_clearence_y

    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE2_p_small_c", l_cover, w_cover, xoff, yoff1)


    rect_region = mpa.build_rectangle_region( mask_inst.big_LE_area_side, mask_inst.big_LE_area_side, 0, 0)

    for i_wf_coord in range(len(mask_inst.wf_marks_coordinates)):
        hole_region = mpa.build_rectangle_region( mask_inst.WF_marker_pitch, mask_inst.WF_marker_pitch, mask_inst.wf_marks_coordinates[i_wf_coord][0], mask_inst.wf_marks_coordinates[i_wf_coord][1])
        rect_region = rect_region - hole_region

    mpa.insert_region( mask_inst.layout, cell_name, "LE2_p_big", rect_region)


    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE2_p_big", mask_inst.LE_pad, mask_inst.LE_pad, 0, yoff_top_WF_stitch)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE2_p_big", mask_inst.LE_pad, mask_inst.LE_pad, 0, -yoff_top_WF_stitch)

    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE2_p_big_c", mask_inst.WF_size_small - 2*3*mask_inst.WF_marker_pitch, 2, 0, mask_inst.WF_size_small/2)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "LE2_p_big_c", mask_inst.WF_size_small - 2*3*mask_inst.WF_marker_pitch, 2, 0, -mask_inst.WF_size_small/2)

def SiN_opening_pads( mask_inst, cell_name, area):

    separation = mask_inst.mesa_off_pads

    radius_opening = ( area / np.pi) ** (1/2) - mask_inst.mesa_open_margin
    radius_opening += mask_inst.mesa_under_etch
    mask_b.build_arc( mask_inst.layout, cell_name, "SiN_mesa", -separation/2, -separation/2, radius_opening, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "SiN_mesa", -separation/2, separation/2, radius_opening, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "SiN_mesa", separation/2, -separation/2, radius_opening, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "SiN_mesa", separation/2, separation/2, radius_opening, 0, 360)

    yoff_open_pad = mask_inst.WF_size_small/2 + mask_inst.LE_pad/2 + mask_inst.pad_off

    mask_b.build_rectangle( mask_inst.layout, cell_name, "SiN_big", mask_inst.SiN_LE_open_size, mask_inst.SiN_LE_open_size, 0, yoff_open_pad)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "SiN_big", mask_inst.SiN_LE_open_size, mask_inst.SiN_LE_open_size, 0, -yoff_open_pad)

def SiN_opening( mask_inst, cell_name, slot_w, area):

    separation = slot_w + 2 * mask_inst.mesa_off

    radius_opening = ( area / np.pi) ** (1/2) - mask_inst.mesa_open_margin
    radius_opening += mask_inst.mesa_under_etch
    mask_b.build_arc( mask_inst.layout, cell_name, "SiN_mesa", 0, -separation/2, radius_opening, 0, 360)
    mask_b.build_arc( mask_inst.layout, cell_name, "SiN_mesa", 0, separation/2, radius_opening, 0, 360)

    yoff_open_pad = mask_inst.WF_size_small/2 + mask_inst.LE_pad/2

    mask_b.build_rectangle( mask_inst.layout, cell_name, "SiN_big", mask_inst.SiN_LE_open_size, mask_inst.SiN_LE_open_size, 0, yoff_open_pad)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "SiN_big", mask_inst.SiN_LE_open_size, mask_inst.SiN_LE_open_size, 0, -yoff_open_pad)


def build_shunting( mask_inst, cell_name, slot_l, area):

    for i_shunt_array in range(mask_inst.shunt_array_number):
        xoff_shunt_array = slot_l/2 + mask_inst.shunt_array_off_beg + i_shunt_array * mask_inst.shunt_array_pitch
        mask_b.build_rectangle( mask_inst.layout, cell_name, "Shunt_array", mask_inst.shunt_array_w, mask_inst.shunt_array_l, xoff_shunt_array, 0)
        mask_b.build_rectangle( mask_inst.layout, cell_name, "Shunt_array", mask_inst.shunt_array_w, mask_inst.shunt_array_l, -xoff_shunt_array, 0)

    ito_width = 2 * area * mask_inst.g0 * mask_inst.margin * mask_inst.ito_length / (mask_inst.ito_cond * mask_inst.ito_thick)
    ito_width = ito_width/2

    ito_length_p = mask_inst.ito_length + 2 * mask_inst.ito_pad

    xoff_shunt = mask_inst.LE_pad/2 + mask_inst.ito_length/2 - (mask_inst.LE_pad - mask_inst.SiN_LE_open_size)/2
    yoff_shunt =  mask_inst.WF_size_small/2 + mask_inst.LE_pad/2

    mask_b.build_rectangle( mask_inst.layout, cell_name, "Shunt", ito_length_p, ito_width, xoff_shunt, yoff_shunt)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "Shunt", ito_length_p, ito_width, xoff_shunt, -yoff_shunt)

def build_FE_pads( mask_inst, cell_name):
    subcell_name = "FE_inners"
    sub_cell = mask_inst.layout.create_cell( subcell_name)
    subcell_name = sub_cell.name
    separation = mask_inst.mesa_off_pads

    arm_size = 10
    temp = separation/2 - arm_size/2

    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", -temp, -temp, -120, -(temp + arm_size))
    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", -120, -temp, -280, -200)

    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", -temp, temp, -120, (temp + arm_size))
    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", -120, temp, -280, 200)

    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", temp, -temp, 120, -(temp + arm_size))
    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", 120, -temp, 280, -200)

    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", temp, temp, 120, (temp + arm_size))
    mask_b.build_rectangle_xy( mask_inst.layout, subcell_name, "FE_small", 120, temp, 280, 200)

    mpa.merge_shapes_in_cell_accros_layer(mask_inst.layout, "FE_small", subcell_name)

    mpa.sub_cell_to_TOPcell( mask_inst.layout, mpa.find_cell( mask_inst.layout, cell_name), subcell_name, 0, 0)

def build_FE( mask_inst, cell_name, slot_w, slot_l, area):
    subcell_name = "FE_inners"
    sub_cell = mask_inst.layout.create_cell( subcell_name)
    subcell_name = sub_cell.name


    separation = slot_w + 2 * mask_inst.mesa_off
    radius = ( area / np.pi) ** (1/2)
    radius += mask_inst.mesa_under_etch

    bridge_1_l = slot_w/2 + mask_inst.mesa_off - mask_inst.bridge_2_l - mask_inst.inner_w/2
    bridge_1_yoff = bridge_1_l/2 + mask_inst.bridge_2_l + mask_inst.inner_w/2
    bridge_2_yoff = mask_inst.bridge_2_l/2 + mask_inst.inner_w/2

    inner_l = slot_l + 2 * mask_inst.inner_clearance

    mask_b.build_arc( mask_inst.layout, subcell_name, "FE_small", 0, separation/2, radius, 0, 180)
    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", mask_inst.bridge_1_w, bridge_1_l, 0, bridge_1_yoff)
    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", mask_inst.bridge_2_w, mask_inst.bridge_2_l, 0, bridge_2_yoff)

    mask_b.build_arc( mask_inst.layout, subcell_name, "FE_small", 0, -separation/2, radius, 180, 360)
    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", mask_inst.bridge_1_w, bridge_1_l, 0, -bridge_1_yoff)
    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", mask_inst.bridge_2_w, mask_inst.bridge_2_l, 0, -bridge_2_yoff)

    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", inner_l, mask_inst.inner_w, 0, 0)

    TL_len = (mask_inst.WF_size_small - inner_l)/2 + mask_inst.TL_extend
    TL_yoff = inner_l/2 + TL_len/2

    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", TL_len, mask_inst.TL_width, TL_yoff, 0)
    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", TL_len, mask_inst.TL_width, -TL_yoff, 0)

    pad_off = inner_l/2 + TL_len + mask_inst.FE_pad_size/2 - mask_inst.TL_extend/2

    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", mask_inst.FE_pad_size, mask_inst.FE_pad_size, pad_off, 0)
    mask_b.build_rectangle( mask_inst.layout, subcell_name, "FE_small", mask_inst.FE_pad_size, mask_inst.FE_pad_size, -pad_off, 0)

    mpa. merge_shapes_in_cell_accros_layer(mask_inst.layout, "FE_small", subcell_name)

    mpa.sub_cell_to_TOPcell( mask_inst.layout, mpa.find_cell( mask_inst.layout, cell_name), subcell_name, 0, 0)



def build_pads(mask_inst, cell_name):

    yoff_open_pad = mask_inst.WF_size_small/2 + mask_inst.LE_pad/2 + mask_inst.pad_off

    mask_b.build_rectangle( mask_inst.layout, cell_name, "FE_dev_pads", mask_inst.LE_pad, mask_inst.LE_pad, 0, yoff_open_pad)
    mask_b.build_rectangle( mask_inst.layout, cell_name, "FE_dev_pads", mask_inst.LE_pad, mask_inst.LE_pad, 0, -yoff_open_pad)

def mesa_fields( mask_inst, cell_name):
    meas_fields_areas = mask_inst.mesa_fields_areas
    mesa_fields_radiuses = (meas_fields_areas/np.pi)**(1/2)
    mesa_fields_radiuses += mask_inst.mesa_under_etch


    for i_mesa_field_row in range(2):
        for i_mesa_field in range(mask_inst.mesa_field_num):
            rad = mesa_fields_radiuses[i_mesa_field_row * mask_inst.mesa_field_num + i_mesa_field]

            x_off_mesa_text = i_mesa_field * mask_inst.mesa_field_x_pitch - 100 + 20
            y_off_mesa_text = -mask_inst.mesa_field_x_pitch + i_mesa_field_row * mask_inst.mesa_field_y_pitch - 100 - 30

            mask_b.write_text(mask_inst.layout, cell_name, "FE_mesa_fields_texts", 0.00004, x_off_mesa_text, y_off_mesa_text, 0, str(np.round(meas_fields_areas[i_mesa_field_row * mask_inst.mesa_field_num + i_mesa_field]*100)/100))

            x_off = 200 + i_mesa_field * mask_inst.mesa_field_x_pitch
            y_off = -600 + i_mesa_field_row * mask_inst.mesa_field_y_pitch
            size_pad = 180

            mask_b.build_rectangle( mask_inst.layout, cell_name, "FE_mesa_fields_pads", size_pad, size_pad, x_off,y_off)

            mask_b.build_rectangle( mask_inst.layout, cell_name, "SiN_big", 200, 200, x_off,y_off)
            mask_b.build_rectangle( mask_inst.layout, cell_name, "SiN_big", 200, 200, x_off-200,y_off)


            for i_mesa_row_q in range(2):
                for i_mesa_column_q in range(2):
                    pitch = mask_inst.mesa_fields_pitches[i_mesa_row_q * 2 + i_mesa_column_q ] + 2 * rad
                    pitch_n = int((100)/pitch)
                    for i_mesa_row in range(pitch_n):
                        for i_mesa_column in range(pitch_n):
                            x_off_mesa = pitch/2 + i_mesa_field * mask_inst.mesa_field_x_pitch - 100 + i_mesa_row_q * 100 + i_mesa_row * pitch
                            y_off_mesa = pitch/2 + -600 + i_mesa_field_row * mask_inst.mesa_field_y_pitch - 100 + i_mesa_column_q * 100 + i_mesa_column * pitch
                            
                            mask_b.build_arc( mask_inst.layout, cell_name, "FE_mesa_fields", x_off_mesa, y_off_mesa, rad, 0, 360)


#################################################################