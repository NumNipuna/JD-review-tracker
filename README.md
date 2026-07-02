# 📋 Job Description Review Tracker

An interactive, corporate-themed data science dashboard built with **Streamlit** and **Plotly** to monitor, track, and audit the completion status of Master Job Descriptions across dynamic company departments.

---

## 🚀 Live Demo
👉 [View the Live Dashboard](https://share.streamlit.io/)

---

## ⚙️ Core Features

* **Real-time Live Sync:** Bypasses operational memory limits with a custom cache-busting architecture to dynamically reload dataset updates from the core Excel sheet in under 5 seconds.
* **Dynamic KPI Metrics:** Instantly counts total workloads, completed tasks, ongoing task backlogs, and micro-calculates execution completion percentages across selected filter bounds.
* **Interactive Data Visualizations:**
    * **Overall Status Breakdown:** A clean, custom-mapped Plotly Donut/Pie Chart handling task states.
    * **Progress by Department:** A horizontal stacked bar chart breaking down operational volumes.
    * **Role Drill-Down Heatmap:** A responsive data matrix displaying exact percentage rates for specific roles.
* **One-Click Snapshots:** Built-in automated browser capture script utilizing `html2canvas.js` to instantly download a high-definition (`scale: 2`) PNG copy of the dashboard for meetings and PowerPoint presentations.
* **Granular Filters:** Multi-select options in the sidebar to drill down cleanly by Department or specific Job Titles.

---

## 🛠️ Tech Stack & Requirements

This system runs on Python 3.x and leverages several core open-source libraries:

* **Streamlit** - User Interface & Core Dashboard Engine
* **Pandas** - Data Wrangling & Analytical Aggrigations
* **Plotly & Plotly Graph Objects** - High-Fidelity Custom Charts
* **Openpyxl** - Excel File Processing
* **Pillow (PIL)** - Static Asset Management
* **html2canvas** - JavaScript-Injected Web Snapshot Capture

---

## 📁 Repository Structure

```text
├── app.py                  # The primary Streamlit application execution script
├── requirements.txt        # Virtual environment library dependency manifest
├── Master JD.xlsx          # Core relational Excel file (Vstak Sheet)
├── logo.png                # Corporate brand asset container
└── README.md               # Documentation and execution guide
