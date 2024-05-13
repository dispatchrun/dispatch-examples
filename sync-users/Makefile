.PHONY: clean deps users

users: users.db

deps:
	pip install -r requirements.txt

users.db:
	python generate_users.py

clean:
	rm -f users.db
