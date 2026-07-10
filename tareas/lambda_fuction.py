import requests
import boto3

s3 = boto3.client("s3")
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
services = ["yellow", "green", "fhv", "fhvhv"]
years = [2024, 2025, 2026]

def lambda_handler(event, context):
    bucket = "xideralaws-curso-paoesquivel2026"
    archivos_subidos = []

    for year in years:
        for service in services:
            for m in range(1, 13):
                url = f"{base_url}{service}_tripdata_{year}-{str(m).zfill(2)}.parquet"
                filename = f"{service}_{year}_{str(m).zfill(2)}.parquet"
                key = f"{year}/{filename}"

                r = requests.get(url)
                print(f"{url} -> {r.status_code}")

                if r.status_code == 200:
                    s3.put_object(Bucket=bucket, Key=key, Body=r.content)
                    archivos_subidos.append(key)
                else:
                    print(f"Archivo no disponible: {url}")

    return {
        "statusCode": 200,
        "message": "Carga completada en S3",
        "files": archivos_subidos
    }
