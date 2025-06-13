# Vibelink
A modular music recommendation system that lets users create and customize their own “vibes” (personalized recommendation algorithms) rather than relying on a black-box.

---
**TEAM:**
_Alex Coppinger_, _Federico Aprile_


---

- **Modular, User‐Driven Recommendations**  
  Vibelink empowers users to build, save, and iterate on their own recommendation “vibes” (algorithms) instead of passively consuming one-off song suggestions.  
- **“Music Spaces” vs. Single Tracks**  
  Rather than recommending a single song, Vibelink models an entire music environment based on user‐defined criteria (e.g., genre, mood). Users generate a “vibe” that represents a custom music bubble, inside which new tracks are discovered. For each algorithm, the user rates the song presented to them–they can then add it or/and move on to the next song.
- **Long-Term, Editable Algorithms**  
  Each vibe is stored in the database so users can revisit, refine, and expand it over time—allowing for deeper, fine-tuned exploration of a chosen music space.  

---

## Strategy
- **Framework & Tools**  
  - **Backend:** Django
  - **API Integration:** Spotipy library + Spotify Web API for playlist and track metadata  
  - **Database:** SQLite for simpler Django integration during prototyping  
  - **Version Control:** Git & GitHub (feature branches, pull requests, merge conflict resolution)  
- **Interactive, Survey-Style Workflow**  
  Users begin by entering keywords (e.g., “Funk Music”) to seed a playlist search. Then, through a simple 1–5 rating interface, they iteratively refine track recommendations—updating internal coefficients that shape the vibe’s music space.  
- **Human & Automated Learning Resources**  
  - Relied on GitHub Copilot and ChatGPT for code snippets and syntax guidance  
  - Received regular feedback, coding best practices, and debugging advice from Professor Janata  
- **Minimum Viable Prototype Focus**  
  Prioritized creating a working proof of concept over implementing a fully optimized, production-grade algorithm.  

---

## Rough Plan
1. **Concept & Scope Definition**  
   - Define “vibe” as a stored user algorithm mapping track weights inside a custom music space.  
   - Identify core features: keyword‐based seeding, iterative rating loop, coefficient updates, and vibe persistence.  
2. **Initial Technology Choices**
   - Django (models → views → templates).  
   - Integrate Spotipy for playlist/track queries.  
4. **Pivot & Simplify**  
   - Scale back advanced ML ideas (tokenization, regressions, neural nets) in favor of correlation analysis.  
5. **Development Workflow**  
   - Each developer works on local feature branches, pushes to a shared GitHub repo.  
   - Merge often, resolve conflicts, and continuously update personal development journals for troubleshooting notes.  
6. **Iterative Prototype Release**  
   - Launch first “seed” version: user inputs a keyword → gets a seed track → rates a few tracks → saves a basic vibe.  
   - Collect instructor feedback, improve stability, and tweak coefficient logic.  
7. **Future Iterations (Beyond MVP)**  
   - Migrate to PostgreSQL or a cloud database for scale.  
   - Refine UI/UX (clean styling, real-time coefficient visualization).  
   - Implement optional randomization to surface niche tracks.  
   - Introduce dynamic “widen/narrow” controls for navigating the music bubble.  

---

## Algorithm Development and Ideas
- **Data Model & Linking Tables**  
  - **Track**: `track_id`, `name`, `artist`, `popularity`, etc.  
  - **Playlist**: `playlist_id`, `name`, `owner`, `creation_date`  
  - **TrackPlaylist (Linking Table)**:
  - **Vibe**: represents a saved algorithm instance (map of `track_id` → `coefficient`)  
  - **UserXPlaylist & UserXTrack**: capture user ratings and playlist inclusion decisions  
- **Coefficient Update Logic (Correlation-Based)**  
  1. **Seed Stage**  
     - Perform a Spotify playlist search using user-provided keywords → retrieve top N tracks.  
     - Initialize each track’s coefficient to zero.  
     - Select the most popular track in that seed space as the first recommendation.  
  2. **Rating Loop** (repeat until user finishes):  
     - **Present Track**: display the current highest-coefficient track (or seed track on first iteration).  
     - **User Action**: rate track on a scale of 1–5, check “Add to Playlist” if desired.  
     - **Update Logic**:
       - Update coefficients
         - Weight Normalization (prevent runaway coefficient inflation)
       - Resolve ties among equal coefficients by selecting the track with higher Spotify popularity.  
       - (Future option: break ties randomly among highest-coefficient tracks to surface niche songs.)  
     - **Proceed**: select next track and loop.  
  3. **Completion Stage**  
     - Save final coefficient map under the user’s Vibe record
     - Vibe persists so the user can return, continue rating, or edit later.
      
- **Advanced Algorithm Ideas (Future Work)**  
  - **Hybrid Approaches**: incorporate audio‐feature similarity (tempo, energy, key, etc.) alongside playlist‐based correlation.   
  - **Dynamic “Widen/Narrow” Controls**: allow users to expand or contract their music bubble in real time—e.g., widen: include related subgenres; narrow: filter by tighter similarity thresholds.  
  - **Negative Feedback Handling**: allow explicit “remove” actions to exclude tracks entirely from the vibe instead of merely setting coefficient to zero.  


