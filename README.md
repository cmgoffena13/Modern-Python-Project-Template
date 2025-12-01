# Modern Python Project Template

Example Python Project showcasing best practices in configuration, logging, testing, and continuous integration.

## Development Setup

 1. Utilize `uv` to sync packages: `uv sync` or utilize the Make command `setup`
 2. Install pre-commit hooks `uv run -- pre-commit install --install-hooks`

## Main Packages
 - Ruff
 - Pydantic-Settings
 - Pytest (Pytest-Xdist for parallel tests)
 - Pre-Commit
 - Logger (StructLog)
   - OpenTelemetry Packages

## Settings

The settings are divided into 4 core classes:  
 - Global Config
   - Holds all environment variables and their defaults
   - Allows for easy overwrites for the other environments
 - Dev Config
   - Override the environment variables in code if static
 - Test Config
   - Override the environment variables in code if static
 - Prod Config
   - Override the environment variables in code if static

The settings setup allows for us to easily set the current environment by declaring `ENV_STATE=` and then we can declare all of our environment variables with the appropriate prefix (DEV, TEST, PROD). This has numerous benefits:  
 1. We explicitly declare our environment to avoid confusion. Ex. `ENV_STATE=DEV`
 2. We explicitly declare our environment variables with the correct prefix to avoid confusion. Ex. `DEV_DATABASE_URL`
 3. We can hardcode specific environment variables to declutter our .env file. Ex. Hardcoding DATABASE_URL in TestConfig to be a sqlite database.
 4. We can overwrite any configuration if needed through an environment variable. Ex. `PROD_LOG_LEVEL=DEBUG`

## Logger

### Logger Components
 - Logger
    - Creates the log messages, normally one per file
 - Handler
    - Handlers determine the destination of the logs
 - Formatter
    - Specifies the format of the log message itself

### Logger Levels
 - DEBUG
   - Show detailed information
   - Example: Show record values that are inserted for every insert
- INFO
   - Normal operation events
   - Example: Show that a batch of records was inserted
- WARNING
   - When something undesirable happens, but does not impact runtime
   - Example: Show that there were no records available to insert, we expect records
- ERROR
   - When an exception occurs
   - Example: Show that the batch insert failed with an exception
   - NOTE: Use `logger.exception` as best practice to include the traceback when its unexpected
- CRITICAL
   - Application cannot continue
   - Example: Show that the database connection could not be created, unable to insert records

### Best Practices
 - Utilize `structlog` to create the Python logger. Ex. `logger = structlog.get_logger(__name__)`
    - This allows for flexible metadata injection. Ex. `logger.info("message", user_id="1235")`
 - Always name your logger utilizing the __name__ dunder method. This has the logger show up under the src directory and inherit from the src logger. Ex. __name__ shows up as `src.utils`
 - Utilize the correct logger level and choose key points in your code for INFO messages to help you understand the code flow.
 - Utilize OpenTelemetry traces to track individual processes. This is especially useful for code that executes in parallel. Ex. 
 ```
 from opentelemetry import trace
 
 tracer = trace.get_tracer(__name__)
  
 with tracer.start_as_current_span("tracer name"):
    trigger_process()
 ```