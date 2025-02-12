import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
from vosk import Model, KaldiRecognizer
import wave
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load VOSK model
MODEL_PATH = "vosk_model"
if not os.path.exists(MODEL_PATH):
    st.error("VOSK model not found! Please download and place it in the project directory.")
    st.stop()

model = Model(MODEL_PATH)

# Correct answers dictionary
correct_answers = {
    "question_1": "Python is a high-level programming language.",
    "question_2": "Flask is a lightweight web framework for Python.",
    "question_3": "Decorators are functions that modify the behavior of other functions."
}

# Calculate similarity score
def calculate_similarity(answer, correct_answer):
    if not answer or not correct_answer:
        return 0
    
    vectorizer = TfidfVectorizer().fit_transform([answer, correct_answer])
    cosine_sim = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return cosine_sim[0][0]  # similarity score between 0 and 1

# Evaluate answers
def evaluate_answer(question_id, student_answer, correct_answers):
    correct_answer = correct_answers.get(question_id)
    if not correct_answer or not student_answer:
        return 0
    similarity_score = calculate_similarity(student_answer, correct_answer)
    return 1 if similarity_score > 0.8 else 0

# Record audio
def record_audio(duration, filename="output.wav"):
    st.info("Recording audio... Speak now!")
    audio_data = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()
    write(filename, 44100, audio_data)
    st.success(f"Audio saved as {filename}")

# Transcribe audio
def transcribe_audio(filename):
    wf = wave.open(filename, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = eval(recognizer.Result())
            text += result.get("text", "")

    return text

# Streamlit UI
st.title("Voice Answer Module")
st.write("Record your answers for the exam questions.")

questions = [
    "What is Python?",
    "Explain Flask.",
    "What are decorators in Python?"
]

answers = {}

# Loop through each question to record and transcribe answers
for i, question in enumerate(questions):
    st.subheader(f"Question {i+1}: {question}")
    
    # Button to start recording for each question
    if st.button(f"Record Answer for Question {i+1}"):

        # Record the audio for the question
        filename = f"answer_{i+1}.wav"
        record_audio(10, filename=filename)
        
        # Transcribe the audio file
        st.write("Transcribing...")
        transcription = transcribe_audio(filename)
        st.success(f"Transcription for Question {i+1}: {transcription}")

        # Store the transcription as the answer
        answers[f"question_{i+1}"] = transcription

# Evaluate answers and calculate score
if st.button("Submit Answers"):
    total_score = 0
    st.write("All Answers Recorded:")
    for i, question in enumerate(questions):
        student_answer = answers.get(f"question_{i+1}")
        score = evaluate_answer(f"question_{i+1}", student_answer, correct_answers)
        total_score += score
        st.write(f"Question {i+1}: {student_answer}")
        st.write(f"Score: {score} (1 for correct, 0 for incorrect)")
    
    # Show results in the same page using HTML-like formatting
    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px; font-family: Arial;">
            <h1 style="color: #4CAF50;">Advanced Online Exam Management System</h1>
            <h2>Results</h2>
            <p>Your total score is: 12</p>
            <p>
                {"You need to improve. Better luck next time!" }
            </p>
            <p style="color: gray;">Try to improve on the areas you missed.</p>
        </div>
    """, unsafe_allow_html=True)
