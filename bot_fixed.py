# Standard library imports
import logging
import os
import json
import math
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Tuple, Dict, Any, List, Final, TypedDict, Union
from dotenv import load_dotenv

# Third-party imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
    MessageRateLimit,
    MessageThrottle
)
import aiohttp
from aiohttp import ClientTimeout
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from supabase import create_client, Client

# Local imports
from translations import TRANSLATIONS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger: logging.Logger = logging.getLogger(__name__)

# ============= Constants and Configuration =============

# API Configuration
TELEGRAM_BOT_TOKEN: Final[str] = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

BORDEAUX_API_KEY: Final[str] = os.getenv('BORDEAUX_API_KEY')
if not BORDEAUX_API_KEY:
    raise ValueError("BORDEAUX_API_KEY environment variable is not set")

BORDEAUX_API_BASE_URL: Final[str] = os.getenv('BORDEAUX_API_BASE_URL')
if not BORDEAUX_API_BASE_URL:
    raise ValueError("BORDEAUX_API_BASE_URL environment variable is not set")

# Supabase Configuration
SUPABASE_URL: Final[str] = os.getenv('SUPABASE_URL')
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is not set")

SUPABASE_KEY: Final[str] = os.getenv('SUPABASE_KEY')
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY environment variable is not set")

# API Request Settings
API_TIMEOUT: Final[int] = 10  # seconds
MAX_RETRIES: Final[int] = 3
RETRY_DELAY: Final[int] = 1  # second
RATE_LIMIT: Final[int] = 100  # requests per hour

# Initialize rate limiting
rate_limit_dict: Dict[str, List[datetime]] = defaultdict(list)

# Initialize geolocator
geolocator: Nominatim = Nominatim(user_agent="bordeaux_transport_bot")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============= Type Definitions =============

class Location(TypedDict):
    """Type definition for location data."""
    lat: float
    lon: float
    name: str

class TransportInfo(TypedDict):
    """Type definition for transport information."""
    line: str
    destination: str
    time: str
    type: str

# ============= Security Functions =============

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass

def validate_address(address: str) -> bool:
    """Validate address input.
    
    Args:
        address: The address to validate
        
    Returns:
        bool: True if address is valid, False otherwise
        
    Raises:
        SecurityError: If address is invalid
    """
    if not address or len(address) > 200:
        raise SecurityError("Invalid address length")
    
    # Add more validation as needed
    return True

def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate geographic coordinates.
    
    Args:
        lat: Latitude to validate
        lon: Longitude to validate
        
    Returns:
        bool: True if coordinates are valid
        
    Raises:
        SecurityError: If coordinates are invalid
    """
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise SecurityError("Invalid coordinates")
    return True

def validate_transport_info(info: TransportInfo) -> bool:
    """Validate transport information.
    
    Args:
        info: Transport information to validate
        
    Returns:
        bool: True if information is valid
        
    Raises:
        SecurityError: If information is invalid
    """
    if not all(key in info for key in ['line', 'destination', 'time', 'type']):
        raise SecurityError("Missing required transport information")
    
    if not info['line'] or not info['destination'] or not info['time']:
        raise SecurityError("Empty transport information")
    
    return True

async def check_rate_limit(user_id: int) -> bool:
    """Check if user has exceeded rate limit.
    
    Args:
        user_id: The user's ID to check
        
    Returns:
        bool: True if user is within rate limit, False otherwise
    """
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old requests
    rate_limit_dict[str(user_id)] = [t for t in rate_limit_dict[str(user_id)] if t > hour_ago]
    
    # Check limit
    if len(rate_limit_dict[str(user_id)]) >= RATE_LIMIT:
        return False
    
    # Add new request
    rate_limit_dict[str(user_id)].append(now)
    return True

async def check_api_rate_limit() -> bool:
    """Check if API rate limit is exceeded.
    
    Returns:
        bool: True if API is within rate limit, False otherwise
    """
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old requests
    rate_limit_dict['api'] = [t for t in rate_limit_dict['api'] if t > hour_ago]
    
    # Check limit
    if len(rate_limit_dict['api']) >= 1000:  # API rate limit
        return False
    
    # Add new request
    rate_limit_dict['api'].append(now)
    return True

async def check_user_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user session is valid.
    
    Args:
        update: The update object from Telegram
        context: The context object from Telegram
        
    Returns:
        bool: True if session is valid, False otherwise
    """
    user_id = update.effective_user.id
    
    # Check rate limit
    if not await check_rate_limit(user_id):
        return False
    
    # Check session expiration and rotate if needed
    if context.user_data.get('session_start'):
        if datetime.now() - context.user_data['session_start'] > timedelta(hours=12):
            await rotate_session_token(context)
    
    # Update session
    context.user_data['session_start'] = datetime.now()
    return True

