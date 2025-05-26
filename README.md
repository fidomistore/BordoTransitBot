# Bordeaux Transport Bot

A Telegram bot for accessing Bordeaux public transport information.

## Features

- Real-time bus arrival information
- Line and stop information
- Route planning
- Service disruptions
- Multi-language support (FR, EN, ES)
- Favorite stops
- Reminders
- User preferences

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd bordeaux-transport-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Bordeaux API
BORDEAUX_API_KEY=your_bordeaux_api_key
BORDEAUX_API_BASE_URL=https://opendata.bordeaux-metropole.fr/api/records/1.0/search/

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

5. Set up the Supabase database:
   - Create a new project in Supabase
   - Run the SQL commands from `supabase_setup.sql` in the Supabase SQL editor
   - Copy the project URL and anon key to your `.env` file

## Running the Bot

```bash
python bot_enhanced.py
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys and tokens secure
- Regularly rotate your API keys and tokens
- Use environment variables in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Commands

- `/start` - Start the bot and see available commands
- `/help` - Display help message
- `/next_bus <stop_name>` - Get next bus arrivals at a specific stop
- `/lines` - List all available transport lines

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment on Render.com

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn bot:main`
4. Add the following environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `BORDEAUX_API_KEY`: Your Bordeaux Métropole API key

## API Documentation

This bot uses the Bordeaux Métropole OpenData API. For more information about the API, visit:
https://opendata.bordeaux-metropole.fr/ 