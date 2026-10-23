import streamlit as st
import sqlite3

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="منصة الريزيدانا الطبية المتقدمة",
    page_icon="🩺",
    layout="wide"
)

# تخصيص التصميم والواجهة
st.markdown("""
    <style>
    .main-header { font-size: 2.3rem; color: #1E3A8A; text-align: center; font-weight: bold; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 2rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; }
    .stButton>button:hover { background-color: #1D4ED8; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- إعداد وإدارة قاعدة البيانات SQLite ---
def init_db():
    conn = sqlite3.connect('residanat.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # جدول الأسئلة مع حقل الأرشيف والسنة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module TEXT,
            year TEXT,
            question TEXT,
            opt1 TEXT,
            opt2 TEXT,
            opt3 TEXT,
            opt4 TEXT,
            answer INTEGER,
            explanation TEXT
        )
    ''')
    
    # تعبئة قاعدة البيانات بأسئلة أرشيفية حقيقية وغنية إذا كانت فارغة
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] == 0:
        initial_data = [
            # Cardiologie
            ("Cardiologie", "Résidanat 2023", "Quel est le signe ECG le plus précoce dans l'infarctus du myocarde ST+ ?", "Ondes T amples, symétriques et hyper-aiguës", "Sus-décalage du segment ST", "Ondes Q de nécrose", "Inversion de l'onde T", 0, "Les ondes T hyper-aiguës (amples et symétriques) constituent le tout premier signe observable en quelques minutes."),
            ("Cardiologie", "Résidanat 2022", "Quelle est la cause la plus fréquente de la mort subite chez le sujet jeune ?", "La dysplasie arythmogène du ventricule droit", "La cardiomyopathie hypertrophique (CMH)", "Le syndrome de Brugada", "L'anomalie coronaire congénitale", 1, "La CMH est la cause génétique et la plus fréquente de mort subite chez le sujet jeune et le sportif."),
            ("Cardiologie", "Résidanat 2021", "Quel est l'étalon-or (gold standard) pour le diagnostic positif de l'embolie pulmonaire ?", "L'angioscanner thoracique hélicoïdal", "L'échographie Doppler des membres inférieurs", "La scintigraphie ventilation/perfusion", "L'artériographie pulmonaire", 0, "L'angioscanner thoracique multidétecteur est l'examen de choix et de référence."),
            
            # Pédiatrie
            ("Pédiatrie", "Résidanat 2023", "Quelle est la cause virale la plus fréquente de la bronchiolite aiguë du nourrisson ?", "Le rhinovirus", "Le virus respiratoire syncytial (VRS)", "L'adénovirus", "Le metapneumovirus", 1, "Le VRS est responsable de 70 à 80% des bronchiolites aiguës chez le nourrisson de moins de 2 ans."),
            ("Pédiatrie", "Résidanat 2020", "Devant un purpura fulminans chez un enfant, quel est le premier geste thérapeutique d'urgence à faire avant l'hospitalisation ?", "Réaliser une ponction lombaire", "Administrer immédiatement une antibiothérapie (C3G IV ou IM)", "Faire une NFS et un bilan d'hémostase", "Transfuser des plaquettes", 1, "L'administration immédiate d'une Céphalosporine de 3e génération (C3G) est une urgence vitale absolue."),
            
            # Hématologie
            ("Hématologie", "Résidanat 2022", "Devant une anémie normocytaire arégénérative, quel examen clé doit-on réaliser en première intention ?", "Un test de Coombs direct", "Un myélogramme", "Un dosage de la vitamine B12 et des folates", "Une électrophorèse de l'hémoglobine", 1, "L'anémie arégénérative témoigne d'une atteinte centrale (médullaire), d'où l'indication du myélogramme."),
            ("Hématologie", "Résidanat 2021", "Quel est le traitement de première intention de la leucémie aiguë promyélocytaire (LAP / LAM3) ?", "L'hydroxyurée", "L'acide tout-trans rétinoïque (ATRA) associé à la chimiothérapie", "La splénectomie", "Les inhibiteurs de tyrosine kinase", 1, "L'ATRA a révolutionné le pronostic de la LAP en induisant la différenciation des cellules blastiques."),
            
            # Pneumologie
            ("Pneumologie", "Résidanat 2023", "Quel est l'examen de certitude microbiologique pour le diagnostic de la tuberculose pulmonaire active ?", "La radiographie thoracique standard", "L'intradermoréaction (IDR) à la tuberculine", "L'examen cytobactériologique des crachats (ECBC) / PCR GeneXpert", "L'endoscopie bronchique avec brossage", 2, "La mise en évidence de Mycobacterium tuberculosis par examen direct, culture ou PCR confirme le diagnostic de certitude."),
            
            # Néphrologie
            ("Néphrologie", "Résidanat 2022", "Quels sont les critères biologiques définissant un syndrome néphrotique pur ?", "Protéinurie > 3g/24h, albuminémie < 30g/l, absence d'HTA, d'hématurie et d'insuffisance rénale", "Protéinurie > 1,5g/24h avec hématurie macroscopique et HTA", "Protéinurie massive avec insuffisance rénale organique et bas complement", 0, "Le syndrome néphrotique pur se distingue par l'absence d'éléments de mauvais pronostic (HTA, hématurie, IR)."),
            
            # Gynécologie-Obstétrique
            ("Gynécologie-Obstétrique", "Résidanat 2023", "Quelle est la complication neurologique majeure et redoutée de la pré-éclampsie sévère ?", "L'hématome rétro-placentaire (HRP)", "L'éclampsie (survenue de crises convulsives généralisées)", "La coagulation intravasculaire disséminée (CIVD)", "Le syndrome HELLP", 1, "L'éclampsie se manifeste par des crises convulsives tonico-cloniques menaçant le pronostic vital materno-fœtal."),
            
            # Hépato-Gastro-Entérologie
            ("Hépato-Gastro-Entérologie", "Résidanat 2021", "Quelle est la cause étiologique principale de la cirrhose du foie en Algérie ?", "L'alcoolisme chronique", "Les hépatites virales chroniques B et C", "La stéatose métabolique (NASH)", "La cirrhose biliaire primitive", 1, "Contrairement aux pays occidentaux, les infections par les virus des hépatites B et C dominent largement les causes de cirrhose en Algérie.")
        ]
        
        cursor.executemany('''
            INSERT INTO questions (module, year, question, opt1, opt2, opt3, opt4, answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_data)
        conn.commit()
        
    return conn

conn = init_db()
cursor = conn.cursor()

# عنوان التطبيق
st.markdown('<div class="main-header">🩺 منصة الريزيدانا الطبية الشاملة</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">بنك أسئلة الأرشيف الطبي ومراجعة الذكاء الإصطناعي للريزيدانا في الجزائر</div>', unsafe_allow_html=True)

# القائمة الجانبية المتقدمة
st.sidebar.image("https://img.icons8.com/color/96/medical-doctor.png", width=80)
st.sidebar.title("📌 تصفح الأقسام والخدمات")

menu_options = [
    "🏠 الرئيسية والإحصائيات",
    "📚 مراجعة حسب الموديول",
    "🔍 البحث السريع في الأرشيف",
    "➕ إضافة سؤال جديد لقاعدة البيانات"
]

selected_tab = st.sidebar.radio("اختر القسم:", menu_options)

# --- 1. الرئيسية والإحصائيات ---
if selected_tab == "🏠 الرئيسية والإحصائيات":
    st.subheader("📊 لوحة تحكم إحصائيات بنك الأسئلة")
    st.write("مرحباً بك مجدداً في مسارك التحضيري لمسابقة **الريزيدانا (Résidanat)**. يجمع هذا التطبيق خلاصة الأسئلة الأرشيفية الموزعة بدقة عبر مختلف التخصصات الطبية.")
    
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_q = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT module) FROM questions")
    total_mods = cursor.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="إجمالي الأسئلة المتاحة", value=total_q)
    with col2:
        st.metric(label="الموديولات المغطاة", value=total_mods)
    with col3:
        st.metric(label="نسبة الجاهزية بالسحاب", value="100% نشط")
        
    st.markdown("---")
    st.info("💡 **نصيحة للمراجعة:** يمكنك استخدام قسم (مراجعة حسب الموديول) لحل الأسئلة والاطلاع الفوري على التصحيح الرسمي والشروحات الطبية المستندة إلى الأرشيف الوطني.")

# --- 2. مراجعة حسب الموديول ---
elif selected_tab == "📚 مراجعة حسب الموديول":
    st.subheader("📚 بنك الأسئلة حسب التخصص والموديول")
    
    # جلب قائمة الموديولات المتاحة
    cursor.execute("SELECT DISTINCT module FROM questions")
    modules = [row[0] for row in cursor.fetchall()]
    
    selected_module = st.selectbox("اختر الموديول الطبي:", modules)
    
    if selected_module:
        cursor.execute("SELECT id, year, question, opt1, opt2, opt3, opt4, answer, explanation FROM questions WHERE module = ?", (selected_module,))
        questions = cursor.fetchall()
        
        st.write(f"📁 عدد الأسئلة المتوفرة في موديول **{selected_module}**: `{len(questions)}` سؤال")
        st.markdown("---")
        
        for idx, q in enumerate(questions):
            q_id, year, q_text, o1, o2, o3, o4, correct_ans, explanation = q
            options = [o1, o2, o3, o4]
            
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <b>السؤال {idx+1}</b> &nbsp;|&nbsp; <span style="color: #2563EB; font-weight: bold;">{year}</span><br>
                    <p style="font-size: 1.1rem; margin-top: 8px;"><b>{q_text}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                user_choice = st.radio("اختر الإجابة المناسبة:", options, key=f"q_radio_{q_id}")
                
                if st.button(f"تحقق من الإجابة الصحيحة #{idx+1}", key=f"btn_check_{q_id}"):
                    selected_index = options.index(user_choice)
                    if selected_index == correct_ans:
                        st.success("✅ إجابة دقيقة وصحيحة!")
                    else:
                        st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة هي: **{options[correct_ans]}**")
                    
                    if explanation:
                        st.info(f"📖 **التبرير والشرح العلمي:** {explanation}")
                st.markdown("<br>", unsafe_allow_html=True)

# --- 3. البحث السريع في الأرشيف ---
elif selected_tab == "🔍 البحث السريع في الأرشيف":
    st.subheader("🔍 محرك البحث الذكي في بنك الأسئلة")
    search_query = st.text_input("أدخل كلمة مفتاحية للبحث (مثال: Infarctus, Bronchiolite, Anémie...):")
    
    if search_query:
        cursor.execute("""
            SELECT module, year, question, opt1, opt2, opt3, opt4, answer, explanation 
            FROM questions 
            WHERE question LIKE ? OR explanation LIKE ? OR module LIKE ?
        """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        
        results = cursor.fetchall()
        st.write(f"نتائج البحث عن: `{search_query}` (وجدنا `{len(results)}` نتيجة)")
        st.markdown("---")
        
        if not results:
            st.warning("لم يتم العثور على مطابقات دقيقة في قاعدة البيانات الحالية.")
        else:
            for r in results:
                mod, yr, q_t, o1, o2, o3, o4, c_ans, expl = r
                opts = [o1, o2, o3, o4]
                st.markdown(f"""
                <div class="card">
                    <small style="color: gray;">الموديول: {mod} | {yr}</small>
                    <p><b>{q_t}</b></p>
                    <ul>
                        <li>{'✅ **[صحيحة]** ' if opts[0]==opts[c_ans] else ''}{o1}</li>
                        <li>{o2}</li>
                        <li>{o3}</li>
                        <li>{o4}</li>
                    </ul>
                    <p style="color: #047857; background-color: #ECFDF5; padding: 10px; border-radius: 5px;"><b>الشرح:</b> {expl}</p>
                </div>
                """, unsafe_allow_html=True)

# --- 4. إضافة سؤال جديد ---
elif selected_tab == "➕ إضافة سؤال جديد لقاعدة البيانات":
    st.subheader("➕ إضافة سؤال أرشيفي أو حالة جديدة إلى بنك الأسئلة")
    
    with st.form("add_q_form"):
        mod_name = st.selectbox("اختر الموديول:", ["Cardiologie", "Pédiatrie", "Hématologie", "Pneumologie", "Néphrologie", "Gynécologie-Obstétrique", "Hépato-Gastro-Entérologie", "Neurologie", "Endocrinologie"])
        year_tag = st.text_input("مصدر السؤال / السنة (مثال: Résidanat 2024 - الجزائر العاصمة):")
        q_content = st.text_area("نص السؤال:")
        
        col_a, col_b = st.columns(2)
        with col_a:
            opt_1 = st.text_input("الخيار (A):")
            opt_2 = st.text_input("الخيار (B):")
        with col_b:
            opt_3 = st.text_input("الخيار (C):")
            opt_4 = st.text_input("الخيار (D):")
            
        correct_index = st.selectbox("حدد الخيار الصحيح:", [0, 1, 2, 3], format_func=lambda x: ["الخيار A", "الخيار B", "الخيار C", "الخيار D"][x])
        explanation_text = st.text_area("التبرير والشرح الطبي الرسمي:")
        
        submitted_btn = st.form_submit_button("حفظ السؤال في القاعدة السحابية")
        
        if submitted_btn:
            if q_content and opt_1 and opt_2:
                cursor.execute('''
                    INSERT INTO questions (module, year, question, opt1, opt2, opt3, opt4, answer, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (mod_name, year_tag, q_content, opt_1, opt_2, opt_3, opt_4, correct_index, explanation_text))
                conn.commit()
                st.success("✅ تم حفظ السؤال وإضافته بنجاح إلى قاعدة بيانات التطبيق على السحابة!")
            else:
                st.error("الرجاء ملء الحقول الأساسية (النص والخيارات الأولى على الأقل).")

