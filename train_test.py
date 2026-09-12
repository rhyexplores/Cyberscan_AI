"""
import pandas as pd
import joblib

from datasets import load_dataset
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# ==============================
# 1. LOAD DATA (NO CONCAT)
# ==============================
ds = load_dataset("Mireu-Lab/NSL-KDD")

train_df = pd.DataFrame(ds["train"])
test_df  = pd.DataFrame(ds["test"])

# ==============================
# 2. TARGET VARIABLE
# ==============================
train_df["target"] = train_df["class"].apply(lambda x: 0 if x == "normal" else 1)
test_df["target"]  = test_df["class"].apply(lambda x: 0 if x == "normal" else 1)

train_df.drop(columns=["class"], inplace=True)
test_df.drop(columns=["class"], inplace=True)

# ==============================
# 3. ENCODE CATEGORICAL
# ==============================
categorical_cols = ["protocol_type", "service", "flag"]

for col in categorical_cols:
    le = LabelEncoder()
    train_df[col] = le.fit_transform(train_df[col])
    test_df[col]  = le.transform(test_df[col])

# ==============================
# 4. SPLIT FEATURES & LABEL
# ==============================
X_train = train_df.drop("target", axis=1)
y_train = train_df["target"]

X_test = test_df.drop("target", axis=1)
y_test = test_df["target"]

# ==============================
# 5. FEATURE SELECTION (TOP 15)
# ==============================
rf_selector = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf_selector.fit(X_train, y_train)

importances = pd.Series(
    rf_selector.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)

selected_features = importances.head(15).index.tolist()

X_train = X_train[selected_features]
X_test  = X_test[selected_features]

# ==============================
# 6. SCALING
# ==============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ==============================
# 7. RANDOM FOREST
# ==============================
rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)

print("\n🔵 Random Forest Results")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

# ==============================
# 8. SVM (OPTIONAL – SLOW)
# ==============================
svm_model = SVC(
    kernel="rbf",
    C=10,
    gamma="scale",
    class_weight="balanced"
)

svm_model.fit(X_train_scaled, y_train)
svm_pred = svm_model.predict(X_test_scaled)

print("\n🟢 SVM Results")
print("Accuracy:", accuracy_score(y_test, svm_pred))
print(classification_report(y_test, svm_pred))

# ==============================
# 9. SAVE
# ==============================
joblib.dump(rf_model, "rf_model.pkl")
joblib.dump(svm_model, "svm_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(selected_features, "selected_features.pkl")

print("\n✅ Training completed correctly (no data leakage)")
"""
import pandas as pd
import joblib
from datasets import load_dataset
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

print("Loading dataset...")
ds = load_dataset("Mireu-Lab/NSL-KDD")

train_df = pd.DataFrame(ds["train"])
test_df = pd.DataFrame(ds["test"])

# ==============================
# TARGET VARIABLE
# ==============================
train_df["target"] = train_df["class"].apply(lambda x: 0 if x == "normal" else 1)
test_df["target"] = test_df["class"].apply(lambda x: 0 if x == "normal" else 1)

train_df.drop(columns=["class"], inplace=True)
test_df.drop(columns=["class"], inplace=True)

# ==============================
# ENCODE CATEGORICAL FEATURES
# ==============================
categorical_cols = ["protocol_type", "service", "flag"]

for col in categorical_cols:
    le = LabelEncoder()
    train_df[col] = le.fit_transform(train_df[col])
    test_df[col] = le.transform(test_df[col])

# ==============================
# SPLIT FEATURES & LABEL
# ==============================
X_train = train_df.drop("target", axis=1)
y_train = train_df["target"]

X_test = test_df.drop("target", axis=1)
y_test = test_df["target"]

# ==============================
# FEATURE SELECTION (TOP 15)
# ==============================
rf_selector = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
rf_selector.fit(X_train, y_train)

importances = pd.Series(
    rf_selector.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)

selected_features = importances.head(15).index.tolist()

X_train = X_train[selected_features]
X_test = X_test[selected_features]
# Features where zero is unrealistic for prediction
non_zero_features = [
    "count",
    "srv_count",
    "dst_host_count",
    "same_srv_rate",
    "dst_host_same_srv_rate"
]

for col in non_zero_features:
    median_value = train_df[col].median()
    train_df[col] = train_df[col].replace(0, median_value)
    test_df[col] = test_df[col].replace(0, median_value)


# ==============================
# SCALING
# ==============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SAVE SAMPLE POINTS FOR VISUALIZATION (ADD THIS)
X_vis = X_train_scaled[:3000]   # keep it lightweight
joblib.dump(X_vis, "X_sample.pkl")
y_vis = y_train[:3000]
joblib.dump(y_vis, "y_sample.pkl")
# ==============================
# RANDOM FOREST MODEL
# ==============================
rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)

print("\nRandom Forest Results")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

# ==============================
# SVM MODEL (OPTIONAL)
# ==============================
svm_model = SVC(
    kernel="rbf",
    C=10,
    gamma="scale",
    class_weight="balanced"
)

svm_model.fit(X_train_scaled, y_train)
svm_pred = svm_model.predict(X_test_scaled)

print("\nSVM Results")
print("Accuracy:", accuracy_score(y_test, svm_pred))
print(classification_report(y_test, svm_pred))

# ==============================
# SAVE FILES
# ==============================
#joblib.dump(svm_model, "svm_model.pkl")
joblib.dump(rf_model, "rf_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(selected_features, "selected_features.pkl")

print("\nTraining completed successfully (no data leakage)")

from sklearn.metrics import classification_report
import json

report = classification_report(y_test, rf_pred, output_dict=True)

with open("model_metrics.json", "w") as f:
    json.dump(report, f, indent=4)

print("Model metrics saved for UI")
