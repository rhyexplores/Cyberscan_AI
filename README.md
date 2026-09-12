# 🛡️ CyberScan AI

### AI-Based Network Traffic Classification

CyberScan AI is a supervised machine learning project that classifies network traffic as **Benign** or **Malicious** using the **NSL-KDD dataset**.

The project covers the complete ML pipeline: **data preprocessing, feature selection, model training, evaluation, and interactive deployment using Streamlit.**

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

Used as the **main classification model** to learn patterns in network traffic and classify connections as benign or malicious.

### SVM

Used as a **comparison model** to evaluate another supervised classification approach.

---

## 📈 Evaluation

The models are evaluated using:

* **Accuracy**
* **Precision**
* **Recall**
* **F1-Score**
* **Classification Report**

The Random Forest evaluation results are saved in:

```text
model_metrics.json
```

---

## 🖥️ Streamlit Application

The **CyberScan AI** application allows users to:

* Enter the 15 network features
* Predict **Benign / Malicious** traffic
* View prediction probabilities
* Visualize the traffic using **PCA**
* Try predefined normal and attack scenarios

---

## 📁 Project Structure

```text
CyberScan-AI/
│
├── train_test.py          # Data preprocessing, training & evaluation
├── app.py                 # Streamlit application
│
├── rf_model.pkl           # Trained Random Forest model
├── scaler.pkl             # Saved feature scaler
├── selected_features.pkl  # Selected 15 features
├── X_sample.pkl           # Sample data for PCA visualization
├── y_sample.pkl           # Sample labels for PCA visualization
└── model_metrics.json     # Model evaluation metrics
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

### 2. Train the model

```bash
python train_test.py
```

This generates the required model, scaler, feature-selection, visualization, and metric files.

### 3. Launch the application

```bash
streamlit run app.py
```

---

## ⚠️ Limitations

* Uses the NSL-KDD benchmark dataset rather than live network traffic.
* The current application requires manual feature input.
* The model only performs **binary classification**: Benign vs Malicious.
* Performance depends on the types of attacks represented in the training dataset.

---

## 🔮 Future Scope

* Real-time network packet capture
* Automatic feature extraction from network traffic
* Real-time attack alerts
* Multi-class attack detection
* Model explainability
* Integration with live security monitoring systems

---

## 📌 Key Takeaway

**CyberScan AI demonstrates an end-to-end machine learning approach for detecting potentially malicious network traffic, from preprocessing and feature selection to model training, evaluation, and interactive deployment.**
