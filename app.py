import streamlit as st
import base64
import os
from datetime import datetime, timezone
from pathlib import Path

st.set_page_config(
    page_title="💕 For My Amori Momo 💕",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load images as base64 ---
@st.cache_data
def load_images():
    image_dir = Path(__file__).parent / "images"
    images = []
    for f in sorted(image_dir.glob("*.jpeg")):
        with open(f, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode()
            images.append(f"data:image/jpeg;base64,{b64}")
    return images

images = load_images()
images_js = ",\n".join([f'"{img}"' for img in images])

# Valentine's Day target: Feb 14, 2026 00:00:00 EST (UTC-5)
# We use UTC offset so JS countdown is accurate
VALENTINE_TARGET_ISO = "2025-01-01T00:00:00-05:00"  # TEMP: set to past date for testing. Change back to "2026-02-14T00:00:00-05:00" before sharing!

# Tobi's words of affirmation for Olamide + original placeholders
affirmations = [
    "Hey love, I know you're wondering what Tobi has in store for this website.. Well, it's just me embracing my luck in finding the one!",
    "My dearest! I love how you love me, and how you hold me when I'm sad. You're my good medicine on a bad day. A joyful personality to behold!",
    "Blessings were flying the day I met you. I would say I've been scared to love you, because I didn't know if I'd do it right.. But your patience, your smile, and your reassurance sets the space for me..",
    "People don't know about all the times you've put me first.. They don't know about all the days you've cried and I couldn't comfort you. Neither the days you've had to be strong for us..",
    "But I see you baby… I know how much you've sacrificed. I don't know what I did right to deserve you. But be rest assured that I'll be down to risk it all when it comes to you..",
    "I would admit that I've been in a bad shape romantically before I met you.. But you came in and taught me how to love properly.. You've dressed me up like a king, You've made me glow better..",
    "You should know that I've never been complemented by a stranger how good looking I am until you came into my life… You were the missing spice..the color to my sketchbook!",
    "I know what it feels like when the walls are closing in.. I know how much chaos we are in right now regarding stability here… But babe! Relax! We've got this!",
    "We might not have all the answers.. But I promise to always guide us through our darkest days.. Be there for us when it seems unsure.. This time, let me be there to help you chase your dreams.. And cuddle you in when it becomes overwhelming..",
    "One thing's certain. Even In wrong times and heavy tides, You'll always matter to me like the last piece of a birthday cake! Likewise always come first in every decision I make!",
    "In a game of chess, I'll take your love and leave the rest at stake. I know I picked the prettiest out of the roses.. And I'll fall over and over again to pick it again.",
    "Even without quantifiable words, I know you'll bear my last name.. As I hold your hands and love you for the rest of forever! 💕",
    "You are the most beautiful soul I have ever known, Olamide.",
    "Every moment with you feels like a blessing I never want to end.",
    "Your smile lights up my entire world, Aminat.",
    "I thank God every day for bringing you into my life on August 18, 2023.",
    "March 16, 2024 — the day you said yes — changed my life forever.",
    "You make me want to be the best version of myself.",
    "My Amori Momo, you are my peace, my joy, and my home.",
    "With you, every adventure becomes a cherished memory.",
    "Your love gives me strength I never knew I had.",
    "I love you more than words could ever express. Happy Valentine's Day, my love. 💕",
]

affirmations_js = ",\n".join([f'"{a}"' for a in affirmations])

# --- Build the full HTML/CSS/JS experience ---
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Great+Vibes&display=swap');

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body, html {{
    width: 100%;
    min-height: 100vh;
    overflow-x: hidden;
    font-family: 'Cormorant Garamond', serif;
    background: #0a0000;
    color: #fff;
  }}

  /* ============ COUNTDOWN / LOCKED SCREEN ============ */
  #countdown-screen {{
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at 30% 20%, #1a0008 0%, #0a0000 50%, #000 100%);
    transition: opacity 1.5s ease, transform 1.5s ease;
  }}

  #countdown-screen.hidden {{
    opacity: 0;
    transform: scale(1.1);
    pointer-events: none;
  }}

  .countdown-lock-icon {{
    font-size: 48px;
    margin-bottom: 20px;
    animation: pulse-glow 2s ease-in-out infinite;
  }}

  @keyframes pulse-glow {{
    0%, 100% {{ filter: drop-shadow(0 0 10px rgba(255,80,120,0.4)); transform: scale(1); }}
    50% {{ filter: drop-shadow(0 0 25px rgba(255,80,120,0.8)); transform: scale(1.05); }}
  }}

  .countdown-title {{
    font-family: 'Great Vibes', cursive;
    font-size: clamp(2.5rem, 6vw, 5rem);
    color: #ff5078;
    text-shadow: 0 0 40px rgba(255,80,120,0.3);
    margin-bottom: 10px;
    text-align: center;
  }}

  .countdown-subtitle {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 2.5vw, 1.4rem);
    color: rgba(255,200,210,0.7);
    font-style: italic;
    margin-bottom: 50px;
    text-align: center;
    letter-spacing: 2px;
  }}

  .countdown-timer {{
    display: flex;
    gap: clamp(15px, 4vw, 40px);
    margin-bottom: 50px;
  }}

  .countdown-unit {{
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .countdown-number {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 7vw, 5.5rem);
    font-weight: 900;
    background: linear-gradient(135deg, #ff5078, #ff8fa3, #ffb3c1, #ff5078);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 4s ease-in-out infinite;
    line-height: 1;
  }}

  @keyframes gradient-shift {{
    0%, 100% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
  }}

  .countdown-label {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(0.7rem, 1.5vw, 1rem);
    color: rgba(255,180,193,0.6);
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 8px;
  }}

  .countdown-separator {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 4rem);
    color: rgba(255,80,120,0.3);
    align-self: flex-start;
    margin-top: 5px;
  }}

  .countdown-message {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 2vw, 1.3rem);
    color: rgba(255,200,210,0.5);
    font-style: italic;
    text-align: center;
    max-width: 500px;
    line-height: 1.6;
  }}

  /* Floating hearts on countdown */
  .bg-heart {{
    position: fixed;
    color: rgba(255,80,120,0.08);
    font-size: 30px;
    animation: float-up linear infinite;
    pointer-events: none;
    z-index: 999;
  }}

  @keyframes float-up {{
    0% {{ transform: translateY(100vh) rotate(0deg); opacity: 0; }}
    10% {{ opacity: 1; }}
    90% {{ opacity: 1; }}
    100% {{ transform: translateY(-10vh) rotate(360deg); opacity: 0; }}
  }}

  /* ============ CELEBRATION EXPLOSION ============ */
  #celebration-overlay {{
    position: fixed;
    inset: 0;
    z-index: 2000;
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: radial-gradient(circle at center, #1a0008, #0a0000);
    opacity: 0;
    transition: opacity 0.5s ease;
  }}

  #celebration-overlay.active {{
    display: flex;
    opacity: 1;
  }}

  .celebration-text {{
    font-family: 'Great Vibes', cursive;
    font-size: clamp(3rem, 8vw, 7rem);
    background: linear-gradient(135deg, #ff5078, #ff8fa3, #ffd1dc, #ff5078);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 3s ease-in-out infinite, celebration-entrance 1s ease-out;
    text-align: center;
    z-index: 2001;
  }}

  .celebration-sub {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.2rem, 3vw, 2rem);
    color: rgba(255,200,210,0.8);
    margin-top: 15px;
    font-style: italic;
    animation: celebration-entrance 1s ease-out 0.3s both;
    text-align: center;
    z-index: 2001;
  }}

  .celebration-enter-btn {{
    margin-top: 40px;
    padding: 16px 50px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #fff;
    background: linear-gradient(135deg, #ff5078, #c9184a);
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: celebration-entrance 1s ease-out 0.6s both;
    z-index: 2001;
  }}

  .celebration-enter-btn:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(255,80,120,0.5);
  }}

  @keyframes celebration-entrance {{
    0% {{ opacity: 0; transform: translateY(30px) scale(0.9); }}
    100% {{ opacity: 1; transform: translateY(0) scale(1); }}
  }}

  /* Confetti / Hearts explosion */
  .confetti-piece {{
    position: fixed;
    z-index: 2002;
    pointer-events: none;
    animation: confetti-fall linear forwards;
  }}

  @keyframes confetti-fall {{
    0% {{ transform: translateY(-10vh) rotate(0deg) scale(0); opacity: 1; }}
    20% {{ transform: translateY(15vh) rotate(180deg) scale(1); opacity: 1; }}
    100% {{ transform: translateY(110vh) rotate(720deg) scale(0.5); opacity: 0; }}
  }}

  /* ============ MAIN CONTENT ============ */
  #main-content {{
    display: none;
    opacity: 0;
    transition: opacity 1.5s ease;
  }}

  #main-content.visible {{
    display: block;
    opacity: 1;
  }}

  /* Hero Section */
  .hero {{
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 20px;
    background: radial-gradient(ellipse at 50% 30%, #1a0008 0%, #0a0000 60%, #000 100%);
    position: relative;
    overflow: hidden;
  }}

  .hero::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: 
      radial-gradient(circle at 20% 80%, rgba(255,80,120,0.06) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(255,140,160,0.04) 0%, transparent 50%);
    pointer-events: none;
  }}

  .hero-name {{
    font-family: 'Great Vibes', cursive;
    font-size: clamp(3.5rem, 9vw, 8rem);
    background: linear-gradient(135deg, #ff5078, #ff8fa3, #ffd1dc, #ffb3c1);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 5s ease-in-out infinite, hero-entrance 1.5s ease-out;
    line-height: 1.2;
    z-index: 1;
  }}

  .hero-tagline {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.1rem, 2.5vw, 1.8rem);
    color: rgba(255,180,193,0.7);
    font-style: italic;
    margin-top: 15px;
    letter-spacing: 2px;
    animation: hero-entrance 1.5s ease-out 0.3s both;
    z-index: 1;
  }}

  .hero-date {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.9rem, 1.5vw, 1.1rem);
    color: rgba(255,140,160,0.4);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 25px;
    animation: hero-entrance 1.5s ease-out 0.6s both;
    z-index: 1;
  }}

  @keyframes hero-entrance {{
    0% {{ opacity: 0; transform: translateY(40px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
  }}

  .scroll-indicator {{
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    animation: bounce 2s ease-in-out infinite;
    z-index: 1;
  }}

  .scroll-indicator span {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.8rem;
    color: rgba(255,180,193,0.4);
    letter-spacing: 3px;
    text-transform: uppercase;
  }}

  .scroll-arrow {{
    width: 20px;
    height: 20px;
    border-right: 2px solid rgba(255,80,120,0.4);
    border-bottom: 2px solid rgba(255,80,120,0.4);
    transform: rotate(45deg);
  }}

  @keyframes bounce {{
    0%, 100% {{ transform: translateX(-50%) translateY(0); }}
    50% {{ transform: translateX(-50%) translateY(10px); }}
  }}

  /* ============ PHOTO SLIDESHOW SECTION ============ */
  .slideshow-section {{
    min-height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px 20px 10px 20px;
    background: linear-gradient(180deg, #0a0000 0%, #120005 50%, #0a0000 100%);
    position: relative;
  }}

  .slideshow-heading {{
    font-family: 'Great Vibes', cursive;
    font-size: clamp(2rem, 5vw, 3.5rem);
    color: #ff5078;
    text-shadow: 0 0 30px rgba(255,80,120,0.2);
    margin-bottom: 25px;
    text-align: center;
  }}

  .slideshow-container {{
    position: relative;
    width: min(85vw, 650px);
    aspect-ratio: 4/5;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 
      0 0 60px rgba(255,80,120,0.15),
      0 20px 60px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,80,120,0.15);
  }}

  .slide {{
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 1.5s ease-in-out;
  }}

  .slide.active {{
    opacity: 1;
  }}

  .slide img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  /* Navigation dots */
  .slide-dots {{
    display: flex;
    gap: 10px;
    margin-top: 25px;
    justify-content: center;
    flex-wrap: wrap;
  }}

  .slide-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,80,120,0.2);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,80,120,0.3);
  }}

  .slide-dot.active {{
    background: #ff5078;
    box-shadow: 0 0 12px rgba(255,80,120,0.6);
    transform: scale(1.2);
  }}

  /* Navigation arrows */
  .slide-nav {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(255,80,120,0.2);
    color: #ff8fa3;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 18px;
    transition: all 0.3s ease;
    z-index: 10;
    backdrop-filter: blur(8px);
  }}

  .slide-nav:hover {{
    background: rgba(255,80,120,0.3);
    box-shadow: 0 0 20px rgba(255,80,120,0.3);
  }}

  .slide-nav.prev {{ left: 12px; }}
  .slide-nav.next {{ right: 12px; }}

  /* ============ AFFIRMATIONS SECTION ============ */
  .affirmations-section {{
    min-height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px 20px 40px 20px;
    background: radial-gradient(ellipse at 50% 50%, #1a0008 0%, #0a0000 70%);
    position: relative;
  }}

  .affirmation-card {{
    max-width: 700px;
    text-align: center;
    padding: 20px 30px;
    position: relative;
  }}

  .affirmation-quote {{
    font-size: 50px;
    color: rgba(255,80,120,0.3);
    font-family: 'Playfair Display', serif;
    line-height: 1;
    margin-bottom: -10px;
  }}

  .affirmation-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.4rem, 3vw, 2.2rem);
    color: rgba(255,220,225,0.9);
    font-style: italic;
    line-height: 1.7;
    font-weight: 300;
    transition: opacity 1s ease, transform 1s ease;
  }}

  .affirmation-number {{
    font-family: 'Playfair Display', serif;
    font-size: 0.9rem;
    color: rgba(255,80,120,0.4);
    letter-spacing: 3px;
    margin-top: 30px;
  }}

  .affirmation-nav {{
    display: flex;
    gap: 20px;
    margin-top: 40px;
  }}

  .affirmation-btn {{
    padding: 12px 30px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ff8fa3;
    background: transparent;
    border: 1px solid rgba(255,80,120,0.3);
    border-radius: 30px;
    cursor: pointer;
    transition: all 0.3s ease;
  }}

  .affirmation-btn:hover {{
    background: rgba(255,80,120,0.15);
    border-color: #ff5078;
    box-shadow: 0 0 20px rgba(255,80,120,0.2);
  }}

  /* ============ FOOTER / LOVE NOTE ============ */
  .footer-section {{
    padding: 40px 20px;
    text-align: center;
    background: linear-gradient(180deg, #0a0000 0%, #0d0002 100%);
  }}

  .footer-heart {{
    font-size: 40px;
    animation: pulse-glow 2s ease-in-out infinite;
    margin-bottom: 20px;
  }}

  .footer-text {{
    font-family: 'Great Vibes', cursive;
    font-size: clamp(1.8rem, 4vw, 3rem);
    color: #ff5078;
    margin-bottom: 10px;
  }}

  .footer-sub {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: rgba(255,180,193,0.5);
    font-style: italic;
  }}

  .footer-date {{
    font-family: 'Playfair Display', serif;
    font-size: 0.85rem;
    color: rgba(255,80,120,0.3);
    letter-spacing: 4px;
    margin-top: 20px;
  }}

  /* ============ MUSIC PLAYER ============ */
  .music-toggle {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(255,80,120,0.2);
    border: 1px solid rgba(255,80,120,0.3);
    color: #ff8fa3;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 5000;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    display: none;
  }}

  .music-toggle.show {{
    display: flex;
  }}

  .music-toggle:hover {{
    background: rgba(255,80,120,0.4);
    box-shadow: 0 0 20px rgba(255,80,120,0.3);
  }}

  .music-toggle .bars {{
    display: flex;
    gap: 2px;
    align-items: flex-end;
    height: 18px;
  }}

  .music-toggle .bar {{
    width: 3px;
    background: #ff8fa3;
    border-radius: 2px;
    animation: none;
  }}

  .music-toggle.playing .bar {{
    animation: eq-bar 0.8s ease-in-out infinite alternate;
  }}

  .music-toggle.playing .bar:nth-child(1) {{ height: 6px; animation-delay: 0s; }}
  .music-toggle.playing .bar:nth-child(2) {{ height: 12px; animation-delay: 0.15s; }}
  .music-toggle.playing .bar:nth-child(3) {{ height: 8px; animation-delay: 0.3s; }}
  .music-toggle.playing .bar:nth-child(4) {{ height: 14px; animation-delay: 0.1s; }}

  @keyframes eq-bar {{
    0% {{ height: 4px; }}
    100% {{ height: 18px; }}
  }}

