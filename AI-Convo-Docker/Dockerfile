# Use the official Ollama base image
FROM ollama/ollama:latest

# Download the Phi model
RUN ollama pull phi

# Expose the Ollama API port
EXPOSE 11434

# Start the Ollama server
CMD ["ollama", "serve"]