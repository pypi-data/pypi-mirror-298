import threading
import time
import os
from queue import Queue
from queue import Empty

def read_file(file_path, follow=False, queue=None):
    """
    读取文件的内容并将其放入队列中。
    如果 follow=True, 则像 tail -f 一样持续监控文件更新。
    否则，就像 cat 一样只读取一次文件内容。
    """
    try:
        with open(file_path, 'r') as file:
            # 移动到文件末尾
            if follow:
                file.seek(0, os.SEEK_END)
                while True:
                    where = file.tell()
                    line = file.readline()
                    if not line:
                        # 如果没有新行并且是 follow 模式，则等待一会儿再尝试读取
                        time.sleep(1)
                        file.seek(where)
                    else:
                        # 将文件名和行内容放入队列
                        queue.put({"log_path": file_path, "line": line})
            else:
                lines = file.readlines()
                for line in lines:
                    # 将文件名和行内容放入队列
                    queue.put({"log_path": file_path, "line": line})
    except FileNotFoundError:
        print(f"File not found: {file_path}")


def consume_queue(queue):
    """
    从队列中消费数据并打印。
    """
    while True:
        item = queue.get()
        if item is None:
            break
        print(item)
        queue.task_done()


def main():
    files = ['/var/log/nginx/www.flyml.net-extended.log']  # 文件列表
    queue = Queue()  # 创建一个队列用于传递数据

    # 创建一个线程专门用于消费队列中的数据
    consumer_thread = threading.Thread(target=consume_queue, args=(queue,))
    consumer_thread.start()

    # 创建读取文件的线程
    threads = []
    for file in files:
        file = file.strip()
        print(f"!!!!! file: {file} exists: {os.path.exists(file)}")
        thread = threading.Thread(target=read_file, args=(file, True, queue))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 确保所有任务都被处理完毕
    queue.join()

    # 告诉消费线程停止
    queue.put(None)
    consumer_thread.join()


if __name__ == "__main__":
    main()