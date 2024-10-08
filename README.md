# YouTube Thumbnail Analyzer

## Environment Setup
1. Create a `.env` file in the project root directory.
2. Add the following variables to the `.env` file:
   ```bash
   # Groq Cloud API Key
   GROQ_CLOUD_API_KEY=your_groq_cloud_api_key_here

   # MySQL database connection info
   MYSQL_USER=root
   MYSQL_PASSWORD=password
   MYSQL_HOST=mysql_db
   MYSQL_DATABASE=thumbnail_feedback
   MYSQL_PORT=3306

   # Groq Cloud Vision Model
   GROQ_CLOUD_MODEL=llama-3.2-11b-vision-preview
   ```
3. Make sure that the MySQL database is properly set up.
   ```sql
   CREATE TABLE feedback (
      id INT AUTO_INCREMENT PRIMARY KEY,
      image_url TEXT NOT NULL,
      score INT NOT NULL,
      comment TEXT NOT NULL,
      created_at DATETIME NOT NULL
   );
   ```


## Running the Project

1. Build and run the services using Docker:
   ```bash
   docker-compose up --build
   ```

2. The FastAPI backend will be available at `http://localhost:8000`, and the frontend (if provided) will be available at `http://localhost:5173`.

## Using the API

- You can send a POST request to `/analyze-thumbnail/` with an image file to get the analysis.