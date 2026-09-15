# 🍽️ OAI Kitchen — AI Food Ordering Chatbot

OAI Kitchen is a full-stack, AI-powered food ordering application that allows customers to interact with a conversational chatbot to place and manage food orders using natural language.

The project combines **Google Dialogflow**, **Python FastAPI**, **MySQL**, and a responsive **HTML/CSS/JavaScript frontend**. The application is deployed to **Railway**, with Dialogflow Messenger embedded directly into the live website.

The system demonstrates an end-to-end conversational application architecture:

**Customer → Frontend → Dialogflow → FastAPI Webhook → MySQL → Response**

---

## 🌐 Live Application

**Live Website:**  
https://nlpchatbotfrontend-production.up.railway.app/

**Backend API / Webhook:**  
https://nlpchatbotbackend-production.up.railway.app/

**FastAPI Swagger Documentation:**  
https://nlpchatbotbackend-production.up.railway.app/docs

> The application is deployed on Railway. The frontend is a static website, while the backend runs as a FastAPI service connected to a Railway-hosted MySQL database.

---

## 📌 Project Overview

OAI Kitchen was built to simulate a real-world restaurant ordering workflow powered by conversational AI.

Instead of requiring customers to navigate through a traditional form-based ordering system, the customer can communicate naturally with the chatbot.

For example:

```text
Customer:
"I want 2 samosas"

Chatbot:
"Added 2 Samosa to your order. Do you need anything else?"

Customer:
"Add 1 jollof rice"

Chatbot:
"Added 1 Jollof rice to your order..."

Customer:
"Complete my order"

Chatbot:
"Awesome. We have placed your order.
Here is your order id: #61.
Your order total is $17.00..."
```

The chatbot can maintain an order during a conversation, modify the order, complete it, and persist the resulting information in MySQL.

## ✨ Features

### 🤖 Conversational AI

The application uses Google Dialogflow to understand natural-language customer requests.

The chatbot supports conversational interactions for:

* Starting a new order
* Adding food items
* Removing food items
* Completing an order
* Tracking an existing order
* Handling unsupported requests through fallback behavior

### 🛒 Order Management

Customers can build an order conversationally.

**Add items**

Example:

```text
"Add 2 samosas"
"I want 3 jollof rice"
"Can I get one pizza?"
```

The chatbot maintains the customer's current order during the conversation.

**Remove items**

Example:

```text
"Remove one samosa"
"Take 2 jollof rice out"
"I don't want the pizza anymore"
```

The system updates the active order and tells the customer what remains.

**Complete orders**

When the customer is finished, the chatbot:

1. Validates the order
2. Generates an order ID
3. Stores the ordered items in MySQL
4. Calculates the order total
5. Creates an order-tracking record
6. Returns the order ID and total to the customer
7. Clears the active in-memory order

Example:

```text
Awesome. We have placed your order.
Here is your order id: #61.
Your order total is $10.00 which you can pay Online
or at the time of delivery!
```

### 📦 Order Tracking

Customers can provide an order ID and ask for its status.

Example:

```text
"What is the status of order 40?"
"Track order 40"
"Where is my order?"
```

The FastAPI backend retrieves the corresponding status from MySQL and returns it through Dialogflow.

Example response:

```text
The order status for order id #40 is: DELIVERED
```

Supported tracking states include statuses such as:

* in progress
* in transit
* delivered

### 🍽️ Menu

The current menu contains:

| #   | Food Item                          |
| --- | ---------------------------------- |
| 1   | Jollof Rice                        |
| 2   | Chicken Sausage and Potato Skillet |
| 3   | Pizza                              |
| 4   | Ground Turkey Stuffed Bell Peppers |
| 5   | Crockpot Black Eyed Peas           |
| 6   | Dutch Oven Chicken Pot Pie         |
| 7   | Beef Stew with Onion Soup Mix      |
| 8   | Authentic Nigerian Fried Rice      |
| 9   | Samosa                             |

Menu prices are stored in the MySQL food_items table rather than hard-coded into the frontend.

This allows the backend/database to remain the source of truth for pricing.

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      Customer        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   OAI Kitchen        │
                         │   Frontend           │
                         │ HTML + CSS + JS      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Dialogflow Messenger │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Google Dialogflow    │
                         │ Conversational AI    │
                         └──────────┬───────────┘
                                    │
                              Webhook Request
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         │      Python          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     MySQL Database   │
                         │                      │
                         │ food_items           │
                         │ orders               │
                         │ order_tracking       │
                         └──────────────────────┘
