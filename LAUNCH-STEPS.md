# Hrid Digital Group website: how to put it live

The website is a set of plain pages kept on GitHub (free) and hosted on Netlify (free). Your domain stays with GoDaddy; you only change two DNS records there.

How changes work later: you ask Claude in this project, Claude edits the pages and pushes them to GitHub, and Netlify updates the live site within a minute or two. You never have to touch code.

## Step 1: GitHub (one time, about 5 minutes)

1. Create a free account at https://github.com/signup if you don't have one.
2. Connect it to Claude: https://claude.ai/connect-github
3. Create an empty repository: https://github.com/new
   - Name: `hrid-website`
   - Private is fine
   - Don't add a README
4. Tell Claude in the thread "repo created". Claude uploads the website to it.

## Step 2: Netlify hosting (one time, about 5 minutes)

1. Sign up at https://app.netlify.com/signup and choose **Sign up with GitHub**.
2. Click **Add new site → Import an existing project → GitHub**, then pick `hrid-website`.
3. Leave the build settings as they are (the `netlify.toml` file already sets them) and click **Deploy**.
4. Netlify gives you a temporary address like `something.netlify.app`. Open it to check the site.
5. In Netlify, go to **Site configuration → Forms** and turn form detection on. Then go to **Forms → Form notifications** and add an email notification to info@hriddigitalgroup.com, so enquiries from the Contact, Consultation and Free Audit forms reach your inbox.

## Step 3: Connect hriddigitalgroup.com (in Netlify, then GoDaddy)

1. In Netlify: **Domain management → Add a domain** → type `hriddigitalgroup.com` → confirm you own it. Choose to keep DNS at your current provider (GoDaddy).
2. In GoDaddy: **My Products → hriddigitalgroup.com → DNS → Manage DNS**.
3. Change these records:

| Type  | Name | Value                         | What to do |
|-------|------|-------------------------------|-----------|
| A     | @    | 75.2.60.5                     | Edit the existing @ A record (often "Parked") to this value. Delete any other @ A records. |
| CNAME | www  | your-site-name.netlify.app    | Edit the existing www record to your Netlify address from Step 2. |

   Netlify shows the exact values for your site on the domain screen. If they differ from the table, use Netlify's.
4. **Don't delete MX records** if you use email at info@hriddigitalgroup.com. They control your email, not your website.
5. Wait between a few minutes and a few hours. Netlify then adds the free HTTPS certificate automatically.

## Before launch: things only you can provide

- Real client reviews (name, company, one or two sentences) for the Testimonials page and home page
- Real case studies with numbers, or permission to keep them anonymous
- Your prices, or confirm you want "Custom quote"
- Founder name, short bio and photo for the About page
- Minimum contract terms for the Pricing FAQ
- Optional: Google Analytics / Tag Manager ID so the site tracks its own visitors

When those are in, Claude removes the "Draft" bar and the "Sample" tags.

## For Claude: how the site is built

- Page content: `src/pages/*.html` (settings in the first comment lines)
- Shared header, footer, contact details and nav: `build.py` (`SITE`, `NAV`, `SHOW_DRAFT_BAR`)
- Styles and brand colours: `site/assets/style.css` (tokens at the top)
- Build: `python3 build.py` writes the finished site to `site/`, which Netlify serves. `python3 build.py --preview` writes the copy used for the Claude preview link.
- Forms use Netlify Forms (`data-netlify="true"`); `site/assets/main.js` submits them.
