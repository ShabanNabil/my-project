from datetime import timedelta
from pathlib import Path

# تعريف المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات أساسية
SECRET_KEY = 'simple-key-for-testing'  # تحذير: غيّر هذا المفتاح في الإنتاج إلى مفتاح قوي وفريد
DEBUG = True  # مفعل للتطوير، قم بتعطيله (False) في الإنتاج
ALLOWED_HOSTS = [
    'nursery-api-zzo0.onrender.com',
    'localhost',
    '127.0.0.1',
    '36bd-196-134-5-73.ngrok-free.app'  # العنوان الفعلي من ngrok
]

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

# الـ Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # يجب أن يكون أولًا لمعالجة CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# إعدادات URL الرئيسية
ROOT_URLCONF = 'Nursery_project.urls'

# إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# تطبيق WSGI
WSGI_APPLICATION = 'Nursery_project.wsgi.application'

# قاعدة البيانات (SQLite للتطوير)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تعطيل التحقق من كلمات السر مؤقتًا (للتطوير فقط)
AUTH_PASSWORD_VALIDATORS = []

# إعدادات اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# إعدادات الملفات الثابتة والوسائط
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# نوع الحقل التلقائي الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# نموذج المستخدم المخصص
AUTH_USER_MODEL = 'App.User'

# إعدادات CSRF (مطابقة لـ HTTPS مع ngrok)
CSRF_COOKIE_SECURE = True  # مفعل لأن ngrok يستخدم HTTPS
SESSION_COOKIE_SECURE = True  # مفعل لأن ngrok يستخدم HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://nursery-api-zzo0.onrender.com',
    'https://36bd-196-134-5-73.ngrok-free.app',  # العنوان الفعلي من ngrok
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]

# إعدادات CORS
CORS_ALLOWED_ORIGINS = [
    'https://nursery-api-zzo0.onrender.com',
    'https://36bd-196-134-5-73.ngrok-free.app',  # العنوان الفعلي من ngrok
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'accept',
    'origin',
]

# إعدادات Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# إعدادات Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'simple-key-for-testing',  # تحذير: غيّر هذا في الإنتاج
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# إعدادات الإيميل (للتطوير فقط)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# إعدادات الـ Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}