from flask import Flask, render_template, request, jsonify, session, send_file
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF for PDF text extraction
import pandas as pd
import matplotlib.pyplot as plt
import io



import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem



import os
import re
import base64
import requests
from functools import lru_cache
from io import BytesIO
from flask import Flask, send_file, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from PIL import Image
from mistralai import Mistral
import imageio
import google.generativeai as genai



from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt



import matplotlib
matplotlib.use('Agg')  # ✅ Use non-GUI backend (no Tkinter)
import matplotlib.pyplot as plt
import pandas as pd
import io, base64, matplotlib.pyplot as plt


import matplotlib
matplotlib.use('Agg')  # ✅ Use non-GUI backend (no Tkinter)
import matplotlib.pyplot as plt
import pandas as pd
import io, base64, matplotlib.pyplot as plt

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_reset_token(email):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt="password-reset-salt")

def verify_reset_token(token, max_age=3600):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=max_age)
    except Exception:
        return None
    return email

from flask import Flask, render_template, request, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

app = Flask(__name__)  # <-- MUST be before using app.config

# SECRET KEY HERE
app.config['SECRET_KEY'] = "your_super_secret_key_here"

# MAIL CONFIG HERE (example)
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="your_email@gmail.com",
    MAIL_PASSWORD="your_app_password"
)

mail = Mail(app)

def generate_reset_token(email):
    s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return s.dumps(email, salt="password-reset-salt")


def verify_reset_token(token, max_age=3600):
    s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=max_age)
    except Exception:
        return None
    return email



from flask import request, redirect, url_for, flash
from flask_mail import Mail, Message

mail = Mail(app)

@app.post("/forgot_password")
def forgot_password():
    email = request.form.get("email")

    # TODO: Check DB if email exists

    token = generate_reset_token(email)
    reset_link = url_for("reset_password", token=token, _external=True)

    msg = Message(
        subject="Reset your Smart Chatbot password",
        recipients=[email],
        body=f"Click to reset your password:\n{reset_link}\n\nIf you didn’t request this, ignore the email."
    )

    mail.send(msg)

    flash("If this email exists, a reset link has been sent.", "info")
    return redirect(url_for("login"))


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return "Reset link expired or invalid", 400

    if request.method == "POST":
        new_password = request.form.get("password")

        # TODO: Update password in DB (hash it!)
        # Example:
        # user = get_user_by_email(email)
        # user.password = hash_password(new_password)
        # db.session.commit()

        return "Password reset successful! You can log in now."

    return render_template("reset_password.html", token=token, email=email)






from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
CORS(app, supports_credentials=True)


# ✅ Function to safely convert markdown-like syntax to HTML
def markdown_to_html(text):
    # Bold: **text**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    # Italic: *text*
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    return text
# Load environment variables
load_dotenv()




os.environ["MISTRAL_API_KEY"] = "IA38lPQ34owIPNRaMFgRXwmOO7UmY3Mr"
api_key = os.environ.get("MISTRAL_API_KEY")
model_name = "pixtral-12b-2409"

if not api_key:
    raise ValueError("API key not found in environment variables")

client = Mistral(api_key=api_key)


# Load API key from environment
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API key not found! Please set GOOGLE_API_KEY in .env")

# Configure Gemini API
genai.configure(api_key=API_KEY)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()



@app.route("/")
def index():
    session.clear()  # clears old chat + pdf
    return render_template("login.html")




# ========================
# Normal Chat + PDF + Image
# ========================
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "")
    language = request.form.get("language", "english")
    file = request.files.get("file")

    pdf_text = ""
    image_obj = None

    # Check if file is uploaded
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Handle PDF file
        if filename.lower().endswith(".pdf"):
            pdf_text = extract_text_from_pdf(filepath)

        # Handle image files (JPG/PNG)
        elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_obj = Image.open(filepath)

    if not user_message and not pdf_text and not image_obj:
        return jsonify({"reply": "Please provide a message or upload a PDF/image!"})

    if "conversation" not in session:
        session["conversation"] = []

    # Combine text and PDF if available
    combined_input = f"{user_message}\n\nPDF Content:\n{pdf_text}" if pdf_text else user_message
    session["conversation"].append(f"User: {combined_input}")
    conversation_text = "\n".join(session["conversation"])

    # Prepare model
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Create the prompt
    prompt = f"""
    Always respond ONLY in {language}.
    If input can be any language, respond only in {language}.
    If PDF or image content is provided, use it to answer the query.
    Conversation so far:
    {conversation_text}
    """

    # Generate based on file type
    if image_obj:
        response = model.generate_content([prompt, image_obj])
    elif pdf_text:
        response = model.generate_content([prompt])
    else:
        response = model.generate_content(prompt)

    bot_reply = response.text.strip() if response and hasattr(response, "text") else "I couldn’t process that file."

    session["conversation"].append(f"Bot: {bot_reply}")
    session["last_reply"] = bot_reply
    # ✅ Save chat to database if logged in
    if "user_id" in session:
        save_chat_history(session["user_id"], user_message, bot_reply, method="text")


    return jsonify({"reply": bot_reply})


