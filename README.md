# 🏙️ City Simulation Service

A real-time city simulation service that simulates people with different roles moving across a hexagonal grid, with role-based interactions and lifecycle dynamics.

## 📋 Overview

The City Simulation Service is a Python-based backend application that:
- Simulates the movement of people with different roles (Citizens, Killers, Police) on a hexagonal grid in real-time
- Implements role-based interactions: Killers target Citizens, Police target Killers
- Manages people lifecycle with lifespan and death mechanics
- Provides a RESTful API for managing people
- Broadcasts simulation state updates via WebSocket
- Persists simulation state with automatic snapshots
- Temporary includes a beautiful web-based visualization

## ✨ Features

- **Real-time Simulation**: Watch people move randomly across a hexagonal grid with live WebSocket updates
- **Role-Based System**: Three distinct roles (Citizens, Killers, Police) with unique behaviors
- **Action System**: Role-based interactions using the Strategy pattern
  - Killers eliminate adjacent Citizens
  - Police eliminate adjacent Killers
  - Citizens live peacefully
- **Lifecycle Dynamics**: People have lifespan (70-100 units) and die naturally when it reaches zero
- **Hexagonal Grid**: Uses axial coordinates (q, r) for proper hexagonal movement with 6 directions
- **RESTful API**: Full CRUD operations for managing people in the simulation
- **State Persistence**: Automatic snapshot system to save/restore simulation state
- **Web Interface**: Interactive HTML visualization with real-time statistics
- **Clean Architecture**: Separation of concerns with repositories, services, and routers
- **Type Safety**: Fully typed with Pydantic models and MyPy strict mode
- **Testing**: Comprehensive unit and integration tests with coverage reporting

## 🏗️ Architecture

```
app/
├── models/          # Domain models (Person, Location, PersonRole)
│   ├── person.py    # Person and Location dataclasses with roles
│   └── errors.py    # Custom exceptions
├── repositories/    # Data access layer
│   ├── in_memory/   # In-memory storage implementation
│   └── text_file/   # JSON snapshot storage
├── routers/         # FastAPI endpoints
│   ├── people.py    # People CRUD operations
│   ├── simulation.py # WebSocket simulation endpoint
│   └── schemas/     # Request/response schemas
├── services/        # Business logic layer
│   ├── people.py    # People management
│   ├── movement.py  # Hexagonal grid movement logic
│   ├── actions/     # Role-based action system
│   │   ├── actions.py     # ActionsService for kill logic
│   │   └── strategies.py  # Strategy pattern for role behaviors
│   ├── simulation.py # Simulation orchestration (actions + movement)
│   ├── snapshot.py  # State persistence
│   └── websocket.py # WebSocket management
└── runner/          # Application startup and configuration
    ├── cli.py       # CLI with PeopleInitializer
    ├── config.py    # Environment configuration
    └── factory.py   # Service factories
```

## 🚀 Getting Started

### Running with Docker (Recommended)

Pull and run the Docker image with a custom configuration using environment variables:
```bash
docker run -d \
  -p 8000:8000 \
  --env GRID_SIZE=10 \
  --env PEOPLE_AMOUNT=10 \
  --env KILLER_PROBABILITY=0.15 \
  --env POLICE_PROBABILITY=0.10 \
  --env SNAPSHOT_PATH=/data/snapshots/people.json \
  --env SNAPSHOT_INTERVAL=10 \
  --volume city-simulation-service:/data/snapshots \
  --name city-simulation-service \
  --restart always \
  ghcr.io/datogoglidze/city-simulation-service:latest
```

The application will be available at `http://localhost:8000`

### Running Locally

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
| `GRID_SIZE` | `100` | Size of the hexagonal grid (width and height) |
| `PEOPLE_AMOUNT` | `100` | Number of people to initialize |
| `KILLER_PROBABILITY` | `0.1` | Probability (0.0-1.0) that a person is a Killer |
| `POLICE_PROBABILITY` | `0.1` | Probability (0.0-1.0) that a person is Police |
| `SNAPSHOT_INTERVAL` | None | Seconds between automatic snapshots (optional) |
| `SNAPSHOT_PATH` | None | Path to snapshot file (optional) |

Example `.env` file:
```env
GRID_SIZE=100
PEOPLE_AMOUNT=150
KILLER_PROBABILITY=0.15
POLICE_PROBABILITY=0.10
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
    "q": 50,
    "r": 50
  },
  "role": "citizen",
  "is_dead": false,
  "lifespan": 80
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
- **Real-time Hexagonal Grid Visualization**: See all people moving across the hexagonal grid
- **Role Differentiation**: Visual distinction between Citizens, Killers, and Police
- **Death Status**: Visual indicators for dead people
- **Live Statistics**: Track people count, updates, and updates per second
- **Interactive Controls**: Connect/disconnect from the WebSocket stream
- **Responsive Design**: Beautiful gradient UI that works on all screen sizes
- **Hover Effects**: Hover over people to highlight them and see their coordinates and status

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

1. **Initialization**: On startup, the application either loads a saved snapshot or generates people with random roles based on configured probabilities
   - Each person gets a random lifespan (70-100)
   - Roles are assigned: Killers (~10%), Police (~10%), Citizens (remaining)
2. **Simulation Loop**: Every second, the simulation executes in this order:
   - **Actions Phase**: Process role-based interactions
     - Killers eliminate adjacent Citizens
     - Police eliminate adjacent Killers  
   - **Movement Phase**: Each living person moves to a random adjacent hexagonal cell
     - Lifespan decreases by 1
     - Person dies if lifespan reaches 0
3. **Broadcasting**: The current state is broadcast to all connected WebSocket clients
4. **Persistence**: If configured, the state is saved to a JSON file at regular intervals
5. **API Access**: RESTful endpoints allow programmatic access to create, read, and delete people

### Movement Logic

People move randomly to adjacent hexagonal cells:
- Hexagonal grid uses axial coordinates (q, r) with 6 directions:
  - East (1, 0), Northeast (1, -1), Northwest (0, -1)
  - West (-1, 0), Southwest (-1, 1), Southeast (0, 1)
- Only living people move (is_dead=False)
- Movements stay within grid boundaries (0 to GRID_SIZE-1)
- People cannot move to occupied cells
- If all adjacent cells are occupied, person stays in place

### Role-Based Actions

The action system uses the Strategy pattern:
- **CitizenStrategy**: No aggressive actions
- **KillerStrategy**: Targets and kills adjacent Citizens
- **PoliceStrategy**: Targets and kills adjacent Killers

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
