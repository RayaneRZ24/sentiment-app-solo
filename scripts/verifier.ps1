param([switch]$Detail)
$ErrorActionPreference = 'Stop'
$racineProjet = Split-Path -Parent $PSScriptRoot
$pythonProjet = Join-Path $racineProjet '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonProjet)) { throw 'Creer .venv et installer les dependances (README.md).' }
function Invoke-Etape {
    param([string]$Titre, [string[]]$ArgumentsPython)
    Write-Host "`n$Titre" -ForegroundColor Cyan
    & $pythonProjet -X utf8 @ArgumentsPython
    if ($LASTEXITCODE -ne 0) { throw "Echec : $Titre (code $LASTEXITCODE)." }
}
Push-Location $racineProjet
try {
    git log --oneline -20
    git status
    Invoke-Etape 'Diagnostic solo' @('scripts/check_setup.py')
    Invoke-Etape 'Donnees' @('src/make_demo.py')
    Invoke-Etape 'Modele de demonstration' @('src/train.py')
    Invoke-Etape 'Evaluation' @('src/evaluate.py')
    Invoke-Etape 'Ruff' @('-m', 'ruff', 'check', '.')
    Invoke-Etape 'Mypy' @('-m', 'mypy', 'api')
    Invoke-Etape 'Tests et couverture' @('-m', 'pytest', '-q', '--cov=api', '--cov-report=term-missing', '--cov-fail-under=95')
    Invoke-Etape 'Version du paquet' @('-m', 'sentiment_app', '--version')
    Invoke-Etape 'Prediction via le paquet' @('-m', 'sentiment_app', 'predict', 'Livraison rapide, produit conforme, tres satisfait')
    if ($Detail) {
        Invoke-Etape 'Tests detailles' @('-m', 'pytest', 'tests/', '-v')
        foreach ($fichierTest in @('test_model.py','test_api.py','test_limites.py','test_integration.py','test_jeu_or.py','test_client.py','test_interface.py','test_packaging.py')) {
            Invoke-Etape $fichierTest @('-m', 'pytest', "tests/$fichierTest", '-q')
        }
        Invoke-Etape 'Courbe du seuil' @('src/courbe_seuil.py')
        Invoke-Etape 'Bilan du jeu or' @('src/bilan_jeu_or.py')
    }
}
finally { Pop-Location }