</style>
</head>
<body>

<!-- ====== COUNTDOWN SCREEN ====== -->
<div id="countdown-screen">
  <div class="countdown-lock-icon">🔒</div>
  <div class="countdown-title">Something Special Awaits...</div>
  <div class="countdown-subtitle">A Valentine's surprise for Olamide</div>
  
  <div class="countdown-timer">
    <div class="countdown-unit">
      <div class="countdown-number" id="cd-days">00</div>
      <div class="countdown-label">Days</div>
    </div>
    <div class="countdown-separator">:</div>
    <div class="countdown-unit">
      <div class="countdown-number" id="cd-hours">00</div>
      <div class="countdown-label">Hours</div>
    </div>
    <div class="countdown-separator">:</div>
    <div class="countdown-unit">
      <div class="countdown-number" id="cd-mins">00</div>
      <div class="countdown-label">Minutes</div>
    </div>
    <div class="countdown-separator">:</div>
    <div class="countdown-unit">
      <div class="countdown-number" id="cd-secs">00</div>
      <div class="countdown-label">Seconds</div>
    </div>
  </div>

  <div class="countdown-message">
    Patience, my love... the best things are worth waiting for. 💕
  </div>
</div>

<!-- ====== CELEBRATION OVERLAY ====== -->
<div id="celebration-overlay">
  <div class="celebration-text">Happy Valentine's Day!</div>
  <div class="celebration-sub">My Dearest Amori Momo 💕</div>
  <button class="celebration-enter-btn" onclick="enterExperience()">Open Your Gift</button>
