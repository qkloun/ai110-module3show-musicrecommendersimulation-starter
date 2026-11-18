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

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.
    Numeric columns are converted so they can be used in math later.
    Required by src/main.py
    """
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
    """Reads a preference by its full name, falling back to the short name main.py uses."""
    return user_prefs.get(key, user_prefs.get(short_key))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences (maximum 5.0 points).
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Energy closeness: up to 2.0 points
    target_energy = _pref(user_prefs, "target_energy", "energy")
    if target_energy is not None:
        closeness = 1 - abs(song["energy"] - target_energy)
        score += 2.0 * closeness
        if closeness >= 0.85:
            reasons.append(f"energy {song['energy']:.2f} is close to your target of {target_energy:.2f}")

    # Valence closeness: up to 1.0 point
    target_valence = _pref(user_prefs, "target_valence", "valence")
    if target_valence is not None:
        closeness = 1 - abs(song["valence"] - target_valence)
        score += 1.0 * closeness
        if closeness >= 0.85:
            reasons.append("its mood level (valence) fits what you want")

    # Acoustic fit: up to 0.5 points
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        fit = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]
        score += 0.5 * fit
        if fit >= 0.7:
            reasons.append("it has the acoustic sound you like" if likes_acoustic
                           else "it has the electronic sound you like")

    # Genre match: +1.0
    if song["genre"] == _pref(user_prefs, "favorite_genre", "genre"):
        score += 1.0
        reasons.append(f"matches your favorite genre ({song['genre']})")

    # Mood match: +0.5
    if song["mood"] == _pref(user_prefs, "favorite_mood", "mood"):
        score += 0.5
        reasons.append(f"matches your favorite mood ({song['mood']})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
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