# ========================
# Voice Assistant Chat
# ========================
@app.route("/voice", methods=["POST"])
def voice_chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    language = data.get("language", "english")

    # Handle empty input
    if not user_message:
        return jsonify({"reply": "Please say something, I didn’t catch that."})

    # Maintain session-based conversation context
    if "voice_conversation" not in session:
        session["voice_conversation"] = []

    # Append new user message
    session["voice_conversation"].append(f"User: {user_message}")
    conversation_text = "\n".join(session["voice_conversation"])

    # 🔹 Generate reply using Gemini model
    prompt = f"""
    You are a friendly AI voice assistant.
    Always respond ONLY in {language}.
    Conversation so far:
    {conversation_text}
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    bot_reply = response.text.strip()

    # Append bot response to conversation
    session["voice_conversation"].append(f"Bot: {bot_reply}")

    # 🎵 If Kannada language → Generate TTS audio (base64)
    audio_b64 = None
    if language.lower() == "kannada":
        from gtts import gTTS
        from io import BytesIO
        import base64

        tts = gTTS(text=bot_reply, lang="kn")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        audio_b64 = base64.b64encode(buffer.read()).decode("utf-8")

    # ✅ Save conversation to PostgreSQL history
    if "user_id" in session:
        save_chat_history(session["user_id"], user_message, bot_reply, method="voice")

    # Return both text and audio reply
    return jsonify({
        "reply": bot_reply,
        "audio": audio_b64
    })







@app.route("/generate_pdf", methods=["GET"])
def generate_pdf():
    query = session.get("last_query", "No query")
    reply = session.get("last_reply", "No reply")
    language = session.get("last_language", "English")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # ✅ Register a Unicode font for Kannada
    try:
        pdfmetrics.registerFont(TTFont("NotoSansKannada", "NotoSansKannada-Regular.ttf"))
        kannada_font = "NotoSansKannada"
    except:
        # fallback if font file not found
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
        kannada_font = "HeiseiMin-W3"

    # Custom styles
    if language.lower() == "kannada":
        normal_style = ParagraphStyle(
            "KannadaStyle",
            parent=styles["Normal"],
            fontName=kannada_font,
            fontSize=12,
            leading=15,
        )
        heading_style = ParagraphStyle(
            "KannadaHeading",
            parent=styles["Heading1"],
            fontName=kannada_font,
            fontSize=16,
            leading=20,
            alignment=1
        )
    else:
        normal_style = styles["Normal"]
        heading_style = styles["Heading1"]

    elements = []

    # Translated labels
    if language.lower() == "kannada":
        title_text = "💬 ಚಾಟ್‌ಬಾಟ್ ಪ್ರತಿಕ್ರಿಯೆ ವರದಿ"
        query_label = "🔹 ಪ್ರಶ್ನೆ:"
        answer_label = "🔹 ಉತ್ತರ:"
        lang_label = "🔹 ಭಾಷೆ:"
    else:
        title_text = "💬 Chatbot Response Report"
        query_label = "🔹 Query:"
        answer_label = "🔹 Answer:"
        lang_label = "🔹 Language:"

    # Add content
    elements.append(Paragraph(title_text, heading_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>{query_label}</b> {query}", normal_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"<b>{lang_label}</b> {language}", normal_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"<b>{answer_label}</b>", normal_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(reply, normal_style))

    doc.build(elements)

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="chat_response.pdf",
        mimetype="application/pdf",
    )




@app.route("/get_youtube", methods=["POST"])
def get_youtube():
    data = request.json
    query = data.get("query", "")
    language = data.get("language", "English")

    if not query:
        return jsonify({"link": "https://www.youtube.com"})

    search_query = f"{query} {language}"
    yt_link = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"

    return jsonify({"link": yt_link})




@app.route("/get_flowchart", methods=["POST"])
def get_flowchart():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"status": "error", "message": "No query provided"})

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    The user asked: "{query}".
    1. If this query can be represented as a flowchart (like steps, process, decision-making), generate a Mermaid.js flowchart definition only.
    2. Do NOT add explanations, do NOT wrap in ```mermaid``` or ``` code blocks.
    3. If it's not suitable for a flowchart, just reply with: NOT_FLOWCHART
    Example output for flowchart:
    graph TD
        A[Start] --> B[Step 1]
        B --> C[Step 2]
        C --> D[End]
    """

    response = model.generate_content(prompt)
    bot_reply = response.text.strip()

    # 🔹 Clean output: remove markdown fences if Gemini adds them
    bot_reply = bot_reply.replace("```mermaid", "").replace("```", "").strip()

    if "NOT_FLOWCHART" in bot_reply:
        return jsonify({"status": "not_flowchart", "message": "This query is not related to a flowchart."})
    
    return jsonify({"status": "ok", "flowchart": bot_reply})


