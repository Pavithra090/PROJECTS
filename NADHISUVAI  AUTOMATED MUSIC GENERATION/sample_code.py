# Function to create MIDI directly without using the model 
# This provides a more reliable fallback that explicitly uses Indian instruments 
def create_direct_midi(genre, output_file): 
    midi_data = pretty_midi.PrettyMIDI() 
     
    # Get appropriate instruments for this genre 
    primary_instrument_name = primary_instrument_by_genre.get(genre, "sitar") 
    secondary_instrument_name = secondary_instrument_by_genre.get(genre, 
"tabla") 
     
    primary_program = INDIAN_INSTRUMENTS[primary_instrument_name] 
    secondary_program = 
INDIAN_INSTRUMENTS[secondary_instrument_name] 
     
    # Create instrument tracks 
    lead_instrument = pretty_midi.Instrument(program=primary_program, 
name=primary_instrument_name) 
    rhythm_instrument = pretty_midi.Instrument(program=secondary_program, 
name=secondary_instrument_name) 
31 
 
     
    # Get the appropriate raga/scale for this genre 
    raga = RAGAS.get(genre, RAGAS["melody"]) 
     
    # Set genre-specific parameters 
    if genre == "fastbeat": 
        note_duration = 0.15 
        velocity_main = 95 
        num_notes = 120 
    elif genre == "classical": 
        note_duration = 0.5 
        velocity_main = 85 
        num_notes = 80 
    else: 
        note_duration = 0.25 
        velocity_main = 90 
        num_notes = 100 
     
    # Generate main melody using raga notes 
    start_time = 0 
    for i in range(num_notes): 
        # Select a note from the raga 
32 
 
        octave = random.randint(4, 6) 
        scale_note = random.choice(raga) 
        note_pitch = scale_note + (octave - 4) * 12 
         
        # Vary velocity for expressiveness 
        if i % 8 == 0:  # Emphasize certain beats 
            velocity = velocity_main + random.randint(-5, 10) 
        else: 
            velocity = velocity_main + random.randint(-10, 5) 
         
        # Vary duration 
        duration = note_duration * random.uniform(0.8, 1.3) 
         
        # Create note 
        note = pretty_midi.Note( 
            velocity=velocity, 
            pitch=note_pitch, 
            start=start_time, 
            end=start_time + duration 
        ) 
         
        # Add note to instrument 
33 
 
        lead_instrument.notes.append(note) 
         
        # Move to next note with slight variation in timing 
        start_time += duration * random.uniform(0.95, 1.05) 
     
    # Add rhythm/percussion notes 
    rhythm_start = 0 
    rhythm_duration = 0.2 
    for i in range(int(num_notes * 1.5)): 
        # Skip some beats for variation 
        if random.random() < 0.2: 
            rhythm_start += rhythm_duration 
            continue 
             
        # Basic rhythm pattern based on genre 
        if genre == "reggae": 
            pitch = 45 if i % 3 == 0 else 47 
        elif genre == "rock": 
            pitch = 48 if i % 4 == 0 else 50 
        elif genre == "fastbeat": 
            pitch = 46 + (i % 3) 
        elif genre == "blues": 
34 
 
            pitch = 48 if i % 2 == 0 else 51 
        else: 
            pitch = 45 + (i % 3) 
             
        # Create percussion note 
        rhythm_note = pretty_midi.Note( 
            velocity=70 + random.randint(-10, 15), 
            pitch=pitch, 
            start=rhythm_start, 
            end=rhythm_start + rhythm_duration * random.uniform(0.8, 1.2) 
        ) 
        rhythm_instrument.notes.append(rhythm_note) 
         
        # Move to next rhythm note 
        rhythm_start += rhythm_duration 
     
    # Add drone for certain genres 
    if genre in ["classical", "melody", "blues"]: 
        tanpura = 
pretty_midi.Instrument(program=INDIAN_INSTRUMENTS["tanpura"], 
name="tanpura") 
        root_note = raga[0]  # Use raga's root note 
35 
 
        fifth_note = root_note + 7  # Perfect fifth 
         
        # Add drone notes 
        for i in range(0, int(start_time), 2): 
            # Root note 
            note = pretty_midi.Note( 
                velocity=50, 
                pitch=root_note - 12,  # Lower octave 
                start=i, 
                end=i + 1.9 
            ) 
            tanpura.notes.append(note) 
             
            # Fifth note 
            note = pretty_midi.Note( 
                velocity=45, 
                pitch=fifth_note - 12,  # Lower octave 
                start=i + 0.7, 
                end=i + 2.6 
            ) 
            tanpura.notes.append(note) 
         
