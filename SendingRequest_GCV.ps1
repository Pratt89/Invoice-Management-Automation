$env:GOOGLE_APPLICATION_CREDENTIALS="service-account-file.json"
$cred = gcloud auth application-default print-access-token
$headers = @{ "Authorization" = "Bearer $cred" }

Invoke-WebRequest `
  -Method POST `
  -Headers $headers `
  -ContentType: "application/json; charset=utf-8" `
  -InFile request.json `
  -Uri "https://vision.googleapis.com/v1/images:annotate" | Select-Object -Expand Content