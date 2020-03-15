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
    System.sleep(SLEEP_MODE_CPU);
    if (toggle == true) {
        digitalWrite(firePin, HIGH);
        delay(4000);
        digitalWrite(firePin, LOW);
        toggle = false;
    }
}