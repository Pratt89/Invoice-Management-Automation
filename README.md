# Invoice-Management-Automation
This project is based on Invoice Management Processing &amp; Automation.

Dependencies are: 
1. pdftotext
2. invoice2data
3. pillow

workflow:
1. if searchable pdf -> feed to yaml template -> save output in invoice.json
2. if non-searchable pdf/image -> base64 encoded string format -> set in content key-value in request.json -> send the request to gcv -> save output in response.json -> perform hocr to make searchable pdf -> feed to yaml template -> save output in invoice.json
