# Sports Money DNA Form

A custom, Ball Without Boundaries-branded questionnaire: stadium background, scoreboard progress bar, jersey-numbered questions and a "trading card" result. It's a single HTML file that runs anywhere.

- **Live file:** `form/sports-money-dna.html` (logos are built in)
- **Source:** `form/src/money-dna.html`. Edit this, then run `python3 form/build.py`

## Go-live checklist
1. **Save responses to Google Sheets:** follow the steps at the top of `form/apps-script.gs`, then paste the web-app URL into `SUBMIT_URL` in `form/src/money-dna.html`.
2. **Set the join link:** replace `JOIN_URL` with your Circle invite link.
3. **Rebuild:** `python3 form/build.py`
4. **Host it:** upload `sports-money-dna.html` to your website (e.g. ballwithoutboundaries.com/dna), or any static host (Netlify, Vercel, GitHub Pages).
5. **Embed in Circle:** add an embed or link in a Circle space or post pointing to the hosted URL.

## What's collected
Part A (12 questions, everyone), an optional Deep Dive (10 questions), the DNA type, a timestamp, and an optional name and email with founder or follow-up interest. Multi-select answers are stored as `a | b | c`.
