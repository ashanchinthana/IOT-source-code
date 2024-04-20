
import RPi.GPIO as GPIO
import time

# Define GPIO pins
IN1, IN2, IN3, IN4 = 24, 23, 27, 22  # Motor control pins
ENA, ENB = 25, 5  # Speed control pins for PWM
IR_left, IR_right ,IR_stop= 20, 21, 4  # IR sensor GPIO Pins
S0, S1, S2, S3, OUT = 18, 15, 26, 6, 14  # Color sensor pins

servo_pin_1 = 19  # Use the correct pin where your first servo is connected
servo_pin_2 = 13
servo_pin_3 = 0
servo_pin_4 = 11    # Use the correct pin where your second servo is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_1, GPIO.OUT)
GPIO.setup(servo_pin_2, GPIO.OUT)
GPIO.setup(servo_pin_3, GPIO.OUT)
GPIO.setup(servo_pin_4, GPIO.OUT)
GPIO.setup(IR_stop, GPIO.IN)


# Setup PWM
pwm1 = GPIO.PWM(servo_pin_1, 50)  # Initialize PWM on servo_pin_1 at 50Hz
pwm1.start(0)
pwm2 = GPIO.PWM(servo_pin_2, 50)  # Initialize PWM on servo_pin_2 at 50Hz
pwm2.start(0)
pwm3 = GPIO.PWM(servo_pin_3, 50)  # Initialize PWM on servo_pin_2 at 50Hz
pwm3.start(0)
pwm4 = GPIO.PWM(servo_pin_4, 50)  # Initialize PWM on servo_pin_2 at 50Hz
pwm4.start(0)

def set_servo_angle(servo, angle, delay=0.03):
    """
    Move the servo to a specified angle with controlled speed.
    
    :param servo: Servo PWM object.
    :param angle: Target angle.
    :param delay: Delay between each incremental move (in seconds). 
                  Smaller values result in faster movement.
    """
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(delay)

