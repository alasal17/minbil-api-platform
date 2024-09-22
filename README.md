# MinBil API Platform

MinBil is an innovative digital platform aimed at improving vehicle maintenance services for both car owners and workshops. This repository contains the API module for the **MinBil Platform**, designed specifically for service providers (workshops). 

## Features

The API provides a range of features for the MinBil platform, including:

- **User Authentication**: Handles user registration, login, and password recovery.
- **Workshop Management**: Allows workshops to manage their profiles, services, and customer bookings.
- **Vehicle Administration**: Stores and manages vehicle information and service history.
- **Appointment System**: Manage workshop availability and customer service bookings.
- **Offer System**: Allows workshops to send offers and track their status.
- **Customer Management**: Manage customer data, including contact details and service history.
- **Billing & Invoicing**: Handle customer billing and service invoices.
- **Analytics & Reporting**: Provides insights into business performance.

## Technologies

The project is built using the following technologies:

- **Python** (backend development)
- **Flask-RESTx** (API development)
- **Firebase** (authentication and real-time database)
- **PostgreSQL** (for relational data)
- **Docker** (for containerization)

## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3.8+
- Docker
- Firebase project setup (refer to the [Firebase documentation](https://firebase.google.com/docs) for details)
- PostgreSQL (if using a relational database)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alasal17/minbil-api-platform.git
   cd minbil-api-platform
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Create a `.env` file in the root directory and configure the necessary variables, such as your Firebase credentials and database URL. Example:
     ```bash
     FIREBASE_API_KEY=your_firebase_api_key
     FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
     POSTGRES_DB=your_db_name
     POSTGRES_USER=your_db_user
     POSTGRES_PASSWORD=your_db_password
     ```

5. Set up the PostgreSQL database:
   ```bash
   docker-compose up -d
   ```

6. Run the migrations to create the necessary tables:
   ```bash
   flask db upgrade
   ```

7. Start the application:
   ```bash
   flask run
   ```

### Firebase Setup

To integrate Firebase, ensure you've configured your Firebase project for authentication and database services. You can find more detailed instructions [here](https://firebase.google.com/docs).

### Running Tests

To run the tests, use the following command:

```bash
pytest
```

Make sure to have the appropriate testing configuration in place before running the tests.

## API Documentation

### Authentication

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Authenticate an existing user.
- **POST /auth/reset-password**: Send password reset instructions to the user.

### Workshop Management

- **GET /workshops**: Get a list of workshops.
- **POST /workshops**: Create a new workshop profile.
- **PUT /workshops/{id}**: Update a workshop profile.
- **DELETE /workshops/{id}**: Remove a workshop profile.

### Booking & Appointment System

- **GET /appointments**: Get a list of all appointments.
- **POST /appointments**: Create a new appointment.
- **PUT /appointments/{id}**: Update an appointment.
- **DELETE /appointments/{id}**: Cancel an appointment.

### Billing & Offers

- **GET /invoices**: Retrieve a list of invoices.
- **POST /invoices**: Generate a new invoice.
- **GET /offers**: Retrieve offers sent to customers.
- **POST /offers**: Create and send a new offer.

For more details, check the [API documentation](https://github.com/alasal17/minbil-api-platform/docs).

## Contributing

We welcome contributions to this project. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch to GitHub and create a pull request.

