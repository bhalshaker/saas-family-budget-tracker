# SAAS Family Budget Tracker

## 📄 Abstract

The **Multi-Family Budget Tracking Application** is a simple secure and collaborative financial management tool that allows multiple families to independently track their budgets, expenses, goals, and transactions. With built-in support for multi-tenancy, each family’s data is isolated and confidential.

Users can create accounts, categorize transactions, assign budgets, and track savings goals. This RestFull API system features a flexible many-to-many relationship between families and users, enabling shared access across households with role-based permissions.

Designed with a RESTful API structure, the application supports integration with web and mobile interfaces, empowering families to plan and manage their finances together — with clarity, control, and transparency.


## 🗺️ Entity-Relationship Diagram (ERD)

The following ERD outlines the data structure for the Multi-Family Budget Tracking Application. It defines how core entities such as Families, Users, Transactions, Accounts, Budgets, Goals, and Attachments are related. This schema supports multi-tenancy and ensures data isolation between families while enabling collaborative financial management within each household.

![Family Budget Tracker ERD](/images/family_budget_erd.png)


## 🌐 API Routes for Family Budget Tracker

### 📁 Families
| Method | Route                     | Description                       |
|--------|---------------------------|-----------------------------------|
| GET    | /families                 | List all families                 |
| POST   | /families                 | Create a new family               |
| GET    | /families/{family_id}     | Retrieve a specific family        |
| PUT    | /families/{family_id}     | Update a family                   |
| DELETE | /families/{family_id}     | Delete a family                   |

### 👨‍👩‍👧‍👦 Family Users (Join Table)
| Method | Route                                         | Description                                 |
|--------|-----------------------------------------------|---------------------------------------------|
| GET    | /families/{family_id}/users                   | List all users in a family                  |
| POST   | /families/{family_id}/users                   | Add a user to a family                      |
| DELETE | /families/{family_id}/users/{user_id}         | Remove a user from a family                 |
| GET    | /users/{user_id}/families                     | List all families a user belongs to         |

### 👤 Users
| Method | Route                        | Description                        |
|--------|------------------------------|------------------------------------|
| GET    | /users/                      | List all users                     |
| POST   | /users/                      | Create a new user                  |
| GET    | /users/me                    | Get current user info              |
| POST   | /users/login                 | Login a user                       |
| GET    | /users/{user_id}             | Retrieve a specific user           |
| PUT    | /users/{user_id}             | Update a user                      |
| DELETE | /users/{user_id}             | Delete a user                      |

### 💼 Accounts
| Method | Route                                 | Description                              |
|--------|---------------------------------------|------------------------------------------|
| GET    | /families/{family_id}/accounts        | List all accounts for a family           |
| POST   | /families/{family_id}/accounts        | Create a new account for a family        |
| GET    | /accounts/{account_id}                | Retrieve a specific account              |
| PUT    | /accounts/{account_id}                | Update an account                        |
| DELETE | /accounts/{account_id}                | Delete an account                        |

### 🏷️ Categories
| Method | Route                                 | Description                              |
|--------|---------------------------------------|------------------------------------------|
| GET    | /families/{family_id}/categories      | List all categories for a family         |
| POST   | /families/{family_id}/categories      | Create a new category for a family       |
| GET    | /categories/{category_id}             | Retrieve a specific category             |
| PUT    | /categories/{category_id}             | Update a category                        |
| DELETE | /categories/{category_id}             | Delete a category                        |

### 💸 Transactions
| Method | Route                                         | Description                              |
|--------|-----------------------------------------------|------------------------------------------|
| GET    | /families/{family_id}/transactions            | List all transactions for a family       |
| POST   | /families/{family_id}/transactions            | Create a new transaction for a family    |
| GET    | /transactions/{transaction_id}                | Retrieve a specific transaction          |
| PUT    | /transactions/{transaction_id}                | Update a transaction                     |
| DELETE | /transactions/{transaction_id}                | Delete a transaction                     |

### 📎 Attachments
| Method | Route                                         | Description                              |
|--------|-----------------------------------------------|------------------------------------------|
| GET    | /transactions/{transaction_id}/attachments    | List attachments for a transaction       |
| POST   | /transactions/{transaction_id}/attachments    | Upload a new attachment                  |
| GET    | /attachments/{attachment_id}                  | Retrieve a specific attachment           |
| DELETE | /attachments/{attachment_id}                  | Delete an attachment                     |

### 📊 Budgets
| Method | Route                                 | Description                              |
|--------|---------------------------------------|------------------------------------------|
| GET    | /families/{family_id}/budgets         | List all budgets for a family            |
| POST   | /families/{family_id}/budgets         | Create a new budget for a family         |
| GET    | /budgets/{budget_id}                  | Retrieve a specific budget               |
| PUT    | /budgets/{budget_id}                  | Update a budget                          |
| DELETE | /budgets/{budget_id}                  | Delete a budget                          |

### 🎯 Goals
| Method | Route                                 | Description                              |
|--------|---------------------------------------|------------------------------------------|
| GET    | /families/{family_id}/goals           | List all goals for a family              |
| POST   | /families/{family_id}/goals           | Create a new goal for a family           |
| GET    | /goals/{goal_id}                      | Retrieve a specific goal                 |
| PUT    | /goals/{goal_id}                      | Update a goal                            |
| DELETE | /goals/{goal_id}                      | Delete a goal                            |

### 🔁 Budget Transactions
| Method | Route                                         | Description                              |
|--------|-----------------------------------------------|------------------------------------------|
| GET    | /families/{family_id}/budgettransactions      | List all budget-transaction mappings     |
| POST   | /families/{family_id}/budgettransactions      | Link a transaction to a budget           |
| GET    | /budgettransactions/{budget_transaction_id}   | Get a specific mapping                   |
| DELETE | /budgettransactions/{budget_transaction_id}   | Remove a transaction from a budget       |

## How to

For detailed instructions on setting up and running the application, please refer to our [Getting Started Guide](howto/START_APP.md).

For detailed instructions on setting up and running PostgreSQL in Docker for this application, please see our [PostgreSQL Docker Setup Guide](howto/INSTALL_PG_DOCKER.md).

For detailed instructions on running tests with pytest, please refer to our [Pytest Testing Guide](howto/TEST_THROUGH_PYTEST.md).

## 📚 Libraries & Technologies Used

This project leverages the following key libraries and technologies:

- **Python** — Core application logic and data processing
- **FastAPI** — Web framework for building RESTful APIs
- **SQLAlchemy** — ORM for managing database models and queries
- **PostgreSQL** — Relational database system
- **JWT / OAuth** — Authentication and user session management
- **Pytest and Pytest-HTML** - Python testing framework

## Attributes

 [pytest with Eric](https://pytest-with-eric.com/)https://pytest-with-eric.com/