</div>

<!-- ====== MAIN CONTENT (hidden until unlocked) ====== -->
<div id="main-content">
  
  <!-- Hero -->
  <section class="hero">
    <div class="hero-name">Olamide</div>
    <div class="hero-tagline">My Amori Momo — My Everything</div>
    <div class="hero-date">Valentine's Day 2026</div>
    <div class="scroll-indicator">
      <span>Scroll</span>
      <div class="scroll-arrow"></div>
    </div>
  </section>

  <!-- Slideshow -->
  <section class="slideshow-section">
    <div class="slideshow-heading">Our Beautiful Moments</div>
    <div class="slideshow-container" id="slideshow">
      <!-- Slides injected by JS -->
      <div class="slide-nav prev" onclick="prevSlide()">&#10094;</div>
      <div class="slide-nav next" onclick="nextSlide()">&#10095;</div>
    </div>
    <div class="slide-dots" id="slide-dots"></div>
  </section>

  <!-- Affirmations -->
  <section class="affirmations-section">
    <div class="slideshow-heading">Words From My Heart</div>
    <div class="affirmation-card">
      <div class="affirmation-quote">&ldquo;</div>
      <div class="affirmation-text" id="affirmation-text"></div>
      <div class="affirmation-number" id="affirmation-number"></div>
      <div class="affirmation-nav">
        <button class="affirmation-btn" onclick="prevAffirmation()">&#10094; Prev</button>
        <button class="affirmation-btn" onclick="nextAffirmation()">Next &#10095;</button>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <section class="footer-section">
    <div class="footer-heart">💕</div>
    <div class="footer-text">Forever Yours, Tobi</div>
    <div class="footer-sub">From the day I first saw you — August 18, 2023</div>
    <div class="footer-date">HAPPY VALENTINE'S DAY 2026</div>
  </section>

