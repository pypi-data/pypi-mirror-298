import simpy 
import time
from datetime import datetime, timedelta
import random
import logging

class Customer(object):
    def __init__(self, env, number,staff,logging, ds_nodash):
        self.env = env
        self.number = number 
        self.staff = staff  # staff 인자를 받아서 클래스 내부에서 사용
        #분포에 따라 customer 도착
        self.action = env.process(self.customer_generate())
        #self.start_time = datetime.now()
        self.logging = logging
        self.start_time = datetime.strptime(str(ds_nodash)+"000000", "%Y%m%d%H%M%S")

    def customer_generate(self):
        for i in range(self.number):
            name = 'Customer-%s'%i            
            #now = time.time()
            #time.sleep(0.5)
            #print(f"{name} {arrive} 카페도착 {now}")
            current_sim_time = self.start_time + timedelta(seconds=self.env.now)
            self.logging.info(f"{name}, [{current_sim_time}], 카페도착")
            #도착한 고객은 주문하러 이동 
            self.env.process(self.order_coffee(name,self.staff))
            
            interval_time = 10
            yield self.env.timeout(interval_time)

    
    def order_coffee(self, name, staff):
        #직원 요청 
        with self.staff.request() as req:
            yield req

            #직원에게 30초동안 주문 
            ordering_duration = 30
            yield self.env.timeout(ordering_duration)
            current_sim_time = self.start_time + timedelta(seconds=self.env.now)
            self.logging.info(f"{name}, [{current_sim_time}], 주문완료")
            
        #주문한 고객은 커피 수령을 위해 대기
        yield self.env.process(self.wait_for_coffee(name))

    def wait_for_coffee(self, name):
        #30초 대기 후 커피 수령 
        waiting_duration = 30
        yield(self.env.timeout(waiting_duration))
        current_sim_time = self.start_time + timedelta(seconds=self.env.now)
        self.logging.info(f"{name}, [{current_sim_time}], 커피수령")

def start(logging,ds_nodash):    
    
    env = simpy.Environment()
    staff = simpy.Resource(env, capacity=2)
    
    random_value = random.randint(1000, 1500)
    print(random_value)
    
    customer = Customer(env, random_value ,staff, logging, ds_nodash)
    env.run()
