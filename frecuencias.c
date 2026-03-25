const int signalPin = 9;
float freqHz = 1.0;
unsigned long halfPeriodMs = 500;
unsigned long lastToggle = 0;
bool pinState = false;

void updateFrequency(float f) {
  if (f <= 0) return;
  freqHz = f;
  halfPeriodMs = (unsigned long)(500.0 / freqHz);
  if (halfPeriodMs < 1) halfPeriodMs = 1;
}

void setup() {
  pinMode(signalPin, OUTPUT);
  digitalWrite(signalPin, LOW);
  Serial.begin(115200);
  updateFrequency(1.0);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "1") updateFrequency(1.0);
    else if (cmd == "5") updateFrequency(5.0);
    else if (cmd == "10") updateFrequency(10.0);

    Serial.print("FREQ=");
    Serial.println(freqHz);
  }

  unsigned long now = millis();
  if (now - lastToggle >= halfPeriodMs) {
    lastToggle = now;
    pinState = !pinState;
    digitalWrite(signalPin, pinState ? HIGH : LOW);
  }
}
