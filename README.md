# 💕 Valentine's Day App for Olamide

A beautiful, interactive Valentine's Day web experience built with Streamlit.

## Features
- **Countdown Timer** — Content stays locked until Valentine's Day (Feb 14, 2026 midnight EST)
- **Celebration Explosion** — Hearts & confetti burst when the countdown hits zero
- **Photo Slideshow** — 16 beautiful photos with smooth fade transitions
- **Words of Affirmation** — Personal messages displayed one-by-one
- **Floating Hearts Animation** — Ambient romantic atmosphere
- **Music Toggle** — Ready for background music integration
- **Fully Responsive** — Looks great on mobile and desktop

## How to Run Locally

```bash
cd valentine_app
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file path to `app.py`
5. Click **Deploy**

Make sure the `images/` folder with all 16 photos is included in the repo.

## Customization

### Update Words of Affirmation
Edit the `affirmations` list in `app.py` (around line 40).

### Add Background Music
To add music, you can embed an audio element in the HTML or use a hosted MP3 URL.

### Change Valentine's Day Target
Edit `VALENTINE_TARGET_ISO` in `app.py` to change the countdown target.

---
*Made with love by Tobi for Olamide 💕*
