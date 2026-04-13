# COMP7940 Chatbot Project README

A Telegram-based AI chatbot deployed on AWS EC2, with Docker containerization for stable operation.

## 1. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Configure credentials in config.ini first, then start the bot
python chatbot.py
```

## 2. Docker Deployment

```bash
# Build Docker image
docker build -t telegram-bot .

# Run container (auto-restart on reboot)
docker run -d --restart always telegram-bot
```

## 3. Project Structure

- `chatbot.py` - Main bot entry, handles message interaction

- `ChatGPT_HKBU.py` - HKBU LLM API wrapper, manages chat requests

- `Dockerfile` - Docker image configuration

- `requirements.txt` - Project dependencies list

- `config.ini` - Sensitive config (bot token, API key), not committed to Git

- `.gitignore` - Excludes sensitive files and temporary data

## 4. Configuration (config.ini)

```ini
[TELEGRAM]
TOKEN = your_telegram_bot_token_here

[CHATGPT]
API_KEY = your_hkbu_llm_api_key_here
BASE_URL = https://genai.hkbu.edu.hk/
```

## 5. Verification & Testing

```bash
# Check container status
docker ps

# Check runtime logs
docker logs <container_id>
```

Verify bot can receive/send messages normally, no runtime errors.

## 6. Notes

- This project uses a personal AWS account for deployment.

- Sensitive information (token, API key) is not committed to Git for security.

- The bot uses long-polling mode, no public port exposure needed.

## 7. Dependencies

python-telegram-bot, httpx, redis, configparser, and supporting network libraries.

## License

For academic use only, COMP7940 Cloud Computing Lab Project.