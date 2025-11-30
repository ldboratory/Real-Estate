# MoviePy 2.x Compatibility Fix

## Issue
The system was failing with:
```
ModuleNotFoundError: No module named 'moviepy.editor'
```

## Root Cause
- `requirements_pro.txt` specified MoviePy 1.0.3
- `pip install` installed MoviePy 2.2.1 instead (latest version)
- MoviePy 2.x has a completely different import structure than 1.x

## Changes Made

### Import Structure (pro_video_creator.py)

**Old (MoviePy 1.x):**
```python
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
```

**New (MoviePy 2.x):**
```python
from moviepy import (
    VideoClip, ImageClip, VideoFileClip, AudioFileClip,
    CompositeVideoClip, TextClip, concatenate_videoclips
)
from moviepy import vfx
```

### API Changes

**1. ImageClip:**
```python
# Old:
clip = ImageClip(chart_file).set_duration(duration)

# New:
clip = ImageClip(chart_file, duration=duration)
```

**2. Effects (Fade In/Out):**
```python
# Old:
clip = clip.fx(fadein, 0.5).fx(fadeout, 0.5)

# New:
clip = clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
```

**3. Audio:**
```python
# Old:
final_video = final_video.set_audio(audio)

# New:
final_video = final_video.with_audio(audio)
```

**4. TextClip:**
```python
# Old:
txt_clip = TextClip(
    text_info['text'],
    fontsize=60,
    color='white'
).set_position(('center', 'bottom')).set_start(0).set_duration(5)

# New:
txt_clip = TextClip(
    text=text_info['text'],
    font_size=60,
    color='white',
    duration=5
).with_position(('center', 'bottom')).with_start(0)
```

**5. Write VideoFile:**
```python
# Old:
clip.write_videofile(output_file, fps=30, codec='libx264')

# New (add logger=None to suppress verbose output):
clip.write_videofile(output_file, fps=30, codec='libx264', logger=None)
```

## Voice Generation Fix

### Issue
pyttsx3 was saving WAV files to wrong directory.

### Fix (pro_voice_generator.py)
```python
# Ensure output directory exists
output_path = Path(output_file)
output_path.parent.mkdir(parents=True, exist_ok=True)

# Save WAV in correct directory
wav_file = str(output_path.parent / 'temp_narration.wav')
```

## Test Results

✅ All components working:
- Investment analysis: Grade A detection
- Professional voice: MP3 generated (385KB)
- Data visualization: 4-panel chart (151KB)
- Final shorts: 2.1MB MP4 video (15 seconds)

## Generated Files

```
output/pro/
├── chart_temp.png              # 92KB - Chart image
├── data_viz.mp4                # 151KB - Data visualization video
├── investment_narration.mp3    # 385KB - Professional voice
├── investment_report.txt       # 1.4KB - Investment analysis report
└── investment_shorts_final.mp4 # 2.1MB - Final YouTube Shorts
```

## Usage

```bash
# Run with default settings (6억 budget, New York comparison)
python generate_pro_shorts.py

# Custom budget and city
python generate_pro_shorts.py --budget 800000000 --city "Tokyo"

# Available cities:
# - New York
# - Tokyo
# - London
# - Singapore
# - Shanghai
```

## Output Example

**Investment Grade:** A
**Budget Used:** $194,625 / $450,000
**Expected ROI:** -3.0% per year
**Advantage over New York:** 5.0%

**Video Structure:**
- 0-3s: Animated intro "INVESTMENT ALERT"
- 3-10s: 4-panel data visualization with narration
- 10-12s: Outro "Grade A Deal!"

## Next Steps

1. Upload `output/pro/investment_shorts_final.mp4` to YouTube Shorts
2. Test different cities for global comparisons
3. Adjust investment scoring weights if needed
4. Add background music (optional)
5. Automate daily shorts generation with cron
