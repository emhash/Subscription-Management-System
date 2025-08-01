import os
import sys
from dotenv import load_dotenv
load_dotenv()

def main():
    load_dotenv()
    try:
        settings_module = os.getenv('DJANGO_SETTINGS_MODULE')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        print(f"#####---===>> Using settings module: {settings_module}")

    except KeyError:
        raise KeyError(
            "DJANGO_SETTINGS_MODULE environment variable is not set. "
            "Please set it to your Django settings module."
        )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()