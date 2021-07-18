import time
import Adafruit_PCA9685

class Motor:

    def __init__(self):
        self.digit = None
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

    def convert(self,result):
        """转换垃圾的名字"""
        waste = {'Residual Waste':'1', 'Household Food Waste':'2'}
        for key, value in waste.items:
            if result == key:
                return value
        
    def Fw_motion(self,a):
        """食物垃圾"""
        n = 1
        while n:
            self.pwm.set_pwm(1, 0, a )      
            time.sleep(2)
            self.pwm.set_pwm(1, 0, a + 160) #return
            n = n - 1
    
    def Hw_motion(self,b):
        """有害垃圾"""
        n = 1
        while n:
            self.pwm.set_pwm(2, 0, b) 
            time.sleep(2)
            self.pwm.set_pwm(2, 0, b + 160)
            n = n - 1


    def motion(self, conn):
        """根据digit，完成不同的工作"""
        while True:
            digit = conn.recv()
            if digit == 'Residual Waste':
                self.Fw_motion(80)
            elif digit == 'Household Food Waste':
                self.Hw_motion(120)
            else:
                pass
