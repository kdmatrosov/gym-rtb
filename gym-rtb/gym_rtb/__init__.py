from gym.envs.registration import register

register(
    id='Rtb-v0',
    entry_point='gym_rtb.envs:RtbEnv',
)