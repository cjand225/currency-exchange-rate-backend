import os


class Config:
    """
    Base configuration class.

    This class provides default configurations for the application. It can be extended by child classes
    to override configurations for specific environments.
    """
    ENV = "development"  # Default environment
    ORIGINS = []  # Default allowed origins for CORS


class DevelopmentConfig(Config):
    """
    Development-specific configurations.

    This class extends the base Config class and overrides configurations specific to the development environment.
    """
    ORIGINS = ['http://localhost:3000', 'https://localhost:3000']


class ProductionConfig(Config):
    """
    Production-specific configurations.

    This class extends the base Config class and overrides configurations specific to the production environment.
    """
    ENV = "production"
    ORIGINS = ['http://localhost:3000', 'https://localhost:3000', 'http://localhost:3000/exchange-rate-app', 'https://localhost:3000/exchange-rate-app']


def get_config():
    """
    Determine the configuration to use based on the ENV environment variable.

    Returns:
        class: A configuration class (either DevelopmentConfig or ProductionConfig).

    Note:
        If the ENV environment variable is not set, it defaults to the development configuration.
    """
    env = os.getenv("ENV", default="development")
    if env == "production":
        return ProductionConfig
    else:
        return DevelopmentConfig
