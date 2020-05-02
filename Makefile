
# Zip lambda from handler.py and site-packages
zip:
	zip -r ../newscollector.zip .

dependencies:
	pip install --upgrade -r requirements.txt -t ./ && chmod -R 755 .
