
# Zip lambda from handler.py and site-packages
zip:
	zip -r ../newscollector.zip .

dependencies:
	pip install -r requirements.txt -t ./ && chmod -R 755 .
