import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="TCS Healthcare AI",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🩺 TCS Healthcare AI")

st.caption(
    "AI-powered clinical documentation and clinical knowledge assistant"
)


# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs([
    "🎙️ Clinical Documentation",
    "🔎 Clinical Knowledge"
])


# ============================================================
# TAB 1 — CLINICAL DOCUMENTATION
# ============================================================

with tab1:

    st.header("🎙️ Clinical Documentation")

    st.write(
        "Provide the clinical consultation using an audio file "
        "or record it directly using your microphone."
    )

    # --------------------------------------------------------
    # INPUT MODE
    # --------------------------------------------------------

    input_mode = st.radio(
        "How would you like to provide the consultation?",
        [
            "📁 Upload Audio",
            "🎤 Record from Microphone"
        ],
        horizontal=True
    )

    audio_file = None

    # ========================================================
    # OPTION 1 — UPLOAD AUDIO
    # ========================================================

    if input_mode == "📁 Upload Audio":

        st.subheader("📁 Upload Consultation")

        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=[
                "mp3",
                "wav",
                "m4a",
                "mp4",
                "mpeg",
                "webm"
            ],
            key="audio_upload"
        )

        if uploaded_file:

            st.success(
                f"Uploaded: {uploaded_file.name}"
            )

            st.audio(
                uploaded_file,
                format=uploaded_file.type
            )

            audio_file = uploaded_file

    # ========================================================
    # OPTION 2 — MICROPHONE
    # ========================================================

    else:

        st.subheader("🎤 Record Consultation")

        st.info(
            "Click the microphone button below and speak naturally "
            "during the consultation."
        )

        recorded_audio = st.audio_input(
            "Start recording"
        )

        if recorded_audio:

            st.success(
                "Recording captured successfully."
            )

            st.audio(
                recorded_audio
            )

            audio_file = recorded_audio

    # ========================================================
    # PROCESS CONSULTATION
    # ========================================================

    if audio_file:

        st.divider()

        st.subheader("⚙️ Process Consultation")

        if st.button(
            "🚀 Process Consultation",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Processing consultation... This may take a while."
            ):

                try:

                    # ------------------------------------------------
                    # SEND AUDIO TO FASTAPI
                    # ------------------------------------------------

                    response = requests.post(
                        f"{API_URL}/consultation/process",
                        files={
                            "file": (
                                "consultation_audio.wav",
                                audio_file.getvalue(),
                                audio_file.type
                            )
                        },
                        timeout=300
                    )

                    # ------------------------------------------------
                    # SUCCESS
                    # ------------------------------------------------

                    if response.status_code == 200:

                        result = response.json()

                        st.success(
                            "✅ Consultation processed successfully!"
                        )

                        # ====================================================
                        # TRANSCRIPT
                        # ====================================================

                        st.divider()

                        st.subheader(
                            "📝 Redacted Transcript"
                        )

                        transcript = result.get(
                            "redacted_transcript",
                            "Transcript not available."
                        )

                        st.text_area(
                            "Transcript",
                            transcript,
                            height=220
                        )

                        # ====================================================
                        # SOAP NOTE
                        # ====================================================

                        st.divider()

                        st.subheader(
                            "📋 SOAP Note"
                        )

                        soap = result.get(
                            "soap_note",
                            {}
                        )

                        # ------------------------------------------------
                        # SUBJECTIVE
                        # ------------------------------------------------

                        col1, col2 = st.columns(2)

                        with col1:

                            st.markdown(
                                "### 🟢 Subjective"
                            )

                            st.write(
                                soap.get(
                                    "subjective",
                                    "Not available."
                                )
                            )

                        # ------------------------------------------------
                        # OBJECTIVE
                        # ------------------------------------------------

                        with col2:

                            st.markdown(
                                "### 🔵 Objective"
                            )

                            st.write(
                                soap.get(
                                    "objective",
                                    "Not available."
                                )
                            )

                        # ------------------------------------------------
                        # ASSESSMENT
                        # ------------------------------------------------

                        col3, col4 = st.columns(2)

                        with col3:

                            st.markdown(
                                "### 🟠 Assessment"
                            )

                            st.write(
                                soap.get(
                                    "assessment",
                                    "Not available."
                                )
                            )

                        # ------------------------------------------------
                        # PLAN
                        # ------------------------------------------------

                        with col4:

                            st.markdown(
                                "### 🔴 Plan"
                            )

                            st.write(
                                soap.get(
                                    "plan",
                                    "Not available."
                                )
                            )

                    # ------------------------------------------------
                    # BACKEND ERROR
                    # ------------------------------------------------

                    else:

                        st.error(
                            f"❌ Backend returned "
                            f"status code {response.status_code}"
                        )

                        st.code(
                            response.text
                        )

                # ----------------------------------------------------
                # CONNECTION ERROR
                # ----------------------------------------------------

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to the FastAPI backend."
                    )

                    st.info(
                        "Make sure FastAPI is running with:"
                    )

                    st.code(
                        "uvicorn backend.main:app --reload"
                    )

                # ----------------------------------------------------
                # TIMEOUT
                # ----------------------------------------------------

                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ The request took too long."
                    )

                    st.info(
                        "Whisper and the local LLM may need more time "
                        "to process the consultation."
                    )

                # ----------------------------------------------------
                # OTHER REQUEST ERROR
                # ----------------------------------------------------

                except requests.exceptions.RequestException as e:

                    st.error(
                        "❌ Request failed."
                    )

                    st.code(
                        str(e)
                    )

                # ----------------------------------------------------
                # UNEXPECTED ERROR
                # ----------------------------------------------------

                except Exception as e:

                    st.error(
                        "❌ Unexpected error occurred."
                    )

                    st.code(
                        str(e)
                    )


