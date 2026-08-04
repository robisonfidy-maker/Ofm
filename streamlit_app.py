import streamlit as st
import json
import urllib.request

# Configuration de la page
st.set_page_config(page_title="Simulator by Kris", page_icon="💬", layout="centered")

# CSS Personnalisé : Thème Violet Clair + Alignement des bulles (Gauche / Droite)
st.markdown("""
<style>
    /* Fond général violet clair */
    .stApp {
        background-color: #F3E8FF;
        color: #2D3748;
    }
    
    /* Titres et en-têtes en violet foncé */
    h1, h2, h3 {
        color: #5B21B6 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
    }
    
    /* Sous-titres et textes d'information */
    .stCaption, p {
        color: #4C1D95;
    }
    
    /* Boutons personnalisés en violet vif */
    div.stButton > button {
        background-color: #7C3AED;
        color: #ffffff;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #6D28D9;
        color: #ffffff;
        box-shadow: 0px 4px 12px rgba(124, 58, 237, 0.4);
    }
    
    /* Alignement des bulles de chat */
    /* Messages de l'assistant (Abonné) -> Alignés à GAUCHE */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {
        background-color: #FFFFFF;
        border-radius: 15px 15px 15px 0px;
        border: 1px solid #DDD6FE;
        margin-right: auto;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Messages de l'utilisateur (Créateur) -> Alignés à DROITE */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background-color: #7C3AED;
        color: #FFFFFF !important;
        border-radius: 15px 15px 0px 15px;
        margin-left: auto;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }

    /* Couleur du texte dans la bulle de l'utilisateur */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) p {
        color: #FFFFFF !important;
    }
    
    /* Formulaire PPV */
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 2px solid #7C3AED;
        border-radius: 15px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ÉTAPE 1 : ÉCRAN DE VÉRIFICATION DE L'ÂGE
# ---------------------------------------------------------
if "age_verified" not in st.session_state:
    st.session_state.age_verified = False

if not st.session_state.age_verified:
    st.title("🔞 TSINDRIO POONGANY IO 18 IO LOU")
    st.write("---")
    st.warning("Ce simulateur est destiné à un usage professionnel de gestion et de formation au chat d'agence (OFM).")
    
    st.write("### Conditions d'accès :")
    check_age = st.checkbox("J'atteste avoir au moins 18 ans et j'accepte d'entrer dans l'espace de simulation.")
    
    if st.button("Entrer sur la plateforme 🚀"):
        if check_age:
            st.session_state.age_verified = True
            st.rerun()
        else:
            st.error("Vous devez cocher la case pour confirmer votre majorité avant de continuer.")
            
    st.stop()

# ---------------------------------------------------------
# ÉTAPE 2 : APPLICATION PRINCIPALE
# ---------------------------------------------------------

st.title("💬 Simulator by Kris")
st.caption("Espace de simulation de chat et vente de PPV")

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
    "Tu es Thomas, un abonné réel sur la plateforme privée d'une créatrice de contenu. "
    "Tu réagis de manière totalement naturelle, spontanée et réaliste comme un vrai fan.\n\n"
    "Règles strictes de comportement :\n"
    "- Parle de façon décontractée, directe et amicale (1 à 2 phrases courtes maximum).\n"
    "- Si l'utilisateur t'envoie un message contenant '[🔒 MEDIA PPV VERROUILLÉ]', cela signifie qu'il te propose une vidéo ou photo payante.\n"
    "- Évalue le prix et le contenu de manière naturelle : si le prix est raisonnable et le contenu attractif, tu peux décider de l'acheter.\n"
    "- SI ET SEULEMENT SI tu décides d'acheter ce PPV, commence IMPÉRATIVEMENT ta réponse par le mot exact : BUY_PPV.\n"
    "  Exemple : 'BUY_PPV Carrément chaud ! Je le prends direct.'\n"
    "- Si tu n'achètes pas (trop cher, pas intéressé, ou simple discussion), NE METS SURTOUT PAS le mot BUY_PPV. Négocie ou discute normalement.\n"
    "- Ne casse jamais ton rôle d'abonné."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Salut ! Trop content d'être sur ta page privée 😉"}
    ]

if "last_sent_is_ppv" not in st.session_state:
    st.session_state.last_sent_is_ppv = False

# Affichage de l'historique du chat (Abonné à gauche, Créateur à droite)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

def call_openrouter():
    payload = {
        "model": "gryphe/mythomax-l2-13b",
        "messages": st.session_state.messages,
        "temperature": 0.85
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply = result['choices'][0]['message']['content']
            
            # L'affichage vert est conditionné : il faut qu'un PPV ait été envoyé ET que l'IA réponde BUY_PPV
            if st.session_state.last_sent_is_ppv and "BUY_PPV" in reply:
                reply_clean = reply.replace("BUY_PPV", "").strip()
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f":green[✅ **PPV DÉBLOQUÉ PAR L'ABONNÉ**]\n\n{reply_clean}"
                })
            else:
                reply_clean = reply.replace("BUY_PPV", "").strip()
                st.session_state.messages.append({"role": "assistant", "content": reply_clean})
            
            # Réinitialisation de l'indicateur PPV après la réponse
            st.session_state.last_sent_is_ppv = False
            st.rerun()
    except Exception as e:
        st.error(f"Erreur d'API : {e}")

# Actions rapides
col1, col2 = st.columns(2)

with col1:
    if st.button("📸 Teaser Gratuit"):
        st.session_state.last_sent_is_ppv = False
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
            st.session_state.last_sent_is_ppv = True
            ppv_message = f"[🔒 MEDIA PPV VERROUILLÉ ({ppv_price}€) - Description: {ppv_desc}]"
            st.session_state.messages.append({"role": "user", "content": ppv_message})
            call_openrouter()

user_input = st.chat_input("Écrivez votre message...")
if user_input:
    st.session_state.last_sent_is_ppv = False
    st.session_state.messages.append({"role": "user", "content": user_input})
    call_openrouter()
