TRANSLATIONS = {
    'fr': {
        'welcome': (
            "👋 Bienvenue sur le Bot de Transport Bordeaux Métropole!\n\n"
            "Commandes disponibles:\n"
            "/next_bus <arrêt> - Prochains passages à un arrêt\n"
            "/lines - Liste des lignes de transport\n"
            "/stops <ligne> - Liste des arrêts d'une ligne\n"
            "/times <ligne> <arrêt> - Horaires complets d'une ligne à un arrêt\n"
            "/disruptions - Perturbations actuelles\n"
            "/nearby <lieu> - Arrêts à proximité\n"
            "/route <départ> <arrivée> - Itinéraire entre deux arrêts\n"
            "/status - État du réseau\n"
            "/favorites - Gérer vos arrêts favoris\n"
            "/reminder - Définir des rappels\n"
            "/settings - Paramètres du bot\n"
            "/language - Changer la langue\n"
            "/help - Affiche ce message d'aide"
        ),
        'help': (
            "📱 Commandes disponibles:\n\n"
            "Informations de base:\n"
            "• /next_bus <arrêt> - Prochains passages à un arrêt\n"
            "• /lines - Liste des lignes de transport\n"
            "• /stops <ligne> - Liste des arrêts d'une ligne\n"
            "• /times <ligne> <arrêt> - Horaires complets\n\n"
            "Informations en temps réel:\n"
            "• /disruptions - Perturbations actuelles\n"
            "• /status - État du réseau\n"
            "• /nearby <lieu> - Arrêts à proximité\n\n"
            "Fonctionnalités avancées:\n"
            "• /route <départ> <arrivée> - Itinéraire\n"
            "• /favorites - Gérer vos arrêts favoris\n"
            "• /reminder - Définir des rappels\n"
            "• /settings - Paramètres du bot\n"
            "• /language - Changer la langue\n\n"
            "Exemples:\n"
            "/next_bus Gambetta\n"
            "/stops 1\n"
            "/times 1 Gambetta\n"
            "/nearby Place de la Victoire\n"
            "/route Gambetta Quinconces"
        ),
        'no_stop': "Veuillez spécifier un arrêt. Exemple: /next_bus Gambetta",
        'no_line': "Veuillez spécifier une ligne. Exemple: /stops 1",
        'no_location': "Veuillez spécifier un lieu. Exemple: /nearby Place de la Victoire",
        'no_route': "Veuillez spécifier le départ et l'arrivée. Exemple: /route Gambetta Quinconces",
        'no_stop_found': "Aucun arrêt trouvé pour '{}'",
        'no_line_found': "Aucun arrêt trouvé pour la ligne {}",
        'no_schedule': "Aucun horaire trouvé pour la ligne {} à l'arrêt {}",
        'no_disruptions': "Aucune perturbation signalée actuellement",
        'no_nearby': "Aucun arrêt trouvé à proximité",
        'location_not_found': "Lieu '{}' non trouvé",
        'no_direct_route': "Aucune ligne directe trouvée. Veuillez consulter le site TBM pour un itinéraire complet.",
        'error': "Désolé, une erreur s'est produite lors de la recherche.",
        'invalid_time': "Format d'heure invalide. Utilisez HH:MM",
        'reminder_set': "✅ Rappel configuré pour la ligne {} à l'arrêt {} à {}",
        'no_favorites': "Vous n'avez pas encore d'arrêts favoris.",
        'favorite_added': "{} ajouté à vos favoris",
        'favorite_removed': "{} supprimé de vos favoris",
        'favorite_exists': "{} est déjà dans vos favoris",
        'favorite_not_found': "{} n'est pas dans vos favoris",
        'settings_updated': "✅ Paramètre '{}' mis à jour",
        'language_changed': "✅ Langue changée en français",
        'select_language': "Choisissez votre langue / Choose your language / Elija su idioma:",
        'next_bus_title': "Prochains passages à {}",
        'stops_title': "Arrêts de la ligne {}",
        'schedule_title': "Horaires de la ligne {} à {}",
        'no_schedule_params': "Veuillez spécifier une ligne et un arrêt. Exemple: /times 1 Gambetta",
        'api_error': "Désolé, une erreur s'est produite lors de la communication avec l'API de transport.",
        'timeout_error': "La requête a pris trop de temps. Veuillez réessayer.",
        'unexpected_error': "Une erreur inattendue s'est produite. Veuillez réessayer plus tard.",
        'invalid_reminder_format': "Format de rappel invalide. Utilisez: /reminder <ligne> <arrêt> <heure>",
        'invalid_line': "Numéro de ligne invalide.",
        'invalid_stop': "Nom d'arrêt invalide.",
        'invalid_time_format': "Format d'heure invalide. Utilisez HH:MM",
        'no_departures': "Aucun départ prévu pour le moment.",
        'no_lines': "Aucune ligne de transport disponible.",
    },
    'en': {
        'welcome': (
            "👋 Welcome to the Bordeaux Transport Bot!\n\n"
            "Available commands:\n"
            "/next_bus <stop> - Next departures at a stop\n"
            "/lines - List of transport lines\n"
            "/stops <line> - List of stops for a line\n"
            "/times <line> <stop> - Complete schedule for a line at a stop\n"
            "/disruptions - Current disruptions\n"
            "/nearby <location> - Stops near a location\n"
            "/route <start> <end> - Route between two stops\n"
            "/status - Network status\n"
            "/favorites - Manage favorite stops\n"
            "/reminder - Set reminders\n"
            "/settings - Bot settings\n"
            "/language - Change language\n"
            "/help - Show this help message"
        ),
        'help': (
            "📱 Available commands:\n\n"
            "Basic information:\n"
            "• /next_bus <stop> - Next departures at a stop\n"
            "• /lines - List of transport lines\n"
            "• /stops <line> - List of stops for a line\n"
            "• /times <line> <stop> - Complete schedule\n\n"
            "Real-time information:\n"
            "• /disruptions - Current disruptions\n"
            "• /status - Network status\n"
            "• /nearby <location> - Nearby stops\n\n"
            "Advanced features:\n"
            "• /route <start> <end> - Route planning\n"
            "• /favorites - Manage favorite stops\n"
            "• /reminder - Set reminders\n"
            "• /settings - Bot settings\n"
            "• /language - Change language\n\n"
            "Examples:\n"
            "/next_bus Gambetta\n"
            "/stops 1\n"
            "/times 1 Gambetta\n"
            "/nearby Place de la Victoire\n"
            "/route Gambetta Quinconces"
        ),
        'no_stop': "Please specify a stop. Example: /next_bus Gambetta",
        'no_line': "Please specify a line. Example: /stops 1",
        'no_location': "Please specify a location. Example: /nearby Place de la Victoire",
        'no_route': "Please specify start and end. Example: /route Gambetta Quinconces",
        'no_stop_found': "No stop found for '{}'",
        'no_line_found': "No stops found for line {}",
        'no_schedule': "No schedule found for line {} at stop {}",
        'no_disruptions': "No disruptions currently reported",
        'no_nearby': "No stops found nearby",
        'location_not_found': "Location '{}' not found",
        'no_direct_route': "No direct line found. Please check the TBM website for a complete route.",
        'error': "Sorry, an error occurred during the search.",
        'invalid_time': "Invalid time format. Use HH:MM",
        'reminder_set': "✅ Reminder set for line {} at stop {} at {}",
        'no_favorites': "You don't have any favorite stops yet.",
        'favorite_added': "{} added to your favorites",
        'favorite_removed': "{} removed from your favorites",
        'favorite_exists': "{} is already in your favorites",
        'favorite_not_found': "{} is not in your favorites",
        'settings_updated': "✅ Setting '{}' updated",
        'language_changed': "✅ Language changed to English",
        'select_language': "Choose your language / Choisissez votre langue / Elija su idioma:",
        'next_bus_title': "Next departures at {}",
        'stops_title': "Stops for line {}",
        'schedule_title': "Schedule for line {} at {}",
        'no_schedule_params': "Please specify a line and stop. Example: /times 1 Gambetta",
        'api_error': "Sorry, an error occurred while communicating with the transport API.",
        'timeout_error': "The request took too long. Please try again.",
        'unexpected_error': "An unexpected error occurred. Please try again later.",
        'invalid_reminder_format': "Invalid reminder format. Use: /reminder <line> <stop> <time>",
        'invalid_line': "Invalid line number.",
        'invalid_stop': "Invalid stop name.",
        'invalid_time_format': "Invalid time format. Use HH:MM",
        'no_departures': "No departures scheduled at the moment.",
        'no_lines': "No transport lines available.",
    },
    'es': {
        'welcome': (
            "👋 ¡Bienvenido al Bot de Transporte de Burdeos!\n\n"
            "Comandos disponibles:\n"
            "/next_bus <parada> - Próximas salidas en una parada\n"
            "/lines - Lista de líneas de transporte\n"
            "/stops <línea> - Lista de paradas de una línea\n"
            "/times <línea> <parada> - Horario completo de una línea en una parada\n"
            "/disruptions - Disrupciones actuales\n"
            "/nearby <ubicación> - Paradas cercanas\n"
            "/route <inicio> <fin> - Ruta entre dos paradas\n"
            "/status - Estado de la red\n"
            "/favorites - Gestionar paradas favoritas\n"
            "/reminder - Establecer recordatorios\n"
            "/settings - Configuración del bot\n"
            "/language - Cambiar idioma\n"
            "/help - Mostrar este mensaje de ayuda"
        ),
        'help': (
            "📱 Comandos disponibles:\n\n"
            "Información básica:\n"
            "• /next_bus <parada> - Próximas salidas en una parada\n"
            "• /lines - Lista de líneas de transporte\n"
            "• /stops <línea> - Lista de paradas de una línea\n"
            "• /times <línea> <parada> - Horario completo\n\n"
            "Información en tiempo real:\n"
            "• /disruptions - Disrupciones actuales\n"
            "• /status - Estado de la red\n"
            "• /nearby <ubicación> - Paradas cercanas\n\n"
            "Características avanzadas:\n"
            "• /route <inicio> <fin> - Planificación de rutas\n"
            "• /favorites - Gestionar paradas favoritas\n"
            "• /reminder - Establecer recordatorios\n"
            "• /settings - Configuración del bot\n"
            "• /language - Cambiar idioma\n\n"
            "Ejemplos:\n"
            "/next_bus Gambetta\n"
            "/stops 1\n"
            "/times 1 Gambetta\n"
            "/nearby Place de la Victoire\n"
            "/route Gambetta Quinconces"
        ),
        'no_stop': "Por favor, especifique una parada. Ejemplo: /next_bus Gambetta",
        'no_line': "Por favor, especifique una línea. Ejemplo: /stops 1",
        'no_location': "Por favor, especifique una ubicación. Ejemplo: /nearby Place de la Victoire",
        'no_route': "Por favor, especifique inicio y fin. Ejemplo: /route Gambetta Quinconces",
        'no_stop_found': "No se encontró parada para '{}'",
        'no_line_found': "No se encontraron paradas para la línea {}",
        'no_schedule': "No se encontró horario para la línea {} en la parada {}",
        'no_disruptions': "No hay disrupciones reportadas actualmente",
        'no_nearby': "No se encontraron paradas cercanas",
        'location_not_found': "Ubicación '{}' no encontrada",
        'no_direct_route': "No se encontró línea directa. Por favor, consulte el sitio web de TBM para una ruta completa.",
        'error': "Lo sentimos, ocurrió un error durante la búsqueda.",
        'invalid_time': "Formato de hora inválido. Use HH:MM",
        'reminder_set': "✅ Recordatorio configurado para la línea {} en la parada {} a las {}",
        'no_favorites': "Aún no tiene paradas favoritas.",
        'favorite_added': "{} añadido a sus favoritos",
        'favorite_removed': "{} eliminado de sus favoritos",
        'favorite_exists': "{} ya está en sus favoritos",
        'favorite_not_found': "{} no está en sus favoritos",
        'settings_updated': "✅ Configuración '{}' actualizada",
        'language_changed': "✅ Idioma cambiado a español",
        'select_language': "Choose your language / Choisissez votre langue / Elija su idioma:",
        'next_bus_title': "Próximas salidas en {}",
        'stops_title': "Paradas de la línea {}",
        'schedule_title': "Horario de la línea {} en {}",
        'no_schedule_params': "Por favor, especifique una línea y una parada. Ejemplo: /times 1 Gambetta",
        'api_error': "Lo sentimos, ocurrió un error al comunicarse con la API de transporte.",
        'timeout_error': "La solicitud tomó demasiado tiempo. Por favor, inténtelo de nuevo.",
        'unexpected_error': "Ocurrió un error inesperado. Por favor, inténtelo más tarde.",
        'invalid_reminder_format': "Formato de recordatorio inválido. Use: /reminder <línea> <parada> <hora>",
        'invalid_line': "Número de línea inválido.",
        'invalid_stop': "Nombre de parada inválido.",
        'invalid_time_format': "Formato de hora inválido. Use HH:MM",
        'no_departures': "No hay salidas programadas en este momento.",
        'no_lines': "No hay líneas de transporte disponibles.",
    }
} 