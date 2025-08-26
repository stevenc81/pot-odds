# Pot Odds Calculator Frontend

A modern, responsive React + TypeScript frontend for calculating poker pot odds and analyzing outs in real-time.

## Features

- 🎯 **Real-time Calculations**: Instant pot odds calculation with 150ms debouncing
- 🃏 **Interactive Card Selection**: Touch-friendly card grid with visual feedback
- 🌓 **Dark/Light Theme**: Persistent theme toggle with system preference detection
- 📱 **Responsive Design**: Mobile-first approach with desktop optimization
- ♿ **Accessibility**: WCAG 2.1 AA compliant with full keyboard navigation
- 🚀 **Performance**: Optimized with code splitting and efficient state management
- 🔄 **Error Handling**: Comprehensive error boundaries and API error handling
- 📊 **Results Visualization**: Outs grouped by draw type with detailed analysis

## Tech Stack

- **React 18** - Modern React with concurrent features
- **TypeScript** - Type-safe development with strict mode
- **Vite** - Fast build tool with HMR
- **Tailwind CSS** - Utility-first styling with custom poker theme
- **Zustand** - Lightweight state management
- **React Query** - Server state management with caching
- **Docker** - Containerized deployment

## Quick Start

### Prerequisites

- Node.js 20+ and npm
- Docker and Docker Compose (optional)

### Development

```bash
# Clone the repository
git clone https://github.com/stevenc81/pot-odds.git
cd pot-odds/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:5173 (Vite default port)
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker Deployment

```bash
# Using pre-built Docker Hub image
docker pull stevenc81/pot-odds-frontend:latest
docker run -d -p 3000:3000 --name pot-odds-frontend stevenc81/pot-odds-frontend:latest

# Or build your own
docker build -t pot-odds-frontend .
docker run -d -p 3000:3000 --name pot-odds-frontend pot-odds-frontend

# Using docker-compose (with backend)
cd .. # Go to project root
docker-compose up frontend
```

## Project Structure

```
src/
├── components/
│   ├── ui/                 # Reusable UI components
│   ├── card-selection/     # Card selection components
│   ├── results/           # Results display components
│   └── layout/            # Layout components
├── hooks/                 # Custom React hooks
├── store/                 # Zustand stores
├── types/                 # TypeScript type definitions
├── utils/                 # Utility functions
└── App.tsx               # Main application component
```

## API Integration

The frontend connects to the backend API:

- Default backend URL: `http://localhost:8000`
- API endpoints:
  - `POST /api/calculate` - Calculate pot odds and outs
  - `GET /health` - Health check endpoint

All API calls are debounced to 150ms to prevent excessive requests during card selection.

## Configuration

### Environment Variables

Create a `.env` file for local development:

```bash
# API URL (optional, defaults to /api proxy)
VITE_API_URL=http://localhost:8000
```

### Theme Configuration

Custom poker-themed design system in `tailwind.config.js`:
- Card suit colors (red/black)
- Custom spacing and animations
- Dark/light mode support

## Nginx Configuration

The production Docker image uses Nginx with:
- Gzip compression for all assets
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- API proxy from `/api/*` to backend service
- Client-side routing support
- Cache control headers

## Accessibility

- Full keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus management
- ARIA labels and roles

## Performance Features

- Code splitting with dynamic imports
- Tree shaking for minimal bundle size
- Image optimization
- Efficient re-rendering with React Query
- Local storage for theme persistence
- Bundle size: ~250KB gzipped

## Development Scripts

```bash
npm run dev          # Start development server (port 5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues
npm run type-check   # TypeScript type checking
```

## Testing

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build test
npm run build
```

## Docker Multi-Stage Build

The Dockerfile uses a multi-stage build:

1. **Build stage**: Node.js Alpine for compilation
2. **Production stage**: Nginx Alpine for static serving

Features:
- Small image size (~25MB)
- Non-root user execution
- Health check endpoint
- Optimized nginx configuration

## Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Mobile browsers (iOS Safari 14+, Chrome Mobile 90+)
- Progressive enhancement for older browsers

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

### Docker Build Issues

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t pot-odds-frontend .
```

### API Connection Issues

Check that:
1. Backend is running on port 8000
2. CORS is configured in backend
3. Proxy settings in vite.config.ts are correct

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Include accessibility attributes
4. Test on mobile and desktop
5. Update documentation as needed
6. Run `npm run lint:fix` before committing

## License

MIT License - See LICENSE file for details