.PHONY: test
test:
	xvfb-run -a uv run pytest
