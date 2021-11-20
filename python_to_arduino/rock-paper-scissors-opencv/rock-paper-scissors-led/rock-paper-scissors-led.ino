int me = 8;
int pc = 9;

int x;

void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
 pinMode(me, OUTPUT);
 pinMode(pc, OUTPUT);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 if(x == 9) {
  digitalWrite(pc, HIGH);
  digitalWrite(me, LOW);
 }
 if(x == 8) {
  digitalWrite(me, HIGH);
  digitalWrite(pc, LOW);
 }
 if(x == 0) {
  digitalWrite(me, HIGH);
  digitalWrite(pc, HIGH);
 }
}
