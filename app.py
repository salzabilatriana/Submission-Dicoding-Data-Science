"""
Prototype Sistem Machine Learning - Prediksi Dropout Siswa
Jaya Jaya Institut

Menjalankan aplikasi secara lokal:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Prediksi Dropout Siswa - Jaya Jaya Institut",
                    page_icon="🎓", layout="centered")

# ---------- Load model & artefak ----------
@st.cache_resource
def load_artifacts():
    model = joblib.load("model/rf_dropout_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    feature_columns = joblib.load("model/feature_columns.pkl")
    status_mapping = joblib.load("model/status_mapping.pkl")
    inverse_mapping = {v: k for k, v in status_mapping.items()}
    return model, scaler, feature_columns, inverse_mapping

model, scaler, feature_columns, inverse_mapping = load_artifacts()

st.title("🎓 Prediksi Status Siswa")
st.markdown(
    "Prototype ini membantu **Jaya Jaya Institut** memprediksi kemungkinan "
    "seorang siswa akan **Dropout**, masih **Enrolled**, atau **Graduate**, "
    "berdasarkan data pendaftaran dan performa akademik semester 1 & 2."
)

st.divider()

tab1, tab2 = st.tabs(["🧍 Input Manual", "📄 Upload CSV (Batch)"])

# ---------- Helper prediksi ----------
def predict(df_input: pd.DataFrame):
    df_input = df_input[feature_columns]
    scaled = scaler.transform(df_input)
    preds = model.predict(scaled)
    probs = model.predict_proba(scaled)
    labels = [inverse_mapping[p] for p in preds]
    return labels, probs

# ---------- TAB 1: Input manual ----------
with tab1:
    st.subheader("Data Siswa")

    with st.form("manual_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Data Pendaftaran**")
            marital_status = st.number_input("Marital status (kode)", 1, 6, 1)
            application_mode = st.number_input("Application mode (kode)", 1, 57, 1)
            application_order = st.number_input("Application order", 0, 9, 1)
            course = st.number_input("Course (kode)", 1, 9999, 9500)
            attendance = st.selectbox("Daytime (1) / Evening (0)", [1, 0])
            prev_qual = st.number_input("Previous qualification (kode)", 1, 43, 1)
            prev_qual_grade = st.slider("Previous qualification grade", 0.0, 200.0, 130.0)
            nationality = st.number_input("Nacionality (kode)", 1, 109, 1)

        with col2:
            st.markdown("**Latar Belakang & Finansial**")
            mother_qual = st.number_input("Mother's qualification (kode)", 1, 44, 1)
            father_qual = st.number_input("Father's qualification (kode)", 1, 44, 1)
            mother_occ = st.number_input("Mother's occupation (kode)", 0, 194, 5)
            father_occ = st.number_input("Father's occupation (kode)", 0, 195, 5)
            admission_grade = st.slider("Admission grade", 0.0, 200.0, 130.0)
            displaced = st.selectbox("Displaced", [0, 1])
            special_needs = st.selectbox("Educational special needs", [0, 1])
            debtor = st.selectbox("Debtor", [0, 1])
            tuition_ok = st.selectbox("Tuition fees up to date", [1, 0])
            gender = st.selectbox("Gender (1=Male, 0=Female)", [1, 0])
            scholarship = st.selectbox("Scholarship holder", [0, 1])
            age = st.slider("Age at enrollment", 16, 70, 20)
            international = st.selectbox("International", [0, 1])

        with col3:
            st.markdown("**Performa Semester 1**")
            cu1_credited = st.number_input("Sem 1 - credited", 0, 30, 0)
            cu1_enrolled = st.number_input("Sem 1 - enrolled", 0, 30, 6)
            cu1_eval = st.number_input("Sem 1 - evaluations", 0, 45, 6)
            cu1_approved = st.number_input("Sem 1 - approved", 0, 30, 5)
            cu1_grade = st.slider("Sem 1 - grade", 0.0, 20.0, 12.0)
            cu1_no_eval = st.number_input("Sem 1 - without evaluations", 0, 30, 0)

            st.markdown("**Performa Semester 2**")
            cu2_credited = st.number_input("Sem 2 - credited", 0, 30, 0)
            cu2_enrolled = st.number_input("Sem 2 - enrolled", 0, 30, 6)
            cu2_eval = st.number_input("Sem 2 - evaluations", 0, 45, 6)
            cu2_approved = st.number_input("Sem 2 - approved", 0, 30, 5)
            cu2_grade = st.slider("Sem 2 - grade", 0.0, 20.0, 12.0)
            cu2_no_eval = st.number_input("Sem 2 - without evaluations", 0, 30, 0)

            st.markdown("**Makroekonomi (saat pendaftaran)**")
            unemployment = st.slider("Unemployment rate (%)", 0.0, 20.0, 10.0)
            inflation = st.slider("Inflation rate (%)", -5.0, 10.0, 1.0)
            gdp = st.slider("GDP", -5.0, 5.0, 1.0)

        submitted = st.form_submit_button("🔍 Prediksi", use_container_width=True)

    if submitted:
        row = {
            "Marital_status": marital_status, "Application_mode": application_mode,
            "Application_order": application_order, "Course": course,
            "Daytime_evening_attendance": attendance, "Previous_qualification": prev_qual,
            "Previous_qualification_grade": prev_qual_grade, "Nacionality": nationality,
            "Mothers_qualification": mother_qual, "Fathers_qualification": father_qual,
            "Mothers_occupation": mother_occ, "Fathers_occupation": father_occ,
            "Admission_grade": admission_grade, "Displaced": displaced,
            "Educational_special_needs": special_needs, "Debtor": debtor,
            "Tuition_fees_up_to_date": tuition_ok, "Gender": gender,
            "Scholarship_holder": scholarship, "Age_at_enrollment": age,
            "International": international,
            "Curricular_units_1st_sem_credited": cu1_credited,
            "Curricular_units_1st_sem_enrolled": cu1_enrolled,
            "Curricular_units_1st_sem_evaluations": cu1_eval,
            "Curricular_units_1st_sem_approved": cu1_approved,
            "Curricular_units_1st_sem_grade": cu1_grade,
            "Curricular_units_1st_sem_without_evaluations": cu1_no_eval,
            "Curricular_units_2nd_sem_credited": cu2_credited,
            "Curricular_units_2nd_sem_enrolled": cu2_enrolled,
            "Curricular_units_2nd_sem_evaluations": cu2_eval,
            "Curricular_units_2nd_sem_approved": cu2_approved,
            "Curricular_units_2nd_sem_grade": cu2_grade,
            "Curricular_units_2nd_sem_without_evaluations": cu2_no_eval,
            "Unemployment_rate": unemployment, "Inflation_rate": inflation, "GDP": gdp,
        }
        df_row = pd.DataFrame([row])
        labels, probs = predict(df_row)

        pred_label = labels[0]
        prob_dict = {inverse_mapping[i]: probs[0][i] for i in range(len(probs[0]))}

        if pred_label == "Dropout":
            st.error(f"⚠️ Prediksi: **{pred_label}** — siswa ini berisiko tinggi untuk dropout.")
        elif pred_label == "Enrolled":
            st.warning(f"ℹ️ Prediksi: **{pred_label}** — siswa diperkirakan masih akan aktif kuliah.")
        else:
            st.success(f"✅ Prediksi: **{pred_label}** — siswa diperkirakan akan lulus.")

        st.markdown("**Probabilitas tiap kelas:**")
        st.bar_chart(pd.Series(prob_dict))

# ---------- TAB 2: Upload CSV batch ----------
with tab2:
    st.subheader("Prediksi Massal via CSV")
    st.markdown(
        "Unggah file CSV (pemisah `;`) dengan kolom yang sama seperti `data.csv` "
        "(tanpa kolom `Status`) untuk memprediksi banyak siswa sekaligus."
    )
    uploaded = st.file_uploader("Pilih file CSV", type=["csv"])

    if uploaded is not None:
        try:
            df_batch = pd.read_csv(uploaded, sep=';')
            missing_cols = [c for c in feature_columns if c not in df_batch.columns]
            if missing_cols:
                st.error(f"Kolom berikut tidak ditemukan pada file: {missing_cols}")
            else:
                labels, probs = predict(df_batch)
                result = df_batch.copy()
                result["Predicted_Status"] = labels
                result["Confidence"] = probs.max(axis=1)
                st.success(f"Berhasil memprediksi {len(result)} siswa.")
                st.dataframe(result[["Predicted_Status", "Confidence"] + feature_columns[:5]])
                st.bar_chart(result["Predicted_Status"].value_counts())

                csv_out = result.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button("⬇️ Unduh Hasil Prediksi", csv_out,
                                    file_name="hasil_prediksi.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca/memproses file: {e}")

st.divider()
st.caption("Model: Random Forest (tuned) — dilatih pada data historis siswa Jaya Jaya Institut.")
