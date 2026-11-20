# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The system underserves listeners who want sad or very calm music, because the catalog leans upbeat and energetic. Only 3 of the 18 songs have a valence below 0.48, and no song has an energy below 0.22, so a user who asks for dark, quiet music has very few close matches. The catalog also has no mood labeled "sad" (the closest is "melancholic"), and exact-match scoring gives no credit for similar words. In testing, this let the pop genre bonus place Sunrise City, one of the happiest songs, at #2 for a user who wanted sad high-energy music. Because energy carries the most weight, users whose tastes fall in thinly covered ranges, such as energy 0.55–0.75, where the catalog has no songs, consistently get weaker recommendations than users near the crowded middle or the high-energy end.

---

## 7. Evaluation  

### Profiles tested

I ran four user profiles against the 18-song catalog with the baseline weights and looked at each top 5:

| Profile | Genre / Mood | Energy | Valence | Likes acoustic | Top 5 |
|---|---|---|---|---|---|
| High-Energy Pop | pop / happy | 0.85 | 0.80 | No | Sunrise City, Gym Hero, Rooftop Lights, Concrete Crown, Barn Dance Fever |
| Chill Lofi | lofi / chill | 0.38 | 0.60 | Yes | Library Rain, Midnight Coding, Spacewalk Thoughts, Coffee Shop Stories, Slow Burn |
| Deep Intense Rock | rock / intense | 0.92 | 0.45 | No | Storm Runner, Gym Hero, Afterhours, Iron Tide, Concrete Crown |
| Conflict: high energy + sad | pop / sad | 0.90 | 0.10 | (not set) | Gym Hero, Sunrise City, Afterhours, Iron Tide, Storm Runner |

For each profile, I checked whether the #1 song matched every preference, whether the rest of the list fit the requested energy and mood, and whether each song's printed reasons made sense.

### Comparing the profiles

**High-Energy Pop vs. Chill Lofi:** The two lists share no songs. The pop list is fast, upbeat, and electronic, while the lofi list is quiet and acoustic. This makes sense because the profiles disagree on almost everything: energy (0.85 vs. 0.38), acoustic preference, genre, and mood.

**High-Energy Pop vs. Deep Intense Rock:** Both want high-energy electronic music, so they share Gym Hero and Concrete Crown. Valence is what separates them. The pop profile (0.80) gets upbeat songs like Sunrise City and Rooftop Lights, while the rock profile (0.45) gets darker songs like Afterhours and Iron Tide. This shows that valence is doing its job: two listeners with the same energy level still get different-feeling lists.

**Chill Lofi vs. Deep Intense Rock:** The lists share no songs, and they sit at opposite ends of both energy and acousticness. Each profile's #1 song scored almost perfectly (4.87 and 4.90), so the system serves both a calm listener and an intense listener equally well when the catalog has a song that fits.

**High-Energy Pop vs. Conflict (high energy + sad):** Both profiles like pop and high energy, but the conflict profile wants very low valence (0.10). Rooftop Lights drops out because the "happy" mood no longer matches. Sunrise City falls from #1 to #2, yet it stays on the list even though it's one of the happiest songs in the catalog. The pop genre bonus is strong enough to outweigh the valence mismatch, which does not make sense for a sad listener.

**Chill Lofi vs. Conflict (high energy + sad):** The lists share no songs. The conflict profile asks for high energy, while the lofi profile asks for calm, so the result is expected. It also shows that low valence alone does not pull in quiet songs, because energy carries more weight.

**Deep Intense Rock vs. Conflict (high energy + sad):** The lists share four songs: Gym Hero, Afterhours, Iron Tide, and Storm Runner. High energy plus low valence describes dark, intense music, so the conflict profile behaves almost like the rock profile. That's a reasonable answer for a "sad but energetic" listener. Storm Runner drops from #1 to #5 because it loses its rock genre and intense mood bonuses.

### Weight Shift experiment

I also re-ran the profiles with energy doubled (2.0 to 4.0) and genre halved (1.0 to 0.5). The Chill Lofi and Deep Intense Rock lists stayed the same, and High-Energy Pop only swapped #4 and #5. The conflict profile changed the most. Afterhours, a dark song, moved to #1, and Sunrise City dropped to #5. This change made the conflicting profile more accurate, but it made genre almost irrelevant for everyone else.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps