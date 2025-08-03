import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
load_dotenv()
try:
    settings_module = os.getenv('SETTINGS_MODULE')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    print(f"#####---===>> In WSGI - settings module: {settings_module}")

except KeyError:
    raise KeyError(
        "DJANGO_SETTINGS_MODULE environment variable is not set. "
        "Please set it to your Django settings module."
    )

application = get_wsgi_application()
