@echo off
REM ============================================================================
REM  scheduled_run.cmd — one scheduled action that (1) publishes ready videos
REM  then (2) embeds the new IDs back into the site and deploys.
REM
REM  EDIT THE THREE VALUES BELOW ONCE, then register with install_schedule.ps1.
REM  (These are the only things I couldn't pre-fill — I don't have your paths.)
REM ============================================================================

REM --- (1) Your Google Drive Video Upload Queue folder (where READY_ folders land).
REM     Drive for desktop usually mounts as a drive letter, e.g. G:\My Drive\... (check yours):
set "QUEUE=G:\My Drive\West FW Living\Video Upload Queue"

REM --- (2) Your local clone of the SITE repo = camelweaver-stack/Anthropic-claude-code
REM     (this same repo holds the site: rent-report\*.html, tv.html, netlify.toml). Point this at
REM     wherever you cloned it on this machine:
set "SITE_REPO=%USERPROFILE%\code\Anthropic-claude-code"

REM --- (3) Site URL + IndexNow key (pre-filled from the key file in the repo root; leave key blank to skip):
set "SITE_URL=https://westfwliving.com"
set "INDEXNOW_KEY=f61db218770282944b56755e36b90509"

REM --- Cadence: which weekday(s) may publish (keeps you to 2-3/week):
set "DAYS=mon,wed,fri"
REM ============================================================================

cd /d "%~dp0"

echo [%date% %time%] publish_queue starting
node publish_queue.mjs --queue "%QUEUE%" --days %DAYS%

echo [%date% %time%] process_pending_embed starting
if "%INDEXNOW_KEY%"=="" (
  node process_pending_embed.mjs --queue "%QUEUE%" --repo "%SITE_REPO%" --site-url "%SITE_URL%"
) else (
  node process_pending_embed.mjs --queue "%QUEUE%" --repo "%SITE_REPO%" --site-url "%SITE_URL%" --indexnow-key "%INDEXNOW_KEY%"
)

echo [%date% %time%] done
