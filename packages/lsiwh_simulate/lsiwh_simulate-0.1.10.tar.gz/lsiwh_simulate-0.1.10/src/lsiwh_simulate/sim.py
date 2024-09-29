from customer import Customer
import simpy

def start():
    env = simpy.Environment()
    staff = simpy.Resource(env, capacity=2)
    customer = Customer(env, 10)

    env.run()
              
