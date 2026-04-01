# 📊 Financial Transactions Analysis Dashboard

This project is an interactive data analysis application built with **Streamlit**, designed to explore financial transaction data across three main dimensions:

* 👤 **Clients**
* 🏪 **Merchants**
* ⚠️ **Fraud x Non Fraud**

The goal is to uncover consumption patterns, identify behavioral trends, and detect anomalies within transactional data.

---

## 🚀 Technologies Used

* **Python**
* **Streamlit**
* **Pandas**
* **NumPy**
* **Matplotlib / Seaborn**
* **Plotly**

---

## 📂 Project Structure

```
📁 project/
│
├── client.py      # Client analysis dashboard
├── merch.py       # Merchant analysis dashboard
├── fraud.py       # Fraud analysis dashboard
├── functions.py   # Helper functions (data loading & filters)
└── main.py        # Page to be runned
```

---

## 📊 Features

### 👤 Client Analysis

* Key KPIs:

  * Total Spending
  * Number of Clients
  * Total Transactions
  * Average Ticket
  * Percentage of VIP Clients

* Analytical Views:

  * Spending distribution by category
  * Monthly transaction behavior
  * Gender-based consumption patterns
  * Transaction distribution by hour
  * Customer segmentation (Low, Medium, High, VIP)
  * Behavioral heatmaps (Category × Hour)

---

### 🏪 Merchant Analysis

* Key KPIs:

  * Number of active merchants
  * Top merchants by gender
  * Average revenue per merchant
  * Average transactions per merchant

* Analytical Views:

  * Revenue concentration by category
  * Top merchants ranking
  * Consumption behavior (weekdays vs weekends)
  * Seasonal transaction patterns
  * Merchant performance trends (rolling average)
  * Cumulative revenue evolution
  * Heatmaps (Category × Time)

---

### ⚠️ Fraud Analysis

* Key KPIs:

  * Total number of frauds
  * Fraud rate (%)
  * Total fraud amount
  * Average fraud vs non-fraud ticket

* Analytical Views:

  * Fraud vs non-fraud distribution
  * Fraud concentration by category
  * Monthly fraud trend
  * Fraud rate by gender and category
  * Fraud distribution by transaction amount range

---

## 🎯 Key Insights Enabled

* Identification of **revenue concentration (Pareto effect)**
* Detection of **seasonality and temporal patterns**
* Understanding of **customer segmentation and behavior**
* Recognition of **high-risk categories for fraud**
* Analysis of **merchant dependency and performance trends**

---

## ⚙️ How to Run the Project

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo.git
```

2. Navigate to the project folder:

```
cd your-repo
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the Streamlit app:

```
streamlit run main.py
```

---

## 📌 Notes

* The dataset is not included in the repository.
* Make sure to properly configure the `functions.py` file to load your data.
* Filters (category, gender, state, and date range) dynamically update all visualizations besides in the fraud page.
* The loading of the data may be slow at first, since is being uploaded from Hugging Faces

---

## 👨‍💻 Author

Developed by **Guilherme Pasqualette**

---

## 📄 License

This project is for educational and analytical purposes.
