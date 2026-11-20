# E-Commerce Website — Project Specifications & Development Tasks

## 1. Project Overview

**Project name:** Basic E-Commerce Website  
**Goal:** Build a responsive online store where customers can browse products, view product details, manage a shopping cart, register/login, and place orders. An administrator can manage products and orders.

### Final technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Django |
| Database | SQLite for development; PostgreSQL can be added for deployment |
| Images | Django media uploads |
| Version control | Git and GitHub |

**Architecture decision:** Use Django templates to render the HTML pages, with CSS and JavaScript for styling and browser-side interactions. This is the simplest way to combine the requested frontend technologies with Django. A separate React frontend is not required.

---

## 2. Finalized Feature Scope

The following features are finalized for Version 1 (MVP).

### A. Customer-facing features

1. **Home page**
   - Display store name, navigation menu, search bar and featured products.
   - Show product categories.
   - Provide links to login, registration and shopping cart.

2. **Product listing**
   - Display products in a responsive grid.
   - Show product image, name, price and availability.
   - Include category filtering.
   - Include keyword search by product name.
   - Include sorting by price (low to high and high to low).

3. **Product details page**
   - Show product image, name, full description and price.
   - Show available stock.
   - Allow the customer to select quantity.
   - Provide an Add to Cart button.
   - Prevent adding a quantity greater than available stock.

4. **User registration and login**
   - Register using name, email and password.
   - Login and logout.
   - Validate user input.
   - Use Django's built-in authentication system.
   - Provide a basic account page showing the user's details and order history.

5. **Shopping cart**
   - Add products to the cart.
   - View cart items, quantities and prices.
   - Increase or decrease quantities.
   - Remove products.
   - Display item subtotal and cart total.
   - Check product availability before checkout.
   - Keep the cart available across pages. For the MVP, use a session-based cart for guests and transfer/merge it into the user's cart after login if implemented.

6. **Checkout**
   - Require the customer to log in before placing an order.
   - Collect recipient name, phone number and delivery address.
   - Display an order summary before confirmation.
   - Validate stock and prices again on the server.
   - Calculate the final total on the server, not using browser-submitted totals.

7. **Order processing**
   - Create an order and its order items after checkout confirmation.
   - Store the price of each product at the time of purchase.
   - Reduce stock only when the order is successfully created.
   - Generate a unique order number.
   - Show an order confirmation page.
   - Allow customers to view their previous orders and order details.
   - Use these order statuses: `Pending`, `Processing`, `Shipped`, `Delivered`, `Cancelled`.

8. **Responsive design**
   - Support desktop, tablet and mobile screen sizes.
   - Use clear navigation, readable text and consistent buttons.
   - Show useful messages for empty carts, invalid forms and unavailable products.

### B. Administrator features

Use Django Admin as the first admin interface. Do not build a separate custom admin dashboard in Version 1.

- Secure administrator login.
- Add, edit and delete products.
- Upload and update product images.
- Manage product categories.
- Update product prices and stock quantities.
- View customer orders and order items.
- Update order statuses.
- View registered users.

### C. Features deliberately excluded from Version 1

To keep the project achievable, do not include these in the first release:

- Online payment gateway integration.
- Product reviews and ratings.
- Wishlist.
- Coupons and discount codes.
- Live shipment tracking.
- Multiple sellers or vendor dashboards.
- Recommendation system.
- Chatbot.
- Advanced analytics dashboard.

**Payment decision:** Use Cash on Delivery (COD) as the only payment option in Version 1. Store the payment method and a simple payment status. Online payments can be a future enhancement.

---

## 3. Main Pages

| Page | Purpose | Access |
|---|---|---|
| Home | Featured products and categories | Public |
| Product List | Browse, search, filter and sort products | Public |
| Product Details | View product information and add to cart | Public |
| Register | Create an account | Public |
| Login | Sign in | Public |
| Cart | Review and update cart | Public |
| Checkout | Enter delivery information and confirm order | Logged-in user |
| Order Success | Display order confirmation | Order owner |
| My Account | View account information | Logged-in user |
| My Orders | View order history | Logged-in user |
| Order Details | View one order and its items | Order owner |
| Django Admin | Manage store data | Staff/admin |

