#!/usr/bin/env python3
"""
SSL Certificate Setup Script for Streamlit App
This script helps resolve SSL certificate issues on Windows
"""

import os
import ssl
import certifi
import subprocess
import sys

def setup_ssl_certificates():
    """Set up SSL certificates for the application"""
    print("🔧 Setting up SSL certificates...")
    
    # Get the path to certifi's certificates
    certifi_path = certifi.where()
    print(f"📁 Certificate path: {certifi_path}")
    
    # Set environment variables
    os.environ['SSL_CERT_FILE'] = certifi_path
    os.environ['REQUESTS_CA_BUNDLE'] = certifi_path
    os.environ['CURL_CA_BUNDLE'] = certifi_path
    
    print("✅ SSL certificates configured")
    print(f"   SSL_CERT_FILE: {os.environ.get('SSL_CERT_FILE')}")
    print(f"   REQUESTS_CA_BUNDLE: {os.environ.get('REQUESTS_CA_BUNDLE')}")

def install_certifi():
    """Install certifi if not already installed"""
    try:
        import certifi
        print("✅ certifi is already installed")
    except ImportError:
        print("📦 Installing certifi...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "certifi"])
        print("✅ certifi installed successfully")

def main():
    print("🚀 SSL Certificate Setup for Samvedna Chatbot")
    print("=" * 50)
    
    # Install certifi if needed
    install_certifi()
    
    # Set up SSL certificates
    setup_ssl_certificates()
    
    print("\n🎉 Setup complete!")
    print("You can now run: streamlit run samvedhna_chatbot/streamlit_app.py")

if __name__ == "__main__":
    main() 