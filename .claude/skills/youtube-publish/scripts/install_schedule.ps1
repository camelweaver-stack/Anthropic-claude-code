<#
  install_schedule.ps1 — register the West FW Living auto-publish task.

  Run once in PowerShell (normal user is fine). It schedules scheduled_run.cmd to fire on the days/time
  below, AND to run as soon as possible after a missed start — so if the PC was off at that time, it runs
  the next time you turn it on. That's what makes scheduled publishing work without an always-on machine.

  Prereq: edit the three values at the top of scheduled_run.cmd first, and run setup_auth.mjs once.

  Change the time/days here if you like, then:  powershell -ExecutionPolicy Bypass -File install_schedule.ps1
#>

$TaskName = "West FW Living Auto-Publish"
$Time     = "9:00AM"
$Days     = "Monday","Wednesday","Friday"      # keep in sync with DAYS in scheduled_run.cmd
$Cmd      = Join-Path $PSScriptRoot "scheduled_run.cmd"

if (-not (Test-Path $Cmd)) { Write-Error "scheduled_run.cmd not found next to this script"; exit 1 }

$action   = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$Cmd`"" -WorkingDirectory $PSScriptRoot
$trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Days -At $Time
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Force |
  Out-Null

Write-Host "Registered '$TaskName' for $($Days -join ', ') at $Time."
Write-Host "It will also run on next startup if a scheduled time was missed (StartWhenAvailable)."
Write-Host "Test it now with:  Start-ScheduledTask -TaskName `"$TaskName`""