async def validate_request(update: Update) -> bool:
    """Validate incoming requests."""
    if not update or not update.effective_user:
        return False
    
    # Validate user input
    if update.message and update.message.text:
        text = update.message.text
        if len(text) > 1000:  # Max message length
            return False
        
        # Check for potential injection attacks
        if any(char in text for char in [';', '--', '/*', '*/', 'xp_']):
            return False
    
    return True

async def log_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log all incoming requests.
    
    Args:
        update: The update object from Telegram
        context: The context object from Telegram
    """
    user_id = update.effective_user.id
    command = update.message.text if update.message else "Unknown"
    logger.info(f"Request from user {user_id}: {command}")

# ============= API Functions =============

class APIError(Exception):
    """Custom exception for API errors."""
    pass

async def make_api_request(params: Dict[str, Any], retries: int = MAX_RETRIES) -> Dict[str, Any]:
    """Make an API request with rate limiting and retry logic.
    
    Args:
        params: The parameters for the API request
        retries: Number of retry attempts
        
    Returns:
        Dict[str, Any]: The API response data
        
    Raises:
        APIError: If the API request fails
    """
    if not await check_api_rate_limit():
        raise APIError("API rate limit exceeded")
    
    timeout = ClientTimeout(total=API_TIMEOUT)
    
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {'Authorization': f'Bearer {BORDEAUX_API_KEY}'}
                async with session.get(BORDEAUX_API_BASE_URL, params=params, headers=headers) as response:
                    if response.status == 429:  # Rate limit
                        if attempt < retries - 1:
                            await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                            continue
                        raise APIError("API rate limit exceeded")
                    
                    if response.status != 200:
                        raise APIError(f"API request failed with status {response.status}")
                    
                    data = await response.json()
                    if not data:
                        raise APIError("Empty response from API")
                    
                    return data
                    
        except aiohttp.ClientError as e:
            if attempt == retries - 1:
                raise APIError(f"Network error: {str(e)}")
            await asyncio.sleep(RETRY_DELAY * (attempt + 1))
            
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                raise APIError("API request timed out")
            await asyncio.sleep(RETRY_DELAY * (attempt + 1))
            
        except json.JSONDecodeError:
            raise APIError("Invalid JSON response from API")

# ============= Database Functions =============

async def handle_database_error(operation: str, error: Exception) -> None:
    """Handle database errors consistently.
    
    Args:
        operation: The operation that failed
        error: The error that occurred
        
    Raises:
        Exception: The original error with additional context
    """
    logger.error(f"Database error during {operation}: {str(error)}")
    if "duplicate key" in str(error).lower():
        raise Exception(f"Duplicate entry during {operation}")
    elif "connection" in str(error).lower():
        raise Exception(f"Database connection error during {operation}")
    else:
        raise Exception(f"Database error during {operation}: {str(error)}")

async def save_user_location(user_id: int, location: Location) -> None:
    """Save user's location to database.
    
    Args:
        user_id: The user's ID
        location: The location data to save
        
    Raises:
        Exception: If database operation fails
    """
    try:
        await supabase.table('user_locations').insert({
            'user_id': user_id,
            'latitude': location['lat'],
            'longitude': location['lon'],
            'name': location['name'],
            'created_at': datetime.now().isoformat()
        }).execute()
    except Exception as e:
        await handle_database_error("save_user_location", e)

async def get_user_location(user_id: int) -> Optional[Location]:
    """Get user's saved location from database.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Optional[Location]: The user's location if found, None otherwise
        
    Raises:
        Exception: If database operation fails
    """
    try:
        response = await supabase.table('user_locations')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            data = response.data[0]
            return {
                'lat': data['latitude'],
                'lon': data['longitude'],
                'name': data['name']
            }
        return None
    except Exception as e:
        await handle_database_error("get_user_location", e)

# ============= Location Functions =============

async def get_location_from_address(address: str) -> Optional[Location]:
    """Get location coordinates from address.
    
    Args:
        address: The address to geocode
        
    Returns:
        Optional[Location]: The location data if found, None otherwise
    """
    try:
        validate_address(address)
        location = await geolocator.geocode(address)
        if location:
            return {
                'lat': location.latitude,
                'lon': location.longitude,
                'name': location.address
            }
        return None
    except SecurityError as e:
        logger.error(f"Security error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Geocoding error: {str(e)}")
        return None

def calculate_distance(loc1: Location, loc2: Location) -> float:
    """Calculate distance between two locations.
    
    Args:
        loc1: First location
        loc2: Second location
        
    Returns:
        float: Distance in kilometers
    """
    return geodesic(
        (loc1['lat'], loc1['lon']),
        (loc2['lat'], loc2['lon'])
    ).kilometers

# ============= Transport Functions =============

async def get_transport_info(location: Location) -> List[TransportInfo]:
    """Get transport information for a location."""
    try:
        # Validate coordinates
        validate_coordinates(location['lat'], location['lon'])
        
        params = {
            'lat': location['lat'],
            'lon': location['lon']
        }
        
        data = await make_api_request(params)
        results = []
        
        for item in data.get('results', []):
            info = {
                'line': item['line'],
                'destination': item['destination'],
                'time': item['time'],
                'type': item['type']
            }
            
            if validate_transport_info(info):
                results.append(info)
        
        return results
    except SecurityError as e:
        logger.error(f"Security error: {str(e)}")
        raise APIError(f"Invalid transport information: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to get transport info: {str(e)}")
        raise APIError(f"Failed to get transport info: {str(e)}")

# ============= Command Handlers =============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not await validate_request(update):
        return
    
    await log_request(update, context)
    
    if not await check_user_session(update, context):
        await update.message.reply_text("Session expired. Please try again.")
        return
    
    user_id = update.effective_user.id
    await update.message.reply_text(
        TRANSLATIONS['welcome'],
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(TRANSLATIONS['set_location'], callback_data='set_location')],
            [InlineKeyboardButton(TRANSLATIONS['get_transport'], callback_data='get_transport')]
        ])
    )

async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle location setting."""
    if not await validate_request(update):
        return
    
    await log_request(update, context)
    
    if not await check_user_session(update, context):
        await update.message.reply_text("Session expired. Please try again.")
        return
    
    user_id = update.effective_user.id
    
    try:
        # Get and validate address
        address = update.message.text.strip()
        if not address:
            await update.message.reply_text("Please provide a valid address.")
            return
        
        # Get location
        location = await get_location_from_address(address)
        if not location:
            await update.message.reply_text("Could not find location. Please try again.")
            return
        
        # Save location
        await save_user_location(user_id, location)
        
        await update.message.reply_text(
            TRANSLATIONS['current_location'].format(location['name']),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TRANSLATIONS['change_location'], callback_data='change_location')]
            ])
        )
    except SecurityError as e:
        await update.message.reply_text("Invalid location. Please try again.")
        logger.error(f"Security error in set_location: {str(e)}")
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again.")
        logger.error(f"Error in set_location: {str(e)}")

