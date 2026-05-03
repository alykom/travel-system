import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# الرابط الخاص بك
API_URL = "https://script.google.com/macros/s/AKfycbyVQqXP6286ehaJ5KikBpUm3hKMsFSWnjuhMN9IH_rW6MH78FJJbVcMoxEVocxVKNQNZw/exec"
PASSWORD = "admin" 

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide")

# تصميم CSS احترافي (يخفي كل عناصر الموقع عند الطباعة)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; }

    /* سحر الطباعة: يخفي كل شيء ما عدا كارت الفاتورة */
    @media print {
        header, footer, .no-print, [data-testid="stSidebar"], [data-testid="stHeader"], .stTabs, .stButton {
            display: none !important;
        }
        .main .block-container { padding: 0 !important; }
        .invoice-card { 
            border: none !important; 
            box-shadow: none !important; 
            width: 100% !important; 
            margin: 0 !important; 
            padding: 20px !important;
        }
    }

    .invoice-card { 
        background: white; border: 1px solid #ddd; padding: 40px; border-radius: 0px; 
        direction: rtl; text-align: right; max-width: 800px; margin: auto;
        border-top: 15px solid #002147; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .invoice-header { display: flex; justify-content: space-between; border-bottom: 2px solid #002147; padding-bottom: 15px; margin-bottom: 25px; }
    .money-table { width: 100%; border-collapse: collapse; margin: 20px 0; background: #f8f9fa; border-right: 8px solid #002147; }
    .money-table td { padding: 15px; border-bottom: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

# نظام الدخول
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<div class='no-print' style='text-align:center;'><h2>🔐 دخول النظام</h2></div>", unsafe_allow_html=True)
    pwd = st.text_input("كلمة المرور", type="password", key="login_pwd")
    if st.button("دخول"):
        if pwd == PASSWORD: st.session_state.auth = True; st.rerun()
        else: st.error("❌ خطأ")
    st.stop()

# القائمة (تختفي عند الطباعة)
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.title("🌍 نظام شركة السفر الدولي | 2026")
tab1, tab2, tab3 = st.tabs(["📊 السجلات", "👤 إضافة ملف", "🔍 الفواتير والطباعة"])
st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    with st.form("reg_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("الاسم الكامل")
            passport = st.text_input("رقم الجواز")
            phone = st.text_input("الهاتف")
        with c2:
            nation = st.text_input("الجنسية")
            service = st.selectbox("المعاملة", ["دراسة", "عمل", "سياحة"])
            branch = st.selectbox("الفرع", ["بيلاروسيا", "مصر"])
        with c3:
            staff = st.text_input("الموظف المضيف")
            total = st.number_input("إجمالي المبلغ ($)", min_value=0.0)
            paid = st.number_input("المدفوع ($)", min_value=0.0)

        if st.form_submit_button("حفظ المزامنة ✅"):
            trk = f"TRK-{random.randint(100, 999)}-{random.randint(100, 999)}"
            row = [name, passport, phone, "", nation, "", service, "قيد المعالجة", "", str(datetime.now().date()), branch, staff, total, paid, trk]
            requests.post(API_URL, json=row)
            st.success("✅ تم الحفظ بنجاح!")

with tab3:
    st.markdown('<div class="no-print">', unsafe_allow_html=True)
    search_q = st.text_input("ابحث عن الاسم لإصدار الفاتورة")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if search_q:
        try:
            res = requests.get(API_URL).json()
            df = pd.DataFrame(res[1:], columns=res)
            match = df[df.iloc[:, 2].astype(str).str.contains(search_q)]
            
            if not match.empty:
                c = match.iloc[0]
                # باركود نصي مؤمن (كحل بديل للصورة المكسورة)
                qr_id = f"REF-{c.iloc[0]}"
                
                st.markdown(f"""
                <div class="invoice-card">
                    <div class="invoice-header">
                        <div>
                            <h1 style="margin:0; color:#002147;">فاتورة رسمية</h1>
                            <p style="margin:0; color:#666;">INTERNATIONAL TRAVEL SERVICES</p>
                        </div>
                        <div style="text-align:left; border: 1px dashed #002147; padding: 5px;">
                            <p style="margin:0; font-size:10px;">VERIFIED ID</p>
                            <h3 style="margin:0; color:#002147;">{qr_id}</h3>
                        </div>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
                        <div>
                            <p><b>السيد/ة:</b> {c.iloc[2]}</p>
                            <p><b>رقم الجواز:</b> {c.iloc[3]} | <b>الهاتف:</b> {c.iloc[4]}</p>
                            <p><b>نوع الخدمة:</b> {c.iloc[8]}</p>
                        </div>
                        <div style="text-align:left;">
                            <p><b>التاريخ:</b> {c.iloc[11]}</p>
                            <p><b>رقم الفاتورة:</b> {c.iloc[0]}</p>
                            <p><b>رقم التتبع:</b> {c.iloc[17]}</p>
                        </div>
                    </div>

                    <div class="money-table">
                        <table style="width:100%;">
                            <tr><td>إجمالي الحساب:</td><td style="text-align:left;"><b>{c.iloc[14]}$</b></td></tr>
                            <tr><td>المبلغ المدفوع:</td><td style="text-align:left;"><b>{c.iloc[15]}$</b></td></tr>
                            <tr style="color:#d32f2f; font-size:1.4em;"><td>المبلغ المتبقي:</td><td style="text-align:left;"><b>{c.iloc[16]}$</b></td></tr>
                        </table>
                    </div>

                    <div style="text-align:center; margin-top:40px; font-size:12px; color:#999; border-top:1px solid #eee; padding-top:15px;">
                        <p>هذه الوثيقة مستخرجة إلكترونياً من فرع {c.iloc[12]} - الموظف: {c.iloc[13]}</p>
                        <p>بيلاروسيا - مصر | © 2026</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="no-print" style="text-align:center; margin-top:20px;">', unsafe_allow_html=True)
                st.info("🖨️ للطباعة بشكل احترافي: اضغط Ctrl + P")
                st.markdown('</div>', unsafe_allow_html=True)
        except: st.error("خطأ في الاتصال بالبيانات")
