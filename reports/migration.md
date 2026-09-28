# Flask Foundation → FastAPI: migration report

## 1. Start with this: the boilerplate no longer installs

Some of this migration will be forced on you whichever framework you pick. `requirements.txt` uses `>=` pins, so a fresh install pulls today's versions, and the app breaks on import:

| File | What breaks on a fresh install |
|---|---|
| `appname/__init__.py:7` | `flask.exthook` was removed in Flask 1.0 |
| `manage.py` | Flask-Script is dead and doesn't work with Flask 2+ |
| `appname/extensions.py:1` | Flask-Cache is dead (its successor is Flask-Caching) |
| `appname/forms.py` | `Form`, `TextField` and `validators.required` were removed in Flask-WTF 1.x / WTForms 3 |
| `requirements.txt` | `mysql-python` only runs on Python 2 |
| `makefile.sh` | Creates a `python2.7` virtualenv |

So this isn't really a port. The **app code moves over** (models, templates, migrations, tests). The **glue gets rebuilt** (factory, extensions, CLI, auth, forms).

## 2. A concrete example: the `/restricted` page

**Today (Flask):**

```
GET /restricted
   │
   ▼
@login_required ──► Flask-Login reads the session cookie
   │                     │
   │                     ▼
   │                user_loader ──► User.query.get(id)   (global db, app context)
   │                     │
   │      not logged in ─┴─► redirect to login_view "main.login"
   ▼
view function runs
```

**In FastAPI:**

```
GET /restricted
   │
   ▼
route has parameter  user = Depends(require_user)
   │
   ▼
require_user ──► depends on get_db (yields a Session)
   │             reads request.session["user_id"]  (Starlette SessionMiddleware)
   │             select(User) ...
   │      not logged in ─► raises a custom exception
   │                            │
   │                            ▼
   │                  exception handler ──► RedirectResponse("/login?next=...")
   ▼
route function runs, with `user` already loaded
```

Takeaway: Flask hides things in globals and decorators (`current_user`, `User.query`, `db.session`). FastAPI makes each one an explicit dependency in the function signature. That means more wiring up front, but it's easier to test and reason about.

## 3. Component mapping

| Flask piece (in this repo) | FastAPI equivalent | Effort |
|---|---|---|
| `create_app(object_name)` + config classes | `create_app()` + **pydantic-settings** `Settings`, chosen with `APP_ENV` / `.env`; startup and shutdown go in `lifespan` | 🟢 Small |
| `Blueprint('main')` | `APIRouter` | 🟢 Small |
| Flask-SQLAlchemy (`db.Model`, `User.query`) | Plain **SQLAlchemy 2.0** (`DeclarativeBase`, `select()`), or **SQLModel**. The session comes from a `get_db` dependency. `Model.query` goes away. | 🟡 Medium |
| Flask-Migrate + existing Alembic setup | **Alembic directly**. `env.py` reads the URL from `Settings` instead of `current_app`. `e1fd4f5d9819_create_table_user.py` can be reused as is. | 🟢 Small |
| Flask-Script `manage.py` (server, shell, show-urls, clean) | `fastapi dev` / `uvicorn` for the server, plus **Typer** for custom commands. The shell is just `ipython` with imports. | 🟢 Small |
| Flask-Login (`login_required`, `current_user`, `user_loader`, `login_view`) | **Nothing first-party.** Either write your own session dependency (above), use **fastapi-users**, or for an API use `OAuth2PasswordBearer` + JWT | 🔴 Largest |
| Flask-WTF (forms, CSRF, `validate_on_submit`) | Pydantic form models (`Form()`). CSRF isn't built in; add `starlette-csrf` or similar. You re-render validation errors into the template yourself. | 🔴 Large |
| `flash()` / `get_flashed_messages` | No equivalent. Write a small session-based helper, or use a tiny library. | 🟡 Medium |
| Jinja templates + `url_for` | `Jinja2Templates`. `url_for` works, but blueprint-relative names like `'.home'` must become route names. `current_user` and flashes must be put into the context, e.g. with a context processor. | 🟡 Medium |
| Flask-Assets (bundling, minifying) | No equivalent. Serve `StaticFiles`, and use Vite/esbuild if you need bundling. | 🟢 Small |
| Flask-Cache `@cache.cached` | `fastapi-cache2`, or better, HTTP cache headers / a reverse proxy | 🟢 Small |
| Flask-DebugToolbar | Optional `fastapi-debug-toolbar`. You also get `/docs` (Swagger) for free. | 🟢 Small |
| `werkzeug.security` hashing | Keep it as a standalone dependency so existing hashes still verify, or switch to `pwdlib`/argon2 and rehash on login | 🟢 Small |
| `test_client()` + pytest fixtures | `TestClient` (httpx-based) + `app.dependency_overrides[get_db]` | 🟡 Medium |
| `mysql-python` | `PyMySQL`/`mysqlclient` for sync, `asyncmy` for async | 🟢 Small |
| `makefile.sh` + flake8 + pylint | `uv` + `pyproject.toml` + **ruff** | 🟢 Small |

## 4. Suggested structure

