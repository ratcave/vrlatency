int analogPin_Left = 2;         // Left PhotoDiode connect on anaglog pin2  
int analogPin_Right = 3;        // Right PhotoDiode connect on anaglog pin3  
int win_len = 700;

int data[700] = {0};

#define FASTADC 1

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

void setup() {

  #if FASTADC
     // set prescale (s=1, c=0) using table from https://forum.arduino.cc/index.php?topic=6549.0
     cbi(ADCSRA,ADPS2) ; 
     sbi(ADCSRA,ADPS1) ;
     cbi(ADCSRA,ADPS0) ;
  #endif
  
  Serial.begin(250000);       //  setup serial
  Serial.write("\n");         // 1 byte
}

void loop() {
  for (int ind=0; ind<win_len; ind++){
    data[ind] = analogRead(analogPin_Left);
  }
   Serial.write((byte*)data, sizeof(data));
}
