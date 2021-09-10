install:
	pip install --upgrade pip && pip install -r requirements.txt

build:
	docker build -t motd:latest .

run:
	docker run -p 8080:8080 motd

run-kube:
	kubectl --kubeconfig ~/.kube/config apply -f kube-motd.yaml

invoke:
	curl --cookie cookie.txt --cookie-jar cookie.txt -H 'Accept: application/json' http://127.0.0.1:8080/motd

all: install build run