```
app/
├── main.py            ← create_app(): middleware, static, routers, lifespan
├── core/
│   ├── config.py      ← Settings (Dev/Test/Prod via APP_ENV)
│   └── security.py    ← password hashing, session/JWT helpers
├── db/
│   ├── base.py        ← DeclarativeBase
│   └── session.py     ← engine, SessionLocal, get_db()
├── models/user.py     ← SQLAlchemy models
├── schemas/user.py    ← Pydantic request/response models  (new layer)
├── dependencies.py    ← get_current_user, require_user
├── routers/
│   ├── pages.py       ← Jinja pages: home, login, logout, restricted
│   └── api/           ← JSON endpoints (where FastAPI shines)
├── templates/  static/
cli.py                 ← Typer (replaces manage.py)
migrations/            ← Alembic
tests/conftest.py      ← app + db fixtures with dependency_overrides
pyproject.toml
```

## 5. Tradeoffs

**What you gain with FastAPI:**

- Pydantic validation and serialization on every endpoint
- OpenAPI docs generated automatically (`/docs`)
- Async support when you need it
- Explicit dependency injection, which makes testing easier
- Type hints throughout

**What you lose:**

- This boilerplate is **server-rendered HTML**: Jinja, forms, a session login and flash messages. That's exactly where Flask's ecosystem is strongest and where FastAPI has no first-party pieces.
- You'd be rebuilding login, CSRF, flash messages and form re-rendering yourself.

```
                 Flask ecosystem      FastAPI ecosystem
HTML + forms     ████████████         ████░░░░░░░░
Session auth     ████████████         ████░░░░░░░░
JSON APIs        ██████░░░░░░         ████████████
Validation/docs  ████░░░░░░░░         ████████████
Async            ████░░░░░░░░         ████████████
```

**Sync or async?** Start **sync**: regular `def` routes and sync SQLAlchemy. FastAPI runs those in a thread pool. Async SQLAlchemy has pitfalls (lazy loading fails, you need `selectinload` everywhere), so only switch when you have a real I/O-bound reason.

## 6. How hard is it?

The codebase is small (about 250 lines of Python), so size isn't the problem.

| Path | Effort | Notes |
|---|---|---|
| **A. Like-for-like HTML port** (Jinja, cookie session, forms) | ~2–4 days | Most of the time goes into auth, CSRF, flash messages and form errors. The most friction for the least benefit. |
| **B. API-first** (JSON + JWT, frontend separate or HTMX) | ~1–2 days | Plays to FastAPI's strengths. Drops Flask-Assets, WTForms and flash messages entirely. |
| **C. Hybrid** (API routers + a few Jinja pages) | ~2–3 days | Good if you want both, but you maintain two auth modes. |
| **D. Stay on Flask, modernize** (Flask 3, Flask-SQLAlchemy 3, `flask` CLI, Flask-Caching) | ~1 day | Worth comparing against. |

**Advice:** if new projects built from this template will mostly be APIs, take **B** and make it a FastAPI API template. If they'll mostly be server-rendered sites, **D** gets you further for less effort.

## 7. Gotchas when porting the tests

- **Redirect status:** `RedirectResponse` defaults to **307**, but `test_urls.py` expects **302**. Set 302 or 303 explicitly. After a POST, 303 is the correct choice.
- **Redirect following:** `TestClient` follows redirects by default. Tests that check for a redirect need `follow_redirects=False`.
- **Test isolation:** `test_user.py` calls `create_app()` in every test and depends on test order. The `@pytest.mark.incremental` marker it uses is never defined, so it does nothing. Replace this with a `conftest.py` that provides a transactional DB fixture.

## 8. Existing bugs to fix during the migration

1. **Cached home page shows the wrong login state.** In `controllers/main.py:21`, `@cache.cached` caches the whole rendered home page, including the navbar that depends on `current_user`. In prod (`CACHE_TYPE='simple'`), users see Login/Logout for whoever loaded the page first.
2. **Open redirect.** `redirect(request.args.get('next'))` doesn't validate the URL. Only allow relative paths.
3. **Broken login helpers.** `models/user.py` overrides `is_active` and `is_anonymous` as *methods*, but Flask-Login expects properties. A bound method is always truthy, so `current_user.is_anonymous` is True even for logged-in users. Drop these overrides; your own dependency replaces them.
4. **Secret key committed.** `SECRET_KEY = 'REPLACE ME'` is in the code. Load it from the environment with pydantic-settings.
5. **Missing file.** `base.html` loads `modernizr.min.js`, which doesn't exist, so every page gets a 404 for it.
6. **Database file committed.** `database/dev.db` is in git.

## Summary

- **The Flask version already needs rebuilding:** Python 2.7 and dead extensions mean the glue has to be redone on either framework. Models, templates, migrations and tests carry over.
- **Easy parts:** config → pydantic-settings, Blueprint → APIRouter, Alembic, the CLI, and replacing the static assets pipeline.
- **Hard parts:** Flask-Login and Flask-WTF/CSRF/flash. FastAPI has no first-party replacements, so you'd build or pick third-party ones.
- **Effort:** about 1–2 days API-first, 2–4 days for a like-for-like HTML port.
- **Recommendation:** go FastAPI API-first (sync SQLAlchemy 2.0, pydantic-settings, Alembic, Typer, uv + ruff) if the template is for APIs. For HTML sites, modernizing Flask is the better deal.
- **Either way:** fix the page cache, the open redirect and the committed secret key.
