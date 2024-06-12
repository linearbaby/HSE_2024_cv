import os

import ultralytics
from pathlib import Path


def process_video(file_path, filename, run_name):
    video_path = Path(file_path)
    save_dir = 'output_data'
    os.makedirs(save_dir, exist_ok=True)

    model = ultralytics.YOLO("best-street-cams-ft.pt")

    for result in model.track(
            video_path,
            save=True,
            project=save_dir,
            stream=True,
            persist=True,
            visualize=False,
            save_frames=False,
            imgsz=640,
            device="cpu",
    ):
        print(f"Saved in {save_dir}")

    return "output_data" + "/" + filename
