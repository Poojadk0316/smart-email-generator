import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartMail AI",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f7f5ff;
    }

    /* Main container */
    .main .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main title */
    .main-title {
        text-align: center;
        color: #4c1d95;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    /* Subtitle */
    .main-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Input labels */
    label {
        font-weight: 600 !important;
        color: #334155 !important;
    }

    /* Input boxes */
    div[data-baseweb="input"] {
        border-radius: 12px !important;
    }

    div[data-baseweb="textarea"] {
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }

    /* Generate button */
    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 13px;
        border: none;
        background: linear-gradient(
            90deg,
            #6d28d9,
            #7c3aed
        );
        color: white;
        font-size: 17px;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(109, 40, 217, 0.25);
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #5b21b6,
            #6d28d9
        );
        color: white;
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        height: 48px;
        border-radius: 12px;
        font-weight: 650;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 40px;
        padding: 20px;
    }

    /* Mobile */
    @media (max-width: 768px) {

        .main-title {
            font-size: 32px;
        }

        .main-subtitle {
            font-size: 15px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✉️ AI-Powered Smart Email Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Create professional and personalized emails with the help of Generative AI.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FEATURE SECTION
# NO HTML CARDS USED
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("## 🧠")

    st.subheader("AI-Powered Writing")

    st.write(
        "Generate natural and professional emails "
        "using Generative AI."
    )


with col2:

    st.markdown("## 🎯")

    st.subheader("Personalized")

    st.write(
        "Customize your email according to "
        "purpose, type and tone."
    )


with col3:

    st.markdown("## ⚡")

    st.subheader("Fast & Simple")

    st.write(
        "Create a complete professional email "
        "within seconds."
    )


# ============================================================
# INFORMATION MESSAGE
# ============================================================

st.write("")

st.info(
    "💡 Enter your email requirements below. "
    "The AI will transform them into a clear and professional email."
)


# ============================================================
# EMAIL DETAILS
# ============================================================

st.markdown("## 📝 Email Details")


# ============================================================
# RECIPIENT AND SENDER
# ============================================================

col1, col2 = st.columns(2)

with col1:

    recipient = st.text_input(
        "Recipient",
        placeholder="Example: HR Manager"
    )


with col2:

    sender = st.text_input(
        "Sender Name",
        placeholder="Example: Pooja"
    )


# ============================================================
# EMAIL TYPE AND TONE
# ============================================================

col1, col2 = st.columns(2)

with col1:

    email_type = st.selectbox(
        "Email Type",
        [
            "Internship Request",
            "Job Application",
            "Leave Request",
            "College Request",
            "Meeting Request",
            "Complaint",
            "Follow-up",
            "Thank You",
            "General"
        ]
    )


with col2:

    tone = st.selectbox(
        "Email Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Polite",
            "Concise"
        ]
    )


# ============================================================
# EMAIL PURPOSE
# ============================================================

purpose = st.text_area(
    "Email Purpose",
    placeholder=(
        "Example: Request for an internship opportunity "
        "in software development."
    ),
    height=110
)


# ============================================================
# KEY POINTS
# ============================================================

key_points = st.text_area(
    "Key Points",
    placeholder=(
        "Example:\n"
        "Third-year Computer Science Engineering student\n"
        "Experience in Python\n"
        "Interested in software development"
    ),
    height=140
)


# ============================================================
# ADDITIONAL INSTRUCTIONS
# ============================================================

additional_instructions = st.text_area(
    "Additional Instructions (Optional)",
    placeholder=(
        "Example: Keep the email short, polite and professional."
    ),
    height=100
)


# ============================================================
# GEMINI EMAIL GENERATION FUNCTION
# ============================================================

def generate_email(prompt):

    primary_model = os.getenv(
        "GEMINI_PRIMARY_MODEL",
        "gemini-3.8-flash"
    )

    fallback_model = os.getenv(
        "GEMINI_FALLBACK_MODEL",
        "gemini-3.5-flash-lite"
    )

    max_retries = 3

    # --------------------------------------------------------
    # PRIMARY MODEL
    # --------------------------------------------------------

    for attempt in range(max_retries):

        try:

            response = client.interactions.create(
                model=primary_model,
                input=prompt
            )

            return response.output_text, primary_model

        except Exception as error:

            error_message = str(error).lower()

            temporary_error = (
                "503" in error_message
                or "service_unavailable" in error_message
                or "high demand" in error_message
                or "temporarily" in error_message
                or "timeout" in error_message
                or "rate limit" in error_message
                or "429" in error_message
            )

            if temporary_error:

                if attempt < max_retries - 1:

                    wait_time = 2 ** (attempt + 1)

                    time.sleep(wait_time)

                else:

                    break

            else:

                raise error


    # --------------------------------------------------------
    # FALLBACK MODEL
    # --------------------------------------------------------

    try:

        response = client.interactions.create(
            model=fallback_model,
            input=prompt
        )

        return response.output_text, fallback_model

    except Exception as fallback_error:

        raise RuntimeError(
            "The primary and fallback Gemini models "
            "were unable to generate the email.\n\n"
            f"Primary model: {primary_model}\n"
            f"Fallback model: {fallback_model}\n\n"
            f"Error: {fallback_error}"
        )


# ============================================================
# GENERATE BUTTON
# ============================================================

st.write("")

generate_clicked = st.button(
    "✨ Generate Professional Email",
    type="primary",
    use_container_width=True
)


# ============================================================
# GENERATION PROCESS
# ============================================================

if generate_clicked:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not api_key:

        st.error(
            "❌ Gemini API key was not found."
        )

        st.info(
            "Please check your .env file."
        )

    elif client is None:

        st.error(
            "❌ Gemini client could not be initialized."
        )

    elif not recipient.strip():

        st.warning(
            "⚠️ Please enter the recipient."
        )

    elif not purpose.strip():

        st.warning(
            "⚠️ Please enter the email purpose."
        )

    elif not key_points.strip():

        st.warning(
            "⚠️ Please enter the key points."
        )

    else:

        # ----------------------------------------------------
        # PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are a professional email writing assistant.

Create a clear, natural, professional and well-structured email
based only on the information provided by the user.

Recipient:
{recipient}

Sender:
{sender}

Email Type:
{email_type}

Tone:
{tone}

Purpose:
{purpose}

Key Points:
{key_points}

Additional Instructions:
{additional_instructions}

Requirements:

1. Generate a suitable subject line.
2. Start with an appropriate greeting.
3. Clearly communicate the purpose of the email.
4. Include all important key points.
5. Follow the requested tone.
6. Use grammatically correct English.
7. Keep the email natural and easy to understand.
8. Do not invent personal information.
9. Do not add facts that were not provided.
10. End with an appropriate professional closing.
11. Return only the completed email.

Format:

Subject: <subject>

<email body>
"""


        # ----------------------------------------------------
        # GENERATE EMAIL
        # ----------------------------------------------------

        try:

            with st.spinner(
                "✨ AI is writing your email..."
            ):

                generated_email, model_used = generate_email(
                    prompt
                )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            st.success(
                "✅ Email generated successfully!"
            )


            # ------------------------------------------------
            # OUTPUT
            # ------------------------------------------------

            st.markdown("## 📨 Generated Email")


            # ------------------------------------------------
            # MODEL INFORMATION
            # ------------------------------------------------

            primary_model = os.getenv(
                "GEMINI_PRIMARY_MODEL",
                "gemini-3.8-flash"
            )

            if model_used == primary_model:

                st.caption(
                    "Generated using the primary Gemini model."
                )

            else:

                st.caption(
                    "The primary model was unavailable. "
                    "A fallback Gemini model was used."
                )


            # ------------------------------------------------
            # EDITABLE EMAIL
            # ------------------------------------------------

            edited_email = st.text_area(
                "Review and edit your email:",
                value=generated_email,
                height=420
            )


            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            st.download_button(
                label="⬇️ Download Email",
                data=edited_email,
                file_name="generated_email.txt",
                mime="text/plain",
                use_container_width=True
            )


        # ----------------------------------------------------
        # ERROR HANDLING
        # ----------------------------------------------------

        except Exception as error:

            st.error(
                "❌ Unable to generate the email."
            )

            st.error(
                f"Error details: {error}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    '✉️ SmartMail AI<br>'
    'AI-Powered Smart Email Generator<br>'
    'Built with Python • Streamlit • Google Gemini'
    '</div>',
    unsafe_allow_html=True
)