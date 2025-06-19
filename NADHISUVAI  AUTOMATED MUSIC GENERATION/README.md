🎼 NADHISUVAI: Automated Music Generation Using Neural Networks
A deep learning-based intelligent music generation system for genre-specific compositions.

🧠 Overview
NADHISUVAI is a genre-aware music generation system that leverages deep learning, constraint satisfaction, and probabilistic modeling to compose melodically rich and rhythmically accurate music. Designed to mimic the style of real-world genres like jazz, classical, blues, and electronic, the system generates MIDI music with seamless integration of melody and rhythm.

Created for musicians, producers, and AI enthusiasts, NADHISUVAI offers an intuitive interface and dynamic output engine capable of creating original compositions based on minimal input. It is ideal for creative assistance, music education, and experimental audio synthesis.

🚀 Features
🎹 MIDI-based Melody and Rhythm Generation

📊 Genre-aware Neural Network Modeling (LSTM)

🧠 Constraint Satisfaction & Hidden Markov Models for Music Theory Adherence

🎵 Real-Time Composition Preview

📁 MIDI File Export

🎛️ Tempo and Style Customization

🎶 Genre Library: Classical, Pop, Jazz, Rock, Blues, Electronic, Reggae, and more

📈 Dynamic Note Velocity and Duration Sampling

📱 Android-Compatible Mobile UI for Playback

🧩 Modules
1. 🎼 MIDI Preprocessing Engine
Extracts pitch, velocity, and duration from raw MIDI files. Applies normalization, augmentation (pitch shifting, time-stretching), and sequence padding.

2. 🎶 Melody Generator
Uses CSP + HMM + LSTM to create musically rich melodies with adherence to key signatures and transition rules.

3. 🥁 Rhythm Synthesizer
Learns beat patterns and time signatures. Aligns rhythmic structures to generated melodies using synchronization constraints.

4. 🧠 Genre Classifier
Enables genre-specific generation by training on categorized MIDI sets. Influences note selection, tempo, and rhythmic feel.

5. 🎛️ Playback & Output Interface
Mobile app allows users to choose genre, preview generated compositions, and download the results in MIDI format.

🛠️ Tech Stack
Languages:

Python

XML/Java (for Android App)

Libraries & Tools:

TensorFlow / Keras

Music21

NumPy, pandas

MIDIUtil

Android Studio

⚙️ How It Works
MIDI files are extracted and normalized by pitch, duration, and velocity.

Melody is generated using LSTM models trained with constraints from CSP and HMMs.

Rhythm is learned from time-signature and beat patterns in genre-specific datasets.

Generated melodies and rhythms are synchronized.

The final output is composed, rendered, and exported as a MIDI file.

User can preview, stop, or download the composition from the mobile interface.

📲 App UI Snapshots
🎵 Home	🎧 Genre Select	🎼 Playing	⬇️ Download
![Fig1]	![Fig2]	![Fig3]	![Fig4]

(Insert actual images or links if uploading screenshots to GitHub)

📈 Results & Evaluation
The system was evaluated based on:

Melodic Coherence

Genre Authenticity

Listener Engagement
Initial feedback indicates high novelty and musicality across genres.

🔮 Future Enhancements
🎤 Voice-based input for melody seed

🧠 Emotional tone control (happy, sad, energetic)

🎨 User-driven style transfer (e.g., “generate Mozart-style pop”)

📡 Web Dashboard Interface for music generation

📡 Real-time Music Jamming with AI

📜 License
This project is part of a B.E. Mini Project submitted to Rajalakshmi Engineering College in partial fulfillment for the degree of B.E. in Artificial Intelligence and Machine Learning (Anna University).

For educational use only. Commercial applications may require licensing.

📚 References
Based on research and citations from IEEE, ACM, and top AI/ML music generation literature. See full citations in the project report.


