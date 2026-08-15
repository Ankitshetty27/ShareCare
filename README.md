# ShareCare

**ShareCare** is a web-based food and clothing redistribution platform designed to reduce waste by connecting donors with verified NGOs that can distribute usable resources to people in need.

The platform provides a centralized system where users can donate surplus food or clothing, while NGOs can view and manage assigned donations and coordinate their collection and distribution.

## Features

* **Food Donation** — Donate surplus food based on quantity, condition, and location.
* **Clothing Donation** — Donate wearable, repairable, or recyclable clothes.
* **NGO Assignment** — Donations can be assigned to suitable NGOs based on location and donation type.
* **Location Tracking** — Uses latitude and longitude to manage donation and NGO locations.
* **Donation Management** — Track donation status and collection information.
* **NGO Dashboard** — NGOs can view donations assigned to them and manage collections.
* **Admin Dashboard** — Provides statistics and analytics about donations and distributions.
* **Donation Analytics** — Displays information such as total donations, meals served, clothes distributed, and NGO activity.
* **Map Integration** — Displays donation and NGO locations using interactive maps.
* **OTP Verification** — Provides email-based OTP verification for user registration.
* **Food Expiry Management** — Food donations are categorized according to their condition and estimated usable time.
* **Smart Donation Routing** — Different donation conditions can be routed toward suitable NGOs or recycling/repair services.

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates
* Bootstrap
* Leaflet.js
* Chart.js

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy

### Database

* PostgreSQL

### Development Tools

* Visual Studio Code
* Git
* GitHub
* pgAdmin

## Project Architecture

```text
ShareCare/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   ├── user.py
│   ├── donation.py
│   └── collection.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── donate.html
│   ├── ngo.html
│   ├── admin.html
│   ├── analytics.html
│   ├── map.html
│   ├── track.html
│   └── ...
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

## How ShareCare Works

```text
Donor
  │
  ▼
Register / Verify Email
  │
  ▼
Submit Donation
  │
  ▼
Donation Details & Location
  │
  ▼
System Processes Donation
  │
  ▼
Suitable NGO / Service
  │
  ▼
Collection
  │
  ▼
Distribution / Recycling
```

## Donation Flow

1. A donor registers on the platform.
2. The donor verifies their email using OTP verification.
3. The donor submits details about the food or clothing donation.
4. The system records the donation and its location.
5. The donation is categorized according to its condition.
6. A suitable NGO or service can be assigned.
7. The NGO views the assigned donation.
8. The donation is collected and distributed or sent for appropriate recycling/repair.

## Food Classification

ShareCare categorizes food according to its condition:

| Condition    |          Approx. Usable Time |
| ------------ | ---------------------------: |
| Fresh        |                     10 hours |
| Medium       |                      5 hours |
| Low          |                      2 hours |
| Contaminated | Not suitable for consumption |

Contaminated food can be directed toward appropriate recycling or disposal processes instead of being distributed for consumption.

## Clothing Classification

Clothing donations can be categorized as:

* **Wearable** — Suitable for direct distribution.
* **Repairable** — Can be repaired before distribution.
* **Recycle** — Not suitable for reuse and can be sent for recycling.

## Dashboard & Analytics

The admin dashboard provides an overview of platform activity, including:

* Total donations
* Meals served
* Clothes distributed
* NGOs served
* Total quantity distributed
* Donation status distribution
* NGO performance
* Donation statistics

Charts are used to make the analytics easier to understand.

## Database

ShareCare uses **PostgreSQL** with **SQLAlchemy** for database management.

The application stores information related to:

* Users
* NGOs
* Donations
* Collections
* Donation status
* Locations
* Distribution information

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ShareCare.git
cd ShareCare
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/sharecare_db
```

**Do not upload the `.env` file to GitHub.**

The `.gitignore` file should contain:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
```

### 5. Create the PostgreSQL Database

Create a PostgreSQL database named:

```text
sharecare_db
```

Make sure PostgreSQL is running before starting the application.

### 6. Run the Application

```powershell
python app.py
```

The application should then be available locally at:

```text
http://127.0.0.1:5000
```

## Security

Sensitive configuration information such as:

* Database passwords
* Flask secret keys
* API keys
* Email credentials

should be stored in environment variables and should **not** be committed to GitHub.

## Future Enhancements

Possible future improvements include:

* Mobile application
* Real-time donation notifications
* Advanced NGO verification
* AI-based food condition detection
* Improved route optimization
* Real-time collection tracking
* Email/SMS notifications
* More detailed impact analytics
* Cloud deployment
* Role-based access control improvements

## Project Objective

The primary objective of ShareCare is to create a digital platform that helps reduce food and clothing waste while improving the redistribution of usable resources through NGOs.

The project aims to make the donation process more organized, transparent, location-aware, and accessible.

## Impact

ShareCare can help:

* Reduce food wastage
* Reduce clothing waste
* Connect donors with NGOs
* Improve donation management
* Support resource redistribution
* Encourage responsible consumption
* Provide better visibility into donation impact

## License

This project was developed as an academic/project-based application.

---

**ShareCare — Turning Surplus Into Support.**
