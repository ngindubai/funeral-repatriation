# strip-costs-v2.ps1
# Fixed CRLF handling + extended patterns for remaining cost references

$contentDir = "C:\Users\garet\Desktop\funeral-repatriation\site\content"
$modified = 0

$allFiles = Get-ChildItem -Path $contentDir -Filter "*.md" -Recurse

foreach ($file in $allFiles) {
    $rawContent = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    # Split with CRLF-safe pattern so lines have no trailing \r
    $lines = $rawContent -split "\r?\n"
    $result = [System.Collections.Generic.List[string]]::new()

    $fmDashes = 0    # 0=before FM, 1=inside FM, 2+=body
    $skipping = $false
    $skipLevel = 0
    $anyChange = $false

    foreach ($line in $lines) {
        $orig = $line

        # ─── Track frontmatter boundaries (trim to handle CRLF remnants) ───
        if ($line.TrimEnd() -eq '---') {
            $fmDashes++
            $result.Add($line)
            continue
        }

        $inFM = ($fmDashes -eq 1)

        # ════════════════════════════════════════
        # FRONTMATTER
        # ════════════════════════════════════════
        if ($inFM) {

            # Remove direct_answer_points cost bullets (contains price figure)
            if (($line -match '^\s+- "(?:Total )?Costs?[\s:]' -or
                 $line -match '^\s+- "Cost[s]? range:' -or
                 $line -match '^\s+- "Cost:') -and
                ($line -match '£[\d,]|\bGBP')) {
                $anyChange = $true
                continue
            }

            # Strip cost sentence from direct_answer_intro
            if ($line -match '^direct_answer_intro:' -and ($line -match '£[\d,]|\bGBP')) {
                $line = $line `
                    -replace '\. [Cc]osts? (?:typically fall|range from|are typically|generally fall) (?:between |from )?(?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '.' `
                    -replace ' and costs? between (?:GBP |£)[\d,]+ and (?:GBP |£)[\d,]+[.,]?', '' `
                    -replace ' and cost between (?:GBP |£)[\d,]+ and (?:GBP |£)[\d,]+[.,]?', '' `
                    -replace ' and costs? (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+[.,]?', ''
            }

            # Strip cost clause from description field
            if ($line -match '^description:' -and ($line -match '£[\d,]|\bGBP')) {
                $line = $line `
                    -replace ' [Ee]xpert guidance from £[\d,]+\.?', '' `
                    -replace ' [Ee]xpert help from £[\d,]+\.?', '' `
                    -replace '\.? ?Costs? from £[\d,]+\.', '' `
                    -replace ' Costs? from £[\d,]+\.? ?', ' ' `
                    -replace ' and costs? £[\d,]+ to £[\d,]+', '' `
                    -replace ' and costs? between £[\d,]+ and £[\d,]+', '' `
                    -replace ' costs? £[\d,]+ to £[\d,]+', '' `
                    -replace ' and costs? (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+', '' `
                    -replace '  +', ' '   # collapse double spaces
                $line = $line -replace '\s+"$', '"'   # trim trailing space before closing quote
            }

            # Strip cost from short_answer (safety net)
            if ($line -match '^short_answer:' -and ($line -match '£[\d,]|\bGBP')) {
                $line = $line `
                    -replace ' (?:and )?costs? (?:between |from )?£[\d,]+ to £[\d,]+[.,]?', '' `
                    -replace ' (?:and )?costs? between £[\d,]+ and £[\d,]+[.,]?', '' `
                    -replace ' [Cc]osts? (?:are typically|range from|typically fall between|generally fall between) (?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '' `
                    -replace '\.? ?Costs? from £[\d,]+\.?', '' `
                    -replace ' [Cc]osts? (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+[.,]?', '' `
                    -replace ' [Cc]osts? between (?:GBP |£)[\d,]+ and (?:GBP |£)[\d,]+[.,]?', ''
            }

            if ($line -ne $orig) { $anyChange = $true }
            $result.Add($line)
            continue
        }

        # ════════════════════════════════════════
        # BODY CONTENT
        # ════════════════════════════════════════

        # ─── Detect cost section header → start skipping ────────────
        if (-not $skipping -and $line -match '^(#{1,4})\s') {
            $heading = $line -replace '^#{1,4}\s+', ''
            if ($heading -match '^(?i)(Costs?[\s:]|Cost and |Cost &|Routing and costs?)') {
                $skipping = $true
                $skipLevel = [regex]::Match($line, '^(#{1,6})').Value.Length
                $anyChange = $true
                continue
            }
        }

        # ─── Inside a skipped cost section ──────────────────────────
        if ($skipping) {
            if ($line -match '^(#{1,6})\s') {
                $hlevel = [regex]::Match($line, '^(#{1,6})').Value.Length
                if ($hlevel -le $skipLevel) {
                    $skipping = $false
                    # Fall through — output this new section header
                } else {
                    continue
                }
            } else {
                continue
            }
        }

        # ─── Clean remaining cost references in body ────────────────
        if ($line -match '£[\d,]|\bGBP\s*\d') {

            # Remove whole-line cost statements
            if ($line -match '^A typical repatriation from .+ costs?') { $anyChange = $true; continue }
            if ($line -match '^Repatriation from .+ costs? (?:between|from|typically)') { $anyChange = $true; continue }
            if ($line -match '^Costs? typically fall between') { $anyChange = $true; continue }
            if ($line -match '^Cases start at \*\*£') { $anyChange = $true; continue }
            if ($line -match '^Realistic cost range:') { $anyChange = $true; continue }
            if ($line -match '^Expect costs? between') { $anyChange = $true; continue }
            if ($line -match '^Expect to pay between £') { $anyChange = $true; continue }
            if ($line -match '^Typical total cost from') { $anyChange = $true; continue }
            if ($line -match '^The total (?:range|cost) for a .+ repatriation') { $anyChange = $true; continue }
            if ($line -match '^Costs? start at \*\*£') { $anyChange = $true; continue }
            if ($line -match '^\- \*\*Natural death') { $anyChange = $true; continue } # cost timeline bullets in guides
            if ($line -match '^\- \*\*INACIF process:') { $anyChange = $true; continue }
            if ($line -match '^\- \*\*Unnatural death:') { $anyChange = $true; continue }
            if ($line -match '^\- \*\*Remote area:') { $anyChange = $true; continue }
            if ($line -match '^\- (?:Natural|Unnatural|Remote) death .+\*\*.*£') { $anyChange = $true; continue }
            if ($line -match '^\*\*(?:Europe|Turkey|USA|Thailand|Latin|Africa|Australia).*:\*\* (?:£|GBP)') { $anyChange = $true; continue }

            # Strip inline cost sentence patterns from mixed lines
            $line = $line `
                -replace '\. [Cc]osts? (?:range|typically fall|are typically|generally fall) (?:from |between )?(?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '.' `
                -replace '\. [Cc]osts? (?:are typically|generally) (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+[.,]?', '.' `
                -replace ', costs? (?:from |between )?(?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '' `
                -replace ' These figures cover professional repatriation services but not UK funeral director fees on arrival\.?', '' `
                -replace ' \(typically £[\d,]+ to £[\d,]+\)', '' `
                -replace ' \(roughly £[\d,]+ to £[\d,]+\)', '' `
                -replace '\. Budget (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+ on top[^.]+\.', '.' `
                -replace ' Budget for translation costs[^.]+\.', '' `
                -replace ' Complex cases involving [^.]+ can exceed \*\*£[\d,]+\*\*[.,]?', '' `
                -replace ' Complex cases[^.]+ can (?:exceed|reach) \*\*£[\d,]+\*\*[^.]*\.', '' `
                -replace '\. Coverage limits vary\. Common limits are £[\d,]+-[\d,]+[^.]+\.', '.' `
                -replace ' Some policies cap at £[\d,]+ or £[\d,]+[^.]+\.', '' `
                -replace ' This significantly reduces costs? \(often £[\d,]+-[\d,]+ all-in[^)]+\)', '' `
                -replace ' The cost (?:ranges?|is) from £[\d,]+ to £[\d,]+[.,]?', '' `
                -replace '\.? The typical total cost depends[^.]+\. [^.]+£[\d,]+[^.]+\. [^.]+£[\d,]+[^.]+\.', '.' `
                -replace ' (?:roughly|typically) £[\d,]+ to £[\d,]+[.,]?', '' `
                -replace ' It is (?:one of the more|the most) (?:affordable|cost-effective)[^.]+\.', '.' `
                -replace ' (?:The )?(?:This|It) is (?:significantly|much) cheaper[^.]+\.', '.' `
                -replace ' This is significantly cheaper and less complicated\.[^.]*\.', '.' `
                -replace '\. (?:Travel|Adventure travel|Most standard UK travel|Check travel|Check expat) insurance[^.]+\.', '.'

            if ($line -ne $orig) { $anyChange = $true }

            # Skip if now empty
            if ($line -match '^\s*$') { continue }
        }

        $result.Add($line)
    }

    if ($anyChange) {
        $newContent = $result -join "`n"
        [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.Encoding]::UTF8)
        $modified++
        Write-Host "Modified: $($file.Directory.Name)\$($file.Name)"
    }
}

Write-Host "`nTotal files modified: $modified"
