alias build_dc='docker build -t projectName . '
alias run_dc='docker run -d --name projectName -p 8000:8000 projectName'
alias run_ptr='poetry run uvicorn main:app --reload --app-dir src '