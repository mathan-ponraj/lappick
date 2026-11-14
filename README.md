# EduHelpDesk

Every ticket, on the clock. A Flask ticketing portal that tracks SLA deadlines and keeps an audit trail of every status change.

[![Live Demo](https://img.shields.io/badge/LIVE%20DEMO-Try%20EduHelpDesk-6366f1?style=for-the-badge&logo=render&logoColor=white)](https://eduhelpdesk.onrender.com/)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20APIs-02569B?style=for-the-badge&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## Problem Statement

Academic support requests often get lost or answered late when there is no system tracking them. Students, support staff, and managers need one place to see every request, its deadline, and who is responsible for it.

## What I Built

In this project, I built a ticketing portal in Flask where students and staff manage requests under role-based access control. It tracks SLA deadlines, flags overdue tickets for escalation, and keeps an audit trail of every status change. I stored the data in SQLite, exposed it through REST APIs, and deployed the app on Render.

## Key Features

- Gives Students, Support Staff, and Managers separate dashboards with role-based access control.
- Creates, assigns, tracks, and resolves support tickets.
- Sets ticket priority to Low, Medium, High, or Critical.
- Tracks SLA deadlines, remaining time, and breaches.
- Flags overdue tickets for escalation and shows ticket ageing.
- Lets managers escalate tickets that need more attention.
- Keeps an audit trail of every status change, with the user and time.
- Shows managers ticket statistics and staff workload.

## Tech Stack

| Area            | Tools                   |
| --------------- | ----------------------- |
| Language        | Python, JavaScript      |
| Frontend        | HTML5, CSS3, JavaScript |
| Backend         | Flask                   |
| Database        | SQLite                  |
| API             | REST APIs               |
| Access control  | Role-based access (RBAC)|
| Deployment      | Render, Gunicorn        |
| Version control | Git, GitHub             |

## Project Structure

```text
EduHelpDesk/
│
├── app.py              # Flask app, routes, and business logic
├── requirements.txt    # Python dependencies
├── templates/          # HTML pages
├── static/             # CSS and JavaScript files
└── README.md           # Project documentation
```

<!-- [TODO: replace this tree with your real folders and files, and add one line per file] -->

## Data

- **Source:** Data created by users inside the app. No outside dataset is used.
- **Database:** SQLite with three main tables.
  - **Users:** Student, staff, and manager accounts, roles, and password hashes.
  - **Tickets:** Ticket details, priority, status, assigned staff, SLA deadline, and resolution details.
  - **Ticket Activity:** The audit trail. It stores each action, comment, user, and timestamp.
- **Why separate tables:** Keeping the audit trail apart from the ticket record shows both the current state and everything that happened before.
- **Size:** [TODO: add the number of tickets or users if you have it]
- **Columns:** [TODO: list the main columns of each table]

## Approach / Methodology

1. Defined three roles and what each one can see and do.
2. Designed the SQLite tables for users, tickets, and ticket activity.
3. Built the Flask backend and REST APIs.
4. Added controlled status changes so a ticket can only move through valid steps.
5. Added staff assignment and workload tracking.
6. Calculated SLA deadlines and breaches from timestamps.
7. Flagged overdue tickets so managers can escalate them.
8. Added a student response step that returns a waiting ticket to In Progress.
9. Logged every status change in the audit trail.
10. Required a resolution comment and saved a resolution time for every closed ticket.
11. Built the HTML, CSS, and JavaScript interface and the manager dashboard.
12. Deployed the app on Render with Gunicorn.

**Ticket lifecycle:**

```text
Ticket created -> Assigned -> In Progress -> Resolved
                                  |
                                  v
                       Waiting for Student
                                  |
                                  v
                          Student responds
                                  |
                                  v
                            In Progress
```

Managers can monitor and escalate tickets at any stage.

**Who can do what:**

| Student                   | Support staff         | Manager                 |
| ------------------------- | --------------------- | ----------------------- |
| Create tickets            | View assigned tickets | Monitor all tickets     |
| Track ticket status       | Respond to students   | Assign tickets          |
| View responses            | Request information   | Escalate tickets        |
| Submit additional details | Resolve tickets       | Monitor SLA performance |
| View resolution details   | Track ageing          | Monitor staff workload  |

## Results and Insights

- Live and deployed: [eduhelpdesk.onrender.com](https://eduhelpdesk.onrender.com/)
- Tested workflows:
  - Registration and login
  - Ticket creation and assignment
  - Priority and status changes
  - Messages between students and staff
  - SLA calculations and ticket ageing
  - Escalation and resolution
  - Audit trail and the manager dashboard
  - Role-based access
- Tickets handled during testing: [TODO: add the number]
- Example insight from the dashboard: [TODO: add one finding, such as the ticket status split]

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/mathan-ponraj/EduHelpDesk.git
```

Go to the project folder:

```bash
cd EduHelpDesk
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux, use `source venv/bin/activate` instead.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Screenshots

| Student dashboard | Create ticket |
| ----------------- | ------------- |
| ![Student dashboard](screenshots/student-dashboard.png) | ![Create ticket](screenshots/create-ticket.png) |

| Staff view | Manager dashboard |
| ---------- | ----------------- |
| ![Staff view](screenshots/staff-view.png) | ![Manager dashboard](screenshots/manager-dashboard.png) |

<!-- [TODO: add your screenshots to a screenshots/ folder with these file names, or update the paths] -->

## What I Learned and Future Improvements

**What I learned**

- Built a backend with Flask and REST APIs.
- Designed a relational database in SQLite and separated current data from history.
- Used timestamps to calculate SLA deadlines, ticket ageing, and breaches.
- Built role-based access control so each user sees only what they should.
- Kept an audit trail so every status change can be traced.
- Turned business rules into code, such as valid status changes and required resolution comments.
- Connected the frontend and backend, then tested, debugged, and deployed the app.

**Future improvements**

- Add charts to the manager dashboard to show ticket trends over time.
- Analyse resolved tickets to find common issues and average resolution time.
- Add email notifications for ticket updates.

## Contact

[![Live Demo](https://img.shields.io/badge/Live%20Demo-EduHelpDesk-6366f1?style=for-the-badge&logo=render&logoColor=white)](https://eduhelpdesk.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-mathan--ponraj-181717?style=for-the-badge&logo=github)](https://github.com/mathan-ponraj)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-mathan03-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/mathan03/)

---

Developed by Mathan
