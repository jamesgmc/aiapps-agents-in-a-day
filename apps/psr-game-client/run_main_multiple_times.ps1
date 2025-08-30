# run_main_multiple_times.ps1
# This PowerShell script runs main.py 4 times in sequence


# Run 4 instances of main.py in parallel (do not wait for each to finish)
for ($i = 1; $i -le 3; $i++) {
    Write-Host "Starting Run #$i in background"
    Start-Process python -ArgumentList 'main.py', 'auto', "bot$i"
    Start-Sleep -Seconds 3
}
