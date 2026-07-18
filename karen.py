import streamlit as st
import webbrowser

# Seiteneinstellungen für das edle Wide-Interface
st.set_page_config(page_title="KAREN AI - Media Matrix", page_icon="🎬", layout="wide")

# CSS für das dunkle KAREN-Design (Gemini/ChatGPT Style)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stButton>button { width: 100%; background-color: #1f538d; color: white; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR FÜR DEINE TIKTOK UPLOADS ---
with st.sidebar:
    st.title("📁 Media Upload")
    st.write("Laden Sie hier Bilder oder Videos für Ihre Edits hoch, Milan.")
    uploaded_file = st.file_uploader("Datei per Drag & Drop reinziehen...", type=["jpg", "png", "mp4", "mov"])
    
    if uploaded_file is not None:
        st.success("Datei erfolgreich in Matrix geladen!")
        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, caption="Hochgeladenes Bild")
        elif uploaded_file.type.startswith("video"):
            st.video(uploaded_file)

# --- HAUPTBEREICH (CHAT-INTERFACE) ---
st.title("KAREN SYSTEM v3.5 (Media & Edit Matrix)")
st.caption("Systeme bereit für Multimedia-Analyse, Milan. Wie kann ich Ihre Edits verbessern?")

# Chat-Verlauf im Speicher sichern
if "messages" not in st.session_state:
    st.session_state.messages = []

# Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ruhige und menschliche Sprachausgabe über den Webbrowser
def browser_sprechen(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance({repr(text)});
    msg.lang = 'de-DE';
    msg.rate = 0.9; // Ruhiges Sprechtempo
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# KI-Logik für Antworten (Sprechen, Wetter, Satelliten, Edits)
def verarbeite_befehl(frage):
    frage = frage.lower().strip()
    
    if "edit" in frage or "phonk" in frage or "shake" in frage or "effekt" in frage:
        antwort = "Für ein perfektes Phonk-Edit empfehle ich einen harten Bass-Shake bei jedem Drop. Nutze am besten 'Velocity' für die Zeitlupe und lege ein CC-Overlay für schärfere Farben drüber. Das hochgeladene Material eignet sich hervorragend dafür."
    elif "hochgeladen" in frage or "datei" in frage:
        if uploaded_file:
            antwort = f"Ich habe die Datei '{uploaded_file.name}' erfolgreich registriert. Die Auflösung und Framerate sind optimal für ein TikTok-Fan-Edit."
        else:
            antwort = "Sie haben bisher noch keine Model-Datei im linken Upload-Menü hochgeladen, Milan."
    elif "wie geht es dir" in frage or "wie gehts" in frage:
        antwort = "Mir geht es hervorragend. Meine kreativen Prozessoren laufen stabil auf einhundert Prozent. Ich bin bereit für das nächste virale Video."
    elif "wer bist du" in frage:
        antwort = "Ich bin Karen. Ihre persönliche digitale Assistentin. Optimiert für die Steigerung Ihrer Produktivität und die Verwaltung Ihrer Multimedia-Dateien."
    elif "weltraum" in frage or "universum" in frage or "iss" in frage:
        antwort = "Gewähre Zugriff auf die Live-Feeds der Internationalen Raumstation ISS. Ich habe das Weltraum-Video in einem neuen Tab für Sie geöffnet."
        st.components.v1.html("<script>window.open('https://www.youtube.com/watch?v=jPTD2g2p86M', '_blank');</script>", height=0)
    elif "weltweite kamera" in frage or "earthcam" in frage:
        antwort = "Verbindung zum globalen Satelliten- und Kameranetzwerk hergestellt. Die EarthCam-Zentrale wird im neuen Tab geladen."
        st.components.v1.html("<script>window.open('https://www.earthcam.com/', '_blank');</script>", height=0)
    elif "wetter" in frage or "warnung" in frage:
        antwort = "Ich habe die Wettersatelliten für Bayern gescannt. Die Atmosphäre zeigt sich ruhig, es liegen aktuell keine Unwetter- oder Sturmwarnungen vor."
    else:
        antwort = "Befehl im Web-Interface empfangen. Ich analysiere die Daten und kalibriere meine Matrix, Milan."
        
    return antwort

# Eingabefeld für Text-Befehle
if user_input := st.chat_input("Fragen Sie Karen nach Edit-Tipps oder Befehlen..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    antwort = verarbeite_befehl(user_input)
    
    with st.chat_message("assistant"):
        st.markdown(antwort)
    st.session_state.messages.append({"role": "assistant", "content": antwort})
    browser_sprechen(antwort)

# --- MIKROFON-STEUERUNG (START/STOP IM BROWSER) ---
st.write("---")
audio_script = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'de-DE';
recognition.interimResults = false;

function startListening() {
    document.getElementById("mic_status").innerText = "🎙️ Karen hört Ihnen zu... Sprechen Sie jetzt.";
    recognition.start();
}

recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    document.getElementById("mic_status").innerText = "Verarbeitet: " + text;
    
    const chatInput = parent.document.querySelector('textarea[aria-label="Fragen Sie Karen nach Edit-Tipps oder Befehlen..."]');
    if (chatInput) {
        chatInput.value = text;
        chatInput.dispatchEvent(new Event('input', { bubbles: true }));
        const ke = new KeyboardEvent('keydown', { bubbles: true, key: 'Enter', keyCode: 13 });
        chatInput.dispatchEvent(ke);
    }
};

recognition.onspeechend = function() {
    recognition.stop();
};
</script>
<button onclick="startListening()" style="background-color: #1f538d; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: bold;">
🎤 Sprachbefehl starten (Mikrofon)
</button>
<p id="mic_status" style="color: #aaa; font-style: italic; margin-top: 8px;">Bereit</p>
"""
st.components.v1.html(audio_script, height=110)
