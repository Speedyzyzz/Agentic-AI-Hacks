# ULTRA-SIMPLE: ONE ENDPOINT DEMO

Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ONE-CLICK OPTIMIZATION DEMO" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# Step 1: Create campaign
Write-Host "Creating campaign..." -ForegroundColor Yellow
$create = Invoke-RestMethod -Uri "http://127.0.0.1:8000/create-campaign" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"brief": "Launch Premium Savings with 8.5% interest. Target high-value customers. Goal: maximize clicks."}'

$cid = $create.campaign_id
Write-Host "✓ Campaign created: $($cid.Substring(0,12))...`n" -ForegroundColor Green

# Step 2: Run FULL CYCLE with ONE endpoint
Write-Host "Running full optimization cycle..." -ForegroundColor Yellow
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/run-full-cycle/$cid" -Method POST

if ($result.success -and $result.optimized) {
    Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ONE-ENDPOINT OPTIMIZATION SUCCESS     ║" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "║  Initial CTR: $([math]::Round($result.improvement.ctr_before * 100, 2))%".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║  Optimized CTR: $([math]::Round($result.improvement.ctr_after * 100, 2))%".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "║  IMPROVEMENT: +$($result.improvement.improvement_percentage)%".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "║  Problem: $($result.optimization.problem_type)".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║  Fixed: $($result.optimization.actions -join ', ')".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
    
    Write-Host "`nView complete logs: http://127.0.0.1:8000$($result.logs_url)" -ForegroundColor Gray
} else {
    Write-Host "ℹ $($result.reason)" -ForegroundColor Yellow
}

Write-Host ""
