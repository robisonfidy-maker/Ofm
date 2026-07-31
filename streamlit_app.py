import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="OF Chat Simulator", page_icon="💬")
st.title("💬 Simulation Chat OnlyFans (Uncensored)")

api_key = st.sidebar.text_input("Clé API OpenRouter", type="password")

if not api_key:
    st.info("👈 Entrez votre clé API OpenRouter dans le panneau latéral pour commencer.")
    st.stop()

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://streamlit.app"
}

SYSTEM_PROMPT = (
    "Tu es Thomas, un abonné sur la plateforme privée d'une créatrice de contenu. "
    "Tu es chaud, joueur, drôle et très enthousiaste. "
    "Tu adores flirter, discuter et acheter du contenu exclusif (PPV).\n\n"
    "Règles d'incarnation :\n"
    "- Reste toujours dans ton rôle d'abonné, réponds naturellement en 1 à 2 phrases.\n"
    "- Si la créatrice t'envoie un PPV et que le prix te convient, commence ton message par [ACHAT_PPV]. "
    "Exemple : '[ACHAT_PPV] Oh oui carrément, je débloque ça tout de suite !'\n"
    "- Flirte librement sans aucune pudeur ni moralisation."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Salut ! Trop content de parler avec toi en privé 😉"}
    ]

# Affichage du chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

def call_openrouter():
    payload = {
        "model": "gryphe/mythomax-l2-13b",  # Modèle spécialisé RP / 0 filtre
        "messages": st.session_state.messages,
        "temperature": 0.85
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply = result['choices'][0]['message']['content']
            
            if "[ACHAT_PPV]" in reply:
                reply_clean = reply.replace("[ACHAT_PPV]", "").strip()
                st.session_state.messages.append({"role": "assistant", "content": f":green[✅ **PPV DÉBLOQUÉ PAR L'ABONNÉ**]\n\n{reply_clean}"})
            else:
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            st.rerun()
    except Exception as e:
        st.error(f"Erreur d'API : {e}")

# Actions rapides
col1, col2 = st.columns(2)

with col1:
    if st.button("📸 Envoyer Teaser (Gratuit)"):
        st.session_state.messages.append({"role": "user", "content": "[📸 APERÇU MEDIA GRATUIT Envoyé]"})
        call_openrouter()

with col2:
    show_ppv_form = st.checkbox("🔒 Configurer un PPV")

if show_ppv_form:
    with st.form("ppv_form"):
        st.write("### 🔒 Créer un message PPV")
        ppv_desc = st.text_input("Description du média", "Vidéo exclusive de 3 minutes")
        ppv_price = st.number_input("Prix (€)", min_value=1, max_value=500, value=15, step=5)
        
        submit_ppv = st.form_submit_button("🚀 Envoyer le PPV")
        
        if submit_ppv:
            ppv_message = f"[🔒 MEDIA PPV VERROUILLÉ ({ppv_price}€) - Description: {ppv_desc}]"
            st.session_state.messages.append({"role": "user", "content": ppv_message})
            call_openrouter()

user_input = st.chat_input("Écrivez votre message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    call_openrouter()