# ============================================================
# TAB 2 — CLINICAL KNOWLEDGE / RAG
# ============================================================

with tab2:

    st.header("🔎 Clinical Knowledge")

    st.write(
        "Ask a clinical question and retrieve information "
        "from the clinical knowledge base."
    )

    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    question = st.text_area(
        "Enter your clinical question",
        placeholder=(
            "Example: What are common causes of cough?"
        ),
        height=120
    )

    # --------------------------------------------------------
    # TOP K
    # --------------------------------------------------------

    top_k = st.slider(
        "Number of sources to retrieve",
        min_value=1,
        max_value=5,
        value=3
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if st.button(
        "🔎 Search Clinical Knowledge",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "⚠️ Please enter a clinical question."
            )

        else:

            with st.spinner(
                "🔍 Searching clinical knowledge..."
            ):

                try:

                    # ------------------------------------------------
                    # SEND QUESTION TO FASTAPI
                    # ------------------------------------------------

                    response = requests.post(
                        f"{API_URL}/clinical/query",
                        json={
                            "question": question,
                            "top_k": top_k
                        },
                        timeout=120
                    )

                    # ------------------------------------------------
                    # SUCCESS
                    # ------------------------------------------------

                    if response.status_code == 200:

                        result = response.json()

                        st.success(
                            "✅ Answer generated successfully!"
                        )

                        # ====================================================
                        # ANSWER
                        # ====================================================

                        st.divider()

                        st.subheader(
                            "💡 Clinical Answer"
                        )

                        answer = result.get(
                            "answer",
                            "Answer not available."
                        )

                        st.write(
                            answer
                        )

                        # ====================================================
                        # SOURCES
                        # ====================================================

                        st.divider()

                        st.subheader(
                            "📚 Retrieved Sources"
                        )

                        sources = result.get(
                            "sources",
                            []
                        )

                        if not sources:

                            st.info(
                                "No sources were returned."
                            )

                        else:

                            for i, source in enumerate(
                                sources,
                                start=1
                            ):

                                score = source.get(
                                    "score",
                                    0
                                )

                                text = source.get(
                                    "text",
                                    "Source text unavailable."
                                )

                                with st.expander(
                                    f"📖 Source {i} — "
                                    f"Similarity: {score:.4f}"
                                ):

                                    st.write(
                                        text
                                    )

                    # ------------------------------------------------
                    # BACKEND ERROR
                    # ------------------------------------------------

                    else:

                        st.error(
                            f"❌ Backend returned "
                            f"status code {response.status_code}"
                        )

                        st.code(
                            response.text
                        )

                # ----------------------------------------------------
                # CONNECTION ERROR
                # ----------------------------------------------------

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to the FastAPI backend."
                    )

                    st.info(
                        "Make sure FastAPI is running with:"
                    )

                    st.code(
                        "uvicorn backend.main:app --reload"
                    )

                # ----------------------------------------------------
                # TIMEOUT
                # ----------------------------------------------------

                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ The request took too long."
                    )

                # ----------------------------------------------------
                # REQUEST ERROR
                # ----------------------------------------------------

                except requests.exceptions.RequestException as e:

                    st.error(
                        "❌ Request failed."
                    )

                    st.code(
                        str(e)
                    )

                # ----------------------------------------------------
                # UNEXPECTED ERROR
                # ----------------------------------------------------

                except Exception as e:

                    st.error(
                        "❌ Unexpected error occurred."
                    )

                    st.code(
                        str(e)
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "TCS Healthcare AI • Local AI-powered clinical assistant"
)