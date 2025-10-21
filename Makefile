# Make

clean:
	@echo cleaning
	rm -rf __pycache__

git:
	git add .
	git commit -m auto
	git push

# EOF
