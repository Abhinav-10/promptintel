# PromptIntel

PromptIntel is a Django app to store prompts, track their effectiveness, and compare results across tools like ChatGPT, Claude, Gemini, and manual workflows.

## What This Project Does

- Save prompts with category, tags, source, and notes.
- Track outcomes with a flexible impact metric/value model.
- Rank prompts by computed score.
- View analytics on dashboard and leaderboard pages.
- Share prompts publicly through the Explore page.

## Core Features

- Authentication: sign up, login, logout.
- Prompt CRUD: create, edit, delete, and browse your prompt library.
- Sorting: best score, newest, highest rated, most reused, highest outcome.
- Analytics:
  - Summary cards (total prompts, avg rating, avg score, top category).
  - Top-performing prompt tables.
  - Leaderboard rankings.
- Public sharing toggle (`is_public`) for community discovery.

## Tech Stack

- Python + Django 4.2
- SQLite (default database)
- Server-rendered Django templates

## Project Structure

```
apps/
  analytics/   # dashboard + leaderboard selectors/views
  prompts/     # prompt models, forms, services, views
  users/       # custom user model + signup
  core/        # shared base models (UUID/timestamps)
config/        # settings + URL config
templates/     # HTML templates for all pages
```

## Setup (Local)

1. Create and activate a virtual environment.
2. Install Django.
3. Run migrations.
4. Start the server.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "Django>=4.2,<5"
python manage.py migrate
python manage.py runserver
```

App URLs:

- Dashboard: `http://127.0.0.1:8000/`
- Prompts: `http://127.0.0.1:8000/prompts/`
- Leaderboard: `http://127.0.0.1:8000/leaderboard/`
- Explore (public prompts): `http://127.0.0.1:8000/prompts/explore/`

## Prompt Scoring

Prompt score is calculated in `apps/analytics/services.py` using:

- Rating component (0-40)
- Reuse component (0-20 cap)
- Outcome component (0-40 cap after normalization)

This gives a single score used in sort order, dashboard rankings, and leaderboard.

## New Prompt Form Behavior

### Prompt Experience (instead of full raw response)

- The old `response_text` field is presented as **Prompt Experience**.
- It is optional and intended for summary notes when full model output is too long.
- Recommended usage:
  - What worked well
  - What failed or needed edits
  - A short key snippet (optional)

### Flexible Outcome Tracking

Outcome fields are now designed for broader use cases (not only social media):

- Time saved
- Tasks completed
- Quality score
- Accuracy
- User satisfaction
- Cost saved
- Revenue impact
- Views/Reach
- Action clicks
- Lead generation
- Custom metric

`Impact Metric` and `Impact Value` are optional. If no metric is selected, value defaults to `0`.

## Main Data Model Notes

Model: `apps.prompts.models.Prompt`

- `source`: where prompt was used (`chatgpt`, `claude`, `gemini`, etc.)
- `prompt_text`: original prompt text
- `response_text`: stored as prompt experience summary in UI
- `rating`: 0-5 effectiveness rating
- `reuse_count`: number of times reused
- `outcome_metric` + `outcome_value`: optional KPI pair
- `score`: computed effectiveness score
- `is_public`: whether visible on Explore page

## Quality Checks

Run this before pushing:

```bash
python manage.py check
```

## Future Improvements

- Add automated tests for forms/selectors/services.
- Add CSV export for analytics.
- Add richer filtering by date ranges and sources.
- Add chart visualizations for score and impact trends.