---

## 4. Database Specifications

Use Django ORM models. Suggested tables/models:

### 4.1 User
Use Django's built-in `User` model for authentication rather than creating password storage yourself.

Important fields:
- Username
- Email
- Password hash (managed by Django)
- First name
- Last name
- Date joined
- Active status

### 4.2 Category
- `id` — primary key
- `name` — category name
- `slug` — URL-friendly unique name
- `description` — optional description

Relationship: One category can contain many products.

### 4.3 Product
- `id` — primary key
- `category` — foreign key to Category
- `name` — product name
- `slug` — URL-friendly unique name
- `description` — product description
- `price` — decimal value
- `image` — uploaded product image
- `stock` — available quantity
- `is_active` — whether the product is visible
- `created_at` — creation date
- `updated_at` — last update date

### 4.4 Order
- `id` — primary key
- `order_number` — unique order reference
- `user` — foreign key to User
- `recipient_name` — delivery recipient
- `phone` — contact number
- `delivery_address` — delivery address
- `total_amount` — order total
- `payment_method` — COD in Version 1
- `payment_status` — for example, Pending or Paid
- `status` — order fulfilment status
- `created_at` — order date

### 4.5 OrderItem
- `id` — primary key
- `order` — foreign key to Order
- `product` — foreign key to Product
- `product_name` — name snapshot at purchase time
- `quantity` — purchased quantity
- `unit_price` — price snapshot at purchase time
- `subtotal` — quantity multiplied by unit price

**Important relationships:**
- Category → Product: one-to-many.
- User → Order: one-to-many.
- Order → OrderItem: one-to-many.
- Product → OrderItem: one-to-many.

**Important data rules:**
- Use `DecimalField` for money, not floating-point fields.
- Use Django password hashing; never store plain-text passwords.
- Keep product name and unit price snapshots in OrderItem so old orders remain accurate if a product changes later.
- Use database transactions when creating an order and updating stock.
- Validate stock on the server during checkout to prevent overselling.

---

## 5. Suggested Django Project Structure

```text
ecommerce/
│
├── manage.py
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── store/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── tests.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── products/
│   │   ├── product_list.html
│   │   └── product_detail.html
│   ├── accounts/
│   │   ├── register.html
│   │   └── login.html
│   ├── cart/
│   │   └── cart.html
│   └── orders/
│       ├── checkout.html
│       ├── success.html
│       ├── my_orders.html
│       └── order_detail.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
└── media/
    └── products/
```

This is a suggested structure. You can split accounts, cart and orders into separate Django apps as the project grows. For a small first version, one `store` app is acceptable.

---

## 6. Development Tasks — Step by Step

### Phase 1: Project setup
- [ ] Install Python and create a virtual environment.
- [ ] Install Django.
- [ ] Create the Django project and `store` app.
- [ ] Configure templates, static files and media uploads.
- [ ] Configure SQLite.
- [ ] Run the development server.
- [ ] Initialize a Git repository.

**Deliverable:** A working Django project with a home page.

### Phase 2: Database and admin
- [ ] Create Category and Product models.
- [ ] Create Order and OrderItem models.
- [ ] Add model relationships and validations.
- [ ] Run migrations.
- [ ] Register models in Django Admin.
- [ ] Add sample categories and products.
- [ ] Test product image uploads.

**Deliverable:** Products and categories can be managed through Django Admin.

### Phase 3: Frontend and product browsing
- [ ] Create a reusable `base.html` layout.
- [ ] Create navigation bar and footer.
- [ ] Build the home page.
- [ ] Build the product listing page.
- [ ] Build the product details page.
- [ ] Add category filtering.
- [ ] Add product search.
- [ ] Add price sorting.
- [ ] Make pages responsive using CSS.

**Deliverable:** Visitors can browse and inspect products.

### Phase 4: Authentication
- [ ] Build the registration form.
- [ ] Implement registration using Django authentication.
- [ ] Build the login page.
- [ ] Implement logout.
- [ ] Restrict checkout and order history to logged-in users.
- [ ] Add an account page.

