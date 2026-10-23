import streamlit as st
import sqlite3

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="منصة الريزيدانا الطبية الشاملة",
    page_icon="🩺",
    layout="wide"
)

# تخصيص التصميم
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; text-align: center; font-weight: bold; }
    .sub-header { font-size: 1.1rem; color: #4B5563; text-align: center; margin-bottom: 2rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- إعداد قاعدة البيانات SQLite ---
def init_db():
    conn = sqlite3.connect('residanat.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # جدول الأسئلة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module TEXT,
            question TEXT,
            opt1 TEXT,
            opt2 TEXT,
            opt3 TEXT,
            opt4 TEXT,
            answer INTEGER,
            explanation TEXT
        )
    ''')
    
    # التحقق مما إذا كانت القاعدة فارغة لإضافة بيانات أولية نموذجية لجميع الموديولات
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] == 0:
        sample_questions = [
            ("Cardiologie", "Quel est le signe ECG le plus précoce dans l'infarctus du myocarde ST+ ?", "Ondes T amples et symétriques", "Sus-décalage du segment ST", "Ondes Q de nécrose", "Inversion de l'onde T", 0, "Les ondes T hyper-aiguës sont le premier signe observable."),
            ("Pédiatrie", "Quelle est la cause la plus fréquente d'une bronchiolite aiguë chez le nourrisson ?", "Le rhinovirus", "Le virus respiratoire syncytial (VRS)", "La grippe", "L'adénovirus", 1, "Le VRS est responsable de 70-80% des cas."),
            ("Hématologie", "Devant une anémie normocytaire arégénérative, quel examen clé faire en premier ?", "Test de Coombs", "Myélogramme", "Dosage vitamine B12", "Électrophorèse de l'Hb", 1, "Nécessaire pour explorer une atteinte centrale médullaire."),
            ("Pneumologie", "Quel est l'examen de certitude pour le diagnostic de la tuberculose pulmonaire active ?", "Radiographie thoracique", "IDR à la tuberculine", "Examen cytobactériologique des crachats (ECBC / BK)", "Spirométrie", 2, "La mise en évidence du bacille de Koch par crachat ou PCR est l'examen de certitude."),
            ("Néphrologie", "Quel est le signe biologique cardinal d'un syndrome néphrotique pur ?", "Hématurie macroscopique", "Protéinurie > 3g/24h", "Insuffisance rénale aiguë", "Hypertension artérielle sévère", 1, "La protéinurie massive supérieure à 3g/24h est le critère clé."),
            ("Gynécologie-Obstétrique", "Quelle est la complication maternelle la plus redoutée au cours de la pré-éclampsie ?", "L'hématome rétro-placentaire", "L'éclampsie (crises convulsives)", "La rupture utérine", "L'infection urinaire", 1, "L'éclampsie représente l'urgence neurologique majeure de la pré-éclampsie."),
            ("Hépato-Gastro-Entérologie", "Quel est l'étiologie la plus fréquente de la cirrhose du foie en Algérie ?", "L'alcoolisme chronique", "L'hépatite virale B et C", "La stéatose hépatique (NASH)", "La cholangite biliaire primitive", 1, "Les hépatites virales chroniques B et C dominent l'étiologie de la cirrhose en Algérie.")
        ]
        cursor.executemany('''
            INSERT INTO questions (module, question, opt1, opt2, opt3, opt4, answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_questions)
        conn.commit()
    
    return conn

conn = init_db()
cursor = conn.cursor()

# العنوان الرئيسي
st.markdown('<div class="main-header">🩺 منصة الريزيدانا الطبية الشاملة</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">بنك الأسئلة المركزي وحالات أرشيف الريزيدانا</div>', unsafe_allow_html=True)

# القائمة الجانبية لتحديد الموديولات والأقسام
st.sidebar.title("📌 تصفح الموديولات")
modules_list = [
    "الرئيسية والإحصائيات",
    "Cardiologie",
    "Pédiatrie",
    "Hématologie",
    "Pneumologie",
    "Néphrologie",
    "Gynécologie-Obstétrique",
    "Hépato-Gastro-Entérologie",
    "Neurologie",
    "Endocrinologie",
    "Infectiologie",
    "Rhumatologie",
    "إضافة سؤال جديد لقاعدة البيانات"
]

selected_section = st.sidebar.radio("اختر القسم أو الموديول:", modules_list)

# --- 1. الرئيسية والإحصائيات ---
if selected_section == "الرئيسية والإحصائيات":
    st.subheader("👋 مرحباً بك في لوحة تحكم المراجعة")
    st.write("هذا التطبيق متصل بقاعدة بيانات محلية (`SQLite`) لتخزين الأسئلة والمراجعات عبر جميع موديولات الريزيدانا.")
    
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_q = cursor.fetchone()[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="إجمالي الأسئلة المتاحة في قاعدة البيانات", value=total_q)
    with col2:
        cursor.execute("SELECT COUNT(DISTINCT module) FROM questions")
        total_mods = cursor.fetchone()[0]
        st.metric(label="الموديولات المفعلة حالياً", value=total_mods)

    st.info("💡 **إرشاد:** يمكنك إضافة أسئلة جديدة تخص أي موديول مباشرة عبر خيار (إضافة سؤال جديد لقاعدة البيانات) في القائمة الجانبية لتوسيع بنك الأسئلة الخاص بك.")

# --- 2. إضافة سؤال جديد لقاعدة البيانات ---
elif selected_section == "إضافة سؤال جديد لقاعدة البيانات":
    st.subheader("➕ إضافة سؤال QCM جديد إلى قاعدة البيانات")
    
    with st.form("new_question_form"):
        mod = st.selectbox("الموديول الطبي:", ["Cardiologie", "Pédiatrie", "Hématologie", "Pneumologie", "Néphrologie", "Gynécologie-Obstétrique", "Hépato-Gastro-Entérologie", "Neurologie", "Endocrinologie", "Infectiologie", "Rhumatologie"])
        q_text = st.text_area("نص السؤال:")
        o1 = st.text_input("الخيار الأول (A):")
        o2 = st.text_input("الخيار الثاني (B):")
        o3 = st.text_input("الخيار الثالث (C):")
        o4 = st.text_input("الخيار الرابع (D):")
        ans_idx = st.selectbox("رقم الإجابة الصحيحة:", [0, 1, 2, 3], format_func=lambda x: ["A", "B", "C", "D"][x])
        exp_text = st.text_area("التبرير والشرح الطبي:")
        
        submitted = st.form_submit_button("حفظ السؤال في القاعدة")
        if submitted:
            if q_text and o1 and o2:
                cursor.execute('''
                    INSERT INTO questions (module, question, opt1, opt2, opt3, opt4, answer, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (mod, q_text, o1, o2, o3, o4, ans_idx, exp_text))
                conn.commit()
                st.success("✅ تم حفظ السؤال بنجاح في قاعدة البيانات!")
            else:
                st.error("الرجاء ملء الحقول الأساسية على الأقل.")

# --- 3. عرض الأسئلة حسب الموديول ---
else:
    st.subheader(f"📝 أسئلة موديول: {selected_section}")
    
    cursor.execute("SELECT id, question, opt1, opt2, opt3, opt4, answer, explanation FROM questions WHERE module = ?", (selected_section,))
    rows = cursor.fetchall()
    
    if not rows:
        st.warning(f"لا توجد أسئلة مسجلة حالياً لهذا الموديول في قاعدة البيانات. يمكنك إضافتها عبر القائمة الجانبية!")
    else:
        for idx, row in enumerate(rows):
            q_id, q_text, o1, o2, o3, o4, correct_ans, explanation = row
            options = [o1, o2, o3, o4]
            
            st.markdown(f"**السؤال {idx+1}:** {q_text}")
            user_choice = st.radio("اختر الإجابة:", options, key=f"q_{q_id}")
            
            if st.button(f"تحقق من الإجابة #{idx+1}", key=f"btn_{q_id}"):
                selected_index = options.index(user_choice)
                if selected_index == correct_ans:
                    st.success("✅ إجابة صحيحة!")
                else:
                    st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة هي: **{options[correct_ans]}**")
                
                if explanation:
                    st.info(f"📖 **الشرح الطبي:** {explanation}")
            st.markdown("---")