@app.route("/generate_graph", methods=["POST"])
def generate_graph():
    # Get form data
    file = request.files.get("file")
    chart_type = request.form.get("chart_type", "bar")
    sort_order = request.form.get("sort_order", "none")
    range_min = request.form.get("range_min")
    range_max = request.form.get("range_max")

    # ✅ If file uploaded, read and save to session
    if file:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        else:
            return {"error": "Unsupported file type"}, 400

        session["data"] = df.to_json()  # store dataframe
    else:
        # ✅ Use last uploaded file from session
        if "data" not in session:
            return {"error": "No file uploaded yet"}, 400
        df = pd.read_json(io.StringIO(session["data"]))

    # Select first two columns
    x_col = df.columns[0]
    y_col = df.columns[1]

    # ✅ Apply range filter
    if pd.api.types.is_numeric_dtype(df[y_col]):
        if range_min:
            try:
                range_min = float(range_min)
                df = df[df[y_col] >= range_min]
            except ValueError:
                pass
        if range_max:
            try:
                range_max = float(range_max)
                df = df[df[y_col] <= float(range_max)]
            except ValueError:
                pass

    # ✅ Apply sorting
    if sort_order == "asc":
        df = df.sort_values(by=y_col, ascending=True)
    elif sort_order == "desc":
        df = df.sort_values(by=y_col, ascending=False)

    # ✅ Generate chart
    plt.figure(figsize=(6, 4))
    if chart_type == "bar":
        plt.bar(df[x_col], df[y_col], color="skyblue")
    elif chart_type == "pie":
        plt.pie(df[y_col], labels=df[x_col], autopct="%1.1f%%")
    elif chart_type == "line":
        plt.plot(df[x_col], df[y_col], marker="o", color="green")

    plt.title(f"{chart_type.capitalize()} Chart")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # ✅ Convert to base64
    img = io.BytesIO()
    plt.savefig(img, format="png", transparent=True)
    img.seek(0)
    chart_data = base64.b64encode(img.read()).decode()
    plt.close()

    return {"chart": chart_data}


@app.route("/generate_visual", methods=["POST"])
def generate_visual():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Example using Stability AI (you can replace with OpenAI or any T2I API)
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image",
            headers={"Authorization": "Bearer YOUR_API_KEY"},
            json={
                "prompt": user_query,
                "width": 512,
                "height": 512,
                "samples": 1
            }
        )
        data = response.json()
        img_base64 = data["artifacts"][0]["base64"]  # base64 image

        return jsonify({"visual": img_base64})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/get_summary", methods=["POST"])
