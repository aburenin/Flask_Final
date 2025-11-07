 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..fc0ea21caa4f9e0ba1a8dc4a321fd3c885846702
--- /dev/null
+++ b/README.md
@@ -0,0 +1,108 @@
+# 📸 Fotos Baby Flask Application
+
+## Overview / Описание
+This repository contains a production-oriented Flask application for a baby and maternity photography studio. The project delivers a marketing website, a password-protected client area, and an internal admin dashboard that allows the studio team to manage photo galleries, pricing bundles, and FAQ content from a single place. Static assets are processed with Flask-Assets, while Cloudflare Turnstile protects the public contact form.
+
+Репозиторий содержит Flask-приложение для фотостудии (новорождённые, беременность и дети). Проект объединяет публичный сайт, личные кабинеты клиентов и админку для ведения галерей, ценовых пакетов и ответов на популярные вопросы. Для статических ресурсов используется Flask-Assets, а контактная форма защищена Cloudflare Turnstile.
+
+## ✨ Key Features
+- **Marketing pages** (home, pricing, portfolio, about, contact, privacy) rendered from Jinja templates.
+- **Dynamic pricing and FAQ blocks** seeded from the database at start-up to keep content in sync with `config.pakets` and `config.qa_list`.
+- **Client proofing area** that generates responsive galleries, supports HTMX-powered approval workflows, and exports ZIP archives of client photos.
+- **Admin dashboard** for creating projects, uploading images, and resetting client passwords using Flask-Login and bcrypt hashing.
+- **Email and CAPTCHA integration** for the contact form via Flask-Mail and Cloudflare Turnstile.
+- **Automated portfolio gallery builder** that pre-renders responsive HTML fragments for each photography category.
+
+## 🗂️ Project Layout
+```
+Flask_Final/
+├── app_init.py          # Application factory: extensions, assets, DB bootstrap
+├── app_route.py         # HTTP routes for public, admin, and client areas
+├── Client.py            # SQLAlchemy model and helpers for studio clients
+├── Proof.py             # Client gallery generation and ZIP export helpers
+├── Preise.py / Question.py
+│   └── Database seeders for pricing and FAQ content
+├── Support.py           # Mail delivery + EXIF-aware image orientation helpers
+├── portfolio/           # Portfolio gallery builder utilities
+├── static/              # Compiled CSS/JS, images, and media assets
+├── templates/           # Jinja templates (public pages, modals, admin UI)
+├── instance/            # SQLite database (`fotos-baby.db`) is created here
+├── requirements.txt     # Python dependencies
+└── Dockerfile           # Production image with Gunicorn + eventlet
+```
+
+## 🚀 Getting Started
+1. **Install prerequisites**
+   - Python 3.12 (matches the Docker image) and pip.
+   - SQLite (ships with Python on most platforms).
+2. **Clone the repository**
+   ```bash
+   git clone https://github.com/<your-org>/Flask_Final.git
+   cd Flask_Final
+   ```
+3. **Create and activate a virtual environment**
+   ```bash
+   python3 -m venv .venv
+   source .venv/bin/activate  # Windows: .venv\Scripts\activate
+   ```
+4. **Install dependencies**
+   ```bash
+   pip install -r requirements.txt
+   ```
+5. **Create the instance folder (if it does not exist)**
+   ```bash
+   mkdir -p instance
+   ```
+
+## 🔐 Environment Configuration
+Create a `.env` file in the project root before launching the app. The table below lists the most important variables referenced in the code base:
+
+| Variable | Required | Description |
+|----------|----------|-------------|
+| `ADMIN_KEY` | ✅ | Master secret used in `config.SECRET_KEY` to sign Flask sessions. Generate a long random string. |
+| `SECRET_KEY` | ✅ | Cloudflare Turnstile secret (server-side) used to verify CAPTCHA tokens. Despite the name collision with Flask, it is read directly via `os.getenv`. |
+| `SITE_KEY` | ✅ | Cloudflare Turnstile public site key injected into the contact template. |
+| `VERIFY_URL` | ✅ | Cloudflare Turnstile verification endpoint (e.g. `https://challenges.cloudflare.com/turnstile/v0/siteverify`). |
+| `IP` / `PORT` | ⬜️ | Host and port for local development when running `python app_route.py`. Defaults are not provided, so set `IP=127.0.0.1`, `PORT=5000` for development. |
+| `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_SERVER`, `MAIL_PORT` | ⬜️ | Override the defaults in `config.py` if you deploy with a different SMTP provider. |
+
+> **Note:** For production deployments rename either the Flask or Turnstile secret in the configuration to avoid ambiguity. The current code base expects both variables.
+
+After creating the `.env` file, reload your shell or export the variables manually so that `python-dotenv` can pick them up.
+
+## 🗃️ Database & Seed Data
+- On the first launch the app creates `instance/fotos-baby.db` and initializes the schema defined in `Client`, `Preise`, and `Question`.
+- Pricing bundles (`pakets`) and FAQ entries (`qa_list`) are synchronized from `config.py` into the database every time the app starts, ensuring changes in code propagate to production automatically.
+- To add an admin user (e.g., `adminka`) or client projects, sign in via `/login/` after inserting the hashed credentials manually, or use the admin dashboard to create new projects once an initial admin account exists in the database.
+
+## ▶️ Running the Application
+### Development server
+```bash
+flask --app app_route run --debug
+# or
+python app_route.py
+```
+The development server compiles CSS bundles on demand (via Flask-Assets) and exposes public pages at `http://127.0.0.1:5000/` by default.
+
+### Production (Gunicorn + eventlet)
+A Dockerfile is provided. Build and run the container after supplying a `.env` file (or Docker secrets):
+```bash
+docker build -t fotos-baby .
+docker run --env-file .env -p 5000:5000 fotos-baby
+```
+Gunicorn serves the Flask application using the `eventlet` worker to support concurrent uploads in the admin area.
+
+## 🧪 Testing
+Preliminary pytest stubs live in `test/`. Extend them with real assertions and run:
+```bash
+pytest
+```
+Pytest will automatically discover files in the `test/` package.
+
+## 🛠️ Useful Maintenance Tasks
+- **Regenerate portfolio galleries**: Every restart calls `Gallery.clear_temlates()` to rebuild `gallery.html` fragments for each portfolio category. Delete the generated files under `static/media/<category>/gallery.html` if you want to force regeneration manually.
+- **Bulk client uploads**: The admin interface stores original files plus optimized `small/` and `blur/` WebP variants and corrects EXIF orientation in background threads.
+- **Client downloads**: Use `/client-gallery/<username>?action=download` to produce ZIP archives with all original images for a project.
+
+---
+Happy shooting and smooth deployments! 📷
 
EOF
)
