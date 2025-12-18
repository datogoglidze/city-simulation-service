# city-simulator-service

## Endpoints
- `GET /` - City visualization page
- `GET /people/` - Get current people positions
- `WS /simulation/ws` - WebSocket for real-time updates

## Environment Variables
- `GRID_SIZE: integer` - Controls the size of the grid square
- `PEOPLE_AMOUNT: integer` - Controls the number of people doring first initialization
- `SNAPSHOT_INTERVAL: integer` - Controls the steps interval between snapshots
- `SNAPSHOT_PATH: string` - Path to save snapshots
