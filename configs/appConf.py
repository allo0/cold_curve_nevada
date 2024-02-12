import pyautogui


class Settings:
    PROJECT_NAME: str = "Cold Curve Nevada"
    PROJECT_VERSION: str = "0.0.1alpha"

    LOG_DISPLAY_DURATION = 8  # Display each message for X messages
    ENABLE_ON_SCREEN_LOGS = True
    ENABLE_LOGS = True

    # Define constants for the game_screen width and height
    SCREEN_WIDTH: int = pyautogui.size().width / 2
    SCREEN_HEIGHT: int = pyautogui.size().height / 2
    RESOLUTION: tuple = (SCREEN_WIDTH, SCREEN_HEIGHT)

    FPS = 60

    # API_URL = "http://127.0.0.1:8000"
    #
    #
    #
    # swagger_ui_parameters = {
    #     "syntaxHighlight.theme": "obsidian"
    # }
    # swagger_ui_default_parameters = {
    #     "dom_id": "#swagger-ui",
    #     "layout": "BaseLayout",
    #     "deepLinking": True,
    #     "showExtensions": True,
    #     "showCommonExtensions": True,
    # }
    #
    # origins = [
    #     "*",
    # ]
    # middleware = [
    #     Middleware(
    #         CORSMiddleware,
    #         allow_origins=origins,
    #         allow_credentials=True,
    #         allow_methods=['*'],
    #         allow_headers=['*'],
    #         expose_headers=['*']
    #     )
    # ]
