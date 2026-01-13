.PHONY: install ingest run eval

install:
	python -m pip install -r requirements.txt

ingest:
	python ingest.py

run:
	streamlit run app.py

eval:
	python eval_run.py
