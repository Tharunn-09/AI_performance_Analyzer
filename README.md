SysOpt AI Monitor 🧠⚡
SysOpt AI is a hybrid desktop application that combines real-time system monitoring with Machine Learning. Unlike standard task managers, SysOpt uses predictive algorithms to forecast CPU usage trends and detect anomalies in system behavior, providing actionable insights and voice-actuated alerts.

📸 Project Screenshot
<img width="1689" height="1086" alt="image" src="https://github.com/user-attachments/assets/535e5831-9325-4ca4-938a-e22fc59b568b" />

🚀 Key Features
Real-Time Monitoring: Live tracking of CPU, Memory, Disk usage, and Network upload/download speeds.

AI Forecasting: Uses Linear Regression to predict CPU load trends 60 seconds into the future based on historical volatility.

Anomaly Detection: Implements an Isolation Forest algorithm to identify unusual CPU spikes that deviate from normal operating patterns.

Smart Optimizations: Provides dynamic suggestions (Normal, Warning, Critical) based on system saturation levels.

Process Management: Identify top CPU-consuming bottlenecks and force-terminate processes directly from the UI.

Voice Alerts: Integrated Text-to-Speech (TTS) engine provides audible alerts when critical system thresholds are breached.

Desktop GUI: Runs as a standalone desktop application using a lightweight webview wrapper.

🛠️ Tech Stack
Backend (Python)
Flask: Serves the API and manages processes.

Psutil: Retrieves system metrics and process information.

Scikit-Learn: Powering the AI modules (LinearRegression & IsolationForest).

Numpy: Data handling for metric history buffers.

Pywebview: Renders the web interface as a native GUI window.

Frontend (React & Tailwind)
React: Component-based UI for dynamic graph rendering.

Tailwind CSS: Modern, utility-first styling for the dark-mode dashboard.

Babel: In-browser compilation (No Node.js build step required).

⚙️ Installation & Setup
1. Clone the Repository
Bash

git clone https://github.com/yourusername/SysOpt-AI.git
cd SysOpt-AI
2. Install Dependencies
Ensure you have Python installed, then run:

Bash

pip install flask flask-cors psutil numpy scikit-learn pywebview
3. Run the Application
Start the application by running the main system script. This will launch the backend server and open the GUI window automatically.

Bash

python system.py
🧠 AI Logic Explained
This project utilizes two specific ML approaches implemented in system.py:

Trend Prediction (Linear Regression): The system maintains a rolling buffer of the last 120 CPU data points. A Linear Regression model fits this data to project a trend line for the next 60 seconds, allowing the user to see if their system load is stabilizing or escalating.

Anomaly Detection (Isolation Forest): An unsupervised learning algorithm (IsolationForest) runs against the CPU history. It isolates observations by randomly selecting a feature and then randomly selecting a split value. Outliers (anomalies) are easier to isolate and are flagged to the user as "Unusual CPU spikes".

📂 Project Structure
Ai-Performance_Analyzer/
├── system.py          # Main entry point, Flask backend, and AI logic
├── dashboard.html     # React frontend and UI visualization
└── README.md          # Project documentation
⚠️ Disclaimer
This tool includes the ability to terminate active processes (os.kill). Please use the "Kill Process" feature with caution, as terminating critical system processes may cause instability.

🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements, such as adding GPU monitoring or improving the prediction model.
