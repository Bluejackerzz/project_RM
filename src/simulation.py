import cv2
import numpy as np
import os

def run_traffic_simulation(green_times, input_path='data/input_video.mp4', output_path='results/output_video.mp4'):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    lanes = ['north', 'south', 'east', 'west']
    lane_colors = {
        'green': (0, 255, 0),
        'red': (0, 0, 255)
    }

    phase_1 = ['north', 'south']
    phase_2 = ['east', 'west']

    duration_ns = max(int(green_times.get('north', 30)), 10)
    duration_ew = max(int(green_times.get('east', 30)), 10)

    total_frames_ns = duration_ns * fps
    total_frames_ew = duration_ew * fps

    lane_positions = {
        'north': (width//2 - 30, 50),
        'south': (width//2 - 30, height - 110),
        'east':  (width - 110, height//2 - 30),
        'west':  (50, height//2 - 30)
    }

    def overlay_lights(frame, active_lanes):
        for lane in lanes:
            color = lane_colors['green'] if lane in active_lanes else lane_colors['red']
            x, y = lane_positions[lane]
            cv2.rectangle(frame, (x, y), (x + 60, y + 60), color, -1)
            status = "GREEN" if lane in active_lanes else "RED"
            cv2.putText(frame, f"{lane.upper()}: {status}", (x - 30, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame

    current_phase = phase_1
    frame_counter = 0
    switch_point = total_frames_ns

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        frame = overlay_lights(frame, current_phase)
        out.write(frame)

        if frame_counter == switch_point:
            current_phase = phase_2 if current_phase == phase_1 else phase_1
            switch_point += total_frames_ew if current_phase == phase_2 else total_frames_ns

    cap.release()
    out.release()