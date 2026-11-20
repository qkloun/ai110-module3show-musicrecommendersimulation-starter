"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs      # python src/main.py


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints recommendations as a numbered list with scores and reasons."""
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print("\n" + "=" * 60)
    print(f"  Top {len(recommendations)} recommendations")
    print(f"  Profile: {profile}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}   ({song['genre']}, {song['mood']})")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print("\n" + "=" * 60 + "\n")


# Standard listener profiles
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop", "favorite_mood": "happy",
        "target_energy": 0.85, "target_valence": 0.80, "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi", "favorite_mood": "chill",
        "target_energy": 0.38, "target_valence": 0.60, "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock", "favorite_mood": "intense",
        "target_energy": 0.92, "target_valence": 0.45, "likes_acoustic": False,
    },
}

# Adversarial / edge-case profiles, designed to trick the scoring logic
EDGE_CASES = {
    "Conflict: high energy + sad mood": {
        "favorite_genre": "pop", "favorite_mood": "sad",
        "target_energy": 0.9, "target_valence": 0.1,
    },
    "Genre not in catalog (k-pop)": {
        "favorite_genre": "k-pop", "favorite_mood": "happy", "target_energy": 0.7,
    },
    "Capitalized labels (Pop / Happy)": {
        "favorite_genre": "Pop", "favorite_mood": "Happy", "target_energy": 0.8,
    },
    "Out-of-range energy (1.5)": {
        "favorite_genre": "lofi", "target_energy": 1.5,
    },
    "Acoustic but maximum energy": {
        "target_energy": 0.95, "likes_acoustic": True,
    },
    "Empty profile": {},
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in {**PROFILES, **EDGE_CASES}.items():
        print(f"\n### {name}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()