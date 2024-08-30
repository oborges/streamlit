# Use the official Streamlit image as a base
FROM streamlit/streamlit:latest

# Copy the app into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.enableCORS=false"]

