#include "FIFO_Queue_2D.h"

#define P1 A0								// Blue 
#define P2 A1								// Green 
#define P3 A2								// Orange 
#define P4 A3								// Yellow 

// Estimated State
float X;
float Y;

// State histroy object
FIFO_Queue_2D queue(50);

// Measured values (for each pin)
int X1;
int X2;
int X3;
int X4;

int Y1;
int Y2;
int Y3;
int Y4;

// Noise from pins
int noiseX;
int noiseY;
int noise_tolerance = 20;

// Setup variables for timing handler
unsigned long t;
unsigned long t1;
unsigned long dumprate = 100;

bool is_contact = false;

void dumpState()
{
	/*
	*	Dump the state of the hardware
	* prints position estimate, all measured pins and noise calculation
	* Meant for debug only
	*/

	if (is_contact)
	{
		Serial.println("Axis\tPosition\tMeasurements\t\t\tNoise"); 
		Serial.print("X:\t\t");
		Serial.print(X); Serial.print("\t\t"); 
		Serial.print(X1); Serial.print("\t");
		Serial.print(X2); Serial.print("\t");
		Serial.print(X3); Serial.print("\t");
		Serial.print(X4); Serial.print("\t");
		Serial.println(float(noiseX)/2048.0);
		Serial.print("Y:\t\t");
		Serial.print(Y); Serial.print("\t\t");
		Serial.print(Y1); Serial.print("\t");
		Serial.print(Y2); Serial.print("\t");
		Serial.print(Y3); Serial.print("\t");
		Serial.print(Y4); Serial.print("\t");
		Serial.println(float(noiseY)/2048.0);
	}
  //queue.print();
  Serial.println("---");
	
}

void interval(unsigned long *last_t, unsigned long interval, void (*f)())
{
	t = millis();
	if (t - *last_t > interval)
	{
		*last_t = t;
		f();
	}
}

void setPins(int p1, int p2, int p3, int p4)
{
	pinMode(p1, INPUT);
	pinMode(p2, INPUT);
	digitalWrite(p2, LOW); // Tri-state

	pinMode(p3, OUTPUT);
	digitalWrite(p3, HIGH);

	pinMode(p4, OUTPUT);
	digitalWrite(p4, LOW);
}

void readPins(int *m1, int *m2, int *m3, int *m4, int *noise)
{
	*m1 = analogRead(P1);
	*m2 = analogRead(P2);
	*m3 = analogRead(P3);
	*m4 = analogRead(P4);
	*noise = *m2 + *m4;
}

void updateState()
{
	// Update X first (priority)
	setPins(P1, P2, P3, P4);
	readPins(&X1, &X2, &X3, &X4, &noiseX);
  float c = X1 - 575.0;
  if (c < 0)
    c *= 2.2;
	X = float(c / 400.0) * 100.0;
  delay(1);
	// Update Y
	setPins(P3, P4, P1, P2);
	readPins(&Y1, &Y2, &Y3, &Y4, &noiseY);
	Y = float((Y1) / (1024.0)) * 100.0;

	// Update contact
	is_contact = (Y <= 100 && Y >= -100) && (X <= 100 && X >= -100);
}

void setup()
{
	Serial.begin(9600);
	t = millis();
	t1 = t;
}

void loop()
{
	interval(&t1, dumprate, &dumpState);
	updateState();
  if (is_contact)
    queue.insert(X, Y);
	delay(100);
	
}








