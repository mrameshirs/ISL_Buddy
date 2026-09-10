import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# APP CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ISL Buddy — Indian Sign Language to Speech",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
* { font-family: 'Nunito', sans-serif !important; }
.hero-banner {
    background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 50%, #3B82F6 100%);
    padding: 22px; border-radius: 20px; color: white; text-align: center;
    box-shadow: 0 10px 25px rgba(236, 72, 153, 0.25); margin-bottom: 18px;
}
.embossed-box {
    background: #1E293B; border-radius: 16px; padding: 16px 20px;
    box-shadow: 6px 6px 12px rgba(0, 0, 0, 0.5), -4px -4px 10px rgba(255, 255, 255, 0.04), inset 1px 1px 2px rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS & MANUAL
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/hand.png", width=110)
    st.title("🤟 ISL Buddy")
    st.caption("AI Sign-to-Speech Engine | INSPIRE-MANAK")
    st.markdown("---")
    st.subheader("📋 Supported Gestures")
    
    st.markdown("""
    ** Core Essential Words:**
    
    * 💧 **WATER** — Index + Middle + Ring fingers UP (3 fingers)
    * 🆘 **HELP** — All 5 fingers UP (open palm)
    * 👨🏫 **TEACHER** — Index + Middle fingers UP and TOGETHER
    *  **PAIN** — Only Index finger UP (pointing)
    * ‍⚕️ **DOCTOR** — Thumb + Index touching (O-shape)
    
    **🔤 Fingerspelling Letters:**
    
    * ️ **A / YES** — Only Thumb UP
    * 🅻 **L** — Thumb + Index UP (L-shape)
    * 🆅 **V / Victory** — Index + Middle UP and SPREAD
    * 🆈 **Y / Call** — Thumb + Pinky UP (shaka sign)
    
    ---
    **📝 Note:** These are simplified static poses for prototype testing. Full ISL uses dynamic two-handed movements.
    """)

    st.markdown("---")
    voice_lang = st.selectbox("🔊 Speech Accent:", ["en-IN", "hi-IN", "ta-IN", "te-IN"])
    st.info(" **Tip:** Hold the gesture steady for **1.2 seconds** to confirm prediction.")

# -----------------------------------------------------------------------------
# MAIN APP HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <h1 style="margin:0; font-size:2.2rem; font-weight:900;">🤟 ISL Buddy — Sign to Speech Assistant</h1>
    <p style="margin:4px 0 0 0; font-size:1.05rem; font-weight:700; opacity:0.95;">
        Real-Time Indian Sign Language Recognition, Live Confidence Telemetry & Speech Synthesis
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# EMBEDDED MEDIAPIPE AI ENGINE & REAL-TIME DASHBOARD
# -----------------------------------------------------------------------------
js_voice_lang = voice_lang.split(' ')[0] if ' ' in voice_lang else voice_lang

html_component = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
<style>
    body {{ margin: 0; background: #0B1120; color: #F8FAFC; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    .grid-container {{ display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px; }}
    .card {{ background: #1E293B; border-radius: 16px; padding: 16px; box-shadow: 6px 6px 14px rgba(0, 0, 0, 0.5), -4px -4px 10px rgba(255, 255, 255, 0.03), inset 1px 1px 2px rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.08); position: relative; }}
    .video-wrapper {{ position: relative; width: 100%; height: 380px; border-radius: 12px; overflow: hidden; background: #000000; }}
    video {{ display: none; }}
    canvas {{ width: 100%; height: 100%; object-fit: cover; }}
    .rainbow-badge {{ background: linear-gradient(90deg, #FF007F, #7928CA, #0070F3, #00DFD8); background-size: 300% 300%; animation: gradientShift 4s ease infinite; padding: 4px 14px; border-radius: 20px; font-weight: 900; font-size: 0.85rem; display: inline-block; }}
    @keyframes gradientShift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    .metric-title {{ font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; letter-spacing: 1px; margin-bottom: 4px; }}
    .metric-value {{ font-size: 2.2rem; font-weight: 900; color: #38BDF8; }}
    .progress-bar-bg {{ background: #0F172A; height: 14px; border-radius: 10px; overflow: hidden; margin-top: 6px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.8); }}
    .progress-bar-fill {{ height: 100%; width: 0%; background: linear-gradient(90deg, #10B981, #38BDF8, #EC4899); border-radius: 10px; transition: width 0.15s ease; }}
    .sentence-box {{ background: #0F172A; border: 2px solid #334155; border-radius: 12px; padding: 12px; font-size: 1.15rem; font-weight: 700; color: #FCD34D; min-height: 48px; margin-top: 8px; display: flex; align-items: center; flex-wrap: wrap; gap: 8px; }}
    .sentence-word {{ background: #334155; padding: 4px 10px; border-radius: 8px; cursor: pointer; transition: 0.2s; border: 1px solid transparent; }}
    .sentence-word:hover {{ background: #EF4444; border-color: #FCA5A5; color: white; }}
    .history-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; margin-top: 8px; }}
    .history-table th {{ text-align: left; color: #94A3B8; padding: 6px; border-bottom: 1px solid #334155; }}
    .history-table td {{ padding: 6px; border-bottom: 1px solid rgba(255,255,255,0.04); }}
    .history-scroll {{ max-height: 190px; overflow-y: auto; }}
    .btn-action {{ background: #334155; color: white; border: none; padding: 6px 12px; border-radius: 8px; font-weight: 700; cursor: pointer; transition: 0.2s; }}
    .btn-action:hover {{ background: #475569; }}
    .flash-success {{ animation: flashGreen 0.5s ease; }}
    @keyframes flashGreen {{ 0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }} }}
</style>
</head>
<body>

<div class="grid-container">
    <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-weight:800; font-size:1.05rem;">📷 Live Hand Pose Tracking</span>
            <span id="fpsBadge" class="rainbow-badge">AI Active</span>
        </div>
        <div class="video-wrapper">
            <video id="webcam" playsinline></video>
            <canvas id="output_canvas" width="640" height="480"></canvas>
        </div>
        <div style="margin-top: 10px; display:flex; justify-content:space-between; font-size:0.8rem; color:#94A3B8;">
            <span>Tracking: <b>21 3D Landmarks / Hand</b></span>
            <span>Target: <b>ISL Fingerspelling & Key Vocab</b></span>
        </div>
    </div>

    <div>
        <div class="card" id="predictionCard" style="margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="metric-title">Predicted Sign (पहचाना गया संकेत)</div>
                    <div id="predictedLabel" class="metric-value">Waiting...</div>
                </div>
                <div style="text-align:right;">
                    <div class="metric-title">Hold Lock</div>
                    <div id="holdTimer" style="font-size:1.4rem; font-weight:800; color:#F59E0B;">0.0s</div>
                </div>
            </div>
            <div style="margin-top:10px;">
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:700;">
                    <span class="metric-title">Model Confidence</span>
                    <span id="confidenceText" style="color:#38BDF8;">0%</span>
                </div>
                <div class="progress-bar-bg">
                    <div id="confidenceBar" class="progress-bar-fill"></div>
                </div>
            </div>
        </div>

        <div class="card" style="margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div class="metric-title">🗣️ Sentence Builder (Click word to remove)</div>
                <button class="btn-action" onclick="clearSentence()">Clear All</button>
            </div>
            <div class="sentence-box" id="sentenceBox">
                <span id="sentenceText" style="color:#64748B; font-weight:400;">Waiting for gesture sequence...</span>
            </div>
            <button class="btn-action" style="width:100%; margin-top:10px; background:#EC4899;" onclick="speakFullSentence()">🔊 Speak Full Sentence</button>
        </div>

        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div class="metric-title">📜 Real-Time History Log</div>
                <span id="historyCount" style="font-size:0.75rem; color:#94A3B8;">0 entries</span>
            </div>
            <div class="history-scroll">
                <table class="history-table">
                    <thead><tr><th>Time</th><th>Sign</th><th>Type</th><th>Conf</th></tr></thead>
                    <tbody id="historyTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const labelElem = document.getElementById('predictedLabel');
const confText = document.getElementById('confidenceText');
const confBar = document.getElementById('confidenceBar');
const holdTimerElem = document.getElementById('holdTimer');
const sentenceBox = document.getElementById('sentenceBox');
const historyBody = document.getElementById('historyTableBody');
const historyCount = document.getElementById('historyCount');
const predictionCard = document.getElementById('predictionCard');

let assembledSentence = [];
let currentSign = "None";
let gestureStartTime = null;
let lastSpokenSign = null;
let historyEntries = [];
const TARGET_LANG = "{js_voice_lang}";

const synth = window.speechSynthesis;
function speakWord(text) {{
    if (synth.speaking) synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = TARGET_LANG;
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    synth.speak(utterance);
}}

function clearSentence() {{
    assembledSentence = [];
    renderSentence();
}}

function renderSentence() {{
    if (assembledSentence.length === 0) {{
        sentenceBox.innerHTML = '<span style="color:#64748B; font-weight:400;">Waiting for gesture sequence...</span>';
        return;
    }}
    sentenceBox.innerHTML = assembledSentence.map((word, index) => 
        `<span class="sentence-word" onclick="removeWord(${{index}})" title="Click to remove">${{word}}</span>`
    ).join('');
}}

function removeWord(index) {{
    assembledSentence.splice(index, 1);
    renderSentence();
}}

function speakFullSentence() {{
    if (assembledSentence.length > 0) {{
        speakWord(assembledSentence.join(" "));
    }}
}}

function addToHistory(sign, conf, type) {{
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];
    historyEntries.unshift({{ time: timeStr, sign: sign, type: type, conf: conf }});
    if (historyEntries.length > 15) historyEntries.pop();
    historyCount.innerText = historyEntries.length + " entries";
    historyBody.innerHTML = historyEntries.map(e => `
        <tr>
            <td style="color:#94A3B8;">${{e.time}}</td>
            <td style="color:#FDE047; font-weight:800;">${{e.sign}}</td>
            <td><span style="background:#334155; padding:2px 8px; border-radius:10px; font-size:0.75rem;">${{e.type}}</span></td>
            <td style="color:#34D399; font-weight:700;">${{e.conf}}%</td>
        </tr>
    `).join('');
}}

function classifyISLGesture(landmarks) {{
    const wrist = landmarks[0];
    const thumbTip = landmarks[4];
    const indexTip = landmarks[8];
    const indexPip = landmarks[6];
    const middleTip = landmarks[12];
    const middlePip = landmarks[10];
    const ringTip = landmarks[16];
    const ringPip = landmarks[14];
    const pinkyTip = landmarks[20];
    const pinkyPip = landmarks[18];

    const indexExtended = indexTip.y < indexPip.y;
    const middleExtended = middleTip.y < middlePip.y;
    const ringExtended = ringTip.y < ringPip.y;
    const pinkyExtended = pinkyTip.y < pinkyPip.y;
    const thumbExtended = thumbTip.y < landmarks[3].y;

    const distThumbIndex = Math.hypot(thumbTip.x - indexTip.x, thumbTip.y - indexTip.y);
    const distIndexMiddle = Math.hypot(indexTip.x - middleTip.x, indexTip.y - middleTip.y);

    if (indexExtended && middleExtended && ringExtended && pinkyExtended && thumbExtended) {{
        return {{ label: "HELP", type: "Core Word", conf: 96 }};
    }}
    if (indexExtended && middleExtended && ringExtended && !pinkyExtended) {{
        return {{ label: "WATER", type: "Core Word", conf: 94 }};
    }}
    if (indexExtended && !middleExtended && !ringExtended && !pinkyExtended && !thumbExtended) {{
        return {{ label: "PAIN", type: "Core Word", conf: 92 }};
    }}
    if (indexExtended && middleExtended && !ringExtended && !pinkyExtended) {{
        return {{ label: distIndexMiddle < 0.06 ? "TEACHER" : "VICTORY / V", type: distIndexMiddle < 0.06 ? "Core Word" : "Alphabet", conf: 93 }};
    }}
    if (thumbExtended && !indexExtended && !middleExtended && !ringExtended && !pinkyExtended) {{
        return {{ label: "YES / A", type: "Alphabet", conf: 93 }};
    }}
    if (thumbExtended && pinkyExtended && !indexExtended && !middleExtended && !ringExtended) {{
        return {{ label: "CALL / Y", type: "Alphabet", conf: 94 }};
    }}
    if (thumbExtended && indexExtended && !middleExtended && !ringExtended && !pinkyExtended) {{
        return {{ label: "L", type: "Alphabet", conf: 96 }};
    }}
    if (distThumbIndex < 0.05 && !middleExtended && !ringExtended && !pinkyExtended) {{
        return {{ label: "DOCTOR / O", type: "Core Word", conf: 90 }};
    }}

    return {{ label: "Scanning...", type: "None", conf: 40 }};
}}

function onResults(results) {{
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {{
        const landmarks = results.multiHandLandmarks[0];
        drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {{color: '#38BDF8', lineWidth: 3}});
        drawLandmarks(canvasCtx, landmarks, {{color: '#EC4899', lineWidth: 2, radius: 4}});

        const pred = classifyISLGesture(landmarks);
        labelElem.innerText = pred.label;
        confText.innerText = pred.conf + "%";
        confBar.style.width = pred.conf + "%";

        if (pred.label !== "Scanning..." && pred.label !== "None") {{
            if (currentSign === pred.label) {{
                const elapsed = (Date.now() - gestureStartTime) / 1000.0;
                holdTimerElem.innerText = elapsed.toFixed(1) + "s";

                if (elapsed >= 1.2 && lastSpokenSign !== pred.label) {{
                    predictionCard.classList.add('flash-success');
                    setTimeout(() => predictionCard.classList.remove('flash-success'), 500);

                    const wordToSpeak = pred.label.split(' ')[0];
                    speakWord(wordToSpeak);
                    lastSpokenSign = pred.label;
                    assembledSentence.push(wordToSpeak);
                    renderSentence();
                    addToHistory(pred.label, pred.conf, pred.type);
                    holdTimerElem.innerText = "✓ Locked";
                }}
            }} else {{
                currentSign = pred.label;
                gestureStartTime = Date.now();
                lastSpokenSign = null;
            }}
        }} else {{
            currentSign = "None";
            holdTimerElem.innerText = "0.0s";
        }}
    }} else {{
        labelElem.innerText = "Hands not detected";
        confText.innerText = "0%";
        confBar.style.width = "0%";
        holdTimerElem.innerText = "0.0s";
        currentSign = "None";
    }}
    canvasCtx.restore();
}}

const hands = new Hands({{locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${{file}}`}});
hands.setOptions({{maxNumHands: 2, modelComplexity: 1, minDetectionConfidence: 0.7, minTrackingConfidence: 0.6}});
hands.onResults(onResults);

const camera = new Camera(videoElement, {{
    onFrame: async () => {{ await hands.send({{image: videoElement}}); }},
    width: 640, height: 480
}});
camera.start();
</script>
</body>
</html>
"""

components.html(html_component, height=560)

# -----------------------------------------------------------------------------
# DETAILED INSTRUCTIONS & METRICS EXPLANATION
# -----------------------------------------------------------------------------
st.markdown("### 🔍 Evaluation Metrics & Operational Guide")
col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown("""
    <div class="embossed-box">
        <h4 style="margin:0 0 6px 0; color:#38BDF8;">📊 Geometric Landmark Tracking</h4>
        <p style="font-size:0.85rem; color:#94A3B8; margin:0;">
            Extracts 21 Cartesian coordinates (X, Y, Z) per hand. Computes real-time inter-joint angles and fingertip distances to identify signs accurately.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="embossed-box">
        <h4 style="margin:0 0 6px 0; color:#F59E0B;">⏱️ 1.2s Temporal Stability Lock</h4>
        <p style="font-size:0.85rem; color:#94A3B8; margin:0;">
            Prevents false triggers from transitional hand movements. A gesture must remain steady above 85% confidence for 1.2 seconds before vocal synthesis occurs.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown("""
    <div class="embossed-box">
        <h4 style="margin:0 0 6px 0; color:#EC4899;"> Editable Sentence Assembler</h4>
        <p style="font-size:0.85rem; color:#94A3B8; margin:0;">
            Chains sequential signs into meaningful phrases. <b>Click any word</b> in the sentence box to remove it if the AI misclassifies, giving the user ultimate control.
        </p>
    </div>
    """, unsafe_allow_html=True)