```

## 🔄 Request Flow

When a customer sends a message, the process works approximately like this:

```text
1. Customer sends a message
          ↓
2. Dialogflow interprets the intent
          ↓
3. Dialogflow sends a webhook request
          ↓
4. FastAPI receives the request
          ↓
5. Backend identifies the requested operation
          ↓
6. Backend interacts with MySQL when required
          ↓
7. FastAPI returns a fulfillment response
          ↓
8. Dialogflow sends the response to the customer
```

For example, completing an order follows:

```text
Customer
   │
   │ "Complete my order"
   ▼
Dialogflow
   │
   │ complete_order intent
   ▼
FastAPI
   │
   ├── Validate active order
   ├── Generate order ID
   ├── Insert order items
   ├── Calculate total
   ├── Create tracking record
   └── Clear active order
   │
   ▼
MySQL
   │
   ├── orders
   └── order_tracking
   │
   ▼
FastAPI
   │
   ▼
Dialogflow
   │
   ▼
Customer
```

## 🧰 Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Dialogflow Messenger

The frontend is intentionally lightweight and does not use a frontend framework.

It contains:

* Responsive navigation
* Hero section
* Menu cards
* Food images
* About section
* Contact section
* Footer
* Embedded Dialogflow chatbot
* Mobile navigation

### Conversational AI

Google Dialogflow

Dialogflow is responsible for:

* Natural-language understanding
* Intent recognition
* Training phrases
* Parameters
* Context/session handling
* Webhook fulfillment
* Conversational responses

Example intents include:

```text
New Order
Add Order
Remove Order
Complete Order
Track Order
Fallback
```

### Backend

Python

Python is used to implement the server-side application logic.

FastAPI

FastAPI provides the webhook endpoint used by Dialogflow.

The backend receives Dialogflow's JSON request, determines the requested intent, processes the operation, and returns the appropriate response.

Uvicorn

Uvicorn is used as the ASGI server for running the FastAPI application.

### Database

MySQL

MySQL stores persistent application data.

The database contains three primary tables:

```text
food_items
orders
order_tracking
```

**food_items**

Stores the available menu items and their prices.

Example structure:

```text
item_id
name
price
```

**orders**

Stores individual items belonging to customer orders.

Example structure:

```text
order_id
item_id
quantity
total_price
```

**order_tracking**

Stores the current tracking status of an order.

Example structure:

```text
order_id
status
```

## 🗄️ Database Functions and Stored Procedures

The project also demonstrates the use of MySQL functions and stored procedures.

**get_price_for_item**

Retrieves the price of a food item from the database.

```text
get_price_for_item(food_item_name)
```

**get_total_order_price**

Calculates the total price associated with an order.

```text
get_total_order_price(order_id)
```

**insert_order_item**

Handles insertion of an individual order item into the orders table.

```text
insert_order_item(
    food_item,
    quantity,
    order_id
)
```

Using database functions and stored procedures keeps important database operations close to the data layer.

## 📁 Project Structure

```text
NLP_Chatbot_project/
│
├── backend/
│   │
│   ├── main.py
│   ├── db_helper.py
│   ├── generic_helper.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── index.html
│   ├── styles.css
│   │
│   └── images/
│       ├── hero-food.jpg
│       ├── Jollof Rice.jpg
│       ├── Chicken Sausage and Potato Skillet.jpg
│       ├── pizza.jpg
│       ├── Ground Turkey Stuffed Bell Peppers.jpg
│       ├── Crockpot Black Eyed Peas.jpg
│       ├── Dutch Oven Chicken Pot Pie.jpg
│       ├── Beef Stew with Onion Soup Mix.jpg
│       ├── Authentic Nigerian Fried Rice.jpg
│       ├── samosa.jpeg
│       └── favicon.jpg
│
├── environment.yml
├── .gitignore
└── README.md
```


## ⚙️ Backend Configuration

The backend reads database configuration from environment variables.

For local development, a .env file can be used.

Example:

```text
host=localhost
user=root
password=YOUR_MYSQL_PASSWORD
database=my_database
```

For production, the Railway environment provides the database credentials through environment variables such as:

```text
MYSQLHOST
MYSQLPORT
MYSQLUSER
MYSQLPASSWORD
MYSQLDATABASE
```

The application reads these values through environment variables rather than hard-coding production credentials.

## 🔐 Environment Variables

Never commit real passwords, API credentials, database credentials, or other secrets to GitHub.

The .gitignore file should include:

```text
.env
__pycache__/
*.pyc
```

If you are running the project locally, create your own .env file.

Example:

```text
host=localhost
user=root
password=your_password
database=database_name
```

## 🚀 Running the Backend Locally

1. Clone the repository

```bash
git clone https://github.com/Ifeanyi-07/NLP_Chatbot.git
```

Move into the project:

```bash
cd NLP_Chatbot
```

2. Create a virtual environment

On Windows:

```bash
python -m venv venv
or
conda create -n venv python=3.12
```

Activate it:

```bash
.\venv\Scripts\Activate.ps1
or
conda activate venv
```

3. Install dependencies

Move into the backend directory:

```bash
cd backend
```

Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure MySQL

Create a MySQL database and configure the .env file with your local database credentials.

5. Start FastAPI

From the backend directory:

```bash
uvicorn main:app --reload
```

The local API should then be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## 🧪 Testing the Backend

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use this interface to inspect and test available API routes.

Dialogflow can also be tested through the Dialogflow console by triggering the configured intents.

## 🤖 Configuring Dialogflow

The Dialogflow agent must be configured with the appropriate intents, training phrases, parameters, contexts, and webhook fulfillment.

The webhook points to the deployed FastAPI backend.

Production webhook:

```text
https://nlpchatbotbackend-production.up.railway.app/
```

The Dialogflow Messenger integration is embedded into the frontend with:

```html
<script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>

