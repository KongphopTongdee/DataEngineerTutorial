# DataEngineerTutorial

## How to install the library in the enviorment 

1. Open your terminalNavigate to the directory where your virtual environment folder (e.g., .venv or my_env) is located.

2. Activate the environmentRun the appropriate activation command for your operating system and shell: For macOS / Linux ( Bash/Zsh ) : source .venv/bin/activate

## Importance of production pattern with the Airflow

1.The file need to become like this: 

The production pattern

The recommended structure (followed by Astronomer and most production Airflow projects) separates pure business logic from orchestration:

project/
├── dags/
│   └── main.py          # Thin DAG: imports logic, wraps it as tasks
└── include/
    └── video_stats.py   # Pure Python, no Airflow imports

meaning of each file: 

-include/video_stats.py: contains plain functions with no Airflow dependencies

-dags/main.py: imports those functions and wraps them with @task to build the DAG

Benefit: 

-estable: you can unit test business logic without spinning up Airflow

-Locally runnable: python video_stats.py works for quick debugging

-Reusable: the same logic can be used outside Airflow (cron, another orchestrator, ad-hoc scripts)

-Cleaner separation of concerns: orchestration vs. business logic

