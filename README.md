# 🛡️ CyberScan AI

### AI-Based Network Traffic Classification

CyberScan AI is a supervised machine learning project that classifies network traffic as **Benign** or **Malicious** using the **NSL-KDD dataset**.

The project covers the complete ML pipeline: **data preprocessing, feature selection, model training, evaluation, and deployment using Streamlit.**

---

## 🎯 Objective

To develop an ML-based cybersecurity system that can identify potentially malicious network traffic from network connection characteristics.

---

## 🔄 Project Workflow

```text
NSL-KDD Dataset
      ↓
Data Preprocessing
      ↓
Categorical Encoding
      ↓
Feature Selection
      ↓
Top 15 Features
      ↓
Feature Scaling
      ↓
Random Forest + SVM
      ↓
Model Evaluation
      ↓
Streamlit Deployment
```

---

## 📊 Dataset

**NSL-KDD** is a network intrusion detection dataset where each record represents a network connection.

The target is converted into:

* `0` → Benign / Normal
* `1` → Malicious / Attack

### Selected Features

The top 15 features are selected using **Random Forest feature importance**:

```text
src_bytes
dst_bytes
count
srv_count
same_srv_rate
diff_srv_rate
serror_rate
srv_serror_rate
dst_host_count
dst_host_srv_count
dst_host_same_srv_rate
dst_host_diff_srv_rate
dst_host_serror_rate
dst_host_srv_serror_rate
dst_host_same_src_port_rate
```

These features represent **data transfer, connection frequency, service behavior, and connection-error patterns**.

---

## 🤖 Machine Learning Models

### Random Forest

Used as the **main classification model** because it can learn complex relationships between network features.

### SVM

Used as a **comparison model** to evaluate another classification approach.

---

## 📈 Evaluation

The models are evaluated using:

* **Accuracy**
* **Precision**
* **Recall**
* **F1-Score**

The Random Forest evaluation results are also stored in `model_metrics.json`.

---

## 🖥️ Streamlit Application

The application, **CyberScan AI**, allows users to:

* Enter the 15 network features
* Predict **Benign / Malicious** traffic
* View prediction probabilities
* Visualize the traffic using PCA
* Try predefined normal and attack scenarios

---

## 📁 Project Structure

```text
CyberScan-AI/
│
├── train_test.py          # Training & evaluation
├── savepoints.py          # Saves visualization samples
├── app.py                 # Streamlit application
│
├── rf_model.pkl           # Trained Random Forest
├── scaler.pkl             # Saved feature scaler
├── selected_features.pkl  # Selected 15 features
├── model_metrics.json     # Evaluation metrics
│
├── X_sample.pkl
├── y_sample.pkl           # Visualization data
├── X_sample.npy
└── y_sample.npy
```

---

## ⚙️ Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* Hugging Face Datasets
* Joblib
* Matplotlib
* Streamlit

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install pandas numpy scikit-learn joblib datasets streamlit matplotlib
```

### 2. Train the models

```bash
python train_test.py
```

### 3. Save visualization samples

```bash
python savepoints.py
```

### 4. Launch the application

```bash
streamlit run app.py
```

---

## ⚠️ Limitations

* Uses the NSL-KDD benchmark dataset rather than live network traffic.
* Current application requires manual feature input.
* Performance depends on the quality and types of attacks represented in the dataset.

---

## 🔮 Future Scope

* Real-time network packet capture
* Automatic feature extraction
* Real-time attack alerts
* Multi-class attack detection
* Model explainability
* Integration with live security monitoring systems

---

## 📌 Key Takeaway

**CyberScan AI demonstrates an end-to-end machine learning approach for detecting potentially malicious network traffic, from preprocessing and feature selection to model training, evaluation, and interactive deployment.**