<df-messenger
    intent="WELCOME"
    chat-title="OAI-Chatbot"
    agent-id="YOUR_DIALOGFLOW_AGENT_ID"
    language-code="en">
</df-messenger>
```

Replace YOUR_DIALOGFLOW_AGENT_ID with the appropriate Dialogflow agent ID.

## ☁️ Deployment

The application is deployed using Railway.

The project uses separate services for:

```text
Railway Project
│
├── Frontend
│   └── Static website
│
├── FastAPI Backend
│   └── Python application
│
└── MySQL
    └── Persistent database
```

### Frontend Deployment

The frontend service uses:

```text
frontend/
```

as its Railway root directory.

This prevents Railway from attempting to deploy the backend and database files as part of the frontend service.

The frontend is served as a static website.

### Backend Deployment

The backend service uses:

```text
backend/
```

as its Railway root directory.

Railway starts the FastAPI application using an ASGI server.

### Database Deployment

The production MySQL database runs on Railway.

The application's database configuration is supplied through Railway environment variables.

The database contains the menu, order, and tracking data required by the application.

## 🔗 Production Services

| Component         | Technology           | Deployment        |
| ----------------- | -------------------- | ----------------- |
| Frontend          | HTML/CSS/JS          | Railway           |
| Chatbot           | Dialogflow Messenger | Google Dialogflow |
| Conversational AI | Dialogflow           | Google Cloud      |
| Backend           | Python/FastAPI       | Railway           |
| Database          | MySQL                | Railway           |
| Source Control    | Git/GitHub           | GitHub            |

## 🔄 Git and Deployment Workflow

The frontend and backend code are maintained in Git.

A typical workflow is:

```text
Make code changes
       ↓
git status
       ↓
git add .
       ↓
git commit
       ↓
git push
       ↓
GitHub
       ↓
