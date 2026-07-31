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

SYSTEM_PROMPT = (
    "Tu es Thomas, un abonné enthousiaste sur une plateforme de contenu privé. "
    "Tu discutes avec ta créatrice préférée. "
    "Lorsqu'elle t'envoie un média PPV (verrouillé avec un prix), tu dois réagir naturellement.\n"
    "SI TU DÉCIDES D'ACHETER LE MÉDIA, commence OBLIGATOIREMENT ton message par le code exact : [ACHAT_PPV]. "
    "Exemple : '[ACHAT_PPV] Trop bien, je prends ! J'ai hâte de regarder.'\n"
    "Si tu trouves le prix trop cher ou que tu n'es pas intéressé, me mets PAS le code [ACHAT_PPV] et négocie ou décline gentiment.\n"
    "Règles :\n"
    "- Ne fais jamais référence à du contenu sexuel explicite ou de la nudité (reste sur des coulisses, vlogs, vêtement stylé, etc.).\n"
    "- Ne casse jamais ton rôle d'abonné (répons en 1 à 2 phrases max)."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Salut ! Trop content d'être sur ta page, j'adore ce que tu fais 😊"}
    ]

# Affichage de l'historique de discussion
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

def call_groq():
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": st.session_state.messages,
        "temperature": 0.7
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply = result['choices'][0]['message']['content']
            
            # Vérification si Thomas achète le PPV
            if "[ACHAT_PPV]" in reply:
                reply_clean = reply.replace("[ACHAT_PPV]", "").strip()
                # Message de confirmation d'achat en vert
                st.session_state.messages.append({"role": "assistant", "content": f":green[✅ **PPV DÉBLOQUÉ PAR L'ABONNÉ**]\n\n{reply_clean}"})
            else:
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
        ppv_desc = st.text_input("Description du média", "Coulisses exclusives de 3 minutes")
        ppv_price = st.number_input("Prix (€)", min_value=1, max_value=500, value=15, step=5)
        
        submit_ppv = st.form_submit_button("🚀 Envoyer le PPV")
        
        if submit_ppv:
            ppv_message = f"[🔒 MEDIA PPV VERROUILLÉ ({ppv_price}€) - Description: {ppv_desc}]"
            st.session_state.messages.append({"role": "user", "content": ppv_message})
            call_groq()

# Saisie de texte libre
user_input = st.chat_input("Écrivez votre message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    call_groq()
