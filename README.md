# 🏙️ City Simulator Service

A real-time city simulation service that simulates people moving randomly across a 100x100 grid.

## 📋 Overview

The City Simulator Service is a Python-based backend application that:
- Simulates the movement of people on a grid in real-time
- Provides a RESTful API for managing people
- Broadcasts simulation state updates via WebSocket
- Persists simulation state with automatic snapshots
- Includes a beautiful web-based visualization interface

## ✨ Features

- **Real-time Simulation**: Watch people move randomly across the grid with live WebSocket updates
- **RESTful API**: Full CRUD operations for managing people in the simulation
- **State Persistence**: Automatic snapshot system to save/restore simulation state
- **Web Interface**: Interactive HTML visualization with real-time statistics
- **Clean Architecture**: Separation of concerns with repositories, services, and routers
- **Type Safety**: Fully typed with Pydantic models and MyPy strict mode
- **Testing**: Comprehensive unit and integration tests with coverage reporting

## 🏗️ Architecture

```
app/
├── models/          # Domain models (Person, Location)
├── repositories/    # Data access layer
│   ├── in_memory/   # In-memory storage implementation
│   └── text_file/   # JSON snapshot storage
├── routers/         # FastAPI endpoints
│   ├── people.py    # People CRUD operations
│   ├── simulation.py # WebSocket simulation endpoint
│   └── schemas/     # Request/response schemas
├── services/        # Business logic layer
│   ├── people.py    # People management
│   ├── simulation.py # Simulation orchestration
│   └── snapshot.py  # State persistence
└── runner/          # Application startup and configuration
```

## 🚀 Getting Started

### Running the Application

Start the server with default settings:
```bash
make run
```

Or with custom host/port:
```bash
python -m app.runner --host localhost --port 8000
```

The application will be available at `http://localhost:8000`

### Configuration

Configure the simulation using environment variables or a `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `GRID_SIZE` | `100` | Size of the grid (width and height) |
| `PEOPLE_AMOUNT` | `100` | Number of people to initialize |
| `SNAPSHOT_INTERVAL` | `50` | Seconds between automatic snapshots |
| `SNAPSHOT_PATH` | `data/people_snapshot.json` | Path to snapshot file |

Example `.env` file:
```env
GRID_SIZE=100
PEOPLE_AMOUNT=150
SNAPSHOT_INTERVAL=60
SNAPSHOT_PATH=data/simulation_state.json
```

## 📡 API Endpoints

### People Management

#### Get All People
```http
GET /people
```

#### Get Single Person
```http
GET /people/{person_id}
```

#### Create Person
```http
POST /people
Content-Type: application/json

{
  "location": {
    "x": 50,
    "y": 50
  }
}
```

#### Delete Person
```http
DELETE /people/{person_id}
```

### Simulation

#### WebSocket Connection
```
WS /simulation/ws
```

Connects to the real-time simulation stream. The server broadcasts the current state of all people approximately once per second.

### Static Files

- `GET /` - Serves the interactive web visualization interface

## 🎨 Web Interface

The built-in web interface provides:
- **Real-time Grid Visualization**: See all people moving across the grid
- **Live Statistics**: Track people count, updates, and updates per second
- **Interactive Controls**: Connect/disconnect from the WebSocket stream
- **Responsive Design**: Beautiful gradient UI that works on all screen sizes
- **Hover Effects**: Hover over people to highlight them and see their coordinates

Simply navigate to `http://localhost:8000` in your browser to access the interface.

## 🧪 Testing

Run the full test suite with coverage:
```bash
make test
```

This runs all unit and integration tests and generates a coverage report.

### Test Structure

```
tests/
├── unit/
│   ├── repository/      # Repository layer tests
│   └── service/         # Service layer tests
└── integration/
    └── fastapi/         # API endpoint tests
```

## 🔧 Development

### Code Quality

Format code:
```bash
make format
```

Run linters and type checking:
```bash
make lint
```

This will:
- Check Poetry configuration
- Run Ruff formatter check
- Run Ruff linter
- Run MyPy type checker

### Dependencies

Update dependencies:
```bash
make update
```

Regenerate lock file:
```bash
make lock
```

## 🔄 How It Works

1. **Initialization**: On startup, the application either loads a saved snapshot or creates random people on the grid
2. **Simulation Loop**: Every second, each person moves to a random adjacent location
3. **Broadcasting**: The current state is broadcast to all connected WebSocket clients
4. **Persistence**: Every N seconds (configurable), the state is saved to a JSON file
5. **API Access**: RESTful endpoints allow programmatic access to create, read, and delete people

### Movement Logic

People move randomly to adjacent cells:
- Each person can move up, down, left, or right
- Movements stay within grid boundaries (0 to GRID_SIZE-1)
- Movement happens synchronously for all people each second

## 📊 Code Coverage

The project targets high code coverage for:
- `app/models`
- `app/repositories`
- `app/routers`
- `app/services`

Coverage reports show:
- Branch coverage
- Missing lines
- Skip empty and fully covered files

## 🛠️ Makefile Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make run` | Run the application |
| `make test` | Run tests with coverage |
| `make lint` | Run all linters and type checking |
| `make format` | Format code with Ruff |
| `make update` | Update dependencies |
| `make lock` | Regenerate Poetry lock file |
| `make amend` | Amend last git commit |

---

**Built with ❤️ using FastAPI and modern Python practices**

*README generated with the help of Cursor and Claude Sonnet 4.5 🤖*
