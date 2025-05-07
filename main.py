from src.detection import detect_vehicles
from src.counting import count_vehicles_per_lane
from src.fuzzy_controller import get_green_times
from src.simulation import run_traffic_simulation

lane_rois = {
    'north': (600,   0, 760, 250),
    'south': (600, 520, 760, 768),
    'east':  (850, 300, 1365, 470),
    'west':  (0,   300, 500, 470),
}

video_path = 'data/input_video.mp4'

detections = detect_vehicles(video_path)
lane_totals = count_vehicles_per_lane(detections, lane_rois)
green_times = get_green_times(lane_totals)
run_traffic_simulation(green_times)

print("\n=== HASIL SIMULASI ===")
print(f"Durasi North-South: {int(green_times.get('north', 30))} detik")
print(f"Durasi East-West  : {int(green_times.get('east', 30))} detik")
print("\nNorth & South = GREEN saat East & West = RED")
print("East & West = GREEN saat North & South = RED")
print("Video simulasi disimpan di: results/output_video.mp4")
