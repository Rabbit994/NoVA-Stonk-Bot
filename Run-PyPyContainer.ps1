Start-Process -FilePath "docker" -ArgumentList "stop pypy-stock" -Wait
Start-Process -Filepath "docker" -ArgumentList "rm pypy-stock" -Wait
Start-Process -FilePath "docker" -ArgumentList "system prune -f" -Wait
Start-Process -FilePath "docker" -ArgumentList "build -t pypy-stock:latest -f pypy.dockerfile ." -Wait
Start-Process -FilePath "docker" -ArgumentList "run -d --name pypy-stock --restart=on-failure:10 pypy-stock:latest"