def get_summary():
    data = request.json
    query = data.get("query", "")
    language = data.get("language", "English")   # ✅ FIXED

    pdf_text = session.get("last_pdf", "")

    if pdf_text and query:
        content_to_summarize = f"User question: {query}\n\nPDF Content:\n{pdf_text}"
    elif pdf_text:
        content_to_summarize = pdf_text
    elif query:
        content_to_summarize = query
    else:
        return jsonify({"status": "error", "message": "No query or PDF content found"})

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Provide a very short summary (max 3 lines) in {language}.
    Focus on the key points only.
    No markdown, no bullets, plain text only.

    Content:
    {content_to_summarize}
    """

    response = model.generate_content(prompt)
    summary = response.text.strip()

    return jsonify({"status": "ok", "summary": summary})





@app.route("/voice")
def voice():
    session.clear()
    return render_template("voice.html")


@app.route('/process_image_and_text', methods=['POST'])
def process_image_and_text():
    data = request.json
    image_data = data.get('image')
    text_prompt = data.get('text', '')
    language = data.get('language', 'en')  # default English

    if not text_prompt and not image_data:
        return jsonify({'error': 'Missing both text and image'}), 400

    try:
        # Initialize session if not exists
        if "chat_history" not in session:
            session["chat_history"] = []

        content = []

        # --- Handle text input ---
        if text_prompt:
            lang_instruction = "" if language == "en" else f"Please respond completely in {language}."
            content.append({
                "type": "text",
                "text": f"{lang_instruction}\nUser said: {text_prompt}"
            })

        # --- Handle image input ---
        if image_data and image_data.strip() != '':
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image_file = BytesIO(image_bytes)
            image_b64 = base64.b64encode(image_file.getvalue()).decode('utf-8')
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
            })
        else:
            # Reuse last image if exists
            if "last_image" in session:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": session["last_image"]}
                })

        if image_data:
            session["last_image"] = image_data

        # --- Add current user message to session ---
        session["chat_history"].append({"role": "user", "content": content})

        # --- Prepare model messages ---
        messages_for_model = [
            {"role": "system", "content": (
                "You are a helpful AI assistant. Use the previous conversation to answer questions. "
                "If a question is unrelated to previous context, answer independently. "
                "Do not invent unrelated details or get distracted by minor things."
                "Respect the user-selected language."
            )}
        ] + session["chat_history"]

        # --- Call AI model ---
        response = client.chat.complete(
            model=model_name,
            messages=messages_for_model
        )

        bot_reply = response.choices[0].message.content

        # --- Translate if needed ---
        if language != 'en':
            translation_prompt = f"Translate to {language}: {bot_reply}"
            translate_response = client.chat.complete(
                model=model_name,
                messages=[{"role": "user", "content": translation_prompt}]
            )
            bot_reply = translate_response.choices[0].message.content

        # --- Save assistant reply ---
        session["chat_history"].append({"role": "assistant", "content": bot_reply})
        session.modified = True

        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Error processing image and text: {e}")
        return jsonify({"error": str(e)}), 500



@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    return jsonify({"status": "session reset"})



@app.route("/liveVideo")
def liveVideo():
    session.clear()
    return render_template("video.html")





@app.route("/ollama_chat", methods=["GET"])
def ollama_chat():
    return render_template("ollama_chat.html")



@app.route("/ollama_api", methods=["POST"])
def ollama_api():
    user_message = request.json.get("message", "").strip()
    language = request.json.get("language", "english").lower()

    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    # --------------------------------------
    # FIX: Reset chat history when language changes
    # --------------------------------------
    if "last_lang" in session and session["last_lang"] != language:
        session["chat_history"] = []  # Clear old history
    session["last_lang"] = language   # Save new language

    # -------------------------------
    # 1. Initialize chat history
    # -------------------------------
    if "chat_history" not in session:
        session["chat_history"] = []

    session["chat_history"].append({"role": "user", "content": user_message})

    session["chat_history"] = session["chat_history"][-10:]

    # -------------------------------
    # 2. System Prompt
    # -------------------------------
    if language == "kannada":
        system_prompt = {
            "role": "system",
            "content": (
                "ನೀವು ಸಹಾಯಕ AI. ಯಾವಾಗಲೂ ಶುದ್ಧ ಮತ್ತು ಸಹಜ ಕನ್ನಡದಲ್ಲಿ ಮಾತ್ರ ಉತ್ತರಿಸಿ. "
                "ವಾಕ್ಯಗಳನ್ನು ಸ್ಪಷ್ಟವಾಗಿ, ವಿವರವಾಗಿ, ಸುಲಭವಾಗಿ ಅರ್ಥವಾಗುವಂತೆ ಬರೆಯಿರಿ. "
                "ಬಳಕೆದಾರರ ಪ್ರಶ್ನೆಗೆ ಉದಾಹರಣೆಗಳು, ಅರ್ಥವ್ಯಾಖ್ಯಾನ ಮತ್ತು ವಿವರವಾದ ವಿವರಣೆಗಳನ್ನು ಸೇರಿಸಿ."
            ),
        }
    else:
        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful assistant who gives long, detailed, natural English explanations. "
                "Use context from previous messages to generate rich, complete responses."
            ),
        }

    messages = [system_prompt] + session["chat_history"]

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2",
                "messages": messages,
                "stream": False,
                "options": { "num_predict": 8000, "temperature": 0.8 },
            },
            timeout=300
        )

        data = response.json()

        reply = (
            data.get("message", {}).get("content")
            or data.get("response")
            or "⚠️ No response from model."
        ).strip()

        session["chat_history"].append({"role": "assistant", "content": reply})

        if "user_id" in session:
            save_chat_history(session["user_id"], user_message, reply, method="ollama")

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})


@app.route("/flowchart_api", methods=["POST"])
def flowchart_api():
    query = request.json.get("query", "")

    final_prompt = f"""
