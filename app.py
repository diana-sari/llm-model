from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import boto3
import os

app = Flask(__name__)

# AWS S3 configuration
s3_client = boto3.client('s3')
bucket_name = 'llm-bucket-dsari'
model_save_path = 'model/'
local_model_dir = './model'

if not os.path.exists(local_model_dir):
    os.makedirs(local_model_dir)

# Download the model from S3
for file_name in s3_client.list_objects_v2(Bucket=bucket_name, Prefix=model_save_path)['Contents']:
    s3_client.download_file(bucket_name, file_name['Key'], os.path.join(local_model_dir, file_name['Key'].split('/')[-1]))

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_model_dir)
model = AutoModelForSequenceClassification.from_pretrained(local_model_dir)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get("text")
    inputs = tokenizer(input_text, return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1).item()
    return jsonify({'prediction': predictions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

