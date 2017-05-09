from environment import Environment
        
if __name__ == '__main__': 
    env = Environment(sim_type=input(), light_type=input())
    env.run()
    #env = Environment(sim_type='train_frame', light_type='gallilean')
    #env = Environment(sim_type='train_frame', light_type='einstein')
    #env = Environment(sim_type='stationary_train', light_type='einstein')
    #env = Environment(sim_type='moving_train', light_type='einstein')
    #env = Environment(sim_type='moving_train', light_type='gallilean')
    #env.run()
    pass
    
    