You are a flowchart generator.
User question: {query}

Reply ONLY with a valid Mermaid flowchart code block.
Do not add explanations, just the Mermaid diagram.
Example:
```mermaid
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
"""
    

# PostgreSQL connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="chatbot_system",  # 🔹 replace with your database name
        user="postgres",
        password="4ai22cd011"        # 🔹 replace with your actual password
    )
    return conn


@app.route("/register_page")
def register_page():
    if "user_id" in session:
        return redirect(url_for("register"))
    return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate
        if not username or not email or not password:
            return render_template("register.html", error="All fields are required")

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, mail, password) VALUES (%s, %s, %s)",
                (username, email, hashed.decode("utf-8")),
            )
            conn.commit()
            # ✅ Redirect user to login page after success
            return redirect(url_for("login_page"))
        except Exception as e:
            conn.rollback()
            return render_template("register.html", error=str(e))
        finally:
            cur.close()
            conn.close()
    return render_template("register.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="Please fill all fields")

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return render_template("login.html", error="User not found")

        stored_password = user["password"]

        if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))  # ✅ fixed redirect
        else:
            return render_template("login.html", error="Incorrect password")

    return render_template("login.html")

@app.route("/index")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    return render_template("index.html", username=username)


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"status": "ok", "message": "Logged out"})










def save_chat_history(user_id, user_message, bot_reply, method="text"):
    conn = get_db_connection()
    cur = conn.cursor()
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id

    cur.execute("""
        INSERT INTO chat_history (user_id, session_id, user_message, bot_reply, method)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, session_id, user_message, bot_reply, method))
    conn.commit()
    cur.close()
    conn.close()






import uuid
from flask import Flask, session, jsonify, request

@app.route("/new_chat", methods=["POST"])
def new_chat():
    new_id = str(uuid.uuid4())
    session["session_id"] = new_id  # store in Flask session
    return jsonify({"status": "ok", "session_id": new_id})


@app.route("/get_sessions", methods=["GET"])
def get_sessions():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT session_id, MIN(timestamp) AS created_at
        FROM chat_history
        WHERE user_id = %s
        GROUP BY session_id
        ORDER BY created_at DESC
    """, (user_id,))

    sessions = [{"session_id": row[0], "created_at": row[1].isoformat()} 
                for row in cur.fetchall()]
    conn.close()
    return jsonify({"status": "ok", "sessions": sessions})

@app.route("/get_history/<session_id>", methods=["GET"])
def get_history(session_id):
    user_id = session.get("user_id")
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_message, bot_reply, timestamp 
        FROM chat_history
        WHERE session_id = %s AND user_id = %s
        ORDER BY timestamp ASC
    """, (session_id, user_id))

    chats = [{"user_message": u, "bot_reply": b} 
             for (u, b, _) in cur.fetchall()]

    conn.close()
    return jsonify({"status": "ok", "history": chats})


if __name__ == "__main__":
    app.run(debug=True)
