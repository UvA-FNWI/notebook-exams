#!/bin/bash

echo "-- Pulling Docker image... (this can take a while)"

docker pull notebookexams/uva-notebook 1> /dev/null

cat > jupyter_config.py << EOF
c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = u''
c.NotebookApp.disable_check_xsrf = True
EOF

echo "-- Starting notebook container..."
echo ""

CID=$(docker run -d -p 8123:8888 -e STUDENT_QUESTIONS_FILE='questions.json' -e STUDENT_ANSWERS_FILE='answers.json' --mount type=bind,source=$(pwd),target=/var/host-files notebookexams/uva-notebook jupyter notebook --ip=0.0.0.0 --allow-root --config=/var/host-files/jupyter_config.py /var/host-files/ 2> /dev/null)

if [ $? -eq 0 ]; then
    sleep 5
    python -m webbrowser "http://localhost:8123"
    
    docker attach $CID
else
    echo ""
    echo "Something went wrong. Is Docker running? If not, start Docker and try again."
    echo ""
fi

