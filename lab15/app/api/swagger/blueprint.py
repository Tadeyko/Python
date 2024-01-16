from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  
API_URL = '/swagger'

api_swagger = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={ 
        'app_name': "My app"
    },
)