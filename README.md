# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

What each Song uses: genre, mood, energy (how intense it feels), valence (how happy or sad it feels), and acousticness (how acoustic or electronic it sounds). Tempo and danceability are stored but not used, because they rise and fall with energy and would count it twice.

What the UserProfile stores: the user’s favorite genre, favorite mood, the energy level they want, how upbeat they want songs to feel, and whether they like acoustic music.

How a song is scored: each song earns up to 5 points based on how well it fits the user.

- Energy: up to 2 points. The closer the song is to the user’s target, the more points it gets, so a calm listener isn’t - pushed toward the loudest song.
- Valence: up to 1 point, also based on closeness.
- Acoustic sound: up to 0.5 points if it matches the user’s preference.
- Genre: +1 point if it’s the user’s favorite.
- Mood: +0.5 points if it’s the user’s favorite.

How a song feels counts for more than its labels. That way, a great match from another genre can still be recommended.

How songs are chosen: every song is scored, then sorted from highest to lowest. Only one song per artist is kept, so the list has variety. The top five are recommended, each with a short reason, such as “close to your energy level” or “matches your favorite genre.”

### Real world system

Real-world services like Spotify and YouTube mostly combine two approaches. Collaborative filtering recommends what similar listeners enjoyed (“people who like X also like Y”). Content-based filtering recommends songs whose attributes resemble what you already like. They also learn from behavior such as skips, replays, and playlist adds. This simulation uses only content-based filtering, since it has a song catalog but no listening history. It prioritizes matching a song’s vibe, meaning how intense and how positive it feels, over matching labels. Genre and mood act as smaller bonuses, so a great match from another genre can still make the list.

### Features used

Song: energy (heaviest weight), valence, acousticness, genre, and mood. tempo_bpm and danceability are left out because in this dataset they move almost in lockstep with energy, so including them would count energy twice. artist is used only in ranking, to limit the list to one song per artist.

UserProfile: favorite_genre, favorite_mood, target_energy (0–1), likes_acoustic (true/false), and an optional target_valence (0–1).

### Algoriithm recipe

The recommender compares every song in the catalog to the user’s taste profile and gives it a score out of 5.0. Most points come from how closely the song’s feel (energy, valence, acousticness) matches what the user wants. Smaller bonuses go to songs in the user’s favorite genre or mood. The highest-scoring songs are recommended, with at most one per artist, and each comes with a short explanation of why it was picked.

### Expected biases and limitations

- Labels can still override the vibe.
- Genre and mood matching is all-or-nothing.
- The catalog is uneven.
- The data reflects my assumptions.
- Energy dominates.
- The artist cap can hide favorites.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Default profile: `{"genre": "pop", "mood": "happy", "energy": 0.8}`

```
Loaded 18 songs from data/songs.csv

============================================================
  Top 5 recommendations
  Profile: genre=pop, mood=happy, energy=0.8
============================================================

1. Sunrise City by Neon Echo
   Score: 3.46   (pop, happy)
   Why:
     - energy 0.82 is close to your target of 0.80
     - matches your favorite genre (pop)
     - matches your favorite mood (happy)

2. Gym Hero by Max Pulse
   Score: 2.74   (pop, intense)
   Why:
     - energy 0.93 is close to your target of 0.80
     - matches your favorite genre (pop)

3. Rooftop Lights by Indigo Parade
   Score: 2.42   (indie pop, happy)
   Why:
     - energy 0.76 is close to your target of 0.80
     - matches your favorite mood (happy)

4. Concrete Crown by Kilo Verse
   Score: 1.96   (hip-hop, confident)
   Why:
     - energy 0.78 is close to your target of 0.80

5. Barn Dance Fever by Copper Creek
   Score: 1.90   (bluegrass, energetic)
   Why:
     - energy 0.85 is close to your target of 0.80

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



