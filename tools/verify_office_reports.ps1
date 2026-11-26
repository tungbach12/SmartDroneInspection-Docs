param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,
    [switch]$ExportPdf
)

$ErrorActionPreference = 'Stop'
$directory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$manifestPath = Join-Path $directory 'manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$previewDirectory = Join-Path $directory 'pdf-previews'
if ($ExportPdf) {
    if (Test-Path -LiteralPath $previewDirectory) {
        throw 'Use a fresh preview directory; existing previews will not be overwritten.'
    }
    New-Item -Path $previewDirectory -ItemType Directory | Out-Null
}
$results = @()
$word = $null
$excel = $null

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $word.Options.UpdateLinksAtOpen = $false

    foreach ($artifact in $manifest.artifacts) {
        if ($artifact.status -ne 'generated') { continue }
        $path = (Resolve-Path -LiteralPath $artifact.output).Path
        $pdfPath = Join-Path $previewDirectory ([IO.Path]::GetFileNameWithoutExtension($path) + '.pdf')
        $before = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
        $document = $null
        $workbook = $null
        try {
            if ([IO.Path]::GetExtension($path) -eq '.docx') {
                # ConfirmConversions=false, ReadOnly=true, AddToRecentFiles=false.
                Write-Output ($artifact.report + ': opening in Word')
                $document = $word.Documents.Open($path, $false, $true, $false)
                $document.Repaginate()
                Write-Output ($artifact.report + ': updating table of contents')
                for ($tocIndex = 1; $tocIndex -le $document.TablesOfContents.Count; $tocIndex++) {
                    $toc = $document.TablesOfContents.Item($tocIndex)
                    $toc.Update()
                    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($toc)
                }
                Write-Output ($artifact.report + ': reading page count')
                $document.Repaginate()
                $pages = $document.ComputeStatistics(2)
                if ($ExportPdf) {
                    Write-Output ($artifact.report + ': exporting PDF')
                    $document.ExportAsFixedFormat($pdfPath, 17)
                }
                $results += [pscustomobject]@{
                    report = $artifact.report
                    opened = $true
                    pages = $pages
                    pdf = $(if ($ExportPdf) { $pdfPath } else { $null })
                    tocCount = $document.TablesOfContents.Count
                }
                Write-Output ($artifact.report + ': Word opened; ' + $pages + ' pages; PDF requested=' + [bool]$ExportPdf)
            }
            elseif ([IO.Path]::GetExtension($path) -eq '.xlsx') {
                # Create Excel only when needed; a long Word pass can leave an
                # idle Excel instance busy with activation/background work.
                if (-not $excel) {
                    $excel = New-Object -ComObject Excel.Application
                    $excel.Visible = $false
                    $excel.DisplayAlerts = $false
                    $excel.AskToUpdateLinks = $false
                    $excel.AutomationSecurity = 3
                }
                Write-Output ($artifact.report + ': opening in Excel')
                # UpdateLinks=0, ReadOnly=true. Do not fetch template external links.
                $workbook = $excel.Workbooks.Open($path, 0, $true)
                $excel.CalculateFullRebuild()
                $sheetNames = @()
                foreach ($sheet in $workbook.Worksheets) {
                    $sheetNames += $sheet.Name
                    if ($ExportPdf) {
                        $sheet.PageSetup.PrintArea = $sheet.UsedRange.Address()
                        $sheet.PageSetup.Zoom = $false
                        $sheet.PageSetup.FitToPagesWide = 1
                        $sheet.PageSetup.FitToPagesTall = $false
                    }
                }
                $result = [ordered]@{
                    report = $artifact.report
                    opened = $true
                    sheets = $sheetNames
                    pdf = $(if ($ExportPdf) { $pdfPath } else { $null })
                }
                if ($artifact.report -eq 'report5') {
                    $featureSheets = @(1..24 | ForEach-Object { "Feature $_" })
                    $missingFeatureSheets = @($featureSheets | Where-Object { $_ -notin $sheetNames })
                    if ($missingFeatureSheets.Count -gt 0) {
                        throw ('Missing Report 5 feature sheets: ' + ($missingFeatureSheets -join ', '))
                    }
                    $statistics = $workbook.Worksheets.Item('Test Statistics')
                    $feature = $workbook.Worksheets.Item('Feature 3')
                    # Totals are read from the Sub total row and cross-checked
                    # against the per-sheet sum rather than against literals, so
                    # the workbook can grow without the verifier going stale.
                    $subtotalRow = 11 + $featureSheets.Count
                    $result['totalCases'] = [int]$statistics.Range("H$subtotalRow").Value2
                    $result['passed'] = [int]$statistics.Range("D$subtotalRow").Value2
                    $result['coverage'] = $statistics.Range("E$($subtotalRow + 5)").Value2
                    $result['successfulCoverage'] = $statistics.Range("E$($subtotalRow + 6)").Value2
                    $result['round1Passed'] = $result['passed']
                    $result['round2Pending'] = 0
                    $result['round3Pending'] = 0
                    $sheetCases = 0
                    foreach ($sheetName in $featureSheets) {
                        $featureRound = $workbook.Worksheets.Item($sheetName)
                        $result['round2Pending'] += $featureRound.Range('D7').Value2
                        $result['round3Pending'] += $featureRound.Range('D8').Value2
                        $sheetCases += $featureRound.Range('B4').Value2
                    }
                    $result['date'] = $feature.Range('G12').Text
                    $result['tester'] = $feature.Range('H12').Text
                    $outcomeTotal = 0
                    foreach ($column in @('D', 'E', 'F', 'G')) {
                        $outcomeTotal += [int]$statistics.Range("$column$subtotalRow").Value2
                    }
                    if ($sheetCases -ne $result.totalCases) {
                        throw ('Report 5 feature sheet case count (' + $sheetCases +
                            ') differs from the statistics total (' + $result.totalCases + ')')
                    }
                    if ($outcomeTotal -ne $result.totalCases) {
                        throw ('Report 5 Sub total outcomes (' + $outcomeTotal +
                            ') do not equal its case total (' + $result.totalCases + ')')
                    }
                    if ($result.passed -gt $result.totalCases) {
                        throw 'Report 5 passed count exceeds its case total.'
                    }
                }
                if ($ExportPdf) { $workbook.ExportAsFixedFormat(0, $pdfPath) }
                $results += [pscustomobject]$result
                Write-Output ($artifact.report + ': Excel opened/recalculated; PDF requested=' + [bool]$ExportPdf)
            }
        }
        finally {
            if ($document) {
                $document.Close(0)
                [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
            }
            if ($workbook) {
                $workbook.Close($false)
                [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($workbook)
            }
            if ($excel) {
                try { $excel.Quit() } catch { Write-Warning ('Excel cleanup: ' + $_.Exception.Message) }
                [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel)
                $excel = $null
            }
        }
        $after = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
        if ($before -ne $after) { throw ('Office modified the generated package: ' + $path) }
    }
}
finally {
    if ($word) {
        try { $word.Quit() } catch { Write-Warning ('Word cleanup: ' + $_.Exception.Message) }
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
    }
    if ($excel) {
        try { $excel.Quit() } catch { Write-Warning ('Excel cleanup: ' + $_.Exception.Message) }
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel)
    }
}

$results | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $directory 'office-verification.json') -Encoding UTF8
Write-Output ('Verified artifacts: ' + $results.Count)
