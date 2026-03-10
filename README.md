# Campus Mart - Student Marketplace

A modern, full-featured e-commerce and service marketplace platform for campus entrepreneurs and customers. Built with Django, Bootstrap 5, and modern web technologies.

## Features

### 👥 User Roles
- **System Administrator**: Manage stores, entrepreneurs, customers, view system logs, monitor activities
- **Entrepreneurs**: Create/manage stores, add products/services, manage customer orders
- **Customers**: Browse products/services, add to cart, place orders with COD, track orders, live chat support

### 🛍️ Core Features
- **Product & Service Management**: Add, edit, delete products/services with images
- **Shopping Cart**: Add items to cart and manage quantities
- **Order System**: Place orders with payment on delivery (COD)
- **Order Tracking**: Track order status from pending to delivered
- **Live Chat**: Real-time customer support and store communication
- **Categories**: Browse products by category
- **Search & Filter**: Find products by name, category, or type
- **Reviews & Ratings**: Customer reviews and product ratings
- **System Logging**: Track all user activities

### 🎨 Design
- **Modern UI**: Clean, attractive interface with Bootstrap 5
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Color Theme**: Light Blue (#87CEEB) and Cream (#FFFDD0)
- **Professional Layout**: Intuitive navigation and user experience

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (default, easily switchable to PostgreSQL)
- **Real-time**: Django Channels (WebSockets support)
- **Image Handling**: Pillow
- **Additional**: django-crispy-forms, channels-redis

## Project Structure

```
campusmart_project/
├── accounts/              # User authentication and roles
├── stores/               # Store management
├── products/             # Products and services
├── orders/               # Cart, checkout, orders
├── chat/                 # Live chat functionality
├── logs/                 # System activity logging
├── templates/            # HTML templates
├── static/               # CSS, JavaScript, images
├── media/                # User-uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd campusmart_project
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

#### SQLite (Default)
No additional configuration needed - Django will create `db.sqlite3` automatically.

#### PostgreSQL (Optional)
If you want to use PostgreSQL instead:

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update `campusmart_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'campusmart_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

When prompted, enter:
- Username: admin
- Email: admin@example.com
- Password: (enter a strong password)

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Create Sample Data (Optional)
```bash
python manage.py shell
```

Then paste this code:
```python
from accounts.models import User
from products.models import Category
from stores.models import Store

# Create categories
categories = [
    Category.objects.create(name='Electronics', description='Electronic gadgets and devices'),
    Category.objects.create(name='Fashion', description='Clothing and accessories'),
    Category.objects.create(name='Food', description='Snacks and beverages'),
    Category.objects.create(name='Books', description='Books and stationery'),
    Category.objects.create(name='Beauty', description='Beauty and personal care'),
    Category.objects.create(name='Services', description='Campus services'),
]

# Create entrepreneur user
entrepreneur = User.objects.create_user(
    username='entrepreneur1',
    email='entrepreneur@example.com',
    password='testpass123',
    first_name='John',
    last_name='Doe',
    role='entrepreneur'
)

# Create store
store = Store.objects.create(
    name='Tech Hub',
    description='Your one-stop shop for all tech needs on campus',
    location='Tech Building',
    entrepreneur=entrepreneur
)

print("Sample data created successfully!")
```

Type `exit()` to exit shell.

### Step 9: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Admin Dashboard

Access the admin panel at `/admin/` with your superuser credentials:
- Username: admin
- Password: (the password you created)

From the admin dashboard, you can:
- Manage users and assign roles
- Create and manage stores
- Create categories
- View system logs
- Monitor orders
- Manage chats

## User Credentials for Testing

### Customer Account
- Username: `customer_user`
- Password: `testpass123`
- Role: Customer

### Entrepreneur Account
- Username: `entrepreneur1`
- Password: `testpass123`
- Role: Entrepreneur
- Store: Tech Hub

### Admin Account
- Username: `admin`
- Password: (created during setup)
- Role: System Administrator

## Usage Guide

### For Customers
1. Register/Login at `/accounts/register/customer/`
2. Browse products at `/products/`
3. Use search and filters to find products
4. Add items to cart
5. Checkout with delivery details
6. Pay on delivery when order arrives
7. Track order status in order history
8. Use live chat for support

### For Entrepreneurs
1. Register at `/accounts/register/entrepreneur/`
2. Wait for admin to approve and assign store
3. Login at `/accounts/login/entrepreneur/`
4. Access dashboard at `/stores/dashboard/`
5. Add products/services
6. Manage customer orders
7. Update order status

### For Admins
1. Login to `/admin/`
2. Manage users, stores, and categories
3. View system activity logs
4. Monitor orders and transactions
5. Manage customer support chats

## Key URLs

| URL | Purpose |
|-----|---------|
| `/` | Homepage |
| `/accounts/register/customer/` | Customer registration |
| `/accounts/register/entrepreneur/` | Entrepreneur registration |
| `/accounts/login/customer/` | Customer login |
| `/accounts/login/entrepreneur/` | Entrepreneur login |
| `/products/` | Browse products |
| `/stores/` | Browse stores |
| `/orders/cart/` | Shopping cart |
| `/orders/history/` | Order history |
| `/chat/` | Live chat |
| `/admin/` | Admin dashboard |

## Database Models

### User
- Custom user model with roles (admin, entrepreneur, customer)
- Phone number, date joined, active status

### Store
- Name, description, location, logo
- Entrepreneur (owner)
- Active status

### Product
- Name, category, description, price, quantity
- Product type (product or service)
- Store reference
- Rating and reviews

### Order
- Order ID, customer, store
- Status (pending, approved, out for delivery, delivered, cancelled)
- Delivery information
- Total price
- Payment on delivery only

### Cart & CartItem
- Customer cart with items
- Product quantity

### ChatRoom & ChatMessage
- Support and entrepreneur chats
- Real-time messaging

### SystemLog
- Track all user activities
- Admin actions, logins, product uploads, orders, etc.

## Deployment

### For Production:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set up proper static/media file serving (AWS S3, CDN)
5. Use environment variables for sensitive data
6. Deploy with Gunicorn + Nginx
7. Enable HTTPS
8. Set up proper logging

Example for environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## Common Issues & Solutions

### Issue: "No such table" error
**Solution**: Run migrations again
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: Permission denied for media uploads
**Solution**: Ensure media folder has write permissions
```bash
chmod -R 755 media
```

### Issue: Database connection error with PostgreSQL
**Solution**: Verify PostgreSQL service is running and credentials are correct

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Future Enhancements

- [ ] Payment gateway integration (Stripe, Paystack)
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Product recommendations
- [ ] Wishlist functionality
- [ ] Seller ratings and reviews
- [ ] Two-factor authentication
- [ ] Mobile app (React Native)
- [ ] Video chat support
- [ ] Bulk order management

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Contact

- Email: support@campusmart.com
- Phone: +1 (555) 123-4567
- Location: University Campus

## Acknowledgments

- Built with Django and Bootstrap 5
- Inspired by modern e-commerce platforms
- Designed for campus entrepreneurship

---

**Campus Mart** - Empowering Student Entrepreneurs. © 2026 All rights reserved.
#   c a m p u s m a r t  
 