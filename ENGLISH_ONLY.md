# ✅ English-Only Version (No Character Issues)

All Korean text has been replaced with English to prevent character encoding issues in videos.

## 🎯 Changes Made

### 1. Visualizer (visualizer.py)
- **Fonts**: Arial, Helvetica (English fonts only)
- **Chart Title**: "Seoul Real Estate Price Trend"
- **Axis Labels**: "Month", "Average Price ($100M KRW)"
- **Price Display**: "$1.2B" instead of "1.2억"

### 2. Data Processor (data_processor.py)
- **Script**: "Today's Seoul real estate hot deals!"
- **Format**: "Number 1, Apartment Name, 199 square feet, $2K!"
- **Currency**: USD approximation (1억 ≈ $75K)

### 3. Voice Narration (voice_generator.py)
- **Language**: English (lang='en')
- **gTTS**: English voice synthesis

## 🚀 Quick Start

### Method 1: Python Script
```bash
python main.py
```

### Method 2: Shell Script
```bash
./generate_english_shorts.sh
```

## 📦 Output

All text in the video will be in English:

```
Title: "Seoul Real Estate Price Trend"
X-axis: "Month" (01, 02, 03, ...)
Y-axis: "Average Price ($100M KRW)"
Price tags: "$1.2B", "$1.5B", etc.

Voice: "Today's Seoul real estate hot deals!
       Number 1, Apartment Name, 199 square feet, $2K!
       Check them out now!"
```

## 🎨 Visual Output Example

```
┌─────────────────────────────────┐
│  Seoul Real Estate Price Trend  │  ← English title
├─────────────────────────────────┤
│                                 │
│         📈 Price Chart          │
│                                 │
│   $1.5B ●─────●                │  ← English price
│         │     │                 │
│   $1.2B ●─────●─────●          │
│         │     │     │           │
│         01    02    03          │  ← Month numbers
│              Month               │  ← English label
│                                 │
│  Average Price ($100M KRW)      │  ← English label
└─────────────────────────────────┘
```

## ✨ Benefits

1. **No Encoding Issues**: All English characters
2. **Global Audience**: International viewers can understand
3. **Clean Display**: No broken characters or boxes
4. **Consistent Fonts**: Arial/Helvetica work on all systems

## 🌍 For Global Shorts

To create fully international shorts with comparison:

```bash
# US comparison (English)
python generate_global_shorts.py --lang en --country US --theme comparison

# Output: "Seoul $450K vs New York $750K - 40% CHEAPER!"
```

## 📊 Generated Files

All in English:
- `output/price_trend.mp4` - Chart with English labels
- `output/narration.mp3` - English voice
- `output/shorts_1080x1920.mp4` - Final shorts (English only)

## ⚡ Currency Conversion

Automatic conversion in script:
- Korean Won → USD
- 1억원 (100M KRW) ≈ $75,000 USD
- 6억원 (600M KRW) ≈ $450,000 USD

Example:
```
Korean: "2.6억원"
English: "$195K" (2.6 × $75K)
```

## 🎤 Voice Script Format

```
Opening: "Today's Seoul real estate hot deals!"

Deals:
- "Number 1, [Apartment], [sqft] square feet, $[price]K!"
- "Number 2, [Apartment], [sqft] square feet, $[price]K!"
- "Number 3, [Apartment], [sqft] square feet, $[price]K!"

Closing: "Check them out now!"
```

## 🔧 No More Issues With

❌ Korean font not found
❌ Character encoding errors
❌ Broken text in videos
❌ Platform compatibility issues

✅ Clean English display
✅ Works on all systems
✅ Global audience ready
✅ Professional appearance

---

**Ready to create viral English shorts!** 🚀

```bash
python main.py
# Output: 100% English video ready for upload!
```
