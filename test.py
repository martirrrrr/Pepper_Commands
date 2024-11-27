import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan
from naoqi import ALProxy

def move_base():
    """Controlla il movimento base di Pepper."""
    pub = rospy.Publisher('/pepper_robot/cmd_vel', Twist, queue_size=10)
    twist = Twist()
    twist.linear.x = 0.3  # Avanza
    twist.angular.z = 0.5  # Ruota
    rospy.loginfo("Pepper sta avanzando e ruotando.")
    for _ in range(10):  # Invia il comando per 1 secondo (10 Hz)
        pub.publish(twist)
        rospy.sleep(0.1)

def move_head():
    """Sposta la testa di Pepper."""
    robot_ip = "127.0.0.1"
    robot_port = 9559
    motion = ALProxy("ALMotion", robot_ip, robot_port)
    rospy.loginfo("Muovendo la testa di Pepper.")
    motion.setAngles("HeadYaw", 0.5, 0.2)  # Ruota la testa a destra

def make_speak():
    """Fa parlare Pepper."""
    robot_ip = "127.0.0.1"
    robot_port = 9559
    tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
    rospy.loginfo("Pepper sta parlando.")
    tts.say("Ciao, sono in simulazione!")

def read_laser():
    """Legge i dati del laser di Pepper."""
    def callback(data):
        rospy.loginfo("Dati laser ricevuti: %s", data.ranges[:5])  # Stampa primi 5 valori
        rospy.signal_shutdown("Laser letti.")  # Ferma il nodo dopo aver letto

    rospy.Subscriber('/pepper_robot/laser/scan', LaserScan, callback)
    rospy.loginfo("In attesa dei dati del laser...")
    rospy.spin()

def read_camera():
    """Legge i dati della camera di Pepper."""
    def callback(data):
        rospy.loginfo("Dati immagine ricevuti. Altezza: %d, Larghezza: %d",
                      data.height, data.width)
        rospy.signal_shutdown("Immagine letta.")  # Ferma il nodo dopo aver letto

    rospy.Subscriber('/pepper_robot/camera/rgb/image_raw', Image, callback)
    rospy.loginfo("In attesa dei dati della camera...")
    rospy.spin()

def record_rosbag():
    """Registra tutti i topic in un rosbag."""
    rospy.loginfo("Registrazione rosbag iniziata. Premi CTRL+C per fermare.")
    try:
        rospy.sleep(10)  # Simula una registrazione di 10 secondi
    except KeyboardInterrupt:
        rospy.loginfo("Registrazione rosbag terminata.")

def main():
    rospy.init_node('pepper_control', anonymous=True)

    # Scegli l'azione da eseguire in base al flag
    flag = "move_base"  # Modifica il flag con "move_head", "make_speak", ecc.

    if flag == "move_base":
        move_base()
    elif flag == "move_head":
        move_head()
    elif flag == "make_speak":
        make_speak()
    elif flag == "read_laser":
        read_laser()
    elif flag == "read_camera":
        read_camera()
    elif flag == "record_rosbag":
        record_rosbag()
    else:
        rospy.logerr("Flag non riconosciuto: %s", flag)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
