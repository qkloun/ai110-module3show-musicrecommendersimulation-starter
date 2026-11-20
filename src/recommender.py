import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# Scoring weights (Algorithm Recipe)
BASELINE_WEIGHTS = {"energy": 2.0, "valence": 1.0, "acoustic": 0.5, "genre": 1.0, "mood": 0.5}

# Experiment: Weight Shift. Energy doubled (2.0 -> 4.0), genre halved (1.0 -> 0.5).
# Set USE_WEIGHT_SHIFT = False to go back to the baseline recipe.
USE_WEIGHT_SHIFT = True
WEIGHT_SHIFT = {**BASELINE_WEIGHTS, "energy": 4.0, "genre": 0.5}

WEIGHTS = WEIGHT_SHIFT if USE_WEIGHT_SHIFT else BASELINE_WEIGHTS


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dictionaries, converting numeric columns to int/float."""
    int_fields = ["id"]
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # row 1 is the header
            song = {key: value.strip() for key, value in row.items()}
            try:
                for field in int_fields:
                    song[field] = int(song[field])
                for field in float_fields:
                    song[field] = float(song[field])
            except (KeyError, ValueError, TypeError) as e:
                raise ValueError(f"Bad value in {csv_path}, row {row_num}: {e}") from None
            songs.append(song)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def _pref(user_prefs: Dict, key: str, short_key: str):
    """Return a preference by its full key (e.g. favorite_genre), falling back to its short key (e.g. genre)."""
    return user_prefs.get(key, user_prefs.get(short_key))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences (max 6.5 with the weight shift, 5.0 baseline) and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Energy closeness: up to WEIGHTS["energy"] points
    target_energy = _pref(user_prefs, "target_energy", "energy")
    if target_energy is not None:
        closeness = 1 - abs(song["energy"] - target_energy)
        score += WEIGHTS["energy"] * closeness
        if closeness >= 0.85:
            reasons.append(f"energy {song['energy']:.2f} is close to your target of {target_energy:.2f}")

    # Valence closeness: up to WEIGHTS["valence"] points
    target_valence = _pref(user_prefs, "target_valence", "valence")
    if target_valence is not None:
        closeness = 1 - abs(song["valence"] - target_valence)
        score += WEIGHTS["valence"] * closeness
        if closeness >= 0.85:
            reasons.append("its mood level (valence) fits what you want")

    # Acoustic fit: up to WEIGHTS["acoustic"] points
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        fit = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]
        score += WEIGHTS["acoustic"] * fit
        if fit >= 0.7:
            reasons.append("it has the acoustic sound you like" if likes_acoustic
                           else "it has the electronic sound you like")

    # Genre match: +WEIGHTS["genre"]
    if song["genre"] == _pref(user_prefs, "favorite_genre", "genre"):
        score += WEIGHTS["genre"]
        reasons.append(f"matches your favorite genre ({song['genre']})")

    # Mood match: +WEIGHTS["mood"]
    if song["mood"] == _pref(user_prefs, "favorite_mood", "mood"):
        score += WEIGHTS["mood"]
        reasons.append(f"matches your favorite mood ({song['mood']})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank highest first with one song per artist, and return the top k."""
    target_energy = _pref(user_prefs, "target_energy", "energy") or 0.5

    # 1. Judge every song: build (song, score, reasons) for the whole catalog
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # 2. Rank: highest score first; ties go to the song closer to the target energy
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy)),
    )

    # 3. Keep one song per artist, stopping once we have k
    results = []
    seen_artists = set()
    for song, score, reasons in ranked:
        if song["artist"] in seen_artists:
            continue
        seen_artists.add(song["artist"])
        explanation = "; ".join(reasons) if reasons else "closest overall match to your profile"
        results.append((song, score, explanation))
        if len(results) == k:
            break

    return results