</div>

<!-- Music toggle -->
<button class="music-toggle" id="music-toggle" onclick="toggleMusic()">
  <div class="bars">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
  </div>
</button>

<script>
  // ===== IMAGE DATA =====
  const images = [
    {images_js}
  ];

  // ===== AFFIRMATIONS =====
  const affirmations = [
    {affirmations_js}
  ];

  // ===== COUNTDOWN =====
  const targetDate = new Date("{VALENTINE_TARGET_ISO}");
  let countdownDone = false;

  function updateCountdown() {{
    const now = new Date();
    const diff = targetDate - now;

    if (diff <= 0) {{
      if (!countdownDone) {{
        countdownDone = true;
        triggerCelebration();
      }}
      return;
    }}

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const mins = Math.floor((diff / (1000 * 60)) % 60);
    const secs = Math.floor((diff / 1000) % 60);

    document.getElementById('cd-days').textContent = String(days).padStart(2, '0');
    document.getElementById('cd-hours').textContent = String(hours).padStart(2, '0');
    document.getElementById('cd-mins').textContent = String(mins).padStart(2, '0');
    document.getElementById('cd-secs').textContent = String(secs).padStart(2, '0');
  }}

  // Create floating hearts on countdown
  function createBgHearts() {{
    const hearts = ['💕', '❤️', '💗', '💖', '🤍', '💘'];
    for (let i = 0; i < 15; i++) {{
      const heart = document.createElement('div');
      heart.className = 'bg-heart';
      heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
      heart.style.left = Math.random() * 100 + '%';
      heart.style.animationDuration = (8 + Math.random() * 12) + 's';
      heart.style.animationDelay = (Math.random() * 10) + 's';
      heart.style.fontSize = (15 + Math.random() * 25) + 'px';
      document.getElementById('countdown-screen').appendChild(heart);
    }}
  }}

  // ===== CELEBRATION =====
  function triggerCelebration() {{
    const overlay = document.getElementById('celebration-overlay');
    const countdown = document.getElementById('countdown-screen');
    
    countdown.classList.add('hidden');
    
    setTimeout(() => {{
      overlay.classList.add('active');
      launchConfetti();
    }}, 1500);
  }}

  function launchConfetti() {{
    const hearts = ['💕', '❤️', '💗', '💖', '🤍', '💘', '✨', '🌹', '💝', '💓'];
    const overlay = document.getElementById('celebration-overlay');
    
    for (let i = 0; i < 60; i++) {{
      setTimeout(() => {{
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';
        piece.textContent = hearts[Math.floor(Math.random() * hearts.length)];
        piece.style.left = Math.random() * 100 + '%';
        piece.style.fontSize = (16 + Math.random() * 28) + 'px';
        piece.style.animationDuration = (3 + Math.random() * 3) + 's';
        overlay.appendChild(piece);
        
        setTimeout(() => piece.remove(), 6000);
      }}, i * 80);
    }}
  }}

  function enterExperience() {{
    const overlay = document.getElementById('celebration-overlay');
    const main = document.getElementById('main-content');
    const musicBtn = document.getElementById('music-toggle');
    
    overlay.style.opacity = '0';
    setTimeout(() => {{
      overlay.style.display = 'none';
      main.classList.add('visible');
      musicBtn.classList.add('show');
      initSlideshow();
      initAffirmations();
    }}, 800);
  }}

  // ===== SLIDESHOW =====
  let currentSlide = 0;
  let slideInterval;

  function initSlideshow() {{
    const container = document.getElementById('slideshow');
    const dotsContainer = document.getElementById('slide-dots');

    images.forEach((src, i) => {{
      const slide = document.createElement('div');
      slide.className = 'slide' + (i === 0 ? ' active' : '');
      slide.innerHTML = `<img src="${{src}}" alt="Memory ${{i+1}}">`;
      container.insertBefore(slide, container.querySelector('.slide-nav'));

      const dot = document.createElement('div');
      dot.className = 'slide-dot' + (i === 0 ? ' active' : '');
      dot.onclick = () => goToSlide(i);
      dotsContainer.appendChild(dot);
    }});

    slideInterval = setInterval(nextSlide, 5000);
  }}

  function goToSlide(index) {{
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.slide-dot');
    
    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');
    
    currentSlide = index;
    
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');

    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000);
  }}

  function nextSlide() {{
    goToSlide((currentSlide + 1) % images.length);
  }}

  function prevSlide() {{
    goToSlide((currentSlide - 1 + images.length) % images.length);
  }}

  // ===== AFFIRMATIONS =====
  let currentAffirmation = 0;

  function initAffirmations() {{
    showAffirmation(0);
  }}

  function showAffirmation(index) {{
    const textEl = document.getElementById('affirmation-text');
    const numEl = document.getElementById('affirmation-number');
    
    textEl.style.opacity = '0';
    textEl.style.transform = 'translateY(15px)';
    
    setTimeout(() => {{
      textEl.textContent = affirmations[index];
      numEl.textContent = `${{index + 1}} / ${{affirmations.length}}`;
      textEl.style.opacity = '1';
      textEl.style.transform = 'translateY(0)';
    }}, 400);
  }}

  function nextAffirmation() {{
    currentAffirmation = (currentAffirmation + 1) % affirmations.length;
    showAffirmation(currentAffirmation);
  }}

  function prevAffirmation() {{
    currentAffirmation = (currentAffirmation - 1 + affirmations.length) % affirmations.length;
    showAffirmation(currentAffirmation);
  }}

  // ===== MUSIC (placeholder) =====
  let musicPlaying = false;

  function toggleMusic() {{
    const btn = document.getElementById('music-toggle');
    musicPlaying = !musicPlaying;
    btn.classList.toggle('playing', musicPlaying);
    // Audio integration can be added here
  }}

  // ===== INIT =====
  createBgHearts();
  updateCountdown();
  setInterval(updateCountdown, 1000);

</script>
</body>
</html>
"""

# --- Render in Streamlit ---
# Hide Streamlit's default UI for a clean experience
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {background: #0a0000;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    [data-testid="stAppViewContainer"] {background: #0a0000;}
    iframe {border: none !important;}
</style>
""", unsafe_allow_html=True)

st.components.v1.html(html_content, height=1800, scrolling=True)
