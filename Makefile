REPO   ?= yamal-herd
REMOTE ?= origin
BRANCH ?= main

.PHONY: help verify size dev build preview serve push tag clean
help:
	@echo "make verify   — статические проверки сборки (скобки, DOM-id, уровни)"
	@echo "make size     — отчёт о размере файлов"
	@echo "make dev      — vite dev server"
	@echo "make serve    — простой статик-сервер (python3, без npm)"
	@echo "make build    — vite build → dist/"
	@echo "make preview  — предпросмотр прод-сборки"
	@echo "make push     — git push + tags"
	@echo "make tag V=4.2.1 — новый тег"

verify: ; @python3 scripts/verify.py
size:   ; @bash scripts/size-report.sh
dev:    ; @npx vite --host
serve:  ; @python3 -m http.server 8080
build:  ; @npx vite build
preview:; @npx vite preview --host
push:   ; @git push $(REMOTE) $(BRANCH) --tags
tag:    ; @git tag -a v$(V) -m "release v$(V)" && git push $(REMOTE) v$(V)
clean:  ; @rm -rf dist node_modules
