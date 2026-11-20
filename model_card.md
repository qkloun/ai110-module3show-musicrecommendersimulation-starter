# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

**Goal:** VibeFinder suggests 5 songs that match a listener's taste. It predicts which songs from a small catalog will feel right to the listener, based on the energy, mood, and style they ask for.

**Intended use:** This is a classroom project for learning how recommender systems work. It's meant for testing ideas, comparing user profiles, and spotting bias.

**Not intended for:** real listeners or real music apps. The catalog is tiny and made up, and the system knows nothing about lyrics, artists, or listening history. It also assumes each user can describe their taste with a few numbers and labels, which real people usually can't.

---

## 3. How the Model Works  

Each song gets a score out of 5 points based on how well it fits the listener.

- **Energy** (up to 2 points): songs closer to the energy level the listener wants get more points.
- **Happiness of the sound** (up to 1 point): songs closer to how upbeat or dark the listener wants get more points.
- **Acoustic sound** (up to 0.5 points): points for sounding acoustic or electronic, whichever the listener prefers.
- **Genre** (1 point): a bonus if the song is the listener's favorite genre.
- **Mood** (0.5 points): a bonus if the song has the listener's favorite mood.

The songs are sorted from highest to lowest score. Only one song per artist is allowed, and the top 5 are recommended. Each song comes with a short list of reasons, such as "matches your favorite genre."

**Changes from the starter logic:** I added happiness of the sound and acoustic preference, rewarded songs for being *close* to a target instead of just high or low, and added the one-song-per-artist rule.

---

## 4. Data  

- **18 songs:** the 10 starter songs, plus 8 I added.
- **15 genres**, including pop, lofi, rock, jazz, hip-hop, classical, metal, and country. Most genres have only one song.
- **14 moods**, such as happy, chill, intense, and melancholic.
- **Features used:** genre, mood, energy, how happy the song sounds (valence), and acousticness. Tempo and danceability are in the file but not used, because they mostly repeat energy.

**Limits:** The catalog is very small, and I made up the numbers for the added songs. It leans toward upbeat and energetic music. It has no lyrics, no release year, and no information about whether a song has vocals.

---

## 5. Strengths  

- It works well for listeners with clear, consistent tastes. The pop, lofi, and rock profiles all got a near-perfect #1 song.
- It clearly separates very different listeners. A calm lofi fan and an intense rock fan got completely different lists.
- Happiness of the sound helps a lot. Two listeners who both want high energy still get different lists if one wants upbeat songs and the other wants dark ones.
- Every recommendation explains itself, so it's easy to see why a song was picked.

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

- **Smarter matching for labels.** Give partial credit for similar words, like "sad" and "melancholic" or "pop" and "indie pop."
- **Admit when there's no good match.** Show a warning when even the best song scores low, instead of presenting a confident top 5.
- **A bigger, more balanced catalog.** Add more sad, very calm, and mid-energy songs, plus more than one song per genre.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps


**Biggest learning moment:** The stress test. My recommender worked well for normal profiles, so I thought it was done. Then a "sad but energetic" listener got Sunrise City, one of the happiest songs, at #2. That showed me a system can look correct on easy cases and still fail on harder ones. I only found the problem because I tested profiles that were designed to break it.

The stress test was the hardest part of the project, as it worked really well for almost all of my profiles so I thought it would do well for the test however when a "sad" profile got one of the happiest songs I had to figure out how to fix this issue.
 
**How AI tools helped, and when I double-checked:** AI helped me plan the scoring rules, write the code, and come up with edge cases I wouldn't have thought of. But I couldn't trust everything it gave me. Some of the code it wrote had a small bug: when breaking ties, a target energy of 0.0 was treated as if the user had given no target. The 8 songs it generated came with its own assumptions, like "metal is angry." When I changed the weights, the README still described the old ones. I learned to run the code myself, compare the output with what I expected, and read the reasons for each song instead of just looking at the top result.
 
**What surprised me:** I was surprised to find out how difficult making a reccomender algorithm really is. It made me think about how complex real reccomendation algorithms are in big companies. 
 
**What I'd try next:** I'd give partial credit for similar labels, like "sad" and "melancholic." I'd also add a warning when no song is a good match. Finally, I'd try adding real listening behavior, like skips and replays, to see how much better the recommendations get compared to features alone.