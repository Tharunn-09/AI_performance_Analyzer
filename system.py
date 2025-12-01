import psutil
import time
import numpy as np
import webview
import threading
import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from collections import deque

app = Flask(__name__)
CORS(app)

# --- Data Buffers ---
cpu_history = deque(maxlen=120)
iso_forest = IsolationForest(contamination=0.1)

# Global variables for Network Speed calculation
last_net_io = psutil.net_io_counters()
last_time = time.time()

def get_optimizations(cpu_percent, mem_percent, anomalies):
    suggestions = []
    # Added explicit severity levels for the frontend to read
    if cpu_percent > 85:
        suggestions.append({"type": "CRITICAL", "msg": "CPU Saturation. Throttle background workers."})
    elif cpu_percent > 50 and "cpu_anomaly" in anomalies:
        suggestions.append({"type": "WARNING", "msg": "Unusual CPU spike detected."})
    
    if mem_percent > 90:
        suggestions.append({"type": "CRITICAL", "msg": "Memory near capacity. Restart required."})
    
    if not suggestions:
        suggestions.append({"type": "NORMAL", "msg": "System operating within normal AI parameters."})
    return suggestions

@app.route('/kill_process', methods=['POST'])
def kill_process():
    try:
        data = request.json
        pid = int(data.get('pid'))
        parent = psutil.Process(pid)
        parent.kill() # Force Kill
        return jsonify({"success": True, "message": f"Terminated PID {pid}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/analyze')
def analyze_system():
    global last_net_io, last_time
    
    # 1. CPU & Mem
    cpu = min(100, psutil.cpu_percent(interval=None))
    mem = psutil.virtual_memory()
    
    # 2. Network Speed Calculation
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    time_delta = current_time - last_time
    
    # Bytes per second
    sent_bytes_sec = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_delta
    recv_bytes_sec = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_delta
    
    # Update globals for next tick
    last_net_io = current_net_io
    last_time = current_time
    
    # 3. AI Forecast Logic
    cpu_history.append([current_time, cpu])
    forecast_msg = "Gathering data..."
    forecast_trend = []
    
    if len(cpu_history) > 20:
        history_array = np.array(list(cpu_history))
        X = history_array[:, 0].reshape(-1, 1)
        y = history_array[:, 1]
        volatility = np.std(y)
        model = LinearRegression().fit(X, y)
        future_times = np.array([[current_time + i*2] for i in range(1, 31)])
        base_trend = model.predict(future_times).flatten()
        noise = np.random.normal(0, volatility * 0.8, len(base_trend))
        forecast_trend = [max(0, min(100, p)) for p in (base_trend + noise)]
        forecast_msg = f"Forecast: CPU likely to hit {np.mean(forecast_trend):.1f}% range."

    # 4. Anomaly Detection
    anomalies = []
    if len(cpu_history) > 30:
        data = np.array([x[1] for x in cpu_history]).reshape(-1, 1)
        iso_forest.fit(data)
        if iso_forest.predict([[cpu]])[0] == -1:
            anomalies.append("cpu_anomaly")

    # 5. Process List
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            p = proc.info
            if p['cpu_percent'] > 0.1 and p['name'] not in ('System Idle Process', 'System', 'Registry'):
                processes.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    return jsonify({
        "metrics": { 
            "cpu": cpu, 
            "memory": mem.percent, 
            "disk": psutil.disk_usage('/').percent,
            "net_sent": sent_bytes_sec, # Send raw bytes, frontend formats it
            "net_recv": recv_bytes_sec
        },
        "analysis": { 
            "forecast": forecast_msg, 
            "forecast_trend": forecast_trend,
            "optimizations": get_optimizations(cpu, mem.percent, anomalies), 
            "bottlenecks": sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5] 
        }
    })

@app.route('/')
def index():
    if os.path.exists('dashboard.html'):
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Error: dashboard.html not found</h1>"

def start_server():
    app.run(host='127.0.0.1', port=5000, threaded=True)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    webview.create_window("SysOpt AI Monitor", "http://127.0.0.1:5000", width=1280, height=850, background_color='#020617')
    webview.start()
    sys.exit()