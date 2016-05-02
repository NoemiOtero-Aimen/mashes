
import yaml
import numpy as np


class Control():
    def __init__(self):
        self.pid = PID()

    def load_conf(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f)
        Kp = data['parameters']['Kp']
        Ki = data['parameters']['Ki']
        Kd = data['parameters']['Kd']
        pwr_min = data['power']['min']
        pwr_max = data['power']['max']
        self.pid.set_parameters(Kp, Ki, Kd)
        self.pid.set_limits(pwr_min, pwr_max)
        return data

    def save_conf(self, filename):
        Kp, Ki, Kd = self.pid.Kp, self.pid.Ki, self.pid.Kd
        pwr_min, pwr_max = self.pid.pwr_min, self.pid.pwr_max
        data = dict(parameters=dict(Kp=Kp, Ki=Ki, Kd=Kd),
                    power=dict(min=pwr_min, max=pwr_max))
        with open(filename, 'w') as f:
            f.write(yaml.dump(data))
        return data

    def output(self, power):
        if power > self.pid.pwr_max:
            power = self.pid.pwr_max
        if power < self.pid.pwr_min:
            power = self.pid_pwr_min
        return power


class PID():
    def __init__(self):
        self.set_parameters(1.0, 1.0, 0.0)
        self.set_limits(0, 1500)
        self.setpoint = 0.0
        self.error = 0.0
        self.time = None
        self.output = 0.0

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_parameters(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def set_limits(self, pwr_min, pwr_max):
        self.pwr_min = pwr_min
        self.pwr_max = pwr_max

    def power(self, value):
        self.output = value
        return self.output

    def update(self, value, time):
        if self.time is None:
            output = self.output
        else:
            error = self.setpoint - value
            delta = time - self.time
            output = self.output + self.Kp * (error - self.error) + self.Ki * error * delta
            self.error = error
            print 'SetPoint', self.setpoint, 'Value', value, 'Time', time
            print 'Delta time', delta, 'Error', error
            if output > self.pwr_max:
                output = self.pwr_max
            if output < self.pwr_min:
                output = self.pwr_min
        self.time = time
        self.output = output
        return output


if __name__ == '__main__':
    filename = '../../config/control.yaml'
    control = Control()
    control.save_conf(filename)
    print control.load_conf(filename)
