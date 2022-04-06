#!/usr/bin/env python
# -*-coding:utf-8-*-


from redis import Redis
conn = Redis()

import redis_lock

from uuid import uuid4

class Test2(object):
    def __init__(self, ):
        self.id = uuid4()
        print(f'Test class id {self.id} init.\n')

    def hello(self):
        import time
        time.sleep(3)
        print(f'Test class id {self.id} say hello.\n')



def f2(x):
    lock = redis_lock.Lock(conn, "name-of-the-lock")
    if lock.acquire():
        print("Got the lock.")

        t = Test2()
        t.hello()

        lock.release()
    else:
        print("Someone else has the lock.")


def main():
    from multiprocessing import Pool
    # f(1)
    with Pool(5) as p:
        print(p.map(f2, range(5)))


if __name__ == '__main__':
    main()