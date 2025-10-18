import os
import json
import cv2
import subprocess

def extract_audio(video_path, output_audio):
    if os.path.exists(output_audio):
        print(f"[info] audio '{output_audio}' already exists, skipping extraction.")
        return output_audio

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "mp3",
        "-y",
        output_audio
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[done] audio extracted to '{output_audio}'")
    return output_audio

def compress_rle(data):
    if not data:
        return []

    compressed = []
    prev = data[0]
    count = 1
    for val in data[1:]:
        if val == prev:
            count += 1
        else:
            compressed.append([prev, count])
            prev = val
            count = 1
    compressed.append([prev, count])
    return compressed

def extract_frames(video_path, output_dir, fps_values=(30, 60), start_time=0, end_time=None):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    cap = cv2.VideoCapture(video_path)
    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / orig_fps

    if end_time is None or end_time > duration:
        end_time = duration

    start_frame = int(start_time * orig_fps)
    end_frame = int(end_time * orig_fps)

    for target_fps in fps_values:
        frame_dir = os.path.join(output_dir, f"{target_fps}fps")
        os.makedirs(frame_dir, exist_ok=True)

        frame_interval = max(1, round(orig_fps / target_fps))
        frame_idx = 0
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame_count >= end_frame:
                break

            if frame_count >= start_frame and frame_count % frame_interval == 0:
                timestamp = frame_count / orig_fps
                # padded frame number, 4 digits
                json_path = os.path.join(frame_dir, f"frame{frame_idx + 1:04}.json")

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pixel_data = frame_rgb.flatten().tolist()
                pixel_data_compressed = compress_rle(pixel_data)

                data = {
                    "pixel_data": pixel_data_compressed,
                    "width": width,
                    "height": height,
                    "sound": f"{base_name}.mp3",
                    "sound_timestamp": timestamp
                }

                with open(json_path, "w") as f:
                    json.dump(data, f)

                frame_idx += 1

            frame_count += 1

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    cap.release()
    print(f"[done] frames extracted for {base_name} from {start_time}s to {end_time}s")

def main():
    video_path = "bad-apple.mp4"
    output_dir = "framedata"
    audio_output = os.path.splitext(video_path)[0] + ".mp3"

    extract_audio(video_path, audio_output)
    extract_frames(video_path, output_dir, fps_values=(30, 60), start_time=0, end_time=42)

if __name__ == "__main__":
    main()
