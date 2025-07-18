from datetime import datetime
import boto3
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

key_id = ''
secret_key_id = ''
bucket_name = ''
local_directory = ''

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=key_id,
    aws_secret_access_key=secret_key_id
)

def merge_files(file1, file2, file3):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df3 = pd.read_excel(file3)

    all_columns = list(df1.columns) + [col for col in df2.columns if col not in df1.columns]
    all_columns = all_columns + [col for col in df3.columns if col not in all_columns]

    for df in [df1, df2, df3]:
        for column in all_columns:
            if column not in df.columns:
                df[column] = pd.NA

    df1 = df1[all_columns]
    df2 = df2[all_columns]
    df3 = df3[all_columns]

    merged_df = pd.concat([df1, df2, df3], ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset=["Номер сообщения", "Номер заявки"])

    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    output_file = f"uvao_ng_ticket_{timestamp}.xlsx"
    merged_df.to_excel(output_file, index=False)
    return output_file

def find_latest_matching_files():
    files = [f for f in os.listdir(local_directory) if f.endswith('.xlsx')]
    messages = [f for f in files if f.startswith('ОИВ Сообщения')]
    replies = [f for f in files if f.startswith('ОИВ Ответы в работе')]

    if len(messages) < 2 or not replies:
        return None, None, None

    sorted_messages = sorted(messages, key=lambda f: os.path.getmtime(os.path.join(local_directory, f)), reverse=True)
    latest_message1 = sorted_messages[0]
    latest_message2 = sorted_messages[1]
    latest_reply = max(replies, key=lambda f: os.path.getmtime(os.path.join(local_directory, f)))

    return (os.path.join(local_directory, latest_message1), 
            os.path.join(local_directory, latest_message2),
            os.path.join(local_directory, latest_reply))

class S3UploadHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_uploaded_triple = None

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.xlsx'):
            return

        time.sleep(2)

        msg_file1, msg_file2, reply_file = find_latest_matching_files()

        if not msg_file1 or not msg_file2 or not reply_file:
            print("Ждём появления трёх файлов (2 сообщений + 1 ответы)...")
            return

        if self.last_uploaded_triple == (msg_file1, msg_file2, reply_file):
            return

        print(f"Объединяем файлы:\n- {os.path.basename(msg_file1)}\n- {os.path.basename(msg_file2)}\n- {os.path.basename(reply_file)}")
        merged_file = merge_files(msg_file1, msg_file2, reply_file)
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        new_file_name = f"uvao_ng_ticket_{timestamp}.xlsx"

        try:
            s3.upload_file(merged_file, bucket_name, f'uploads/{new_file_name}')
            print(f"Файл {new_file_name} загружен в стораге.")
            self.last_uploaded_triple = (msg_file1, msg_file2, reply_file)
        except Exception as e:
            print(f"Ошибка: {e}")


event_handler = S3UploadHandler()
observer = Observer()
observer.schedule(event_handler, path=local_directory, recursive=False)
observer.start()
print("Чекаем директорию на появление трёх файлов (2 сообщений + 1 ответы)...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()