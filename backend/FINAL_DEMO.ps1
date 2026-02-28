# FINAL STABLE DEMO - ONE CLEAN LOOP

Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  CAMPAIGNX - AUTONOMOUS OPTIMIZATION ENGINE" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# STEP 1: CREATE
Write-Host "[1/5] Creating campaign..." -ForegroundColor Yellow
$create = Invoke-RestMethod -Uri "http://127.0.0.1:8000/create-campaign" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"brief": "Launch Elite Card with 12% cashback. Premium members get 18%. Goal: maximize clicks for signups."}'

$cid = $create.campaign_id
Write-Host "  ✓ Campaign: $($cid.Substring(0,12))..." -ForegroundColor Green
Write-Host "  ✓ Product: $($create.parsed_brief.product_name)" -ForegroundColor White
Write-Host "  ✓ Variants: $($create.variants.Count)" -ForegroundColor White

# STEP 2: FETCH INITIAL METRICS
Write-Host "`n[2/5] Computing initial metrics..." -ForegroundColor Yellow
$metrics1 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/fetch-metrics/$cid" -Method POST

if ($metrics1.metrics_count -eq 0) {
    Write-Host "  ❌ FAILED: No metrics computed" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Metrics computed: $($metrics1.metrics_count)" -ForegroundColor Green

# Calculate average CTR
$avgCTR1 = ($metrics1.metrics | Measure-Object -Property click_rate -Average).Average
Write-Host "`n  VERSION 1 RESULTS:" -ForegroundColor Cyan
Write-Host "  Average CTR: $([math]::Round($avgCTR1 * 100, 2))%" -ForegroundColor White

# Show individual metrics
$metrics1.metrics | ForEach-Object {
    $o = [math]::Round($_.open_rate * 100, 1)
    $c = [math]::Round($_.click_rate * 100, 1)
    Write-Host "    Variant $($_.variant_id): Open=$o% CTR=$c%" -ForegroundColor Gray
}

# STEP 3: OPTIMIZE
Write-Host "`n[3/5] Running autonomous optimizer..." -ForegroundColor Yellow
$opt = Invoke-RestMethod -Uri "http://127.0.0.1:8000/optimize/$cid" -Method POST

if (-not $opt.optimized) {
    Write-Host "  ℹ No optimization: $($opt.reason)" -ForegroundColor Yellow
    Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  SYSTEM OPERATIONAL - Performance Already Good" -ForegroundColor Green
    Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan
    exit 0
}

Write-Host "  ✓ Optimization triggered!" -ForegroundColor Green
Write-Host "  Problem: $($opt.problem_type)" -ForegroundColor Yellow
Write-Host "  Actions: $($opt.actions -join ', ')" -ForegroundColor Yellow
Write-Host "  Original variant: $($opt.original_variant_id) (v$($opt.version.from))" -ForegroundColor Gray
Write-Host "  New variant: $($opt.new_variant_id) (v$($opt.version.to))" -ForegroundColor Gray

# STEP 4: FETCH V2 METRICS
Write-Host "`n[4/5] Computing optimized metrics..." -ForegroundColor Yellow
$metrics2 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/fetch-metrics/$cid" -Method POST

# Find the new variant's metrics
$newMetric = $metrics2.metrics | Where-Object { $_.variant_id -eq $opt.new_variant_id }

if ($newMetric) {
    $v2CTR = $newMetric.click_rate
    $v2Open = $newMetric.open_rate
    
    Write-Host "`n  VERSION 2 RESULTS:" -ForegroundColor Cyan
    Write-Host "  New variant CTR: $([math]::Round($v2CTR * 100, 2))%" -ForegroundColor White
    Write-Host "  New variant Open: $([math]::Round($v2Open * 100, 2))%" -ForegroundColor White
    
    # STEP 5: CALCULATE IMPROVEMENT
    Write-Host "`n[5/5] Computing improvement..." -ForegroundColor Yellow
    
    $originalCTR = $opt.original_metrics.click_rate
    $improvement = (($v2CTR - $originalCTR) / $originalCTR) * 100
    
    Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "║  VERSION 1 CTR: $([math]::Round($originalCTR * 100, 2))%".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║  VERSION 2 CTR: $([math]::Round($v2CTR * 100, 2))%".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "║  IMPROVEMENT: +$([math]::Round($improvement, 1))%".PadRight(41) + "║" -ForegroundColor Green
    Write-Host "║                                        ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════╝`n" -ForegroundColor Green
}

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✓ OPTIMIZATION COMPLETE" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "Campaign ID: $cid" -ForegroundColor Gray
Write-Host "View logs: http://127.0.0.1:8000/campaigns/$cid/logs`n" -ForegroundColor Gray
