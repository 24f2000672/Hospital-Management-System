# MAD 2 Project
# To open out folder in vs code:
    go to the root folder,go inside,rightclick and give open terminal and give command:
        code.

# command to run backend:
    Create cirtual environment with name mad2venv using 
        python -m venv mad2venv
    to Activate :
        mad2venv/Scripts/activate
    create requirements file and to update it use:
        pip freeze > requirements.txt
    install all requirements
        pip install flask-restful
        pip install  -r.\requirements.txt
        pip install flask_sqlalchemy
to return to main forlder use cd..

# Day 2:
1.Used JWS tokens and authentication
2.Provided role based access for admin,doctor and patient
3.For npm,after downloading node.js do this 
    i.npm create vue@latest and answer all questions
    ii.afterthat locate to frontend folder and give command to run frontend:
        cd frontend
        npm install
        npm run format
        npm run dev
