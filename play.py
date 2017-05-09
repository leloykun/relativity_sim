from environment import Environment
import thorpy

if __name__ == '__main__':
    env = Environment(menu=None, reference_frame='ground', has_time_dim=True, transformation='lorrentz', switchable=True)
    env.run()