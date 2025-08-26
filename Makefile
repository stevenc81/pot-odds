# Makefile for building and pushing Pot Odds Calculator Docker images
DOCKER_HUB_USER := stevenc81
FRONTEND_IMAGE := $(DOCKER_HUB_USER)/pot-odds-frontend
BACKEND_IMAGE := $(DOCKER_HUB_USER)/pot-odds-backend
APP_IMAGE := $(DOCKER_HUB_USER)/pot-odds-app
TAG := latest

.PHONY: all build push clean help login frontend backend app

# Default target
all: build push

# Build all images
build: frontend backend app
	@echo "✅ All images built successfully"

# Push all images to Docker Hub
push: push-frontend push-backend push-app
	@echo "✅ All images pushed to Docker Hub"

# Build frontend image
frontend:
	@echo "🔨 Building frontend image..."
	@cd frontend && docker build -t $(FRONTEND_IMAGE):$(TAG) .
	@echo "✅ Frontend image built: $(FRONTEND_IMAGE):$(TAG)"

# Build backend image
backend:
	@echo "🔨 Building backend image..."
	@cd backend && docker build -t $(BACKEND_IMAGE):$(TAG) .
	@echo "✅ Backend image built: $(BACKEND_IMAGE):$(TAG)"

# Build combined app image
app:
	@echo "🔨 Building combined app image..."
	@docker build -t $(APP_IMAGE):$(TAG) .
	@echo "✅ App image built: $(APP_IMAGE):$(TAG)"

# Push frontend image
push-frontend:
	@echo "📤 Pushing frontend image to Docker Hub..."
	@docker push $(FRONTEND_IMAGE):$(TAG)
	@echo "✅ Frontend image pushed: $(FRONTEND_IMAGE):$(TAG)"

# Push backend image
push-backend:
	@echo "📤 Pushing backend image to Docker Hub..."
	@docker push $(BACKEND_IMAGE):$(TAG)
	@echo "✅ Backend image pushed: $(BACKEND_IMAGE):$(TAG)"

# Push combined app image
push-app:
	@echo "📤 Pushing app image to Docker Hub..."
	@docker push $(APP_IMAGE):$(TAG)
	@echo "✅ App image pushed: $(APP_IMAGE):$(TAG)"

# Login to Docker Hub
login:
	@echo "🔐 Logging in to Docker Hub..."
	@docker login -u $(DOCKER_HUB_USER)

# Run the combined app locally
run:
	@echo "🚀 Running Pot Odds Calculator app..."
	@docker run -d -p 8080:80 --name pot-odds-app $(APP_IMAGE):$(TAG)
	@echo "✅ App running at http://localhost:8080"
	@echo "   Stop with: docker stop pot-odds-app"
	@echo "   Remove with: docker rm pot-odds-app"

# Stop and remove running container
stop:
	@echo "🛑 Stopping and removing pot-odds-app container..."
	@docker stop pot-odds-app 2>/dev/null || true
	@docker rm pot-odds-app 2>/dev/null || true
	@echo "✅ Container stopped and removed"

# Clean up local images
clean:
	@echo "🧹 Cleaning up local images..."
	@docker rmi $(FRONTEND_IMAGE):$(TAG) 2>/dev/null || true
	@docker rmi $(BACKEND_IMAGE):$(TAG) 2>/dev/null || true
	@docker rmi $(APP_IMAGE):$(TAG) 2>/dev/null || true
	@echo "✅ Local images cleaned"

# Development: rebuild and run
dev: stop build run
	@echo "✅ Development environment ready at http://localhost:8080"

# Show all available commands
help:
	@echo "Pot Odds Calculator - Docker Build System"
	@echo ""
	@echo "Available commands:"
	@echo "  make all          - Build and push all images (default)"
	@echo "  make build        - Build all three Docker images"
	@echo "  make push         - Push all images to Docker Hub"
	@echo "  make frontend     - Build frontend image only"
	@echo "  make backend      - Build backend image only"
	@echo "  make app          - Build combined app image only"
	@echo "  make login        - Login to Docker Hub"
	@echo "  make run          - Run the app locally on port 8080"
	@echo "  make stop         - Stop and remove running container"
	@echo "  make dev          - Rebuild and run for development"
	@echo "  make clean        - Remove all local images"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Docker Hub images:"
	@echo "  Frontend: $(FRONTEND_IMAGE):$(TAG)"
	@echo "  Backend:  $(BACKEND_IMAGE):$(TAG)"
	@echo "  App:      $(APP_IMAGE):$(TAG)"