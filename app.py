import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from transformers import pipeline
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found in environment.")

client = Groq(api_key=GROQ_API_KEY)

# Load the specialized disaster classification model
# Using a global variable to cache it
classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        classifier = pipeline("image-classification", model="Luwayy/disaster_images_model")
    return classifier

# --- DATA ---
RESCUE_CONTACTS = {
    "India": {"Ambulance": "102", "Fire": "101", "Security": "Ext 100", "Maintenance": "Ext 55"},
    "USA": {"Emergency": "911", "Security": "Ext 0", "Maintenance": "Ext 11"},
    "UK": {"Emergency": "999", "Security": "Ext 9", "Maintenance": "Ext 88"}
}

LANGUAGES = {"English": "en", "Urdu": "ur", "Hindi": "hi", "Japanese": "ja"}
LOCATIONS = ["Grand Phoenix Hotel, Mumbai", "Regency Suites, Karachi", "London Royal Stay", "The Plaza, New York"]

PRECAUTIONS = {
    "fire": [
        "Activate fire suppression system in affected zone.",
        "Initiate verbal evacuation commands via PA system.",
        "Staff to guide guests to designated assembly points.",
        "Secure gas lines and electrical mains in the kitchen area.",
        "Avoid elevators; use emergency stairwells only."
    ],
    "medical": [
        "Dispatch on-site First Aid Responder to room/area immediately.",
        "Prepare AED unit if cardiac symptoms are reported.",
        "Clear lobby/entrance for incoming ambulance access.",
        "Retrieve guest emergency contact info from PMS.",
        "Maintain calm environment for other guests."
    ],
    "security": [
        "Lock down all non-essential entry and exit points.",
        "Direct guests to remain in rooms and secure doors.",
        "Monitor CCTV feed for the affected sector.",
        "Notify local law enforcement immediately.",
        "Silence non-essential alarms to prevent panic."
    ]
}

@app.route('/')
def index():
    return render_template('index.html', 
                           locations=LOCATIONS, 
                           languages=LANGUAGES, 
                           contacts=RESCUE_CONTACTS)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    location = data.get('location', 'Hotel Main')
    language = data.get('language', 'English')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        model = "llama-3.3-70b-versatile"
        sys_msg = (
            f"You are the 'Adaptive Explainable AI Crisis Orchestrator' for {location}. "
            f"Your role is to detect, decide, and coordinate real-time responses in a hospitality environment. "
            f"Output Language: {language}. "
            "For every crisis report, you MUST provide exactly four sections in Markdown: "
            "1. **DECISION**: What is the immediate command? "
            "2. **WHO**: Who is assigned to this action? (Guests/Kitchen Staff/Security/Management) "
            "3. **WHERE**: Which zones are affected/safe? "
            "4. **REASONING (XAI)**: Explain WHY this decision was made based on system logic and safety protocols. "
            "Be authoritative, calm, and prioritize life safety."
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        full_res = response.choices[0].message.content
        return jsonify({"response": full_res})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/image-analysis')
def image_analysis_page():
    return render_template('image_analysis.html', 
                           languages=LANGUAGES, 
                           locations=LOCATIONS, 
                           contacts=RESCUE_CONTACTS)

@app.route('/analyze', methods=['POST'])
def analyze():
    manual_override = request.form.get('manual_override', 'None')
    file = request.files.get('file')
    
    label = None
    source = None
    
    if manual_override != 'None':
        label = manual_override.lower()
        source = "User Override"
    elif file:
        try:
            img = Image.open(file.stream).convert("RGB")
            c = get_classifier()
            results = c(img)
            
            label = results[0]['label'].lower()
            confidence = results[0]['score']
            source = f"AI Model ({confidence:.1%})"
            
            # Simple keyword mapping
            if "fire" in label: label = "fire"
            elif "water" in label or "flood" in label: label = "flood"
            elif "earthquake" in label or "quake" in label: label = "earthquake"
            elif "land" in label: label = "landslide"
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    if label:
        tips = PRECAUTIONS.get(label, [
            "Maintain a safe distance from the hazard zone.",
            "Contact local emergency services immediately.",
            "Follow official government evacuation orders."
        ])
        return jsonify({
            "label": label.title(),
            "source": source,
            "precautions": tips
        })
    else:
        return jsonify({"error": "No image or override provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
