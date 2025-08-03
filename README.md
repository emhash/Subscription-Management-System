# Subscription Management System
A subscription management system with MVT architecture and REST API


## Highlighted Features

### 1. Environment-Based Settings Management
The system supports multiple environment configurations for flexible deployment:

**Development (Default):**
```bash
SETTINGS_MODULE=core.settings.local
```
- Uses SQLite3 database
- Debug mode enabled
- Local development optimizations

**Production:**
```bash
SETTINGS_MODULE=core.settings.production
```
- Uses MySQL database
- Debug mode disabled
- Production security settings

### 2. Centralized API Response Management
The `respond` folder contains a sophisticated response management system:

**StandardizedJSONRenderer** (`respond/renderers.py`):
- Automatically standardizes all API responses
- Consistent response format across all endpoints
- Proper error handling and validation
- Clean JSON structure with success/error indicators

**Response Format:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Operation successful",
    "data": {...}
}
```

**Error Handling:**
```json
{
    "success": false,
    "status_code": 400,
    "message": "Validation error occurred.",
    "error_details": {
        "field": "plan_id",
        "message": "This field is required."
    }
}
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/emhash/Subscription-Management-System.git
cd subscribe
```

### 2. Environment Setup
```bash
python -m venv venv
source venv/bin/activate
```
On Windows:
```bash
source venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.save .env
```
Edit `.env` with your configuration

### 5. Database Setup
```bash
python manage.py migrate
python manage.py create_sample_data
python manage.py createsuperuser
```

### Management Commands
Custom Django management commands for system administration:

**Create Sample Data:**
```bash
python manage.py create_sample_data
```
- Creates test users, plans, and subscriptions
- Populates database with realistic data
- Perfect for development and testing

**Test Celery Tasks:**
```bash
python manage.py test_celery
```
- Tests background task execution
- Validates Celery configuration
- Ensures periodic tasks are working

### 6. Run the Server
```bash
python manage.py runserver
```
Run Celery:
```bash
celery -A core worker --loglevel=INFO --pool=solo
```
Run Celery Beat:
```bash
celery -A core beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Project Architecture:

### Directory Structure
```
subscribe/
├── core/
│   ├── settings/
│   │   ├── configurations/
│   │   │   ├── restapi.py
│   │   │   ├── celery_settings.py
│   │   │   └── content_path.py
│   │   ├── credentials/
│   │   │   ├── stripe.py
│   │   │   └── sslcommerz.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── apps/
│   └── subscription/
│       ├── management/
│       │   └── commands/
│       │       ├── create_sample_data.py
│       │       └── test_celery.py
│       ├── views/
│       │   ├── api_view.py
│       │   └── mvt_view.py
│       ├── migrations/
│       ├── models.py
│       ├── serializers.py
│       ├── tasks.py
│       ├── utils.py
│       ├── admin.py
│       ├── urls.py
│       ├── views.py
│       ├── apps.py
│       └── tests.py
├── templates/
│   ├── base.html
│   └── subscriptions/
│       └── subscription_list.html
├── static/
├── staticfiles/
├── media/
├── respond/
│   ├── renderers.py
│   └── utils.py
├── scripts/
├── manage.py
├── requirements.txt
└── db.sqlite3
```

### Technology Stack
- **Backend**: Django 5.2.4, Django REST Framework
- **Database**: SQLite3 (local), MySQL (production)
- **Authentication**: JWT (JSON Web Tokens)
- **Background Tasks**: Celery with Redis
- **Frontend**: Bootstrap 5, Django Templates
- **API Documentation**: DRF Spectacular (Swagger/OpenAPI)

## Snippets for Clone and Run the Project:

### Quick Start Commands

Clone and setup:
```bash
git clone https://github.com/emhash/Subscription-Management-System.git
cd subscribe
```
```
python -m venv venv
source venv/bin/activate  
```

or, On Windows:
```bash
source venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Environment setup (Edit .env with your configuration):
```bash
cp .env.save .env
```

Database setup:
```bash
python manage.py migrate
python manage.py create_sample_data
python manage.py createsuperuser
```

Run the server:
```bash
python manage.py runserver
```

## API Testing

Get JWT token:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "sampleuser", "password": "testuser1234"}'
```

List plans:
```bash
curl -X GET http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Create subscription:
```bash
curl -X POST http://127.0.0.1:8000/api/subscribe/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": 1}'
```

List user subscriptions:
```bash
curl -X GET http://127.0.0.1:8000/api/subscriptions/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Cancel subscription:
```bash
curl -X POST http://127.0.0.1:8000/api/cancel/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"subscription_id": 1}'
```

Get exchange rate:
```bash
curl -X GET "http://127.0.0.1:8000/api/exchange-rate/?base=USD&target=BDT" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Get exchange rate history:
```bash
curl -X GET "http://127.0.0.1:8000/api/exchange-rate/history/?base=USD&target=BDT" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## About The Project Flow

### Models (MVT Pattern) Flow:
1. **User Model**: Django's built-in User model for authentication
2. **Plan Model**: Defines subscription plans with name, price, and duration
3. **Subscription Model**: Links users to plans with status tracking
4. **ExchangeRateLog Model**: Stores currency exchange rate history

### REST API Testing Flow:
1. **Authentication**: Obtain JWT token via `/api/auth/token/`
2. **Plan Management**: List available plans via `/api/plans/`
3. **Subscription Operations**:
   - Create: `POST /api/subscribe/`
   - List: `GET /api/subscriptions/`
   - Cancel: `POST /api/cancel/`
4. **Exchange Rates**: `GET /api/exchange-rate/?base=USD&target=BDT`

### Currency Exchange API Integration Flow:
1. **External API**: Integrates with exchangerate-api.com
2. **Real-time Fetching**: API calls for current exchange rates
3. **Database Storage**: All rates stored in ExchangeRateLog model
4. **History Tracking**: Historical rate data available via API

### Celery Task (Celery+Redis) Flow:
1. **Background Processing**: Periodic exchange rate fetching
2. **Task Scheduling**: Hourly updates via Celery Beat
3. **Database Updates**: Automatic logging of exchange rates
4. **Error Handling**: Robust error handling and logging

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Get JWT access token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Subscription Management
- `GET /api/plans/` - List all subscription plans
- `POST /api/subscribe/` - Create new subscription
- `GET /api/subscriptions/` - List user's subscriptions
- `POST /api/cancel/` - Cancel active subscription

### Exchange Rates
- `GET /api/exchange-rate/` - Get current exchange rate
- `GET /api/exchange-rate/history/` - Get exchange rate history

### Documentation
- `GET /api/docs/` - Swagger UI documentation
- `GET /api/schema/` - OpenAPI schema
- `GET /api/redoc/` - ReDoc documentation

## API Sample Responses

### Authentication Responses

**Success - JWT Token:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "",
    "data": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
}
```

**Error - Invalid Credentials:**
```json
{
    "success": false,
    "status_code": 401,
    "message": "Invalid credentials",
    "error_details": {
        "detail": "No active account found with the given credentials"
    }
}
```

### Subscription Management Responses

**Success - List Plans:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Plans retrieved successfully",
    "data": {
        "count": 5,
        "data": [
            {
                "id": 1,
                "name": "Basic Plan",
                "price": "9.99",
                "duration_days": 30,
                "created_at": "2025-08-03T13:45:50.107637+06:00",
                "updated_at": "2025-08-03T13:45:50.107637+06:00"
            },
            {
                "id": 2,
                "name": "Premium Plan",
                "price": "19.99",
                "duration_days": 30,
                "created_at": "2025-08-03T13:45:50.195691+06:00",
                "updated_at": "2025-08-03T13:45:50.195691+06:00"
            }
        ]
    }
}
```

**Success - Create Subscription:**
```json
{
    "success": true,
    "status_code": 201,
    "message": "Subscription created successfully",
    "data": {
        "data": {
            "id": 5,
            "user": {
                "id": 5,
                "username": "testuser",
                "email": "test@example.com",
                "first_name": "",
                "last_name": ""
            },
            "plan": {
                "id": 1,
                "name": "Basic Plan",
                "price": "9.99",
                "duration_days": 30
            },
            "plan_name": "Basic Plan",
            "plan_price": "9.99",
            "start_date": "2025-08-03T14:43:13.306213+06:00",
            "end_date": "2025-09-02T14:43:13.306213+06:00",
            "status": "active",
            "days_remaining": 29,
            "is_expired": false,
            "created_at": "2025-08-03T14:43:13.306213+06:00",
            "updated_at": "2025-08-03T14:43:13.306213+06:00"
        }
    }
}
```