Railway automatically deploys
```

Dialogflow configuration is different.

Changes made directly inside Dialogflow, such as:

* Training phrases
* Intents
* Parameters
* Contexts
* Responses
* Fulfillment settings

are saved in Dialogflow and do not require a Git push.

## 🧠 Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* Conversational AI
* Natural-language understanding
* Intent classification
* Entity/parameter extraction
* Webhooks
* REST-style backend development
* FastAPI
* Python
* MySQL
* SQL
* Stored procedures
* Database functions
* Stateful order management
* Session handling
* API integration
* Cloud deployment
* Environment variables
* Git/GitHub
* Railway deployment
* Responsive frontend development
* Dialogflow Messenger integration

## 🧩 Challenges Solved During Development

Several practical deployment and integration issues were addressed while building the application.

**Database migration**

The local MySQL database had to be migrated to the Railway-hosted MySQL instance.

The migration included:

* Menu data
* Existing orders
* Order tracking data
* Database functions
* Stored procedures

**Production database/schema mismatch**

The Railway MySQL environment initially contained the default railway database while the application expected the required tables.

The database schema and data were subsequently created and populated correctly in the production database.

**Stored procedure dependencies**

The order-completion workflow depended on MySQL routines including:

```text
insert_order_item
get_price_for_item
get_total_order_price
```

These routines were recreated in the production database so the backend could successfully complete orders.

**Local versus production configuration**

The application was configured so that local development can use local MySQL credentials while production uses Railway-provided environment variables.

This avoids hard-coding production database credentials into the source code.

**Static frontend deployment**

The frontend was deployed separately from the FastAPI backend using Railway's static hosting configuration.

The frontend root directory is:

```text
/frontend
```

## 🧪 Example Conversation

A typical ordering conversation can look like:

```text
Customer:
Hello

Bot:
Welcome to OAI Kitchen! How can I help you today?

Customer:
I want 2 samosas

Bot:
So far you have: 2 Samosa. Do you need anything else?

Customer:
Add 1 pizza

Bot:
So far you have: 2 Samosa, 1 Pizza.
Do you need anything else?

Customer:
Actually remove the pizza

Bot:
Removed 1 Pizza from your order!

Customer:
Complete my order

Bot:
Awesome. We have placed your order.
Here is your order id: #61.
Your order total is $10.00...
```

The completed order is then persisted in MySQL.

Example:

```text
orders
-----------------------------------------
order_id | item_id | quantity | total
61       | 9       | 2        | 10.00
```

And the tracking record:

```text
order_tracking
----------------------------
order_id | status
61       | in progress
```

## 📊 Database Validation

The production database can be queried to verify completed orders.

Example:

```sql
USE railway;

SELECT *
FROM orders
WHERE order_id = 61;
```

Order totals can be verified using:

```sql
SELECT get_total_order_price(61);
```

Order tracking can be checked using:

```sql
SELECT *
FROM order_tracking
WHERE order_id = 61;
```

## 🛡️ Security Considerations

The project follows several basic security practices:

* Database passwords are stored in environment variables.
* .env is excluded from Git.
* Production database credentials are not hard-coded.
* Railway environment variables are used for production configuration.
* The public frontend does not contain database credentials.
* The Dialogflow agent communicates with the backend through the configured webhook.

For a production commercial application, additional measures would be recommended, including:

* Authentication and authorization
* Request validation
* Rate limiting
* Structured logging
* Monitoring and alerting
* Payment gateway integration
* Stronger session persistence
* Input sanitization
* HTTPS enforcement and security headers
* Automated tests
* CI/CD validation

## 🔮 Future Improvements

Possible future enhancements include:

* 💳 Online payment integration
* 👤 Customer accounts and authentication
* 📱 Progressive Web App support
* 📦 More advanced order tracking
* 🧾 Digital receipts
* 📧 Order confirmation emails
* 📊 Restaurant administration dashboard
* 📈 Sales analytics
* 🗣️ Voice-based ordering
* 🌍 Multi-language support
* 🧠 More advanced conversational understanding
* 🧪 Automated backend and integration tests
* 🔐 Persistent customer sessions
* 📱 Mobile application
* 🔔 Real-time order notifications

## 📸 Screenshots

Screenshots of the OAI Kitchen website and chatbot.

```markdown
[OAI Kitchen Homepage](screenshots/homepage.png)

[AI Chatbot](screenshots/chatbot.png)

[Menu](screenshots/menu.png)
```

## 🎯 Project Purpose

This project was developed as a practical demonstration of how conversational AI can be integrated into a complete web application rather than being used as an isolated chatbot.

The project combines:

```text
Conversational AI
        +
Backend Engineering
        +
Database Engineering
        +
Web Development
        +
Cloud Deployment
```

The result is a working, cloud-deployed food ordering system where a user can interact naturally with an AI assistant and have those interactions translated into persistent database operations.

## 👨‍💻 Author

Obiajulu Ifeanyichukwu Abah  
Software Engineer | AI, Machine Learning & MLOps Engineer

GitHub:  
https://github.com/Ifeanyi-07

