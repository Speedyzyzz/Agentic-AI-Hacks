# CAMPAIGNX DEMO WITH HUMAN-IN-THE-LOOP APPROVAL

Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  CAMPAIGNX - WITH APPROVAL WORKFLOW" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# STEP 1: CREATE CAMPAIGN
Write-Host "[1/3] Creating campaign..." -ForegroundColor Yellow
$create = Invoke-RestMethod -Uri "http://127.0.0.1:8000/create-campaign" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"brief": "Launch Premium Savings Account with 8.5% APR. Target affluent customers. Goal: maximize signups."}'

$cid = $create.campaign_id
Write-Host "  ✓ Campaign created: $($cid.Substring(0,12))..." -ForegroundColor Green
Write-Host "  ✓ Status: $($create.status)" -ForegroundColor White
Write-Host "  ✓ Variants: $($create.variants.Count)" -ForegroundColor White

# STEP 2: SHOW APPROVAL REQUIRED
Write-Host "`n[2/3] ⚠️  APPROVAL REQUIRED" -ForegroundColor Yellow
Write-Host "══════════════════════════════════════════════════`n" -ForegroundColor Yellow

Write-Host "  🌐 Opening approval page in browser..." -ForegroundColor Cyan
Write-Host "  URL: $($create.approval_url)`n" -ForegroundColor Gray

# Open approval page in default browser
Start-Process $create.approval_url

Write-Host "  📋 Review campaign content:" -ForegroundColor White
Write-Host "     - Product: $($create.parsed_brief.product_name)" -ForegroundColor Gray
Write-Host "     - Objective: $($create.parsed_brief.objective)" -ForegroundColor Gray
Write-Host "     - Segments: $($create.plan.segments.Count)" -ForegroundColor Gray
Write-Host "     - Send Time: $($create.plan.send_time)" -ForegroundColor Gray

Write-Host "`n  ⏸  Waiting for approval..." -ForegroundColor Yellow
Write-Host "  (Click 'Approve' in the browser to continue)`n" -ForegroundColor Gray

# Wait for approval
$approved = $false
$timeout = 180  # 3 minutes
$elapsed = 0

while (-not $approved -and $elapsed -lt $timeout) {
    Start-Sleep -Seconds 2
    $elapsed += 2
    
    # Check campaign status
    $campaign = Invoke-RestMethod -Uri "http://127.0.0.1:8000/campaigns/$cid" -Method GET
    
    if ($campaign.status -eq "approved") {
        $approved = $true
        Write-Host "  ✓ Campaign APPROVED!" -ForegroundColor Green
        break
    }
    
    if ($campaign.status -eq "rejected") {
        Write-Host "  ✗ Campaign REJECTED" -ForegroundColor Red
        exit 1
    }
}

if (-not $approved) {
    Write-Host "  ⏱  Timeout waiting for approval" -ForegroundColor Red
    exit 1
}

# STEP 3: RUN OPTIMIZATION LOOP (POST-APPROVAL)
Write-Host "`n[3/3] Running optimization loop..." -ForegroundColor Yellow

# Fetch metrics
Write-Host "  Computing initial metrics..." -ForegroundColor Gray
$metrics1 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/fetch-metrics/$cid" -Method POST

$avgCTR1 = ($metrics1.metrics | Measure-Object -Property click_rate -Average).Average
Write-Host "  ✓ Initial CTR: $([math]::Round($avgCTR1 * 100, 2))%" -ForegroundColor White

# Optimize
Write-Host "`n  Running optimizer..." -ForegroundColor Gray
$opt = Invoke-RestMethod -Uri "http://127.0.0.1:8000/optimize/$cid" -Method POST

if (-not $opt.optimized) {
    Write-Host "  ℹ No optimization needed: $($opt.reason)" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Optimization complete!" -ForegroundColor Green
    Write-Host "  Problem: $($opt.problem_type)" -ForegroundColor Gray
    Write-Host "  Actions: $($opt.actions -join ', ')" -ForegroundColor Gray
    
    # Compute new metrics
    Write-Host "`n  Computing optimized metrics..." -ForegroundColor Gray
    $metrics2 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/fetch-metrics/$cid" -Method POST
    
    # Find new variant metrics
    $newMetric = $metrics2.metrics | Where-Object { $_.variant_id -eq $opt.new_variant_id } | Select-Object -First 1
    
    if ($newMetric) {
        $improvement = (($newMetric.click_rate - $opt.original_metrics.click_rate) / $opt.original_metrics.click_rate * 100)
        
        Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║  OPTIMIZATION SUCCESS                  ║" -ForegroundColor Green
        Write-Host "║                                        ║" -ForegroundColor Green
        Write-Host "║  Before: $([math]::Round($opt.original_metrics.click_rate * 100, 2))%".PadRight(41) + "║" -ForegroundColor Green
        Write-Host "║  After:  $([math]::Round($newMetric.click_rate * 100, 2))%".PadRight(41) + "║" -ForegroundColor Green
        Write-Host "║                                        ║" -ForegroundColor Green
        Write-Host "║  IMPROVEMENT: +$([math]::Round($improvement, 1))%".PadRight(41) + "║" -ForegroundColor Green
        Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
    }
}

Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✓ DEMO COMPLETE" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "View logs: http://127.0.0.1:8000/campaigns/$cid/logs" -ForegroundColor Gray
Write-Host ""
