short right_LED = 8;
short left_LED = 10;
int analogPin_Left = 0;         // Left PhotoDiode connect on anaglog pin2
int analogPin_Right = 1;        // Right PhotoDiode connect on anaglog pin3
int averaged_sensor_value = 0;

bool led_state = 0;
int i = 0;
int pkt_n_point = 80;  // make sure this value is similar to python side

int received_data = 0;
int ping = 0;

bool toggle = true;

struct Packet {
  unsigned long time_m;
  int left; 
  int right;
  bool LED_state;
};

void setup() {
  
  // initialize digital LED pin as an output.
  pinMode(9, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(right_LED, OUTPUT);
  pinMode(left_LED, OUTPUT);

  // set the LEDs high or low
  digitalWrite(9, HIGH);
  digitalWrite(11, HIGH);
  digitalWrite(right_LED, LOW);
  digitalWrite(left_LED, LOW);

  // start seria comm
  Serial.begin(250000);       //  setup serial
//  Serial.write("\n");         // 1 byte

}

void loop() {

  if (Serial.available() > 0){
    received_data = Serial.read();

    if (received_data == 68){ // ord('D') - Display
      digitalWrite(9, LOW);
      digitalWrite(11, LOW);
      for (i=0; i < pkt_n_point; i++){
        averaged_sensor_value = (analogRead(analogPin_Left) + analogRead(analogPin_Right)) / 2;
        Packet data = {micros(), averaged_sensor_value};
        Serial.write((byte*)&data, 6); // 4 + 2
      }
    }

    else if (received_data == 84){ // ord('T') - Tracking
      toggle = !toggle;
      if(toggle){
        digitalWrite(right_LED, LOW);
        digitalWrite(left_LED, HIGH);
        }
      else{
        digitalWrite(right_LED, HIGH);
        digitalWrite(left_LED, LOW);
        }
      Serial.write(toggle);  // Send the LED position
    }
    
    else if (received_data == 83){  // ord('S') - Total
      if (led_state){
        digitalWrite(right_LED, LOW);
        digitalWrite(left_LED, HIGH);
        led_state = 0;
        }
      else{
        digitalWrite(right_LED, HIGH);
        digitalWrite(left_LED, LOW);
        led_state = 1;
        }
      
      for (i=0; i<pkt_n_point; i++){
        Packet data = {micros(), analogRead(analogPin_Left), analogRead(analogPin_Right), led_state};
        Serial.write((byte*)&data, 9); // 4 + 2 + 2 + 1
        }
      }
      
      else if (received_data == 82){ // ord('R') - connection response
        Serial.write("yes");
        }
    }
}
