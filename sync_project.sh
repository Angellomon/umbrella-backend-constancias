rsync -r . angel@umbrella-services:~/services/backend-constancias --exclude-from='.gitignore' --exclude '.insomnia' --exclude '.vscode' --exclude .git -v
