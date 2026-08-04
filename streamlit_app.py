import streamlit as st
import json
import urllib.request
import random

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
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {
        background-color: #FFFFFF;
        border-radius: 15px 15px 15px 0px;
        border: 1px solid #DDD6FE;
        margin-right: auto;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background-color: #7C3AED;
        color: #FFFFFF !important;
        border-radius: 15px 15px 0px 15px;
        margin-left: auto;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }

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
# ÉTAPE 2 : GENERATION DE L'IDENTITE ET PSYCHOLOGIE DU SUB
# ---------------------------------------------------------
if "sub_identity" not in st.session_state:
    prenoms = ["Thomas", "Alexandre", "Julien", "Maxime", "Lucas", "Antoine", "Mathieu", "Romain"]
    villes = ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Toulouse", "Nantes", "Nice"]
    metiers = ["Ingénieur", "Commercial", "Développeur", "Électricien", "Comptable", "Architecte", "Mécanicien"]

    st.session_state.sub_identity = {
        "prenom": random.choice(prenoms),
        "age": f"{random.randint(22, 45)} ans",
        "ville": random.choice(villes),
        "metier": random.choice(metiers)
    }

if "kyc_discovered" not in st.session_state:
    st.session_state.kyc_discovered = {
        "prenom": None,
        "age": None,
        "ville": None,
        "metier": None
    }

# ---------------------------------------------------------
# ÉTAPE 3 : APPLICATION PRINCIPALE & BARRE KYC
# ---------------------------------------------------------

st.title("💬 Simulator by Kris")
st.caption("Espace de simulation de chat et vente de PPV (Funnel OFM)")

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

# Calcul de la progression du KYC
discovered = st.session_state.kyc_discovered
score_kyc = sum(1 for val in discovered.values() if val is not None) * 25

st.markdown("### 📊 Progression KYC")
st.progress(score_kyc / 100)
st.write(f"**Complété à : {score_kyc}%**")

# Affichage des informations découvertes
cols = st.columns(4)
cols[0].write(f"👤 **Prénom:** {discovered['prenom'] if discovered['prenom'] else '❓'}")
cols[1].write(f"🎂 **Âge:** {discovered['age'] if discovered['age'] else '❓'}")
cols[2].write(f"📍 **Ville:** {discovered['ville'] if discovered['ville'] else '❓'}")
cols[3].write(f"💼 **Métier:** {discovered['metier'] if discovered['metier'] else '❓'}")
st.write("---")

sub = st.session_state.sub_identity

SYSTEM_PROMPT = (
    f"Tu es un abonné masculin sur la plateforme OnlyFans d'une créatrice de contenu.\n"
    f"Ton identité secrète :\n"
    f"- Prénom : {sub['prenom']}\n"
    f"- Âge : {sub['age']}\n"
    f"- Ville : {sub['ville']}\n"
    f"- Métier : {sub['metier']}\n\n"
    "PSYCHOLOGIE & DIRECTIVES DE CONVERSATION (FUNNEL ONLYFANS) :\n"
    "1. STYLE DE RÉPONSE : Sois TRÈS NATUREL. Réponds en 1 seule phrase (maximum 2 phrases courtes). Utlise un ton informel de mec (flirt, emojis occasionnels, langage SMS léger).\n"
    "2. ÉTAPES DU CHAT :\n"
    "   - Phase 1 (Faire connaissance) : Au début, tu es amical mais réservé. Ne donne PAS tes infos persos d'un coup. Donne ton prénom, âge, ville ou métier SEULEMENT si la créatrice te le demande gentiment.\n"
    "   - Phase 2 (Flirt / Connexion) : Si la créatrice te fait des compliments ou s'intéresse à toi, commence à flirter subtilement et montre de l'enthousiasme.\n"
    "   - Phase 3 (Sexualisation) : Si la discussion devient chaude/intime, tu deviens excité et réceptif.\n"
    "3. RÈGLE DES PPV (Achats) :\n"
    "   - Si la créatrice t'envoie un PPV verrouillé '[🔒 MEDIA PPV VERROUILLÉ]' trop tôt (alors que la discussion vient de commencer ou sans sexualisation), REFUSE gentiment ou hésite ('C'est un peu tôt non ?', 'Haha tu vas vite').\n"
    "   - Si la discussion est déjà bien chaude et qu'elle t'a chauffé, tu ACHÈTES la vidéo/photo avec grand plaisir.\n"
    "   - SI TU ACHÈTES LE PPV : Commence OBLIGATOIREMENT ton message par le mot exact : BUY_PPV.\n"
    "     Exemple : 'BUY_PPV Trop hâte de voir ça, je débloque direct ! 🔥'\n"
    "   - SI TU REFUSES OU NÉGOCIES : Ne mets SURTOUT PAS le mot BUY_PPV."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Coucou ! Trop content que tu me répondes 😉"}
    ]

if "last_sent_is_ppv" not in st.session_state:
    st.session_state.last_sent_is_ppv = False

# Affichage du chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

def update_kyc_automatically(reply):
    """Met à jour le KYC quand l'abonné donne une info en répondant"""
    reply_lower = reply.lower()
    sub_info = st.session_state.sub_identity
    
    # Prénom
    if sub_info["prenom"].lower() in reply_lower:
        st.session_state.kyc_discovered["prenom"] = sub_info["prenom"]
        
    # Âge
    age_num = sub_info["age"].split()[0]
    if age_num in reply_lower:
        st.session_state.kyc_discovered["age"] = sub_info["age"]
        
    # Ville
    if sub_info["ville"].lower() in reply_lower:
        st.session_state.kyc_discovered["ville"] = sub_info["ville"]
        
    # Métier
    if sub_info["metier"].lower() in reply_lower:
        st.session_state.kyc_discovered["metier"] = sub_info["metier"]

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
            
            # Détection KYC
            update_kyc_automatically(reply)
            
            # Traitement de la décision d'achat PPV
            if st.session_state.last_sent_is_ppv and "BUY_PPV" in reply:
                reply_clean = reply.replace("BUY_PPV", "").strip()
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f":green[✅ **PPV DÉBLOQUÉ PAR L'ABONNÉ**]\n\n{reply_clean}"
                })
            else:
                reply_clean = reply.replace("BUY_PPV", "").strip()
                st.session_state.messages.append({"role": "assistant", "content": reply_clean})
            
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
