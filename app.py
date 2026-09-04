import streamlit as st
import streamlit.components.v1 as components

from streamlit_webrtc import webrtc_streamer, RTCConfiguration

from vision.processor import VisionProcessor
from vision.state import vision_state


st.set_page_config(
    page_title="AI Vision Assistant",
    page_icon="👁️",
    layout="centered"
)

st.title("👁️ AI Vision Assistant")
st.caption("Your AI-powered extra pair of eyes")


# ==================================================
# SETTINGS
# ==================================================

st.sidebar.header("⚙️ Settings")

confidence = st.sidebar.slider(
    "Detection Confidence",
    min_value=0.20,
    max_value=0.90,
    value=0.45,
    step=0.05
)


# ==================================================
# CAMERA
# ==================================================

st.subheader("📷 Live Camera")

RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [
        {
            "urls": [
                "stun:stun.l.google.com:19302"
            ]
        }
    ]
})

ctx = webrtc_streamer(
    key="vision-assistant",

    video_processor_factory=VisionProcessor,

    rtc_configuration=RTC_CONFIGURATION,

    media_stream_constraints={
        "video": True,
        "audio": False
    },

    async_processing=True
)


if ctx.video_processor:
    ctx.video_processor.confidence = confidence


# ==================================================
# CURRENT STATE
# ==================================================

message, detections, version = vision_state.get()


# ==================================================
# AI ASSISTANT
# ==================================================

st.subheader("🧠 AI Assistant")

st.success(
    "🔊 " + message.capitalize()
)


# ==================================================
# VOICE
# ==================================================

st.subheader("🔊 Voice Assistant")

components.html(
    f"""
    <div style="
        font-family: Arial, sans-serif;
        padding: 10px;
        text-align: center;
    ">

        <button
            id="voiceButton"
            style="
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
            "
        >
            🔊 Enable Voice
        </button>

        <p id="voiceStatus">
            Voice disabled
        </p>

        <p style="font-size:13px;color:gray;">
            Tap Enable Voice once to allow browser speech.
        </p>

    </div>

    <script>

        const button =
            document.getElementById("voiceButton");

        const status =
            document.getElementById("voiceStatus");


        let enabled = false;


        button.addEventListener(
            "click",
            function() {{

                enabled = true;

                status.innerText =
                    "Voice enabled ✓";


                const speech =
                    new SpeechSynthesisUtterance(
                        "Voice assistant enabled."
                    );


                speech.lang = "en-US";

                speech.rate = 0.95;

                speech.volume = 1;


                window.speechSynthesis.cancel();

                window.speechSynthesis.speak(
                    speech
                );

            }}
        );


        const message =
            {message!r};


        if (
            enabled &&
            message
        ) {{

            const speech =
                new SpeechSynthesisUtterance(
                    message
                );


            speech.lang = "en-US";

            speech.rate = 0.95;

            speech.volume = 1;


            window.speechSynthesis.cancel();

            window.speechSynthesis.speak(
                speech
            );

        }}

    </script>
    """,
    height=180
)


# ==================================================
# OBJECTS
# ==================================================

if detections:

    st.subheader("🔎 Detected Objects")

    for detection in detections:

        st.write(
            f"### {detection['name'].title()}"
        )

        st.write(
            f"Confidence: "
            f"{detection['confidence']:.0%}"
        )

        st.write(
            f"Position: "
            f"{detection['position']}"
        )

        if detection["distance"] is not None:

            st.write(
                f"Distance: "
                f"{detection['distance']} m"
            )

        else:

            st.write(
                "Distance: Unknown"
            )

        st.divider()


# ==================================================
# PIPELINE
# ==================================================

st.subheader("ℹ️ How it works")

st.write(
    """
📷 Live Camera
→
🤖 YOLO
→
📍 Position
→
📏 Distance
→
🧠 AI Assistant
→
🔊 Voice
"""
)


st.warning(
    "⚠️ Distance estimates are approximate. "
    "This prototype should NOT be used for "
    "safety-critical navigation."
)