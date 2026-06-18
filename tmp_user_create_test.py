import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
if User.objects.filter(username='admin_test').exists():
    user = User.objects.get(username='admin_test')
else:
    user = User.objects.create_superuser(username='admin_test', email='admin@test.com', password='Admin123!')

client = Client()
print('login', client.login(username='admin_test', password='Admin123!'))

payload = {
    'username': 'testuser_unique_123',
    'email': 'test_unique_123@example.com',
    'role': 'member',
    'password': 'Password123!',
    'phone_number': '',
    'dob': '',
    'age': '',
    'salary': '',
    'address': ''
}

response = client.post(
    '/api/users/',
    content_type='application/json',
    data=json.dumps(payload),
    HTTP_HOST='localhost',
    HTTP_X_FORWARDED_PROTO='https',
    SERVER_NAME='localhost',
)
print('status', response.status_code)
print('redirects', response.redirect_chain if hasattr(response, 'redirect_chain') else [])
print('body', response.content.decode('utf-8'))
