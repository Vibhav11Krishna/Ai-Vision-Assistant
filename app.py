import streamlit as st

from streamlit_webrtc import webrtc_streamer

from vision.processor import VisionProcessor


st.set_page_config(
    page_title="AI Vision Assistant",
    page_icon="👁️",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("👁️ AI Vision Assistant")

st.caption(
    "Your AI-powered extra pair of eyes"
)


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

st.sidebar.header("⚙️ Settings")


confidence = st.sidebar.slider(
    "Detection Confidence",

    min_value=0.20,

    max_value=0.90,

    value=0.45,

    step=0.05
)


# --------------------------------------------------
# LIVE CAMERA
# --------------------------------------------------

st.subheader("📷 Live Camera")


ctx = webrtc_streamer(

    key="vision-assistant",

    video_processor_factory=VisionProcessor,

    media_stream_constraints={
        "video": True,
        "audio": False
    },

    async_processing=True
)


# --------------------------------------------------
# ASSISTANT
# --------------------------------------------------

st.subheader("🧠 Assistant")


if ctx.video_processor:

    # Update confidence

    ctx.video_processor.confidence = confidence

    message = (
        ctx.video_processor.current_message
    )

else:

    message = "Start the camera to begin."


# Display current message

st.info(
    "🔊 " + message.capitalize()
)


# --------------------------------------------------
# AUTOMATIC SPEECH
# --------------------------------------------------

st.subheader("🔊 Voice Assistant")


# Streamlit custom component
# sends the message to browser JavaScript.

try:

    speech_component = st.components.v2.component(

        name="vision_voice_assistant",

        html="""
        <div>
            <button id="voiceButton">
                🔊 Enable Voice
            </button>

            <p id="voiceStatus">
                Voice is disabled
            </p>
        </div>
        """,

        css="""

        button {

            padding: 10px 18px;

            border-radius: 10px;

            border: none;

            cursor: pointer;

            font-size: 16px;

        }

        p {

            font-size: 14px;

            opacity: 0.7;

        }

        """,

        js="""

        export default function(component) {

            const {
                data,
                parentElement
            } = component;


            const button =
                parentElement.querySelector(
                    "#voiceButton"
                );


            const status =
                parentElement.querySelector(
                    "#voiceStatus"
                );


            let voiceEnabled = false;

            let lastMessage = "";


            // Enable voice after user interaction

            button.onclick = () => {

                voiceEnabled = true;

                status.textContent =
                    "Voice enabled ✓";


                // Unlock speech synthesis

                const test =
                    new SpeechSynthesisUtterance(
                        "Voice assistant enabled."
                    );

                window.speechSynthesis.speak(
                    test
                );

            };


            // Speak new messages

            const message =
                data?.message || "";


            if (
                voiceEnabled &&
                message &&
                message !== lastMessage
            ) {

                lastMessage = message;


                window.speechSynthesis.cancel();


                const speech =
                    new SpeechSynthesisUtterance(
                        message
                    );


                speech.rate = 1.0;

                speech.pitch = 1.0;

                speech.volume = 1.0;


                window.speechSynthesis.speak(
                    speech
                );

            }


            return () => {};

        }

        """

    )


    speech_component(

        data={
            "message": message
        },

        key="voice-component"

    )


except Exception:

    st.warning(
        "Voice component requires "
        "a recent Streamlit version."
    )


# --------------------------------------------------
# DETECTED OBJECTS
# --------------------------------------------------

if ctx.video_processor:

    detections = (
        ctx.video_processor.detections
    )

    if detections:

        st.subheader(
            "🔎 Detected Objects"
        )


        for detection in detections:

            name = detection["name"]

            confidence_value = (
                detection["confidence"]
            )

            position = (
                detection["position"]
            )

            distance = (
                detection["distance"]
            )


            if distance is not None:

                distance_text = (
                    f"{distance} m"
                )

            else:

                distance_text = (
                    "Unknown"
                )


            st.write(
                f"### {name.title()}"
            )

            st.write(
                f"Confidence: "
                f"{confidence_value:.0%}"
            )

            st.write(
                f"Position: {position}"
            )

            st.write(
                f"Distance: {distance_text}"
            )

            st.divider()


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.subheader(
    "ℹ️ How it works"
)


st.write(
    """
📷 Camera

↓

🤖 YOLO Object Detection

↓

📍 Position Detection

↓

📏 Distance Estimation

↓

🧠 AI Assistant

↓

🔊 Voice Output
"""
)


# --------------------------------------------------
# SAFETY WARNING
# --------------------------------------------------

st.warning(
    "⚠️ Distance estimates are approximate. "
    "This prototype should NOT be used for "
    "safety-critical navigation."
)