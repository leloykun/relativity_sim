from environment import Environment
        
if __name__ == '__main__': 
    env = Environment(menu=None, sim_type=input(), light_type=input())
    env.run()
    #env = Environment(sim_type='train_time', light_type='gallilean')
    #env = Environment(sim_type='train_time', light_type='lorentz')
    #env = Environment(sim_type='train_notime', light_type='lorentz')
    #env = Environment(sim_type='ground_notime', light_type='lorentz')
    #env = Environment(sim_type='ground_notime', light_type='gallilean')
    #env.run()
    pass
    
    