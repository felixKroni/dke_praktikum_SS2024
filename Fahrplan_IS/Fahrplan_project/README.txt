To install all dependencies execute: 
...\Fahrplan_IS\Fahrplan_project>  pip install -r requirements.txt


Docker stuff
Navigate to Folder where the Dockerfile is located
Create image: docker build -t fahrplan:latest .
Create Container: docker run --name fahrplan -d -p 8000:5000 --rm fahrplan:latest

