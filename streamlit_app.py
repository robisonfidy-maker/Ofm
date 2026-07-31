import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="OF Chat Simulator", page_icon="💬")
st.title("💬 Simulation Chat OnlyFans")

api_key = st.sidebar.text_input("Clé API Groq", type="password")

if not api_key:
    st.info("👈 Veuillez entrer votre clé API Groq dans le panneau latéral pour commencer.")
    st.stop()

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Prompt Système renforcé pour inciter au jeu de rôle réaliste
SYSTEM_PROMPT = (
    "Tu es Thomas, 28 ans, un abonné fidèle et enthousiaste sur OnlyFans. "
    "Tu t'adresses directement au créateur/à la créatrice du compte. "
    "Tu aimes recevoir du contenu exclusif, discuter en privé et réagir aux médias/PPV proposés. "
    "Règles d'incarnation du personnage :\n"
    "- Réponds de manière naturelle, réaliste et dynamique, comme sur une messagerie instantanée (1 à 3 phrases max).\n"
    "- Ne casse JAMAIS le rôle : ne dis jamais que tu es une IA ou une simulation.\n"
    "- Quand tu reçois un Teaser ou un PPV, réagis en fonction de la description et du prix (tu peux être curieux, enthousiaste, ou parfois trouver ça un peu cher et négocier légèrement).\n"
    "- Utilise des emojis occasionnellement et un ton décontracté."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Salut ! Trop content d'être sur ta page, j'adore ce que tu fais 😊"}
    ]

# Affichage de l'historique
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

def call_groq():
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": st.session_state.messages,
        "temperature": 0.8  # Augmente la créativité et le réalisme des réponses
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply = result['choices'][0]['message']['content']
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
    except Exception as e:
        st.error(f"Erreur d'API : {e}")

# Zone d'envoi rapide (Teaser / PPV)
col1, col2 = st.columns(2)

with col1:
    if st.button("📸 Envoyer Teaser (Gratuit)"):
        st.session_state.messages.append({"role": "user", "content": "[📸 APERÇU MEDIA GRATUIT Envoyé]"})
        call_groq()

with col2:
    show_ppv_form = st.checkbox("🔒 Configurer un PPV")

# Formulaire PPV
if show_ppv_form:
    with st.form("ppv_form"):
        st.write("### 🔒 Créer un message PPV")
        ppv_desc = st.text_input("Description du média", "Vidéo exclusive de 3 minutes")
        ppv_price = st.number_input("Prix (€)", min_value=1, max_value=500, value=30, step=5)
        
        submit_ppv = st.form_submit_button("🚀 Envoyer le PPV")
        
        if submit_ppv:
            ppv_message = f"[🔒 MEDIA PPV VERROUILLÉ ({ppv_price}€) - {ppv_desc}]"
            st.session_state.messages.append({"role": "user", "content": ppv_message})
            call_groq()

# Message classique
user_input = st.chat_input("Écrivez votre message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    call_groq()