**Success - List User Subscriptions:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Subscriptions retrieved successfully",
    "data": {
        "count": 1,
        "data": [
            {
                "id": 4,
                "user": {
                    "id": 5,
                    "username": "testuser",
                    "email": "test@example.com"
                },
                "plan": {
                    "id": 1,
                    "name": "Basic Plan",
                    "price": "9.99",
                    "duration_days": 30
                },
                "plan_name": "Basic Plan",
                "plan_price": "9.99",
                "start_date": "2025-08-03T14:43:13.306213+06:00",
                "end_date": "2025-09-02T14:43:13.306213+06:00",
                "status": "active",
                "days_remaining": 29,
                "is_expired": false
            }
        ]
    }
}
```

**Success - Cancel Subscription:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Subscription cancelled successfully",
    "data": {
        "data": {
            "id": 4,
            "user": {
                "id": 5,
                "username": "testuser",
                "email": "test@example.com"
            },
            "plan": {
                "id": 1,
                "name": "Basic Plan",
                "price": "9.99",
                "duration_days": 30
            },
            "plan_name": "Basic Plan",
            "plan_price": "9.99",
            "start_date": "2025-08-03T14:43:13.306213+06:00",
            "end_date": "2025-09-02T14:43:13.306213+06:00",
            "status": "cancelled",
            "days_remaining": 0,
            "is_expired": false
        }
    }
}
```

### Exchange Rate Responses

**Success - Get Exchange Rate:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Exchange rate retrieved successfully",
    "data": {
        "data": {
            "base_currency": "USD",
            "target_currency": "BDT",
            "rate": 122.332526,
            "fetched_at": "2025-08-03T08:43:45.888163Z",
            "message": "Exchange rate fetched successfully"
        }
    }
}
```

**Success - Exchange Rate History:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Exchange rate history retrieved successfully",
    "data": {
        "count": 1,
        "data": [
            {
                "id": 1,
                "base_currency": "USD",
                "target_currency": "BDT",
                "rate": "122.332526",
                "fetched_at": "2025-08-03T14:43:45.888163+06:00"
            }
        ]
    }
}
```

### Error Responses

**Validation Error:**
```json
{
    "success": false,
    "status_code": 400,
    "message": "Validation error occurred.",
    "error_details": {
        "field": "plan_id",
        "message": "This field is required."
    }
}
```

**Authentication Error:**
```json
{
    "success": false,
    "status_code": 401,
    "message": "Authentication credentials were not provided.",
    "error_details": {
        "detail": "Authentication credentials were not provided."
    }
}
```

**Not Found Error:**
```json
{
    "success": false,
    "status_code": 404,
    "message": "Plan not found.",
    "error_details": {
        "field": "plan_id",
        "message": "Plan not found."
    }
}
```

**Unsupported Currency Error:**
```json
{
    "success": false,
    "status_code": 400,
    "message": "Currency pair EUR/USD not supported yet",
    "error_details": {
        "success": false
    }
}
```

**Server Error:**
```json
{
    "success": false,
    "status_code": 500,
    "message": "Failed to create subscription: Database error",
    "error_details": {
        "message": "Failed to create subscription: Database error"
    }
}
```

## Frontend Pages
- `/` - Main subscription list page (no login required)
- `/admin/` - Django admin interface


## Screenshots

### Sample Data Creation
![Create Sample Data](xtra(Screen%20Shots)/creates-sample-data.jpg)
*Management command to create sample data for testing the system*

### Celery Beat Success
![Celery Beat Success](xtra(Screen%20Shots)/celery-beat-success-sample.jpg)
*Background task execution showing successful periodic exchange rate fetching*

### Celery Test Management Command
![Celery Test](xtra(Screen%20Shots)/celery-test-management-command.jpg)
*Testing Celery background tasks using Django management commands*

