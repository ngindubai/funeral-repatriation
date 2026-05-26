# strip-costs.ps1
# Removes all cost figures (£X, GBP X) from site content markdown files
# Strategy:
#   1. Remove entire dedicated cost sections (## Costs, ### Cost and Complexity, etc.)
#   2. Clean frontmatter: description, short_answer, direct_answer_intro, direct_answer_points
#   3. Remove standalone cost lines remaining in body content

$contentDir = "C:\Users\garet\Desktop\funeral-repatriation\site\content"
$modified = 0

$allFiles = Get-ChildItem -Path $contentDir -Filter "*.md" -Recurse

foreach ($file in $allFiles) {
    $rawContent = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    $lines = $rawContent -split "`n"
    $result = [System.Collections.Generic.List[string]]::new()

    $fmDashes = 0    # 0=before FM, 1=inside FM, 2+=body
    $skipping = $false
    $skipLevel = 0
    $anyChange = $false

    foreach ($line in $lines) {
        $orig = $line

        # ─── Track frontmatter boundaries ───────────────────────────
        if ($line -ceq '---' -or $line -ceq '--- ') {
            $fmDashes++
            $result.Add($line)
            continue
        }

        $inFM = ($fmDashes -eq 1)

        # ════════════════════════════════════════
        # FRONTMATTER
        # ════════════════════════════════════════
        if ($inFM) {

            # Remove direct_answer_points bullets that mention price figures
            if (($line -match '^\s+- "(?:Total )?Costs?[\s:]' -or $line -match '^\s+- "Cost range:') -and
                ($line -match '£[\d,]|\bGBP\s*\d')) {
                $anyChange = $true
                continue
            }

            # Strip cost sentence from direct_answer_intro
            if ($line -match '^direct_answer_intro:' -and ($line -match '£[\d,]|\bGBP\s*\d')) {
                $line = $line `
                    -replace '\. [Cc]osts? (?:typically fall|range from|are typically|generally fall) (?:between |from )?(?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '.' `
                    -replace ' and costs? between (?:GBP |£)[\d,]+ and (?:GBP |£)[\d,]+[.,]?', '' `
                    -replace ' and cost between (?:GBP |£)[\d,]+ and (?:GBP |£)[\d,]+[.,]?', ''
            }

            # Strip cost clause from description field
            if ($line -match '^description:' -and ($line -match '£[\d,]|\bGBP\s*\d')) {
                $line = $line `
                    -replace ' [Ee]xpert guidance from £[\d,]+\.', '.' `
                    -replace ' [Ee]xpert help from £[\d,]+\.', '.' `
                    -replace '\.? ?Costs? from £[\d,]+\.', '' `
                    -replace ' Costs? from £[\d,]+\.? ', ' ' `
                    -replace ' and costs? £[\d,]+ to £[\d,]+', '' `
                    -replace ' and costs? between £[\d,]+ and £[\d,]+', '' `
                    -replace ' costs? £[\d,]+ to £[\d,]+', '' `
                    -replace ' and costs? (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+', ''
                # Clean double spaces or trailing punctuation
                $line = $line -replace '  +', ' '
                $line = $line -replace '\."$', '."'
            }

            # Strip cost from short_answer (safety net)
            if ($line -match '^short_answer:' -and ($line -match '£[\d,]|\bGBP\s*\d')) {
                $line = $line `
                    -replace ' (?:and )?costs? (?:between |from )?£[\d,]+ to £[\d,]+[.,]?', '' `
                    -replace ' (?:and )?costs? between £[\d,]+ and £[\d,]+[.,]?', '' `
                    -replace ' [Cc]osts? (?:are typically|range from|typically fall between|generally fall between) (?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '' `
                    -replace '\.? ?Costs? from £[\d,]+\.?', '' `
                    -replace ' [Cc]osts? (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+[.,]?', ''
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
                    # Fall through — output this new section header normally
                } else {
                    continue  # Sub-header within the cost section
                }
            } else {
                continue  # Body line within cost section
            }
        }

        # ─── Clean any remaining cost references in body ────────────
        if ($line -match '£[\d,]|\bGBP\s*\d') {

            # Remove whole lines that are purely cost statements
            if ($line -match '^A typical repatriation from .+ costs?') {
                $anyChange = $true; continue
            }
            if ($line -match '^Repatriation from .+ costs? (?:between|from|typically)') {
                $anyChange = $true; continue
            }
            if ($line -match '^Costs? typically fall between') {
                $anyChange = $true; continue
            }
            if ($line -match '^Cases start at \*\*£[\d,]+\*\*') {
                $anyChange = $true; continue
            }
            if ($line -match '^Realistic cost range:') {
                $anyChange = $true; continue
            }
            if ($line -match '^Expect costs between') {
                $anyChange = $true; continue
            }

            # For mixed lines, strip the cost sentence/clause
            $line = $line `
                -replace '\. [Cc]osts? (?:range|typically fall|are typically|generally fall) (?:from |between )?(?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '.' `
                -replace '\. [Cc]osts? (?:are typically|generally) (?:GBP |£)[\d,]+ to (?:GBP |£)[\d,]+[.,]?', '.' `
                -replace ', costs? (?:from |between )?(?:GBP |£)[\d,]+ (?:to|and) (?:GBP |£)[\d,]+[.,]?', '' `
                -replace ' These figures cover professional repatriation services but not UK funeral director fees on arrival\.?', '' `
                -replace ' It is (?:one of the more|the most) (?:affordable|cost-effective)[^.]+\.', '.' `
                -replace '\. (?:Travel|Adventure travel|Most standard UK travel|Check travel|Check expat) insurance[^.]+\.', '.' `
                -replace ' Complex cases involving [^.]+ can exceed \*\*£[\d,]+\*\*[.,]?', '' `
                -replace ' Complex cases[^.]+ can (?:exceed|reach) \*\*£[\d,]+\*\*[^.]*\.', ''

            if ($line -ne $orig) { $anyChange = $true }

            # If line is now empty/whitespace after cleanup, skip it
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
