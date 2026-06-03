# RouteSage: AI-Driven Dynamic Logistics Optimizer

RouteSage is a sophisticated platform designed for logistics companies to optimize delivery routes in real-time, simulate various scenarios, and gain predictive insights into their operations. Leveraging AI, it continuously improves routing recommendations and provides analytics on delivery ETAs and resource utilization.

## Core Features

*   **Real-time GPS tracking integration:** Monitor vehicle locations and progress dynamically.
*   **Dynamic route re-optimization:** Adjust routes on the fly based on live traffic, new orders, or unexpected events.
*   **Multi-vehicle routing problem (MVRP) solver:** Efficiently assign and sequence orders across multiple vehicles.
*   **Scenario simulation and 'what-if' analysis:** Test the impact of potential disruptions (e.g., traffic changes, new orders, vehicle breakdowns) before they happen.
*   **Predictive ETA and delay forecasting:** Provide accurate estimated times of arrival and predict potential delays.
*   **Driver performance and efficiency metrics dashboard:** Track and analyze driver performance, on-time delivery rates, and route efficiency.
*   **API for third-party system integration:** Seamlessly connect with existing logistics management systems.

## Project Structure

```
. 
├── config/                 # Configuration files (e.g., settings.py)
├── docs/                   # API documentation and other project docs
├── src/                    # Main application source code
│   ├── api/                # FastAPI routes and Pydantic schemas
│   ├── data_ingestion/     # Modules for GPS tracking and order parsing
│   ├── metrics/            # Performance analysis and dashboard generation
│   ├── routing_engine/     # Core routing optimization and graph building logic
│   ├── simulation/         # Scenario generation and simulation engine
│   └── main.py             # Application entry point
├── tests/                  # Unit and integration tests
└── requirements.txt        # Python dependencies
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/routesage.git
    cd routesage
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables (optional but recommended):**
    Create a `.env` file in the project root based on `config/settings.py`.
    Example `.env`:
    ```
    DATABASE_URL="sqlite:///./routesage.db"
    API_KEY="your_super_secret_api_key"
    MAP_PROVIDER_API_KEY="your_map_api_key" # e.g., for Google Maps API
    DEFAULT_VEHICLE_SPEED_KMH=40.0
    ```

## How to Run

1.  **Start the FastAPI application:**
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

2.  **Access the API documentation:**
    Once the server is running, you can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the unit and integration tests, use `pytest`:

```bash
pytest
```

## API Endpoints Overview

*   `POST /api/v1/optimize`: Calculate optimal delivery routes.
*   `POST /api/v1/simulate`: Run a logistics scenario simulation.
*   `POST /api/v1/gps_update`: Receive GPS update and trigger re-optimization.
*   `POST /api/v1/orders`: Add new orders to the system.
*   `GET /api/v1/metrics/driver/{driver_id}`: Get driver performance metrics.
*   `GET /api/v1/metrics/dashboard_report`: Generate a comprehensive dashboard report.

For detailed API specifications, refer to `docs/api_reference.md` or the interactive Swagger UI.

## Future Enhancements

*   Integration with real-time map and traffic APIs (e.g., Google Maps, HERE Technologies).
*   Advanced MVRP algorithms (e.g., Google OR-Tools, custom metaheuristics).
*   Machine learning models for more accurate ETA prediction and traffic forecasting.
*   Persistent data storage (PostgreSQL, MongoDB) instead of in-memory dictionaries.
*   User authentication and authorization.
*   A dedicated frontend dashboard for visualization.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.