# edusharing-crawler

## Requirements
* splash service nedded by crawlers
    * Splash creates screenshots from web pages when thumbnails are not available
    * for example use [ntppool/splash](https://artifacthub.io/packages/helm/ntppool/splash)

## List of available Crawlers/Scripts
* mediothek_pixiothek_spider
* merlin_spider
* oeh_importer
* permission_updater
* sodix_spider

## Helm Chart Registry
The Helm Charts get published in: [helm-charts-registry](https://github.com/hpi-schul-cloud/helm-charts-registry)

## Helm Chart Installation
Provide the needed Environment Values and install the Helm Chart
```
helm repo add dbildungscloud https://hpi-schul-cloud.github.io/helm-charts-registry/
helm repo update
helm install dbildungscloud/edusharing-crawlers -f myvalues.yaml
```

## Environment Variables
The following environment variables are read:

| Name        | Crawler/Scripts      | Description | Example Value |
| ----------- | ----------- | ----------- | ------------- |
| CRAWLER | ALL | Name of the crawler/script | `sodix_spider` |
| SCHEDULE | ALL | Time on which the Crawler starts to run  | `*-*-20:00` |
| EDU_SHARING_BASE_URL | ALL | Edusharing Instance Url  | `http://edusharing-repository-service.my-namespace.svc.cluster.local:8081/edu-sharing/` |
| EDU_SHARING_USERNAME | ALL | Edusharing User to authenticate | `my_user` |
| EDU_SHARING_PASSWORD | ALL | Edusharing Password to authenticate  | `my_password` |
| DRY_RUN | ALL (optinal) | Define whether not to upload to Edu-Sharing instance (default is `False`)  | `False` |
| LOG_LEVEL | ALL (optional) | Set the Log Level (default is `INFO`)  | `INFO` |
| SPLASH_URL | mediothek_pixiothek_spider, merlin_spider, oeh_importer, sodix_spider | Provide Url for Crawler to connect to | `http://splash.my-namespace.svc.cluster.local:8050` |
| SODIX_USER | sodix_spider | Sodix User to authenticate  | `my_sodix_user` |
| SODIX_PASSWORD | sodix_spider | Sodix Password to authenticate  | `my_sodix_password` |
| S3_ACCESS_KEY | h5p_upload, fwu_upload | Access Key with access to the Bucket  | `my_s3_access_key` |
| S3_SECRET_KEY | h5p_upload, fwu_upload| Secret Key with access to the Bucket  | `my_s3_secret_key` |
| S3_ENDPOINT_URL | h5p_upload, fwu_upload| URL of the S3 storage provider   | `my_s3_endpoint_url` |
| S3_BUCKET_NAME | h5p_upload, fwu_upload| Name of the bucket to connect to  | `my_s3_bucket_name` |



