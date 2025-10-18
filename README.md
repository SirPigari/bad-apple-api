# 🍎 Bad Apple API

A static API for serving Bad Apple frame data via GitHub Pages.

## 📁 Project Structure

```
bad-apple-api/
├── api/
│   ├── bad-apple.mp3          # Audio file
│   ├── bad-apple.mp4          # Video file  
│   ├── generate.py            # Frame generation script
│   └── framedata/
│       ├── 30fps/             # 1260 frame files at 30 FPS
│       │   ├── frame1.json
│       │   ├── frame2.json
│       │   └── ... (frame1-frame1260)
│       └── 60fps/             # Frame files at 60 FPS (if available)
├── .github/
│   └── workflows/
│       ├── deploy.yml         # GitHub Pages deployment
│       └── validate-data.yml  # Data validation workflow
└── README.md
```

## 📋 Frame Data

### Available Data
- **Total frames (30fps)**: 1,260 frames
- **Frame format**: JSON with pixel data
- **Resolution**: 480x360 pixels
- **Audio**: Included as `bad-apple.mp3`

### Frame Structure
Each frame file (`frameX.json`) contains:
```json
{
  "pixel_data": [[0, 518400]],
  "width": 480,
  "height": 360, 
  "sound": "bad-apple.mp3",
  "sound_timestamp": 0.0
}
```

## 🚀 API Usage

### Direct File Access
Access individual frames directly via GitHub Pages:

```javascript
// Get a specific frame
fetch('https://sirpigari.github.io/bad-apple-api/api/framedata/30fps/frame0001.json')
  .then(response => response.json())
  .then(frame => {
    console.log(`Frame dimensions: ${frame.width}x${frame.height}`);
    console.log('Pixel data:', frame.pixel_data);
  });

// Get multiple frames
async function getFrames(start, end) {
  const frames = [];
  for (let i = start; i <= end; i++) {
    const frameFile = `frame${String(i).padStart(4, '0')}.json`; // pad to 4 digits
    const response = await fetch(`https://sirpigari.github.io/bad-apple-api/api/framedata/30fps/${frameFile}`);
    const frame = await response.json();
    frames.push(frame);
  }
  return frames;
}

// Get frames 1-10
getFrames(1, 10).then(frames => console.log(frames));
```

### Bulk Access Examples

#### Python
```python
import requests
import json

# Get a single frame
response = requests.get('https://sirpigari.github.io/bad-apple-api/api/framedata/30fps/frame1.json')
frame = response.json()
print(f"Frame size: {frame['width']}x{frame['height']}")

# Get multiple frames
def get_frame_range(start, end):
    frames = []
    for i in range(start, end + 1):
        url = f'https://sirpigari.github.io/bad-apple-api/api/framedata/30fps/frame{i}.json'
        response = requests.get(url)
        if response.status_code == 200:
            frames.append(response.json())
    return frames

frames = get_frame_range(1, 100)  # Get first 100 frames
```

#### cURL
```bash
# Get single frame
curl -o frame1.json https://sirpigari.github.io/bad-apple-api/api/framedata/30fps/frame1.json

# Download multiple frames using bash loop
for i in {1..100}; do
  curl -o "frame${i}.json" "https://sirpigari.github.io/bad-apple-api/api/framedata/30fps/frame${i}.json"
done
```

## 🎵 Media Files

### Audio
- **File**: `api/bad-apple.mp3`
- **URL**: `https://sirpigari.github.io/bad-apple-api/api/bad-apple.mp3`

### Video  
- **File**: `api/bad-apple.mp4`
- **URL**: `https://sirpigari.github.io/bad-apple-api/api/bad-apple.mp4`

## 🔧 Development

### Frame Generation
The project includes a Python script (`api/generate.py`) for generating frame data from the source video.

### GitHub Actions
- **Auto-deployment** to GitHub Pages on push to main
- **Data validation** workflows for quality assurance

### Adding New Frame Data
1. Place new frame JSON files in appropriate FPS directory
2. Follow the existing naming convention (`frameX.json`)
3. Ensure JSON structure matches existing format
4. Push to trigger automatic deployment

## 📊 Frame Data Details

- **Frame count**: 1,260 frames
- **Duration**: ~42 seconds at 30 FPS  
- **Pixel encoding**: Run-length encoded pixel data
- **Audio sync**: Each frame includes sound timestamp

## 🌐 CORS & Access

All files are served with CORS headers enabled, making them accessible from any domain for web applications.

## 📄 License

This project is open source and available under the MIT License.
