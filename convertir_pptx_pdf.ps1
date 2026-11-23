param(
    [string]$Pptx = (Join-Path $PSScriptRoot "NexusNav_Presentacion_Arquitectura.pptx"),
    [string]$Pdf  = (Join-Path $PSScriptRoot "NexusNav_Presentacion_Arquitectura.pdf")
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Pptx)) {
    throw "No existe el archivo PPTX: $Pptx"
}

$ppApp = New-Object -ComObject PowerPoint.Application

try {
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    # WithWindow = 0 (msoFalse)
    $pres = $ppApp.Presentations.Open($Pptx, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    
    # 32 = ppSaveAsPDF
    $pres.SaveAs($Pdf, 32)
    $pres.Close()
    Write-Output "PDF_OK: $Pdf"
}
finally {
    $ppApp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppApp) | Out-Null
}
