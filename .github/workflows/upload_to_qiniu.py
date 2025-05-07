import os
import qiniu

def upload_file(local_file, key, access_key, secret_key, bucket):
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket, key, 3600)

    try:
        ret, info = qiniu.put_file(token, key, local_file)
        if ret is not None:
            print(f"File {local_file} uploaded successfully as {key}")
        else:
            print(f"Failed to upload file {local_file}: {info}")
    except Exception as e:
        print(f"An error occurred while uploading file {local_file}: {e}")

def main():
    source_dir = 'dist'
    dest_dir = '/dist/'

    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    for root, _, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir)
            key = os.path.join(dest_dir.strip('/'), relative_path).lstrip('/')
            upload_file(local_path, key, os.getenv('QINIU_ACCESS_KEY'), os.getenv('QINIU_SECRET_KEY'), os.getenv('QINIU_BUCKET'))

if __name__ == "__main__":
    main()



