
# Zip lambda from handler.py and site-packages
zip:
	zip -r ../newscollector.zip . -x '*.git*'

dependencies:
	pip install --upgrade -r requirements.txt -t ./ && chmod -R 755 .
