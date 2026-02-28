# EDGE CASE TESTING FOR LIVE DEMO ADAPTABILITY

Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  EDGE CASE TESTING - LIVE DEMO ADAPTABILITY" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$testCases = @(
    @{
        Name = "TEST 1: Open Rate Objective (not click)"
        Brief = "Launch Premium Credit Card for doctors. Target: medical professionals. Goal: maximize open rate."
    },
    @{
        Name = "TEST 2: Conversion Objective"
        Brief = "Promote Business Loan for startup founders age 25-35. Focus: conversions."
    },
    @{
        Name = "TEST 3: Multiple Special Segments"
        Brief = "Launch Fixed Deposit with 7.5% interest. Female senior citizens get 8%. Goal: maximize signups."
    },
    @{
        Name = "TEST 4: Unusual Product Name"
        Brief = "XtraSave SuperMax Account with crypto features. Young professionals target. Goal: clicks."
    }
)

$passed = 0
$failed = 0

foreach ($test in $testCases) {
    Write-Host "`n$($test.Name)" -ForegroundColor Yellow
    Write-Host "Brief: $($test.Brief)" -ForegroundColor Gray
    Write-Host "Testing..." -ForegroundColor Gray
    
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/create-campaign" `
            -Method POST `
            -ContentType "application/json" `
            -Body "{`"brief`": `"$($test.Brief)`"}" `
            -ErrorAction Stop
        
        if ($response.success) {
            Write-Host "✓ PASSED - Campaign created" -ForegroundColor Green
            Write-Host "  Product: $($response.parsed_brief.product_name)" -ForegroundColor Gray
            Write-Host "  Objective: $($response.parsed_brief.objective)" -ForegroundColor Gray
            Write-Host "  Variants: $($response.variants.Count)" -ForegroundColor Gray
            $passed++
        } else {
            Write-Host "✗ FAILED - $($response.error)" -ForegroundColor Red
            $failed++
        }
    }
    catch {
        Write-Host "✗ FAILED - Exception: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
    
    Start-Sleep -Seconds 1
}

Write-Host "`n════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  TEST RESULTS" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PASSED: $passed / $($testCases.Count)" -ForegroundColor Green
Write-Host "  FAILED: $failed / $($testCases.Count)" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
Write-Host "════════════════════════════════════════════════════`n" -ForegroundColor Cyan

if ($failed -eq 0) {
    Write-Host "✅ ALL EDGE CASES PASSED - SYSTEM READY FOR LIVE DEMO" -ForegroundColor Green
} else {
    Write-Host "⚠️  SOME EDGE CASES FAILED - REVIEW FAILURES ABOVE" -ForegroundColor Yellow
}
