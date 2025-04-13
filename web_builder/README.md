# AI-Powered Website Builder

An application that generates website content using Hugging Face's AI models and renders it using a professional template.

## Features

- User authentication with JWT
- AI-generated website content based on business name and industry
- Professional website template
- Preview functionality
- MongoDB storage for users and websites

## Prerequisites

- Python 3.7+
- MongoDB
- Hugging Face API key

## Setup Instructions

1. Clone the repository
2. cd web_builder
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key-for-jwt-tokens
   JWT_SECRET_KEY=your-jwt-secret-key
   MONGO_URI=your-mongodb-connection-string
   HUGGINGFACE_API_KEY=your-huggingface-api-key
   HUGGINGFACE_MODEL=deepseek  # or another model of your choice
   ```

5. Run the application:
   ```
   python main.py
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "access_token": "jwt-token", "user": { "id": "user-id", "email": "user@example.com" } }`

- `POST /api/auth/login` - Login a user
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "access_token": "jwt-token", "user": { "id": "user-id", "email": "user@example.com" } }`

- `GET /api/auth/user` - Get current user info (protected)
  - Response: `{ "user": { "id": "user-id", "email": "user@example.com", "created_at": "timestamp", "last_login": "timestamp" } }`

### Websites

- `POST /api/websites` - Create a new website (protected)
  - Request body: `{ "name": "Business Name", "industry": "Industry", "description": "Optional description" }`
  - Response: `{ "message": "Website created successfully", "website": { ... } }`

- `GET /api/websites` - Get all websites for current user (protected)
  - Response: `{ "websites": [ ... ] }`

- `GET /api/websites/<website_id>` - Get a specific website (protected)
  - Response: `{ "website": { ... } }`

- `PUT /api/websites/<website_id>` - Update a website (protected)
  - Request body: `{ "content": { ... }, "name": "Updated Name", "industry": "Updated Industry" }`
  - Response: `{ "message": "Website updated successfully", "website": { ... } }`

- `DELETE /api/websites/<website_id>` - Delete a website (protected)
  - Response: `{ "message": "Website deleted successfully" }`

- `GET /api/websites/preview/<website_id>` - Preview a website (protected)
  - Response: HTML content of the rendered website

## Implementation Notes

- Authentication is handled using Flask-JWT-Extended with JWT tokens.
- Website content is generated using Hugging Face's API.
- MongoDB is used for storing user accounts and website data.
- The template is built with Tailwind CSS for responsive design.