# Initialize GPIO setup
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Disable warnings

    # Setup GPIO pins
    GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB, S0, S1, S2, S3, IR_left, IR_right, OUT], GPIO.OUT)
    GPIO.setup([IR_left, IR_right, OUT], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output([S0, S1], [GPIO.HIGH, GPIO.LOW])

    # Initialize PWM
    pwmA = GPIO.PWM(ENA, 100)
    pwmB = GPIO.PWM(ENB, 100)
    pwmA.start(0)
    pwmB.start(0)

    return pwmA, pwmB

# Initialize GPIO and PWM
pwmA, pwmB = init_gpio()

# Pulse counter for color sensor
pulse_count = 0

def pulse_counter(channel):
    global pulse_count
    pulse_count += 1

GPIO.add_event_detect(OUT, GPIO.FALLING, callback=pulse_counter)

# Function definitions for motor control and color detection
def control_motors(motor1, motor2, speed=25):
    GPIO.output([IN1, IN2], motor1)
    GPIO.output([IN3, IN4], motor2)
    pwmA.ChangeDutyCycle(speed if motor1 != (False, False) else 0)
    pwmB.ChangeDutyCycle(speed if motor2 != (False, False) else 0)

def stop():
    control_motors((False, False), (False, False))
    
def stop1():
    control_motors((False, False), (False, False))
    arm1()
def cool1():
    while True:
        print("dfgdf")

def forward(speed=20):
    control_motors((False, True), (False, True), speed)
def back(speed=20):
    control_motors((True, False), (True, False), speed)

def left(speed=40):
    control_motors((False, True), (True, False), speed)

def right(speed=40):
    control_motors((True, False), (False, True), speed)

def rightonly(speed=40):
    control_motors((True, False), (False, False), speed)

def leftonly(speed=40):
    control_motors((False, False), (False, True), speed)
def read_color():
    global pulse_count
    color_readings = {}
    for filter_color in ['Red', 'Green', 'Blue']:
        GPIO.output(S2, filter_color == 'Blue')
        GPIO.output(S3, filter_color == 'Red' or filter_color == 'Blue')
        pulse_count = 0
        time.sleep(0.01)
        color_readings[filter_color] = pulse_count
    return color_readings['Red'], color_readings['Green'], color_readings['Blue']

def detect_color(red, green, blue):
    # Check to avoid division by zero
    denominator = red + green + blue if red + green + blue > 0 else 1

    # Normalize the RGB components
    red_ratio = red / denominator
    green_ratio = green / denominator
    blue_ratio = blue / denominator

    if red_ratio > green_ratio and red_ratio > blue_ratio:
        if red_ratio - green_ratio > 0.4 and red_ratio - blue_ratio > 0.4:
            print("Color Detected: Red")
            return "red"
        elif red_ratio - green_ratio < 0.2 and green_ratio - blue_ratio > 0.2:
            print("Color Detected: Orange")
            return "orange"
        else:
            print("Color Detected: Pink")
            return "pink"
    elif green_ratio > red_ratio and green_ratio > blue_ratio:
        if green_ratio - red_ratio > 0.4:
            print("Color Detected: Green")
            return "green"
        else:
            print("Color Detected: Yellow")
            return "yellow"
    elif blue_ratio > red_ratio and blue_ratio > green_ratio:
        if blue_ratio - red_ratio > 0.4:
            print("Color Detected: Blue")
            return "blue"
        else:
            print("Color Detected: Purple")
            return "purple"
    elif red_ratio > 0.4 and green_ratio > 0.3 and blue_ratio < 0.2:
        print("Color Detected: Brown")
        return "brown"
    elif abs(red_ratio - green_ratio) < 0.1 and blue_ratio < 0.5:
        print("Color Detected: Yellow")
        return "yellow"
    else:
        print("Unknown Color")
        return "unknown"





# Example usage
red, green, blue = read_color()  # Assuming read_color() returns the normalized values of red, green, and blue
color = detect_color(red, green, blue)
print(f"Color Detected: {color}")

def arm1():
    print("sdfgjkldfffsdfkgjsdofigjhsdfijgosdjfgosjfdgojsfdgioj")
    
    for angle in range(90, 180, 1):  
        set_servo_angle(pwm1, angle, delay=0.03)
    print("1")   
    for angle in range(120, 180, 1):  
        set_servo_angle(pwm2, angle, delay=0.03) 
    for angle in range(1, 89, 1):  
        set_servo_angle(pwm3, angle, delay=0.03)
    print("2") 
    for angle in range(180, 140, -1):  
        set_servo_angle(pwm2, angle, delay=0.03)
    for angle in range(88, 70, -1):  
        set_servo_angle(pwm3, angle, delay=0.03)
    for angle in range(180, 0, -1):  
        set_servo_angle(pwm4, angle, delay=0.07)
    print("3") 
    for angle in range(69, 0, -1):  
        set_servo_angle(pwm3, angle, delay=0.03)
    for angle in range(139, 121, -1):  
        set_servo_angle(pwm2, angle, delay=0.03) 
    print("5")  
    for angle in range(179, 89, -1):  
        set_servo_angle(pwm1, angle, delay=0.03)
        #for angle in range(180, 90, 1):  
            #set_servo_angle(pwm4, angle, delay=0.07)
    pwm1.stop()
    pwm2.stop()
    pwm3.stop()
    pwm4.stop()
    runback()




def homearm():
    
    for angle in range(90, 180, 1):  
        set_servo_angle(pwm1, angle, delay=0.03)
    for angle in range(0, 180, 1):  
        set_servo_angle(pwm4, angle, delay=0.001)
    print("1")

    for angle in range(120, 180, 1):  
        set_servo_angle(pwm2, angle, delay=0.03) 
    for angle in range(1, 89, 1):  
        set_servo_angle(pwm3, angle, delay=0.03)
    print("2")

    for angle in range(180, 140, -1):  
        set_servo_angle(pwm2, angle, delay=0.03)
    for angle in range(88, 70, -1):  
        set_servo_angle(pwm3, angle, delay=0.03)
    print("3")


    for angle in range(180, 0, -1):  
        set_servo_angle(pwm4, angle, delay=0.07)

        #for angle in range(180, 0, -1):  
            #set_servo_angle(pwm1, angle, delay=0.03)

   # Slow movement
        #for angle in range(180, 0, 1):  
            #set_servo_angle(pwm4, angle, delay=0.07)
    for angle in range(69, 0, -1):  
        set_servo_angle(pwm3, angle, delay=0.03)
    print("4")
    for angle in range(139, 121, -1):  
        set_servo_angle(pwm2, angle, delay=0.03)  
    for angle in range(180, 91, -1):  
        set_servo_angle(pwm1, angle, delay=0.03)
    print("8")

    run1()

  # Faster movement
        








def run1():
    try:
        while True:
            red, green, blue = read_color()
            color = detect_color(red, green, blue)
            print(color)

            IR_left_state = GPIO.input(IR_left)
            IR_right_state = GPIO.input(IR_right)

            # Movement logic based on IR sensor states
            if IR_left_state == 0 and IR_right_state == 0 and color == "yellow":
                print("forward")
                forward()
            elif IR_left_state == 1 and IR_right_state == 0 and color == "yellow":
                print("left")
                left()
            elif color == "purple":
                stop1()
            elif IR_left_state == 0 and IR_right_state == 1 and color == "yellow":
                print("right")
                right()

            time.sleep(0.00001)  # Adjust as needed for responsiveness

    except KeyboardInterrupt:
        stop()

def runback():
    try:
        while True:
            red, green, blue = read_color()
            color = detect_color(red, green, blue)
            print(color)

            IR_left_state = GPIO.input(IR_left)
            IR_right_state = GPIO.input(IR_right)
            IR_stop1 = GPIO.input(IR_stop)

            # Movement logic based on IR sensor states
            if IR_left_state == 0 and IR_right_state == 0 and IR_stop1 == 0:
                print("forward")
                forward()
            elif IR_left_state == 1 and IR_right_state == 0 and IR_stop1 == 0:
                print("left")
                left()
                
                
            elif IR_stop1==1:
                stop()
            elif IR_left_state == 0 and IR_right_state == 1 and IR_stop1 == 0:
                print("right")
                
                right()

            time.sleep(0.00001)  # Adjust as needed for responsiveness

    except KeyboardInterrupt:
        stop()