36 
 
midi_data.instruments.append(tanpura) 
# Add instruments to the MIDI file 
midi_data.instruments.append(lead_instrument) 
midi_data.instruments.append(rhythm_instrument) 
# Write the MIDI file 
midi_data.write(output_file) 
print(f"Direct MIDI file saved as '{output_file}' with genre '{genre}' using 
Indian instruments {primary_instrument_name} and 
{secondary_instrument_name}") 
from flask import Flask, request, jsonify, send_file 
import random 
import numpy as np 
import pretty_midi 
import os 
import traceback 
# Attempt to load the model and handle potential errors 
try: 
from tensorflow.keras.models import load_model 
37 
    model = load_model('D:\music_generator 
main\music_generator\model\music_generation_model.h5') 
except Exception as e: 
    print(f"Error loading model: {e}") 
    traceback.print_exc()  # Print detailed error for debugging 
    model = None 
 
# Temperature sampling function for randomness 
def sample_with_temperature(predictions, temperature=1.0): 
    predictions = np.log(predictions + 1e-8) / temperature 
    predictions = np.exp(predictions) 
    predictions /= np.sum(predictions) 
    return np.random.choice(len(predictions), p=predictions) 
 
# Define Indian instruments with their MIDI program numbers 
INDIAN_INSTRUMENTS = { 
    "sitar": 104,        # Sitar 
    "sarod": 105,        # Banjo (closest to Sarod) 
    "bansuri": 73,       # Flute 
    "shehnai": 111,      # Shanai 
    "tabla": 116,        # Taiko Drum (closest to Tabla) 
    "santoor": 15,       # Dulcimer (closest to Santoor) 
38 
 
    "sarangi": 110,      # Fiddle (closest to Sarangi) 
    "tanpura": 106,      # Koto (closest to Tanpura) 
    "mridangam": 117,    # Melodic Drum (closest to Mridangam) 
    "harmonium": 22      # Accordion (closest to Harmonium) 
} 
 
# Define ragas (scales) for different genres 
# These will help create more authentic Indian music characteristics 
RAGAS = { 
    "melody": [48, 50, 52, 53, 55, 57, 59, 60],      # Yaman (similar to Ionian) 
    "fastbeat": [48, 50, 51, 55, 56, 58, 59, 60],    # Bhairav 
    "jazz": [48, 49, 52, 55, 56, 58, 60],            # Purvi 
    "rock": [48, 51, 53, 55, 58, 60],                # Bhairavi (with phrygian influence) 
    "classical": [48, 50, 52, 54, 55, 57, 59, 60],   # Bhupali (similar to major 
pentatonic) 
    "blues": [48, 51, 53, 54, 55, 58, 60],           # Charukeshi (with blue notes) 
    "pop": [48, 50, 52, 53, 55, 57, 58, 60],         # Khamaj 
    "electronic": [48, 50, 53, 55, 58, 60],          # Malkauns with electronic 
influence 
    "reggae": [48, 50, 52, 55, 57, 60]               # Desh with reggae rhythm 
} 
 
39 
 
# Define chord sequence options for each genre based on Indian music 
structures 
# Using combinations of notes from appropriate ragas 
chord_sequences_by_genre = { 
    "melody": [ 
        [[48, 52, 55], [50, 53, 57], [52, 55, 59], [53, 57, 60]], 
        [[48, 52, 55], [50, 55, 59], [55, 59, 62], [57, 60, 64]] 
    ], 
    "fastbeat": [ 
        [[48, 51, 55], [51, 55, 58], [55, 58, 62], [56, 59, 63]], 
        [[48, 51, 56], [51, 56, 59], [56, 59, 63], [58, 61, 65]] 
    ], 
    "jazz": [ 
        [[48, 52, 55, 58], [49, 52, 56, 59], [52, 56, 59, 62], [56, 58, 62, 65]], 
        [[48, 52, 55, 58], [52, 55, 58, 62], [55, 58, 62, 65], [58, 62, 65, 69]] 
    ], 
    "rock": [ 
        [[48, 51, 55], [51, 55, 58], [53, 58, 62], [55, 58, 62]], 
        [[48, 53, 58], [51, 55, 60], [53, 58, 62], [55, 58, 63]] 
    ], 
    "classical": [ 
        [[48, 52, 55], [50, 54, 57], [52, 55, 59], [54, 57, 60]], 
40 
 
        [[48, 52, 55], [50, 54, 57], [52, 55, 59], [55, 59, 62]] 
    ], 
    "blues": [ 
        [[48, 51, 54], [51, 54, 58], [53, 54, 58], [54, 58, 61]], 
        [[48, 51, 54], [51, 53, 58], [53, 58, 61], [54, 58, 61]] 
    ], 
    "pop": [ 
        [[48, 52, 55], [52, 55, 57], [53, 57, 60], [52, 55, 58]], 
        [[48, 50, 55], [50, 53, 57], [52, 55, 58], [53, 57, 60]] 
    ], 
    "electronic": [ 
        [[48, 53, 58], [50, 55, 58], [53, 58, 62], [55, 58, 62]], 
        [[48, 53, 55], [50, 53, 58], [53, 55, 62], [55, 62, 65]] 
    ], 
    "reggae": [ 
        [[48, 52, 55], [50, 55, 57], [52, 55, 60], [55, 57, 60]], 
        [[48, 50, 55], [50, 52, 57], [52, 55, 57], [55, 57, 60]] 
    ] 
} 
 
# Map genres to appropriate Indian instruments 
primary_instrument_by_genre = { 
41 
 
    "melody": "bansuri",      # Flute for melodic pieces 
    "fastbeat": "tabla",      # Tabla for rhythmic fast beats 
    "jazz": "santoor",        # Santoor for jazz-like improvisations 
    "rock": "sitar",          # Sitar for rock-style pieces 
    "classical": "sarangi",   # Sarangi for classical pieces 
    "blues": "sarod",         # Sarod has a bluesy quality 
    "pop": "harmonium",       # Harmonium works well for pop 
    "electronic": "santoor",  # Santoor with processing for electronic 
    "reggae": "sitar"         # Sitar for reggae-influenced pieces 
} 
 
secondary_instrument_by_genre = { 
    "melody": "tanpura",      # Tanpura drone for melody 
    "fastbeat": "mridangam",  # Mridangam for fast beats 
    "jazz": "sarod",          # Sarod for jazz solos 
    "rock": "tabla",          # Tabla for rock beats 
    "classical": "tanpura",   # Tanpura drone for classical 
    "blues": "bansuri",       # Bansuri for blues melodies 
    "pop": "sitar",           # Sitar for pop hooks 
    "electronic": "tabla",    # Tabla for electronic beats 
    "reggae": "tabla"         # Tabla for reggae rhythm 
} 
42 
 
 
# Add variation parameters to avoid repetitive patterns 
def add_variation(note, variation_level=0.2): 
    """Add slight variations to note timing and velocity to avoid repetitive 
patterns""" 
    # Apply small random variations to note parameters 
    velocity_variation = random.uniform(1 - variation_level, 1 + variation_level) 
    timing_variation = random.uniform(1 - variation_level/2, 1 + 
variation_level/2) 
    # Ensure values stay within valid ranges 
    velocity = min(127, max(60, int(note.velocity * velocity_variation))) 
    note.velocity = velocity 
    # Modify note timing slightly, but ensure it doesn't overlap with next note 
    # (implemented by caller who controls note.end) 
    return timing_variation 
 
# Generate notes with user-defined genre using Indian scales 
def generate_notes_based_on_genre(model, start_sequence, num_notes, 
int_to_note, sequence_length=50, temperature=0.9, genre="melody"): 
    pattern = start_sequence 
    generated_notes = [] 
     
43 
 
    # Use the raga for this genre 
    raga = RAGAS.get(genre, RAGAS["melody"]) 
     
    # Select chord sequence for the genre 
    chord_sequence = random.choice(chord_sequences_by_genre.get(genre, 
chord_sequences_by_genre["melody"])) 
     
    # Use a higher temperature for more variation 
    temp = temperature + random.uniform(0.1, 0.3) 
     
    # Generate notes with non-repetitive patterns by introducing variations 
    for i in range(num_notes): 
        if len(pattern) > sequence_length: 
            pattern = pattern[-sequence_length:] 
             
        prediction_input = np.reshape(pattern, (1, sequence_length, 1)) 
        prediction = model.predict(prediction_input, verbose=0) 
         
        # Use temperature sampling for more variation 
        note_index = sample_with_temperature(prediction[0], temp) 
         
        # Apply raga constraints but with variations to avoid repetition 
44 
 
        if i % 7 == 0:  # Occasionally allow notes outside the raga for variation 
            result = int_to_note[note_index] 
        else: 
            # Map to nearest raga note but with some variations 
            nearest_raga_note = min(raga, key=lambda x: abs(x - (note_index % 12) 
+ 48)) 
            octave = note_index // 12 
            result = int_to_note[nearest_raga_note + (octave - 4) * 12] 
             
            # Occasionally use chord notes for harmony 
            if random.random() < 0.3: 
                current_chord = chord_sequence[i % len(chord_sequence)] 
                chord_note = random.choice(current_chord) 
                result = int_to_note[chord_note] 
         
        generated_notes.append(result) 
         
        # Add slightly modified note index to pattern to avoid repetition 
        modified_index = note_index 
        if random.random() < 0.15:  # Small chance to introduce a variation 
            modified_index = max(0, min(127, note_index + random.randint(-2, 2))) 
        pattern.append(modified_index) 
45 
 
         
        # Occasionally vary the temperature to add more unpredictability 
        if random.random() < 0.1: 
            temp = temperature + random.uniform(-0.2, 0.4) 
            temp = max(0.5, min(1.5, temp))  # Keep temperature in reasonable 
range 
 
    return generated_notes 
 
# Convert notes to MIDI with Indian instruments 
def notes_to_midi(generated_notes, genre, output_file='unique_music.mid'): 
    midi_data = pretty_midi.PrettyMIDI() 
     
    # Get primary and secondary instruments for this genre 
    primary_instrument_name = primary_instrument_by_genre.get(genre, "sitar") 
    secondary_instrument_name = secondary_instrument_by_genre.get(genre, 
"tabla") 
     
    primary_program = INDIAN_INSTRUMENTS[primary_instrument_name] 
    secondary_program = 
INDIAN_INSTRUMENTS[secondary_instrument_name]
# Create the main instrument track 
    main_instrument = pretty_midi.Instrument(program=primary_program) 
    secondary_instrument = 
pretty_midi.Instrument(program=secondary_program) 
     
    # Add a tanpura drone for certain genres 
    if genre in ["classical", "melody"]: 
        tanpura = 
pretty_midi.Instrument(program=INDIAN_INSTRUMENTS["tanpura"]) 
        root_note = RAGAS[genre][0]  # Use the root note of the raga 
        fifth_note = root_note + 7 
         
        # Add tanpura drone notes throughout the piece 
        for i in range(0, 120, 2):  # Add drone every 2 seconds 
            # Root note 
            note = pretty_midi.Note( 
                velocity=45, 
                pitch=root_note, 
                start=i, 
                end=i + 1.8 
            ) 
            tanpura.notes.append(note) 
47 
 
             
            # Fifth note 
            if i % 4 == 0:  # Add fifth every 4 seconds 
                note = pretty_midi.Note( 
                    velocity=40, 
                    pitch=fifth_note, 
                    start=i + 0.5, 
                    end=i + 2.3 
                ) 
                tanpura.notes.append(note) 
         
        midi_data.instruments.append(tanpura) 
     
    # Set timing parameters based on genre 
    if genre == "fastbeat": 
        base_duration = 0.15 
        duration_range = (0.1, 0.25) 
    elif genre == "classical": 
        base_duration = 0.5 
        duration_range = (0.3, 0.8) 
    else: 
        base_duration = 0.3 
48 
 
        duration_range = (0.2, 0.5) 
     
    # Add main melody notes 
    start_time = 0 
    for i, note_name in enumerate(generated_notes): 
        note_number = int(note_name) 
         
        # Vary velocity for expressiveness 
        if i % 8 == 0:  # Emphasize certain beats 
            velocity = random.randint(90, 110) 
        else: 
            velocity = random.randint(70, 95) 
         
        # Vary duration for more natural sound and to avoid repetition 
        if i % 4 == 0 and random.random() < 0.7: 
            # Longer notes on certain beats 
            duration = random.uniform(base_duration * 1.5, base_duration * 2.2) 
        else: 
            # Normal notes with slight variation 
            duration = random.uniform(duration_range[0], duration_range[1]) 
             
        # Create and add the note 
49 
 
        note = pretty_midi.Note( 
            velocity=velocity, 
            pitch=note_number, 
            start=start_time, 
            end=start_time + duration 
        ) 
         
        # Apply variation to avoid repetitive patterns 
        timing_variation = add_variation(note, 0.15) 
         
        # Determine which instrument gets this note 
        if random.random() < 0.8:  # 80% of notes go to primary instrument 
            main_instrument.notes.append(note) 
        else: 
            # Shift some notes to secondary instrument for texture 
            secondary_note = pretty_midi.Note( 
                velocity=min(100, velocity + random.randint(-10, 10)), 
                pitch=note_number, 
                start=start_time + random.uniform(0, 0.1),  # Slight timing offset 
                end=start_time + duration * 0.9  # Slightly different duration 
            ) 
            secondary_instrument.notes.append(secondary_note) 
50 
 
         
        # Apply timing variations to avoid repetitive rhythm 
        start_time += duration * timing_variation 
     
    # Add rhythmic patterns for tabla/percussion (secondary instrument) in 
certain genres 
    if genre in ["fastbeat", "rock", "pop", "electronic", "reggae"]: 
        rhythm_start = 0 
         
        # Create non-repetitive but genre-appropriate rhythm patterns 
        rhythm_duration = 0.2 if genre == "fastbeat" else 0.3 
         
        for i in range(int(start_time * 2)):  # Fill throughout the piece 
            if random.random() < 0.25:  # Add some randomness to avoid repetition 
                continue 
                 
            # Vary the rhythm note pitch based on genre 
            if genre == "reggae": 
                pitch = 45 if i % 3 == 0 else 47 
            elif genre == "rock": 
                pitch = 48 if i % 4 == 0 else 50 
            elif genre == "fastbeat": 
51 
 
                pitch = 46 + (i % 5) 
            else: 
                pitch = 45 + (i % 4) 
                 
            # Create percussion note 
            rhythm_note = pretty_midi.Note( 
                velocity=75 + random.randint(-15, 15), 
                pitch=pitch, 
                start=rhythm_start, 
                end=rhythm_start + rhythm_duration * random.uniform(0.8, 1.2) 
            ) 
            secondary_instrument.notes.append(rhythm_note) 
             
            # Vary timing to avoid strict repetition 
            rhythm_start += rhythm_duration * random.uniform(0.95, 1.05) 
     
    # Add the instruments to the MIDI file 
    midi_data.instruments.append(main_instrument) 
    midi_data.instruments.append(secondary_instrument) 
     
    # Write the MIDI file 
    midi_data.write(output_file) 
52 
 
    print(f"MIDI file saved as '{output_file}' with genre '{genre}' using Indian 
instruments {primary_instrument_name} and {secondary_instrument_name}") 
 
# Initialize Flask app 
app = Flask(_name_) 
 
@app.route('/generate_music', methods=['GET']) 
def generate_music(): 
    try: 
        if model is None: 
            # Fallback to direct MIDI generation if model isn't loaded 
            return generate_direct_midi() 
             
        genre = request.args.get('genre', 'melody').lower() 
         
        # Start with notes that fit the genre's scale 
        if genre in RAGAS: 
            raga_notes = RAGAS[genre] 
            start_sequence = [random.choice(raga_notes) for _ in range(50)] 
        else: 
            start_sequence = [random.randint(48, 72) for _ in range(50)] 
         
53 
 
        num_notes = 200 
        int_to_note = {i: str(i) for i in range(128)} 
         
        # Adjust temperature based on genre for more variation 
        if genre in ["jazz", "blues"]: 
            temp = 1.0  # More variation for jazz and blues 
        elif genre in ["electronic", "rock"]: 
            temp = 0.9  # Medium variation 
        else: 
            temp = 0.8  # Standard variation 
         
        generated_notes = generate_notes_based_on_genre( 
            model,  
            start_sequence,  
            num_notes,  
            int_to_note,  
            genre=genre,  
            temperature=temp 
        ) 
         
        output_filename = f"{genre}_unique_music.mid" 
        notes_to_midi(generated_notes, genre, output_file=output_filename) 
 
 
        if os.path.exists(output_filename): 
            return send_file(output_filename, as_attachment=True) 
        else: 
            return jsonify({"error": "Failed to generate MIDI file."}), 500 
     
    except Exception as e: 
        print(f"Error in generate_music: {e}") 
        traceback.print_exc()  # Print detailed error for debugging 
        # Fallback to direct MIDI generation 
        return generate_direct_midi() 
 
# Fallback function that creates MIDI directly without the model 
def generate_direct_midi(): 
    genre = request.args.get('genre', 'melody').lower() 
    output_filename = f"{genre}_unique_music.mid" 
     
    # Create MIDI file directly without using the model 
    create_direct_midi(genre, output_filename) 
     
    if os.path.exists(output_filename): 
        return send_file(output_filename, as_attachment=True)
        else: 
return jsonify({"error": "Failed to generate MIDI file."}), 500 
if _name_ == '_main_': 
app.run(debug=True, host='0.0.0.0', port=5000)
