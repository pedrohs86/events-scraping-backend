default: deploy-dev

deploy-prod:
	docker build -t events-scraping-backend:prod .
	docker-compose -f composes/events-scraping-backend-prod/docker-compose.yml up -d

deploy-dev:
	docker build -t events-scraping-backend:dev .
	docker-compose -f composes/events-scraping-backend-dev/docker-compose.yml up -d