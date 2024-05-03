import cv2
import argparse
from pathlib import Path
import threading 
import time
import queue

def capture_frames(cap, output_queue, stop_event):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        output_queue.put(frame)

    # Signal that capturing is done
    output_queue.put(None)

def write_video(output_path, input_queue, width, height, fps):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        frame = input_queue.get()
        if frame is None:  # None indicates end of frames
            break
        out.write(frame)

    out.release()

def main():
    cap = cv2.VideoCapture(1)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20.0
    output_queue = queue.Queue()
    stop_event = threading.Event()

    capture_thread = threading.Thread(target=capture_frames, args=(cap, output_queue, stop_event))
    write_thread = threading.Thread(target=write_video, args=("captured_video.mp4", output_queue, width, height, fps))

    capture_thread.start()
    write_thread.start()
    time.sleep(5)

    stop_event.set()

    capture_thread.join()
    write_thread.join()

    cap.release()  # Release camera resource

if __name__ == "__main__":
    main()
