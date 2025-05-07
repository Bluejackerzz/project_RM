import cv2
import numpy as np

def run_traffic_simulation(green_times, output_path='results/output_video.mp4'):
    width, height = 800, 800
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 1, (width, height))

    lanes = ['north', 'south', 'east', 'west']
    lane_colors = {
        'green': (0, 255, 0),
        'red': (0, 0, 255)
    }

    # Tentukan grup lampu menyala berpasangan (north-south vs east-west)
    phase_1 = ['north', 'south']
    phase_2 = ['east', 'west']

    duration_ns = max(int(green_times.get('north', 30)), 10)
    duration_ew = max(int(green_times.get('east', 30)), 10)

    def draw_frame(active_lanes):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        lane_positions = {
            'north': (370, 50),
            'south': (370, 700),
            'east':  (700, 370),
            'west':  (50, 370)
        }

        for lane in lanes:
            color = lane_colors['green'] if lane in active_lanes else lane_colors['red']
            x, y = lane_positions[lane]
            if lane in ['north', 'south']:
                cv2.rectangle(frame, (x, y), (x + 60, y + 60), color, -1)
            else:
                cv2.rectangle(frame, (x, y), (x + 60, y + 60), color, -1)

            status = "GREEN" if lane in active_lanes else "RED"
            cv2.putText(frame, f"{lane.upper()}: {status}", (x - 30, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame

    # Simulasikan fase north-south
    for _ in range(duration_ns):
        frame = draw_frame(phase_1)
        out.write(frame)

    # Simulasikan fase east-west
    for _ in range(duration_ew):
        frame = draw_frame(phase_2)
        out.write(frame)

    out.release()