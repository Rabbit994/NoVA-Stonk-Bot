Start-Process -FilePath "docker" -ArgumentList "stop stonk-bot" -Wait
Start-Process -Filepath "docker" -ArgumentList "rm stonk-bot" -Wait
Start-Process -FilePath "docker" -ArgumentList "system prune -f" -Wait
Start-Process -FilePath "docker" -ArgumentList "build -t stonk-bot:latest . --no-cache" -Wait
Start-Process -FilePath "docker" -ArgumentList "run -d --name stonk-bot --restart=on-failure:10 stonk-bot:latest"