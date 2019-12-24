Get-ChildItem -Path $(Get-Location) -File -Include 0001_initial.py,db.sqlite3 -Recurse | Remove-Item -Force -Verbose
python manage.py makemigrations
python manage.py migrate
python .\script.py