async def get_transport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle transport information request."""
    if not await validate_request(update):
        return
    
    await log_request(update, context)
    
    if not await check_user_session(update, context):
        await update.message.reply_text("Session expired. Please try again.")
        return
    
    user_id = update.effective_user.id
    location = await get_user_location(user_id)
    
    if not location:
        await update.message.reply_text(TRANSLATIONS['no_location'])
        return
    
    try:
        transport_info = await get_transport_info(location)
        if not transport_info:
            await update.message.reply_text(TRANSLATIONS['no_transport'])
            return
        
        message = TRANSLATIONS['transport_info'].format(location['name'])
        for info in transport_info:
            message += f"\n{info['line']} - {info['destination']} ({info['time']})"
        
        await update.message.reply_text(message)
    except APIError as e:
        await update.message.reply_text(TRANSLATIONS['api_error'])
        logger.error(f"API error: {str(e)}")

# ============= Session Management =============

async def rotate_session_token(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Rotate session token for security.
    
    Args:
        context: The context object from Telegram
        
    Returns:
        str: New session token
    """
    token = os.urandom(32).hex()
    context.user_data['session_token'] = token
    context.user_data['session_start'] = datetime.now()
    return token

# ============= Main Function =============

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_location", set_location))
    application.add_handler(CommandHandler("get_transport", get_transport))
    
    # Add rate limiting
    application.add_handler(MessageRateLimit(rate_limit=100, per=3600))
    application.add_handler(MessageThrottle(rate_limit=10, per=60))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main() 