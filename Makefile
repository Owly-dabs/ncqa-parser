install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
install-uv:
		uv pip install -r requirements.txt