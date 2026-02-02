
# ChemFlow Analytics

**React · Django · PyQt5 · Python · TypeScript**

A full-stack chemical equipment data analysis platform with both web and desktop applications.

Upload CSV datasets, visualize equipment metrics, generate PDF reports, and track analysis history — all through a modern, intuitive interface.

---

## Features

### Data Analysis

* **CSV Upload & Parsing** — Drag-and-drop or browse to upload equipment data
* **Real-time Statistics** — Automatic calculation of mean, median, standard deviation, min/max
* **Equipment Distribution** — Visual breakdown by equipment type
* **Interactive Charts** — Histograms, box plots, correlation analysis, trend lines

---

### Visualizations

* Flowrate vs Pressure comparisons
* Temperature trend analysis
* Equipment type distribution (Doughnut / Pie charts)
* Metric-specific analysis (Flowrate, Pressure, Temperature)
* Correlation scatter plots

---

### Reporting

* **PDF Report Generation** — Export comprehensive analysis reports
* **Upload History** — Track and revisit previous analyses (last 5 datasets)
* **Data Preview** — View raw data with sorting and search

---

### Authentication

* User registration and login
* Token-based authentication
* Secure data isolation per user

---

## Architecture

```
chemflow-analytics/
├── backend/                 # Django REST API
│   ├── analyzer/            # Main app
│   │   ├── models.py        # Dataset, Report models
│   │   ├── views.py         # API endpoints
│   │   ├── serializers.py  # DRF serializers
│   │   └── utils.py         # CSV analysis, PDF generation
│   └── config/              # Django settings
│
├── frontend/                # React Web Application
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── contexts/        # Auth & History contexts
│   │   ├── services/        # API client
│   │   └── types/           # TypeScript types
│   └── public/
│
└── desktop/                 # PyQt5 Desktop Application
    ├── gui/                 # UI components
    │   ├── main_window.py
    │   ├── charts_widget.py
    │   ├── stats_widget.py
    │   └── login_dialog.py
    ├── api/                 # Backend client
    │   └── client.py
    └── main.py              # Entry point
```

---

## Quick Start

### Prerequisites

* Python 3.10+
* Node.js 18+
* pip, npm, or yarn

---

## Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/chemflow-analytics.git
cd chemflow-analytics/backend
```

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

```bash
# Run migrations
python manage.py migrate
```

```bash
# Create superuser (optional)
python manage.py createsuperuser
```

```bash
# Start server
python manage.py runserver
```

The API will be available at:
`http://127.0.0.1:8000/api/`

---

## Web Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The web app will be available at:
`http://localhost:5173`

---

## Desktop App Setup

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

---

## API Endpoints

| Endpoint                              | Method | Description                  |
| ------------------------------------- | ------ | ---------------------------- |
| `/api/auth/register/`                 | POST   | Register new user            |
| `/api/auth/login/`                    | POST   | Login and get token          |
| `/api/auth/logout/`                   | POST   | Logout user                  |
| `/api/auth/profile/`                  | GET    | Get user profile             |
| `/api/datasets/`                      | GET    | List user's datasets         |
| `/api/datasets/upload/`               | POST   | Upload CSV file              |
| `/api/datasets/{id}/`                 | GET    | Get dataset details          |
| `/api/datasets/{id}/data/`            | GET    | Get dataset data (paginated) |
| `/api/datasets/{id}/summary/`         | GET    | Get analysis summary         |
| `/api/datasets/{id}/generate_report/` | POST   | Generate PDF report          |
| `/api/reports/`                       | GET    | List generated reports       |

---

## CSV Format

Your CSV file should contain the following columns:

| Column         | Type   | Description                                 |
| -------------- | ------ | ------------------------------------------- |
| Equipment Name | String | Name/identifier of the equipment            |
| Type           | String | Equipment type (e.g., Pump, Valve, Reactor) |
| Flowrate       | Number | Flow rate measurement                       |
| Pressure       | Number | Pressure measurement                        |
| Temperature    | Number | Temperature measurement                     |

### Sample CSV

```
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,120.5,45.2,78.3
Valve-A12,Valve,85.3,32.1,65.8
Reactor-R1,Reactor,200.0,120.5,180.2
```

---

## Tech Stack

### Backend

* Django 4.x — Web framework
* Django REST Framework — API toolkit
* Pandas — Data analysis
* NumPy — Numerical computing
* ReportLab — PDF generation

### Web Frontend

* React 18 — UI library
* TypeScript — Type safety
* Vite — Build tool
* Tailwind CSS — Styling
* Chart.js — Visualizations
* shadcn/ui — Component library

### Desktop App

* PyQt5 — GUI framework
* Matplotlib — Charts and plots
* Pandas — Data processing
* Requests — API communication

---

## Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
MAX_DATASET_HISTORY=5
```

### Frontend Environment Variables

Create a `.env` file in the frontend directory:

```
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## Running Tests

```bash
# Backend tests
cd backend
python manage.py test
```

```bash
# Frontend tests
cd frontend
npm run test
```

---

## Production Builds

### Web Frontend

```bash
cd frontend
npm run build
```

### Desktop App (PyInstaller)

```bash
cd desktop
pyinstaller --onefile --windowed --name="ChemFlow" main.py
```

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes

   ```bash
   git commit -m "Add amazing feature"
   ```
4. Push to the branch
5. Open a Pull Request

---

## Author

Aanya Singh

GitHub: [@AanyaSingh-s]

---

## Acknowledgments

shadcn/ui for React components
Chart.js for interactive charts
ReportLab for PDF generation
