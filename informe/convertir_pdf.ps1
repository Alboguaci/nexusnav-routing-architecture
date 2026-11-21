param(
    [string]$Docx  = (Join-Path $PSScriptRoot "Informe_Actividad6_Navegando_Mareas.docx"),
    [string]$Tmp   = (Join-Path $PSScriptRoot "_export_tmp.pdf"),
    [string]$Final = (Join-Path $PSScriptRoot "Informe_Actividad6_Navegando_Mareas.pdf")
)

$ErrorActionPreference = "Stop"
$log = Join-Path $PSScriptRoot "convertir_pdf.log"
function Log($m) { Add-Content -Path $log -Value ("{0:HH:mm:ss} {1}" -f (Get-Date), $m) -Encoding UTF8 }
Set-Content -Path $log -Value "" -Encoding UTF8

Log "inicio $Docx"
if (-not (Test-Path $Docx)) { throw "no existe el docx: $Docx" }
if (Test-Path $Tmp) { Remove-Item $Tmp -Force }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.AutomationSecurity = 3
Log "word listo"

try {
    $doc = $word.Documents.Open($Docx, $false, $false, $false)
    Log "abierto"
    Start-Sleep -Seconds 2

    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    Log "indice"
    Start-Sleep -Seconds 1

    $doc.Repaginate()
    Log "repaginado"

    # Guardar cambios en el propio DOCX para que el TOC quede actualizado permanentemente
    $doc.Save()
    Log "docx guardado con toc actualizado"

    # Exportar como PDF (formato 17)
    $doc.SaveAs2($Tmp, 17)
    Log "guardado pdf"

    $pages = $doc.ComputeStatistics(2)
    $doc.Close($false)
    Log "fin paginas=$pages"

    Move-Item $Tmp $Final -Force
    Write-Output "PDF=$Final"
    Write-Output "PAGES=$pages"
}
finally {
    $word.Quit()
}
