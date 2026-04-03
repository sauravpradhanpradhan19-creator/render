mkdir -p ~/.streamlit

echo "[server]
port = $PORT
enableCORS = false
headless = true
address = 0.0.0.0
" > ~/.streamlit/config.toml