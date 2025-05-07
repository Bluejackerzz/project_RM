def count_vehicles_per_lane(detections_per_frame, lane_rois):
    lane_totals = {lane: 0 for lane in lane_rois}

    for detections in detections_per_frame:
        frame_count = {lane: 0 for lane in lane_rois}
        for (cx, cy) in detections:
            for lane, (x1, y1, x2, y2) in lane_rois.items():
                if x1 <= cx <= x2 and y1 <= cy <= y2:
                    frame_count[lane] += 1
        for lane in lane_totals:
            lane_totals[lane] += frame_count[lane]

    return lane_totals
