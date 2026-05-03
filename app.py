import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# --- إعدادات الرابط الخاص بك ---
API_URL = "https://script.google.com/macros/s/AKfycbzTP0ypdZbmZ7z1X4oihlL4qD08KkwzmpxeqxhHTvt1RDBen2Ske5ava8P5s_1NBhkVLg/exec"
PASSWORD = "admin" 

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide", page_icon="🌍")

# --- تصميم الواجهة العصرية 2026 ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stTabs [aria-selected="true"] { background: #002147 !important; color: white !important; border-radius: 10px; }
    .invoice-card { 
        background: white; border: 2px solid #002147; padding: 40px; border-radius: 15px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: auto; max-width: 800px;
        border-top: 15px solid #002147;
    }
    .money-badge { background: #f8f9fa; padding: 15px; border-radius: 10px; border-right: 8px solid #002147; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الحماية ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("<h2 style='text-align:center; margin-top:50px;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == PASSWORD: st.session_state.auth = True; st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# --- القائمة الرئيسية ---
tab1, tab2, tab3 = st.tabs(["📊 السجلات والحسابات", "👤 تسجيل عميل جديد", "🧾 البحث وطباعة الفاتورة"])

# --- التبويب الأول: عرض البيانات (محمي من الانهيار) ---
with tab1:
    st.subheader("📋 قاعدة البيانات الموحدة")
    if st.button("🔄 تحديث ومزامنة السحابة"):
        try:
            res = requests.get(API_URL)
            if res.status_code == 200:
                data_json = res.json()
                df = pd.DataFrame(data_json[1:], columns=data_json)
                st.dataframe(df, use_container_width=True)
            else: st.error("عذراً، جوجل ترفض الوصول. تأكد من إعداد Anyone في النشر.")
        except: st.error("خطأ في قراءة البيانات. تأكد من ملء صف واحد على الأقل في الشيت.")

# --- التبويب الثاني: تسجيل عميل (توليد تتبع عشوائي) ---
with tab2:
    st.subheader("📝 نموذج تسجيل ملف جديد")
    with st.form("main_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("اسم العميل")
            passport = st.text_input("رقم الجواز")
            phone = st.text_input("رقم الهاتف")
            email = st.text_input("الإيميل")
        with c2:
            nation = st.text_input("الجنسية")
            residence = st.text_input("بلد الإقامة")
            service = st.selectbox("المعاملة", ["دراسة", "عقد عمل", "سياحة"])
            branch = st.selectbox("الفرع", ["بيلاروسيا", "مصر"])
        with c3:
            v_date = st.date_input("موعد السفارة")
            staff = st.text_input("الموظف المضيف")
            status = st.selectbox("حالة الطلب", ["قيد المعالجة", "تم الحجز", "مرفوض"])
        
        st.write("---")
        f1, f2 = st.columns(2)
        with f1: total = st.number_input("إجمالي المبلغ ($)", min_value=0.0)
        with f2: paid = st.number_input("المبلغ المدفوع ($)", min_value=0.0)
        
        if st.form_submit_button("حفظ المزامنة وإصدار الفاتورة ✅"):
            # توليد رقم تتبع عشوائي احترافي
            trk = f"TRK-{random.randint(100000, 999999)}-{branch[:2].upper()}"
            # إرسال البيانات الـ 15 الأساسية
            row = [name, passport, phone, email, nation, residence, service, status, str(v_date), str(datetime.now().date()), branch, staff, total, paid, trk]
            try:
                requests.post(API_URL, json=row)
                st.success(f"✅ تم الحفظ بنجاح! رقم التتبع: {trk}")
                st.balloons()
            except: st.error("فشل في إرسال البيانات.")

# --- التبويب الثالث: البحث والطباعة الملكية ---
with tab3:
    st.subheader("🔍 استخراج الفاتورة الذكية")
    search_q = st.text_input("ابحث باسم العميل أو رقم جواز السفر")
    if search_q:
        try:
            res = requests.get(API_URL).json()
            df = pd.DataFrame(res[1:], columns=res)
            # بحث ذكي يعتمد على ترتيب الأعمدة (الاسم في العمود 3 والجواز في العمود 4)
            match = df[df.iloc[:, 2].astype(str).str.contains(search_q) | df.iloc[:, 3].astype(str).str.contains(search_q)]
            
            if not match.empty:
                c = match.iloc[0] # جلب أول نتيجة بحث
                st.markdown(f"""
                <div class="invoice-card">
                    <table style="width:100%">
                        <tr>
                            <td style="text-align:right"><h1>🧾 فاتورة رسمية</h1><p>International Travel Services</p></td>
                            <td style="text-align:left"><h2 style="color:#002147">{c.iloc[0]}</h2><p>{c.iloc[18]}</p></td>
                        </tr>
                    </table>
                    <hr style="border:1px solid #002147">
                    <div style="display:flex; justify-content:space-between; margin-top:20px;">
                        <div>
                            <p style="font-size:1.2em"><b>العميل:</b> {c.iloc[2]}</p>
                            <p><b>رقم الجواز:</b> {c.iloc[3]} | <b>الهاتف:</b> {c.iloc[4]}</p>
                        </div>
                        <div style="text-align:left">
                            <p><b>التاريخ:</b> {c.iloc[11]}</p>
                            <p><b>المعاملة:</b> {c.iloc[8]}</p>
                            <p><b>رقم التتبع:</b> {c.iloc[17]}</p>
                        </div>
                    </div>
                    <div class="money-badge">
                        <h3 style="margin-top:0">💰 الموقف المالي:</h3>
                        <p>الإجمالي: {c.iloc[14]}$ | المدفوع: {c.iloc[15]}$</p>
                        <h2 style="color:#d32f2f; margin-bottom:0">المبلغ المتبقي: {c.iloc[16]}$</h2>
                    </div>
                    <div style="text-align:center; margin-top:30px; color:#666; font-size:12px;">
                        <p>تم استخراج هذه الفاتورة آلياً - فرع {c.iloc[12]}</p>
                        <p>الموظف المسؤول: {c.iloc[13]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info("💡 اضغط Ctrl + P لطباعة الفاتورة أو حفظها كـ PDF.")
            else: st.warning("⚠️ العميل غير موجود في السجلات.")
        except Exception as e: st.error(f"خطأ في قراءة البيانات: {e}")
