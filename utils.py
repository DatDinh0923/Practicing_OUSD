def rgb2pct(color_tuple):
    if len(color_tuple)==3:
        red_pct = color_tuple[0] / 255
        green_pct = color_tuple[1] / 255
        blue_pct = color_tuple[2] / 255
        return (red_pct, green_pct, blue_pct)
    
    else:
        return "ONLY accept RGB"
    
if __name__ == "__main__":
    print(rgb2pct((145,117,77)))
    # plank_widths = [False] + [True] * 5 + [False]*2
    # print(plank_widths)
    # Top Plank layer
    # pallet_width_Z = 120.0
    # plank_widths = [13.0, 11.0] + [9.5] * 5 + [11.0, 13.0]
    # has_gap_after = [False] + [True]*6 + [False]*2
    # total_plank_width = sum(plank_widths)
    # total_gaps = sum(has_gap_after)
    # gap_size = (pallet_width_Z - total_plank_width) / total_gaps

    # top_plank_layout = []
    # current_edge = -pallet_width_Z / 2.0

    # for i, width  in enumerate(plank_widths):
    #     centre_pos = current_edge + (width / 2)
    #     top_plank_layout.append((centre_pos, width))
    #     current_edge += width
    #     if has_gap_after[i]:
    #         current_edge += gap_size

    # print(top_plank_layout)

