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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tu es Thomas, un abonné OnlyFans. Réponds en 1 à 2 phrases courtes."},
        {"role": "assistant", "content": "Salut ! Je viens de m'abonner à ta page 😊"}
    ]

# Affichage de l'historique de discussion
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

def call_groq():
    payload = {"model": "llama-3.3-70b-versatile", "messages": st.session_state.messages}
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

# Formulaire d'envoi de PPV personnalisé
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

# Saisie de texte libre
user_input = st.chat_input("Écrivez votre message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    call_groq()
