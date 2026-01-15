@echo off
echo ================================================
echo     Pronote Ameliore - Installation
echo ================================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8 ou superieur depuis python.org
    pause
    exit /b 1
)

REM Creer l'environnement virtuel s'il n'existe pas
if not exist ".venv" (
    echo [1/4] Creation de l'environnement virtuel...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree
) else (
    echo [OK] Environnement virtuel deja existant
)

echo.
echo [2/4] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

echo [OK] Environnement virtuel active
echo.
echo [3/4] Installation des dependances...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer les dependances
    pause
    exit /b 1
)

echo [OK] Dependances installees
echo.
echo [4/4] Lancement de l'application...
echo.
python -m app.main

REM Si l'application se ferme, garder la fenetre ouverte
if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] L'application s'est terminee avec une erreur
    pause
)
