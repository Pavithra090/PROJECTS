🎵 NADHISUVAI: Automated Music Generation Using Neural Networks
NADHISUVAI is an AI-powered music generation system that composes melodically coherent and aesthetically pleasing music using deep learning techniques. Built as part of our coursework in Mobile Application Development and Machine Learning & Deep Learning Applications, the project focuses on integrating melody and rhythm to create music across multiple genres.

🧠 Overview
This project leverages:

🎶 MIDI Dataset processing

🧩 Constraint Satisfaction Problems (CSPs) for enforcing music theory rules

📊 Hidden Markov Models (HMMs) for pattern prediction

🔁 Recurrent Neural Networks (RNNs) and LSTM for melody sequence generation

🎼 Rhythm-melody synchronization for genre-specific outputs

🎯 Features
Generate music in various genres: 🎷 Jazz, 🎹 Classical, 🎸 Rock, 🎧 Electronic, and more

Real-time generation and playback

Export generated music as MIDI files

Customize style, tempo, and mood

Mobile-friendly interface for quick generation and playback

🧰 Tech Stack
Frontend: Flutter / Android XML (as per app UI)

Backend: Python (TensorFlow, NumPy, Music21, etc.)

AI Models: LSTM, HMM

File Handling: MIDI format parsing and generation

🗃️ Dataset
MIDI Files across multiple genres

Preprocessed for pitch, velocity, and duration

Augmented using:

Pitch shifting

Time stretching

Note reordering

🛠️ Methodology
Feature Extraction: Pitch, velocity, duration from MIDI

Data Augmentation: Enhances genre diversity

Melody Generation: Combines CSPs + HMMs + LSTM

Rhythm Generation: Beat & tempo analysis

Integration: Synchronizes rhythm with melody

Playback & Download: Outputs playable and downloadable MIDI files

📲 App Screenshots
Genre Selection	Music Playing	Download Screen
![Genre List]	![Playing Screen]	![Download UI]

(Images to be added here manually or linked from your repository)

📈 Results
Generated music in genres like jazz, classical, and pop

Evaluated based on:

Musicality

Novelty

Listener engagement

High adaptability to new genre inputs and style variations

📚 Literature References
Our model builds on prior research including LSTM networks for music sequence learning, GANs for melody quality, and attention mechanisms for dynamic variation. Full references are available in the report.

👨‍💻 Contributors
Maharaja R – GitHub Profile

Pavithra J – GitHub Profile

Project under the guidance of Rajalakshmi Engineering College (Anna University) – Department of Artificial Intelligence and Machine Learning

📦 How to Run
bash
Copy
Edit
# Clone the repo
git clone https://github.com/your-username/nadhisuvai.git

# Install dependencies
pip install -r requirements.txt

# Run the music generator
python app.py

# Launch mobile app / emulator to use GUI
🎼 Sample Output
You can find sample generated MIDI files in the samples/ folder.

📄 License
This project is for academic and educational purposes. Please contact us before commercial use.
