#define firePin D7

bool toggle = false;

int fireRocket(String command) {
    toggle = true;
    return 0;
}

void setup() {
    pinMode(firePin, OUTPUT);
    Particle.function("ToggleFire", fireRocket);
}

void loop() {
    System.sleep(SLEEP_MODE_CPU); // Put system on Low Power Mode
    if (toggle == true) {         // Transistor Gate ON
        digitalWrite(firePin, HIGH);
        delay(4000);              // Pin active for 4 seconds
        digitalWrite(firePin, LOW); // Turn off transistor gate
        toggle = false;
    }
}