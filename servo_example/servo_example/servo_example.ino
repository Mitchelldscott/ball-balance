#define S1 11
#define V1 12
#define G1 13

double signal;

double t;

void setup() {
  // put your setup code here, to run once:
  pinMode(G1, INPUT);
  pinMode(V1, OUTPUT);

  digitalWrite(V1, HIGH);
  digitalWrite(G1, LOW);

  pinMode(S1, OUTPUT);
  Serial.begin(9600);
  signal = 0.0;
  t = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  signal = int(((cos(t) + 1) / 2) * 200) + 55;
  analogWrite(S1, signal);
  
  t += 0.01;

  if (t > 6.26)
    t -= 6.26;

  Serial.print(signal);
  Serial.print("\t"); Serial.println(t);
  delay(10);
}
