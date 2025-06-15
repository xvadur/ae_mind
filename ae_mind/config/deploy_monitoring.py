#!/usr/bin/env python3
"""
Grafana Monitoring Deployment and Configuration Script
"""
import argparse
import requests
import json
import time
import sys
import os
from pathlib import Path

def setup_grafana():
    """Configure Grafana with optimized settings"""
    grafana_url = "http://localhost:3000"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # Wait for Grafana to be ready
    print("Waiting for Grafana to be ready...")
    retries = 30
    while retries > 0:
        try:
            response = requests.get(f"{grafana_url}/api/health")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        retries -= 1
    
    if retries == 0:
        print("Error: Grafana is not responding")
        sys.exit(1)

    # Load dashboard configuration
    dashboard_path = Path(__file__).parent.parent / "monitoring" / "grafana_dashboards.json"
    with open(dashboard_path) as f:
        dashboard_config = json.load(f)

    # Configure data source
    datasource = {
        "name": "Prometheus",
        "type": "prometheus",
        "url": "http://prometheus:9090",
        "access": "proxy",
        "isDefault": True
    }
    
    response = requests.post(
        f"{grafana_url}/api/datasources",
        headers=headers,
        json=datasource,
        auth=("admin", "aetheros_admin")
    )
    
    if response.status_code not in [200, 409]:  # 409 means already exists
        print(f"Error configuring datasource: {response.text}")
        sys.exit(1)

    # Deploy dashboard
    dashboard_payload = {
        "dashboard": dashboard_config,
        "overwrite": True
    }
    
    response = requests.post(
        f"{grafana_url}/api/dashboards/db",
        headers=headers,
        json=dashboard_payload,
        auth=("admin", "aetheros_admin")
    )
    
    if response.status_code != 200:
        print(f"Error deploying dashboard: {response.text}")
        sys.exit(1)

    # Configure alerting
    alerting_config = {
        "alertmanagerUid": "alertmanager",
        "name": "Alertmanager",
        "type": "alertmanager",
        "url": "http://alertmanager:9093",
        "isDefault": True
    }
    
    response = requests.post(
        f"{grafana_url}/api/alertmanager/alertmanagers",
        headers=headers,
        json=alerting_config,
        auth=("admin", "aetheros_admin")
    )
    
    if response.status_code not in [200, 409]:
        print(f"Error configuring alerting: {response.text}")
        sys.exit(1)

    print("Grafana configuration completed successfully")

def main():
    parser = argparse.ArgumentParser(description="Deploy and configure Grafana monitoring")
    parser.add_argument("--force-reconfigure", action="store_true", 
                      help="Force reconfiguration of existing settings")
    args = parser.parse_args()

    try:
        setup_grafana()
    except Exception as e:
        print(f"Error during deployment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