**Deliverable:** Customers can register, log in and log out.

### Phase 5: Shopping cart
- [ ] Create add-to-cart functionality.
- [ ] Store guest cart data in the Django session.
- [ ] Display cart products and quantities.
- [ ] Implement quantity updates.
- [ ] Implement item removal.
- [ ] Calculate cart totals on the server.
- [ ] Validate product availability.
- [ ] Show an empty-cart message.

**Deliverable:** Customers can manage a working shopping cart.

### Phase 6: Checkout and order processing
- [ ] Build the checkout form.
- [ ] Collect recipient name, phone and delivery address.
- [ ] Display an order summary.
- [ ] Recheck product stock and prices on the server.
- [ ] Create Order and OrderItem records.
- [ ] Use a database transaction for order creation and stock reduction.
- [ ] Set payment method to COD.
- [ ] Generate a unique order number.
- [ ] Clear the cart after successful order creation.
- [ ] Build the order confirmation page.

**Deliverable:** Customers can place COD orders.

### Phase 7: Order history and administration
- [ ] Build the My Orders page.
- [ ] Build the Order Details page.
- [ ] Ensure customers can only view their own orders.
- [ ] Allow administrators to update order statuses.
- [ ] Verify that stock changes correctly after an order.
- [ ] Verify that cancelled orders follow a defined stock-restoration rule.

**Deliverable:** Customers can track order status and administrators can process orders.

### Phase 8: Testing and final polish
- [ ] Test registration, login and logout.
- [ ] Test product search, filtering and sorting.
- [ ] Test adding, updating and removing cart items.
- [ ] Test checkout with available stock.
- [ ] Test checkout when stock is insufficient.
- [ ] Test that users cannot access another user's orders.
- [ ] Test invalid form submissions.
- [ ] Test mobile and desktop layouts.
- [ ] Check error messages and empty states.
- [ ] Add a README with setup instructions and screenshots.

**Deliverable:** A tested, documented Version 1 project.

---

## 7. Important Business Rules

1. Only active products should appear in the public product listing.
2. A product with zero stock should be marked out of stock.
3. A customer cannot add zero or negative quantities.
4. A customer cannot order more than the available stock.
5. The backend must calculate prices and totals; never trust totals sent by JavaScript.
6. Revalidate stock and current prices when checkout is submitted.
7. Create the order and reduce stock atomically using a database transaction.
8. Customers may view only their own orders.
9. Only authorized staff may manage products and update order statuses.
10. Do not permanently delete products that are referenced by past orders; deactivate them instead.

---

## 8. Basic Acceptance Criteria

Version 1 is complete when all of the following work:

- A visitor can open the home page and browse products.
- A visitor can search, filter and sort products.
- A visitor can view a product's full details.
- A customer can register, log in and log out.
- A customer can add products to the cart and update quantities.
- The cart shows correct item subtotals and total.
- A logged-in customer can enter delivery details and place a COD order.
- The system saves the order and its items in the database.
- Stock is reduced correctly after a successful order.
- A customer can view their own order history and order details.
- An administrator can manage products, categories and order statuses.
- The site works on desktop and mobile screen sizes.

---

## 9. Future Enhancements (After Version 1)

Consider these only after the core application works:

- Online payments using a payment gateway.
- Wishlist.
- Product reviews and ratings.
- Coupons and discounts.
- Email order confirmation.
- Product recommendations.
- Pagination and advanced filters.
- PostgreSQL deployment and cloud image storage.
- Deployment to a hosting platform with HTTPS.

---

## 10. Recommended Build Order

Build and test one complete feature at a time:

1. Django setup and database models.
2. Admin product management.
3. Product listing and details.
4. Registration and login.
5. Shopping cart.
6. Checkout and COD order creation.
7. Order history and admin order management.
8. Responsive styling, testing and documentation.

**Final scope:** A single-store e-commerce website with product browsing, search/filter/sort, customer authentication, session-based shopping cart, COD checkout, order history, stock management and Django Admin. This is a realistic and demonstrable beginner-to-intermediate full-stack project.
