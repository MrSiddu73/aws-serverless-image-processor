# Pillow Layer Setup for Lambda (Python 3.9)

1. Open CloudShell.
2. Run:

mkdir pillow-layer
cd pillow-layer
python3.9 -m pip install pillow -t python/lib/python3.9/site-packages/
zip -r pillow_layer.zip python

3. Upload ZIP to S3:
aws s3 cp pillow_layer.zip s3://imageuploadsiddu/

4. Go to Lambda → Layers → Create Layer
5. Select S3 file → pillow_layer.zip
6. Select runtime: Python 3.9
7. Add layer to your Lambda function.
